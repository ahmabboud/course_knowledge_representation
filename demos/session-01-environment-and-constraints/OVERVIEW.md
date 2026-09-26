# Read first: what this lab is doing

This lab asks a simple project question:

> Before we model or validate data, what do the real datasets contain, and
> which rules can we support with evidence?

## The short story

You first verify the tools used later in the course. You then profile two real
supply chain datasets and turn observations into a constraint inventory. That
inventory is the evidence base for the ontology, SHACL shapes, and mappings in
later sessions.

```text
real datasets -> profiling and clustering -> evidence -> constraint inventory
```

## The tools in this lab

These tools answer different parts of the same question. They do not decide
which rules are true for you.

| Tool | What it does here | What it cannot decide |
|---|---|---|
| Python and `pandas` | Read the CSV files and count, group, and compare their values. | Whether an unusual value is an error or a legitimate exception. |
| ydata-profiling | Produces a first report of nulls, value ranges, duplicates, and distributions. | Whether a pattern should become a business rule. |
| OpenRefine | Groups near-identical spellings, such as codes with a space, dash, or typo. | Which spelling is the authoritative one. |
| Constraint inventory | Records the evidence, source, proposed rule, and open question. | Nothing automatically: it makes the modelling decision reviewable. |

The smoke test checks Python, Java, Docker, and Protégé because later labs use
them. It is an environment check, not part of the data analysis.

## The data you are using

| Source file | One row means | Why this lab needs it |
|---|---|---|
| `DataCoSupplyChainDataset.csv` | one order line | A wide operational dataset for profiling nulls, values, and near duplicates. |
| `OrderList.csv` | one Brunel order | A compact supply chain event used throughout later sessions. |
| Other Brunel CSV sheets | a plant, rate, product, or port relationship | They show why rules often span tables rather than one column. |

## How the items relate

For example, a profile may show that an order has a carrier code, a plant,
and a port. The `PlantPorts.csv` table can then show whether that plant is
permitted to use that port. The first observation is a value in one row; the
second is a relationship across tables. The constraint inventory must name
which kind of evidence supports a proposed rule.

## What each step proves

| Step | You run or edit | What it does | What you should understand afterward |
|---|---|---|---|
| 1 | `smoke_test.py` | Checks Python, Java, Docker, and Protégé. | Later work should fail because of data or logic, not an unknown installation. |
| 2 | `data/fetch_data.py` | Downloads the real datasets and exports Brunel sheets. | The course works from a known source, not invented examples. |
| 3 | `profiling.py` | Builds profiling reports and charts. | Counts, nulls, ranges, and distributions suggest questions, not automatic rules. |
| 4 | OpenRefine clustering | Groups near duplicate values. | Different spellings can hide a rule or a data cleaning decision. |
| 5 | `constraint_inventory_template.csv` | Records a rule, evidence, and source column or table. | A proposed rule needs evidence a reader can check. |

## The files and their roles

| File | Role | Do you edit it? |
|---|---|---|
| `smoke_test.py` | Environment check. | Run it. |
| `profiling.py` | Notebook style profiling workflow. | Run it and read its outputs. |
| `session1_facts.py` | Recomputes the numbers used in the Session 1 deck. | Run it if a number needs checking. |
| `constraint_inventory_template.csv` | Place to record evidence based rules. | Yes. |
| `reference-outputs/` | Recorded facts and clustering results. | Read only. |

## Terms you need first

| Term | Plain definition |
|---|---|
| **profile** | A summary of values, nulls, ranges, and distributions in data. |
| **constraint inventory** | A list of proposed rules, each tied to evidence and a source. |
| **clustering** | Grouping similar values to reveal likely duplicates or inconsistencies. |
| **evidence** | A reproducible observation that supports a rule or explains an exception. |

## How to judge an assertion

1. **Source fact:** a value or count in the downloaded dataset.
2. **Profiling result:** a statistic or cluster produced by a named tool run.
3. **Modelling decision:** a rule proposed for later RDF, OWL, or SHACL work.

Do not turn a pattern into a rule without recording its evidence and source.
Now return to the [lab README](README.md), then run the steps in order.
