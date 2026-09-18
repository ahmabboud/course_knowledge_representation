# Session 5 lab: RML mapping, materialize versus virtualize, entity resolution

Not built yet. This README states what the syllabus already commits
to.

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
at the repository root), RML / Morph-KGC, the RML Playground (browser
fallback), Ontop.

## What will live here once built

- `docker-compose.yml` — a PostgreSQL service, run alongside the
  repository root's `docker-compose.yml`, not instead of it.
- `load_postgres.py` — loads DataCo into the container.
- `mapping_template.rml.ttl` — a starting RML mapping to the Session 3
  ontology.
- `compare_materialize_vs_virtualize.md` — where the freshness/latency/
  workload comparison gets written down, live, during the lab.

## What "done" looks like

A correct RML mapping, both paths working over the same data, an
entity resolution layer reporting precision and recall (not a single
accuracy figure) if the topic combines two sources, per the Session 5
deliverable.
