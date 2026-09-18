# Session 1 lab: environment, profiling, constraint inventory

Builds the syllabus deliverable: a verified environment, a profiling
report for both datasets, and a written constraint inventory with
evidence for each entry, per `course_knowledge_representation/lectures/kr-session-01.html`'s
lab brief slide.

## Run, in order

1. `python smoke_test.py` — checks Python 3.12, JDK 21, Docker, and that
   Protege is installed, in one pass. Matches the syllabus's own
   smoke-test description; run it before assuming anything else works.
2. `python data/fetch_data.py` from the repository root, if not already
   done.
3. `python profiling.py` — profiles both DataCo and Brunel with
   ydata-profiling, writes an HTML report per dataset next to this
   README (gitignored, regenerate, do not commit). Cluster values in
   OpenRefine separately; OpenRefine is a GUI tool, not scripted here.
4. Fill in `constraint_inventory_template.csv` as you work. An entry
   needs all three columns: the rule, the evidence in the data, and the
   source column or table. Two out of three is not a finding, per the
   lecture's own "what scores" callout.

## Real tools, matching the lecture

- **ydata-profiling** for cardinalities, nulls, ranges, distributions.
- **OpenRefine**, run separately (`openrefine` from a terminal, or the
  desktop app), for clustering near-duplicate values, this is where
  hidden rules tend to surface.
- **Protege**, checked by the smoke test, used starting Session 3.

## What "done" looks like

A profiling report for both datasets, and a constraint inventory that
is substantive rather than trivial: each entry cites evidence a reader
could check, and a rule with real exceptions is noted as such rather
than silently dropped. This file is the input to Sessions 3, 4, and 5.
