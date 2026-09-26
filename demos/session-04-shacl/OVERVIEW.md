# Read first: what this lab is doing

This lab asks one practical question:

> When the graph is open to new facts, how do we state the data rules that
> must hold today, explain failures fairly, and stop a bad change before it is
> merged?

Session 2 made the Brunel tables into an RDF graph. Session 3 added meanings
and inference. Session 4 adds SHACL, a separate language for checking whether
the graph meets a stated data rule.

## The short story

The input is Session 2's `brunel.ttl`, a graph of 135,841 triples. Its orders
use properties including `orderId`, `orderedBy`, `carriedBy`, `fromPlant`,
`shipsFrom`, `ofProduct`, `weight`, and `serviceLevel`. The graph also has
`RateBand` nodes with `bandCarrier`, lane, and weight facts. The shapes target
`Order` and `RateBand` and check their properties and cross graph rules.

```text
Session 2 Brunel graph
        |
        | SHACL shapes
        v
validation report
        |
        | triage each result
        v
Violations block a gate, Warnings remain visible
```

## The data and the problem

| Source file | One row means | Why this lab needs it |
|---|---|---|
| `OrderList.csv` | one Brunel order | Supplies the order, carrier, plant, ports, date, customer, service, and weight facts checked by the order shapes. |
| `FreightRates.csv` | one carrier price band | Supplies the rate bands used to test whether an order's weight fits its priced lane. |
| `PlantPorts.csv` | one plant to port link | Lets a SPARQL shape check that an order leaves through a port linked to its plant. |
| `ProductsPerPlant.csv` | one product a plant makes | Lets a SPARQL shape check that an order's plant makes its product. |

The graph is intentionally open world. An OWL axiom can say what follows if a
fact exists, but it does not treat an absent carrier or customer as an error.
A SHACL shape is a closed, operational check: for this data release, every
order must have the properties and values the rule requires. A shape is not an
OWL axiom, and it does not add meaning or infer facts.

## Why there are two shapes files

`brunel-shapes-v0.ttl` is the first draft. It turns every Session 1 rule into
a Violation before reading the report. On the full graph it returns 3,435
Violations: 2,224 orders outside a rate band, 1,209 rate bands whose carrier
is not typed `Carrier`, and 2 zero weight orders.

`brunel-shapes.ttl` is the same rule set after TRIAGE comments identify what
the report actually means. It returns 2 Violations and 2,579 Warnings:

| Result | Count | Triage decision |
|---|---:|---|
| Orders with zero weight | 2 Violations | The data is wrong. Orders `1447336276.7` and `1447215484.7` have weight 0 and remain failures for the data owner. |
| Orders in a rate gap | 1,370 Warnings | The data needs investigation. These orders have a priced lane but no matching weight band. |
| Rate bands with an untyped carrier | 1,209 Warnings | The Session 2 conversion is incomplete. Seven carriers appear only in `FreightRates.csv`, so the converter did not type them as `Carrier`. Session 5 fixes the mapping. |
| CRF orders with no rate bands | 854 removed from this check | The first rule was wrong for these orders. CRF is absent from `FreightRates.csv`, so they are not priced lanes and must not be reported as rate gaps. |

The report is a work queue, not a verdict that every reported row is bad.

## How the items relate

```text
brunel.ttl + brunel-shapes-v0.ttl -> 3,435 Violations
brunel.ttl + brunel-shapes.ttl    -> 2 Violations, 2,579 Warnings
ci/sample-orders.ttl              -> 3 Warnings, gate passes
ci/sample-orders-broken.ttl       -> 1 Violation, gate fails
```

## The tools in this lab

| Tool | What it does here | What it does not do |
|---|---|---|
| `rdflib` | Reads the Brunel graph and the Turtle shape files. | Decide whether a shape is a sensible business rule. |
| pySHACL | Applies the shapes to the graph and returns a report. | Repair the data or choose a severity for the team. |
| `validate.py` | Presents pySHACL's report as a small work queue and makes Violations fail the command. | Turn every warning into an error. |
| GitHub Actions | Runs the small validation gate on a shared repository change. | Replace validation of the full graph or an instructor's judgement. |

The lab uses Python libraries and a repository workflow, not a separate
desktop application or a service students must keep running.

The CI sample contains six real Brunel orders and the related carriers,
plants, ports, products, plant links, and rate bands, 515 triples in all. It
is small so GitHub can check it in about a second. The broken sample changes
only order `1447385217.7`: carrier `V444_0` becomes `V444_O`, letter O rather
than zero. This creates one `carriedBy` class Violation.

`part-b/test-orders.ttl` is a teaching copy of the same slice. Its header
lists four planted faults on real orders: a second customer, no customer, a
2031 order date, and a CRF order carried by `V444_0` instead of `V44_3`.

