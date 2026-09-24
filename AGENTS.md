# AGENTS.md, building a lecture in this repository

You are writing an interactive teaching lecture as a **single static HTML file**. Read this whole file before you write anything. When it and your own instincts disagree, this file wins.

**Before anything else:** read `PROGRESS.md` (what is built), then `REPLAN-STATE.md` (the open to-do list, decisions, and where every file lives). Update both in the same change as your work.

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

## 2c. Teaching standard: visual first, every term defined (approved 2026-09-22)

Written after an instructor review found Sessions 1 to 3 hard to follow:
terms used before they were defined, mostly text slides, tools used in
labs with no guide, and datasets never shown. The full audit and the new
session outlines are in `COURSE-REPLAN.md`. These rules apply to every
deck built or rebuilt from now on.

| Rule | What it means in practice |
|---|---|
| **1. Visual first.** | Every concept slide leads with a picture that carries the idea: a diagram on the course's own entities (`.lu-board`, `.lu-pipeline`, `.lu-matrix`, inline SVG kit), an annotated **real** screenshot, or a real data table. The text explains the picture, never the reverse. A slide of bullets only is allowed for the glossary and the wrap, nowhere else. |
| **2. Define at first use, visibly.** | The first time a term appears in the course it is **bolded** and defined on the slide in one plain sentence, in a visible definition box (`.lu-callout--concept` labelled "Definition", or `.lu-defs`). A popover alone is not a definition, a student reading a printout never sees it. Later uses are linked automatically: add the term to `GLOSSARY.md`, run `python3 scripts/build-glossary.py`, and `assets/lu-glossary.js` makes its first use on every slide a clickable definition (no hand-written popover needed). `python3 scripts/check-glossary.py` must print nothing before you stop. No term is used before its defining slide. |
| **3. Why, then how, then example.** | Each part opens with the problem the idea solves (why), then the mechanism (how), then a worked example on the course's teaching slice. |
| **4. One cast of characters.** | The same small set of real entities from the course data appears on every slide of every session. Never invent a new order or carrier for one slide. |
| **5. Concept first, then one slide per tool.** | Revised 2026-09-24 by the instructor. Teach the concept first (what profiling is, what clustering is), then give the tool **one slide** with a real annotated screenshot, on our own files. A trivial or common tool (Jupyter, a terminal, a browser) gets no slide at all. A complex GUI tool gets a linked **video tutorial** plus that one slide on what is specific to our files (Protégé is the model). No standalone guide decks. |
| **6. Glossary slide.** | Every deck ends (before the self-check) with a glossary slide listing the terms it introduced, matching `GLOSSARY.md`. |
| **7. Depth.** | About 30 content slides per session (title, dividers, wrap and self-check not counted). The slide count is not the goal; content and time distribution are. A session is about 180 minutes (about 2 hours of slides, about 1 hour of lab), flexible per session: a heavy lab takes more (Session 3 was allowed about 230). Give every slide a realistic `data-minutes`: a dry run on 2026-09-24 delivered the old Session 1 (planned at 112 minutes) in about 40, so planned minutes had been inflated. Budget each part by what it teaches, then check the total against the session's lab. This replaces the 24 to 28 slide guidance in section 4. |
| **8. Real only.** | Every screenshot, number, error message and output comes from a real run, and the run is recorded under the lab's `reference-outputs/`. Screenshots live in `assets/img/`, named `s<N>-<what>.png`. Annotation marks (numbered circles, boxes) may be drawn onto a real capture; nothing else may be drawn. |

