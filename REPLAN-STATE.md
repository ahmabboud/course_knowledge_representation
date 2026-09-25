# Open work and handoff, Knowledge Representation course

**Any new session or agent: read this file right after `PROGRESS.md`.**
The checklist below is the single to-do list. Tick an item (`[x]`) and add a
dated line to the log at the bottom in the same change as the work.
Last updated: 2026-09-24 (handoff checked; both repos clean and pushed;
session protocol added to the top of `AGENTS.md`).

Companion documents:

- `PROGRESS.md`: what is built, per session (status table reconciled
  2026-09-24).
- `COURSE-REPLAN.md`: the approved plan: audit findings, outlines for
  Sessions 3, 1, 2.
- `AGENTS.md` section 2c: the teaching standard; graphics route 0 for flow
  diagrams (`lu-flow`), the default for anything with arrows.
- `GLOSSARY.md`: plain definitions for every term in Sessions 1 to 6 (234
  terms). The slides link to it automatically (item 16).

Rules that always hold: never mark a session done in `PROGRESS.md` without
the instructor's explicit agreement; push to `main` at the end of each work
session, only after the audit is clean, never force push (Claude pushes
since 2026-09-24, see item 10; a push publishes the site through GitHub
Pages); never delete a file without asking; no
dashes in prose; audit every deck you touch before you stop (item 15); every
new term goes into `GLOSSARY.md` (item 16); commit messages carry no
`Co-Authored-By`, session link or other AI attribution (instructor's
standing preference). The start, during and end steps of every work
session are at the top of `AGENTS.md`. Running a lab end to end goes to a
Sonnet sub-agent with a self-contained brief and a short report back, to
keep the main session's context clear (instructor's preference, 2026-09-24).

**Where to continue (2026-09-24, end of day):**

1. **Session 2 (item 8):** built, audited and pushed; waits for the instructor's
   review. Ask for it first. If changes are asked, edit
   `scripts/deckgen-s2/part_*.py`, run `python3 scripts/deckgen-s2/build.py`,
   audit (item 15), glossary check (item 16), push (item 10).
2. **Then Session 3, parts 3 to 6 (item 2),** with items 3 to 5. Reuse the
   Session 1 and 2 generator pattern (`scripts/deckgen-s1/kit.py`). Convert
   `demos/session-03-ontology/sample-shipments.ttl` individuals to the IRI
   convention (`AGENTS.md` 2d) while there.
3. **Later:** item 9 (Sessions 4 to 6 visual pass; Session 4 examples move to
   the 2d IRIs), item 18 (syllabus alignment question).

**Settled decisions a new session must not reopen:** tool rule (2c rule 5:
concept first, one slide per tool, no slide for trivial tools, video only for
complex GUI tools); timing (2c rule 7: about 180 minutes, about 2 hours slides
and 1 hour lab, **a guide, not a rule**; `data-minutes` realistic); animation
(section 7 route 0: grey blocks, colour only for states, animate whatever
unfolds in steps); labs are **individual**, the capstone is the **team
project** and its divider says so; **labs are not collected or graded**,
they exist for understanding and the capstone, and follow the lab standard
(`AGENTS.md` 2e, reference `demos/session-02-rdf-sparql/`); IRIs (2d); Fuseki runs from
`demos/fuseki/Dockerfile` (Apache 5.5.0 release, no login, localhost only).

**How the work was run (2026-09-24):** edits and git on the instructor's Mac
through the device shell; Playwright audits, Java (Fuseki), Morph-KGC and
downloads in the cloud workspace, on copies. The Mac repo is the only source
of truth: never commit from a copy. Not yet run for real: the Docker build of
`demos/fuseki` (no Docker in the workspace; the instructor runs
`docker compose up -d` once) and the Ontop path of Session 5.

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

6. [x] **Done 2026-09-24, approved by the instructor.** **Decided yes (2026-09-24):** build a "Your project begins"
   part in Session 1 (about 4 slides, 15 minutes, before the lab brief:
   what you build, topic menu, team rules and deadline, rubric and
   milestones), as DSCAI module 1 does. Today the capstone is one callout on
   the wrap slide. Build it as part of item 7.
7. [x] **Done 2026-09-24, approved by the instructor** (46 slides, 185 minutes, audit clean at rest and revealed, glossary check clean; generator `scripts/deckgen-s1/`, numbers from `demos/session-01-environment-and-constraints/session1_facts.py`). **Full rebuild: more slides, more depth, more visuals.** The current
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

