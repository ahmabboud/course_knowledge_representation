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
requirements.txt     Pinned shared Python dependencies, Sessions 1 to 6
requirements-nodeps.txt  Morph-KGC (Session 5), installed with --no-deps
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

Each session folder has its own `README.md`: why the lab exists, the steps,
what to expect at each step, and what to take to the team project. Labs are
individual and nothing is handed in; they exist to make the concepts
concrete and to prepare the capstone. Status per session is in
`../PROGRESS.md`.

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
| JDK 21 (checked by the Session 1 smoke test; first used in Session 3 for ROBOT) | Run `brew install openjdk@21`, then register it once: `sudo ln -sfn /opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-21.jdk`. Verify with `java -version`. | Install the JDK 21 LTS release from [Eclipse Temurin](https://adoptium.net/temurin/releases/?version=21&package=jdk), or run `winget install EclipseAdoptium.Temurin.21.JDK`. Close and reopen PowerShell, then verify with `java -version`. |
| Docker Desktop | Install [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/), open it, and wait until it reports that the engine is running. Verify with `docker info`. Give it at least 4 GB of memory (Settings, Resources). | Install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/), completing its WSL 2 or virtualization prompts. Needs administrator rights once, and virtualization turned on in the BIOS (Task Manager, Performance, CPU shows "Virtualization: Enabled"). Open it and verify with `docker info`. If Docker cannot run on your laptop, tell the instructor in Session 1; Session 2 has a Python-only fallback (Oxigraph). |
| Protégé Desktop | Download [Protégé Desktop](https://protege.stanford.edu/software/), move `Protégé.app` to `/Applications`, and open it once. | Download [Protégé Desktop](https://protege.stanford.edu/software/), use the Windows installer if offered, and open it once. If using a ZIP distribution, extract it under `%LOCALAPPDATA%\Programs\Protege-<version>` so the smoke test can locate it. |

## Setup, once

### macOS or Linux

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-deps -r requirements-nodeps.txt
```

### Windows (PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install --no-deps -r requirements-nodeps.txt
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
2. Before Session 2, run `docker compose up -d`. The first time, it builds
   the Fuseki image from Apache's own 5.5.0 release (`fuseki/Dockerfile`,
   about a minute, needs internet). This starts Fuseki
   (`localhost:3030`, no login) and Neo4j (`localhost:7474` browser,
   `localhost:7687` bolt), both reachable from this computer only. Individual sessions may add their own
   `docker-compose.yml` for a service only that session needs (PostgreSQL in
   Session 5, for example); run that session's compose file in addition to
   this one, not instead of it.
3. Copy `.env.example` to `.env` once you reach Session 7. Not needed
   before then.
4. See `data/README.md` and run its fetch step before Session 1.

## Session-specific environments

The root `requirements.txt` is one shared environment for Sessions 1
through 6. The second install line adds Morph-KGC (Session 5) without its
declared dependencies: its package asks for `rdflib` below 7.3 and
`pyoxigraph` below 0.4, but it runs unchanged on the course's 7.6.0 and
0.5.11 (tested 2026-09-25), and its real dependencies are pinned in
`requirements.txt`. `pip check` therefore reports two Morph-KGC lines; that
is expected. Already set up before Session 5? Run both install lines again
in the active environment. Session 6 adds PyTorch (CPU), PyTorch Geometric,
PyKEEN and scikit-learn, about 400 MB. On macOS and Windows the normal
install gets the CPU build. **On Linux**, install the CPU build first, or pip
downloads about 2 GB of GPU libraries:
`python -m pip install torch==2.8.0 --index-url https://download.pytorch.org/whl/cpu`,
then the two install lines.

## Conventions, so eight sessions of code still look like one thing

- One folder per session, numbered, so the order is never ambiguous.
- Each session folder's `README.md` states what it builds, which
  syllabus deliverable it produces, and which real tools it uses. Read
  it before the code.
- Shared code that more than one session needs (the IRI scheme, data
  paths) lives in `common/`, imported, never copy-pasted between
  session folders. The IRI convention is fixed in `common/iri.py`
  (`AGENTS.md` 2d); Session 2 discusses it, it does not reinvent it.
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
