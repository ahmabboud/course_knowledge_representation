"""Turn the Brunel graph into the shape a graph neural network reads: one
table of features per kind of node, one list of links per kind of edge
(PyTorch Geometric's HeteroData).

    python build_graph.py

Run from demos/session-06-learning/ with demos/.venv active. Reads Session 5's
materialized graph (demos/session-05-integration/brunel-mapped.nt), or, if
that is missing, Session 2's (demos/session-02-rdf-sparql/brunel.ttl): the
same orders. Writes data/brunel-graph.pt.

The label to predict, "is this order late?", is in the graph TWICE: as the
class ul:LateOrder and as the value ul:lateDays. Both are removed from what
the model sees; the label is kept apart, in y. Leave either one in and any
model scores perfectly, and learns nothing (baseline.py shows it).
"""

import sys
import time
from pathlib import Path

import numpy as np
import torch
from rdflib import RDF, Graph, Namespace
from torch_geometric.data import HeteroData

HERE = Path(__file__).resolve().parent
SOURCES = [HERE.parent / "session-05-integration" / "brunel-mapped.nt",
           HERE.parent / "session-02-rdf-sparql" / "brunel.ttl"]
OUT = HERE / "data" / "brunel-graph.pt"
UL = Namespace("https://ul.edu.lb/kr/scm#")
# Each order links to one thing of each of these kinds.
ORDER_LINKS = [(UL.orderedBy, "customer"), (UL.carriedBy, "carrier"), (UL.fromPlant, "plant"),
               (UL.shipsFrom, "port"), (UL.ofProduct, "product")]
SERVICE = ["CRF", "DTD", "DTP"]


def main():
    src = next((p for p in SOURCES if p.exists()), None)
    if src is None:
        sys.exit("No Brunel graph found. Run Session 5's materialize.py, or Session 2's convert_to_rdf.py.")
    t0 = time.time()
    g = Graph().parse(src, format="nt" if src.suffix == ".nt" else "turtle")
    orders = sorted(set(g.subjects(RDF.type, UL.Order)) | set(g.subjects(RDF.type, UL.LateOrder)), key=str)

    # The label, kept apart. It comes from the class; lateDays says the same.
    y = np.array([1 if (o, RDF.type, UL.LateOrder) in g else 0 for o in orders])

    ids = {"order": {o: i for i, o in enumerate(orders)}}
    def node(kind, iri):
        table = ids.setdefault(kind, {})
        return table.setdefault(iri, len(table))

    edges = {}
    for o in orders:
        for prop, kind in ORDER_LINKS:
            edges.setdefault(("order", str(prop).split("#")[1], kind), []).append((ids["order"][o], node(kind, g.value(o, prop))))
    # rdflib does not guarantee graph iteration order.  Stable node IDs and
    # edge order make the fixed training seeds reproducible across machines.
    for plant, product in sorted(g.subject_objects(UL.makes), key=lambda pair: tuple(map(str, pair))):
        edges.setdefault(("plant", "makes", "product"), []).append((node("plant", plant), node("product", product)))
    for plant, port in sorted(g.subject_objects(UL.servesPort), key=lambda pair: tuple(map(str, pair))):
        edges.setdefault(("plant", "servesPort", "port"), []).append((node("plant", plant), node("port", port)))

    # What the model may see about an order: weight, quantity, service level.
    # NOT lateDays and NOT the class: that would be the answer.
    weight = np.array([float(g.value(o, UL.weight)) for o in orders])
    qty = np.array([float(g.value(o, UL.unitQuantity)) for o in orders])
    svc = np.array([[1.0 if str(g.value(o, UL.serviceLevel)) == s else 0.0 for s in SERVICE] for o in orders])
    x = np.column_stack([np.log1p(weight), np.log1p(qty), svc])

    data = HeteroData()
    data["order"].x = torch.tensor(x, dtype=torch.float)
    for kind, table in ids.items():
        if kind != "order":
            data[kind].x = torch.eye(len(table))  # one column per node: "which one is it"
    for (s, r, t), pairs in edges.items():
        data[s, r, t].edge_index = torch.tensor(np.array(pairs).T, dtype=torch.long).contiguous()

    extra = {
        "y": torch.tensor(y),
        "late_days": torch.tensor([int(g.value(o, UL.lateDays)) for o in orders]),  # kept ONLY for the leak demo
        "customer": torch.tensor([ids["customer"][g.value(o, UL.orderedBy)] for o in orders]),
        "plant": torch.tensor([ids["plant"][g.value(o, UL.fromPlant)] for o in orders]),
        "carrier": torch.tensor([ids["carrier"][g.value(o, UL.carriedBy)] for o in orders]),
        "order_iri": [str(o) for o in orders],
        "names": {k: [str(i) for i in t] for k, t in ids.items() if k != "order"},
        "source": src.name,
    }
    OUT.parent.mkdir(exist_ok=True)
    torch.save({"data": data, **extra}, OUT)

    print(f"read {src.name}: {len(g):,} triples in {time.time() - t0:.1f} s")
    print("nodes: " + ", ".join(f"{k} {len(v):,}" for k, v in ids.items()))
    print("edges: " + ", ".join(f"{r} {len(p):,}" for (_, r, _), p in edges.items()))
    print(f"label: {int(y.sum())} late orders of {len(y):,} ({y.mean():.1%}), taken out of the features "
          "(the ul:LateOrder class and ul:lateDays)")
    print(f"written: {OUT.relative_to(HERE)}")


if __name__ == "__main__":
    main()
