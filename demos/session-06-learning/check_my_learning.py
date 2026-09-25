"""Check your part B functions (my_learning.py): right, or not yet with a hint.

    python check_my_learning.py                                  # your file
    python check_my_learning.py solutions/my_learning_solutions.py

Each function is tested on small cases with known answers, and Y1 also on
the real plant of every Brunel order (data/brunel-graph.pt, if built).
Any correct code passes; how it is written does not matter.
"""

import importlib.util
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def load(path):
    spec = importlib.util.spec_from_file_location("student", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_y1(f):
    plant = np.array([0, 0, 1, 1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 9, 9])
    real = HERE / "data" / "brunel-graph.pt"
    if real.exists():
        import torch
        plant = torch.load(real, weights_only=False)["plant"].numpy()
    train, test = f(plant, 0.3, 0)
    train, test = np.asarray(train), np.asarray(test)
    if len(np.intersect1d(train, test)) or len(train) + len(test) != len(plant):
        return "every order must be in exactly one of train and test."
    both = np.intersect1d(np.unique(plant[train]), np.unique(plant[test]))
    if len(both):
        return f"{len(both)} plants have orders on both sides. Group by plant, as split_by_customer groups by customer."
    n_test = len(np.unique(plant[test]))
    want = int(round(0.3 * len(np.unique(plant))))
    if n_test != want:
        return f"{n_test} plants in the test set; about 30% of {len(np.unique(plant))} plants is {want}."
    return None


def check_y2(f):
    y = np.array([1, 0, 1, 0, 0, 1, 0, 0, 0, 1])
    s = np.array([.9, .8, .7, .6, .5, .4, .3, .2, .1, .05])
    got = f(y, s, 3)
    if abs(got - 2 / 3) < 1e-9:
        return "that is precision (2 of the top 3 are late). Recall divides by ALL late orders: 2 of 4."
    if abs(got - 0.5) > 1e-9:
        return f"expected 0.5 (the top 3 hold 2 of the 4 late orders), got {got}."
    if abs(f(y, s, 10) - 1.0) > 1e-9:
        return "with k covering every order, recall must be 1.0."
    return None


def check_y3(f):
    ranks = [1, 2, 3, 10, 11, 50]
    got = f(ranks, 10)
    if abs(got - 3 / 6) < 1e-9:
        return "rank 10 is a hit at k = 10: use <= k, not < k."
    if abs(got - 4 / 6) > 1e-9:
        return f"expected 4 of 6 = 0.667 (ranks 1, 2, 3 and 10), got {got}."
    if abs(f(ranks, 1) - 1 / 6) > 1e-9:
        return "at k = 1 only rank 1 counts: expected 1 of 6."
    return None


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "my_learning.py"
    try:
        mod = load(path)
    except Exception as e:
        sys.exit(f"{path.name} does not run yet: {e}")
    right = 0
    for y, name, check in (("Y1", "split_by_plant", check_y1), ("Y2", "recall_at_k", check_y2), ("Y3", "hits_at_k", check_y3)):
        try:
            problem = check(getattr(mod, name))
        except NotImplementedError:
            problem = "not written yet (the TODO is still there)."
        except Exception as e:
            problem = f"the function stops with {type(e).__name__}: {e}"
        if problem is None:
            right += 1
            print(f"{y}  right.")
        else:
            print(f"{y}  not yet: {problem}")
    print(f"\n{right} of 3 right.")


if __name__ == "__main__":
    main()
