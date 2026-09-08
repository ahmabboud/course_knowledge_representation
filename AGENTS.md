# AGENTS.md, building a lecture in this repository

You are writing an interactive teaching lecture as a **single static HTML file**. Read this whole file before you write anything. When it and your own instincts disagree, this file wins.

---

## 0. What this repository is

```
index.html                     Course index. Every finished lecture is linked here.
design-system.html             The design system + live gallery of all 12 components.
                               Open it. It is the visual and behavioural reference.
AGENTS.md                      This file.
manifest.webmanifest           PWA manifest.
sw.js                          Service worker (offline cache).
.nojekyll                      Required, without it GitHub Pages hides _template.html.
.github/workflows/pages.yml    Deploy. There is no build step.
assets/
  lu.css                       The entire design system. ~1,200 lines, sectioned.
  lu-deck.js                   The runtime. Frames slides, wires every component.
  sparql-lite.js               Offline SPARQL engine. Only needed for query sandboxes.
  icon.svg, icon-maskable.svg  PWA icons.
  img/                         Instructor-supplied screenshots and plots.
scripts/
  audit-deck.js                Paste into the console. Measures what static checks cannot.
lectures/
  _template.html               COPY THIS. Your starting point, always.
  kr-session-03.html           The worked example. Read it before writing your own.
```

No framework. No bundler. No npm. No CDN at runtime except the two webfonts. A lecture opened straight from the filesystem must work.

---

## 1. The workflow

1. **Read `design-system.html`** in a browser. It has every component live, with the markup.
2. **Read `lectures/kr-session-03.html`.** It is 21 slides and uses all nine layouts and all twelve components. Imitate its structure.
3. **Copy `lectures/_template.html`** to `lectures/<course-slug>-session-NN.html`.
4. Fill in `<title>`, the `<meta name="description">`, and the `<body data-*>` attributes.
5. Write the slides. Delete template slides you do not need; never delete the deck frame (`.deck > .deck__stage > .slide`).
6. Add a card for the lecture in `index.html` (copy an existing `<a class="lu-lecture-card">`).
7. **Verify by measuring, not by reading.** Serve it over http, open with a
   `?cb=` cache-buster, clear this deck's `lu:` localStorage keys, reload, and
   paste `scripts/audit-deck.js` into the console. Fix everything it reports.
   Then by hand: `→` through every slide and every build step, `?`, `O`, `/`,
   `S`, and **print preview with Handout on**. Nothing may throw.

   A query sandbox can also be verified away from the browser, which is faster
   and works before the page is deployed:

   ```
   node -e "global.window={}; require('./assets/sparql-lite.js');
     const {parse,query}=global.window.LUSparql; /* feed it the templates */"
   ```


---

## 2. Non-negotiable rules

| Rule | Why |
|---|---|
| **No `<style>` blocks. No new colours, fonts or sizes in inline styles.** | One stylesheet is the only reason a dozen lectures look like one course. Layout nudges using existing `var(--lu-*)` tokens are fine; a new design decision belongs in `lu.css`. |
| **Nothing below 20px** on a slide. | Projection at the back of a room. `--lu-t-caption` is the floor. |
| **Two grounds per deck:** paper (default) and `.slide--night` (title + dividers). `.slide--tint` marks a change of activity. | Three backgrounds reads as three different decks. |
| **Every slide: `data-label`, `data-section`, `data-minutes`, `<template data-notes>`.** | Contents, search, presenter view, pacing and the handout all read these. A slide missing one is broken, not merely incomplete. |
| **Max ~5 bullets, ~60 characters per line.** | If it does not fit, it is two slides. |
| **Unique `data-qid` per graded component,** session-prefixed (`s3-q1`). | It is the `localStorage` key and the self-check row identity. A collision silently overwrites a student's answer. |
| **Every answer option gets a rationale** (`.lu-mcq__why`), correct ones included. | The rationale is the teaching. The verdict is bookkeeping. |
| **No emoji, no gradient backgrounds, no invented icons.** | Type and palette carry the tone. |
| **Never draw a photograph or a screenshot as SVG.** Ship a `.lu-figure__ph` placeholder saying exactly what capture goes where. | An honest placeholder is useful. A hand-drawn fake screenshot is a lie that ships. |

---

## 2b. Nine traps this system has already shipped

