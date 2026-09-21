"""Session 6 lab, step 3 -- link prediction for supplier/product
relations using `torch_geometric.nn.kge.TransE`, read and used exactly
as its real ~60-line source is written
(`torch_geometric/nn/kge/{base,transe}.py` in the installed package):

  TransE(num_nodes, num_relations, hidden_channels, margin=1.0, p_norm=1.0, sparse=False)
  model.loader(head_index, rel_type, tail_index, batch_size=..., shuffle=...)
      -> torch_geometric.nn.kge.loader.KGTripletLoader
  model.loss(head_index, rel_type, tail_index) -> Tensor
  model.test(head_index, rel_type, tail_index, batch_size, k=10, log=True)
      -> (mean_rank: float, mrr: float, hits_at_k: float)

IMPORTANT REAL GOTCHA, the reason this lab also has train_pykeen.py:
`KGEModel.test()` (the base class TransE inherits from) computes RAW /
UNFILTERED ranking metrics -- it ranks the true tail against every
other node in the graph as a candidate, including other known-true
triples for the same (head, relation) pair. It does not filter known
positives out of the candidate list the way the standard KGE
evaluation protocol does. The MRR/Hits@k this script reports are NOT
directly comparable to train_pykeen.py's filtered numbers on the same
triples -- see that script's docstring, and see the README for the
real side-by-side numbers this produces.

Run:
    python3 train_link_prediction.py
"""
import argparse
import json
import time
from pathlib import Path

import torch
from torch_geometric.nn.kge import TransE

from build_heterodata import load_or_build

HERE = Path(__file__).resolve().parent
RESULTS_PATH = HERE / "data" / "link_prediction_transe_results.json"

SEED = 0


def build_triples(dataset):
    suppliers, products, orders = dataset["suppliers"], dataset["products"], dataset["orders"]
    n_suppliers, n_products = len(suppliers), len(products)
    num_nodes = n_suppliers + n_products  # unified entity id space

    # Single relation type: "supplies" (rel id 0), derived from
    # supplier/product co-occurrence across real orders in the
    # dataset -- the same edge set as (supplier, supplies, product) in
    # build_heterodata.py.
    sp_pairs = sorted(set((o["supplier_idx"], o["product_idx"]) for o in orders))
    heads = torch.tensor([s for s, p in sp_pairs], dtype=torch.long)
    tails = torch.tensor([n_suppliers + p for s, p in sp_pairs], dtype=torch.long)
    rels = torch.zeros(len(sp_pairs), dtype=torch.long)
    return heads, rels, tails, num_nodes, 1


def split_triples(heads, rels, tails, train_frac=0.8, seed=0):
    n = heads.size(0)
    g = torch.Generator().manual_seed(seed)
    perm = torch.randperm(n, generator=g)
    n_train = int(train_frac * n)
    train_idx, test_idx = perm[:n_train], perm[n_train:]
    return (heads[train_idx], rels[train_idx], tails[train_idx]), \
           (heads[test_idx], rels[test_idx], tails[test_idx])


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--epochs", type=int, default=150)
    parser.add_argument("--hidden-channels", type=int, default=32)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    dataset, _ = load_or_build()
    heads, rels, tails, num_nodes, num_relations = build_triples(dataset)
    print(f"Unified entity space: {num_nodes} nodes "
          f"({len(dataset['suppliers'])} suppliers + {len(dataset['products'])} products)")
    print(f"Total (supplier, supplies, product) triples: {heads.size(0)}")

    (tr_h, tr_r, tr_t), (te_h, te_r, te_t) = split_triples(heads, rels, tails, seed=args.seed)
    print(f"Train triples: {tr_h.size(0)}  Test triples: {te_h.size(0)}")

    model = TransE(num_nodes=num_nodes, num_relations=num_relations,
                    hidden_channels=args.hidden_channels, margin=1.0, p_norm=1.0)
    print(model)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loader = model.loader(head_index=tr_h, rel_type=tr_r, tail_index=tr_t,
                           batch_size=args.batch_size, shuffle=True)

    t0 = time.time()
    model.train()
    for epoch in range(1, args.epochs + 1):
        total_loss, n_batches = 0.0, 0
        for h, r, t in loader:
            optimizer.zero_grad()
            loss = model.loss(h, r, t)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            n_batches += 1
        if epoch % 30 == 0 or epoch == 1:
            print(f"  epoch {epoch:3d}  avg_loss={total_loss / n_batches:.4f}")
    train_time = time.time() - t0
    print(f"train_time={train_time:.2f}s")

    model.eval()
    mean_rank, mrr, hits_at_10 = model.test(
        head_index=te_h, rel_type=te_r, tail_index=te_t, batch_size=64, k=10, log=False,
    )
    print(f"\n[torch_geometric.nn.kge.TransE, UNFILTERED] "
          f"test mean_rank={mean_rank:.2f}  MRR={mrr:.4f}  Hits@10={hits_at_10:.4f}  "
          f"(out of {num_nodes} candidate entities)")

    results = dict(
        num_nodes=num_nodes, num_relations=num_relations,
        n_train_triples=int(tr_h.size(0)), n_test_triples=int(te_h.size(0)),
        train_time_s=train_time,
        unfiltered_mean_rank=mean_rank, unfiltered_mrr=mrr, unfiltered_hits_at_10=hits_at_10,
    )
    RESULTS_PATH.parent.mkdir(exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved results to {RESULTS_PATH.relative_to(HERE)}")


if __name__ == "__main__":
    main()
