# Open work and handoff, Knowledge Representation course

**Any new session or agent: read this file right after `PROGRESS.md`.**
The checklist below is the single to-do list. Tick an item (`[x]`) and add a
dated line to the log at the bottom in the same change as the work.
Last updated: 2026-09-24.

Companion documents:

- `PROGRESS.md`: what is built, per session (status table reconciled
  2026-09-24).
- `COURSE-REPLAN.md`: the approved plan: audit findings, outlines for
  Sessions 3, 1, 2.
- `AGENTS.md` section 2c: the teaching standard; graphics route 0 for flow
  diagrams (`lu-flow`), the default for anything with arrows.
- `GLOSSARY.md`: plain definitions for every term in Sessions 1 to 6 (215
  terms). The slides link to it automatically (item 16).

Rules that always hold: never mark a session done in `PROGRESS.md` without
the instructor's explicit agreement; push to `main` at the end of each work
session, only after the audit is clean, never force push (Claude pushes
since 2026-09-24, see item 10; a push publishes the site through GitHub
Pages); never delete a file without asking; no
dashes in prose; audit every deck you touch before you stop (item 15); every
new term goes into `GLOSSARY.md` (item 16).

**Where to continue:** **Session 1 first** (instructor, 2026-09-24: the course has not started and Session 1 is taught first). Next open items are **6 and 7**. Session 3 (item 2) resumes after Session 1 is closed.
Items marked `[x]` are done; everything else is still open.

---

## Open items, in order

### A. Session 3 rebuild (in progress)