Plain English on slides: short sentences, no idioms, and name every acronym
the first time (ERP is "Enterprise Resource Planning, the system that holds
purchase orders").

## 2d. IRI convention (from Session 2, 2026-09-24)

One convention for every lab, deck and team project. It lives in code in
`demos/common/iri.py`; import it rather than writing IRIs by hand.

| What | Namespace | Example |
|---|---|---|
| Words: classes and properties | `https://ul.edu.lb/kr/scm#` (prefix `ul:`) | `ul:Order`, `ul:carriedBy` |
| Things: one IRI per real thing | `https://ul.edu.lb/kr/id/{kind}/{source}/{key}` | `.../kr/id/carrier/brunel/V44_3`, `.../kr/id/purchase-order/erp/po88` |

The source system is always part of a thing's IRI, and the key is used exactly
as the source writes it. Never a row number, never a name. Older examples of
the form `ul:carrier-dhl` (Session 3 sample individuals, Session 4 slides) are
converted when those sessions are rebuilt (REPLAN-STATE items 2 and 9).

## 2e. Lab standard (instructor's decisions, 2026-09-24)

**What a lab is for.** Labs are individual and are **not collected or
graded**. They exist for two things only: to make the session's concepts
concrete on the real data, and to prepare the team project (the capstone).
Graded work is the team project and its milestones, nothing else. So a lab
never says "deliverable", "hand in", "commit" or "due"; it says what the
student should understand and what to take to the project.

**Shape of every lab** (about 60 minutes, flexible, 2c rule 7):

| Part | What the student does | Rule |
|---|---|---|
| A · Build and observe | Runs the real scripts, in order, on the real data. | Every step states **Expect** (the exact number or file) and, where the concept shows, **Look at** or **Notice** (what to see and why). |
| B · Write your own | Writes 2 to 4 small things the lecture taught (a query, a shape, an axiom, a mapping), each practising one named concept. | A checker script says "right" or "not yet" with a hint. It compares answers, not code, so any correct solution passes. Solutions live in `solutions/`; the solutions and one common wrong answer are run through the checker and recorded in `reference-outputs/`. |
| C · Think | Answers 2 or 3 questions; at least one applies the idea to the student's **own project data**. | Feeds the closing discussion. |

Then two short lists: **"You understood this lab if you can say"** (3 or 4
lines, one per concept) and **"Take it to your team project"** (which file
is a template, which decision the team must make, what goes in the report).

**The lab README** (`demos/session-NN-*/README.md`), sections in this order:
why this lab exists; before you start (prerequisites, working directory,
services running, the fallback); Part A; Part B; Part C; optional (notebook
walkthrough, instructor demos); you understood this lab if; take it to your
team project. Reference implementation: `demos/session-02-rdf-sparql/`.

**Tools, Windows and macOS.**

- `demos/README.md` is the one place for installs. A new tool gets a row
  with the macOS and Windows commands and a way to verify it, and, if every
  student needs it, a check in Session 1's `smoke_test.py`. Give both
  commands wherever the platforms differ (PowerShell and a macOS shell).
- Every step that needs a service (Docker, Java) has a documented
  Python-only fallback, and the README says which concept the fallback
  loses. A broken laptop never stops the lab.
- Services publish on `127.0.0.1` only.
- Presentation: terminal scripts are the main path; the tool's own web page
  or app (Fuseki page, Neo4j Browser, Protégé) is for looking; an optional
  `lab_walkthrough.py` with `# %%` cells serves the projector (VS Code: Run
  Cell; JupyterLab: right-click, Open With, Notebook). No slide for trivial
  tools (2c rule 5).
- Concepts a lab needs are taught in the deck before the lab. A tool the
  students have not met gets one slide (or a video plus one slide if it is a
  complex GUI tool), per 2c rule 5.

**In the deck** (section 4): lab divider; lab brief with the three parts in
three lines, a "Nothing to hand in" callout and a fallback callout; at most
one tool slide; lab time with three checkpoints (end of A, B, C); the
closing discussion built on Part C. Speaker notes name the most common
blocker and the most common wrong answer.

**Before a lab counts as built:** every step run end to end, the checker run
on the solutions and on one wrong answer, outputs recorded in
`reference-outputs/` with the date, and anything that could not be run here
(a Docker build, a desktop app) written into `REPLAN-STATE.md`.

---

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
3. **Objective**, tint. `.lu-statement` with what students leave with (labs are not graded, 2e), plus `.lu-layers` for the time budget.
4. **Section divider**, night, no chrome. One per part.
5. **Concept**, paper. `.lu-split--wide-left`: argument left with term popovers, evidence right (code, diagram, reveal). This is most of the lecture.
6. **Walkthrough**, paper. One per session, on the single hardest idea.
7. **Check / drill**, tint. After each concept block.
8. **Lab brief**, paper. Parts A, B, C in three lines, "Nothing to hand in" callout, fallback callout (2e).
9. **Wrap**, then **self-check**, tint, then paper. Always the last two slides.

**Pacing: 3 to 4 minutes per content slide.** (For the depth target now in force, see section 2c, rule 7.) A three-hour session with 60
minutes of lecture wants 15 to 20 lecture slides, not 11. Counting dividers and
the wrap, a 180-minute session lands around 24 to 28 slides in total.

This number was wrong here for a while. The original guidance said "about 20
slides for 180 minutes", which works out at 6 to 7 minutes per slide. That asks
the instructor to talk for six minutes against six things on screen, and it
leaves the student with a study artifact holding a fraction of what was said.
It is also what pushed slides over the fixed slide box, because the fix for a
slide with too much on it is to split it, not to shrink it.

A useful signal while writing: count the *beats* on a slide, meaning the things
you can point at and talk to (a bullet, a code line, a table row, a callout, a
reveal, a walkthrough step). Aim for 5 to 8 beats on a 4-minute slide. Under
about 1 beat per minute and the slide is carrying more time than content.

Also: a divider before every part, a check question after every concept block,
and never more than four consecutive paper slides.

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

0. **Flow diagram** (`.lu-flow` + `assets/lu-flow.js`, design system v1.2, 2026-09-23). The default for anything with blocks and arrows, and for every step-animated explanation. Arrows name their blocks, so they cannot drift. Colour comes only from `kind` (`ours` blue, `reused` teal, `upper` plum, `individual` green, `literal`/`builtin` grey) and `state` (`inferred` amber, `impossible` red, `active` ring). Never pick a colour for looks: if two blocks share a colour, they share a layer. Reference: `design-system.html` section 7 and `lectures/proto-diagrams.html`. Do not hand-position new `.lu-board` diagrams. **When to animate** (instructor, 2026-09-24): put a flow in a `.lu-walk` wherever an idea unfolds in steps (data moving through the architecture, a profiling check, a rule catching an error, a proof); a structure that does not change stays a static flow. **Before an ontology exists** (Session 1, Session 2 before RDFS): blocks use the default `builtin` kind (grey, just omit `kind`), and only `state` carries colour (`active` ring, `impossible` red for a broken rule or bad data, `inferred` amber for something derived). Do not borrow the layer colours before Session 3 gives them their meaning.
1. **CSS primitives** (`.lu-pipeline`, `.lu-layers`, `.lu-matrix`, `.lu-table`). Semantic, restyleable, highlightable by `data-state`. For structures without arrows.
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