Every one of these was invisible in the HTML and obvious under measurement.
`scripts/audit-deck.js` checks all of them. Read this before you get clever.

| Trap | What happened | Rule |
|---|---|---|
| **`display` beats `[hidden]`** | `.lu-mcq__why{display:block}` and later `[data-walk-step]{display:grid}` both outranked the UA `[hidden]` rule. Rationales kept their space; all five walkthrough steps rendered stacked. | Never set `display` on something the runtime hides. If you must, ship a `[hidden]{display:none}` companion in the same commit. |
| **Grid children need a column** | `.lu-mcq__opt` is `44px 1fr`. `.lu-mcq__why` had no `grid-column`, landed in the 44px column, and rendered one word per line at 44x462 instead of 691x54. | Any child of a grid with a narrow first column gets an explicit `grid-column`. |
| **`aspect-ratio` ignores available height** | `.lu-board` is `width:100%` plus `aspect-ratio`, so inside a height-constrained walkthrough it computed a height taller than the space and covered the caption bar. | In a height-constrained box, set an explicit height and `aspect-ratio:auto`. The canvas is a fixed 1600x900, so a fixed px height is deterministic. |
| **Source order decides ties** | `.lu-svg{height:auto}` is declared after `.lu-board__edges{height:100%}` at equal specificity, so edge layers kept the wrong height and arrows drifted off the diagram. | When two single-class rules fight, raise specificity deliberately (`.lu-board > .lu-board__edges`). |
| **The tall column sets the height** | Trimming a two-column slide by shortening the short column changes nothing. | Measure both columns first. Cut the tall one. |
| **Print is a second layout** | `.slide` is `height:900px; overflow:hidden` and the print block overrode neither, while `.lu-print-notes` is a flex child *inside* the slide. The handout silently cut 237px off every slide with notes. | Any change to slide sizing must be checked in print preview with Handout on. |
| **You may be measuring a stale page** | GitHub Pages serves HTML with `max-age=600`, so a plain `fetch` inside the service worker was answered by the HTTP cache. Hours were spent measuring a version that was not on the server. | Always verify with a `?cb=` cache-buster, and confirm the version you think you loaded. |
| **A sandbox that runs and returns nothing** | A `.lu-query` seeded with a find-the-violation query over data containing no violation. It parsed, executed, reported "0 rows" and read to the student as a broken button. | Run the seeded query through the engine and confirm it returns rows. Any query you *suggest* in a caption too. |
| **Em dashes and stray characters** | 74 em dashes across the decks, five of them emitted by the runtime into visible UI (the study-mode toast, a popover aria-label, the presenter label, the empty result cell). | This course does not use em or en dashes as punctuation. Non-ASCII on a slide must be a deliberate symbol. The audit checks both. |

Two measurement rules that cost real time:

- **Units.** `getBoundingClientRect()` is in scaled screen pixels;
  `clientHeight` / `scrollHeight` are in unscaled canvas pixels. Mixing them
  inflates every number by `1/scale`. Pick one and say which.
- **State.** A restored answer or an open reveal makes a slide taller. Clear
  the deck's `lu:` localStorage keys before measuring a baseline, and measure
  the revealed state separately. That is the state you teach in.

## 3. Anatomy of a lecture file

```html
<body
  data-deck-id="kr-s03"          <!-- REQUIRED. localStorage namespace. Unique per lecture. -->
  data-course="Knowledge Representation"   <!-- left side of every slide header -->
  data-session="Session 3 of 8"            <!-- right side of every slide header -->
  data-duration="180"                      <!-- planned contact minutes -->
  data-app-root="../"                      <!-- path from THIS file to repo root -->
  data-unit="Lebanese University · MSc">   <!-- footer line -->
```

`data-app-root` is how the service worker is found. A file in `lectures/` uses `"../"`; a file at the root uses `"./"`. Get it wrong and offline support silently does not register.

```html
<div class="deck"><div class="deck__stage">
  <section class="slide" data-label="…" data-section="…" data-minutes="8">
     …your content, written as if the header and footer already exist…
     <template data-notes><p>What to say.</p></template>
  </section>
  …
</div></div>
<script src="../assets/sparql-lite.js"></script>   <!-- only if you use .lu-query -->
<script src="../assets/lu-deck.js" defer></script>
```

