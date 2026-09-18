# Session 8, the defense day

Session 8 has no lecture deck. It is a fully supervised 150-minute build,
deployment, and defense block, per `PROJECT-REDESIGN.md`. This document
is the instructor's own run-of-show for that day.

## The format is parallel, not sequential

This is not DSCAI's model (one team presents to the whole room, then the
next). All teams work on their own deployment at the same time, the way
a lab session already works. The instructor rotates between teams for a
focused defense visit, while every other team keeps building. That is
what makes the math work: the constraint is the instructor's own time
per team, not the whole room's attention.

At teams of 2 to 3 and a cohort of 12 to 24, that is **4 to 12 teams**.
Budget **10 to 12 minutes of dedicated instructor time per team** for the
defense visit itself (separate from ambient walk-around help with
deployment issues). That is 40 to 144 minutes across the full team range,
comfortably inside the 150-minute block even at the top of the range,
with room left over for troubleshooting. If the actual team count runs
past what fits, use up to 1 extra hour, the same buffer DSCAI's own
Module 6 keeps, rather than compressing any team's defense time.

## Before this day

Confirm, per team, before the block starts:

- The repository is pushed and the stack is expected to come up from a
  clean checkout with one command, per the "Code and artifacts" policy.
  Session 8 is where it gets graded by actually doing that, it should
  not be the first time the team has tried it.
- Milestone 2 was submitted at the end of Session 6, so Session 7's own
  contact and out-of-class time was available to finish the access layer
  and harden deployment. A team arriving at Session 8 with the access
  layer unstarted has not used that time, and the schedule has no slack
  to build it from zero here.
- The technical report is close to final, referenced during the defense
  visit rather than read live.

## Running the block

**1. Standup and blocker triage, 20 minutes.** Each team states in under
a minute what is deployed, what is not, and their single largest
blocker. Triage blockers into the order you will actually get to them,
out loud, so teams know whether to keep working around a blocker or wait
for you.

**2. Supervised build and rotating defense, 150 minutes.** Teams work in
parallel on their own deployment. Move through teams for their defense
visit, roughly 10 to 12 minutes each. **Any of the 2 to 3 teammates can
be asked about any part**, the data, the ontology, the SHACL shapes, the
integration, the model, the access layer, or the code, not only the part
they personally wrote, per the "Team work" policy. Spread questions
across teammates deliberately, do not let one person answer everything.

One question per rubric line is enough to keep a visit inside 10 to 12
minutes without turning it into a full re-grade of the artifact, the
artifact is already being graded separately by cloning and running it.
Good questions to have ready, drawn from the rubric in `PROJECT-REDESIGN.md`:

- Ask one teammate to name the real published vocabulary the ontology
  reuses, and why it fits the team's chosen topic, without looking at
  the report.
- Ask another to point at one constraint in the inventory and explain
  why it became a SHACL shape rather than an OWL restriction, or the
  reverse.
- Ask a third what the tabular baseline scored against the graph model,
  and whether losing to it would have been reported honestly.
- Pick one deployment step and ask what happens if it fails on a clean
  checkout, has anyone actually tried that.
- Ask what full-scale validation would require, for any part of the
  system a smoke test stood in for.

Between defense visits, use the remaining time in the block for ambient
troubleshooting help, the same way any lab session runs.

**3. Course close, 10 minutes.** Consolidate the reference architecture
from Session 1 against what teams actually built, and point to further
study paths.

## Scoring

Score each team right after its defense visit, while it is fresh,
against the 100-point rubric in `PROJECT-REDESIGN.md` plus the separate
10 percent defense line from the Assessment table. Record which
teammate answered which question, that record is what "individual
accountability" in a team grade actually rests on if a mark is ever
questioned later.

## After this day

What this document protects is that every team gets a real, focused
defense inside one session, extended by up to an hour if the actual team
count needs it, rather than a rushed or uneven one. It does not fix
grading turnaround, that is governed by the Assessment section of the
syllabus.
