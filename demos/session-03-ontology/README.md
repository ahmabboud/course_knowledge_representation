# Session 3 lab: ontology construction in Protege

Not built yet, `kr-session-03.html`'s lecture deck exists but this
lab's code has not been written against it. This README states what
the syllabus and lecture already commit to, so the lab can be built
directly from here once it is time.

## What the syllabus commits to

Ontology construction in Protege, starting from **IOF SCRO** loaded in
a provided workspace, not an empty file. Write eight competency
questions and record them as annotations. Extend SCRO with the classes
and properties the Session 1 constraint inventory demands, reusing
**GS1 Web Vocabulary** terms where they fit. Run **ELK**, then
**HermiT**, and read the inferred class hierarchy as a diagnostic:
unsatisfiable classes, unintended equivalences, unintended subsumptions.

## Real tools

Protege (GUI, checked by Session 1's smoke test), the ELK and HermiT
reasoner plugins (bundled with Protege), IOF SCRO as the starting
ontology, GS1 Web Vocabulary for reuse.

## What will live here once built

- `workspace/` — the provided Protege project pre-loaded with IOF SCRO,
  handed to students rather than an empty file.
- `competency_questions_template.md` — a place to draft and record the
  eight questions before they become annotations in the ontology.
- A short script or checklist step to run ROBOT's quality report
  against the saved ontology (ROBOT is named in Session 1's tooling
  table as actively maintained; not yet wired up here).

## What "done" looks like

A domain ontology, version 1, built on IOF SCRO, eight annotated
competency questions, a clean reasoner run, a recorded OWL profile, and
a ROBOT quality report, per the Session 3 deliverable.
