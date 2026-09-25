# Read first: what this lab is doing

Do not begin with a command. First understand the question this lab asks:

> Can a model learn something useful from the shape of the Brunel graph, and
> how do we know the number it reports is honest?

This is an individual practice lab. Nothing is submitted or graded.

## The short story

Session 5 turned the Brunel tables into a graph: 9,215 orders, each linked
to its customer, carrier, plant, port and product. Today two kinds of model
learn from it.

- A **graph neural network** (GraphSAGE) predicts which orders are late,
  using each order's own values and what its neighbours hold.
- A **knowledge graph embedding** (TransE) predicts a missing link: which
  plant makes a product.

Each is compared with the simplest model that could do the job: a logistic
regression on the order's row, and "the plant that makes the most products".
The honest result is the lesson. The graph model looks better only when the
test lets it memorise customers, and the embedding loses to the count.

```text
Session 5's graph (brunel-mapped.nt, 135,799 triples)
        |
        | build_graph.py: label removed, nodes and edges by kind
        v
data/brunel-graph.pt (PyTorch Geometric HeteroData)
        |                         |                          |
   baseline.py                 gnn.py                 link_prediction.py
   logistic regression         GraphSAGE              TransE (PyKEEN)
   on the order row            (to_hetero)            against popularity
        \_________ same splits: random, and by customer _________/
```

## The data you are using

The graph Session 5's mapping built from four Brunel tables (Brunel
University London, *Supply Chain Logistics Problem Dataset*, Figshare
7558679 v2, CC BY 4.0). If it is missing, `build_graph.py` reads Session 2's
graph instead: the same orders.

| Kind of node | How many | What the model sees about it |
|---|---|---|
| order | 9,215 | weight, unit quantity, service level (CRF, DTD or DTP) |
| customer | 46 | only which one it is |
| carrier | 3 | only which one it is |
| plant | 20 | only which one it is (PLANT01 to PLANT19, and CND9, which appears only in ProductsPerPlant; orders ship from 7 of them) |
| port | 11 | only which one it is |
| product | 1,540 | only which one it is |

Edges: each order's customer, carrier, plant, port and product (9,215 each),
which plant makes which product (2,036), which plant serves which port (22).

**The label:** is the order late? 192 of 9,215 are (2.1%). In the graph it
appears twice, as the class `ul:LateOrder` and as the value `ul:lateDays`.
`build_graph.py` removes both from what the model sees.

## Facts about the data that decide everything

- Only **4 of 46 customers** ever have a late order. Late orders are almost
  entirely "which customer".
- **Every order has the same date**, 2013-05-26. A split by time, the right
  test for data with dates, is impossible here; the lab splits by customer
  instead.
- Guessing scores PR-AUC 0.021 (the share of late orders), and "never late"
  scores accuracy 0.979. Accuracy is useless here.

## What each step proves

| Step | You run | What it does | What you should understand afterward |
|---|---|---|---|
| 1 | `build_graph.py` | Reads the RDF graph and writes a PyTorch Geometric graph, label removed. | A knowledge graph becomes tables of features and lists of edges, one per kind. |
| 2 | `baseline.py` | Logistic regression: with the label left in, with a random split, with a split by customer. | A perfect score means a leak; a random split rewards memory; a split by customer tests what was learned. |
| 3 | `gnn.py` | GraphSAGE through `to_hetero`, on the same splits. | Message passing uses the neighbours; here it only helps to remember customers. |
| 4 | `link_prediction.py` | TransE ranks plants for hidden "makes" links, against popularity. | A simple count can beat an embedding; some links cannot be predicted at all. |
| B | `my_learning.py`, `check_my_learning.py` | You write three functions, each a copy of one in `learning_utils.py` with one change. | Splits and ranking scores are a few lines each. |
| C | questions | What would a split by time need, for your own data? | How to design an honest test for your project. |

## The files and their roles

| File | Role | Do you edit it? |
|---|---|---|
| `build_graph.py` | RDF graph to PyTorch Geometric graph, label removed. | No; run it. |
| `learning_utils.py` | The splits and scores the scripts use: the worked examples for Part B. | No; read it. |
| `baseline.py` | The logistic regression baseline, three runs. | No; run it. |
| `gnn.py` | The graph neural network. | No; read it and run it. |
| `link_prediction.py` | TransE against popularity. | No; run it. |
| `data/brunel-graph.pt` | The converted graph. Generated. | No; regenerate it. |
| `my_learning.py` | Your work area for Part B. | Yes. |
| `check_my_learning.py` | Checks your three functions. | No. |
| `solutions/`, `reference-outputs/` | Answers, and a real run of every step. | Read them; do not edit. |

## Terms you need before running the lab

| Term | Plain definition |
|---|---|
| **node classification** | Predicting a label for each node, here "late or not" for each order. |
| **link prediction** | Predicting a missing edge, here "plant makes product". |
| **baseline** | The simplest reasonable model; a new model must be compared with it. |
| **message passing** | Each node updates itself from what its neighbours send it, one round per layer. |
| **GraphSAGE** | A graph neural network layer: a node combines its own values with the average of its neighbours'. |
| **to_hetero** | PyTorch Geometric's tool that copies a model once per kind of edge. |
| **embedding** | A short list of numbers learned for each thing, so that related things end up close. |
| **TransE** | An embedding where head + relation should land near the tail. |
| **PR-AUC** | How well late orders are ranked above the rest; guessing scores the share of late orders. |
| **MRR, Hits@k** | For link prediction: the average of 1/rank of the right answer; the share of right answers in the top k. |
| **leakage** | When the test lets the model see the answer, or something that gives it away. |

## How to judge an assertion in this lab

1. **Source fact:** what the data holds, such as 192 late orders from only 4
   customers, or one order date for all.
2. **Course decision:** how the lab sets the test, such as removing
   `lateDays`, or splitting by customer.
3. **Result:** what a model scored, such as PR-AUC 0.788 on a random split.
   A result is only as honest as the split it was measured on.

Now return to the [lab README](README.md) and begin Part A.
