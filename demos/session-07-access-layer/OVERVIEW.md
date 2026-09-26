# Read first: what this lab is doing

Do not begin with a command. First understand the question this lab asks:

> Can someone who knows no SPARQL ask the Brunel graph a question in plain
> English, get a correct answer with its evidence, and hear "I cannot
> answer that" when the graph does not hold the answer?

This is an individual practice lab. Nothing is submitted or graded.

## The short story

A language model writes the SPARQL. On its own it guesses: it invents
properties that sound right (`ul:shippedBy`), counts only `ul:Order` and
forgets the late orders, or answers a question the graph cannot answer. So
the lab wraps the model in four small parts, and measures what each adds.

```text
question in English
   |
   |  1 schema: what the graph holds, from its VoID description (void.ttl)
   |  2 examples: the 3 example queries closest to the question (examples.ttl)
   v
language model (Gemini) ---> a SPARQL query, or "REFUSE: ..."
   |
   |  3 check: valid SPARQL? only properties the graph has?
   |    if not: the problems go back to the model, up to 2 repairs
   v
the graph (Session 2's Brunel graph) ---> rows: the answer and its evidence
   |
   |  4 score: the rows against the right query's rows (TEXT2SPARQL's F1)
   v
a number you can compare, before and after one improvement
```

## The data you are using

Session 2's Brunel graph (`demos/session-02-rdf-sparql/brunel.ttl`, 135,841
triples), the same one your Fuseki or Oxigraph serves. Things in it are
named by **codes**, not names: carrier `V44_3`, plant `PLANT03`, port
`PORT04`, customer `V555_15`. So questions use codes too.

| File | What one entry is | Why the lab needs it |
|---|---|---|
| `void.ttl` | one class of the graph with its count, and each property with the class or datatype it points to | the schema the model is told about, and what the check compares against |
| `examples.ttl` | one question with its SPARQL, in the SHACL vocabulary sparql-llm uses | the model copies patterns from the closest ones |
| `questions.yaml` | one test question with its right ("gold") query, or with the reason it must be refused | the test set: 12 answerable, 3 not |

No test question is an example: a model that has seen the answer measures
nothing (Session 6's leak, in a new place).

## Facts about the data that decide everything

- The graph has **9,215 orders**, but only 9,023 are typed `ul:Order`: the
  192 late ones are typed `ul:LateOrder` only, a subclass. A query for
  `?o a ul:Order` answers 9,023, which is wrong.
- The graph has **no names, places, contact details or order status**. The
  questions about Beirut, an email address and cancelled orders must be
  refused.
- Only 3 carriers are typed `ul:Carrier` (V444_0, V444_1, V44_3), the ones
  with orders.

## What each step proves

| Step | You run | What it does | What you should understand afterward |
|---|---|---|---|
| 1 | `make_void.py` | Describes the graph with VoID: 189 triples. | A graph can describe itself; that description, not the whole ontology, goes to the model. |
| 2 | `show_prompt.py` | Prints the prompt for one question, without calling the model. | The prompt is rules, schema, three examples and the question: nothing hidden. |
| 3 | `ask.py` | Asks one question and shows each try, its problems, and the rows. | The rows are the evidence; a user can check the answer. |
| 4 | `check.py` | Checks a broken query. | The check turns a wrong guess into a hint the model can use. |
| 5 | `evaluate.py` | Scores 15 questions in three settings: schema only, plus examples, plus repair. | Each part's value is a measured number, not a belief. |
| 6 | `serve.py` | Serves the TEXT2SPARQL contract: one GET address. | A benchmark harness, or Session 8's stack, can call your access layer. |
| B | `my_examples.ttl`, `my_access.py`, `my_questions.yaml` | You add an example, a class check and a test question. | Each improvement is small, and each is measured. |
| C | questions | What would your own graph need? | How to build this for your project. |

## The files and their roles

| File | Role | Do you edit it? |
|---|---|---|
| `access_layer.py` | The five parts: schema, examples, model, check, loop. | No; read it. |
| `make_void.py`, `show_prompt.py`, `ask.py`, `check.py`, `evaluate.py`, `serve.py` | One script per step. | No; run them. |
| `score_utils.py` | TEXT2SPARQL's set precision, recall and F1. | No; read it. |
| `examples.ttl`, `questions.yaml`, `broken.sparql` | The examples, the test set, a broken query. | No. |
| `my_examples.ttl`, `my_access.py`, `my_questions.yaml` | Your part B work. | Yes. |
| `check_my_access.py` | Checks part B. No model call. | No. |
| `record_llm.py` | The instructor's recording run. | No. |
| `deploy/` | A container and a Compose service for Session 8. | Copy it into your team's stack. |
| `solutions/`, `reference-outputs/` | Answers, and a real run of every step (`llm-cache.json`: the recorded model answers). | Read them; do not edit. |

## Terms you need before running the lab

| Term | Plain definition |
|---|---|
| **text to SPARQL** | Turning a question in plain language into a SPARQL query. |
| **VoID** | Vocabulary of Interlinked Datasets: a small RDF description of a graph's classes, properties and counts. |
| **prompt** | Everything the model is given in one call: rules, schema, examples, question. |
| **few-shot examples** | Worked question and query pairs placed in the prompt for the model to imitate. |
| **validation and repair** | Checking the model's query and sending the problems back for another try. |
| **refusal** | Saying "the graph cannot answer this" instead of guessing. |
| **execution accuracy** | Judging a query by the answer it returns, not by its text. |
| **TEXT2SPARQL** | A yearly benchmark for text to SPARQL systems, with a fixed contract and scorer. |

## How to judge an assertion in this lab

1. **Source fact:** what the graph holds, such as 9,215 orders, 192 typed
   only `ul:LateOrder`, no customer locations.
2. **Course decision:** how the lab is built, such as 3 examples, 2 repairs,
   a refusal that scores 0 on an answerable question.
3. **Result:** what a model did, such as its F1 in one setting. A model's
   result is one run: yours may differ from the recording, and the
   difference is worth discussing.

Now return to the [lab README](README.md) and begin Part A.