8. [ ] **Built 2026-09-24, awaiting the instructor's review** (42 slides, 173 minutes: lecture about 98, lab 61, discussion and wrap 14; audit clean; generator `scripts/deckgen-s2/`, sharing `deckgen-s1/kit.py`). The lab was rebuilt too and run end to end: see the log.  Full rebuild to the 2c standard, per `COURSE-REPLAN.md`.

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
    The helper only finds the token when `LebUniv/` itself is reachable. A
    Cowork session given only the `Knowledge Representation` folder cannot
    see it: request access to `LebUniv/`, then run git from the repo path
    under that mount (`.../mnt/LebUniv/Knowledge Representation/course_knowledge_representation`),
    where the helper's relative path resolves (confirmed 2026-09-24). Never
    read, print or copy the token, and never put it in a remote URL. On the
    iCloud mount `rm` of a lock file is refused: move it aside instead, and
    move a lock found under `.git/refs/` out to `.git/stale-locks/`, because
    a renamed file left inside `refs/` reads as a bogus ref and breaks the
    next fetch ("did not send all necessary objects").
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
18. [ ] **Syllabus alignment (asked 2026-09-24, no answer yet).** The syllabus
    still places RDF versus property graphs in Session 1 and gives the lab 85
    minutes. Ask the instructor whether to update it to match the rebuilt
    Sessions 1 and 2.
19. [ ] **Bring every lab to the lab standard (`AGENTS.md` 2e).** Session 2
    is done (2026-09-24). Session 1 is approved but its lab slides and
    README still say "deliverable", "committed" and "due tonight": change
    only with the instructor's agreement. Sessions 3 to 6: apply 2e when
    each is rebuilt (items 2 and 9): parts A, B (write your own, with a
    checker), C, and "take it to your team project".
20. [ ] **Keep the lecture skill in step.** `.claude/skills/lu-lecture-builder/SKILL.md`
    is a copy of the instructor's account skill of the same name, committed
    so every session and device can use it (Claude Code loads it
    automatically). When the skill changes, update both copies, or note the
    drift in the log. It is course-agnostic, so it also belongs in the
    template repo; copy it there when that repo is next touched.
