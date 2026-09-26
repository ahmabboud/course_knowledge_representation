# Session 6 lab: learning over the graph

**Read this first:** [What this lab is doing](OVERVIEW.md). It explains the
data, why each step exists, and the role of every file.

**Why this lab exists:** to make the lecture concrete (embeddings, message
passing, leakage) on the Brunel graph Session 5 built, and to give you the
evaluation pattern Milestone 2 asks for on your own project. Nothing is
handed in or graded.

Every number in `lectures/kr-session-06.html` that comes from a run comes
from the files in `reference-outputs/`, produced by these scripts on
2026-09-25 (CPU only, no GPU needed).

## Before you start

- The shared course environment `demos/.venv`, active, **installed with both
  lines** of `demos/README.md`. Session 6 adds PyTorch, PyTorch Geometric,
  PyKEEN and scikit-learn (about 400 MB). Already set up earlier? Run both
  install lines again now. **On Linux**, install the CPU build of PyTorch
  first (the command is in `demos/README.md`).
- Session 5's graph exists (`demos/session-05-integration/brunel-mapped.nt`,
  from its `materialize.py`). If not, `build_graph.py` uses Session 2's
  `brunel.ttl` instead: the same orders.
- Run every command from this folder, `demos/session-06-learning/`.

## Part A · build and observe (about 30 minutes)

1. `python build_graph.py`. Turns the RDF graph into a PyTorch Geometric
   graph. **Expect:** `nodes: order 9,215, customer 46, carrier 3, plant 20,
   port 11, product 1,540`, then `label: 192 late orders of 9,215 (2.1%),
   taken out of the features`. **Look at:** the `edges` loop in the script: one
   list of (source, target) pairs per kind of link, and `x`, the only three
   things the model knows about an order.
2. `python baseline.py`. Logistic regression on each order's row, three
   ways. **Expect:** line 1 (lateDays kept) `PR-AUC 1.000`; line 2 (random
   split) `PR-AUC 0.788` and `accuracy 0.944`; the split by customer between
   `0.002` and `0.019`, and seed 4 `nothing to measure`. **Notice:** guessing
   scores 0.021. A perfect score is a leak, and the split by customer is
   at the level of guessing.
3. `python gnn.py` (about 30 seconds). GraphSAGE, made heterogeneous with
   `to_hetero`, on the same splits. **Expect:** random split `PR-AUC` 0.859,
   0.864 and 0.875 over three training seeds; split by customer between
   `0.004` and `0.046`. **Look at:** `class SAGE`: two layers, so each order
   hears from nodes two links away. **Notice:** the argument is named
   `edge_index`; `to_hetero` fails with a confusing error under any other
   name.
4. `python link_prediction.py` (under a minute). TransE ranks the 19 plants
   for hidden "plant makes product" links. **Expect** for seed 0: `TransE
   MRR 0.555`, `popularity MRR 0.608`; on all three seeds the count wins.
   **Notice:** `72 left out`: a product that appears in no other link gives
   the model nothing to learn from.

Your numbers may differ in the last digit on another computer (PyTorch
training is not bit-for-bit the same everywhere). The pattern must not:
leak near 1.0, random split high, split by customer near 0.02, popularity
ahead of TransE.

## Part B · three small functions (about 15 minutes)

Open `my_learning.py` next to `learning_utils.py`. Each function is a copy
of one in `learning_utils.py` with one thing changed:

| Task | Write | Copy | Change |
|---|---|---|---|
| Y1 | `split_by_plant` | `split_by_customer` | group by plant |
| Y2 | `recall_at_k` | `precision_at_k` | divide by all late orders, not by k |
| Y3 | `hits_at_k` | `mrr` | average "rank at most k", not 1/rank |

Then:

```sh
python check_my_learning.py
```

It tests each function on small cases with known answers, and Y1 also on
the real plant of every order. **Expect** when all three are right: `3 of 3
right.` Stuck? `solutions/my_learning_solutions.py`. The common wrong
answers and their hints are in `reference-outputs/my-learning-check.txt`.

## Part C · think (about 10 minutes)

1. The random split scored PR-AUC 0.788 and the split by customer 0.019.
   Which number would you report to the company, and why?
2. Every Brunel order has the same date, so a split by time is impossible
   here. In **your team project's data**, which field is the date, and what
   would "train on the past, test on the future" look like?
3. Popularity beat TransE. When is losing to a baseline still a result
   worth reporting?

## Optional

- In `gnn.py`, set `EPOCHS` to 20 or `HIDDEN` to 8 and compare the random
  split.
- In `link_prediction.py`, try `model="DistMult"` in the `pipeline(...)`
  call.

## You understood this lab if you can say

- how an RDF graph becomes node features and edge lists, one per kind;
- why the label must leave the features, and where it was hiding twice;
- why accuracy is useless when 2% of orders are late;
- why a random split flatters and what a split by group tests instead;
- what MRR and Hits@k measure, and why "filtered" matters;
- why a simple count can beat an embedding.

## Take it to your team project

Milestone 2 (due at the end of this session, on your own topic) asks for a
node classification model, a link prediction model, a tabular baseline, a
split that does not leak, and a written evaluation of the limits. This lab
is the pattern:

- Convert your graph as `build_graph.py` does, and list what you removed
  from the features and why.
- Split by time if your data has dates; if not, split by group, as here,
  and say why. Never report only a random split.
- Report the baseline next to every model, and the score guessing gets.
- Run more than one seed and report the spread, not the best run.
