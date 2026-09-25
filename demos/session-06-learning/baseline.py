"""The baseline: a plain logistic regression on the flattened order row, the
model any graph model must beat. Three runs, one line each:

  1. lateDays kept as a feature      (the leak: the answer is in the input)
  2. a random split of the orders
  3. a split by customer             (test customers never seen in training)

    python baseline.py

Run from demos/session-06-learning/ after build_graph.py. About 5 seconds.

The flattened row is what a table gives: the order's weight, quantity and
service level, and which customer, carrier and plant it has (one column per
possible value, "one-hot"). Scores: PR-AUC (1.0 is perfect, and a model that
guesses scores the share of late orders, 0.021 here), ROC-AUC (0.5 is
guessing) and precision at 100 (of the 100 orders ranked most at risk, the
share that were late). Accuracy is printed too, to show why it is useless
when only 2% of orders are late.
"""

from pathlib import Path

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, average_precision_score, roc_auc_score
from sklearn.preprocessing import OneHotEncoder

from learning_utils import precision_at_k, split_by_customer, split_random

HERE = Path(__file__).resolve().parent
SEEDS = range(5)


def load():
    b = torch.load(HERE / "data" / "brunel-graph.pt", weights_only=False)
    ids = np.column_stack([b["customer"], b["carrier"], b["plant"]])
    return b["data"]["order"].x.numpy(), ids, b["late_days"].numpy(), b["y"].numpy(), b["customer"].numpy()


def fit_score(x, ids, y, train, test, extra=None):
    onehot = OneHotEncoder(handle_unknown="ignore").fit(ids[train])
    def rows(i):
        parts = [onehot.transform(ids[i]).toarray(), x[i]]
        return np.hstack(parts + ([extra[i, None]] if extra is not None else []))
    model = LogisticRegression(max_iter=2000, class_weight="balanced").fit(rows(train), y[train])
    p = model.predict_proba(rows(test))[:, 1]
    yt = y[test]
    return {"late in test": int(yt.sum()), "PR-AUC": average_precision_score(yt, p) if yt.sum() else float("nan"),
            "ROC-AUC": roc_auc_score(yt, p) if 0 < yt.sum() < len(yt) else float("nan"),
            "precision@100": precision_at_k(yt, p, 100), "accuracy": accuracy_score(yt, p > 0.5)}


def line(name, r):
    if r["late in test"] == 0:
        return f"{name:<34} late in test   0  no late order in the test set: nothing to measure"
    return (f"{name:<34} late in test {r['late in test']:>3}  PR-AUC {r['PR-AUC']:.3f}  ROC-AUC {r['ROC-AUC']:.3f}  "
            f"precision@100 {r['precision@100']:.2f}  accuracy {r['accuracy']:.3f}")


def main():
    x, ids, late_days, y, customer = load()
    print(f"{len(y):,} orders, {int(y.sum())} late ({y.mean():.1%}). Guessing scores PR-AUC {y.mean():.3f}; "
          f"\"never late\" scores accuracy {1 - y.mean():.3f}.\n")
    train, test = split_random(len(y), y)
    print(line("1 · random split, lateDays kept", fit_score(x, ids, y, train, test, extra=late_days)))
    print(line("2 · random split", fit_score(x, ids, y, train, test)))
    for s in SEEDS:
        train, test = split_by_customer(customer, seed=s)
        print(line(f"3 · split by customer, seed {s}", fit_score(x, ids, y, train, test)))
    late_customers = np.unique(customer[y == 1])
    print(f"\nOnly {len(late_customers)} of {len(np.unique(customer))} customers ever have a late order. "
          "A split by customer puts 0, 1 or 2 of them in the test set.")


if __name__ == "__main__":
    main()
