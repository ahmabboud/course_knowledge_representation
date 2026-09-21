"""Session 6 lab, step 1 -- the provided conversion utility: build a
synthetic supply-chain graph and turn it into a PyTorch Geometric
`HeteroData` object.

Node types: supplier, product, plant, port, carrier, order.
Edge types (order-centric edges are directed order -> {supplier,
product, carrier, port, plant}; downstream scripts that need message
passing INTO the order type add reverse edges with
`torch_geometric.transforms.ToUndirected()`, see
train_node_classification.py's own note on why):

  (order,    ordered_from,    supplier)
  (order,    contains,        product)
  (order,    shipped_via,     carrier)
  (order,    departs_from,    port)
  (order,    destined_to,     plant)
  (supplier, ships_from,      port)
  (plant,    served_by,       port)
  (carrier,  operates_at,     port)
  (supplier, supplies,        product)

Real DataCo/Brunel operational data is not reachable from this
repository's own tooling (Kaggle needs a personal token, Brunel's
direct Figshare download has been unreliable, see
session-05-integration/README.md's own note on the same problem) and
neither dataset has anything resembling a knowledge graph shape
anyway. So this is a documented, honestly-labeled SYNTHETIC generator,
not real operational data -- but it reuses the course's real running
case study rather than inventing a new one: ontology namespace
`https://ul.edu.lb/kr/scm#` (`common/iri.py`), purchase orders
po88/po99/po101/po104 (po99's dispatch/delivery dates are still
backwards, same broken row as Sessions 4 and 5), carriers dhl/aramex,
and the six suppliers from Session 5's entity-resolution exercise
(Acme Logistics, Brunel Freight Group, Mediterranean Shipping Co,
Northline Carriers, Cedars Cargo, Atlas Overland). Everything else
(products, plants, ports, the extra suppliers and carrier, the 360
orders) is invented to give the graph enough scale to train on and to
make the temporal-leakage demo in leakage_demo.py reproduce a real,
visible gap.

Design note on the temporal-leakage story (see leakage_demo.py):
  - Port of Hamburg gets a genuine injected regime change starting
    2026-01-01: before that date, orders routed through Hamburg have
    a normal on-time rate; from that date on, transit times blow out
    and the late rate jumps sharply.
  - Carrier SLA promises do NOT adapt to the congestion (contracts
    don't renegotiate themselves), so "late" becomes much more common
    for Hamburg-routed orders after the cutoff.
  - No node feature encodes "is this the congested regime" directly;
    the only way a model can find out is to have been trained on
    orders from that period. That is what makes the random-vs-temporal
    split comparison in leakage_demo.py honest.

Run:
    python3 build_heterodata.py

prints the graph structure and the real regime-change statistics, and
writes data/dataset.pkl (raw tables, gitignored, regenerate not
commit) and data/full_graph.pt (the HeteroData object) so the other
scripts in this folder can load them instead of rebuilding from
scratch. Every other script here imports `build_dataset()` and
`build_graph()` directly and calls `load_or_build()` (below) to reuse
a cached graph when one is on disk, since the generator is fully
deterministic (module-level seed=42) -- loading and rebuilding produce
byte-identical results, loading is just faster.
"""
import argparse
import pickle
import random
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import torch
from torch_geometric.data import HeteroData

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
DATASET_PATH = DATA_DIR / "dataset.pkl"
GRAPH_PATH = DATA_DIR / "full_graph.pt"

# ---------------------------------------------------------------------
# Static entities (reusing the course's real IRIs & names where given)
# ---------------------------------------------------------------------

SUPPLIERS = [
    # (name, region) -- the first six are the real Session 5
    # entity-resolution suppliers; the rest are synthetic, added only
    # to give the graph enough scale to train on.
    ("Acme Logistics", "Beirut"),
    ("Brunel Freight Group", "Rotterdam"),
    ("Mediterranean Shipping Co", "Hamburg"),
    ("Northline Carriers", "Tripoli"),
    ("Cedars Cargo", "Beirut"),
    ("Atlas Overland", "Rotterdam"),
    ("Levant Components", "Tripoli"),
    ("Rhine Valley Parts", "Hamburg"),
    ("Delta Textiles", "Beirut"),
    ("NorthSea Machinery", "Rotterdam"),
]

PRODUCTS = [
    # (name, category, fragile)
    ("Marine Diesel Pump", "machinery", False),
    ("Industrial Bearing Set", "machinery", False),
    ("Solar Inverter Unit", "electronics", True),
    ("LED Lighting Array", "electronics", True),
    ("Woven Textile Roll", "textiles", False),
    ("Surgical Mask Carton", "pharma", True),
    ("Vaccine Cold-Chain Box", "pharma", True),
    ("Steel Pipe Section", "machinery", False),
    ("Circuit Board Tray", "electronics", True),
    ("Olive Oil Drum", "food", False),
    ("Frozen Produce Pallet", "food", True),
    ("Cotton Bale", "textiles", False),
]

