# Read first: what this lab is doing

Do not begin with a command. First understand the question this lab asks:

> How can several operational tables become one graph that we can query for
> relationships, missing information, and business rules?

This is an individual practice lab. Nothing is submitted or graded. You are
not learning a command sequence; you are following one data pipeline from its
source tables to questions over a graph.

## The short story

Brunel is a supply-chain planning dataset. Its information is split across
separate tables. An order says which plant made it, which port it left from,
which carrier moved it, and which product it contains. Other tables say which
ports a plant may use, which products a plant makes, and which freight-rate
bands apply to a carrier, route, service level, and weight range.

Those tables are related, but a spreadsheet does not make all relationships
easy to follow. This lab converts selected rows into RDF facts. The facts form
one graph, so SPARQL can follow links across the former tables.

```text
Brunel CSV tables
        |
        | convert_to_rdf.py
        v
RDF graph: brunel.ttl / brunel.trig
        |
        | load_fuseki.py
        v
Fuseki: a local RDF database
        |
        | SPARQL queries
        v
Answers about carriers, routes, order types, and rate gaps
```

## The data you are using

The source is Brunel University London's *Supply Chain Logistics Problem
Dataset*, Figshare article 7558679, version 2, licensed CC BY 4.0. The course
download script verifies the publisher's checksums. See
[`../data/README.md`](../data/README.md) for the source and all seven tables.

This lab deliberately uses four of those tables:

| Source table | One row means | Why this lab needs it |
|---|---|---|
| `OrderList.csv` | one order | The central business event: its plant, ports, carrier, customer, product, weight, service level, and late days become facts about an order. |
| `PlantPorts.csv` | one permitted plant-to-port link | Lets us ask whether an order leaves through a port that its plant serves. |
| `ProductsPerPlant.csv` | one product a plant can make | Makes production capability an explicit graph relationship. |
| `FreightRates.csv` | one carrier price for a route, service level, and weight range | Lets us find orders with no matching price band. |

The full source workbook also has warehouse costs, capacities, and VMI
customers. We do not convert those in Session 2. That is a teaching scope
decision, not a claim that they are irrelevant. They remain available for a
later project or mapping.

### The business question behind the lab

The graph must make it possible to ask questions such as:

- Which carrier handled each order, and how many of its orders were late?
- Does an order leave through a port that its plant is permitted to use?
- Does a carrier have freight-rate bands for its work?
- Does an order's weight fit at least one rate band on its route?

The last question matters because a missing rate band can signal a data-quality
or pricing problem. It is not proof that an order is wrong. In this dataset,
`V44_3` has 854 CRF orders but no rate bands in `FreightRates.csv`; that is a
fact of these source tables, not an inference that the carrier did not price
the work elsewhere.

## How the items relate

For one order, the converter creates facts like these:

```text
order 1447296446.7  --fromPlant-->  PLANT03
order 1447296446.7  --shipsFrom--> port
order 1447296446.7  --carriedBy--> carrier V44_3
PLANT03             --servesPort--> port
```

The same real thing receives the same IRI whenever it appears. For example,
the carrier code `V44_3` becomes
`https://ul.edu.lb/kr/id/carrier/brunel/V44_3`. That is why facts from the
order table and facts from the rate table can meet at the same carrier node.

A freight-rate band is different. The source gives it no separate stable key;
it is defined only by its carrier, route, service level, and weight interval.
The converter therefore represents it as an RDF blank node. This is a modelling
decision: do not invent a permanent identifier for a source record that lacks
one.

## What each step proves

