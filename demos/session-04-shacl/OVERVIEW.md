# Read first: what this lab is doing

In this lab we check the Brunel graph with **SHACL**, and we learn to read the
result. SHACL is a language for writing data rules that a computer can check.

> **The lab in one sentence:** we write rules about the data, run them on the
> real graph, and find that the first report shows 3,435 problems but only 2
> of them are wrong orders. The other problems are mistakes in our rules or in
> the conversion. Then we make the check run automatically, so a bad change
> cannot be accepted.

This lab is for understanding. Nothing is handed in or graded.

## The lab in five steps

Read this top to bottom. It is the whole lab.

```text
1. START WITH TWO THINGS

   The data                          The rules
   Session 2's Brunel graph:         Session 1's business rules,
   135,841 facts about orders,       written as SHACL shapes
   carriers, plants and rate bands   (brunel-shapes-v0.ttl)
                 \                   /
                  \                 /
                   v               v
2. RUN THE FIRST DRAFT
   python validate.py --shapes brunel-shapes-v0.ttl
   Result: 3,435 Violations.  That looks terrible.
                         |
                         |  triage: look at each group of results
                         |  and ask "is the rule wrong, or the data?"
                         v
3. READ THE REPORT AS A LIST OF WORK
   2,224  orders outside a rate band
            854: our rule was wrong (CRF has no prices)
            1,370: the rate table has a gap
   1,209  bands whose carrier has no type -> the Session 2 conversion
   2      orders that weigh 0 kg      -> the data is really wrong
                         |
                         |  fix the rules, set severities
                         v
4. RUN THE TRIAGED SHAPES
   python validate.py
   Result: 2 Violations (real errors) and 2,579 Warnings (to investigate).
                         |
                         |  put the check in a GitHub workflow
                         v
5. THE GATE STOPS A BAD CHANGE
   A sample with one wrong letter in a carrier code fails (red).
   The same sample without the typo passes (green).
```

## What a SHACL rule looks like

One real rule from this lab, shortened. It says: every order has exactly one
carrier.

```turtle
uls:OrderShape a sh:NodeShape ;
    sh:targetClass ul:Order ;          # check every order
    sh:property [
        sh:path ul:carriedBy ;         # look at the carrier
        sh:minCount 1 ;                # at least one
        sh:maxCount 1 ] .              # at most one
```

If an order has no carrier, the report says:

```text
Violation: MinCount on ul:carriedBy, for order 1447291369.7
```

Words that start with `sh:` come from the SHACL standard. Words that start
with `uls:` or `ul:` are ours.

## What the gate does

A gate is an automatic check that every change must pass.

```text
you push a change
        |
        v
GitHub runs validate.py on a small sample (about 1 second)
        |
        +--> no Violation  -> green: the change can be accepted
        |
        +--> a Violation   -> red:   the change is stopped
```

Warnings are printed, but they do not stop a change. Only Violations do.

## The data

| Source file | One row means | Why this lab needs it |
|---|---|---|
| `OrderList.csv` | one Brunel order | The order, carrier, plant, ports, date, customer, service and weight facts that the order shapes check. |
| `FreightRates.csv` | one carrier price band | The rate bands used to test whether an order's weight fits its priced lane. |
| `PlantPorts.csv` | one plant to port link | Lets a SPARQL rule check that an order leaves through a port linked to its plant. |
| `ProductsPerPlant.csv` | one product a plant makes | Lets a SPARQL rule check that an order's plant makes its product. |

Session 2 turned these tables into the graph `brunel.ttl`. Today's rules run
on that graph.

## Why there are two shapes files

`brunel-shapes-v0.ttl` is the **first draft**. It turns every Session 1 rule
into a Violation, without looking at the report first. On the full graph it
gives 3,435 Violations.

`brunel-shapes.ttl` is the **same rules after triage**. Triage means reading
the report one group at a time and deciding what each group means. Every
decision is written next to its rule in a comment that starts with TRIAGE.

| Result | Count | Triage decision |
|---|---:|---|
| Orders with zero weight | 2 Violations | The data is wrong. Orders `1447336276.7` and `1447215484.7` have weight 0. They stay failures for the data owner. |
| Orders in a gap of the rate table | 1,370 Warnings | The data needs investigation. These orders have a priced lane, but no rate band covers their weight. |
| Rate bands whose carrier has no type | 1,209 Warnings | The Session 2 conversion is incomplete. Seven carriers appear only in `FreightRates.csv`, so the converter did not give them the type `Carrier`. Session 5 fixes the mapping. |
| CRF orders with no rate bands | 854, removed from this check | Our first rule was wrong for these orders. CRF is not in `FreightRates.csv`, so these orders have no price lane to check. |

The report is a list of work. It is not a verdict that every reported row is
bad.

## Open world and closed world

This idea explains why we need SHACL. Session 3's ontology works in an **open
world**: if a fact is missing, OWL treats it as unknown, not as wrong. So an
order with no carrier is not an error for OWL.

SHACL works in a **closed world**: it checks only the data it is given. A
missing carrier is a problem. A SHACL shape does not add meaning and does not
infer new facts. It only checks.

## What each step proves