PLANTS = [
    # (name, region)
    ("Beirut Assembly Plant", "Beirut"),
    ("Tripoli Packaging Plant", "Tripoli"),
    ("Rotterdam Distribution Center", "Rotterdam"),
    ("Hamburg Fulfillment Center", "Hamburg"),
]

PORTS = [
    # (name, region, base_congestion) -- base_congestion is a mild
    # structural prior only; the DYNAMIC Hamburg congestion event
    # below is what drives the leakage demo.
    ("Port of Beirut", "Beirut", 0.05),
    ("Port of Rotterdam", "Rotterdam", 0.08),
    ("Port of Hamburg", "Hamburg", 0.06),
    ("Port of Tripoli", "Tripoli", 0.05),
]

CARRIERS = [
    # (name, sla_days, base_late_rate) -- dhl and aramex are the real
    # carriers used since Session 4; fedex is added for scale.
    ("dhl", 4, 0.10),
    ("aramex", 5, 0.12),
    ("fedex", 4, 0.15),
]

HAMBURG_CONGESTION_START = date(2026, 1, 1)
DATE_RANGE_START = date(2025, 5, 1)
DATE_RANGE_END = date(2026, 8, 31)

N_ORDERS = 360


def _random_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def build_dataset():
    """Builds the raw synthetic tables (plain Python lists/dicts),
    independent of any GNN framework, and returns them as a dict. This
    is the single source of truth every downstream script (node
    classification, link prediction, the tabular baseline, the
    leakage demo) reuses instead of each re-simulating its own data."""
    suppliers, products, plants, ports, carriers = SUPPLIERS, PRODUCTS, PLANTS, PORTS, CARRIERS

    # Real PO ids from earlier sessions, kept as literal rows so the
    # running case study stays recognizable across the whole course.
    known_pos = [
        dict(po_id="po88", carrier="dhl", dispatch=date(2026, 3, 10), delivered=date(2026, 3, 14)),
        dict(po_id="po99", carrier="aramex", dispatch=date(2026, 3, 20), delivered=date(2026, 3, 18)),  # backwards, kept as-is
        dict(po_id="po101", carrier="dhl", dispatch=date(2026, 2, 1), delivered=None),
        dict(po_id="po104", carrier="aramex", dispatch=date(2026, 4, 5), delivered=None),
    ]

    orders = []
    for i in range(N_ORDERS):
        supplier_idx = random.randrange(len(suppliers))
        product_idx = random.randrange(len(products))
        plant_idx = random.randrange(len(plants))
        carrier_idx = random.randrange(len(carriers))
        # Bias port choice towards the supplier's home region, like a
        # real logistics network would, but leave some cross-shipping.
        supplier_region = suppliers[supplier_idx][1]
        home_ports = [j for j, p in enumerate(ports) if p[1] == supplier_region]
        if home_ports and random.random() < 0.75:
            port_idx = random.choice(home_ports)
        else:
            port_idx = random.randrange(len(ports))

        dispatch = _random_date(DATE_RANGE_START, DATE_RANGE_END)

        carrier_name, sla_days, base_late_rate = carriers[carrier_idx]
        port_name, port_region, port_base_congestion = ports[port_idx]
        _, _, fragile = products[product_idx]

        # --- transit time simulation ---
        transit_days = np.random.normal(loc=sla_days - 0.5, scale=1.1)
        transit_days += np.random.exponential(scale=base_late_rate * 3)
        transit_days += np.random.exponential(scale=port_base_congestion * 3)
        if fragile:
            transit_days += np.random.uniform(0, 0.6)

        # *** the injected regime change ***
        # Carrier SLAs are contractual and do not change, so this
        # directly inflates the late rate for Hamburg-routed orders
        # dispatched on/after the cutoff.
        if port_name == "Port of Hamburg" and dispatch >= HAMBURG_CONGESTION_START:
            transit_days += np.random.normal(loc=4.5, scale=1.2)

        transit_days = max(0.5, transit_days)
        delivered = dispatch + timedelta(days=round(transit_days))
        late = int((delivered - dispatch).days > sla_days)

        order_value = float(np.random.lognormal(mean=7.0, sigma=0.6))
        quantity = int(np.random.randint(1, 500))

        orders.append(dict(
            po_id=f"po_synth_{i:04d}",
            supplier_idx=supplier_idx,
            product_idx=product_idx,
            plant_idx=plant_idx,
            carrier_idx=carrier_idx,
            port_idx=port_idx,
            dispatch=dispatch,
            delivered=delivered,
            sla_days=sla_days,
            transit_days=(delivered - dispatch).days,
            late=late,
            order_value=order_value,
            quantity=quantity,
        ))

    return dict(
        suppliers=suppliers, products=products, plants=plants, ports=ports,
        carriers=carriers, orders=orders, known_pos=known_pos,
        hamburg_congestion_start=HAMBURG_CONGESTION_START,
    )