The runtime wraps your slide content in `.slide__body` and injects the header, footer and print-notes block. **Write content only.** Two exceptions, both needing `data-chrome="none"`: the title slide and section dividers, which supply their own `<div class="slide__body">`.

---

## 4. Slide layouts, in the order a session uses them

Copy these from `kr-session-03.html` rather than composing from scratch.

1. **Title**, night, no chrome. Lockup, eyebrow, `.lu-display`, lead, meta row.
2. **Recap / where we are**, paper. `.lu-pipeline` showing the stage you are at, plus two callouts: what they brought, what is still missing.
3. **Objective**, tint. `.lu-statement` with the deliverable, plus `.lu-layers` for the time budget.
4. **Section divider**, night, no chrome. One per part.
5. **Concept**, paper. `.lu-split--wide-left`: argument left with term popovers, evidence right (code, diagram, reveal). This is most of the lecture.
6. **Walkthrough**, paper. One per session, on the single hardest idea.
7. **Check / drill**, tint. After each concept block.
8. **Lab brief**, paper. Numbered steps, deliverable callout.
9. **Wrap**, then **self-check**, tint, then paper. Always the last two slides.

Rhythm target for 180 minutes: about 20 slides, a divider before every part, a check question after every concept block, and never more than four consecutive paper slides.

---

## 5. Component cheat sheet

Full live examples with markup: `design-system.html` §8. Graded components are marked ⓖ, they need a `data-qid` and appear in the self-check.

| Component | Class | Notes |
|---|---|---|
| Term popover | `.lu-term` on a `<button type="button">` | `data-term`, `data-kind`, and either `data-def="…"` or a nested `<template>` for rich content. Becomes an inline note in study mode. |
| Click to reveal | `.lu-reveal` > `.lu-reveal__btn` + `.lu-reveal__panel[hidden]` | Runtime wires `aria-expanded`/`aria-controls`. Forced open in study mode and in handouts. |
| Multiple choice ⓖ | `.lu-mcq` | `data-answer="b"`, `data-label`, `data-fb-correct`, `data-fb-wrong`; each `.lu-mcq__opt` has `data-key` and a hidden `.lu-mcq__why`. |
| Walkthrough | `.lu-walk` | Children `[data-walk-step]` with `data-caption` (HTML ok) and `data-caption-short`. Arrow keys when focused. |
| Progressive build | `data-build="1"` on any element | Same number = same step. `data-build-style="dim"` or `"hold"`. Deep-links as `#/12/2`. |
| Code block | `.lu-code` + `<pre><code>` | `data-name` is the filename chip. `data-run="js"` adds a sandboxed Run. Highlight with `.tok-kw/-str/-num/-com/-fn/-var` spans, there is no highlighter library. |
| Drag to order ⓖ | `.lu-sort` > `.lu-sort__list` > `.lu-sort__item[data-rank]` | Correct order is ascending `data-rank`. Up/down buttons are injected, do not remove them, they are the keyboard path. |
| Fill the blank ⓖ | `.lu-blanks` with `input.lu-blank` | `data-answer="TBox\|T-Box"`, `data-label` (accessible name). Matching ignores case and punctuation. |
| Compare wipe | `.lu-compare` + two `.lu-compare__pane--a/--b` | `data-a`, `data-b` label the sides. **Registered content only:** two states of the same thing, sharing baselines (identical first line, identical structure). Two different prose passages garble at the seam, use `.lu-split` for those. Prints as two columns. |
| Query sandbox | `.lu-query` | `<template data-data>` Turtle, `<template data-query>` seed query. Escape `<` and `>` as `&lt;` `&gt;` inside templates. Needs `sparql-lite.js`. |
| Timed poll ⓖ | `.lu-poll` | `data-seconds`, `data-answer`. Local answers only, a static page cannot aggregate votes. Instructor tallies the room manually. |
| Self-check ⓖ | `<div data-score></div>` | One per deck, on the last slide. Finds every `data-qid` by itself. |

Other useful pieces: `.lu-pipeline`, `.lu-layers`, `.lu-board`/`.lu-node`/`.lu-edge`, `.lu-matrix`, `.lu-table`, `.lu-defs`, `.lu-callout` (+`--concept`, `--neutral`), `.lu-card`, `.lu-tag`, `.lu-list` (+`--num`, `--check`, `--tight`), `.lu-figure`, `.lu-statement`.

---

## 6. Speaker notes are part of the deliverable

