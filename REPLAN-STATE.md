# Open work and handoff, Knowledge Representation course

**Any new session or agent: read this file right after `PROGRESS.md`.**
The checklist below is the single to-do list. Tick an item (`[x]`) and add a
dated line to the log at the bottom in the same change as the work.
Last updated: 2026-09-25 (Session 3 approved and in place in both repos).

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

**Where to continue (2026-09-25):**

1. **Session 6: done** (approved by the instructor 2026-09-25). One thing
   left: ask before deleting its old synthetic lab files
   (`build_heterodata.py`, `train_node_classification.py`,
   `train_link_prediction.py`, `train_pykeen.py`, `leakage_demo.py`,
   `tabular_baseline.py`, the folder's own `requirements.txt`).
2. **Session 7 rebuild, waiting for the instructor's review (item 9).** Lab
   built (`demos/session-07-access-layer/`, commit e5a9389) and deck rebuilt
   (`lectures/kr-session-07-new.html` from `scripts/deckgen-s7/`, 47 slides,
   179 minutes) with the real recorded numbers on the "Three settings" slide.
   `record_llm.py` run again on the Mac 2026-09-25 against the revised prompt
   rules (rules `ccb41f71`, model gemini-3.5-flash-lite): mean F1 0.792
   (schema), 1.000 (examples), 1.000 (repair) on 12 answerable questions; all
   three unanswerable questions refused correctly in every setting, no
   answerable question refused; two answerable questions were wrong in the
   schema-only setting, both fixed once examples were added. Live audit
   clean, glossary check clean, Docker image built. After approval: rename
   over `kr-session-07.html`, add its `index.html` card, mark PROGRESS row 7
   Done.
3. **Later:** Session 8 (defense day, no deck; `module-08-defense/`), item 18 (syllabus alignment
   question), items 12 and 19.

**Settled decisions a new session must not reopen:** Session 7 uses Gemini only, no Ollama or other provider (instructor, 2026-09-25); lab simplicity (instructor, 2026-09-25): slides never depend on the lab or its results, every slide example is complete on the slide; every Part B task mirrors a worked example of the same kind already shown on a slide or done in Part A, changing one thing; labs stay short and simple, one script per step with one expected result (to be added to `AGENTS.md` 2e once the coding agent's current edit of that file is pushed); visual variety (instructor, 2026-09-25, on approving Session 3: mix picture types across a deck, `AGENTS.md` 2c rule 9); tool rule (2c rule 5:
concept first, one slide per tool, no slide for trivial tools, video only for
complex GUI tools); timing (2c rule 7: about 180 minutes, about 2 hours slides
and 1 hour lab, **a guide, not a rule**; `data-minutes` realistic); animation
(section 7 route 0: grey blocks, colour only for states, animate whatever
unfolds in steps); labs are **individual**, the capstone is the **team
project** and its divider says so; **labs are not collected or graded**,
they exist for understanding and the capstone, and follow the lab standard
(`AGENTS.md` 2e, reference `demos/session-02-rdf-sparql/`); IRIs (2d); **Session 3
rebuild (instructor, 2026-09-24):** one cast, so Session 3's individuals become the
real Brunel orders and carriers of Sessions 1 and 2 (the "sanctioned carrier" is a
clearly labelled teaching flag on one anonymised carrier code, never a real company
name); lab Part B is 2 to 3 axioms the student writes, checked by a reasoner
(HermiT through owlready2, on the JDK students already have); Parts 1 and 2 are
converted (arrow diagrams to `lu-flow`, set pictures kept as SVG but in the layer
colours, stale references fixed); Fuseki runs from
`demos/fuseki/Dockerfile` (Apache 5.5.0 release, no login, localhost only).

**How the work was run (2026-09-24):** edits and git on the instructor's Mac
through the device shell; Playwright audits, Java (Fuseki), Morph-KGC and
downloads in the cloud workspace, on copies. The Mac repo is the only source
of truth: never commit from a copy. The Session 5 Ontop path was run on
2026-09-25; its reference output records the result and the two runner fixes.
(The Docker build of `demos/fuseki` was verified on the instructor's Mac on
2026-09-24.)

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
2. [x] **Done 2026-09-25, approved by the instructor** (48 slides, 231 minutes, audit clean, generator `scripts/deckgen-s3/`). **Session 3 deck, parts 3 to 6** (reasoner, reuse and BFO, profiles,
   lab and wrap), outline in section 3. Draw every diagram with `lu-flow`
   (the reasoner proof already exists as a spec:
   `scripts/proto-diagrams/spec.json`). Parts 1 and 2 were built before
   lu-flow existed: convert their arrow diagrams too.
3. [x] **Done 2026-09-25.** Replace `lectures/kr-session-03.html` with the new deck, then copy it to
   the template repo's `lectures/kr-session-03.html` (it is the reference
   deck there).
