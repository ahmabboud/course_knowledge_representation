# Read first: what this lab is doing

Do not begin with a command. First understand the question this lab asks:

> The data lives in a company database that changes every day. How do we
> keep a graph of it without writing a new converter each time, and how do
> we know that two systems mean the same customer?

This is an individual practice lab. Nothing is submitted or graded.

## The short story

In Session 2 a Python script, `convert_to_rdf.py`, read four Brunel CSV files
and wrote a graph. That works once. A real company keeps this data in a
relational database, and the rows change every day.

Today the same four tables sit in a database, PostgreSQL. Instead of a
script, we write a **mapping**: a file that says, table by table, which
triples each row becomes. The mapping is written in R2RML, a W3C standard,
so different tools can run it:

- **Morph-KGC materializes:** it reads the tables once and writes the whole
  graph to a file. Then we check that file against Session 2's graph, and
  run Session 4's shapes on it.
- **Ontop virtualizes:** it keeps no graph at all. It turns each SPARQL
  question into SQL, asks the database, and turns the rows into answers.

Last, a second system (a transport management system, TMS) lists the same
customers under slightly different codes. Matching them is **entity
resolution**, and we measure how often the matcher is wrong.

```text
Brunel CSV tables
        |
        | load_database.py
        v
PostgreSQL (or brunel.db, without Docker)
        |                               \
        | brunel-mapping.ttl (R2RML)     \ the same mapping
        v                                 v
materialize.py: Morph-KGC           ontop/run_ontop.py: Ontop
   writes brunel-mapped.nt             SPARQL in, SQL to the database,
        |                              answers out; nothing stored
        | compare_with_session2.py
        | Session 4's validate.py
        v
the same graph as Session 2, now checked

er/tms-customers.csv  +  Brunel's customers
        |
        | er/match_customers.py
        v
matches, with precision and recall
```

## The data you are using

The database holds the four Brunel tables Session 2 converted (Brunel
University London, *Supply Chain Logistics Problem Dataset*, Figshare
7558679 v2, CC BY 4.0; see [`../data/README.md`](../data/README.md)).

| Database table | From | One row means | Why this lab needs it |
|---|---|---|---|
| `orders` | `OrderList.csv` | one order (9,215 rows) | The main triples map: an order, its carrier, plant, ports, customer, product, weight. |
| `plant_ports` | `PlantPorts.csv` | one permitted plant to port link (22) | Plants and ports, and `servesPort`. |
| `products_per_plant` | `ProductsPerPlant.csv` | one product a plant makes (2,036) | Products, and `makes`. |
| `freight_rates` | `FreightRates.csv` | one price band (1,540), plus `rate_id` | Rate bands. The source has no key: see below. |

Two more files:

- `er/tms-customers.csv` is **teaching data**, made by
  `er/make_teaching_set.py`. It pretends a second system exported Brunel's
  46 real customers, with realistic drift in the codes (lower case, a dash,
  spaces, a padded number, a lost letter, a lost 5, two digits swapped),
  plus 6 customers that are not in Brunel. `er/truth.csv` says which is
  which. No real second system exists for this data, so the truth is known
  only because we built it.
- `vocabulary.ttl` is Session 2's vocabulary: the class and property names,
  and one rule, every late order is an order.

## How the items relate

A mapping builds a subject from a key, then adds properties:

```text
row of orders: order_id 1447296446.7, carrier V44_3, plant_code PLANT16, ...
        |
        | template  https://ul.edu.lb/kr/id/order/brunel/{order_id}
        v
order 1447296446.7  --carriedBy-->  carrier V44_3   (template .../carrier/brunel/{carrier})
order 1447296446.7  --weight-->     14.3             (column, datatype xsd:decimal)
```

The link to the carrier needs no join: the carrier's IRI is built from the
key in the order's own row, with the same template the carrier's own map
uses. That is why the naming rule of Session 2 matters so much.

A rate band has no key of its own: of 1,540 rows, only 1,258 differ on
carrier, ports, service and minimum weight, and 5 rows are exact copies of
another row. So a band gets no IRI; it becomes a blank node, one per row.

## What each step proves

