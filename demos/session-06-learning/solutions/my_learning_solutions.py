"""Solutions to part B (my_learning.py). Each is its twin in learning_utils.py
with one thing changed. Other correct code passes the checker too."""

import numpy as np


def split_by_plant(plant, test_share=0.3, seed=0):
    """Y1 · split_by_customer with plant in place of customer."""
    rng = np.random.RandomState(seed)
    groups = np.unique(plant)
    rng.shuffle(groups)
    test_groups = groups[: int(round(test_share * len(groups)))]
    test = np.flatnonzero(np.isin(plant, test_groups))
    train = np.flatnonzero(~np.isin(plant, test_groups))
    return train, test


def recall_at_k(y_true, scores, k=100):
    """Y2 · precision_at_k, divided by all late orders instead of by k."""
    y_true = np.asarray(y_true)
    top = np.argsort(-np.asarray(scores), kind="stable")[:k]
    return float(y_true[top].sum() / y_true.sum())


def hits_at_k(ranks, k=10):
    """Y3 · mrr, averaging "rank at most k" instead of 1/rank."""
    return float(np.mean(np.asarray(ranks) <= k))
