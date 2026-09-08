repo: ahmabboud/course_knowledge_representation
branch: main
upstream template: ahmabboud/LebUniv_Course_Template @ `2322f1a`

## Last sync

date: 2026-09-07
commits: `537820e` (initial), `68599d9` (defect fixes)
status: `537820e` is pushed and live. **`68599d9` is committed locally and not
yet pushed.** Run `git push origin main`.
direction: this repository is DOWNSTREAM of the template. The stylesheet,
runtime and authoring contract were authored in `LebUniv_Course_Template`.

### `68599d9` fixes three defects that belong upstream

Diagnosed against the live site. All three are in `assets/` and affect every
deck built on this system, including the `kr-session-03` reference lecture,
which shows the same symptoms.

| # | File | Defect | Effect |
|---|---|---|---|
| 1 | `lu.css` | `.lu-mcq__why` set `display:block` with no `[hidden]` companion rule, so the UA `[hidden]` rule lost | Every unrevealed rationale still occupied space. MCQ and poll slides rendered 4 to 5 times taller than the slide: 1,440px and 1,398px of overflow here, 859px and 1,234px in session 3 |
| 2 | `lu.css` | A `.lu-board` inside `.lu-walk__view` is `width:100%` plus `aspect-ratio`, so it derived a height taller than the space available | The diagram overlapped the walkthrough caption bar by 90px here and 78px in session 3. Height now leads, width follows, with a print override |
| 3 | `lu-deck.js` | On reload the poll set `data-verdict="correct"` on whatever the student had answered, ignoring `data-answer` | A student restoring a wrong answer saw it confirmed as right. Now marks `data-picked` and leaves correctness to the reveal |

**These three fixes should be ported to `LebUniv_Course_Template`.** Until they
are, every new course seeded from the template inherits all three.

Also in `68599d9`: 46 content trims across 14 slides of session 1, and the
`&mdash;` entities removed from the walkthrough captions. Asset query strings
bumped to `v=1.0.3` in all four HTML files and in `SHELL` in `sw.js`.

### `NEXT` corrects a regression I introduced in `68599d9`

`68599d9` fixed the board overlap with `display:grid` on `[data-walk-step]`,
which is the same class of bug as defect 1 in the table above: it beat the UA
`[hidden]` rule, so all five walkthrough steps rendered stacked on top of each
other. `width:auto` also collapsed the board to 90x39px and crammed the nodes.

Corrected: no `display` is set on the step at all, `[hidden]` is asserted
explicitly, and the board keeps full width with `aspect-ratio:auto` and a fixed
`height:400px`. The stage is a fixed 1600x900 canvas, so a fixed height is
deterministic. A fourth defect surfaced doing this: `.lu-svg{height:auto}` is
declared after `.lu-board__edges{height:100%}` at equal specificity, so the
edge layer kept its own height and the arrows drifted off the diagram.
`.lu-board > .lu-board__edges` outranks it.

The session 1 walkthrough geometry was also rebuilt. Node positions are in
percentages and SVG paths are in viewBox units; I had set them independently by
eye and they did not correspond, so no edge met a node. Coordinates are now
computed from the node positions, and the viewBox is `0 0 1000 276` to match
the board's 1448x400 render so `preserveAspectRatio="none"` does not stretch
the labels. Verified: every edge endpoint lands within 0 to 16px of a node and
no two nodes overlap, on all five steps.

### Two more defects found by driving the deployed page

**Stale cache (the worst one).** GitHub Pages serves HTML with
`Cache-Control: max-age=600`. `sw.js` was network-first for documents, but its
plain `fetch(req)` is answered by the browser's own HTTP cache, so "network
first" quietly meant "stale first" and a student who once opened a lecture kept
that version through reloads. Measured directly: server had v1.0.3, the browser
rendered v1.0.2 with `transferSize: 0`. Fixed with `fetch(req, {cache:'no-store'})`,
`CACHE` bumped to `lu-slides-v3`, and registration with `updateViaCache:'none'`
plus an explicit `reg.update()`.

