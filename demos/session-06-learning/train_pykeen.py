"""Session 6 lab, step 4 -- filtered ranking metrics (MRR, Hits@k) with
PyKEEN, on the identical supplier/product link-prediction task and the
same 80/20 split protocol as train_link_prediction.py (same random
seed, same proportions), so the unfiltered `torch_geometric.nn.kge`
numbers and PyKEEN's filtered numbers are a real, honest side-by-side
comparison of the SAME triples, not two different datasets that happen
to look similar.

Exact PyKEEN API used (verified against the installed 1.11.1 source):
  pykeen.triples.TriplesFactory.from_labeled_triples(triples: np.ndarray, ...)
  pykeen.pipeline.pipeline(training=..., testing=..., model='TransE',
                            model_kwargs=..., training_kwargs=...,
                            random_seed=..., evaluator_kwargs=..., ...)
  pykeen.evaluation.RankBasedEvaluator(filtered: bool = True, ...)

Trivial real gotcha: `pykeen.__version__` raises `AttributeError`, the
package does not expose a top-level version string. Use `pip show
pykeen` or `importlib.metadata.version('pykeen')` instead.

Run:
    python3 train_pykeen.py
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch
from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory

from build_heterodata import load_or_build

HERE = Path(__file__).resolve().parent
RESULTS_PATH = HERE / "data" / "link_prediction_pykeen_results.json"

SEED = 0


def build_labeled_triples(dataset):
    suppliers, products, orders = dataset["suppliers"], dataset["products"], dataset["orders"]
    sp_pairs = sorted(set((o["supplier_idx"], o["product_idx"]) for o in orders))
    return np.array([
        [f"supplier:{suppliers[s][0]}", "supplies", f"product:{products[p][0]}"]
        for s, p in sp_pairs
    ], dtype=str)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--epochs", type=int, default=150)
    parser.add_argument("--embedding-dim", type=int, default=32)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    dataset, _ = load_or_build()
    triples = build_labeled_triples(dataset)
    print(f"Total labeled triples: {len(triples)}")

    tf = TriplesFactory.from_labeled_triples(triples)
    print(f"PyKEEN TriplesFactory: {tf.num_entities} entities, {tf.num_relations} relations, "
          f"{tf.num_triples} triples")

    # PyKEEN's own splitter (numpy/torch RNG state, not byte-identical
    # to the manual split in train_link_prediction.py, but same
    # protocol -- 80/20, same seed -- on the same underlying triples).
    training, testing = tf.split([0.8, 0.2], random_state=args.seed)
    print(f"Train triples: {training.num_triples}  Test triples: {testing.num_triples}")

    result = pipeline(
        training=training,
        testing=testing,
        model="TransE",
        model_kwargs=dict(embedding_dim=args.embedding_dim),
        optimizer="Adam",
        optimizer_kwargs=dict(lr=0.01),
        training_kwargs=dict(num_epochs=args.epochs, batch_size=args.batch_size, use_tqdm=False),
        negative_sampler="basic",
        negative_sampler_kwargs=dict(num_negs_per_pos=1),
        random_seed=args.seed,
        evaluator_kwargs=dict(filtered=True),
    )

    both_realistic = result.metric_results.to_dict()["both"]["realistic"]
    mrr = both_realistic["inverse_harmonic_mean_rank"]
    mean_rank = both_realistic["arithmetic_mean_rank"]
    hits_at_1 = both_realistic["hits_at_1"]
    hits_at_3 = both_realistic["hits_at_3"]
    hits_at_10 = both_realistic["hits_at_10"]

    print(f"\n[PyKEEN TransE, FILTERED, both-directions 'realistic'] "
          f"MRR={mrr:.4f}  MR={mean_rank:.2f}  "
          f"Hits@1={hits_at_1:.4f}  Hits@3={hits_at_3:.4f}  Hits@10={hits_at_10:.4f}")

    out = dict(
        num_entities=tf.num_entities, num_relations=tf.num_relations,
        n_train_triples=training.num_triples, n_test_triples=testing.num_triples,
        filtered_mrr=mrr, filtered_mean_rank=mean_rank,
        filtered_hits_at_1=hits_at_1, filtered_hits_at_3=hits_at_3, filtered_hits_at_10=hits_at_10,
    )
    RESULTS_PATH.parent.mkdir(exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved results to {RESULTS_PATH.relative_to(HERE)}")


if __name__ == "__main__":
    main()
