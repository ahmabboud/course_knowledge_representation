# KR labs

The instructor's own labs repository for **Knowledge Representation**.
Run by the instructor, live, in every session. Separate from
`kr-team-template`, which is what each student team clones for its own
project. This repository holds the real, runnable version of the
shared supply chain case: DataCo and Brunel, the same data every
session's lecture and lab work against.

The sandbox boxes inside the lecture slides (`course_knowledge_representation/lectures/`)
are toy examples: seven rows, no setup, runs in the browser. They exist
to teach a concept in two minutes. This repository is not that. It is
real code against the real datasets, with a real triplestore and a real
graph database, the thing actually run during the hands-on lab block of
each session.

## Structure

```
requirements.txt     Shared Python dependencies, every session
docker-compose.yml    Shared services: Fuseki (TDB2) and Neo4j
.env.example          Copy to .env once Session 7 needs an LLM key
common/                Shared code: IRI scheme, data paths, once
                       Session 2 fixes the IRI convention it does not
                       get reinvented every session after
data/                  Where DataCo and Brunel live once downloaded
                       (gitignored, see data/README.md)
session-01-environment-and-constraints/
session-02-rdf-sparql/
session-03-ontology/
session-04-shacl/
session-05-integration/
session-06-learning/
session-07-access-layer/
session-08-deploy-and-defend/
```

Sessions 1 through 3 have working lab code, matching the lab briefs in
their built lecture decks. Session 3 is a run-and-observe walkthrough,
not a build-it-yourself lab: `fetch_ontologies.py`, a finished
reference ontology, a competency-question reference doc, and the ROBOT
wrapper are all built and verified, and the Protege and reasoner steps
are run live in the room from those same finished files, nobody drafts
a competency question or extends an ontology in this one, see its own
README for why. Sessions 4 through 8 have a
README each, accurate to the syllabus segment text and naming the real
tools, but neither lab code nor a lecture deck yet (see
`course_knowledge_representation/README.md`'s status table), and
writing lab code ahead of the deck it serves risks locking in the
wrong shape. Build each session's lab code once that session's deck
exists, from its own README here.

## Setup, once

1. `python3 -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `docker compose up -d` — brings up Fuseki (`localhost:3030`) and
   Neo4j (`localhost:7474` browser, `localhost:7687` bolt). Individual
   sessions may add their own `docker-compose.yml` for a service only
   that session needs (PostgreSQL in Session 5, for example); run that
   session's compose file in addition to this one, not instead of it.
4. Copy `.env.example` to `.env` once you reach Session 7. Not needed
   before then.
5. See `data/README.md` and run its fetch step before Session 1.

## Conventions, so eight sessions of code still look like one thing

- One folder per session, numbered, so the order is never ambiguous.
- Each session folder's `README.md` states what it builds, which
  syllabus deliverable it produces, and which real tools it uses. Read
  it before the code.
- Shared code that more than one session needs (the IRI scheme, data
  paths) lives in `common/`, imported, never copy-pasted between
  session folders. The one exception is intentional: Session 2 fixes
  the cohort's IRI convention as a discussion outcome, so it lands in
  `common/iri.py` right after that session, not before.
- Notebooks for anything meant to be read and run step by step in the
  room; a plain `.py` script for anything meant to run once as a batch
  step (loading a container, materializing a graph). Both are fine,
  pick per task, not per session.
- Every function and every notebook cell that is not obvious from its
  name gets a comment saying what it does and, where it matters, why.
  This is taught from, so it has to read cleanly at the front of a
  room, not just run correctly.
- Real data, real containers, real errors. No mocked services standing
  in for Fuseki or Neo4j; if a demo needs to be resilient to a bad
  network day, that is a documented fallback (see Session 2's Oxigraph
  fallback), not a fake in place of the real thing.

## Data

DataCo and Brunel, per `data/README.md`. No personal, employer, or
client data in this repository, ever, same rule as everywhere else in
this course.
