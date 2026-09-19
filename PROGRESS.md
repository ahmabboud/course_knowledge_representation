# Progress tracker, Knowledge Representation

Read this file first, before touching a session. It is the single place
that says what is built, what is in flight, and what a new session should
pick up next. Update it in the same change as any work it describes, do
not let it drift behind the actual state of the repository.

**Read `PROJECT-REDESIGN.md` next.** It covers a separate decision, the
capstone project's shape (teams of 2 to 3, own topic, own database,
evaluated at the end), decided 2026-09-17 and fully shipped, all six items
in its own "Still to build" list are done. It does not track lecture-deck
or lab-code progress, that is this file's job.

## Status by session

| # | Module | Title | Lecture deck | Lab code |
|---|---|---|---|---|
| 1 | 1 | Enterprise Knowledge Representation and the Supply Chain Problem | Built | Built, notebook-presented |
| 2 | 1 | RDF, SPARQL, and the Graph as a Data Model | Built | Built, notebook-presented |
| 3 | 2 | Ontology Engineering: Description Logic, OWL, and Reuse | Built, reworded for run-and-observe, visual QA of the reworded slides still owed, see Session 3 detail | Built as a run-and-observe walkthrough on a finished reference ontology, Protege/reasoner steps run live in the room from it |
| 4 | 2 | Constraints, Quality, and Provenance: SHACL | Not built | Not started |
| 5 | 3 | Integrating Operational Data | Not built | Not started |
| 6 | 4 | Learning Over the Graph: Embeddings and Graph Neural Networks | Not built | Not started |
| 7 | 5 | The Agentic Query Layer, Deployment, and Open Problems | Not built | Not started |
| 8 | 5 | Supervised Build, Deployment, and Defense | Not built (defense day, see `module-08-defense/`) | N/A, live supervised session |

Session 4 carries Milestone 1 (20%), due at end of that session. Session 6
carries Milestone 2, due at end of that session. Both against each team's
own capstone topic, per `PROJECT-REDESIGN.md`, not the shared case.

## Repository layout, so a new session orients fast

```
lectures/kr-session-NN.html        One self-contained lecture per built session
lectures/_template.html            Copy this to start a new session's deck
design-system.html                 Live component gallery, start here before authoring
AGENTS.md                          Authoring contract, read before writing a lecture
PROMPT.md                          Paste-ready brief for handing a new session to an agent
PROJECT-REDESIGN.md                Locked capstone design (teams, topics, defense), done
demos/                             Instructor-only labs, real code against real data
  session-01-environment-and-constraints/
  session-02-rdf-sparql/
  session-03-ontology/
  session-04-shacl/  ...session-08-deploy-and-defend/
```

`demos/` lives inside this repository, matching DSCAI's own layout
(instructor labs are not a separate sibling repo). Moved here 2026-09-18
from a wrongly-separated `kr-labs` repo, see this file's session-1-to-3
detail below.

## Session 1, detail

Deck and lab both built. Lab code (`demos/session-01-environment-and-constraints/`)
rewritten 2026-09-18 into Jupytext percent-format `.py` cells
(`profiling.py`), so it opens as a real notebook in JupyterLab or VS Code:
a `quality_summary()` table, a `plot_missingness()` chart, and the
ydata-profiling report rendered inline via `to_notebook_iframe()`, all
guarded so the same file still runs cleanly as a plain script outside a
notebook (`IN_NOTEBOOK = get_ipython() is not None`, `try/except
NameError`). Nothing left to build here.

## Session 2, detail

Deck and lab both built. Lab code (`demos/session-02-rdf-sparql/`) got the
same notebook treatment plus a new file, `lab_walkthrough.py`: imports the
real functions from `convert_to_rdf.py`, `load_fuseki.py`, `run_queries.py`
and `neo4j_comparison.py` rather than duplicating logic, and adds a sample-
triples table, a small `networkx` graph drawing, a SPARQL-results-to-pandas
helper, a timings chart and Neo4j load-count queries. `convert_to_rdf.py`
also had a code smell fixed (`__import__("rdflib").URIRef(...)` replaced
with a plain import). Nothing left to build here.