21. [x] **Done 2026-09-24, with the instructor's agreement.** **Session 1 rate band sentence, precision.**
    Session 1's rate band walkthrough says "1,370 orders fall in gaps like
    this; 1,364 of them on this one lane". All 1,370 are on that lane
    (V444_1, DTD, PORT04 to PORT09): 1,364 in the 2.51 to 70.50 kg hole and
    6 in 0.01 kg slivers between bands (`demos/session-02-rdf-sparql/reference-outputs/q6-versions-oxigraph.txt`).
    Session 1 is approved, so change `scripts/deckgen-s1/part_c.py` only
    with the instructor's agreement.

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
- 2026-09-24: Session 1 rebuilt with a generator, `scripts/deckgen-s1/` (build.py plus four parts; rebuild with `cd scripts/deckgen-s1 && python3 build.py ../../lectures/kr-session-01.html`). 46 slides, 185 minutes: opening 11, data 25, meaning 20, architecture 15, profiling 30, project 15, lab 65, wrap 4. Thirteen lu-flow diagrams, eleven animated, neutral blocks, states only. Every number from a real run: `session1_facts.py` writes `reference-outputs/s1-facts.txt`. Real screenshots: `assets/img/s1-ydata-alerts.png` (ydata-profiling, Brunel OrderList) and `s1-openrefine-clusters.png` (OpenRefine 3.8.7, Order City, 3 clusters, all different cities). The old deck's plant and port example ("41 of 200 pairs, three transhipments") was not real and is replaced: 22 of 209 pairs, 0 exceptions. RDF against property graphs moved to Session 2 as planned. Glossary: 17 terms added (grain, order line, one to many, clustering, fingerprint, CRF, DTD, VMI, GTFS, OCDS...). `lu-flow.js` v1.2.1 in both repos: optional per diagram `flags` to rename a state badge, and wider badges so text is not clipped.
- 2026-09-24: instructor review, round 1: the project divider now says plainly it is the team project; a lab title slide added; the lab is individual work (no pairs), inventories compared as a room.
- 2026-09-24: Session 1 approved and closed by the instructor. Next: Session 2 (item 8).
- 2026-09-24: Session 2 rebuilt, deck and lab. Lab bugs found and fixed: `convert_to_rdf.py` linked each order to its Origin Port as if it were a plant, and `neo4j_comparison.py` did the same; the question set had no carrier or port links, so the syllabus's multi-hop question could not run. New lab: full OrderList plus PlantPorts, ProductsPerPlant and FreightRates (rate bands as blank nodes), 135,841 triples, 5 named graphs, a small RDFS schema; `common/iri.py` now separates words (`ul:`, #) from things (`https://ul.edu.lb/kr/id/`, /). Seven questions, all run for real on Fuseki 5.5 and Oxigraph; Neo4j 5.26 comparison; `rdfs_entailment_demo.py` (owlrl). Real findings on the slides: Q6 took 172 s with NOT EXISTS and 2.3 s rewritten; 9,023 orders by type against 9,215 with a subclass path, in both SPARQL and Cypher. Screenshots `s2-fuseki-query.png`, `s2-neo4j-browser.png`. Sandbox now uses nine real orders. Note for the instructor: `docker-compose.yml` uses the `stain/jena-fuseki` image, which is old and not maintained by Apache; the lab was verified with Fuseki 5.5 run directly.
- 2026-09-24: instructor accepted Session 2's timing and asked to fix the two open points. (1) IRI convention: written into `AGENTS.md` 2d; Session 5's mappings (`mapping_template.rml.ttl`, `mapping.obda`) now mint `https://ul.edu.lb/kr/id/carrier/erp/...` and `.../purchase-order/erp/...`; the RML path was re-run with Morph-KGC 2.10.0 on the same seed rows (SQLite in place of Postgres): 19 triples, po99 still fails the Session 4 shapes as before. The Ontop mapping was changed the same way but not re-run (no Ontop here). Still to convert when rebuilt: Session 3's `sample-shipments.ttl` individuals (`ul:carrier-dhl`...) in item 2, Session 4's slide examples in item 9. (2) Fuseki: `demos/docker-compose.yml` now builds `demos/fuseki/Dockerfile` (Apache's own Fuseki 5.5.0 release, SHA512 checked, Java 21, TDB2 dataset /kr, no login, published on 127.0.0.1 only) instead of the old `stain/jena-fuseki` image. The container command was verified outside Docker (load and all queries); the Docker build itself was not run here.

- 2026-09-24: Handoff check. Both repos clean and in sync with GitHub; stale `.git` lock files removed; credential helper confirmed portable (relative path to `LebUniv/.github-token`). "Where to continue" rewritten with the settled decisions; item 18 added.
- 2026-09-24: Session 2 lab gaps fixed, at the instructor's request. Instructor's decision: labs are individual, not collected, not graded; they are for understanding and the capstone. Added part B, "write your own": `my_queries.sparql` (three questions: GROUP BY, FILTER NOT EXISTS, HAVING), `check_my_queries.py` (right or not yet, with hints; Oxigraph or Fuseki), `solutions/`; run on Oxigraph: PLANT03 ships 8,541 of 9,215 orders; 8 of 11 served ports never ship; 16 of 46 customers order from more than one plant; the wrong Y3 without DISTINCT gives 44 (`reference-outputs/my-queries-check.txt`). README rewritten (why, expect at each step, parts A to C, understood if, take to your project, notebook tip, Windows Docker notes). Deck: no deliverable or due wording, IRI task is now test the course scheme and sketch one for your project, lab checkpoints 25/45/55; still 42 slides, 173 minutes, audit clean (known noise only), glossary check clean. `demos/README.md`: stale status lines replaced, Docker needs on Windows, JDK row clarified; Neo4j now published on 127.0.0.1 only. New `AGENTS.md` 2e (lab standard) and `PROMPT.md` aligned. Item 19 added.
- 2026-09-24: session protocol written down, at the instructor's request, after a sync miss. A Cowork session reported its 2026-09-20 deck edits (commit `1147f0a`: two Session 2 diagrams, question-first part dividers in Sessions 1 to 3, bolded key claims) as lost. They were in history all along: the 2c generator rebuilds of Sessions 1 and 2 replaced those HTML files, and the edits had never been recorded here, so no later session knew of them. Their intent is already covered by `AGENTS.md` 2c (visual first, bold and define at first use, why then how). The old `kr-session-03.html` still carries them until item 3 replaces it. Added the start, during and end checklist to the top of `AGENTS.md`, the no AI attribution rule and the Cowork token note (item 10) here, and the same protocol to the instructor's `lu-lecture-builder` skill. No deck touched, so no audit run.
- 2026-09-24: the `lu-lecture-builder` skill committed to the repo at `.claude/skills/lu-lecture-builder/SKILL.md`, identical to the account copy, so sessions on any device can use it; `AGENTS.md` start step points at it. Item 20 added to keep the two copies in step.
- 2026-09-24: Session 2 lab reviewed at the instructor's request (Cowork; run end to end on Oxigraph on a copy; Fuseki and Neo4j not rerun, no Docker there). Every README number reproduced. Checked against the whole repo before fixing: the 1,370 rate band gap is already explained in Session 1, and `DISTINCT`, `HAVING` and subqueries work as in SQL, which the syllabus assumes, so no new slide. Fixed: (1) `queries.sparql` Q6 now states it counts orders on a priced lane (8,361, the 854 CRF orders have no rates, as in Session 1) and carries the `FILTER NOT EXISTS` version the README told students to read but which was in no file; run as written it gives 1,370, and without its `FILTER EXISTS` line 2,224 (`reference-outputs/q6-versions-oxigraph.txt`); the README asks why. (2) `common/iri.py` and `common/README.md` no longer say the room overwrites the scheme (contradicted `AGENTS.md` 2d and the discussion slide). (3) New `named_graphs.py` reproduces the named graphs slide numbers from `brunel.trig` (same as the recorded file); README step 2 runs it. (4) `check_my_queries.py` ignores column order (a correct Y1 with swapped columns was "not yet"). (5) README: Q1 and Q7 expected rows, Q6 row says "on a priced lane", one line pointing Part B at SQL and at Q4 and Q6 as models. No deck touched, so no audit. Item 21 added. Session 2 still awaits the instructor's review (item 8).
- 2026-09-24: item 21 done, instructor agreed ("correct if there is any wrong sentence"). Checked every Session 1 sentence about the rate bands; only the Step 3 caption of "Rule or exception?" was wrong. It now reads "1,370 orders fall in gaps, all on this lane: 1,364 in this one, 6 in 0.01 kg gaps between two bands." Edited in `scripts/deckgen-s1/part_c.py` and rebuilt (the generator reproduced the committed deck byte for byte before the edit; the rebuild changes only that caption). `session1_facts.py` now also prints the gap orders by lane and the 6 outside the big gap, and `reference-outputs/s1-facts.txt` was regenerated (one added line, nothing else changed). Glossary check clean. Not audited yet: Playwright's browser download is blocked in the Cowork workspace, so the audit runs on the live page after the push. The new caption (150 characters) is shorter than two captions in the same deck that already audit clean.
- 2026-09-24: Session 1 audited live after the push (`66daae6`, GitHub Pages, cache-buster, `lu:` state cleared, `scripts/audit-deck.js`): 46 slides, no overflow at rest or revealed, no hidden leaks, no collisions. Only the known noise (`tinyText` on kbd, inline code and the title lockup) and accented real city names on the OpenRefine slides (Los Ángeles, Vitória, Mâcon). Step 3 of "Rule or exception?" shows the new caption in full on two lines. Cowork can push: connect `LebUniv/` and run git from the repo under that mount (item 10 corrected; skill updated to match).
- 2026-09-24: **skill drift (item 20).** The account copy of `lu-lecture-builder` now says to connect the parent folder and push instead of concluding a push is impossible (end step 4, plus a trap row). Cowork cannot write inside `.claude/`, so the repo copy `.claude/skills/lu-lecture-builder/SKILL.md` is one change behind. The instructor, or a Claude Code session, copies the account version over it.
- 2026-09-24: drift resolved. The instructor copied the account skill into `.claude/skills/lu-lecture-builder/SKILL.md`; checked byte for byte identical before committing. Standing note for item 20: Cowork can never write inside `.claude/`, so a skill change made in Cowork always needs the instructor (or Claude Code) to copy it into the repo.
- 2026-09-24: Session 2 lab code run end to end on a clean copy, fresh virtual environment with the pinned lab packages (pandas 2.3.3, rdflib 7.6.0, pyoxigraph 0.5.11, requests 2.34.2, neo4j 6.3.1, matplotlib 3.10.0, owlrl 7.6.2), after the instructor approved the slides. Ran: `convert_to_rdf.py` (135,841 triples, 5 named graphs, 13 sample triples, 6 s), `named_graphs.py`, `run_queries.py oxigraph` (all seven answers as in the README), `check_my_queries.py` (blank 0 of 3, solutions 3 of 3), `rdfs_entailment_demo.py` (9,023 then 9,216), `lab_walkthrough.py` (falls back to Oxigraph, skips Neo4j cleanly). Fixed: (1) `convert_to_rdf.py` wrote `sample/order.nt` in a different line order each run, so git showed a changed file after every conversion; the lines are now sorted (same 13 triples). (2) With Fuseki not running, `run_queries.py` and `load_fuseki.py` stopped with a raw traceback and `check_my_queries.py fuseki` told the student "the query did not run" three times, as if their queries were wrong; all three now print one line saying Fuseki is not answering and how to start it or use Oxigraph. (3) An unused import in `run_queries.py`. Not run here: Fuseki, Neo4j and the Docker build (the Cowork workspace has only Java 11 and cannot download Fuseki, Neo4j or Python 3.12), and the full `requirements.txt` install (needs Python 3.12; `networkx==3.7` does not install on 3.10). Those need one run on the instructor's Mac.
