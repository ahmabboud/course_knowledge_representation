# Session 4 lab: the SHACL shape graph, Milestone 1

Not built yet. This README states what the syllabus already commits
to.

## What the syllabus commits to

Take the Session 1 constraint inventory and express each entry as a
SHACL shape, running **pySHACL** against the Session 2 graph after each
addition. The interesting failures are constraints that turn out to be
false in the data, decide in each case whether the constraint was
wrong or the data is dirty, and record the decision. Load GS1's
published `epcis-shacl.ttl` and note three patterns worth borrowing.
Add a provided GitHub Action so validation runs in continuous
integration.

This is **Milestone 1**: the Session 3 ontology plus this shape graph,
a validation report with every failure triaged, provenance
annotations, a version IRI, and a working CI gate, worth 20 percent of
the grade per the assessment table.

## Real tools

pySHACL, shacl-play (browser, used live in the lecture), GS1's
`epcis-shacl.ttl` as a professional reference example.

## What will live here once built

- `shapes_template.ttl` — a starting shape graph, one shape per
  constraint-inventory entry, to fill in.
- `validate.py` — a pySHACL wrapper, the same shape this session's
  `kr-team-template/scripts/validate_shapes.py` mirrors for teams.
- `.github/workflows/validate.yml` — the CI gate itself, once this
  session's own repo layout is decided; teams get theirs from
  `kr-team-template`.

## What "done" looks like

Shapes cover the inventory, every failure triaged, provenance and a
version IRI present, and the CI gate demonstrably blocks a bad commit.
