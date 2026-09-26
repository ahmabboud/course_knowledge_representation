# Session 4 lab: validate, triage, gate, write your own

**Why this lab exists:** to make the lecture concrete (open against closed
world, SHACL core, SPARQL constraints, severity, triage, provenance, version
IRIs, a validation gate) on the real Brunel graph, and to give you the
pipeline Milestone 1 of your team project asks for. Nothing is handed in or
graded. The lab works when you can explain why the first report has 3,435
Violations and only 2 of them are the orders' fault.

**Read this first:** [What this lab is doing](OVERVIEW.md). It explains the
Session 2 graph, why SHACL is a data check rather than an OWL axiom, triage,
the CI sample and gate, file roles, terms, and how to separate facts from
validation decisions. Do not start Part A until the overall story is clear.

Every number in `lectures/kr-session-04.html` comes from the files in
`reference-outputs/`, produced by these scripts on 2026-09-25.

## Before you start

- Shared setup from `demos/README.md` done in Session 1, and `demos/.venv`
  active. pySHACL 0.40.1 is in `demos/requirements.txt`; if
  `python -c "import pyshacl"` fails, run `pip install -r demos/requirements.txt`.
- **The Session 2 graph exists:** `demos/session-02-rdf-sparql/brunel.ttl`.
  If not, run `python convert_to_rdf.py` in that folder first (about 20 s).
- Run every command from this folder, `demos/session-04-shacl/`.
- A full validation of the 135,841 triple graph takes about two minutes.
  Short of time or on a slow laptop? Add `--data ci/sample-orders.ttl` to any
  `validate.py` command: the same shapes on six real orders, in a second.
  You see every concept except the size of the real report.

## Part A · build and observe (about 25 minutes)

1. `python validate.py --shapes brunel-shapes-v0.ttl` (about 90 s). The first
   draft: every Session 1 business rule, all Violations. **Expect:** focus
   nodes 9,215 for each order shape and 1,540 for the rate band shape, then
   `3,435 Violation`: 2,224 weight in no rate band, 1,209 band carrier not a
   Carrier, 2 weight not above 0. `GATE: FAIL`, exit code 1.
   **Look at:** the focus node lines come first. A shape with 0 focus nodes
   checks nothing; try `python validate.py --shapes shapes_template.ttl`
   (**Expect:** focus nodes 0, `conforms (SHACL): True`, in under a second).
2. Open `brunel-shapes.ttl` and read each comment that starts with TRIAGE.
   Then `python validate.py` (about 110 s). **Expect:** `2 Violation,
   2,579 Warning`: the 2 orders that weigh 0 kg (1447336276.7, 361 units;
   1447215484.7, 348 units) stay Violations; 1,370 weight in band and 1,209
   band carrier are Warnings. **Notice:** the 854 CRF orders are gone
   because the shape was wrong (CRF is not in the rate table at all), not
   because anything was hidden. `conforms` is still False: any result, of
   any severity, makes it false.
