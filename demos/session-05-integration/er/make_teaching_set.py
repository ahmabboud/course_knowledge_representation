"""Build the entity resolution teaching set: a second system's customer list.

    python er/make_teaching_set.py

Writes er/tms-customers.csv and er/truth.csv. Run from
demos/session-05-integration/. You never need to run it: both files are
committed. It is here so you can see exactly how they were made.

TEACHING DATA. Brunel is the only source that has these customers, so there
is no real second system to match against. This script pretends there is
one, a transport management system (TMS), that exported Brunel's own 46
real customers, the way systems really drift: lower case, a dash for the
underscore, stray spaces, a padded number, a missing letter, a lost 5, two
digits swapped. It adds 6 customers that are not in Brunel: the 2 real VMI
customers that never order (VmiCustomers.csv) and 4 invented look-alikes.
The home plant and main service level of each real customer come from
OrderList.csv. Because the file is built this way, the truth is known:
er/truth.csv says which TMS record is which Brunel customer.
"""

import csv
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from common.data_paths import BRUNEL_TABLES  # noqa: E402


def drift(code, rule):
    head, num = code.split("_")
    return {
        "same": code,
        "lower": code.lower(),
        "dash": f"{head}-{num}",
        "spaces": f"  {code} ",
        "padded": f"{head}_{int(num):03d}",
        "no-v": code[1:],
        "lost-5": f"{head[:-1]}_{num}" if len(head) > 2 else code,
        "swapped": f"{head}_{num[::-1]}" if len(num) == 2 and num[0] != num[1] else code,
    }[rule]


def plant_as(plant, i):
    return [plant, plant.lower(), "Plant " + plant[5:], plant][i % 4]


RULES = ["same", "lower", "dash", "spaces", "padded", "same", "no-v", "lost-5", "lower", "swapped"]
LOOKALIKES = [  # suffix numbers no Brunel customer has: 18, 21, 43, 48
    ("V555555555555555555_18", "PLANT03", "DTP"),
    ("V55555_21", "PLANT03", "DTD"),
    ("V555555555_43", "PLANT03", "DTP"),
    ("V5555555555_48", "PLANT12", "DTD"),
]


def main():
    o = pd.read_csv(BRUNEL_TABLES["order_list"])
    home = o.groupby("Customer")["Plant Code"].agg(lambda s: s.value_counts().index[0])
    level = o.groupby("Customer")["Service Level"].agg(lambda s: s.value_counts().index[0])
    customers = sorted(home.index)
    rows, truth = [], []
    for i, c in enumerate(customers):
        tid = f"TMS-{i + 1:03d}"
        rows.append((tid, drift(c, RULES[i % len(RULES)]), plant_as(home[c], i), level[c]))
        truth.append((tid, c, RULES[i % len(RULES)]))
    vmi = pd.read_csv(BRUNEL_TABLES["vmi_customers"])
    never = sorted(set(vmi["Customers"]) - set(customers))
    vplant = vmi.drop_duplicates("Customers").set_index("Customers")["Plant Code"]
    extra = [(c, vplant[c], "") for c in never] + LOOKALIKES
    for j, (c, p, lv) in enumerate(extra):
        tid = f"TMS-{len(customers) + j + 1:03d}"
        rows.append((tid, c, p, lv))
        truth.append((tid, "", "not in Brunel: VMI customer who never orders" if j < len(never) else "not in Brunel: invented look-alike"))
    with open(HERE / "tms-customers.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tms_id", "customer_code", "home_plant", "main_service"])
        w.writerows(rows)
    with open(HERE / "truth.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tms_id", "brunel_customer", "how_it_was_made"])
        w.writerows(truth)
    print(f"tms-customers.csv: {len(rows)} records ({len(customers)} Brunel customers, {len(extra)} not in Brunel); truth.csv")


if __name__ == "__main__":
    main()
