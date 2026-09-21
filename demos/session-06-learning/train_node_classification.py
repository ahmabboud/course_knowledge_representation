"""Session 6 lab, step 2 -- late-delivery node classification on the
ORDER node type, trained two ways on the identical HeteroData graph
from build_heterodata.py:

  (a) `to_hetero()` wrapping a plain 2-layer GraphSAGE backbone (the
      "one-line" version -- write a homogeneous GNN once, PyG turns it
      into a heterogeneous one automatically).
  (b) an explicitly wired `RGCNConv` model (relation-specific weight
      matrices, built by hand).

Both are evaluated on the same random 70/15/15 train/val/test split of
ORDER nodes (transductive: every node/edge is visible, only the
order-node LABELS are masked). Real accuracy/F1/precision/recall are
printed for both and saved to data/node_classification_results.json.

Run:
    python3 train_node_classification.py

Two real, load-bearing gotchas fixed here (both hit for real while
building this graph, not hypothetical):

  GOTCHA 1 (blocking). Edges are built directed order -> {supplier,
  product, carrier, port, plant}. Feeding that straight into
  `to_hetero()` crashes:
      ValueError: Cannot generate a graph node 'relu' for type 'order'
      since it does not exist. Please make sure that all node types
      get updated during message passing.
  because `order` never appears as a DESTINATION type, so its
  embedding is never produced by the transformed module's call graph
  (`to_hetero()`'s fx-based tracer only emits per-type update code for
  node types that receive at least one relation). Fix: add reverse
  edges with `torch_geometric.transforms.ToUndirected()` before
  calling `to_hetero()`, so every node type receives messages.
  `RGCNConv` needs the same fix, applied separately (by hand) in
  `to_homogeneous_for_rgcn()`, on the ORIGINAL directed graph rather
  than the `ToUndirected()` copy, to avoid double-adding reverse edges.

  GOTCHA 2 (non-blocking, but silently wrong). A fixed 100-epoch
  training loop with `hidden_channels=32` drives the `to_hetero`/SAGE
  model to 100% TRAIN accuracy while TEST accuracy falls BELOW the
  majority-class baseline -- textbook transductive overfitting on a
  tiny graph (360 order nodes, 9 relations x 2 with reverses, each its
  own SAGEConv). Fix: shrink hidden_channels 32 -> 16, add
  weight_decay, and early-stop on a held-out validation split
  (patience-based) instead of a fixed epoch count, applied identically
  to both models for a fair comparison.
"""
import argparse
import json
import time
from pathlib import Path

import torch
import torch.nn.functional as F
import torch_geometric.transforms as T
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from torch_geometric.nn import RGCNConv, SAGEConv, to_hetero

from build_heterodata import load_or_build

HERE = Path(__file__).resolve().parent
RESULTS_PATH = HERE / "data" / "node_classification_results.json"

SEED = 0


def make_splits(n, seed=0, ratios=(0.7, 0.15, 0.15)):
    g = torch.Generator().manual_seed(seed)
    perm = torch.randperm(n, generator=g)
    n_train = int(ratios[0] * n)
    n_val = int(ratios[1] * n)
    train_idx, val_idx, test_idx = perm[:n_train], perm[n_train:n_train + n_val], perm[n_train + n_val:]
    train_mask = torch.zeros(n, dtype=torch.bool)
    val_mask = torch.zeros(n, dtype=torch.bool)
    test_mask = torch.zeros(n, dtype=torch.bool)
    train_mask[train_idx] = True
    val_mask[val_idx] = True
    test_mask[test_idx] = True
    return train_mask, val_mask, test_mask


def metrics(y_true, y_pred):
    return dict(
        accuracy=accuracy_score(y_true, y_pred),
        f1=f1_score(y_true, y_pred, zero_division=0),
        precision=precision_score(y_true, y_pred, zero_division=0),
        recall=recall_score(y_true, y_pred, zero_division=0),
    )


# ---------------------------------------------------------------------
# (a) to_hetero() + GraphSAGE backbone
# ---------------------------------------------------------------------