| Step | You run | What it does | What you should understand afterward |
|---|---|---|---|
| 1 | `validate.py --shapes brunel-shapes-v0.ttl` | Runs the first draft on the full graph. | A large report can show a bad rule or a bad conversion, not only bad data. |
| 2 | Read the TRIAGE comments, then `validate.py` | Runs the triaged shapes. | Severity records a decision: Violations block, Warnings stay visible. |
| 3 | `add_provenance.py` | Records the source graph, source file, conversion run and program. | A result needs a trace back to its source. |
| 4 | `version_ontology.py` | Copies the Session 3 ontology with a version IRI. | Validation must name the ontology version it depends on. |
| 5 | Validate both CI samples | One passes with warnings. One fails because of one typo. | A gate can stop a data error automatically. |
| 6 | `fetch_epcis.py` | Inspects GS1's published EPCIS shapes. | Good patterns to reuse: named property shapes, forbidden fields, messages that say what to fix. |
| B | `check_my_shapes.py` | Optional. Runs the checker on the worked solutions, or on three shapes you write. | A shape is correct when it flags exactly the intended orders. |
| C | Discussion questions | Choose rules, severities and evidence for your project. | A team must justify its validation policy. |

## The tools in this lab

| Tool | What it does here | What it does not do |
|---|---|---|
| `rdflib` | Reads the Brunel graph and the Turtle shape files. | Decide whether a shape is a good business rule. |
| pySHACL | Applies the shapes to the graph and returns a report. | Repair the data or choose a severity for the team. |
| `validate.py` | Shows pySHACL's report as a short list of work, and makes Violations fail the command. | Turn every warning into an error. |
| GitHub Actions | Runs the small validation gate when someone changes the repository. | Replace validation of the full graph, or a person's judgement. |

The lab uses Python libraries and a repository workflow. You do not need a
desktop application or a service that keeps running.

## The two samples for the gate

The CI sample has six real Brunel orders and the carriers, plants, ports,
products, plant links and rate bands that belong to them: 515 triples in all.
It is small, so GitHub can check it in about a second.

The broken sample changes only order `1447385217.7`. Its carrier `V444_0`
becomes `V444_O`: the letter O instead of the number zero. This creates one
Violation: the carrier is not a `Carrier`.

`part-b/test-orders.ttl` is a teaching copy of the same slice. Its header lists
four faults placed on real orders: a second customer, no customer, an order
date in 2031, and a CRF order carried by `V444_0` instead of `V44_3`.

## The gate in the repository

`.github/workflows/shacl-gate.yml` runs on pushes and pull requests that touch
the Session 4 lab or the workflow. It installs pySHACL 0.40.1 and rdflib
7.6.0, then runs `validate.py` on the committed sample with the triaged
shapes. Any Violation gives a red run. Warnings are printed but pass.

The real green run is on `main`. The real red run is on the branch
`demo/broken-carrier-code`. Their links and results are in
`reference-outputs/ci-runs.txt`. The demo branch is kept for teaching and is
never merged.

## The files and their roles

| File | Role | Do you edit it? |
|---|---|---|
| `brunel-shapes-v0.ttl` | First draft, before triage. | Read only. |
| `brunel-shapes.ttl` | The triaged shapes and the decisions. | Read it; use it as a model for your project. |
| `validate.py` | Runs pySHACL and applies the gate rule. | Run it. |
| `ci/sample-orders.ttl` | Six real orders for the green gate. | No. Regenerate with `make_ci_sample.py` if Session 2 changes. |
| `ci/sample-orders-broken.ttl` | The same sample with one typo. | No. It is for the red demonstration. |
| `part-b/test-orders.ttl` | A slice of real orders with four listed faults. | No. |
| `my_shapes.ttl` | Three shapes for the optional Part B. | Only if you want to practise. |
| `check_my_shapes.py` | Checks which orders each Part B shape flags. | Run it. |
| `add_provenance.py` | Builds provenance for the source graphs. | Run it. |
| `version_ontology.py` | Shows a version IRI without changing Session 3. | Run it. |
| `fetch_epcis.py` | Downloads GS1 EPCIS shapes and counts their patterns. | Run it when you have the network. |
| `shapes_template.ttl` | An old template that targets `PurchaseOrder`. It is the real example of a shape that checks nothing (Part A, step 1). | No. Run it once to see the problem. |
| `reference-outputs/` | Recorded validation, provenance, checker and CI results. | Read only. |

## Terms you need first

| Term | Plain definition |
|---|---|
| **SHACL** | A language for checking RDF data against stated shapes. |
| **shape** | A rule that says which nodes to check and what values they must have. |
| **target** | The nodes a shape applies to. A shape with no focus nodes checks nothing. |
| **Violation** | A result serious enough to fail this course's gate. |
| **Warning** | A result that should be investigated, but is allowed through the gate. |
| **triage** | Reading a report one group at a time and deciding: is the rule wrong, is the data wrong, or is the conversion wrong? |
| **SPARQL constraint** | A shape rule written as a query, for checks that core SHACL cannot state. |
| **provenance** | Information that traces a graph or a result back to its source and process. |
| **version IRI** | A stable name for one released version of an ontology. |
| **validation gate** | An automatic check that must pass before a change is accepted. |
| **pySHACL** | The Python library that checks the graph against SHACL shapes in this lab. |
| **GitHub Actions** | GitHub's automation service, used here to run the gate after a repository change. |

## How to judge a statement in this lab

1. **Source fact:** a value in the Brunel tables, such as a zero weight or a
   carrier code.
2. **Validation decision:** the shape, its target, its severity and its TRIAGE
   label. These are course decisions, and each one must state its evidence.
3. **Conversion result:** facts produced by Session 2, including the missing
   carrier types for carriers that appear only in the freight rates.
4. **Validation result:** a result produced when one shapes file runs on one
   graph. Reproduce it and compare it with `reference-outputs/`.

Now return to the [lab README](README.md), then begin Part A.
