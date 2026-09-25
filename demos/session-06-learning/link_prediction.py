"""Link prediction: which plant makes this product? A knowledge graph
embedding (TransE, with PyKEEN) against the simplest possible baseline,
"guess the plant that makes the most products".

    python link_prediction.py

Run from demos/session-06-learning/ after build_graph.py. Under a minute.

The question: hide 10% of the "plant makes product" links, learn from the
rest, and for each hidden link rank the plants from most to least likely.
Scores are "filtered": other plants already known to make that product do
not count against the model. TransE learns from five kinds of link: makes,
and four more from the orders (which customer orders the product, which
carrier ships it, which port it leaves from, which port a plant serves).
The pairs "this plant shipped this product" are left out on purpose: every
one of them is also a "makes" link, so they would give the answer away.
"""

import collections
from pathlib import Path

import numpy as np
import torch
from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory

from learning_utils import mrr

HERE = Path(__file__).resolve().parent
SEEDS = range(3)


def triples(b):
    names, d = b["names"], b["data"]
    name = lambda kind, i: names[kind][i].rsplit("/", 1)[-1]
    makes = [(name("plant", p), "makes", name("product", q)) for p, q in d["plant", "makes", "product"].edge_index.T.tolist()]
    other = set()
    oi = lambda rel: d["order", rel, {"orderedBy": "customer", "carriedBy": "carrier", "shipsFrom": "port", "ofProduct": "product"}[rel]].edge_index[1].tolist()
    prod, cust, car, port = oi("ofProduct"), oi("orderedBy"), oi("carriedBy"), oi("shipsFrom")
    for q, c, k, p in zip(prod, cust, car, port):
        other.add((name("customer", c), "orders", name("product", q)))
        other.add((name("product", q), "shippedBy", name("carrier", k)))
        other.add((name("product", q), "leavesFrom", name("port", p)))
    other |= {(name("plant", p), "servesPort", name("port", q)) for p, q in d["plant", "servesPort", "port"].edge_index.T.tolist()}
    return makes, sorted(other)


def ranks_among_plants(score, test, known, plants):
    """Rank the true plant among all plants, filtered; returns one rank per test link."""
    out = []
    for h, _, t in test:
        cand = [p for p in plants if p == h or p not in known[t]]
        order = sorted(cand, key=lambda p: -score(p, t))
        out.append(order.index(h) + 1)
    return out


def main():
    b = torch.load(HERE / "data" / "brunel-graph.pt", weights_only=False)
    makes, other = triples(b)
    plants = sorted({h for h, _, _ in makes})
    known = collections.defaultdict(set)
    for h, _, t in makes:
        known[t].add(h)
    print(f"{len(makes):,} makes links ({len(plants)} plants), {len(other):,} other links")
    for seed in SEEDS:
        rng = np.random.RandomState(seed)
        perm = rng.permutation(len(makes))
        n = len(makes) // 10
        test, valid, train = [makes[i] for i in perm[:n]], [makes[i] for i in perm[n:2 * n]], [makes[i] for i in perm[2 * n:]]
        tf = TriplesFactory.from_labeled_triples(np.array(train + other))
        seen = lambda L: [x for x in L if x[0] in tf.entity_to_id and x[2] in tf.entity_to_id]
        cold = len(test) - len(seen(test))
        test, valid = seen(test), seen(valid)
        mk = lambda L: TriplesFactory.from_labeled_triples(np.array(L), entity_to_id=tf.entity_to_id, relation_to_id=tf.relation_to_id)
        result = pipeline(training=tf, validation=mk(valid), testing=mk(test), model="TransE",
                          model_kwargs=dict(embedding_dim=32), training_kwargs=dict(num_epochs=150, batch_size=512),
                          random_seed=seed, device="cpu", use_tqdm=False)
        model, ent, rel = result.model, tf.entity_to_id, tf.relation_to_id["makes"]
        with torch.no_grad():
            cache = {}
            def transe(p, t):
                if t not in cache:
                    cache[t] = model.score_h(torch.tensor([[rel, ent[t]]]))[0]
                return float(cache[t][ent[p]]) if p in ent else float("-inf")  # a plant never seen in training ranks last
            r_model = ranks_among_plants(transe, test, known, plants)
        popular = collections.Counter(h for h, _, _ in train)
        r_pop = ranks_among_plants(lambda p, t: popular.get(p, 0), test, known, plants)
        hits1 = lambda r: float(np.mean(np.asarray(r) == 1))
        print(f"seed {seed}: {len(test)} hidden links scored ({cold} left out: their product appears in no other link)")
        print(f"  TransE      MRR {mrr(r_model):.3f}  Hits@1 {hits1(r_model):.3f}")
        print(f"  popularity  MRR {mrr(r_pop):.3f}  Hits@1 {hits1(r_pop):.3f}")


if __name__ == "__main__":
    main()
