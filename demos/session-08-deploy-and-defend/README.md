# Session 8: supervised build, deployment, and defense

Not built yet as code; this is a supervised lab and defense block, not
a taught lecture (`course_knowledge_representation` has no Session 8
deck by design, see `PROMPT.md`). The actual run-of-show is
`course_knowledge_representation/module-08-defense/DEFENSE-DAY.md`.

## Note: this session's syllabus segment text is stale

The `segments` text for Session 8 in `syllabus-source.json` still reads
"Participants," "individual defense," and "nobody is defended before
their stack comes up," language from before the team redesign.
Everything else about Session 8 (`DEFENSE-DAY.md`, the assessment
table, the rubric) was updated to teams during the 2026-09-17 redesign;
this one field was missed. Flagged here rather than silently worked
around; fix it in `syllabus-source.json` to match `DEFENSE-DAY.md`'s
parallel, per-team format before this session is taught.

## What the (corrected) shape actually is

Standup and blocker triage, then a 150-minute supervised build block
run in parallel across teams (not sequential), with the instructor
rotating for each team's defense visit, per `DEFENSE-DAY.md`. Assembles
Sessions 1 through 7 into one Docker Compose project per team:
triplestore with the integrated graph, RML mappings runnable on
demand, the SHACL gate wired into CI, the trained model served behind
an interface, and the natural language query layer in front. The
reproducibility requirement, coming up from a clean checkout with one
command, is where most of the time goes.

## What will live here once built

Nothing session-specific: each team's own stack lives in their own
repository, created from `kr-team-template`. This folder is where an
instructor-side checklist or scoring-sheet script could go, if one gets
built separately from `DEFENSE-DAY.md`'s own scoring section.
