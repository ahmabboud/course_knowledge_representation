"""Match the TMS customer list to Brunel's customers, and measure the error.

    python er/match_customers.py                 # both thresholds
    python er/match_customers.py --threshold 8

Run from demos/session-05-integration/ (demos/.venv active; the database is
not needed). Reads er/tms-customers.csv and Brunel's OrderList.csv, and only
at the end er/truth.csv, to count the mistakes.

The method, Fellegi and Sunter's (1969), in four steps:
1. Clean both sides the same way (upper case, dash to underscore, spaces off,
   the V put back, a padded number unpadded).
2. Blocking: compare only records with the same home plant, not every pair.
3. For each pair, compare three fields. Each outcome adds a weight:
   log2(m / u), where m is how often the outcome happens for a true match and
   u how often for two different customers. The weights below are stated,
   not learned; Splink estimates them from the data, for the same model at
   scale.
4. Pair each TMS record with its best Brunel candidate. Above the threshold,
   call it a match.
"""

import argparse
import csv
import math
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from common.data_paths import BRUNEL_TABLES  # noqa: E402

# outcome: (m, u) = P(outcome | same customer), P(outcome | different customers)
WEIGHTS = {
    "code exact": (0.60, 0.001), "code close": (0.35, 0.02), "code different": (0.05, 0.979),
    "plant same": (0.95, 0.80), "plant different": (0.05, 0.20),
    "service same": (0.90, 0.40), "service different": (0.10, 0.60),
}
THRESHOLDS = (4, 8)


def clean_code(s):
    s = s.strip().upper().replace("-", "_")
    s = s if s.startswith("V") else "V" + s
    head, _, num = s.partition("_")
    return f"{head}_{int(num)}" if num.isdigit() else s


def clean_plant(s):
    return re.sub(r"[^A-Z0-9]", "", s.upper())


def jaro_winkler(a, b):
    if a == b:
        return 1.0
    reach = max(len(a), len(b)) // 2 - 1
    ma, mb = [False] * len(a), [False] * len(b)
    m = 0
    for i, ca in enumerate(a):
        for j in range(max(0, i - reach), min(len(b), i + reach + 1)):
            if not mb[j] and b[j] == ca:
                ma[i] = mb[j] = True
                m += 1
                break
    if not m:
        return 0.0
    sa = [c for c, f in zip(a, ma) if f]
    sb = [c for c, f in zip(b, mb) if f]
    t = sum(x != y for x, y in zip(sa, sb)) / 2
    jaro = (m / len(a) + m / len(b) + (m - t) / m) / 3
    prefix = next((k for k in range(min(4, len(a), len(b))) if a[k] != b[k]), min(4, len(a), len(b)))
    return jaro + prefix * 0.1 * (1 - jaro)


def score(t, b):
    code = "code exact" if t["code"] == b["code"] else (
        "code close" if jaro_winkler(t["code"], b["code"]) >= 0.93 else "code different")
    outcomes = [code, "plant same" if t["plant"] == b["plant"] else "plant different"]
    if t["service"]:
        outcomes.append("service same" if t["service"] == b["service"] else "service different")
    return sum(math.log2(WEIGHTS[o][0] / WEIGHTS[o][1]) for o in outcomes), outcomes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--threshold", type=float, action="append")
    thresholds = ap.parse_args().threshold or THRESHOLDS
    o = pd.read_csv(BRUNEL_TABLES["order_list"])
    brunel = [{"code": c, "plant": clean_plant(p), "service": s} for c, p, s in zip(
        o.groupby("Customer")["Plant Code"].agg(lambda x: x.value_counts().index[0]).index,
        o.groupby("Customer")["Plant Code"].agg(lambda x: x.value_counts().index[0]),
        o.groupby("Customer")["Service Level"].agg(lambda x: x.value_counts().index[0]))]
    tms = [{"id": r["tms_id"], "raw": r["customer_code"], "code": clean_code(r["customer_code"]),
            "plant": clean_plant(r["home_plant"]), "service": r["main_service"]}
           for r in csv.DictReader(open(HERE / "tms-customers.csv"))]
    pairs = [(t, b) for t in tms for b in brunel if t["plant"] == b["plant"]]
    print(f"{len(tms)} TMS records, {len(brunel)} Brunel customers: {len(tms) * len(brunel):,} possible pairs, "
          f"{len(pairs):,} after blocking on home plant")
    best = {}
    for t, b in pairs:
        s, why = score(t, b)
        if t["id"] not in best or s > best[t["id"]][0]:
            best[t["id"]] = (s, b["code"], why)
    truth = {r["tms_id"]: r["brunel_customer"] for r in csv.DictReader(open(HERE / "truth.csv"))}
    raw = {t["id"]: t["raw"].strip() for t in tms}
    for th in thresholds:
        found = {tid: code for tid, (s, code, _) in best.items() if s >= th}
        tp = sum(1 for tid, code in found.items() if truth[tid] == code)
        fp = [tid for tid, code in found.items() if truth[tid] != code]
        fn = [tid for tid, code in truth.items() if code and found.get(tid) != code]
        p, r = tp / max(len(found), 1), tp / sum(1 for c in truth.values() if c)
        print(f"\nthreshold {th:g}: {len(found)} matches, {tp} right. precision {p:.3f}, recall {r:.3f}")
        for tid in fp:
            print(f"  wrong match  {tid} {raw[tid]!r:<28} -> {found[tid]}  (truth: {truth[tid] or 'not in Brunel'})")
        for tid in fn:
            s, code, why = best.get(tid, (None, None, []))
            print(f"  missed       {tid} {raw[tid]!r:<28}    (truth: {truth[tid]}; best score {s:.1f}: {', '.join(why)})")


if __name__ == "__main__":
    main()
