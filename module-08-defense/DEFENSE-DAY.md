# Session 8, the defense day

Session 8 is the defense and nothing else: no build, no lecture. The system
and the report were handed in 48 hours before, and scored then. This is the
instructor's run of show.

## The grade (instructor, 2026-09-26)

| Part | Weight | When and how |
|---|---|---|
| Attendance and lab run | 15 | Sessions 1 to 7: present, and the lab run in class |
| Final team project, system and report | 55 | Scored once, offline, from the hand-in 48 hours before Session 8 |
| Individual defense | 30 | Session 8: one overall mark per student |

The milestones at the end of Sessions 4 and 6 are checkpoints for feedback,
not graded.

## Before the day: score the project once

Teams push the final repository and report 48 hours before Session 8. For
each team, at your desk:

1. Clone it into an empty folder, add a `.env` with your key, run
   `docker compose up --build`.
2. Give each of the six layers one mark: **works** (full points), **partly**
   (half), **missing** (none). A layer that cannot be shown working from the
   clean checkout is at most partly.

| Layer | Points |
|---|---|
| Ontology: a reused published vocabulary, competency questions, a clean reasoner run | 10 |
| Shapes and validation: the inventory covered, failures triaged, the gate in CI | 10 |
| Mapping and integration: the team's own source mapped; entity resolution with precision and recall | 9 |
| Learning over the graph: baseline, a split that does not leak | 9 |
| Access layer: answers checked and repaired, a real refusal, the score recorded | 9 |
| Report and open problem: what was deployed, one open problem with three sources | 8 |
| **Total** | **55** |

3. Write 3 or 4 questions for the team from what you saw: the weakest layer,
   a decision that looks borrowed, a number you could not trace.

## On the day (180 minutes, 24 students, 8 to 12 teams)

**Opening, 10 minutes.** The order of the teams on the board, and how the
defense is marked.

**Team defenses, about 15 minutes each.** One team at the front at a time;
the other teams may leave and come back for their slot.

- **Demonstration, 3 minutes (team).** The stack is already running: it
  answers one question you choose and refuses one it cannot answer. This
  confirms the offline score; it is not marked again.
- **Questions, 2 or 3 per student.** Each student is asked about a part of
  the system they did not build, from your prepared questions. Do not try to
  cover every topic: the questions sample understanding.

**Course close, 10 minutes.** The Session 1 reference architecture against
what the teams built, and further study.

At 12 teams the slots are 13 minutes; at 8 teams, 20. If the count needs
more time, use up to one extra hour rather than cutting a team short.

## The defense mark: one per student, 0 to 3

Judge the answers together, not question by question:

| Mark | The student |
|---|---|
| 0 | cannot explain the team's system, even the parts they are asked about |
| 1 | says what the parts do, not why |
| 2 | explains why the team decided as it did |
| 3 | defends the decisions against an alternative or a failure in their own system |

Defense points = mark × 10 (out of 30). The syllabus policy still holds: an
ontology the team cannot defend loses its ontology points.

Good questions to have ready:

- Why does this class exist? Which competency question needs it?
- Why is this constraint a SHACL shape and not an OWL axiom, or the reverse?
- Does your split leak? What did the baseline score?
- What does your system do when it does not know?

Record which question each student answered and the mark, on the scoring
sheet (`scoring-sheet.html`), right after the slot.