**`.lu-mcq__why` landed in the 44px key column.** `.lu-mcq__opt` is a
`44px 1fr` grid and the rationale is its third child, so with no explicit column
it fell into the narrow one and rendered **one word per line, 44px wide and
462px tall instead of 691x54**. Every revealed rationale in every MCQ and poll,
in every deck. Fixed with `.lu-mcq__why { grid-column: 2; }`. This, not long
prose, is what made the check-question slides explode.

### Slide overflow: what is real and what is left

A `.slide` is a fixed box with `overflow:hidden`, so content that does not fit
is cut with no scrollbar and no error. Measured on the deployed page, clean
localStorage, in canvas pixels against a 652px body:

| | clipped slides | worst |
|---|---|---|
| before | 11 | 559px |
| after the grid-column fix and the trims | 3 | 125px |

A runtime guard now logs every overflowing slide to the console at load, so
this fails loudly for the author instead of silently for the student.

**Auto-fit was tried and rejected.** Shrinking an overflowing body to fit needed
a scale below 0.78 on nine of ten slides, which pushes the 20px type floor under
16px. Evidence, not preference: the fix is less content, not smaller content.

**Known gap:** study mode (`S`) does not reflow. It sets `.lu-selfstudy` but the
deck stays `overflow:hidden`, and expanding every reveal makes clipping worse.
`AGENTS.md` claims study mode is the reflow-conforming alternative for WCAG
1.4.10. That claim is currently false. Fixing it is a design-system decision,
not made here.

### Print and handout were cutting content on every slide

`.slide` is `height:900px; overflow:hidden`, and the print block did not
override either. `.lu-print-notes` is appended as a flex child *inside* the
slide, so in handout mode the notes took their height out of the slide body and
the rest was clipped. Measured on slide 2: notes 276px, body squeezed to 376px
when it needed 613, so **237px of content was silently cut from the printed
handout**, mid-sentence.

Fixed in the print block: `height:auto; min-height:900px; overflow:visible`,
`break-inside:auto`, and `.slide__body { overflow: visible }`. On paper there is
no reason to lose text; a long slide simply runs onto a second sheet. Handout
mode now uses a named `@page lu-handout-page` at 1600x1500 so a slide and its
notes fit on one sheet. The printed walkthrough board is pinned to 400px to
match the screen geometry rather than 700px per step.

Verified by forcing the print media block to apply on screen and re-measuring
all 22 slides: content cut went from every slide with notes to **zero slides**.
Stylesheet parses clean (tinycss2: 433 top-level rules, 0 errors, 21 rules in
the print block, both `@page` rules present).

### Verified how

Components were exercised directly on the live page: MCQ, fill-in-the-blank,
drag-to-order, poll, reveals, term popovers, the compare wipe, code copy and
run, progressive builds and the self-check all function correctly. The two
`lu.css` fixes were injected into the live page and re-measured before being
written to the file. **The content trims have not yet been measured against a
live render** and should be re-checked after this commit deploys.

## Screen map

| Repo path | Built from |
|---|---|
| `index.html` | template, narrowed to this course |
| `lectures/kr-session-01.html` | `Knowledge Representation - Syllabus.docx`, Session 1 |
| `lectures/kr-session-03.html` | template worked example, same syllabus, Session 3 |
| `lectures/_template.html`, `design-system.html`, `assets/*` | template, unchanged |
| `AGENTS.md`, `PROMPT.md` | template, unchanged |

## Sessions still to build

2, 4, 5, 6, 7, 8. Source of truth is
`../Knowledge Representation - Syllabus.docx` and its `syllabus-source.json`.
Use the brief in `PROMPT.md` and build against `AGENTS.md`.

## Notes

- Asset links carry `?v=1.0.2`. Bump in every HTML file and in `SHELL` in `sw.js`
  when anything in `assets/` changes.
- Enable Pages with **GitHub Actions** as the source before the first push, or
  the workflow will run and fail on the deploy step.
- `.nojekyll` must stay. Without it Jekyll hides `lectures/_template.html`.
- Session 1 slide 16 asserts the maintenance status of eight libraries as of
  September 2026. Re-check every row before teaching it.
- `<html class="lu-deck-page">` on both lectures is inherited from the template
  and is not defined in `lu.css`. Harmless, but it is dead markup upstream.
