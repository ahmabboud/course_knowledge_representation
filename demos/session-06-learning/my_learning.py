"""Session 6 lab, part B: write three small functions.

Each one is the twin of a function in learning_utils.py, with one thing
changed. Open learning_utils.py next to this file, copy the twin, change it.

  Y1  split_by_plant   twin of split_by_customer: group the orders by plant
  Y2  recall_at_k      twin of precision_at_k: divide by all late orders
  Y3  hits_at_k        twin of mrr: count a rank as a hit if it is at most k

Then run, from demos/session-06-learning/:
    python check_my_learning.py
The checker tests each function on small, known cases and says right or not
yet, with a hint. Only open solutions/my_learning_solutions.py after trying.
"""

import numpy as np


def split_by_plant(plant, test_share=0.3, seed=0):
    """Y1. Put about 30% of the PLANTS in the test set, with all their orders.
    No plant may have orders on both sides. Returns (train, test), arrays of
    order positions."""
    # TODO: copy split_by_customer from learning_utils.py and change what it groups by
    raise NotImplementedError


def recall_at_k(y_true, scores, k=100):
    """Y2. Of ALL the late orders, the share found among the k orders the model
    ranks most at risk."""
    # TODO: copy precision_at_k from learning_utils.py and change what it divides by
    raise NotImplementedError


def hits_at_k(ranks, k=10):
    """Y3. The share of right answers ranked at position k or better (1 is best)."""
    # TODO: copy mrr from learning_utils.py and change what it averages
    raise NotImplementedError
