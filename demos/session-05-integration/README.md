# Session 5 lab: RML mapping, materialize versus virtualize, entity resolution

## What the syllabus commits to

Load DataCo into a provided **PostgreSQL** container, a genuine
relational source rather than a CSV pretending to be one. Write an RML
mapping from that schema to the Session 3 ontology and materialize the
graph with **Morph-KGC** (drafting in the browser-based RML Playground
first if the local toolchain misbehaves). Configure **Ontop** over the
same database and ontology, answer the same SPARQL questions by
virtualization, and inspect the SQL Ontop generates. Compare the two on
freshness, latency, and which queries each handles badly. Run the
Session 4 shapes against the result. A 10-minute team clinic: each team
states which integration architecture its own project will use and
why.

## Real tools

PostgreSQL (own container, additive to the shared `docker-compose.yml`
at the repository root), RML / Morph-KGC 2.10.0, Ontop 5.5.0, Splink
4.0.

## Status

Built and tested against a real Postgres container (schema, both
mapping paths, and the entity resolution script all produce the
numbers documented below); **not yet confirmed against the real Ontop
CLI on a live database from this machine**, that step needs a
container runtime this environment cannot use, see the note under
Ontop below. Do not treat this folder as the finished Milestone-2
lab until that confirmation and a live run-through are both done.

### What's here

- `docker-compose.yml` — the PostgreSQL service, run alongside the
  repository root's `docker-compose.yml`, not instead of it.
- `load_postgres.py` — loads a small, hand-built purchase-order and
  carrier seed (real DataCo/Brunel data was not available while
  building this, see its own docstring for why and how to swap in the
  real fetched CSVs later).
- `mapping_template.rml.ttl` + `config_materialize.ini` — the RML
  mapping and Morph-KGC config for the materialize path. Real,
  verified output: with `po99`'s carrier code absent from the
  `carriers` table, materializing produces every triple for `po99`
  except `ul:hasCarrier`, silently, no error.
- `ontology.ttl`, `mapping.obda`, `ontop.properties`, `query.sparql` —
  the Ontop virtualize path over the same Postgres source, verified
  for real (CLI flags and mapping syntax checked against the actual
  downloaded 5.5.0 distribution) but **not yet run against a live
  database**: this repository's own tooling cannot start a Postgres
  container to test it end to end (see Status). Run it yourself with
  `ONTOP_LOG_LEVEL=debug` and paste the generated SQL into
  `compare_materialize_vs_virtualize.md` the first time you do.
- `validate_materialized.py` — runs Session 4's shapes against
  `materialized.nt`. Not a plain `pyshacl` CLI call, its own docstring
  explains why (a real, confirmed prefix-resolution gotcha, not a
  maybe).
- `entity_resolution/` — Splink over two synthetic supplier lists
  (DataCo-style and Brunel-style) describing five of the same real
  suppliers under different names and IDs. Real, run output:
  `threshold_match_probability=0.5` gives precision 0.556 / recall
  1.000 (4 false positives, all same-country pairs); raising it to 0.8
  gives 1.000 / 1.000. Swap in your own team's two sources and labeled
  sample once you have one.
- `compare_materialize_vs_virtualize.md` — where the freshness/latency/
  workload comparison and the clinic's decision get written down, live,
  during the lab.

### Working directory and platform status

Run the commands below from `demos/session-05-integration/`. The documented
setup block is currently for macOS/Linux shells only: it uses `source`,
`curl`, `unzip`, `chmod`, and Unix environment-variable syntax. This session
has not yet been verified end to end on Windows, so it must not be presented
as a Windows-ready lab until a PowerShell recipe and a Windows reference run
are added.

### Setup

```bash
docker compose -f ../docker-compose.yml -f docker-compose.yml up -d

# Load the seed data
python3 -m venv .venv-pg && source .venv-pg/bin/activate
python -m pip install -r requirements-postgres.txt
python3 load_postgres.py
deactivate

# Materialize path, its own venv (see load_postgres.py's docstring
# for why morph-kgc and pyshacl cannot share one environment)
python3 -m venv .venv-materialize && source .venv-materialize/bin/activate
python -m pip install -r requirements-materialize.txt
python3 -m morph_kgc config_materialize.ini   # writes materialized.nt
deactivate

# Validate with Session 4's shapes, the repository's shared venv
source ../.venv/bin/activate
python3 validate_materialized.py

# Virtualize path
curl -sSL -o ontop-cli.zip https://github.com/ontop/ontop/releases/download/ontop-5.5.0/ontop-cli-5.5.0.zip
unzip -q ontop-cli.zip -d ontop-cli
curl -sSL -o ontop-cli/jdbc/postgresql.jar https://jdbc.postgresql.org/download/postgresql-42.7.4.jar
chmod +x ontop-cli/ontop
ONTOP_LOG_LEVEL=debug ontop-cli/ontop query -m mapping.obda -t ontology.ttl \
  -p ontop.properties -q query.sparql -o ontop_results.csv

# Entity resolution
cd entity_resolution
python3 -m venv .venv-er && source .venv-er/bin/activate
python -m pip install -r requirements.txt
python3 run_splink.py
```

## What "done" looks like

A correct RML mapping, both paths working over the same data, an
entity resolution layer reporting precision and recall (not a single
accuracy figure) if the topic combines two sources, per the Session 5
deliverable, plus a live Ontop run confirmed on this machine and the
comparison doc filled in from that real run, not left as placeholders.