# ---------------------------------------------------------------------
# HeteroData construction
# ---------------------------------------------------------------------

def _onehot_region_features(items, region_getter, extra=None):
    regions = sorted(set(region_getter(item) for item in items))
    region_to_idx = {r: i for i, r in enumerate(regions)}
    feats = []
    for item in items:
        onehot = [0.0] * len(regions)
        onehot[region_to_idx[region_getter(item)]] = 1.0
        if extra is not None:
            onehot.append(extra(item))
        feats.append(onehot)
    return torch.tensor(feats, dtype=torch.float)


def _supplier_features(suppliers):
    return _onehot_region_features(suppliers, lambda s: s[1])


def _product_features(products):
    cats = sorted(set(c for _, c, _ in products))
    cat_to_idx = {c: i for i, c in enumerate(cats)}
    feats = []
    for name, cat, fragile in products:
        onehot = [0.0] * len(cats)
        onehot[cat_to_idx[cat]] = 1.0
        onehot.append(1.0 if fragile else 0.0)
        feats.append(onehot)
    return torch.tensor(feats, dtype=torch.float)


def _plant_features(plants):
    return _onehot_region_features(plants, lambda p: p[1])


def _port_features(ports):
    return _onehot_region_features(ports, lambda p: p[1], extra=lambda p: p[2])


def _carrier_features(carriers):
    return torch.tensor([[float(sla_days), base_late_rate] for _, sla_days, base_late_rate in carriers],
                         dtype=torch.float)


def _order_features(orders):
    # Deliberately NOT including the raw dispatch date (that would be
    # a trivial giveaway of the regime). Features are order-intrinsic
    # only; any signal about the Hamburg congestion has to come
    # through message passing from the port/carrier nodes and from
    # which OTHER orders the model was trained on -- exactly the
    # transductive-vs-temporal point leakage_demo.py makes.
    vals = np.array([[o["order_value"], o["quantity"], o["sla_days"]] for o in orders], dtype=np.float32)
    mean = vals.mean(axis=0, keepdims=True)
    std = vals.std(axis=0, keepdims=True) + 1e-6
    vals = (vals - mean) / std
    return torch.tensor(vals, dtype=torch.float)


def build_graph(dataset, order_indices=None):
    """Builds a HeteroData object containing all static entity nodes
    plus the ORDER nodes/edges listed in `order_indices` (default: all
    orders). Used both for the full transductive graph (order_indices
    left as None) and for inductive train-time subgraphs that only
    contain the training period's orders (see leakage_demo.py).

    Returns (data, order_indices, supplier_product_pairs)."""
    suppliers, products, plants, ports, carriers = (
        dataset["suppliers"], dataset["products"], dataset["plants"],
        dataset["ports"], dataset["carriers"],
    )
    orders = dataset["orders"]

    if order_indices is None:
        order_indices = list(range(len(orders)))
    sub_orders = [orders[i] for i in order_indices]
    n = len(sub_orders)

    data = HeteroData()
    data["supplier"].x = _supplier_features(suppliers)
    data["product"].x = _product_features(products)
    data["plant"].x = _plant_features(plants)
    data["port"].x = _port_features(ports)
    data["carrier"].x = _carrier_features(carriers)

    data["order"].x = _order_features(sub_orders)
    data["order"].y = torch.tensor([o["late"] for o in sub_orders], dtype=torch.long)
    data["order"].po_id = [o["po_id"] for o in sub_orders]
    data["order"].dispatch_ordinal = torch.tensor(
        [o["dispatch"].toordinal() for o in sub_orders], dtype=torch.long
    )

    order_arange = torch.arange(n, dtype=torch.long)

    def rel_edge_index(key):
        dst = torch.tensor([o[key] for o in sub_orders], dtype=torch.long)
        return torch.stack([order_arange, dst], dim=0)

    data["order", "ordered_from", "supplier"].edge_index = rel_edge_index("supplier_idx")
    data["order", "contains", "product"].edge_index = rel_edge_index("product_idx")
    data["order", "shipped_via", "carrier"].edge_index = rel_edge_index("carrier_idx")
    data["order", "departs_from", "port"].edge_index = rel_edge_index("port_idx")
    data["order", "destined_to", "plant"].edge_index = rel_edge_index("plant_idx")

    # Static structural edges (not order-indexed): a supplier ships
    # from any port in its own region, a plant is served by any port
    # in its own region.
    supplier_port_pairs = [
        (si, pi) for si, (_, region) in enumerate(suppliers)
        for pi, (_, pregion, _) in enumerate(ports) if pregion == region
    ]
    if supplier_port_pairs:
        src, dst = zip(*supplier_port_pairs)
        data["supplier", "ships_from", "port"].edge_index = torch.tensor([list(src), list(dst)], dtype=torch.long)

    plant_port_pairs = [
        (pli, pi) for pli, (_, region) in enumerate(plants)
        for pi, (_, pregion, _) in enumerate(ports) if pregion == region
    ]
    if plant_port_pairs:
        src, dst = zip(*plant_port_pairs)
        data["plant", "served_by", "port"].edge_index = torch.tensor([list(src), list(dst)], dtype=torch.long)

    carrier_port_pairs = [(ci, pi) for ci in range(len(carriers)) for pi in range(len(ports))]
    src, dst = zip(*carrier_port_pairs)
    data["carrier", "operates_at", "port"].edge_index = torch.tensor([list(src), list(dst)], dtype=torch.long)

    # supplier -> supplies -> product, derived from which orders pair a
    # given supplier with a given product across the WHOLE dataset
    # (real co-occurrence), used for link prediction in
    # train_link_prediction.py / train_pykeen.py.
    sp_pairs = sorted(set((o["supplier_idx"], o["product_idx"]) for o in orders))
    src, dst = zip(*sp_pairs)
    data["supplier", "supplies", "product"].edge_index = torch.tensor([list(src), list(dst)], dtype=torch.long)

    return data, order_indices, sp_pairs