4. [x] **Done 2026-09-24.** `demos/session-03-ontology/closed_world_demo.py` (the SQLite foreign
   key demo that part 2's notes refer to).
5. [x] **Done 2026-09-24.** `demos/session-03-ontology/README.md` rewritten
   to `AGENTS.md` 2e (Parts A, B, C with Expect and Notice, optional,
   understood if, take to your project); no guide deck. Part A step 6
   (sample shipments in Protégé) waits on the Mac run in item 2's note.

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

8. [x] **Done 2026-09-24, approved by the instructor** (slides reviewed, lab run end to end on his Mac and on Oxigraph). **Built 2026-09-24** (42 slides, 173 minutes: lecture about 98, lab 61, discussion and wrap 14; audit clean; generator `scripts/deckgen-s2/`, sharing `deckgen-s1/kit.py`). The lab was rebuilt too and run end to end: see the log.  Full rebuild to the 2c standard, per `COURSE-REPLAN.md`.

### D. Sessions 4 to 6

9. [ ] **Full rebuild of Sessions 4, 5 and 6 (instructor, 2026-09-25),** not
   a visual pass: the same standard as Sessions 1 to 3 (generator, 2c, the
   Brunel cast and 2d IRIs, varied visuals per 2c rule 9, realistic minutes)
   and each lab brought to 2e (item 19). Session 4's lab is built from
   scratch (only a template today). **One session at a time:** Session 4
   deck and lab, instructor review and approval, then 5, then 6.

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
- 2026-09-24: Session 2 on the instructor's Mac. `docker compose up -d --build fuseki` built `kr-fuseki:5.5.0` from Apache's release (checksum OK) and started it; Cowork's browser pane reaches it at localhost:3030. Then `convert_to_rdf.py`, `load_fuseki.py`, `run_queries.py` (all seven answers as in the README, Q6 1.2 s; `reference-outputs/query-timings-fuseki.txt` refreshed) and `check_my_queries.py fuseki` (blank file, 0 of 3, connection fine) all ran; `sample/order.nt` stayed unchanged, so the sorting fix holds. `neo4j_comparison.py` failed with Neo4j `AuthError`: the Neo4j on 7687 was a stopped container the instructor had restarted by hand, not the compose service (`docker compose ps` listed only Fuseki), so it does not use `kr-labs-pw`. Fixed: the script now prints one line for "not answering" and for "wrong password", and the README step 5 has an "If Neo4j refuses the password" note (stop the other container, or recreate the compose volume). Neo4j comparison still to run once on the Mac.
- 2026-09-24: Neo4j comparison run on the Mac after stopping the hand-started container and starting the compose service (`docker compose up -d neo4j`, fresh `demos_neo4j-data` volume): 9,215 orders and 22 plant to port links loaded in 10.5 s; Q2, Q4, Q5a (9,023), Q5b (9,215) and the path query (3) all as expected; `reference-outputs/neo4j-comparison.txt` refreshed. Every step of the Session 2 lab has now run end to end on the instructor's Mac (Docker build, Fuseki, Neo4j) and on Oxigraph. The instructor has reviewed the Session 2 slides; item 8 stays open until he says Session 2 is approved.
- 2026-09-24: Session 2 approved and closed by the instructor (item 8). Next: Session 3 parts 3 to 6 (item 2).
- 2026-09-24: Session 3 rebuild started (item 2). Instructor decisions recorded under "Settled decisions": Brunel cast, reasoner-checked Part B, Parts 1 and 2 converted and recoloured. Known cost of the cast change: Protégé screenshots 16b, 17 and 18 show the old individuals (4472, 4473) and need recapturing on the Mac once the new sample file exists; placeholders until then.
- 2026-09-24: Session 3 lab, first stage (items 2, 4, 5, 19). `sample-shipments.ttl` now uses the course cast with 2d IRIs: shipments of Brunel orders 1447385217.7 (carrier V444_0), 1447291369.7 and 1447311670.7 (carrier V444_1, the labelled teaching flag "sanctioned"; 1447311670.7 has no type, so the domain makes it a Shipment). New `local_reasoner.py` runs HermiT (owlready2 0.51, added to `requirements.txt`) offline through the workspace catalog: v0 gives the two impossible classes HermiT gave in ROBOT (13 s), the reference file none (19 s), matching `reference-outputs/explain_v0_HermiT.md`. HermiT realization of the sample file took over 165 s here, so realization stays with ELK in Protégé or ROBOT. Part B built to 2e: `my_axioms.ttl` (Y1 disjoint Plant and Port, Y2 a defined class with and, Y3 some plus only), `check_my_axioms.py` (compares meaning, not text: it adds probe classes and asks HermiT; about 20 s), `solutions/`; solutions 3 of 3, five common wrong answers each get the right hint (`reference-outputs/my-axioms-check.txt`). `closed_world_demo.py` (item 4): SQLite refuses the row for shipment 1447311670.7, `reference-outputs/closed-world-demo.txt`. Still to run on the Mac: ROBOT with ELK on the new `sample-shipments.ttl` (the two old `realized_sample_shipments_*` files show the old cast), then recapture screenshots 16b, 17, 18. README rewrite (item 5) is next.
- 2026-09-24: Session 3 deck, full draft built with the generator (item 2): `cd scripts/deckgen-s3 && python3 build.py` writes `lectures/kr-session-03-new.html` (48 slides, 231 minutes) next to the old deck until the instructor approves it (item 3). `build.py` now imports `deckgen-s1/kit.py` (which gained an optional `legend`, S1 and S2 rebuild byte for byte) and loads the glossary and `lu-flow`. Parts 1 and 2 converted: arrow diagrams are `lu-flow`, the set pictures stay SVG in the layer colours (`svgkit.py` recoloured), the cast is Brunel, stale guide-deck references removed. New parts 3 (reasoner: 4,819 axioms, three jobs, the red class, a domain-mistake walkthrough from the real HermiT run on `domain-mistake.ttl`, which makes the ontology inconsistent, reading an explanation, check), 4 (the stack, BFO continuants, the reuse trap drawn from Protégé's real explanation via `scripts/proto-diagrams/spec.json`, competency sort, poll on a `Service Level` class, alignment hazards), 5 (profiles, ELK 1 against HermiT 2, drill), 6 (lab, Protégé tool slide, checkpoints, licensing, discussion, glossary, wrap, self-check). GLOSSARY gains MIT licence; glossary check clean. Not yet: live audit, the ELK realization run on the Mac (the SubClassOf and EquivalentTo table and the lab checkpoint assume two V444_1 shipments at risk), screenshots 16b, 17, 18, and the README rewrite.
- 2026-09-24: Session 3 draft, last visual defect fixed. On "The reuse trap: our real bug" the "The fix" callout under the walk squeezed the walk view, so the flow overlapped the step bar by 69 px (canvas). The fix sentence now ends the step 6 caption and the callout is gone. Live (`d965d27`, cache-buster): the four flow walks (slides 17, 25, 32, 38) all end above their step bar at every step, slide 32 by 64 px at step 6; no slide overflow.
- 2026-09-24: item 5 done. Lab README rewritten to 2e: before you start (workspace/ rule, `local_reasoner.py` fallback), Part A six steps with Expect (ELK: Order for a sole-sourced good; HermiT adds Sole-sourced component; reference file none; At-risk shipment: shipments of 1447291369.7 and 1447311670.7), Part B `check_my_axioms.py` (3 of 3), Part C the three discussion questions, optional (ROBOT, `realize_sample.py`, instructor demos, licensing), understood if, take to your project. Stale pointers fixed in the lab files (comments only, every file still parses): `scro-extension-v0.ttl` no longer points at the Protégé guide; both ontologies and `competency_questions.md` pointed at a "lab brief" query that no longer exists, so the query now lives in `competency_questions.md` (run with rdflib: CancelledShipment, CommittedDate, Plant, Port in both files); `domain-mistake.ttl` names the real slide. Still to run on the Mac: `fetch_ontologies.py`, `realize_sample.py --jar ~/tools/robot.jar` (the ELK table and Part A step 6), and the Protégé screenshots 16b, 17, 18.
- 2026-09-25: `realize_sample.py` run on the instructor's Mac (ROBOT 1.9.10 at `~/tools/robot.jar`, ELK): as shipped, the shipments of 1447291369.7 and 1447311670.7 are At-risk shipments and 1447385217.7 is not; with the axiom as SubClassOf, none is. Matches the table on "SubClassOf and EquivalentTo" and README Part A step 6; recorded in `reference-outputs/realized-sample.txt`. `fetch_ontologies.py` rerun there too (catalog check passes); its closing message and docstring now send students to `workspace/scro-extension-v0.ttl`, not the finished file. Protégé screenshots 16b, 17 and 18 are not used by the new deck (the ELK table replaced them), so no recapture is needed. The old `realized_sample_shipments_ELK.ttl` and `_primitive_ELK.ttl` (22 Sept, old individuals) are superseded; kept until the instructor agrees to remove them.
- 2026-09-25: instructor agreed: the two superseded `realized_sample_shipments_*.ttl` files removed. The last placeholder in the Session 3 draft (licensing exercise) replaced with the two real lines as code panels, `scor.ttl` line 22 (`dct:license` ODC PDDL) and `README.md` line 40 ("All rights reserved"), both at `vocol/scor` commit `d12544b` (12 January 2018, still the latest), checked live 2026-09-25. Code panels instead of a screenshot: the browser pane cannot save an image file, and text projects more legibly. The draft now has no placeholders.
- 2026-09-25: **Session 3 approved by the instructor** (items 2 and 3), who named the variety of visualisation, not always one type, as what worked; written into `AGENTS.md` as 2c rule 9 and into the settled decisions. `lectures/kr-session-03-new.html` renamed to `lectures/kr-session-03.html` (the old 22 slide deck replaced; `build.py` now writes there by default and rebuilds it byte for byte). `index.html` cards corrected for all three rebuilt sessions (they still showed the old slide and question counts); its intro no longer says labs extend a graded system. `AGENTS.md` and `PROMPT.md` no longer call the worked example "21 slides, all twelve components": it uses all nine layouts but not reveal, build, compare wipe or the query sandbox, which `design-system.html` shows. Template repo: the deck copied as its worked example with its five screenshots (`assets/img/s3-*.png`) and this course's glossary data as `lectures/kr-session-03-glossary.js` (the template's own `assets/glossary.js` is a two-term sample, so the example's term links would otherwise vanish); its README, AGENTS, PROMPT, index card and `github.md` updated to match.
- 2026-09-25: item 9 scoped by the instructor: full rebuild of Sessions 4 to 6 (not a visual pass), one session at a time with approval before the next; Session 4 first. Measured before starting: Sessions 4, 5, 6 have 42, 40, 36 slides, of which only 5, 2 and 5 carry any visual; no `lu-flow`, no Brunel identifiers.
- 2026-09-25: Session 4 outline approved by the instructor (six parts: why OWL cannot check, SHACL core on Brunel, the inventory as shapes with a triage walk on the real 2,224 rate band results, provenance and versions, reuse and the gate, lab and wrap; lab to 2e with Part B shapes checked by the orders they flag). CI gate decided: a real GitHub Actions workflow in the course repo, run only when `demos/session-04-shacl/` changes, on a small committed sample of Brunel orders, plus one demo branch with a broken triple so students can open a real red run. Clarified with the instructor: the Milestone 1 rubric line on CI belongs to the team project, which is scored; the lab only shows the gate once. `demos/session-04-shacl/shapes_template.ttl` stays untouched until Session 5 is rebuilt, because Session 5 code hardcodes it.
- 2026-09-25: Lab overview standard added to `AGENTS.md` 2e, with Session 2 as the reference. New read first overviews added for Sessions 1 and 4, and the Session 2 sample example corrected to PLANT16 and PORT09. Session 4 EPCIS inspection ran against GS1's live file with rdflib 7.6.0: 1,137 lines, 30 node shapes, 71 property shapes, 0 SPARQL constraints, 0 explicit severities, 27 reused property shapes, 13 forbidden shapes, and 77 messages. The README and Session 4 generator were corrected from 1,138 to 1,137, then the draft deck was rebuilt. The shacl play screenshot was not present, so its honest placeholder remains. Both Part B checkers pass on their supplied solutions; Session 4 still awaits the instructor review and browser audit.
- 2026-09-25: **Session 4 lab built** (item 9, item 19) in `demos/session-04-shacl/`, every step run here with pySHACL 0.40.1 on the real Session 2 graph and recorded in `reference-outputs/`: `brunel-shapes-v0.ttl` (the Session 1 rules as a first draft, all Violations) gives 3,435 Violations (2,224 weight in no rate band, 1,209 band carrier not a Carrier, 2 weight not above 0); `brunel-shapes.ttl` (triaged, each change commented TRIAGE) gives 2 Violations and 2,579 Warnings. New real finding, not in Session 1: orders 1447336276.7 (361 units) and 1447215484.7 (348 units) weigh 0 kg. `validate.py` prints focus nodes first and exits 1 on a Violation; the old `shapes_template.ttl` targets `ul:PurchaseOrder`, 0 focus nodes, conforms True (the targeting trap, recorded). `shape_timings.py`: core order shape 2.6 s, one SPARQL shape 73.1 s. `add_provenance.py` (PROV-O on the four named graphs, 43 triples), `version_ontology.py` (Session 3 ontology released as 1.0.0 into `workspace/`; the Session 3 file is unchanged), `fetch_epcis.py` (GS1 EPCIS shapes: 1,138 lines, 30 node shapes, 71 property shapes, 0 SPARQL, 0 severities; counted in the browser, the script itself still to run once where GS1 is reachable, the Cowork workspace is not), `make_ci_sample.py` (six real orders, 515 triples, for the gate and Part B). Part B: `my_shapes.ttl` (Y1 exactly one customer, Y2 order date in 2013, Y3 CRF orders by V44_3, none of them in the reference shapes), `check_my_shapes.py` (compares flagged orders on `part-b/test-orders.ttl`, four planted faults on real orders), solutions 3 of 3, five wrong answers recorded; one surprise fixed in the hint: text date bounds flag every order in pySHACL, not none. CI gate: `.github/workflows/shacl-gate.yml` (runs only when the lab folder changes), green on main (run 36143273457), red on branch `demo/broken-carrier-code` (run 36143360459, one carrier code V444_O); the branch is kept and never merged. README to 2e. `shapes_template.ttl` untouched for Session 5.
- 2026-09-25: **Session 4 deck drafted** with a new generator, `scripts/deckgen-s4/` (shares `deckgen-s1/kit.py`, `deckgen-s3/common.py` and `svgkit.py`): `lectures/kr-session-04-new.html`, 42 slides, 194 minutes (lecture about 125, lab 54, wrap 14), next to the old deck until approved. Five flow walks, set picture, tables, code, a timing bar chart, 2 MCQs, 2 blank drills, a poll, self-check. Old deck's errors not carried over: the invented cast (po88, carrier-dhl), the MCQ that said a Warning keeps conforms true (false, checked in pySHACL), the wrong version IRI base, the graded lab. Glossary: Triage, Version IRI, Validation gate, GitHub Actions added; Node shape and PROV-O definitions corrected; check clean. Live audit (built-in browser, GitHub Pages, cache buster, `lu:` state cleared): a Sonnet visual QA pass found code blocks wider than their columns, four slides reaching the footer and three diagram label collisions, which the earlier sweep had missed (it measured hidden slides, and only the slide's own scroll height); all fixed and re-measured with a stronger check (walks at the last step against the step bar, content against the footer, code width, diagram labels against nodes and badges against the canvas). One placeholder remains by design: the shacl-play screenshot (slide "The tool: shacl-play"), to capture on the instructor's Mac.
- 2026-09-25: interactive check of the Session 4 draft found the MCQ feedback reading "Correct. Correct.": `lu-deck.js` already prints Correct. or Not quite., and the Session 3 and 4 generators repeated it in `data-fb-correct` / `data-fb-wrong` (Sessions 1 and 2 did not). Removed in both generators; Session 3 rebuilt (4 attribute lines change, nothing else) and copied again to the template repo. Session 4's first check question trimmed: answered, it overflowed by 15 px.
- 2026-09-25: note for whoever reads the log: while Session 4 was being built, three Session 2 lab commits were pushed from another session (1180f72 Docker locality, 1423b66 lab concept overview `OVERVIEW.md`, 884c757 query practice guidance). Session 2 was approved and closed on 2026-09-24; those changes were not part of the Session 4 work and are not recorded elsewhere in this log. The GitHub Pages deploy of 45255ba failed in its deploy step (transient); this commit redeploys.
- 2026-09-25: Session 5 rebuild started (item 9). Instructor decisions: (1) the live operational database holds the four Brunel tables Session 2 converted, in PostgreSQL; the RML mapping replaces Session 2's Python converter, its output is compared with the Session 2 graph, Session 4's shapes run on it, and the mapping fixes the 1,209 untyped rate table carriers (Session 4 triage); (2) entity resolution uses a clearly labelled teaching set: a second "TMS export" of Brunel's real customers and carriers written the way another system drifts, plus decoys, truth known by construction (checked first: DataCo and Brunel share no entities, Brunel customer codes are anonymised and unique, DataCo names are personal data never shown); (3) Ontop is a lab step with a fallback (recorded output when Docker or Java is missing). Facts checked for the rebuild: FreightRates has 1,540 rows, 1,537 distinct, 1,258 distinct on (carrier, ports, service, minimum weight), so a rate band has no natural key.
- 2026-09-25: instructor rule for all future labs recorded under Settled decisions: slides independent of lab results, every Part B task has a worked twin, keep labs simple. Session 5 is designed to it.
- 2026-09-25: **Session 5 lab built** (item 9) in `demos/session-05-integration/`, run here on the SQLite path (PostgreSQL and Ontop need the instructor's Mac). Instructor asked to keep one shared course environment: `demos/requirements.txt` now covers Sessions 1 to 5 (SQLAlchemy, psycopg2-binary and Morph-KGC's real dependencies added) and `demos/requirements-nodeps.txt` installs Morph-KGC 2.10.0 with `--no-deps` (it declares rdflib < 7.3 and pyoxigraph < 0.4 but runs unchanged on 7.6.0 and 0.5.11, tested three ways); `demos/README.md` setup has the second install line. New: `docker-compose.yml` (PostgreSQL 16, 127.0.0.1 only, new volume), `load_database.py` (four Brunel tables, decimals kept as the CSV writes them), `brunel-mapping.ttl` (R2RML, Session 2 vocabulary, logical views, blank node per rate row, all 10 carriers typed), `materialize.py`, `compare_with_session2.py`, `vocabulary.ttl` (Session 2's 49 schema triples), `ontop/` (setup, properties, Q2, run script; not run here), `er/` (labelled TMS teaching set of the 46 real customers plus 6 not in Brunel, Fellegi and Sunter matcher with stated weights instead of Splink, for simplicity), Part B `my_mapping.ttl` + `check_my_mapping.py` + solutions (each task the twin of a rule in the file), OVERVIEW.md, README to 2e. Real results: mapped graph 135,799 triples = Session 2's 135,841 minus its 49 schema triples plus 7 newly typed carriers, 0 differences otherwise (decimals compared to 12 digits: pandas' fast parser misread some long CSV decimals by one unit in the last digit in Session 2); Session 4 shapes on it: 2 Violations, 1,370 Warnings, 0 band carrier warnings (was 1,209); without the vocabulary the order shapes reach 9,023 orders, not 9,215 (the targeting trap, found by accident, recorded); matcher: 2,392 pairs, 1,818 after blocking, threshold 4 P 0.878 R 0.935, threshold 8 P 1.000 R 0.870; checker 3 of 3 on solutions, four wrong answers recorded. Old draft files (load_postgres.py, mapping_template.rml.ttl, mapping.obda, ontology.ttl, ...) are no longer used; deletion waits for the instructor.
- 2026-09-25: **Session 5 deck drafted** with a new generator, `scripts/deckgen-s5/` (shares `deckgen-s1/kit.py`, `deckgen-s3/common.py`): `lectures/kr-session-05-new.html`, 38 slides, 183 minutes (lecture about 115, lab 54, wrap 14), next to the old deck until approved. Built to the new rule: every slide example is complete on the slide, and Part B's three tasks each copy a rule shown in full. Five flow walks, tables, code, a pair-count bar, 2 MCQs, a blank drill, a poll, self-check. The Ontop slide shows Session 2's answers and a hand-written SQL, labelled so; the SQL Ontop generates is recorded only after the Mac run. Glossary: Triples map, IRI template, Logical view, Match weight, RML-LV added; check clean. Live audit (built-in browser, Pages, cache buster, state cleared, the stronger check from Session 4 plus table width): 3 label collisions, 2 walks touching the bar and 2 slides too tall fixed; answered MCQs, filled blanks, revealed poll and self-check all fit.
- 2026-09-25: Session 5 PostgreSQL run on the instructor's Mac: `load_database.py` loaded 9,215 orders, 22 plant ports, 2,036 products per plant, and 1,540 freight rates. `materialize.py` produced 135,799 triples; comparison found 0 only in Session 2 and 7 newly typed rate only carriers in the mapped graph, recorded in `reference-outputs/materialize-and-compare-postgres.txt`. Part B solutions pass 3 of 3. Ontop 5.5.0 setup succeeded, but its query stopped before execution because the property file path contains a space in `Library/Mobile Documents`, recorded in `ontop/last-run.log`; the mapping and prior `ontop-q2.txt` were left unchanged.
- 2026-09-25: **Sessions 4 and 5 approved by the instructor.** `lectures/kr-session-04-new.html` and `kr-session-05-new.html` renamed over the old decks (generators now write there by default and rebuild them unchanged); `index.html` Session 4 card corrected (5 questions, triage walkthrough) and a real Session 5 card replaces the "Not yet built" placeholder. With the instructor's agreement the old Session 5 draft files were deleted (`load_postgres.py`, `mapping_template.rml.ttl`, `config_materialize.ini`, `validate_materialized.py`, `ontology.ttl`, `mapping.obda`, `ontop.properties`, `query.sparql`, `compare_materialize_vs_virtualize.md`, `requirements-materialize.txt`, `requirements-postgres.txt`, `entity_resolution/`). Session 4's `shapes_template.ttl` is no longer read by Session 5; its README and OVERVIEW now keep it only as the targeting trap example. Session 6 rebuild started.
- 2026-09-25: Session 6 decisions (instructor): (1) learn on the Brunel graph Session 5 materializes, the one cast; late order prediction with the real leakage lessons (the label is in the graph twice, as the ul:LateOrder type and ul:lateDays, and must be removed; a random split memorises 4 customers, a split by customer shows the truth); link prediction on which plant makes which product (2,036 real links); the temporal split is taught on a slide as the rule for data with dates (all Brunel orders share one date, 2013-05-26); (2) a simple core: one GNN (GraphSAGE through to_hetero), one link predictor (TransE in PyKEEN, filtered metrics), one baseline (logistic regression), the split comparison; RGCN, DistMult, ComplEx, RotatE and XGBoost on slides only; (3) the learning stack goes into the shared course environment. Facts checked for the rebuild: 192 of 9,215 orders late; only 4 customers have late orders; Brunel has no supplier table.
- 2026-09-25: Session 6 feasibility, real runs in the Cowork workspace on Session 5's `brunel-mapped.nt` (torch 2.8.0 CPU, torch-geometric 2.8.0.post1, pykeen 1.11.1, scikit-learn 1.7.2, all next to the shared pins without new conflicts). Late orders, logistic regression: lateDays left in PR-AUC 1.000; random split PR-AUC 0.777 (ROC 0.988); split by customer PR-AUC 0.002 to 0.019 against a chance level of 0.021; accuracy 0.95 to 1.00 everywhere (majority 0.979). GraphSAGE through to_hetero: random split PR-AUC 0.936, split by customer 0.005 to 0.034. Plant makes product, TransE on 5 relations, ranked among plants, filtered: MRR 0.547 against popularity 0.632; 61 of 203 held-out links name a product seen nowhere else. A to_hetero gotcha found for real: the model's forward must name its argument edge_index, or every convolution fails with a misleading edge_index error.
- 2026-09-25: at the instructor's request ("make sure any new session knows what is done and how we plan the labs and the sessions"): `AGENTS.md` 2e now states the three lab rules (slides stand on their own, every Part B task has a worked twin, keep labs simple) and the one shared environment rule; new `AGENTS.md` 2f writes down the rebuild method used for Sessions 3 to 6, step by step; new `scripts/audit-live.js` is the live check used since Session 4 (walks, footer, code width, table width, diagram labels and badges), so no session has to re-derive it. "Where to continue" now lists exactly what of Session 6 is built and what comes next.
- 2026-09-25: **Session 6 lab built** (item 9) and pushed (292ecc8). Recorded runs in `reference-outputs/`: graph 9,215 orders, 46 customers, 3 carriers, 20 plants (PLANT01 to PLANT19 and CND9, which appears only in ProductsPerPlant; orders ship from 7), 11 ports, 1,540 products; logistic regression lateDays kept PR-AUC 1.000, random split 0.788 (accuracy 0.944), split by customer 0.002 to 0.019 and one seed with no late order in test; GraphSAGE random split 0.857 to 0.879 over three training seeds, split by customer 0.004 to 0.045; TransE MRR 0.573, 0.469, 0.543 against popularity 0.631, 0.597, 0.634 (61 to 77 held-out links left out, their product appears in no other link); Part B checker 0 of 3 blank, 3 of 3 solutions, three wrong answers recorded. The feasibility numbers in the entry above were from earlier settings and are superseded by these. Two em dashes in `demos/requirements.txt` comments replaced.
- 2026-09-25: **Session 6 deck drafted** with a new generator, `scripts/deckgen-s6/` (shares `deckgen-s1/kit.py`, `deckgen-s3/common.py` and `svgkit.py`): `lectures/kr-session-06-new.html`, 42 slides, 185 minutes (opening 8, why a graph 16, embeddings 32, message passing 33, leakage 26, lab 54, wrap 16), next to the old deck until approved. Every example is complete on the slide: one real late order (1447135386.7, customer V555_15, whose 110 orders are all late) carries Parts 1, 3 and 4; the real product 1681878 (made by PLANT07, 08 and 10) carries negative sampling and a real popularity ranking (raw rank 13, filtered 11). Added from counts on `brunel-mapped.nt`: the four customers with late orders (V555_15 110 of 110, V555555555555555_44 9 of 9, V555555555_27 69 of 521, V555555555_14 4 of 351), and the reach of message passing (two layers reach a median 9,074 of the other 9,214 orders, four reach all). Syllabus points covered on slides only: DistMult, ComplEx, RotatE (pattern table), RGCN and the weight count, the ontology deciding node and link kinds, the temporal split rule. Visuals: 3 flow walks, 3 SVG drawings (TransE, the 46 customers, a time split), 5 bar panels, tables, code, 2 MCQs, a blank drill, a poll. Glossary: Session 6 terms added (Hits@k, filtered ranking, negative sampling, DistMult, ComplEx, RotatE, logistic regression, PR-AUC, precision@k, GraphSAGE, to_hetero, HeteroData, RGCN, oversmoothing, inductive, transductive, leakage, random split, split by group, temporal split, CPU, GPU); Baseline no longer says a result only counts if it beats it; `check-glossary.py` ignores CND9 and the task labels Y1 to Y3; check clean. Live audit (audit-live.js, cache buster, state cleared): 10 slides fixed over three rounds, then clean; both MCQs answered right and wrong from a clean state, blanks filled, poll revealed: the revealed poll overflowed and now has two options. The Pages deploy of 8d6a0c5 failed (transient); this commit redeploys.
- 2026-09-25: Session 6 draft, Sonnet visual pass over all 42 slides (walks stepped to the end, drill and poll answered): no defect. One label in the TransE drawing sat on its dashed line (seen by hand); moved. Handed to the instructor for review.
- 2026-09-25: Session 6 lab verified on macOS with the shared Python 3.12 environment after installing the pinned PyTorch, PyTorch Geometric, PyKEEN and scikit-learn packages. `build_graph.py`, `baseline.py`, `gnn.py`, all three Part B solution checks, and `link_prediction.py` passed. Fixed two portability and reproducibility failures: PyKEEN now keeps its PyStow cache under the ignored generated lab data instead of assuming a writable home directory, and the graph builder sorts RDF `makes` and `servesPort` relations before assigning IDs. Two independent builds now produce the same `makes` edge-order hash.
- 2026-09-25: Overview audit for Sessions 1 to 6 against Session 2's student-facing standard. Sessions 2, 3 and 5 already explain the question, data, tools, relationships, steps, file roles, terms, and the boundary between source facts and course choices. Session 1 now explains what profiling, clustering, and the inventory each can and cannot decide, plus its cross-table evidence example. Session 4 now identifies rdflib, pySHACL, `validate.py`, and GitHub Actions and their distinct roles. Session 6 now identifies rdflib, PyTorch Geometric, scikit-learn, and PyKEEN, and walks one order through retained features, graph links, and the two withheld leakage labels.
- 2026-09-25: Session 5 PostgreSQL and Ontop path run end to end on macOS. Database loading (9,215 orders, 22 plant ports, 2,036 product links, 1,540 rate bands), materialization (135,799 triples), comparison (0 only in Session 2, 7 only in the mapping), entity resolution, and the Part B solution checker (3 of 3) all passed. Ontop 5.5.0 Q2 returned the three expected carrier totals. Fixed `ontop/run_ontop.py`: Ontop now receives paths relative to the lab, avoiding the space in `Mobile Documents`, and reads a temporary CSV rather than debug logs. The output is recorded in `reference-outputs/ontop-q2.txt`. The full SHACL validation was started twice but did not complete within the available 30-second command window; its prior recorded SQLite result remains the evidence for step 5.
- 2026-09-25: **Session 7 rebuild started** (item 9 method, AGENTS.md 2f; the instructor reviews Session 6 later). Research brief (sub-agent, checked): sparql-llm 0.1.4 (2026-01-21, MIT; about 215 MB with fastembed, qdrant-client, onnxruntime; downloads an embedding model and calls Expasy endpoints on import; does not import on Python 3.10), void-generator v0.19 (Java 17+), TEXT2SPARQL 2026 (contract `GET /?question=&dataset=` returning `{dataset, question, query}`; overall leaderboard led by SPARQL-LLM, F1 0.790), text2sparql-client 2.1.0 (Python 3.11+, forces numpy below 2 and a C build of pytrec-eval, so not in the shared environment). Gemini is available in Lebanon with a free tier; current models include `gemini-3.5-flash-lite` (checked on ai.google.dev, 2026-09-24). From this sandbox no LLM API is reachable and there is no Python 3.12 or Java 17, so every live model call is recorded on the instructor's Mac. Instructor decisions: (1) **everyone live with Gemini** in the lab (a free key per student; a replay of the recorded answers stays as the fallback when a key fails); (2) **a simple core** written for the course (schema from VoID, example retrieval, validate and repair, refusal, a scorer with the TEXT2SPARQL metric, the GET contract), with sparql-llm and text2sparql-client on slides and as optional steps; (3) the reference answers are **recorded with Gemini Flash-Lite on the instructor's Mac** (`record_llm.py`), and the deck reads the recorded file; (4) deployment and governance on **slides plus a Docker Compose template** for the access layer that teams copy into their Session 8 stack, not run in class.
- 2026-09-25: Session 7 feasibility (no model call possible here): VoID of Session 2's graph by one CONSTRUCT in void-generator's layout, 189 triples, 8 classes, 0.2 s; 12 answerable test questions with verified answers (9,215 orders; 192 late; carriers V444_0, V444_1, V44_3; V44_3 854; PLANT03 makes 781; 7 plants serve PORT04; V555_15 110 orders; 4 customers with late orders; CRF, DTD, DTP; PORT09 173; PLANT03 most products; V444_0 39 rate bands) and 3 it cannot answer (location, email, cancellation); the validator catches an invented `ul:shippedBy` and lists the real properties; the repair loop and refusal path pass with a scripted model. **Outline approved by the instructor** ("Build it as planned"): deck about 42 slides, 180 minutes (why text to SPARQL is hard, grounding, validate repair refuse, measuring, deployment and governance, open problems, lab, wrap); lab Part A make_void, show_prompt, ask, check, evaluate (three settings: schema only, plus examples, plus repair), serve; Part B Y1 an example in the SHACL vocabulary, Y2 `unknown_classes` (twin of `unknown_properties`), Y3 a test question with its gold query (not one of the examples).
- 2026-09-25: **Session 7 lab built and deck drafted.** Lab: `access_layer.py` (schema from VoID, examples by shared words, the model through Gemini's OpenAI compatible address with `GOOGLE_API_KEY` from `demos/.env`, modes live, record and replay; check by parsing and by unknown properties; up to 2 repairs; refusal), one script per step (`make_void.py` 189 triples, `show_prompt.py` examples 1, 2, 4 and 2,920 characters, `ask.py`, `check.py` 1 problem, `evaluate.py` three settings, `serve.py` the TEXT2SPARQL GET contract with the standard library only), `SPARQL_ENDPOINT` to use Fuseki (`kr` dataset), Part B (Y1 an example in the SHACL vocabulary, Y2 `unknown_classes`, Y3 a test question; checker 0 of 3 blank, 3 of 3 solutions, three wrong answers recorded), `record_llm.py`, `deploy/` (Dockerfile and a Compose service, not built here). The plumbing was tested end to end with a fake OpenAI compatible server (not a model) and a small local SPARQL endpoint; nothing from those tests was kept. Part B's Y3 is a test question instead of the planned `set_recall`, because the scorer needs recall itself. Deck: 47 slides, 179 minutes; the settings slide says "recorded run pending" until `evaluate.txt` exists. Glossary: a Session 7 section (29 terms); `check-glossary.py` also ignores citation venues and a team name. Live audit: 3 slides fixed, then clean in every state; Sonnet visual pass over 47 slides: no defect.
- 2026-09-25: **Sessions 5 and 6 approved by the instructor** (labs run by the instructor on the Mac, labs and slides approved). `lectures/kr-session-06-new.html` renamed over `kr-session-06.html` (the generator now writes there), `index.html` Session 6 card made live (42 slides, 185 minutes, 4 questions, Milestone 2), PROGRESS row 6 Done. Before the rename, the Session 6 lab was rerun in the cloud workspace after the Mac session's reproducibility fix (d27e4ee sorts the makes and servesPort links): baseline unchanged; GraphSAGE random split now 0.859, 0.864, 0.875 and by customer 0.004 to 0.046; TransE MRR 0.555, 0.495, 0.519 against popularity 0.608, 0.562, 0.570 (131, 133, 141 links scored; 72, 70, 62 left out). The story is unchanged (the count wins every seed; the GNN wins only by remembering customers); `reference-outputs/`, the deck and the README now carry these numbers. They were run on Linux CPU; a Mac run may differ in the last digit.
- 2026-09-25: **First Session 7 recording (Mac, gemini-3.5-flash-lite) showed over-refusal:** mean F1 0.500 (schema), 0.417 (examples), 0.417 (repair); all 3 unanswerable questions refused, but also 4, 7 and 7 answerable ones, with reasons such as "the schema does not support aggregation functions like COUNT" and "REFUSE: carrier V444_0"; the repair loop never ran, because a refusal skips the check. So the prompt rules were revised: every code in a question is a thing in the graph; all of SPARQL 1.1 (COUNT, GROUP BY, ORDER BY, ...) is allowed; refuse only for a kind of fact the schema does not list, with a person's name as the example (not one of the three test refusals, to avoid a leak). The prompt is now 3,239 characters (rules 1,021). Recorded outputs now carry a fingerprint of the rules (`RULES_ID`, today `ccb41f71`), and the deck ignores a recording made with other rules, so the first recording (left uncommitted in `reference-outputs/`, made with the old rules) must be recorded again before the deck shows numbers. Keep the first run's numbers for the discussion: they are a real example of a refusal rule that is too strong.
- 2026-09-25: Session 7 free tier limits (instructor's question; Gemini rate limits page, 2026-09-02: RPM, TPM and RPD per project, RPD resets at midnight Pacific, actual numbers only in AI Studio): every live call now waits 4 s by default (0 for a local server), retries a 429 three times after 20, 40, 60 s, and stops with a plain message on a daily limit ("PerDay" in the error) or after four tries. Tested here against a fake server returning 429 (per minute, then success) and a daily-limit 429. README "Before you start" says so; the lab makes about 60 calls.
- 2026-09-25: **Instructor rule: Gemini only.** No Ollama or any other model provider anywhere in Session 7 (lab, README, code, glossary, slides). Removed: the README's Ollama option, the Ollama glossary term, the `LLM_BASE_URL` and `LLM_API_KEY` settings in `access_layer.py` (the address is Gemini's, the key is `GOOGLE_API_KEY`), and Ollama in the daily-limit message. The fallback when a key fails stays `LLM_MODE=replay`.
- 2026-09-25: **Session 7 recorded again on the Mac, against the revised prompt rules (rules `ccb41f71`, model gemini-3.5-flash-lite).** `make_void.py` wrote 189 triples; `check_my_access.py solutions` gave 3 of 3 right; `record_llm.py` made its recorded run and wrote `reference-outputs/llm-cache.json` plus the four output files, all opening with "rules ccb41f71)". `evaluate.py --quiet` gave: schema mean F1 0.792, examples mean F1 1.000, repair mean F1 1.000, each on 12 answerable questions; every setting refused all 3 unanswerable questions and refused none of the answerable ones. Two answerable questions were wrong in the schema-only setting, both right once examples were added: "How many orders did customer V555_15 place?" (the model wrote `?order a ul:Order ; ul:orderedBy <...V555_15>`, which requires the explicit class and returns count 0, instead of dropping that clause) and "How many orders leave from port PORT09?" (the model used `ul:shipsTo` instead of `ul:shipsFrom`, counting arrivals, 9,023, instead of departures). `LLM_MODE=replay python ask.py` and `LLM_MODE=replay python evaluate.py --quiet` reproduced the same answer and the same three summary lines with no network use. The deck was rebuilt (`cd scripts/deckgen-s7 && python3 build.py`): the "Three settings" slide now reads these real numbers. `python3 scripts/check-glossary.py` printed nothing. Docker Desktop was running, so `docker build -f deploy/Dockerfile -t access-layer .` was also run (image built, not run). Session 6 rerun on this Mac for comparison, without overwriting its reference outputs: `build_graph.py` reproduced its own printed numbers; `gnn.py` matched the Linux reference (`reference-outputs/gnn.txt`) on every line except training seed 1, where PR-AUC read 0.863 against 0.864 and precision@100 read 0.52 against 0.54; `link_prediction.py` matched every popularity-baseline line and every hidden-link count exactly, with TransE's MRR differing in the third decimal on all three seeds (0.550, 0.494, 0.520 against 0.555, 0.495, 0.519) and Hits@1 differing only on seed 0 (0.351 against 0.359); the story (TransE never beats the popularity baseline) is unchanged. Session 7 waits for the instructor's review.
- 2026-09-25: Session 7 slides and README now use the recorded run's real mistakes: in the `schema` setting the model wrote `?order a ul:Order` for customer V555_15 (0 instead of 110: all 110 are typed `ul:LateOrder` only) and `ul:shipsTo` for "leave from" PORT09 (9,023 instead of 173); both passed the check, both were fixed by the examples; no question needed a repair (the notes say so: the loop is insurance). Session 6 on the Mac differs from the Linux reference only in the third decimal (GNN seed 1 0.863 against 0.864; TransE MRR 0.550, 0.494, 0.520 against 0.555, 0.495, 0.519; popularity identical): the reference stays, and the README already says the last digit may differ.