## Session 3, detail

Deck built. Lab redesigned 2026-09-19 (see "Redesign round 3" below)
from an authoring exercise into a run-and-observe walkthrough:

- `fetch_ontologies.py`, downloads the real IOF Core and Supply Chain
  (SCRO) ontologies at tag `Release_202603` (MIT licensed), the real
  GS1 Web Vocabulary (Apache 2.0), and copies in the finished reference
  ontology, into a gitignored `workspace/`, with a self-check that the
  SupplyChain to Core to BFO import chain resolves fully offline before
  Protege ever opens.
- `scro-extension-reference.ttl`, a complete, finished ontology
  (verified with rdflib), all eight competency questions answered,
  nothing left for anyone to add or fix. Correcting the deck's own
  illustrative example (`iof:MaterialTransport`, which does not exist
  in real SCRO) to a real, verified class (`ioc:Shipment`), and reusing
  several more real SCRO classes and properties directly
  (`ioc:Facility`, `ioc:Carrier`, `ioc:MaterialComponent`,
  `ioc:MaterialProduct`, `ioc:PurchaseOrder`, `ioc:ShippingRoute`,
  `ioc:dependsOnProduct`, `ioc:dependsOnSupplier`), all checked against
  the real Release_202603 files, not assumed.
- `competency_questions.md`, a reference (not a worksheet) mapping all
  eight competency questions to the class that answers each, and
  explaining the four classes that deliberately do not answer one.
- `robot_report.py`, wraps the two ROBOT commands the deck's lab brief
  shows (`reason` with ELK, then `report --fail-on none`), against the
  finished reference file.

Protege, the reasoners, and the licensing exercise are still run live
in the room, per the deck and this lab's own README, now framed as
something the room watches and discusses rather than something each
student builds, see "Redesign round 3" below for why. Nothing further
to build here unless the deck's brief changes.

### Slide QA, 2026-09-19

- **Slide 6 ("The three reasoning tasks"), fixed, a real bug.** The three
  cards plus the click-to-reveal panel below them slightly exceeded the
  fixed 1600×900 slide canvas once the panel was opened, so the reveal
  button's text was visibly sliced off at the bottom (confirmed by
  rendering the deck headless and measuring the DOM, not just by eye).
  Fixed by trimming card and reveal copy to a tighter word count (same
  meaning, fewer wrapped lines) and dropping two redundant inline
  `margin-top` styles that double-spaced on top of the slide's own flex
  gap, a pattern this slide had that no other slide in the deck uses.
  Re-verified headless with every card and the reveal panel open: fits
  cleanly with margin to spare. If a future edit to this slide's copy
  makes it grow again, check it the same way: open `lectures/kr-session-03.html#/6`
  in a browser, step `→` through all four builds, click the reveal open,
  and look for clipped text at the bottom edge.