3. `python add_provenance.py`. **Expect:** `provenance.ttl: 43 triples about
   4 named graphs, 1 run, 1 program`, then the answer to "where does order
   1447296446.7 carried by V44_3 come from?": the OrderList graph, the file
   OrderList.csv, one conversion run and its time (your time differs: it is
   when you ran Session 2's conversion).
4. `python version_ontology.py`. **Expect:** the Session 3 ontology has no
   version IRI (176 triples); `workspace/scro-extension-1.0.0.ttl` has
   `owl:versionIRI <https://ul.edu.lb/kr/scm/1.0.0>` (178 triples). The
   Session 3 file is not changed.
5. The gate, on your laptop: `python validate.py --data ci/sample-orders.ttl`
   (**Expect:** 3 Warnings, `GATE: PASS`, exit code 0), then
   `python validate.py --data ci/sample-orders-broken.ttl` (**Expect:**
   1 Violation, Class on carriedBy for order 1447385217.7, `GATE: FAIL`,
   exit code 1). The broken file differs by one character: carrier V444_O
   (letter O) instead of V444_0 (zero). Then open the same check on GitHub,
   in the repository's Actions tab: workflow **SHACL gate**, green on
   `main`, red on the branch `demo/broken-carrier-code`
   (links in `reference-outputs/ci-runs.txt`).
6. `python fetch_epcis.py` (needs the network once). Downloads GS1's EPCIS
   2.0 shapes into `workspace/` and prints what they are made of.
   **Expect:** 1,137 lines, 30 node shapes, 71 property shapes, 0 SPARQL
   constraints, 0 severities set; 27 property shapes reused by more than
   one node shape, 13 "forbidden" shapes (`sh:maxCount 0`), 77 shapes with
   an `sh:message`. These are the three patterns worth borrowing.

## Part B · write your own shapes (about 15 minutes)

Open `my_shapes.ttl`. It asks for three shapes, each practising one idea
from the lecture: Y1 cardinality (every order has exactly one customer),
Y2 a value range (every order date falls in 2013), Y3 a SPARQL constraint
(a CRF order is carried by V44_3). None of them is in `brunel-shapes.ttl`,
but the patterns are. Complete each shape under its marker, then:

```sh
python check_my_shapes.py
```

The checker runs each shape alone on `part-b/test-orders.ttl` (six real
orders, four of them changed on purpose, each listed at the top of that
file) and compares which orders your shape flags with the orders it should
flag. **Expect** when all three are right: `3 of 3 right.` Any shape that
flags exactly the right orders passes. Stuck after trying?
`solutions/my_shapes_solutions.ttl`. The common wrong answers and the
checker's hints are in `reference-outputs/my-shapes-check.txt`.

## Part C · think (about 10 minutes)

Answer for yourself, then in the closing discussion:

1. Pick one Session 1 rule OWL could state as an axiom. Should it live in
   the ontology, in the shapes, or both?
2. The 1,370 orders in the rate table's gap: who fixes what, and how would
   the report show that it is fixed?
3. Name two rules in **your team project's own data**: which are core
   SHACL, which need SPARQL, and what severity does each get?

## Optional

- `python shape_timings.py` times each shape alone on the full graph
  (about 2 minutes): the numbers on the slide "The cost of reaching for
  SPARQL too early" (`reference-outputs/shape-timings.txt`).
- `python make_ci_sample.py` rebuilds `ci/` and `part-b/` from the Session 2
  graph. You never need it unless the Session 2 conversion changes.
- shacl-play (<https://shacl-play.sparna.fr/play/validate>): paste
  `ci/sample-orders-broken.ttl` as data and `brunel-shapes.ttl` as shapes
  for the same report in a browser, from a second SHACL engine.

## You understood this lab if you can say

- why the reasoner stays silent about a missing carrier and SHACL does not;
- why a shape with 0 focus nodes "conforms", and why that is a bug;
- which of the 3,435 first draft results were the rule's fault, which the
  data's, and which the conversion's;
- when a rule needs SPARQL, and what it costs;
- what the gate checks on every push, and why it stops at a Violation but
  not at a Warning.

## Take it to your team project

- `validate.py` and `.github/workflows/shacl-gate.yml` are the templates
  for your gate: copy the workflow, change the data and shapes paths.
- `brunel-shapes.ttl` is the model for your shapes file: one shape per
  business rule, and a TRIAGE comment on every rule you changed.
- `add_provenance.py` and `version_ontology.py` show the provenance and the
  version IRI Milestone 1 asks for.
- Milestone 1 (a checkpoint for feedback, not graded, end of this session): your ontology
  with a version IRI, shapes covering your rule list, a triaged report,
  provenance, and a gate that blocks a bad commit.

## The old template, kept on purpose

`shapes_template.ttl` is the old Session 4 template. It targets
`ul:PurchaseOrder`, which the Session 2 graph does not have, so it is kept
as the real example of the targeting trap (Part A step 1). Do not build on it.
