# Session 2 lab: from tables to a graph you can query

Builds the syllabus deliverable: a loaded SPARQL endpoint over the Brunel
data, a documented IRI scheme, and the question set answered with timings.
Every number in `lectures/kr-session-02.html` comes from the files in
`reference-outputs/`, produced by the scripts below on 2026-09-24.

## Working directory

Finish the shared setup in `demos/README.md` first and keep `demos/.venv`
active. Step 1 runs from `demos/`; every other step runs from this folder,
`demos/session-02-rdf-sparql/`.

## Run, in order (about 60 minutes)

1. From `demos/`: `docker compose up -d`. Starts Fuseki (port 3030, user
   `admin`, password `admin`) and Neo4j (port 7474, user `neo4j`, password
   `kr-labs-pw`).
2. `python convert_to_rdf.py` (about 20 seconds). Converts OrderList,
   PlantPorts, ProductsPerPlant and FreightRates with rdflib and the IRI
   scheme in `common/iri.py`. Writes `brunel.ttl` (135,841 triples),
   `brunel.trig` (the same triples in 5 named graphs, one per table plus the
   schema) and `sample/` (one order in Turtle, N-Triples and JSON-LD).
3. `python load_fuseki.py`. Loads `brunel.ttl` into the `kr` dataset (TDB2)
   and checks the endpoint answers: `135841 triples loaded`. Then open
   <http://localhost:3030>, dataset `kr`, tab **query**, and paste any query
   from `queries.sparql`.
4. `python run_queries.py` (against Fuseki) or `python run_queries.py
   oxigraph` (no Java, no Docker: pyoxigraph inside Python). Runs the seven
   questions in `queries.sparql` and writes timings to `reference-outputs/`.
   If Fuseki or Java fails in the room, use Oxigraph and keep going.
5. `python neo4j_comparison.py`. Loads the same orders into Neo4j and asks
   the same questions in Cypher. Then open <http://localhost:7474> and run
   `MATCH (o:Order {id: '1447296446.7'})-[r]->(n) RETURN o, r, n`.
6. Optional, instructor demo: `pip install owlrl`, then
   `python rdfs_entailment_demo.py`. RDFS turns a careless triple into a new
   "fact" instead of an error.

`lab_walkthrough.py` runs stages 2 to 5 as notebook cells (JupyterLab or VS
Code), with tables and a timing chart.

## What the questions show (real answers)

| Question | Answer |
|---|---|
| Q2 orders and late orders per carrier | V444_0: 6,264 and 183 · V444_1: 2,097 and 9 · V44_3: 854 and 0 |
| Q3 carriers with a freight rate | V44_3 has 0 rate bands |
| Q4 any order leaving through a port its plant does not serve? | false |
| Q5 orders typed Order, and with subclasses | 9,023, and 9,215 |
| Q6 orders whose weight falls in no rate band | 1,370 |

Q6 took 172 seconds written with `FILTER NOT EXISTS` and under 3 seconds
rewritten as one join plus a group (both on Oxigraph, same answer). That is
the "where does the time go" part of the deliverable.

## What "done" looks like

A loaded endpoint that answers all seven questions, your own IRI scheme
written in three lines (what an IRI contains, why, and what happens when a
second source arrives), and a table of your timings. The IRI scheme agreed by
the room goes into `common/iri.py`; Session 3 onward imports it.