def load_or_build(force_rebuild=False):
    """Loads the cached dataset + full graph from data/ if present,
    otherwise builds them and saves them there. The generator is fully
    deterministic (module-level seed=42), so a cached copy and a fresh
    build are byte-identical -- this exists purely so every other
    script here does not re-simulate 360 orders on every run.

    Returns (dataset, full_graph)."""
    if not force_rebuild and DATASET_PATH.exists() and GRAPH_PATH.exists():
        with open(DATASET_PATH, "rb") as f:
            dataset = pickle.load(f)
        # weights_only=False: this file was written by save_all() below,
        # in this same folder, in the same run -- not an untrusted
        # download. torch >=2.6 defaults torch.load to weights_only=True,
        # which rejects PyG's HeteroData/BaseStorage classes outright
        # (a real gotcha hit while adapting this lab: the verified
        # prototype wrote full_graph.pt but never actually round-tripped
        # a load of it, and the default load raises
        # `_pickle.UnpicklingError: Weights only load failed ... Unsupported
        # global: GLOBAL torch_geometric.data.storage.BaseStorage`).
        full_graph = torch.load(GRAPH_PATH, weights_only=False)
        print(f"Loaded cached dataset + graph from {DATA_DIR.relative_to(HERE)}/ "
              "(pass --force-rebuild to regenerate)")
        return dataset, full_graph

    dataset = build_dataset()
    full_graph, _, _ = build_graph(dataset)
    save_all(dataset, full_graph)
    print(f"Built and saved dataset + graph to {DATA_DIR.relative_to(HERE)}/")
    return dataset, full_graph


def save_all(dataset, full_graph):
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATASET_PATH, "wb") as f:
        pickle.dump(dataset, f)
    torch.save(full_graph, GRAPH_PATH)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force-rebuild", action="store_true",
                         help="Ignore any cached data/dataset.pkl and data/full_graph.pt and rebuild.")
    args = parser.parse_args()

    dataset, data = load_or_build(force_rebuild=args.force_rebuild)
    print(data)

    n_late = sum(o["late"] for o in dataset["orders"])
    print(f"\nTotal orders: {len(dataset['orders'])}, late: {n_late} ({n_late / len(dataset['orders']):.1%})")

    hamburg_idx = next(i for i, p in enumerate(dataset["ports"]) if p[0] == "Port of Hamburg")
    before, after = [], []
    for o in dataset["orders"]:
        if o["port_idx"] == hamburg_idx:
            (before if o["dispatch"] < HAMBURG_CONGESTION_START else after).append(o["late"])
    print(f"\nPort of Hamburg late rate BEFORE {HAMBURG_CONGESTION_START}: "
          f"{np.mean(before):.1%} (n={len(before)})")
    print(f"Port of Hamburg late rate AFTER  {HAMBURG_CONGESTION_START}: "
          f"{np.mean(after):.1%} (n={len(after)})")

    other_late = [o["late"] for o in dataset["orders"] if o["port_idx"] != hamburg_idx]
    print(f"All other ports, overall late rate: {np.mean(other_late):.1%} (n={len(other_late)})")

    print("\nEdge types:")
    for et in data.edge_types:
        print(" ", et, tuple(data[et].edge_index.shape))
    print("\nNode types:")
    for nt in data.node_types:
        print(" ", nt, tuple(data[nt].x.shape) if "x" in data[nt] else None)


if __name__ == "__main__":
    main()
