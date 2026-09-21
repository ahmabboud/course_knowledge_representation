"""Session 6 lab, step 5 -- the graded evaluation core: random split
vs. temporal split on the SAME late-delivery node classification task
(same model, same hyperparameters, same training protocol). This is
the single most important real finding in this lab.

THE INJECTED REAL LEAK (full mechanism in build_heterodata.py's
docstring): Port of Hamburg suffers a genuine congestion event
starting 2026-01-01. Before that date its late rate is ~42%; from that
date on it jumps to ~100% (real numbers, see build_heterodata.py's own
output). No node feature encodes "is this the congested regime" -- the
only way a model can know about it is to have been TRAINED on orders
from that period.

PROTOCOL (kept identical between the two splits so the comparison is
fair -- and genuinely INDUCTIVE, not just a different labeling of a
transductive split):
  1. Pick a test set of ORDER nodes, either
       (a) uniformly at random (30%), or
       (b) all orders dispatched on/after a cutoff date, sized to
           match the random test set as closely as possible.
  2. Build a TRAIN-TIME graph containing ONLY the train+val orders and
     their edges (the test orders/edges do not exist yet at training
     time -- the honest, deployment-realistic setup: in reality you
     cannot message-pass over orders that have not been created yet).
  3. Train a to_hetero(GraphSAGE) node classifier on the train-time
     graph only, with early stopping on a validation slice carved out
     of the train orders (never touching test).
  4. Build the FULL graph (train + val + test orders/edges) and run a
     single inductive forward pass; read off predictions for the test
     order nodes only.
  5. Report accuracy/F1 for both splits, side by side.

What had to be engineered to make the gap show up at all (worth
knowing before you tweak this): the first naive design -- plain random
70/15/15 split trained/evaluated TRANSDUCTIVELY on the whole static
graph at once, no regime change in the data -- showed NO gap, because
(a) a transductive GNN sees every node's features regardless of
train/test label masking, so temporal vs. random LABELING of a static
graph doesn't by itself withhold any structural information, and (b)
without an injected regime change there's no actual distribution shift
to leak. Two changes were required: a genuine temporal regime change
in the data-generating process, AND an inductive evaluation protocol
(train-time graph excludes the test period's orders/edges entirely,
not just their labels).

Run a single seed (fast, ~2s):
    python3 leakage_demo.py

Run the 5-seed robustness check the syllabus's "a split leaks" review
calls for (same fixed dataset throughout -- only model-init/training
stochasticity varies across seeds, ~10s total):
    python3 leakage_demo.py --seeds 0 1 2 3 4

A single run's accuracy gap is noisy on a 108-example test set (one
seed even shows a small negative gap, see the README) -- the
reproducible finding across seeds is qualitative: the temporally-split
model's test accuracy never beats its own majority-class baseline,
while the randomly-split model usually does.
"""
import argparse
import json
import time
from datetime import date
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
import torch_geometric.transforms as T
from sklearn.metrics import accuracy_score, f1_score
from torch_geometric.nn import to_hetero

from build_heterodata import build_graph, load_or_build
from train_node_classification import SAGE

HERE = Path(__file__).resolve().parent
RESULTS_PATH = HERE / "data" / "leakage_demo_results.json"

TEST_FRAC = 0.30
HIDDEN = 16
EPOCHS = 200
PATIENCE = 20


def random_split(n_orders, test_frac=TEST_FRAC, seed=0):
    g = torch.Generator().manual_seed(seed)
    perm = torch.randperm(n_orders, generator=g).tolist()
    n_test = int(round(test_frac * n_orders))
    return sorted(perm[n_test:]), sorted(perm[:n_test])


def temporal_split(orders, test_frac=TEST_FRAC):
    """Test = the most recent `test_frac` of orders by dispatch date
    (cutoff chosen so the test set size matches the random split's as
    closely as possible). Train = everything dispatched strictly
    before the cutoff."""
    dispatch_ordinals = np.array([o["dispatch"].toordinal() for o in orders])
    order = np.argsort(dispatch_ordinals)
    n = len(orders)
    n_test = int(round(test_frac * n))
    cutoff_pos = n - n_test
    cutoff_date = date.fromordinal(int(dispatch_ordinals[order[cutoff_pos]]))
    train_idx = sorted(int(i) for i in order[:cutoff_pos])
    test_idx = sorted(int(i) for i in order[cutoff_pos:])
    return train_idx, test_idx, cutoff_date


def carve_val_from_train(train_idx, val_frac=0.15, seed=0):
    g = torch.Generator().manual_seed(seed)
    perm = torch.randperm(len(train_idx), generator=g).tolist()
    n_val = int(round(val_frac * len(train_idx)))
    val_pos = set(perm[:n_val])
    real_train = [train_idx[i] for i in range(len(train_idx)) if i not in val_pos]
    val = [train_idx[i] for i in range(len(train_idx)) if i in val_pos]
    return real_train, val