class SAGE(torch.nn.Module):
    """Plain homogeneous 2-layer GraphSAGE, written exactly like you
    would for a single node/edge type graph. `to_hetero()` does the
    heavy lifting of turning this into a per-relation model."""

    def __init__(self, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x


def run_to_hetero(data, train_mask, val_mask, test_mask, epochs, patience, hidden_channels):
    model = SAGE(hidden_channels=hidden_channels, out_channels=2)
    model = to_hetero(model, data.metadata(), aggr="sum")
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-3)

    x_dict, edge_index_dict, y = data.x_dict, data.edge_index_dict, data["order"].y

    with torch.no_grad():
        model(x_dict, edge_index_dict)  # lazy init: materializes the (-1,-1) SAGEConv weight shapes

    best_val_acc, best_state, best_epoch, epochs_no_improve = -1.0, None, 0, 0
    t0 = time.time()
    for epoch in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad()
        out = model(x_dict, edge_index_dict)["order"]
        loss = F.cross_entropy(out[train_mask], y[train_mask])
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            out = model(x_dict, edge_index_dict)["order"]
            val_acc = (out.argmax(dim=-1)[val_mask] == y[val_mask]).float().mean().item()

        if val_acc > best_val_acc:
            best_val_acc, best_state, best_epoch, epochs_no_improve = (
                val_acc, {k: v.clone() for k, v in model.state_dict().items()}, epoch, 0)
        else:
            epochs_no_improve += 1

        if epoch % 20 == 0 or epoch == 1:
            print(f"  [to_hetero/SAGE] epoch {epoch:3d}  loss={loss.item():.4f}  val_acc={val_acc:.3f}")
        if epochs_no_improve >= patience:
            print(f"  [to_hetero/SAGE] early stopping at epoch {epoch} (best val_acc={best_val_acc:.3f} @ epoch {best_epoch})")
            break
    train_time = time.time() - t0

    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        pred = model(x_dict, edge_index_dict)["order"].argmax(dim=-1)

    train_m, val_m, test_m = (metrics(y[m].numpy(), pred[m].numpy()) for m in (train_mask, val_mask, test_mask))
    print(f"  [to_hetero/SAGE] train_time={train_time:.2f}s  best_epoch={best_epoch}")
    print(f"  [to_hetero/SAGE] train:{train_m}")
    print(f"  [to_hetero/SAGE] val:  {val_m}")
    print(f"  [to_hetero/SAGE] test: {test_m}")
    return dict(train=train_m, val=val_m, test=test_m, train_time_s=train_time, best_epoch=best_epoch,
                n_params=sum(p.numel() for p in model.parameters()))


# ---------------------------------------------------------------------
# (b) explicit RGCNConv model
# ---------------------------------------------------------------------

class RGCNNodeClassifier(torch.nn.Module):
    """Explicitly wired R-GCN over the whole heterogeneous graph.

    RGCNConv only supports a HOMOGENEOUS edge_index + an integer
    edge_type vector (one weight matrix per relation id), so unlike
    to_hetero() we have to (1) concatenate every node type into one
    flat node index space (padded to a common feature width) and (2)
    concatenate every relation's edge_index into one edge_index, with
    a parallel edge_type tensor. This is exactly the "parameter
    explosion" trade-off from the lecture: RGCNConv gets one
    in_channels x out_channels weight matrix PER RELATION (or
    num_bases of them, with basis decomposition), whereas to_hetero()
    reuses the same 2-layer SAGE weights defined once by copying the
    module graph per relation -- structurally similar cost, written
    completely differently. `num_bases`/`num_blocks` exist specifically
    to tame RGCNConv's growth (not used here, num_bases=None, but real
    verified constructor args)."""

    def __init__(self, in_channels, hidden_channels, out_channels, num_relations, num_bases=None):
        super().__init__()
        self.conv1 = RGCNConv(in_channels, hidden_channels, num_relations, num_bases=num_bases)
        self.conv2 = RGCNConv(hidden_channels, out_channels, num_relations, num_bases=num_bases)

    def forward(self, x, edge_index, edge_type):
        x = self.conv1(x, edge_index, edge_type).relu()
        return self.conv2(x, edge_index, edge_type)


def to_homogeneous_for_rgcn(data):
    """Builds a single flat node feature matrix (zero-padded to the
    widest per-type feature dim) plus global node index offsets, and a
    homogeneous edge_index/edge_type pair covering every relation in
    `data`, including the reverse of each (RGCNConv needs both
    directions to pass messages both ways -- added here by hand, on
    the ORIGINAL directed `data`, to keep the relation vocabulary
    explicit and to avoid double-adding reverses that ToUndirected()
    would already have added). Returns everything needed to run
    RGCNConv plus the global index range for 'order' nodes."""
    node_types = data.node_types
    max_dim = max(data[nt].x.size(-1) for nt in node_types)

    offsets, offset, xs = {}, 0, []
    for nt in node_types:
        offsets[nt] = offset
        x = data[nt].x
        if x.size(-1) < max_dim:
            x = torch.cat([x, torch.zeros(x.size(0), max_dim - x.size(-1))], dim=-1)
        xs.append(x)
        offset += data[nt].x.size(0)
    x_all = torch.cat(xs, dim=0)

    edge_types = data.edge_types
    edge_index_list, edge_type_list = [], []
    for rel_id, (src_t, rel, dst_t) in enumerate(edge_types):
        ei = data[(src_t, rel, dst_t)].edge_index
        src, dst = ei[0] + offsets[src_t], ei[1] + offsets[dst_t]
        edge_index_list.append(torch.stack([src, dst], dim=0))
        edge_type_list.append(torch.full((ei.size(1),), rel_id, dtype=torch.long))
        rev_rel_id = len(edge_types) + rel_id
        edge_index_list.append(torch.stack([dst, src], dim=0))
        edge_type_list.append(torch.full((ei.size(1),), rev_rel_id, dtype=torch.long))

    edge_index = torch.cat(edge_index_list, dim=1)
    edge_type = torch.cat(edge_type_list, dim=0)
    num_relations = 2 * len(edge_types)

    order_start = offsets["order"]
    order_end = order_start + data["order"].x.size(0)
    return x_all, edge_index, edge_type, num_relations, order_start, order_end


