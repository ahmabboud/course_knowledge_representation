# Session 8: supervised build, deployment, and defense

No lab of its own: the day is each team's own build, in parallel, with the
instructor rotating for a 10 to 12 minute defense visit per team. The
materials:

- `kr-team-template/` (repository root): the starter repository every team
  builds its project in, one folder per layer, one `docker compose up
  --build` for the whole stack, the SHACL gate in CI, and a report outline
  mapped to the rubric. It comes up on a tiny real Brunel example; teams
  replace the example with their own data, layer by layer. The instructor
  publishes it as a GitHub template repository for the teams.
- `module-08-defense/DEFENSE-DAY.md`: the instructor's run of show.
- `module-08-defense/scoring-sheet.html`: one printable page per team.
- `lectures/kr-session-08.html`: the short day deck (plan, standup,
  checklist, defense, rubric, report, course close).

The Session 8 checklist (agreed in Session 7) is in the template's README:
one command from a clean checkout; ports on 127.0.0.1 and keys only in
`.env`; the SHACL gate before the endpoint and in CI; the test set's score
recorded with model and date; a real unanswerable question refused.
