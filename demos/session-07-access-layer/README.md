# Session 7 lab: the natural language access layer

**Read this first:** [What this lab is doing](OVERVIEW.md). It explains the
data, why each step exists, and the role of every file.

**Why this lab exists:** to make the lecture concrete (grounding a model in
the graph's own description, validation and repair, refusal, measuring)
on the Brunel graph, and to give you the access layer your team's Session 8
stack puts in front of its own graph. Nothing is handed in or graded.

The model's numbers in `lectures/kr-session-07.html` come from the
instructor's recorded run (`reference-outputs/`, made with `record_llm.py`);
everything else from runs of these scripts on 2026-09-25.

## Before you start

- The shared course environment `demos/.venv`, active (no new packages).
- Session 2's graph exists (`demos/session-02-rdf-sparql/brunel.ttl`). If
  not, run `python convert_to_rdf.py` there first.
- **A Gemini key.** Make a free one at https://aistudio.google.com/apikey
  (you must be 18 or older), copy `demos/.env.example` to `demos/.env`, and
  put the key after `GOOGLE_API_KEY=`. Never paste it into a script, a
  slide or a commit. The free tier's content may be used by Google to
  improve its products: ask only about this course's data.
- Run every command from this folder, `demos/session-07-access-layer/`.
- **Key not working, or no internet?** Add `LLM_MODE=replay` in front of any
  command (PowerShell: `$env:LLM_MODE="replay"` first). It replays the
  instructor's recorded answers for the lab's own questions. You lose only
  your own live run.
- **Too many requests** (error 429, free tier): the scripts wait and retry;
  if it keeps happening, set `LLM_DELAY=4` (seconds between calls).

## Part A · build and observe (about 30 minutes)

1. `python make_void.py`. Describes the graph. **Expect:** `wrote void.ttl:
   189 triples`. **Look at:** `void.ttl`, one class partition: the class,
   its count, and for each property the class it points to.
2. `python show_prompt.py "How many orders did carrier V44_3 carry?"`. No
   model call. **Expect:** `examples picked: 1, 2, 4` and about 2,900
   characters. **Notice:** the whole prompt fits on two screens: rules,
   schema, three examples, the question.
3. `python ask.py "How many orders did carrier V44_3 carry?"`. One live
   call, or more if it repairs. **Expect:** a query using `ul:carriedBy`, and
   `n=854`. **Look at:** the rows are the evidence: 854 is checkable.
4. `python check.py broken.sparql`. **Expect:** `1 problem`: `ul:shippedBy
   is not a property of this graph`, followed by the real properties.
   **Notice:** that list is the hint the repair loop sends back.
5. `python evaluate.py` (about 50 calls, a few minutes). **Expect:** three
   summary lines, `schema`, `examples`, `repair`, each with a mean F1 and
   the refusals. The recorded run is in `reference-outputs/evaluate.txt`;
   **your numbers may differ**, because the model does not always write the
   same query. **Look at:** question 1 in the `schema` setting: 9,023 or
   9,215?
6. `python serve.py`, then open
   `http://127.0.0.1:8000/?question=How%20many%20late%20orders%20are%20there%3F&dataset=https://ul.edu.lb/kr/brunel/`
   in a browser. **Expect:** JSON with `dataset`, `question` and `query`: the
   TEXT2SPARQL contract. Stop the server with Ctrl+C.

## Part B · three small improvements (about 15 minutes)

Each is a copy of something already in the lab, with one thing changed:

| Task | Write in | Copy | Change |
|---|---|---|---|
| Y1 | `my_examples.ttl` | `ex:3` of `examples.ttl` | "Which ports does plant PLANT08 ship through?", `ul:servesPort` |
| Y2 | `my_access.py` | `unknown_properties` in `access_layer.py` | classes instead of properties |
| Y3 | `my_questions.yaml` | question 5 of `questions.yaml` | plant PLANT08, id 101 |

Then:

```sh
python check_my_access.py
```

No model call. **Expect** when all three are right: `3 of 3 right.` Stuck?
`solutions/`. The common wrong answers and their hints are in
`reference-outputs/my-access-check.txt`. Then measure your improvement:

```sh
python evaluate.py --setting repair --add-class-check --questions my_questions.yaml
```

## Part C · think (about 10 minutes)

1. Which setting helped more on your run, the examples or the repair? Is
   the difference bigger than the difference between two runs?
2. A refusal scores 0 on an answerable question. Would a company rather
   have a wrong number or no number? Should the score say so?
3. For **your team project's graph**: which three example queries would you
   write first, and which question must it refuse?

## Optional

- Point the lab at your running Session 2 endpoint instead of the file:
  `SPARQL_ENDPOINT=http://127.0.0.1:3030/kr/sparql python ask.py "..."`
  (Session 2's Fuseki, its `kr` dataset, started from `demos/` with `docker compose up -d`).
- **Ollama, no key:** `ollama pull qwen2.5-coder:7b` (4.7 GB), then
  `LLM_BASE_URL=http://localhost:11434/v1 LLM_MODEL=qwen2.5-coder:7b python evaluate.py`.
- **void-generator** (SIB, Java 17 or later, needs a running endpoint)
  writes the same kind of VoID file from any endpoint:
  `java -jar void-generator-0.19-uber.jar -r <endpoint> -p <endpoint> --void-file void.ttl --iri-of-void https://ul.edu.lb/kr/brunel/void`.
- **The official harness:** `text2sparql-client` (Python 3.11+) can read
  `questions.yaml` and call `serve.py`. Install it in a separate
  environment: it needs numpy below 2, which the course environment
  cannot have.
- **sparql-llm** (SIB, the leading system of TEXT2SPARQL 2026) does these
  same steps at scale, with embeddings for picking examples. It is about
  215 MB and downloads a model on first import: try it in a separate
  environment.

## You understood this lab if you can say

- why the model gets the VoID description and not the whole ontology;
- what the check catches, what it cannot catch, and why its message is a hint;
- why the refusal path is part of the design, not a failure;
- how TEXT2SPARQL scores one answer, and why a query's text is not judged;
- why your score and the recorded score can differ.

## Take it to your team project

- Generate `void.ttl` for your own graph (`make_void.py` with your file, or
  void-generator on your endpoint).
- Write 6 to 10 example queries for your own graph in `examples.ttl`'s
  layout, and a test set in `questions.yaml`'s layout, never overlapping.
- Record your score before and after one improvement, with the model and
  the date.
- Add `deploy/compose-access-layer.yml` to your stack for Session 8, with
  `SPARQL_ENDPOINT` pointing at your endpoint and your key in `.env`.