`<template data-notes>` feeds the presenter view and the printed handout. Write for the instructor, not the transcript:

- how long to spend, and what to cut if you are behind;
- the question the room will ask, and the answer;
- the misconception the slide exists to break;
- the blocker that will appear at minute 20 of the lab, and its cause.

Do not restate the slide. If a note only repeats what is visible, delete it and write something useful.

---

## 7. Graphics: three routes, in order

1. **CSS primitives** (`.lu-pipeline`, `.lu-layers`, `.lu-board`, `.lu-matrix`, `.lu-table`). Semantic, restyleable, highlightable by `data-state`. Try these first, every time.
2. **Inline SVG using the kit classes** (`.lu-svg` with `.s-fill-red`, `.s-stroke`, `.s-hair`, `.s-label`, `.s-mono`). For genuinely geometric relationships. Never hardcode a hex value. Add `role="img"` + `<title>`, or `aria-hidden="true"` when a caption carries the meaning.
3. **Image placeholder** (`.lu-figure__ph`). For anything photographic or captured. State the exact path (`assets/img/<slug>.png`), the size, and what must be visible in the shot.

---

## 8. Accessibility, concretely

The target is WCAG 2.2 AA. The system meets most of it structurally; these are the parts you can break:

- Give every `input.lu-blank` a `data-label`.
- Give every `[data-walk-step]` a `data-caption-short`.
- Never remove the injected up/down buttons from a `.lu-sort`, they are the keyboard equivalent of dragging (SC 2.5.7).
- Never say "the green one" or "the red box". Name the thing.
- Decorative SVG gets `aria-hidden="true"`; meaningful SVG gets `role="img"` and a `<title>`.
- Do not add a `tabindex` above 0, and do not remove focus outlines.
- Keep the skip link as the first element in `<body>`.

Known gap, stated honestly: a scaled fixed canvas cannot satisfy SC 1.4.10 reflow. The printed handout is a conforming alternative. **Study mode is not, yet**, it sets `.lu-selfstudy` but the deck stays `overflow:hidden`, so a long slide is still clipped and expanding every reveal makes it worse. Do not claim unqualified AA for the slide view, and do not claim study mode as the reflow alternative until it scrolls.

---

## 9. Runtime behaviour you can rely on

`→`/`Space` next step or slide · `←` back · `↓`/`↑` skip builds · digits jump · `Home`/`End` · `O` contents · `/` search · `T` timer · `S` study mode · `P` presenter view · `F` fullscreen · `?` shortcuts · `Esc` close.

- Deep links: `#/12` and `#/12/3`.
- State in `localStorage` under `lu:<deck-id>:*`, position, answers, query drafts, study mode. **Never write outside your own namespace, and never clear the whole store.**
- Presenter view is the same file with `?presenter=1`, synchronised over `BroadcastChannel`.
- `window.LUDeck.go(n)` jumps to slide *n* (1-indexed) if you need it from the console.

---

## 10. Deployment

Push to `main`. The workflow uploads the repository as-is. Nothing to build, nothing to configure beyond enabling Pages with "GitHub Actions" as the source.

Two things that will bite you:

- **`.nojekyll` must exist.** Jekyll excludes files beginning with `_`, so without it `lectures/_template.html` 404s.
- **Asset links are versioned** (`assets/lu.css?v=1.0.2`). When you edit anything in `assets/`, bump that query string in all four HTML files and in the `SHELL` list in `sw.js`, one find-and-replace. Skip it and returning visitors keep the old stylesheet. Assets are otherwise served stale-while-revalidate, so it self-heals on the load after next; the version bump makes it immediate.

---

## 11. Adding a component to the system

Only when a genuine teaching interaction has no home. Then, in order:

1. Add the CSS to the right numbered section of `assets/lu.css`, using existing tokens only.
2. Add an `init()` to `assets/lu-deck.js` and call it from `boot()`. Follow the existing shape: find nodes, inject the chrome the author should not have to write, wire ARIA, register with `register({qid, kind, label, slide, check})` if it is graded.
3. Handle study mode (expanded), print (expanded), and keyboard parity.
4. Add a live demo and the markup to `design-system.html` §8.
5. Add a row to the cheat sheet in §5 of this file.
6. Bump the `?v=` query on the asset links (see §10).

A component that is not documented in `design-system.html` does not exist, because the next agent will not find it.