1. [x] ~~Protégé guide deck~~ **Replaced 2026-09-24 (instructor's decision):**
   no standalone guide. Students learn the basics from the YouTube series
   (<https://www.youtube.com/watch?v=CduRWyyL3q8&list=PLNohRKRAHaszTV3puqFM9yXDXnEqjS6Fd>),
   and the Session 3 lab part gets **one slide**, "Protégé on our files: four
   things the video does not show": (a) open the file inside `workspace/` so
   imports resolve (screenshot 16), (b) the Asserted / Inferred dropdown shows
   what the reasoner added (06, crops z-h and z-b), (c) the ? button explains a
   red class (09b), (d) Save as a new file, never over v0. Fold this into
   item 2. Section 5 below and `guide1.py` are kept only as source material.
2. [ ] **Session 3 deck, parts 3 to 6** (reasoner, reuse and BFO, profiles,
   lab and wrap), outline in section 3. Draw every diagram with `lu-flow`
   (the reasoner proof already exists as a spec:
   `scripts/proto-diagrams/spec.json`). Parts 1 and 2 were built before
   lu-flow existed: convert their arrow diagrams too.
3. [ ] Replace `lectures/kr-session-03.html` with the new deck, then copy it to
   the template repo's `lectures/kr-session-03.html` (it is the reference
   deck there).
4. [ ] `demos/session-03-ontology/closed_world_demo.py` (the SQLite foreign
   key demo that part 2's notes refer to).
5. [ ] Rewrite `demos/session-03-ontology/README.md` as honest steps: which
   tab, what the student should see, pointing at the guide deck.

### B. Session 1

6. [ ] **Decided yes (2026-09-24):** build a "Your project begins"
   part in Session 1 (about 4 slides, 15 minutes, before the lab brief:
   what you build, topic menu, team rules and deadline, rubric and
   milestones), as DSCAI module 1 does. Today the capstone is one callout on
   the wrap slide. Build it as part of item 7.
7. [ ] **Full rebuild: more slides, more depth, more visuals.** The current
   deck audits clean since 2026-09-23 but is the old standard: 15 content
   slides, only 4 led by a picture, 112 minutes, no `lu-flow`. Target: about
   33 content slides, every concept slide led by a picture (`AGENTS.md` 2c),
   every arrow diagram in `lu-flow`, new Part 2 on the supply chain and the
   two datasets, profiling concepts each shown on real data, real
   ydata-profiling and OpenRefine screenshots. Full outline and the target
   table: `COURSE-REPLAN.md` section 5. Session about 180 minutes: about
   120 of slides, about 60 of lab; time budget per part in `COURSE-REPLAN.md`
   section 5. The old deck's planned 112 minutes ran about 40 in a dry run,
   so `data-minutes` must be realistic. **Decided 2026-09-24:** Jupyter gets
   no slide (trivial tool). Profiling is taught as a concept first, then
   one slide introduces ydata-profiling; clustering is taught first, then
   one slide introduces OpenRefine (`AGENTS.md` 2c rule 5, revised).
   Animations and diagrams follow the settled `lu-flow` rules (graphics
   route 0), no new diagram styles. Deadline on the project slides: teams
   and topic locked **before Session 2 starts** (`PROJECT-REDESIGN.md`),
   no date. Screenshots: Claude captures the ydata-profiling report and
   the OpenRefine clusters from real runs on the instructor's Mac.

### C. Session 2

8. [ ] Full rebuild to the 2c standard, per `COURSE-REPLAN.md`.

### D. Sessions 4 to 6

9. [ ] Visual pass: redraw arrow diagrams with `lu-flow`, apply 2c. After
   Sessions 1 to 3.

### E. Housekeeping

10. [x] **Commits and pushes.** Since 2026-09-24 Claude pushes both repos
    (KR and the template) at the end of each work session, after a clean
    audit. How: a GitHub token saved by the instructor at
    `LebUniv/.github-token` (outside every repo, never committed), read by a
    repo local credential helper (`git config credential.https://github.com.helper`).
    Never force push. After pushing, confirm with
    `git ls-remote origin refs/heads/main` that GitHub matches `HEAD`, then
    delete leftover `.git/*.lock` and `tmp_obj_*` files. If the push fails
    (token expired or revoked), tell the instructor; do not work around it.
    2026-09-24: both repos pushed and confirmed (KR `9b61704`, template
    `a7e4bed`).
11. [x] `PROGRESS.md` status table reconciled with the repository
    (2026-09-24, at the instructor's request). Facts only, no session marked
    done.
12. [ ] `index.html` has cards only for Sessions 1 to 4. Add 5, 6 and the
    guide deck once the instructor confirms they are ready.
13. [ ] DSCAI's design system is behind on purpose (instructor's choice,
    2026-09-23): no `lu-flow`, and missing two poll fixes
    (`.lu-poll__bars[hidden]`, timer hidden once bars show). Port when asked.
14. [ ] Keep `assets/lu.css`, `assets/lu-flow.js`, `assets/lu-deck.js` and `assets/lu-glossary.js`
    identical between this repo and the template repo. They were identical
    on 2026-09-23. Change both, or note the drift here.
15. [ ] Standing check, not a one-off: run `scripts/audit-deck.js` with
    Playwright on every deck you touch, at rest and fully revealed
    (`scripts/deckgen-s3/auditnew.py` does it). Two findings are known noise:
    `tinyText` on `<kbd>` (13px) and inline code (19.8px) from design-system
    defaults, and a U+2212 minus drawn by the pace timer.

16. [x] **Automatic glossary (done 2026-09-24).** Instructor's goal: anyone can
    understand any slide. `GLOSSARY.md` is the single source;
    `scripts/build-glossary.py` turns it into `assets/glossary.js`;
    `assets/lu-glossary.js` (loaded with `defer` BEFORE `lu-deck.js`) makes the
    first use of each term on every slide a clickable definition (study mode S
    shows them inline). Wired into Sessions 1 to 6 and `_template.html`, also
    in the template repo (with a sample glossary). Link rules live at the top
    of `build-glossary.py`: `SKIP` (plain English, never linked),
    `ONCE_PER_DECK` (common words, once per deck from their session on),
    `ALIASES`. A slide or element can opt out with `data-glossary="off"`.
    Standing rule: after editing any deck run
    `python3 scripts/check-glossary.py` (lists undefined acronyms; must print
    nothing), then `python3 scripts/audit-all.py` (audits all six decks; serve
    the repo root on port 8660 first). Audit on 2026-09-24: all clean except
    two findings that predate the glossary and belong to item 8: Session 2
    slides 9 and 20 overflow when their answers are revealed (99px and
    184px). Known small miss: in Session 4 the first "edge" linked is the
    plain English "edges of the spec".
17. [ ] Future decks (Sessions 7 and 8): add their terms to `GLOSSARY.md` as a
    `## Session N` table while building them.

### Not course material

- `lectures/proto-diagrams.html` is the `lu-flow` demo (design system v1.2),
  not linked from `index.html`. Rebuild with `scripts/proto-diagrams/builddemo.py`.

---
## 1. Decisions the instructor approved (2026-09-22)

| Question | Decision |
|---|---|
| Scope | Rebuild Sessions 3, 1 and 2, Session 3 first |
| Length | Let Session 3 run about 230 minutes (about 30 content slides) |
| Tool guide | A standalone guide deck plus the session deck |
| Screenshots | Real screenshots, captured from the instructor's own Protege |

---

## 2. What is already done and verified

### Data and tooling (committed earlier, working)

- `demos/data/fetch_data.py` downloads DataCo and the Brunel supply chain
  workbook directly, checks hashes, exports the Brunel sheets to CSV.
- `demos/session-03-ontology/robot_report.py` runs ROBOT 1.9.10 from
  `~/tools/robot.jar` with `--catalog workspace/catalog-v001.xml`, reasons,
  writes an explanation when a class is unsatisfiable, then reports on the
  source file (34 findings, not the 515 false alarms the reasoned file gave).
- `demos/session-03-ontology/fetch_ontologies.py` copies the three lab files
  into `workspace/` and registers the catalog entry.

### Session 3 lab files (real, reasoner verified)

| File | Role |
|---|---|
| `scro-extension-v0.ttl` | Lab starting point. Contains a real modelling error on purpose. |
| `scro-extension-reference.ttl` | The fixed version. Uses `ul:suppliedBy` and `ul:hasComponent`. |
| `sample-shipments.ttl` | Three shipments and two carriers, imports the fixed file through the catalog. |
| `workspace/catalog-v001.xml` | Maps `https://ul.edu.lb/kr/scm#` to the fixed file. |
| `reference-outputs/` | Recorded runs: ELK and HermiT explanations, two realization outputs. |

Verified reasoner story: ELK finds one impossible class
(`Order for a sole-sourced good`), HermiT finds two (adds
`Sole-sourced component`), the fix removes both, and realization over
`sample-shipments.ttl` infers `At-risk shipment` for shipments 4472 and 4473.

### Protege screenshots (21 files, pushed)

In `assets/img/`, named `s3-protege-NN-*.png`, all captured from the
instructor's Protege 5.6 on 2026-09-22:

| File | Shows |
|---|---|
| 01 open-in-current-window | The "open in current window?" prompt |
| 02 active-ontology | Active ontology tab, metrics (4,819 axioms, 254 classes) |
| 03 entities-classes | Entities tab, collapsed class tree |
| 04 class-primitive | At-risk shipment in v0: SubClass Of only, no Equivalent To |
| 05 reasoner-menu | Reasoner menu with ELK 0.6.0 ticked |
| 06 asserted-inferred-dropdown | The Asserted / Inferred dropdown open |
| 06b status-reasoner-active | "Reasoner active" in the status bar |
| 07 inferred-view | Inferred tree: yellow background, red owl:Nothing, Shipment moved under TraceableResourceUnit |
| 08 red-class-selected | The red class selected, Equivalent To owl:Nothing |
| 09 explanation-window | The full explanation window, three justifications |
| 09b explanation-1 | Explanation 1 alone, six lines |
| 10 hermit-two-red | HermiT: two red classes |
| 11 hermit-explanation-1 | HermiT explanation for Sole-sourced component |
| 12 edit-restriction | The class expression editor with the fix typed in |
| 13 out-of-sync | "Reasoner state out of sync with active ontology" |
| 14 synchronize-menu | Reasoner menu with Synchronize reasoner |
| 15 fixed-no-red | After the fix: no red class, the order sits under PurchaseOrder |
| 16 sample-imports | sample-shipments imports resolved to the local file by the catalog |
| 16b sample-metrics | Metrics for the ABox file (8 individuals) |
| 17 realization-instances | Direct instances (inferred) of At-risk shipment: 4472 and 4473 |
| 18 inferred-type-4473 | Shipment 4473: no asserted type, one fact, inferred type in yellow |

Nothing in Protege was saved: the two test edits were undone, so both `.ttl`
files on disk are unchanged.

### New Session 3 deck, parts 1 and 2

Built with the generator in `scripts/deckgen-s3/` (see section 4). Twenty
slides, 74 minutes, audit clean. Covers: recap, objectives, one word three
numbers, an ontology in one picture, the class tree, two kinds of arrow,
two layers, then sets, some, only, and/or/not/disjoint, counting,
domain and range (with a real SQLite foreign key error to contrast),
SubClassOf versus EquivalentTo, property characteristics, plus one multiple
choice and one drill.

---

## 3. Session 3 outline as planned on 2026-09-22 (status: see open items)

1. **Guide deck** `lectures/guide-protege.html`: one step per slide, built
   around the 21 screenshots. No tool before its guide, so this comes before
   the lab part of the session deck.
2. **Session 3 deck parts 3 to 6**:
   - Part 3, the reasoner: open world, the three jobs (consistency,
     classification, realization), the red class, reading an explanation,
     what Asserted versus Inferred actually shows.
   - Part 4, reuse: BFO continuant and occurrent, dependence, the real reuse
     trap that produced our bug, competency questions, alignment.
   - Part 5, profiles: EL versus DL, the real ELK 1 versus HermiT 2 result.
   - Lab part and wrap: brief, the guided steps, reading the 34 line report,
     licensing, discussion, glossary slide, self check.
   Then replace `lectures/kr-session-03.html`.
3. **`demos/session-03-ontology/closed_world_demo.py`**: the SQLite foreign
   key demo referenced in the deck notes.
4. **Rewrite `demos/session-03-ontology/README.md`**: honest steps that point
   at the guide, say which tab to look at and what to expect.
5. **Audit** with Playwright, then one commit, pushed, and no
   change to `PROGRESS.md` status without asking.
6. **Then Session 1, then Session 2**, per `COURSE-REPLAN.md`.

---

## 4. How to rebuild the deck

The generator lives in `scripts/deckgen-s3/`:

    build.py     assembles a deck file from parts
    common.py    slide, divider, defbox, callout, figure, code
    svgkit.py    SVG helpers, all diagrams are inline SVG, arrowheads are polygons
    part1.py     slides 1 to 9
    part2.py     slides 10 to 20
    auditnew.py  Playwright audit, needs a local web server on port 8643
    shoot.py     screenshots of chosen slides for eyeballing

Rebuild:

    python3 build.py /path/to/lectures/kr-s3-new.html part1 part2 part3 ...

Design constraints that the audit enforces: no `<style>` blocks, no new
colours or fonts, nothing below 20px, every slide needs data-label,
data-section, data-minutes and notes, unique data-qid, no dashes in prose.
Canvas is 1600x900, content width 1448, split columns 688, wide split
803 and 573, and about 540px of height below the heading.

---

## 5. Plan for the Protégé guide deck (superseded 2026-09-24, see item 1)

Kept as source material only. Do not build this deck.

The next task is the guide deck `lectures/guide-protege.html`. Its plan is
fixed and its screenshots are already in `assets/img/`. Build it with the
generator in `scripts/deckgen-s3/`, adding `guide1.py` and `guide2.py` next to
`part1.py`, and a builder that writes the deck head with
`data-deck-id="kr-guide-protege"`.

Slide list, 24 screens, sections Getting ready, The window, The reasoner,
Changing the file, Individuals, Reference:

1. Title, night slide.
2. What Protege is: editor, ontology file, reasoner. Define ontology,
   reasoner, Protege. It is not a database.
3. Setup: `python3 fetch_ontologies.py`, what lands in `workspace/`, define
   catalog file.
4. Step 1, open the file. Screenshot 01. Warn: open the copy inside
   `workspace/`.
5. Step 2, the window map. Screenshot 04, five numbered places.
6. Which tab answers which question. Table plus screenshot 02, define axiom
   and import.
7. Step 3, search by name, cmd F, read the Found in column, the breadcrumb.
8. Step 4, reading one class. Crop z-a-primitive-desc, define SubClass Of
   versus Equivalent To.
9. Divider, part 2 of the guide.
10. Step 5, choose and start a reasoner. Screenshots 05 and 06b.
11. Step 6, Asserted versus Inferred, the key screen. Crops z-h-asserted-tree
    and z-b-inferred-tree, plus screenshot 06.
12. What the colours mean: yellow, white, red, the orange triangle. Define
    owl:Nothing.
13. Step 7, when a class turns red. Crops z-i-nothing-branch and
    z-c-red-equivalent.
14. Step 8, ask the reasoner why. The ? button, screenshot 09b, define
    justification.
15. Step 9, a second reasoner finds more. Crop z-j-hermit-branch, screenshot 11.
16. Divider, part 3 of the guide.
17. Step 10, edit one axiom. Screenshot 12 plus a Manchester syntax table
    (some, only, exactly, and, or, not).
18. Step 11, synchronize. Screenshots 13 and 14, crop z-k-no-nothing.
19. Step 12, saving. Save as a new name, never overwrite v0, inferred axioms
    are not saved, Export inferred axioms as ontology.
20. Opening a file that imports another. Screenshot 16, define ABox and TBox.
21. The payoff, realization. Crops z-l-instances-wide and z-g-inferred-type.
22. Troubleshooting, eight rows.
23. Guide glossary, ten terms.
24. End, night slide, pointing at the Session 3 deck.

Screens 1 to 9 are written: `scripts/deckgen-s3/guide1.py` (it already links
the YouTube series on screen 2). Screens 10 to 24 go in a new `guide2.py`.




---

## Log

### 2026-09-23

- Session 1 lab: verified working by the instructor. `PROGRESS.md` updated.
- Session 1 deck: eleven overflowing slides fixed, audit clean at rest and
  fully revealed. Still due for its full rebuild.
- The instructor recommends this Protege fundamentals video series for
  students: <https://www.youtube.com/watch?v=CduRWyyL3q8&list=PLNohRKRAHaszTV3puqFM9yXDXnEqjS6Fd>
  (The AI & DS Channel). Linked from `demos/session-03-ontology/README.md`
  ("Learn Protege first"). The guide deck must link it on screen 2 and on
  the last screen.
- Open question for the instructor: add a full "Your project begins" part
  to Session 1, as DSCAI module 1 does, instead of the single callout on
  the wrap slide.
- Diagram tool prototype: `lectures/proto-diagrams.html` shows the same
  step-animated diagram built with an in-house component (`assets/lu-flow.js`)
  and with React Flow (`assets/proto-reactflow.*`). Measured differences on
  its slide 4. Waiting on the instructor's choice before any deck uses either.
- **Decided 2026-09-23: diagrams use lu-flow** (design system v1.2). React Flow
  rejected and its files removed. Colour now names the ontology layer (blue
  ours, teal reused, plum BFO, green individual) and the reasoner's result
  (amber inferred, red impossible). Rule in `AGENTS.md` graphics route 0;
  gallery in `design-system.html` section 7; demo `lectures/proto-diagrams.html`.
  Every diagram in the Session 3 rebuild, and later Sessions 1 and 2, uses it.
- Same day: lu-flow and the diagram colours were also added to the shared
  template repo (`Interactive HTML teaching slides system`: lu.css, lu-flow.js,
  design-system.html, AGENTS.md, sw.js, lectures/_template.html) and to KR's
  `lectures/_template.html`. DSCAI deliberately left unchanged.
- Same day: the template repo's stale `kr-session-03.html` (Sep 7 copy, 11
  overflowing slides) was replaced with this repo's current one, and the two
  poll fixes were ported, so both `lu.css` copies are identical. Template
  decks audit clean.
- Same day: this file restructured into the open-items list above so any new
  session can pick up from it.
- 2026-09-24: both repos committed locally (not pushed). Instructor decisions:
  the Protégé guide becomes the YouTube series plus one course-specific slide
  in the Session 3 lab (item 1); Session 1 gets a "Your project begins" part
  (item 6). Next: item 2, Session 3 parts 3 to 6.
- 2026-09-24: automatic glossary built and wired into all decks (item 16); GLOSSARY.md extended to Sessions 4 to 6; lu.css v1.3.0 (auto term style) in both repos.
- 2026-09-24: items 7 and `COURSE-REPLAN.md` made explicit about Session 1's planned growth (slide count, depth, visuals); the replan's stale "proposed" status corrected to approved.
- 2026-09-24: back on track check against the repository and GitHub. PROGRESS status table and "What's next" rewritten from facts (item 11). Found: template repo has three unpushed commits (item 10); old Protégé guide plan marked superseded.
- 2026-09-24: Claude now pushes (instructor's decision). Token at `LebUniv/.github-token`; credential helper set in both repos; template's three pending commits pushed; both repos confirmed equal to GitHub.
- 2026-09-24: instructor decisions for Session 1: build it before finishing Session 3; tools rule revised (concept first, one slide per tool, no slide for trivial tools, video only for complex GUI tools), recorded in `AGENTS.md` 2c rule 5; project deadline stated as before Session 2.
- 2026-09-24: session length corrected by the instructor: about 180 minutes (about 2 hours of slides, about 1 hour of lab), flexible per session; slide count is not the goal, time distribution is. Old Session 1 dry run: slides about 40 minutes, lab about 60. Time budget per part added to `COURSE-REPLAN.md` section 5; `AGENTS.md` 2c rule 7 updated.
- 2026-09-24: animation rules settled for the rebuilds (both repos, `AGENTS.md` graphics route 0 and `design-system.html`): animate wherever an idea unfolds in steps, not one per session; before an ontology exists, neutral blocks and only states carry colour.
