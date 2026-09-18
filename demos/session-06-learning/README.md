# Session 6 lab: graph neural networks, Milestone 2

Not built yet. This README states what the syllabus already commits
to.

## What the syllabus commits to

Construct a **PyTorch Geometric** `HeteroData` object from the
integrated graph (supplier, product, order, plant, port, carrier node
types), using a provided conversion utility so class time is not spent
on plumbing. Train a late-delivery node classification model: first
`to_hetero` over a GraphSAGE backbone in one line, then an explicitly
wired `RGCNConv` model, compared. Train a link prediction model with
`torch_geometric.nn.kge` (TransE), reading the roughly sixty lines of
the implementation rather than treating it as a black box. A 15-minute
team clinic reviewing each team's own Milestone 2 evaluation design,
focused on whether the split leaks.

This is **Milestone 2**: a trained heterogeneous node classification
model and a link prediction model, a leakage-free temporal split, a
tabular baseline, and a written evaluation of the limits, worth 20
percent of the grade.

## Real tools

PyTorch Geometric (`to_hetero`, `RGCNConv`, `torch_geometric.nn.kge`),
a gradient-boosted-tree library for the tabular baseline (e.g.
scikit-learn or XGBoost).

## What will live here once built

- `build_heterodata.py` — the provided conversion utility from the
  integrated graph to a PyG `HeteroData` object.
- `train_node_classification.py` — both the `to_hetero`/GraphSAGE and
  the explicit `RGCNConv` variants, compared.
- `train_link_prediction.py` — the TransE model via
  `torch_geometric.nn.kge`.
- `tabular_baseline.py` — the same prediction task on the flattened
  join, for honest comparison.

## What "done" looks like

Models train, the split is leakage-free and temporal where time
matters, a tabular baseline is reported, and a graph model that loses
to it, reported honestly with an explanation, scores full marks on this
line, per the rubric.
