# Session 2 lab: from tables to a graph you can query

**Why this lab exists:** to make the lecture concrete (triples, IRIs, RDFS,
SPARQL, RDF against a property graph) and to give you a working pipeline you
will reuse for your team project. Nothing is handed in or graded. The lab
works when you can explain what each step did and why the numbers came out
as they did.

**Read this first:** [What this lab is doing](OVERVIEW.md). It introduces the
Brunel data, the business problem, how the tables become a graph, the purpose
of each step, the role of each file, and the terms used below. Do not start
Part A until the overall story is clear.

Every number in `lectures/kr-session-02.html` comes from the files in
`reference-outputs/`, produced by these scripts on 2026-09-24.

## Before you start

- Shared setup from `demos/README.md` done in Session 1 (Python 3.12,
  Docker Desktop, `demos/.venv`, the data downloaded). Keep `demos/.venv`
  active.
- **Docker Desktop is open and running** (`docker info` answers). On Windows
  this needs WSL 2 and virtualization turned on; see `demos/README.md`.
- Step 1 runs from `demos/`; every other step from this folder,
  `demos/session-02-rdf-sparql/`.
- No Docker? Skip steps 1, 3 and 5 and use Oxigraph (step 4, and the
  checker in part B). You still see every concept except Neo4j.

## Part A · build and query the graph (about 30 minutes)

1. From `demos/`: `docker compose up -d`. Starts Fuseki 5.5 (port 3030, no
   login; the first run builds it from Apache's release, about a minute) and
   Neo4j (port 7474, user `neo4j`, password `kr-labs-pw`). Both run locally
   in Docker on your computer only.
2. `python convert_to_rdf.py` (about 20 seconds). Converts OrderList,
   PlantPorts, ProductsPerPlant and FreightRates with rdflib and the IRI
   scheme in `common/iri.py`. **Expect:** `brunel.ttl` (135,841 triples),
   `brunel.trig` (5 named graphs, one per table plus the schema), `sample/`
   (one order in Turtle, N-Triples and JSON-LD). **Look at:**
   `sample/order.ttl`, and find the row you met in Session 1. Then
   `python named_graphs.py`. **Expect:** five named graphs with their triple
   counts (OrderList 119,844, FreightRates 12,320, ProductsPerPlant 3,576,
   PlantPorts 52, schema 49), the table on the named graphs slide.
   **Notice:** the rate bands, which are blank nodes, all live in the
   FreightRates graph, so each triple still says which table it came from.
3. `python load_fuseki.py`. **Expect:** `135841 triples loaded`. Then open
   <http://localhost:3030>, dataset `kr`, tab **query**, paste Q2 from
   `queries.sparql`, press the run arrow.
4. `python run_queries.py` (Fuseki) or `python run_queries.py oxigraph`
   (no Docker). Runs the seven questions and prints each answer and its
   time. **Expect:** the table below.
5. `python neo4j_comparison.py`. Loads the same orders into Neo4j and asks
   the same questions in Cypher. Then open <http://localhost:7474> and run
   `MATCH (o:Order {id: '1447296446.7'})-[r]->(n) RETURN o, r, n`.
   **Notice:** Q5 needs the order hierarchy written into the Cypher query;
   in RDF it is data (`rdfs:subClassOf`).

   **If Neo4j refuses the password** ("unauthorized"): the Neo4j answering
   on port 7687 is not the course's. Either another Neo4j container is
   running (`docker ps`; stop it with `docker stop <name>`), or the course's
   data volume was first created with a different password (Neo4j only reads
   `NEO4J_AUTH` the first time). From `demos/`: `docker compose rm -sf neo4j`,
   `docker volume rm demos_neo4j-data`, then `docker compose up -d neo4j`,
   and wait about 20 seconds before running the step again.

| Question | Expected answer |
|---|---|
| Q1 orders carried by V44_3 | 5 rows (the query stops at 5), every one service level CRF; which 5 depends on the store |
| Q2 orders and late orders per carrier | V444_0: 6,264 and 183 · V444_1: 2,097 and 9 · V44_3: 854 and 0 |
| Q3 carriers with a freight rate | V44_3 has 0 rate bands |
| Q4 any order leaving through a port its plant does not serve? | false |
| Q5 orders typed Order, and with subclasses | 9,023, and 9,215 |
| Q6 orders on a priced lane whose weight falls in no rate band | 1,370 (of 8,361), as in Session 1 |
| Q7 CONSTRUCT carrier serves plant | 12 new triples |

Q6 took 172 seconds written with `FILTER NOT EXISTS` and under 3 seconds
rewritten as one join plus a group (both on Oxigraph, same answer). Read
both versions in `queries.sparql` and say why. Then think about the
warning under version 2: without its `FILTER EXISTS` line it answers 2,224.
Which 854 orders did it add, and why does Session 1 say they have no rate?

## Part B · write your own queries (about 20 minutes)

Open `my_queries.sparql`. It asks three questions, each practising one idea
from the lecture: Y1 grouping, Y2 absence (`FILTER NOT EXISTS`), Y3 a
condition on a group (`HAVING`). `DISTINCT`, `HAVING` and a `SELECT`
inside a `SELECT` work in SPARQL exactly as in SQL. For models, Q4 in
`queries.sparql` uses `FILTER NOT EXISTS` and Q6 puts a `SELECT` inside a
`SELECT`. Write each query under its marker, then:

```sh
python check_my_queries.py            # Oxigraph, no Docker needed
python check_my_queries.py fuseki     # or against your Fuseki
```

The checker says, per question, right or not yet, with a hint. Any query
that returns the right answer counts. Stuck after trying?
`solutions/my_queries_solutions.sparql`. Test your queries in the Fuseki
page first if you like: the error messages there are clearer.

## Part C · think about names (about 10 minutes)

Read `common/iri.py` (the course convention, `AGENTS.md` 2d). Answer for
yourself, then in the closing discussion:

1. What does each part of `https://ul.edu.lb/kr/id/order/brunel/1447296446.7`
   protect against?
2. A second system arrives with its own order `1447296446.7`. What happens?
3. Sketch the same kind of scheme for **your team project's own database**:
   which kinds of things, which source name, which key.

## Optional

- `lab_walkthrough.py` runs parts A's steps 2 to 5 as notebook cells with
  tables and a timing chart. In **VS Code**: open it and click **Run Cell**
  above each `# %%`. In **JupyterLab**: right-click the file, **Open With →
  Notebook**.
- Instructor demo: `pip install owlrl`, then `python rdfs_entailment_demo.py`.
  RDFS turns a careless triple into a new "fact" instead of an error.

## You understood this lab if you can say

- why a foreign key in a table became an edge, and a rate band a blank node;
- why Q5 gives two different counts, and what RDFS has to do with it;
- why the same Q6 answer can take 172 seconds or 3;
- what RDF gives you that Neo4j did not, and the other way round.

## Take it to your team project

- `convert_to_rdf.py` is the template for converting your own tables.
- Your IRI scheme sketch from part C is the start of your project's naming.
- Your own questions, written like Y1 to Y3, become the questions your
  graph must answer; keep the timings, they belong in your report.
- Decide early: RDF or property graph for your topic, and why. You defend
  that choice at the end.
