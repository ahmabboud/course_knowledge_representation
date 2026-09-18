# Session 7 lab: the natural language access layer

Not built yet. This README states what the syllabus already commits
to.

## What the syllabus commits to

Stand up **sparql-llm** over the participant's own endpoint. Generate a
VoID description with **void-generator**, author example queries in the
expected vocabulary, and get a first natural language question
answered. Implement the validation-and-repair loop and measure the
improvement. Wrap the result in the **TEXT2SPARQL contract** (a single
GET endpoint returning the generated query) and score it with the
official `text2sparql-client` harness against a provided question set.
Record the score, improve one thing, record it again. Add a refusal
path and confirm it refuses a question the graph genuinely cannot
answer. A 30-minute open-problems segment follows, not in service of
this lab, that names this session's reading list.

## Real tools

sparql-llm, void-generator, the TEXT2SPARQL contract and
`text2sparql-client` harness, an LLM API (see the repository root's
`.env.example`, `GOOGLE_API_KEY` by default).

## What will live here once built

- `generate_void.py` — runs void-generator against the team's endpoint.
- `example_queries/` — the authored example query set sparql-llm
  retrieves against.
- `repair_loop.py` — the validation-and-repair implementation.
- `text2sparql_server.py` — the single GET endpoint, matching the
  contract, that the harness scores.

## What "done" looks like

Questions answered against the team's own ontology, the repair loop's
improvement measured before and after, and the refusal path
demonstrated on a real unanswerable question, per the Session 7
deliverable.