def run_rgcn(data, train_mask, val_mask, test_mask, epochs, patience, hidden_channels):
    x_all, edge_index, edge_type, num_relations, order_start, order_end = to_homogeneous_for_rgcn(data)
    y = data["order"].y

    model = RGCNNodeClassifier(
        in_channels=x_all.size(-1), hidden_channels=hidden_channels, out_channels=2,
        num_relations=num_relations, num_bases=None,
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-3)

    best_val_acc, best_state, best_epoch, no_improve = -1.0, None, 0, 0
    t0 = time.time()
    for epoch in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad()
        out_order = model(x_all, edge_index, edge_type)[order_start:order_end]
        loss = F.cross_entropy(out_order[train_mask], y[train_mask])
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            out_order = model(x_all, edge_index, edge_type)[order_start:order_end]
            val_acc = (out_order.argmax(dim=-1)[val_mask] == y[val_mask]).float().mean().item()

        if val_acc > best_val_acc:
            best_val_acc, best_state, best_epoch, no_improve = (
                val_acc, {k: v.clone() for k, v in model.state_dict().items()}, epoch, 0)
        else:
            no_improve += 1

        if epoch % 20 == 0 or epoch == 1:
            print(f"  [RGCNConv]       epoch {epoch:3d}  loss={loss.item():.4f}  val_acc={val_acc:.3f}")
        if no_improve >= patience:
            print(f"  [RGCNConv]       early stopping at epoch {epoch} (best val_acc={best_val_acc:.3f} @ epoch {best_epoch})")
            break
    train_time = time.time() - t0

    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        pred = model(x_all, edge_index, edge_type)[order_start:order_end].argmax(dim=-1)

    train_m, val_m, test_m = (metrics(y[m].numpy(), pred[m].numpy()) for m in (train_mask, val_mask, test_mask))
    print(f"  [RGCNConv]       train_time={train_time:.2f}s  num_relations={num_relations}  best_epoch={best_epoch}")
    print(f"  [RGCNConv]       train:{train_m}")
    print(f"  [RGCNConv]       val:  {val_m}")
    print(f"  [RGCNConv]       test: {test_m}")
    return dict(train=train_m, val=val_m, test=test_m, train_time_s=train_time,
                num_relations=num_relations, best_epoch=best_epoch,
                n_params=sum(p.numel() for p in model.parameters()))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--patience", type=int, default=20, help="Early-stopping patience, in epochs with no val-accuracy improvement.")
    parser.add_argument("--hidden-channels", type=int, default=16)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    _, data = load_or_build()

    n = data["order"].num_nodes
    train_mask, val_mask, test_mask = make_splits(n, seed=args.seed)
    print(f"\nOrder nodes: {n}  train={train_mask.sum().item()} val={val_mask.sum().item()} test={test_mask.sum().item()}")
    print(f"Base rate (majority-class accuracy if always predicting 'on time'): "
          f"{1 - data['order'].y.float().mean().item():.3f}")

    # See GOTCHA 1 above: add reverse edges so every node type
    # (including 'order') receives at least one message.
    data_undirected = T.ToUndirected()(data.clone())
    print(data_undirected)

    print("\n=== (a) to_hetero() + GraphSAGE ===")
    sage_results = run_to_hetero(data_undirected, train_mask, val_mask, test_mask,
                                  epochs=args.epochs, patience=args.patience, hidden_channels=args.hidden_channels)

    print("\n=== (b) explicit RGCNConv ===")
    rgcn_results = run_rgcn(data, train_mask, val_mask, test_mask,
                             epochs=args.epochs, patience=args.patience, hidden_channels=args.hidden_channels)

    RESULTS_PATH.parent.mkdir(exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(dict(to_hetero_sage=sage_results, rgcn=rgcn_results), f, indent=2)
    print(f"\nSaved results to {RESULTS_PATH.relative_to(HERE)}")


if __name__ == "__main__":
    main()