| Step | You run | What it does | What you should understand afterward |
|---|---|---|---|
| 1 | `docker compose up -d` | Starts Fuseki and Neo4j locally in Docker. | A graph database is a service on your own computer, not a website shared with the class. |
| 2 | `convert_to_rdf.py` | Reads the four CSV files and writes RDF. | A table row becomes several linked facts; foreign-key-like values become links between shared things. |
| 2a | `named_graphs.py` | Counts facts in each source-specific graph in `brunel.trig`. | Named graphs preserve where a fact came from. |
| 3 | `load_fuseki.py` | Replaces the contents of Fuseki's `/kr` dataset with `brunel.ttl`. | A Turtle file can be loaded into an RDF database and queried over HTTP. |
| 4 | `run_queries.py` | Runs seven SPARQL questions and records their results. | SPARQL can follow links, count groups, test absence, traverse a class hierarchy, and construct new facts. |
| 5 | `neo4j_comparison.py` | Loads a smaller comparison graph into Neo4j and runs related Cypher questions. | RDF/RDFS keeps the order hierarchy as data; this Neo4j example writes that hierarchy into the query. |
| B | `my_queries.sparql` and `check_my_queries.py` | You write three queries; the checker compares their answers with the reference answers. | A query is correct because it returns the right result, not because it copies a particular solution. |
| C | `common/iri.py` | You inspect the naming rule and design one for your project. | A stable identifier needs a kind, source system, and source key. |

## The files and their roles

| File | Role | Do you edit it? |
|---|---|---|
| `convert_to_rdf.py` | The course converter: CSV rows to RDF triples, schema, and example serializations. Uses `pandas` to read CSV and `rdflib` to write standard RDF. | Read it; use it as a project template later. |
| `common/iri.py` | The course naming rule. It mints IRIs from kind, source system, and original source key; it is not a lookup dictionary. | Read only. Make your project's equivalent in your own project. |
| `brunel.ttl` | One RDF graph, used by Fuseki and the query scripts. Generated in step 2. | Do not hand-edit; regenerate it. |
| `brunel.trig` | The same facts separated into named graphs by source table. Generated in step 2. | Do not hand-edit; regenerate it. |
| `sample/order.ttl` | One converted order, kept small enough to inspect. | Read it after step 2. |
| `load_fuseki.py` | Uploads `brunel.ttl` to the local Fuseki `/kr` dataset and counts the loaded triples. | Run it in step 3. |
| `queries.sparql` | The seven course SPARQL examples. | Read and run; use them as models. |
| `run_queries.py` | Sends the course queries to Fuseki, or runs them with the Docker-free Oxigraph fallback. | Run it in step 4. |
| `my_queries.sparql` | Three unfinished questions for you to write. | Yes, this is your work area. |
| `check_my_queries.py` | Checks the answers returned by your queries and gives hints. | Run it; do not change its expected answers. |
| `neo4j_comparison.py` | A deliberately smaller property-graph comparison. | Run it in step 5 if Docker is available. |
| `reference-outputs/` | Recorded results from a real course run. | Use it to check a surprising result; do not treat it as data to edit. |

## Terms you need before running the lab

| Term | Plain definition |
|---|---|
| **RDF** | A standard way to express facts as subject–relationship–object triples. |
| **triple** | One RDF fact, such as `an order — carried by — a carrier`. |
| **graph** | A set of linked triples. |
| **IRI** | A globally unique identifier written like a web address. It identifies a thing even if opening it in a browser shows nothing. |
| **Turtle (`.ttl`)** | A readable text format for RDF. |
| **named graph** | A labelled group of triples; here, one group per source table plus the schema. |
| **blank node** | A graph node with no global identifier; here, a rate band with no source key of its own. |
| **RDFS** | A small vocabulary for describing classes, properties, and class hierarchies. It can derive additional type information; it does not reject bad data. |
| **SPARQL** | The query language for RDF graphs. |
| **Fuseki** | The local RDF database server that stores the `kr` graph and accepts SPARQL queries. |
| **Cypher** | Neo4j's query language for property graphs. |
| **Oxigraph** | The Python-based local fallback used when Docker or a server is unavailable. |

## How to judge an assertion in this lab

Keep three categories separate:

1. **Source fact:** a value present in Brunel's CSV files, such as an order's
   carrier or the absence of a `V44_3` row in `FreightRates.csv`.
2. **Course modelling decision:** how the course represents that fact, such as
   using an IRI for an order, a blank node for a rate band, or putting a class
   hierarchy into RDFS.
3. **Query result:** an answer produced from those facts and decisions, such as
   the 1,370 orders that have a priced lane but no matching weight band.

When a number surprises you, reproduce it with the relevant script, then look
in `reference-outputs/`. The files record the source, converter, and query
result used for the lecture; they do not turn an interpretation into a source
fact.

Now return to the [lab README](README.md) and begin Part A.
