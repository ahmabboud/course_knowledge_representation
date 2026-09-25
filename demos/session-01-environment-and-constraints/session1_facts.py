"""Every number the Session 1 slides quote, recomputed from the real data.

Run from this folder after `python ../data/fetch_data.py`:

    python session1_facts.py > reference-outputs/s1-facts.txt

The deck (lectures/kr-session-01.html) may only quote what this prints.
"""
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
DATA = Path(__file__).resolve().parents[1] / "data"


def fingerprint(s):
    """OpenRefine 3.8 key collision fingerprint: punctuation removed, lower case, accents off, sorted unique tokens."""
    s = re.sub(r"[^\w\s]", "", str(s).strip().lower())
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return " ".join(sorted(set(s.split())))


print("== DataCo ==")
d = pd.read_csv(DATA / "dataco" / "DataCoSupplyChainDataset.csv", encoding="latin-1")
print("rows (order lines)", len(d), "columns", d.shape[1])
print("orders", d["Order Id"].nunique(), "customers", d["Customer Id"].nunique(), "products", d["Product Card Id"].nunique())
od = pd.to_datetime(d["order date (DateOrders)"], format="%m/%d/%Y %H:%M")
sd = pd.to_datetime(d["shipping date (DateOrders)"], format="%m/%d/%Y %H:%M")
print("order dates", od.min(), "to", od.max())
print("shipped before ordered", int((sd < od).sum()))
real, sched = d["Days for shipping (real)"], d["Days for shipment (scheduled)"]
print("Delivery Status", d["Delivery Status"].value_counts().to_dict())
print("late by status", int((d["Delivery Status"] == "Late delivery").sum()),
      "late by days (real > scheduled)", int((real > sched).sum()))
print(pd.crosstab(d["Delivery Status"], real > sched).to_string())
nulls = d.isna().sum()
print("null counts", nulls[nulls > 0].to_dict())
print("constant columns", [c for c in d.columns if d[c].nunique(dropna=False) == 1])
print("Customer Country", d["Customer Country"].value_counts().to_dict())
print("Order Country (top 5)", d["Order Country"].value_counts().head(5).to_dict(), "distinct", d["Order Country"].nunique())
print("Shipping Mode", d["Shipping Mode"].value_counts().to_dict())
u = pd.Series(d["Order City"].dropna().unique())
groups = u.groupby(u.map(fingerprint)).agg(list)
for names in groups[groups.map(len) > 1]:
    for n in names:
        s = d[d["Order City"] == n]
        print("cluster", repr(n), len(s), s["Order Country"].value_counts().to_dict(), s["Order State"].value_counts().to_dict())
cols = ["Order Id", "order date (DateOrders)", "Order City", "Order Country", "Product Name",
        "Shipping Mode", "Days for shipping (real)", "Days for shipment (scheduled)", "Delivery Status"]
print(d[cols].head(5).to_string())

print("\n== Brunel ==")
b = DATA / "brunel"
names = ["OrderList", "FreightRates", "WhCosts", "WhCapacities", "ProductsPerPlant", "VmiCustomers", "PlantPorts"]
T = {n: pd.read_csv(b / f"{n}.csv") for n in names}
for n, t in T.items():
    print(n, t.shape, list(t.columns))
    print("  first row", t.iloc[0].to_dict())
o, pp, ppl, fr = T["OrderList"], T["PlantPorts"], T["ProductsPerPlant"], T["FreightRates"]
print("order dates", o["Order Date"].unique().tolist())
print("Order ID dtype", o["Order ID"].dtype, "first", o["Order ID"].iloc[0], "all whole numbers", bool((o["Order ID"] % 1 == 0).all()))
plants, ports = pp["Plant Code"].nunique(), pp["Port"].nunique()
print("plants", plants, "ports", ports, "linked pairs", len(pp), "possible pairs", plants * ports)
pairs = set(map(tuple, pp[["Plant Code", "Port"]].values))
print("orders leaving through an unlinked port", sum((a, p) not in pairs for a, p in o[["Plant Code", "Origin Port"]].values))
prod = set(map(tuple, ppl[["Plant Code", "Product ID"]].values))
print("orders for a product the plant does not make", sum((a, p) not in prod for a, p in o[["Plant Code", "Product ID"]].values))
print(pd.crosstab(o["Carrier"], o["Service Level"]).to_string())
print("carriers in FreightRates", sorted(fr["Carrier"].unique()))
k = ["Carrier", "orig_port_cd", "dest_port_cd", "svc_cd"]
m = o.merge(fr, left_on=["Carrier", "Origin Port", "Destination Port", "Service Level"], right_on=k, how="left", indicator=True)
print("orders with no rate lane at all", m.loc[m["_merge"] == "left_only", "Order ID"].nunique())
mm = m[m["_merge"] == "both"]
inband = mm[(mm["Weight"] >= mm["minm_wgh_qty"]) & (mm["Weight"] <= mm["max_wgh_qty"])]["Order ID"].unique()
lane_orders = mm["Order ID"].unique()
print("orders with a lane", len(lane_orders), "weight inside a band", len(inband), "weight in a gap between bands", len(lane_orders) - len(inband))
band = fr[(fr["Carrier"] == "V444_1") & (fr["orig_port_cd"] == "PORT04") & (fr["svc_cd"] == "DTD")]
print("V444_1 PORT04 DTD bands", sorted(set(zip(band["minm_wgh_qty"], band["max_wgh_qty"]))))
print("mode_dsc raw values", fr["mode_dsc"].unique().tolist())
print("WhCapacities header", list(T["WhCapacities"].columns))

print("\n== Grain and links ==")
lines = d.groupby("Order Id").size()
print("order lines per order", lines.value_counts().sort_index().to_dict())
print(d[d["Order Id"] == 2][["Order Id", "Order Item Id", "order date (DateOrders)", "Product Name", "Order Item Quantity", "Order City"]].to_string())
print("plant to port links", pp.groupby("Plant Code")["Port"].apply(list).to_dict())
print("orders per plant and origin port", o.groupby(["Plant Code", "Origin Port"]).size().to_dict())
g = o[(o["Carrier"] == "V444_1") & (o["Origin Port"] == "PORT04") & (o["Service Level"] == "DTD")]
print("V444_1 PORT04 DTD orders", len(g), "with weight between 2.5 and 70.51", int(((g["Weight"] > 2.5) & (g["Weight"] < 70.51)).sum()))
print("example weight in the gap", g[(g["Weight"] > 2.5) & (g["Weight"] < 70.51)]["Weight"].head(3).tolist())
gap_ids = set(lane_orders) - set(inband)
gap = o[o["Order ID"].isin(gap_ids)]
lanes = gap.groupby(["Carrier", "Origin Port", "Service Level"]).size().to_dict()
sliver = gap[~((gap["Weight"] > 2.5) & (gap["Weight"] < 70.51))]
print("gap orders by lane", lanes, "outside the 2.5 to 70.51 hole", len(sliver), "their weights", sorted(sliver["Weight"].round(4).tolist()))
print("Ship Late Day count zeros", int((o["Ship Late Day count"] == 0).sum()), "Ship ahead day count zeros", int((o["Ship ahead day count"] == 0).sum()))
