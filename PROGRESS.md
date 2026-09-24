# Progress tracker, Knowledge Representation

Read this file first, before touching a session. It is the single place
that says what is built, what is in flight, and what a new session should
pick up next. Update it in the same change as any work it describes, do
not let it drift behind the actual state of the repository.

**Open work lives in `REPLAN-STATE.md`: read it second.** Its checklist is
the single to-do list. The status table below was reconciled against the
repository on 2026-09-24 (REPLAN-STATE item 11). "Built" means the file
exists and works; no session counts as done until the instructor says so.

**Where to continue (2026-09-24):** Session 1 is done. Session 2 is rebuilt and waits for the instructor's review (REPLAN-STATE item 8); then Session 3 parts 3 to 6 (item 2).
Done most recently (2026-09-24): Session 1 rebuilt and approved; Session 2
deck and lab rebuilt and verified; IRI convention written into `AGENTS.md` 2d
and applied to Session 5 mappings; Fuseki now built from Apache's release
(`demos/fuseki/`). Every new term goes into `GLOSSARY.md`.

**Read `PROJECT-REDESIGN.md` next.** It covers a separate decision, the
capstone project's shape (teams of 2 to 3, own topic, own database,
evaluated at the end), decided 2026-09-17 and fully shipped, all six items
in its own "Still to build" list are done. It does not track lecture-deck
or lab-code progress, that is this file's job.

## Status by session

| # | Module | Title | Lecture deck | Lab code |
|---|---|---|---|---|
| 1 | 1 | Enterprise Knowledge Representation and the Supply Chain Problem | **Done**: rebuilt to the 2c standard and approved by the instructor 2026-09-24 (46 slides, 185 min) | Built, verified working by the instructor 2026-09-23 |
| 2 | 1 | RDF, SPARQL, and the Graph as a Data Model | Rebuilt 2026-09-24 to the 2c standard (42 slides, 173 min, audit clean), awaiting the instructor's review (REPLAN-STATE 8) | Rebuilt 2026-09-24 and run end to end (Fuseki 5.5, Oxigraph, Neo4j 5.26); two linking bugs fixed; brought to the lab standard (`AGENTS.md` 2e) with a write your own part and a checker |
| 3 | 2 | Ontology Engineering: Description Logic, OWL, and Reuse | Old deck live; new deck in progress, parts 1 and 2 built by the generator, parts 3 to 6 next (REPLAN-STATE 2, 3) | Built and reasoner verified (v0 file with a real modelling error, reference fix, sample shipments, reference outputs); `closed_world_demo.py` and README rewrite still open (REPLAN-STATE 4, 5) |
| 4 | 2 | Constraints, Quality, and Provenance: SHACL | Built (197 min), visual pass pending (REPLAN-STATE 9) | Not built: only README and `shapes_template.ttl` |
| 5 | 3 | Integrating Operational Data | Built as a draft (172 min), pending the instructor's confirmation; visual pass pending | Built as a draft, tested on Postgres; not yet confirmed with the real Ontop CLI (see its README Status) |
| 6 | 4 | Learning Over the Graph: Embeddings and Graph Neural Networks | Built (159 min), visual pass pending | Built and run end to end on CPU (Milestone 2) |
| 7 | 5 | The Agentic Query Layer, Deployment, and Open Problems | Not built | Not started (README only) |
| 8 | 5 | Supervised Build, Deployment, and Defense | Not built (defense day, see `module-08-defense/`) | N/A, live supervised session |

All six built decks carry the automatic glossary (2026-09-24). Sessions 1 and 2 use
`lu-flow` diagrams; Sessions 3 to 6 not yet. `index.html` has cards for Sessions 1 to 4 only
(REPLAN-STATE 12).

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

**2026-09-23:** the instructor ran the lab end to end after his own
repairs (working directory steps in the README, a broader `smoke_test.py`)
and confirmed it works. Same day, the deck was re-audited: eleven slides
had drifted into overflow after later edits (content cut off at the
bottom, including reveals and answer rationales). All fixed, audit now
reports no overflow, at rest or fully revealed. Slide 12's drag-to-compare
widget, which hid half of each answer, became two side by side cards.
The deck is still due for its full rebuild (REPLAN-STATE item 7): from
15 content slides to about 33, every concept slide led by a picture,
diagrams in `lu-flow`, deeper coverage of the data and of profiling.
Targets in `COURSE-REPLAN.md` section 5.

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

### Lab dry run, 2026-09-19, two real bugs found and fixed

Actually ran the scriptable half of the lab end to end (real network,
real ROBOT 1.9.10, not just rdflib parse-checks) rather than trusting it
because it looked right. Found and fixed two bugs neither the earlier
build nor a parse check had caught:

- `robot report --profile QC` is not valid ROBOT syntax (`--profile`
  wants a custom rules file path, not a named preset), and the lecture
  slide's own terminal code sample showed the same invalid command.
  ROBOT's `report` also exits non-zero on ERROR-level violations, the
  normal case for an unfinished student ontology, so `robot_report.py`
  was one violation away from crashing on an otherwise-successful run.
  Fixed both in `robot_report.py` and in `lectures/kr-session-03.html`'s
  code sample: drop `--profile QC`, add `--fail-on none`.
- `demos/.gitignore` blanket-ignored `session-03-ontology/workspace/`,
  which silently dropped the three files `session-03-ontology/README.md`
  tells students to commit (`scro-extension.ttl`, `reasoned.ttl`,
  `report.tsv`), since both the fetch script and the Protege "Save As"
  step put them in that same folder. Narrowed the ignore to the fetched
  third-party material only; verified with `git check-ignore` and a real
  `git add` that the right files go either way.

Committed `dd07c41`. Not yet checked, flagged here rather than changed:
slide 16 ("Query the ontology live")'s sandbox SPARQL data block
(`lectures/kr-session-03.html` around line 585) still declares
`ul:Shipment rdfs:subClassOf iof:MaterialTransport`, the same
illustrative class this session already found does not exist in real
SCRO and corrected to `ioc:Shipment` in `scro-extension-starter.ttl`.
That slide's data is an explicitly offline, self-contained sandbox (not
loaded against the real ontology), so it may be a deliberate
simplification rather than a bug, but it is inconsistent with the
now-corrected starter file. Worth a decision next time this file is
touched: match it to `ioc:Shipment` too, or leave it and say why.

## What's next

See `REPLAN-STATE.md` "Where to continue" (Session 1, items 6 and 7, then Session 3 item 2).
After the Sessions 1 to 3 rebuild: the Session 4 lab (only a template
today), confirming the Session 5 lab on a live Ontop, a visual pass on
Sessions 4 to 6, then Sessions 7 and 8 (deck and lab).

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
- Push discipline: since 2026-09-24 Claude pushes to `main` at the end of
  each work session, after a clean audit, using the token set up in
  REPLAN-STATE item 10. Never force push. A push to `main` publishes the
  course site through GitHub Pages. At the start of a session, check
  `git log origin/main..HEAD`; anything listed is unpushed work.
