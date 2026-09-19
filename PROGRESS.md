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
| 3 | 2 | Ontology Engineering: Description Logic, OWL, and Reuse | Built | Scriptable parts built, Protege/reasoner steps are manual by design |
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

Deck built. Lab is smaller by design, Protege is a GUI application, so only
its scriptable parts are built:

- `fetch_ontologies.py`, downloads the real IOF Core and Supply Chain
  (SCRO) ontologies at tag `Release_202603` (MIT licensed), plus the real
  GS1 Web Vocabulary (Apache 2.0), into a gitignored `workspace/`, with a
  self-check that the SupplyChain to Core to BFO import chain resolves
  fully offline before Protege ever opens.
- `scro-extension-starter.ttl`, a valid starter ontology (verified with
  rdflib), correcting the deck's own illustrative example
  (`iof:MaterialTransport`, which does not exist in real SCRO) to a real,
  verified class (`ioc:Shipment`), with the correction documented inline.
- `competency_questions_template.md`, seeded with the deck's four given
  competency questions.
- `robot_report.py`, wraps the two ROBOT commands the deck's lab brief
  shows (`reason` with ELK, then `report` at QC profile).

Still manual, by design, per the deck: opening the starter file in Protege,
running ELK then HermiT, reading the inferred hierarchy, and the ten-minute
licensing exercise (a real, still-live SCORVoc licence conflict, documented
in `workspace/LICENCES.md`, deliberately left unsolved so the room resolves
it live). Nothing further to build here unless the deck's brief changes.

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
