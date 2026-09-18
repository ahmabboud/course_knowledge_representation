# Session 2 lab: RDF conversion, SPARQL, and a Neo4j comparison

Builds the syllabus deliverable: a loaded SPARQL endpoint over a supply
chain data slice, a documented IRI scheme, and a query notebook
answering the provided question set with timings, per
`course_knowledge_representation/lectures/kr-session-02.html`'s lab
brief slide.

## Run, in order

1. From the repository root: `docker compose up -d` (Fuseki and Neo4j).
2. `python convert_to_rdf.py` — converts a slice of the Brunel tables to
   Turtle with rdflib, using `common/iri.py`'s scheme. Writes
   `brunel_slice.ttl` next to this README.
3. `python load_fuseki.py` — loads `brunel_slice.ttl` into the `kr`
   dataset on the running Fuseki container and confirms the endpoint
   answers a trivial query. If Fuseki or the JDK misbehaves, switch
   `TRIPLESTORE = "oxigraph"` at the top of `run_queries.py` instead of
   debugging Java live in the room, per the lecture's own fallback
   guidance.
4. `python run_queries.py` — works through `queries.sparql`'s question
   set against the loaded endpoint, printing each result and its
   timing.
5. `python neo4j_comparison.py` — loads the same slice into the Neo4j
   container and runs the equivalent multi-hop Cypher query, printed
   next to the SPARQL version for the room to compare, not scored
   against each other.

## Real tools, matching the lecture

- **rdflib** for the conversion.
- **Fuseki with TDB2** as the primary endpoint; **pyoxigraph** as the
  documented fallback above roughly a million triples or when the JDK
  setup fails.
- **Neo4j Community** with the `neo4j` Python driver for the comparison
  segment.

## What "done" looks like

A loaded endpoint that answers every question in `queries.sparql`, a
documented IRI scheme (`common/iri.py`, updated once the cohort agrees
its final form in the discussion block), and timings recorded for each
query. This IRI scheme is what Session 3 onward imports, get it right,
or at least get it written down, here.