| Step | You run | What it does | What you should understand afterward |
|---|---|---|---|
| 1 | `docker compose up -d` | Starts an empty PostgreSQL on this computer. | The source is a live database, not a file. |
| 2 | `load_database.py` | Loads the four Brunel tables. | Each CSV is now a table with rows and columns. |
| 3 | `materialize.py` | Morph-KGC runs `brunel-mapping.ttl` and writes `brunel-mapped.nt`. | A mapping is a declaration, not a program: the tool does the work. |
| 4 | `compare_with_session2.py` | Compares that graph with Session 2's, triple by triple. | Two routes, the same graph; the only difference is the 7 carriers the mapping now types. |
| 5 | `../session-04-shacl/validate.py` | Runs Session 4's shapes on the mapped graph. | The Session 4 triage fix works: 0 band carrier warnings instead of 1,209. The vocabulary must come with the data. |
| 6 | `ontop/run_ontop.py` | Ontop answers Session 2's Q2 from the database. | Virtualizing: answers straight from the tables, and the SQL Ontop wrote. |
| 7 | `er/match_customers.py` | Matches TMS customers to Brunel's, at two thresholds. | Every matcher makes mistakes; precision and recall say which kind. |
| B | `my_mapping.ttl`, `check_my_mapping.py` | You add three rules, each a copy of one already there with one thing changed. | Subject maps, links and datatypes are three small patterns. |
| C | questions | Materialize or virtualize, for your own project? | The choice depends on freshness, speed and checking. |

## The files and their roles

| File | Role | Do you edit it? |
|---|---|---|
| `docker-compose.yml` | Starts PostgreSQL 16 on 127.0.0.1:5432 (user `kr`, database `brunel`). | No. |
| `load_database.py` | Creates and fills the four tables (or `brunel.db` with `--sqlite`). | No; run it. |
| `brunel-mapping.ttl` | The course mapping, R2RML. | Read it; it is the model for your project. |
| `vocabulary.ttl` | Session 2's vocabulary, 49 triples. | No. |
| `materialize.py` | Runs Morph-KGC on a mapping and writes the graph. | No; run it. |
| `brunel-mapped.nt` | The materialized graph. Generated. | No; regenerate it. |
| `compare_with_session2.py` | Shows every difference with Session 2's graph. | No; run it. |
| `ontop/setup_ontop.py` | Downloads Ontop 5.5.0 and the PostgreSQL driver, once. | No; run it once. |
| `ontop/run_ontop.py`, `ontop/brunel.properties`, `ontop/q2-orders-per-carrier.sparql` | Ask Ontop one question and show its SQL. | You may write your own question file. |
| `er/make_teaching_set.py`, `er/tms-customers.csv`, `er/truth.csv` | The entity resolution teaching data, and how it was made. | No. |
| `er/match_customers.py` | The matcher, with its weights written out. | Read it; try another `--threshold`. |
| `my_mapping.ttl` | Your work area for Part B. | Yes. |
| `check_my_mapping.py` | Checks your three rules. | No. |
| `solutions/`, `reference-outputs/` | Answers, and a real run of every step. | Read them; do not edit. |

## Terms you need before running the lab

| Term | Plain definition |
|---|---|
| **mapping** | A file that says how rows of a table become triples. |
| **R2RML** | The W3C standard language for mappings from relational databases (2012). |
| **triples map** | One part of a mapping: one table or query, one kind of subject. |
| **template** | A pattern like `.../order/brunel/{order_id}` that builds an IRI from a column. |
| **logical view** | An SQL query used as the table of a triples map. |
| **materialize** | Produce the whole graph now and store it. |
| **virtualize** | Store nothing; answer each query from the database. |
| **Morph-KGC** | The tool that materializes our mapping. |
| **Ontop** | The tool that virtualizes it. |
| **entity resolution** | Deciding which records in two sources are the same real thing. |
| **precision / recall** | Of the matches found, how many are right / of the true matches, how many were found. |

## How to judge an assertion in this lab

1. **Source fact:** what the tables contain, such as 1,540 rate rows with no
   key, or carrier V44_3 on every CRF order.
2. **Course modelling decision:** how we map it, such as the IRI templates,
   a blank node per rate band, typing all 10 carriers.
3. **Result:** what a tool produced, such as 135,799 mapped triples, 1,370
   warnings, or precision 0.878 at threshold 4.

The entity resolution data is a fourth kind: **teaching data**, built on
purpose. Its numbers show how matching behaves; they say nothing about
Brunel.

Now return to the [lab README](README.md) and begin Part A.