def build_inductive_graphs(dataset, train_idx, val_idx, test_idx):
    """Returns (train_graph, full_graph, n_train, n_val, n_test):
    train_graph contains only train+val orders (val is still "seen" at
    training time, as part of the labeled pool used for early
    stopping -- only TEST is held back structurally), full_graph
    appends the test orders/edges afterwards in the same fixed order,
    so slicing works: [0:n_train]=train, [n_train:n_train+n_val]=val,
    [n_train+n_val:]=test."""
    train_val_idx = train_idx + val_idx
    train_graph, _, _ = build_graph(dataset, order_indices=train_val_idx)
    train_graph = T.ToUndirected()(train_graph)

    full_graph, _, _ = build_graph(dataset, order_indices=train_val_idx + test_idx)
    full_graph = T.ToUndirected()(full_graph)

    return train_graph, full_graph, len(train_idx), len(val_idx), len(test_idx)


def run_split(name, dataset, train_idx, val_idx, test_idx, epochs=EPOCHS, patience=PATIENCE, hidden=HIDDEN):
    train_graph, full_graph, n_train, n_val, n_test = build_inductive_graphs(dataset, train_idx, val_idx, test_idx)

    train_mask = torch.zeros(n_train + n_val, dtype=torch.bool)
    train_mask[:n_train] = True
    val_mask = torch.zeros(n_train + n_val, dtype=torch.bool)
    val_mask[n_train:] = True
    y_train_graph = train_graph["order"].y

    model = SAGE(hidden_channels=hidden, out_channels=2)
    model = to_hetero(model, train_graph.metadata(), aggr="sum")
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-3)

    x_dict, ei_dict = train_graph.x_dict, train_graph.edge_index_dict
    with torch.no_grad():
        model(x_dict, ei_dict)

    best_val_acc, best_state, best_epoch, no_improve = -1.0, None, 0, 0
    t0 = time.time()
    for epoch in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad()
        out = model(x_dict, ei_dict)["order"]
        loss = F.cross_entropy(out[train_mask], y_train_graph[train_mask])
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            out = model(x_dict, ei_dict)["order"]
            val_acc = (out.argmax(dim=-1)[val_mask] == y_train_graph[val_mask]).float().mean().item()

        if val_acc > best_val_acc:
            best_val_acc, best_state, best_epoch, no_improve = (
                val_acc, {k: v.clone() for k, v in model.state_dict().items()}, epoch, 0)
        else:
            no_improve += 1
        if no_improve >= patience:
            break
    train_time = time.time() - t0

    model.load_state_dict(best_state)

    # Inductive evaluation: a forward pass on the FULL graph (train+val
    # orders unchanged, test orders/edges appearing for the first
    # time), reading off predictions for the test slice only.
    model.eval()
    with torch.no_grad():
        pred_full = model(full_graph.x_dict, full_graph.edge_index_dict)["order"].argmax(dim=-1)

    y_full = full_graph["order"].y
    test_pred = pred_full[n_train + n_val:]
    test_true = y_full[n_train + n_val:]

    acc = accuracy_score(test_true.numpy(), test_pred.numpy())
    f1 = f1_score(test_true.numpy(), test_pred.numpy(), zero_division=0)
    base_rate_ontime = 1 - test_true.float().mean().item()
    base_rate_late = test_true.float().mean().item()

    print(f"[{name}] n_train={n_train} n_val={n_val} n_test={n_test}  "
          f"best_epoch={best_epoch}  best_val_acc={best_val_acc:.3f}  train_time={train_time:.2f}s")
    print(f"[{name}] test late-rate={base_rate_late:.3f}  "
          f"majority-class baseline acc={max(base_rate_ontime, base_rate_late):.3f}")
    print(f"[{name}] TEST accuracy={acc:.4f}  F1={f1:.4f}")

    return dict(
        name=name, n_train=n_train, n_val=n_val, n_test=n_test,
        best_epoch=best_epoch, best_val_acc=best_val_acc, train_time_s=train_time,
        test_late_rate=base_rate_late,
        majority_baseline_acc=max(base_rate_ontime, base_rate_late),
        test_accuracy=acc, test_f1=f1,
    )