- **Slide 14 ("The upper ontology stack"), not a bug, by design.** Landing
  on it directly shows only the heading and the figure placeholder; the
  four ontology layers, the alignment tags, and the callout are
  `data-build` steps that reveal one at a time on `→` (same mechanic as
  slide 6's cards), and the figure is an intentional placeholder already
  on `README.md`'s "Before teaching from it" checklist. Confirmed by
  stepping through the builds; no code change made. Worth knowing if this
  question comes up again for a different slide: check whether the
  "missing" content is behind an unstepped `data-build`, or press `S` for
  study mode, before assuming it's broken.

### Lab dry-run round 2, 2026-09-19: three straightforwardness fixes

Goal this round: the lab should be unambiguous to run, no step where a
student has to guess. Re-ran `fetch_ontologies.py` end to end and
re-read the starter file and templates with that lens. Found and fixed
three real issues, none of them reasoning bugs, all of them "a student
would stop here and not know what to do":

- **`fetch_ontologies.py` had a single point of failure.** `fetch_gs1()`
  had no error handling and ran before `copy_starter()` and
  `write_licences_note()`, so any network hiccup on the GS1 download
  (the least essential fetch, only needed for the later term-reuse
  step) crashed the script with a raw traceback and skipped the parts
  a student actually needs to open Protege. Fixed: `fetch_gs1()` now
  warns and continues on failure, and runs after the starter-file copy
  and licence note, so those always complete regardless. Verified by
  forcing the GS1 request to fail: the script now finishes cleanly with
  a warning, catalog check still passes.
- **The starter file failed its own "every class needs a competency
  question" rule, twice, unexplained.** Running the lecture's own
  "classes with no competency question" SPARQL query against the
  untouched starter returns `CancelledShipment` and `CommittedDate`.
  `CancelledShipment` not having one is deliberate, it is the deck's
  own later exercise target, but that framing lived only in the slide,
  not in the lab files. `CommittedDate` not having one is a different,
  legitimate reason (it is a support class, not a business entity a
  competency question would name), also never stated anywhere. A
  student running that query on their own lightly-edited file could
  not have told a designed exercise from an oversight. Fixed: added a
  comment on each explaining which is which and why.
- **Two different, disagreeing counts of classes left to build.**
  `README.md` and `competency_questions_template.md` both say four
  competency questions given, four the student's own. The starter
  file's own closing comment said "six are yours," undercounting by
  one: only one of the four given questions has a class built for it,
  so seven classes are actually needed, not six. Fixed: reworded the
  starter file's closing comment to state the count the same way as
  the other two files, and corrected it to seven.

None of this touches the manual Protege walkthrough itself (open,
extend, run ELK then HermiT, read the hierarchy), which still has not
been dry-run by anyone, that remains the biggest untested part of this
lab. Also still open: a real `robot_report.py` run against a file with
several real added classes, not just the bare starter, to see what a
realistic `report.tsv` looks like. Sandbox used for this round had no
path to install ROBOT itself to do that here.

### Redesign round 3, 2026-09-19: run-and-observe, not build-it-yourself

Instructor decision, overriding round 2's fixes rather than building on
them: round 2 made the authoring-based lab's own files internally
consistent, but the lab's whole shape was the actual problem. Feedback:
the lab needs to be straightforward to run, with no unclear step, and
was not expecting students to draft competency questions or extend an
ontology live at all, just run the pipeline and observe it.

What changed:

- `scro-extension-starter.ttl` (a starter meant to be extended) is
  replaced by `scro-extension-reference.ttl` (a finished ontology,
  meant to be opened, reasoned over, and read, never edited). All eight
  competency questions are answered in the file itself, authored using
  real SCRO reuse wherever SCRO covers the concept, and two genuinely
  new classes (`ul:Port`, `ul:FreightRateBand`) where reuse search
  against both SCRO and GS1 came up empty, an honest, checked outcome,
  not an assumption. `ul:CancelledShipment` (no competency question, on
  purpose) and three support classes (`ul:CommittedDate`, `ul:Plant`,
  `ul:Port`) are kept and explained inline, so the "classes with no
  competency question" query still has something real to find and
  discuss, without anyone needing to have written anything themselves.
- `competency_questions_template.md` (a fill-in-the-blanks worksheet)
  is replaced by `competency_questions.md` (a reference table, question
  to class, plus where the real authoring skill actually gets
  practiced: each team's own capstone topic, not this file).
- `README.md` rewritten end to end as a run-in-order script for
  whoever is driving the room, addressed to that person (matching
  `demos/README.md`'s own description of this repository as
  instructor-run, live), not to a student working alone at a laptop.
  Removed the individual "push your ontology to your repository
  tonight" deliverable, there is no student deliverable from this
  session's shared-case walkthrough, the real deliverable stays the
  team's own capstone milestone. Added a "Nothing here is broken"
  section: since every file is now supposed to come back clean, the
  README now says explicitly what a real problem looks like versus the
  two documented, deliberate exceptions, so a genuine bug is not
  mistaken for part of the design, or the reverse.
- `fetch_ontologies.py` and `robot_report.py` reworded throughout,
  starter/extend language removed, function and default-filename
  renamed to match (`copy_reference`,
  `scro-extension-reference.ttl`), the "Save As before editing" Protege
  instruction dropped since nothing gets edited.
- `demos/.gitignore` and `demos/README.md` reworded to stop calling the
  workspace outputs "student deliverables," they are the instructor's
  own checked-in example of a clean run.
- The lecture deck (`lectures/kr-session-03.html`) updated to match, in
  every place it previously described a 95-minute individual
  build-and-submit exercise: the objective slide's deliverable callout
  and "how the 180 minutes are spent" list, the "four given, four
  yours" competency-question reveal (now "four of eight, shown as a
  preview"), the reading slide's code block and caption
  (`scro-extension-reference.ttl`, not `scro-extension.ttl`, and not
  "graded"), the ontology-layers slide's SCRO note and Figure 3.1
  caption, the lab brief's title, numbered steps (now six: open,
  find the CQs, run ELK/HermiT, run ROBOT, discuss
  `ul:CancelledShipment`, licensing exercise), its terminal command
  (`scro-extension-reference.ttl`) and deliverable callout, and the
  closing pairs exercise (now: answer a CQ against the reference file,
  debate `ul:CancelledShipment`, then check in on the team's own
  topic, replacing "push ontology v1 to your repository tonight" with
  an optional, no-pressure push of real capstone progress).
  Tag-balance checked (`section`/`div`/`ol`/`ul`/`li`/`h2`/`p` open and
  close counts match) but **not** visually rendered, this sandbox
  cannot open local files in a browser to headlessly check layout the
  way the 2026-09-19 slide-6 fix did. Several edited slides (3, 15, 18,
  20) now carry longer paragraph and list-item text than before; do
  the same headless step-through those slides got during that earlier
  fix (`lectures/kr-session-03.html#/3`, `#/15`, `#/18`, `#/20`) before
  trusting them not to clip, especially slide 18's numbered list and
  deliverable callout, the ones that grew the most.

Two old files could not be deleted from this session (a filesystem
permission restriction on this mount blocked every `rm`, `git rm`, and
`unlink`, even though renaming worked): `scro-extension-starter.ttl`
and `competency_questions_template.md` are now stub files pointing at
their replacements. Delete both by hand next time you have normal
filesystem access to this repository.

## What's next

**Session 4 (SHACL)** is the next unbuilt session, and the one carrying
Milestone 1. Building order, same as Sessions 1 to 3: confirm the deck
against the syllabus segment text, build it in `lectures/`, add its
`index.html` card, then build `demos/session-04-shacl/`'s lab code from its
own (already-written) README once the deck exists, not before, building lab
code ahead of the deck it serves risks locking in the wrong shape.

Sessions 5 through 8 remain entirely unbuilt (deck and lab), each with a
README in `demos/` stating what it will build, accurate to the syllabus.

## Standing conventions

- One folder per session in `demos/`, numbered, matching the deck it
  serves. Each folder's own README states what it builds, which syllabus
  deliverable it produces, and which real tools it uses, read that before
  the code.
- Notebooks (Jupytext `# %%` percent-format `.py` files, not raw `.ipynb`)
  for anything meant to be read and run step by step in the room, a plain
  `.py` script for a batch step. Both are fine, pick per task.
- Real data, real containers, real sources. Session 3's ontologies and
  vocabulary are the real published files, not stubs, same rule as the
  Session 1/2 data.
- Push discipline: this repository is worked on from a device bridge shell
  that has no stored GitHub credentials, so commits land locally but do not
  reach `origin/main` on their own. Check `git log origin/main..HEAD` at
  the start of a session, if it is non-empty, the user still needs to push
  from their own terminal or Git client before the remote reflects the
  local work.