## What each step proves

| Step | You run | What it does | What you should understand afterward |
|---|---|---|---|
| 1 | `validate.py --shapes brunel-shapes-v0.ttl` | Runs the untriaged draft on the full graph. | A large report can expose a bad rule or conversion, not only bad data. |
| 2 | Read TRIAGE comments, then `validate.py` | Runs the triaged shapes. | Severity records an action decision: Violations block, Warnings remain visible. |
| 3 | `add_provenance.py` | Records the source graph, source file, conversion run, and program. | A result needs a trace back to its source. |
| 4 | `version_ontology.py` | Copies the Session 3 reference ontology with a version IRI. | Validation must name the ontology version it depends on. |
| 5 | Validate both CI samples | Demonstrates a passing warning only sample and one carrier typo that fails. | A gate can stop a data error automatically. |
| 6 | `fetch_epcis.py` | Inspects GS1's published EPCIS shapes. | Reuse patterns include named property shapes, forbidden fields, and actionable messages. |
| B | `my_shapes.ttl` and `check_my_shapes.py` | You write three shapes against four planted faults. | Correctness means flagging exactly the intended orders. |
| C | Discussion questions | Choose rules, severities, and evidence for your project. | A team must justify its validation policy. |

## The gate

`.github/workflows/shacl-gate.yml` runs on pushes and pull requests that
touch the Session 4 lab or workflow. It installs pySHACL 0.40.1 and rdflib
7.6.0, then runs `validate.py` on the committed sample and triaged shapes.
Any Violation gives a red run. Warnings are printed but pass.

The real green run is on `main`; the real red run is on branch
`demo/broken-carrier-code`. Their links and results are recorded in
`reference-outputs/ci-runs.txt`. The demo branch is kept for teaching and is
never merged.

## The files and their roles

| File | Role | Do you edit it? |
|---|---|---|
| `brunel-shapes-v0.ttl` | First draft, before report triage. | Read only. |
| `brunel-shapes.ttl` | Triaged course shapes and decisions. | Read it; use as a project model. |
| `validate.py` | Runs pySHACL and applies the gate rule. | Run it. |
| `ci/sample-orders.ttl` | Six real orders for the green CI gate. | No, regenerate with `make_ci_sample.py` if Session 2 changes. |
| `ci/sample-orders-broken.ttl` | The same sample with one intentional carrier typo. | No, it exists for the red demonstration branch. |
| `part-b/test-orders.ttl` | Real order slice with four listed teaching faults. | No. |
| `my_shapes.ttl` | Three Part B shapes to complete. | Yes. |
| `check_my_shapes.py` | Checks which orders each Part B shape flags. | Run it. |
| `add_provenance.py` | Builds provenance for the source graphs. | Run it. |
| `version_ontology.py` | Demonstrates a version IRI without changing Session 3. | Run it. |
| `fetch_epcis.py` | Downloads and counts GS1 EPCIS SHACL patterns. | Run it when the network is available. |
| `shapes_template.ttl` | Old template targeting `PurchaseOrder`: the real example of the targeting trap (Part A step 1). | No; run it once to see a shape that checks nothing. |
| `reference-outputs/` | Recorded validation, provenance, checker, and CI results. | Read only. |

## Terms you need first

| Term | Plain definition |
|---|---|
| **SHACL** | A language for checking RDF data against stated shapes. |
| **shape** | A rule describing which nodes to check and what values they must have. |
| **target** | The nodes a shape applies to. A shape with no focus nodes checks nothing. |
| **Violation** | A result serious enough to fail this course's validation gate. |
| **Warning** | A result recorded for investigation but allowed through the gate. |
| **triage** | Classifying a result as a rule issue, data issue, conversion issue, or accepted warning. |
| **SPARQL constraint** | A shape rule expressed as a query for relationships core SHACL cannot state directly. |
| **provenance** | Information that traces a graph or result to its source and process. |
| **version IRI** | A stable identifier for one released ontology version. |
| **validation gate** | An automated check that must pass before a change is accepted. |
| **pySHACL** | The Python library that checks the graph against SHACL shapes in this lab. |
| **GitHub Actions** | GitHub's automation service, used here to run the small validation gate after a repository change. |

## How to judge an assertion

1. **Source fact:** a value in the Brunel tables, such as a zero weight or a
   carrier code.
2. **Modelling or validation decision:** the shape, its target, severity, and
   TRIAGE label. These are course decisions that must state their evidence.
3. **Conversion result:** facts produced by Session 2, including missing
   carrier types for carriers appearing only in freight rates.
4. **Validation result:** a result produced when a named shapes file runs on
   a named graph. Reproduce it and compare it with `reference-outputs/`.

Now return to the [lab README](README.md), then begin Part A.