def run_one_seed(dataset, seed, verbose_headers=False):
    orders = dataset["orders"]
    n = len(orders)

    if verbose_headers:
        print("=" * 70 + "\nRANDOM SPLIT\n" + "=" * 70)
    torch.manual_seed(seed)
    r_train_full, r_test = random_split(n, seed=seed)
    r_train, r_val = carve_val_from_train(r_train_full, seed=seed)
    random_result = run_split(f"RANDOM seed={seed}", dataset, r_train, r_val, r_test)

    if verbose_headers:
        print("\n" + "=" * 70 + "\nTEMPORAL SPLIT\n" + "=" * 70)
    torch.manual_seed(seed)
    t_train_full, t_test, cutoff_date = temporal_split(orders, test_frac=TEST_FRAC)
    t_train, t_val = carve_val_from_train(t_train_full, seed=seed)
    if verbose_headers:
        print(f"Temporal cutoff date: {cutoff_date} (test = orders dispatched on/after this date)")
    temporal_result = run_split(f"TEMPORAL seed={seed}", dataset, t_train, t_val, t_test)
    temporal_result["cutoff_date"] = str(cutoff_date)

    gap = random_result["test_accuracy"] - temporal_result["test_accuracy"]
    return random_result, temporal_result, gap, cutoff_date


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seeds", type=int, nargs="+", default=[0],
                         help="One or more seeds. A single seed (default) runs the primary "
                              "demo with full side-by-side printout. Several seeds (e.g. "
                              "'--seeds 0 1 2 3 4') run the robustness check: same fixed "
                              "dataset throughout, only model-init/training stochasticity varies.")
    args = parser.parse_args()

    dataset, _ = load_or_build()  # built once, fixed for every seed below

    if len(args.seeds) == 1:
        seed = args.seeds[0]
        random_result, temporal_result, gap, cutoff_date = run_one_seed(dataset, seed, verbose_headers=True)

        print()
        print("=" * 70)
        print("SIDE-BY-SIDE COMPARISON")
        print("=" * 70)
        print(f"{'metric':<28}{'RANDOM split':<18}{'TEMPORAL split':<18}")
        print(f"{'n_test':<28}{random_result['n_test']:<18}{temporal_result['n_test']:<18}")
        print(f"{'test late-rate':<28}{random_result['test_late_rate']:<18.3f}{temporal_result['test_late_rate']:<18.3f}")
        print(f"{'majority-class baseline':<28}{random_result['majority_baseline_acc']:<18.3f}{temporal_result['majority_baseline_acc']:<18.3f}")
        print(f"{'GNN test accuracy':<28}{random_result['test_accuracy']:<18.4f}{temporal_result['test_accuracy']:<18.4f}")
        print(f"{'GNN test F1':<28}{random_result['test_f1']:<18.4f}{temporal_result['test_f1']:<18.4f}")
        print(f"\nAccuracy gap (random - temporal): {gap:+.4f}")

        out = dict(random=random_result, temporal=temporal_result, accuracy_gap=gap)
    else:
        rows = []
        for seed in args.seeds:
            print(f"\n{'#' * 70}\nSEED {seed}\n{'#' * 70}")
            random_result, temporal_result, gap, _ = run_one_seed(dataset, seed)
            print(f"--- seed={seed} GAP (random_acc - temporal_acc) = {gap:+.4f}  "
                  f"(random_f1={random_result['test_f1']:.3f} temporal_f1={temporal_result['test_f1']:.3f})")
            rows.append(dict(
                seed=seed, random_acc=random_result["test_accuracy"], temporal_acc=temporal_result["test_accuracy"],
                random_f1=random_result["test_f1"], temporal_f1=temporal_result["test_f1"],
                random_baseline=random_result["majority_baseline_acc"],
                temporal_baseline=temporal_result["majority_baseline_acc"], gap=gap,
            ))

        gaps = [r["gap"] for r in rows]
        n_positive = sum(1 for g in gaps if g > 0)
        n_temporal_below_baseline = sum(1 for r in rows if r["temporal_acc"] <= r["temporal_baseline"])
        n_random_below_baseline = sum(1 for r in rows if r["random_acc"] <= r["random_baseline"])
        print(f"\n{'=' * 70}\nSUMMARY ACROSS {len(rows)} SEEDS\n{'=' * 70}")
        print(f"Mean gap: {sum(gaps) / len(gaps):+.4f}   Range: [{min(gaps):+.4f}, {max(gaps):+.4f}]")
        print(f"Gap positive (random > temporal) in {n_positive}/{len(gaps)} seeds")
        print(f"Temporal test acc <= its own majority baseline in {n_temporal_below_baseline}/{len(gaps)} seeds")
        print(f"Random test acc <= its own majority baseline in {n_random_below_baseline}/{len(gaps)} seeds")

        out = dict(rows=rows, mean_gap=sum(gaps) / len(gaps), min_gap=min(gaps), max_gap=max(gaps))

    RESULTS_PATH.parent.mkdir(exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved results to {RESULTS_PATH.relative_to(HERE)}")


if __name__ == "__main__":
    main()
