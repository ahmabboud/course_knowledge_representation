# Session 1 lab: environment, profiling, constraint inventory

Builds the syllabus deliverable: a verified environment, a profiling
report for both datasets, and a written constraint inventory with
evidence for each entry, per `course_knowledge_representation/lectures/kr-session-01.html`'s
lab brief slide.

**Read this first:** [What this lab is doing](OVERVIEW.md). It explains the
two datasets, what profiling and clustering can show, the purpose of the
constraint inventory, file roles, terms, and how evidence supports a rule.
Do not begin the commands until the overall story is clear.

## Working directories

Start in `DEMO_ROOT`, the folder containing `requirements.txt`, `data/`, and
every `session-*/` folder. It is described in the shared `README.md` one
level above this folder. Complete that setup first and keep `DEMO_ROOT/.venv`
activated. The commands below work in macOS/Linux shells and Windows
PowerShell because `cd` and `python` have the same use after activation.

## Run, in order

1. Starting from `DEMO_ROOT`, run:

   ```text
   cd session-01-environment-and-constraints
   python smoke_test.py
   ```

   This checks Python 3.12, JDK 21, Docker, and that Protege is installed in
   one pass. Run it before assuming anything else works.
2. Return to `DEMO_ROOT` and fetch the data:

   ```text
   cd ..
   python data/fetch_data.py
   ```

   This downloads the source datasets and exports Brunel's workbook sheets to
   CSV. `openpyxl` comes from the shared `requirements.txt`.
3. Return to this Session 1 folder and run:

   ```text
   cd session-01-environment-and-constraints
   python profiling.py
   ```

   It profiles both DataCo and Brunel with
   ydata-profiling, writes an HTML report per dataset next to this
   README (gitignored, regenerate, do not commit). Cluster values in
   OpenRefine separately; OpenRefine is a GUI tool, not scripted here.
   This file is written in `# %%` cells (Jupytext), so open it in
   JupyterLab or VS Code instead to run it step by step, with the
   missingness charts and DataCo's full profile rendered inline as you
   go, rather than running it as one batch script.
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

## Where the slide numbers come from

`python session1_facts.py > reference-outputs/s1-facts.txt` recomputes every
number the Session 1 deck quotes from the real data. If a number on a slide
and this file disagree, the file wins.

## What "done" looks like

A profiling report for both datasets, and a constraint inventory that
is substantive rather than trivial: each entry cites evidence a reader
could check, and a rule with real exceptions is noted as such rather
than silently dropped. This file is the input to Sessions 3, 4, and 5.
