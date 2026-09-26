# Session 8: the defense

No lab and no build (instructor, 2026-09-26): teams hand in the system and
the report 48 hours before; the instructor scores the project once,
offline; the day is one team at a time, about 15 minutes each (a 3 minute
demonstration, then 2 or 3 questions per student, one mark per student).
The materials:

- `kr-team-template` (https://github.com/ahmabboud/kr-team-template), a GitHub template repository: each
  team presses "Use this template" to create its own. One folder per layer,
  one `docker compose up --build` for the whole stack, the SHACL gate in CI,
  and a report outline mapped to the rubric. It comes up on a tiny real
  Brunel example; teams replace the example with their own data, layer by
  layer. Verified end to end on the instructor's Mac with Docker (2026-09-26): the
  pipeline loaded Fuseki and the access layer answered through Gemini; its
  CI is green.
- `module-08-defense/DEFENSE-DAY.md`: the instructor's run of show.
- `module-08-defense/scoring-sheet.html`: one printable page per team.
- `lectures/kr-session-08.html`: the short day deck (the plan, one team's
  slot, how students are marked, the defenses, the course close).

The checklist agreed in Session 7 is in the template's README, as the
things to check before handing in:
one command from a clean checkout; ports on 127.0.0.1 and keys only in
`.env`; the SHACL gate before the endpoint and in CI; the test set's score
recorded with model and date; a real unanswerable question refused.
