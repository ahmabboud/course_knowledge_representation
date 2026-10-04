"""Session 1 lab: six rule checks, each printed with its count.

Run from this folder after `python ../data/fetch_data.py`:

    python rule_checks.py

Nothing to edit. Read each block: the question, the count, and what it means.
Then copy the numbers into constraint_inventory_template.csv.
"""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
orders = pd.read_csv(DATA / "brunel" / "OrderList.csv")
ports = pd.read_csv(DATA / "brunel" / "PlantPorts.csv")
makes = pd.read_csv(DATA / "brunel" / "ProductsPerPlant.csv")
rates = pd.read_csv(DATA / "brunel" / "FreightRates.csv")
dataco = pd.read_csv(DATA / "dataco" / "DataCoSupplyChainDataset.csv", encoding="latin-1")


def show(n, question, result, meaning):
    print(f"\nCheck {n}: {question}\n  Result : {result}\n  Meaning: {meaning}")


# 1. Plant and port
linked = set(zip(ports["Plant Code"], ports["Port"]))
bad = sum((p, q) not in linked for p, q in zip(orders["Plant Code"], orders["Origin Port"]))
show(1, "Does every Brunel order leave through a port its plant is linked to?",
     f"{bad} of {len(orders)} orders break it",
     "No exceptions: this is a rule the data always obeys, and no column states it.")

# 2. Plant and product
made = set(zip(makes["Plant Code"], makes["Product ID"]))
bad = sum((p, q) not in made for p, q in zip(orders["Plant Code"], orders["Product ID"]))
show(2, "Does every order ask a plant for a product that plant makes?",
     f"{bad} of {len(orders)} orders break it",
     "Again no exceptions: a second rule that lives across two tables.")

# 3. Carrier and service level
table = pd.crosstab(orders["Carrier"], orders["Service Level"])
print("\nCheck 3: Which carrier uses which service level?")
print(table.to_string())
print("  Meaning: each carrier sticks to one level, except V444_0 which uses two.")

# 4. Orders with a rate
lanes = set(zip(rates["Carrier"], rates["orig_port_cd"], rates["dest_port_cd"], rates["svc_cd"]))
none = sum(k not in lanes for k in zip(orders["Carrier"], orders["Origin Port"],
                                       orders["Destination Port"], orders["Service Level"]))
show(4, "How many orders have no matching lane in the freight rate table?",
     f"{none} of {len(orders)} orders",
     "These orders can never be priced from the rate table. The rule 'every order has a rate' fails.")

# 5. Delivery status and days
late = dataco["Days for shipping (real)"] > dataco["Days for shipment (scheduled)"]
tab = pd.crosstab(dataco["Delivery Status"], late)
tab.columns = ["not later than scheduled", "later than scheduled"]
print("\nCheck 5: Does DataCo's Delivery Status agree with real days against scheduled days?")
print(tab.to_string())
print("  Meaning: three statuses agree exactly. 'Shipping canceled' does not, so the label is not days-based.")

# 6. Order City against country
cities = dataco[dataco["Order City"].isin(["Los Angeles", "Los Ángeles", "Macon", "Mâcon"])]
show(6, "Do near-identical city names belong to the same country?",
     "\n" + cities.groupby(["Order City", "Order Country"]).size().to_string(),
     "Different countries: these are different cities, not typos. Merging them would be wrong.")
