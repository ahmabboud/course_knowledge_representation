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
requirements.txt     Pinned shared Python dependencies, Sessions 1 to 4
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

## Start here: the lab repository root

This README lives in the lab repository root, referred to below as
`DEMO_ROOT`. It is the folder containing `requirements.txt`,
`docker-compose.yml`, `data/`, and all `session-*/` folders. Open a terminal
in this folder before following the setup instructions. A quick check:

```text
DEMO_ROOT/
  requirements.txt
  docker-compose.yml
  data/
  session-01-environment-and-constraints/
```

Do not create the virtual environment inside a session folder.

## Install prerequisites

Install these once before creating the virtual environment. The supported
Python range is 3.12 or 3.13; do not use Python 3.14 for this repository yet.
After installing the four tools, run Session 1's `smoke_test.py` to verify the
machine rather than guessing from an installer window.

| Tool | macOS | Windows |
| --- | --- | --- |
| Python 3.12 | Install from [Python.org](https://www.python.org/downloads/) or run `brew install python@3.12`; verify with `python3.12 --version`. | Install Python 3.12 from [Python.org](https://www.python.org/downloads/windows/) or run `winget install Python.Python.3.12`; verify with `py -3.12 --version`. |
| JDK 21 | Run `brew install openjdk@21`, then register it once: `sudo ln -sfn /opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-21.jdk`. Verify with `java -version`. | Install the JDK 21 LTS release from [Eclipse Temurin](https://adoptium.net/temurin/releases/?version=21&package=jdk), or run `winget install EclipseAdoptium.Temurin.21.JDK`. Close and reopen PowerShell, then verify with `java -version`. |
| Docker Desktop | Install [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/), open it, and wait until it reports that the engine is running. Verify with `docker info`. | Install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/), completing its WSL 2 or virtualization prompts. Open it and verify with `docker info`. |
| Protégé Desktop | Download [Protégé Desktop](https://protege.stanford.edu/software/), move `Protégé.app` to `/Applications`, and open it once. | Download [Protégé Desktop](https://protege.stanford.edu/software/), use the Windows installer if offered, and open it once. If using a ZIP distribution, extract it under `%LOCALAPPDATA%\Programs\Protege-<version>` so the smoke test can locate it. |

## Setup, once

### macOS or Linux

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Check `python3.12 --version` (macOS/Linux) or `py -3.12 --version`
(Windows) before creating the environment. Python 3.14 is currently too new
for the Session 1 profiling dependency.

If PowerShell blocks activation, run
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal,
then run the activation command again. This changes the policy only for the
current terminal session.

After activating the environment on either platform:

1. Start Docker Desktop and run `docker info`. Session 1's smoke test checks
   that Docker's engine is reachable; it does not start any course service.
2. Before Session 2, run `docker compose up -d`. This starts Fuseki
   (`localhost:3030`) and Neo4j (`localhost:7474` browser,
   `localhost:7687` bolt). Individual sessions may add their own
   `docker-compose.yml` for a service only that session needs (PostgreSQL in
   Session 5, for example); run that session's compose file in addition to
   this one, not instead of it.
3. Copy `.env.example` to `.env` once you reach Session 7. Not needed
   before then.
4. See `data/README.md` and run its fetch step before Session 1.

## Session-specific environments

The root `requirements.txt` is intentionally installable as one shared
environment for Sessions 1 through 4. Session 5's Morph-KGC materialization
uses an incompatible `rdflib` range, and Session 6's graph-learning stack
uses an incompatible pandas range. Their pinned requirements files live next
to those labs and are installed only into their own virtual environments, as
their READMEs specify.

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
