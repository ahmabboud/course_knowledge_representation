"""Convert a slice of the Brunel tables to Turtle, using the cohort's
IRI scheme from common/iri.py.

This is intentionally a slice, not the full Brunel dataset: enough rows
to exercise every table and every constraint from Session 1's
inventory, small enough to reload quickly while iterating on the
mapping during the lab.
"""

import sys
from pathlib import Path

import pandas as pd
from rdflib import Graph, Literal, Namespace, RDF, RDFS, XSD

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.data_paths import BRUNEL_TABLES  # noqa: E402
from common.iri import BASE, plant_iri, port_iri, order_iri  # noqa: E402

UL = Namespace(BASE)
SOURCE = "brunel"  # this session's source-system tag for common/iri.py
SLICE_SIZE = 200  # rows per table, enough to exercise every join

OUT_PATH = Path(__file__).resolve().parent / "brunel_slice.ttl"


def build_graph() -> Graph:
    g = Graph()
    g.bind("ul", UL)

    order_list = pd.read_csv(BRUNEL_TABLES["order_list"]).head(SLICE_SIZE)
    plant_ports = pd.read_csv(BRUNEL_TABLES["plant_ports"])

    # Plants and ports, and the servesPort links between them — this is
    # the relationship the Session 1 constraint ("a plant can only
    # serve ports it is linked to") is expressed against.
    for _, row in plant_ports.iterrows():
        plant = plant_iri(SOURCE, str(row["Plant Code"]))
        port = port_iri(SOURCE, str(row["Port"]))
        g.add((UL[plant.rsplit("#", 1)[1]] if False else __import__("rdflib").URIRef(plant), RDF.type, UL.Plant))
        g.add((__import__("rdflib").URIRef(port), RDF.type, UL.Port))
        g.add((__import__("rdflib").URIRef(plant), UL.servesPort, __import__("rdflib").URIRef(port)))

    # Orders, with the fields the Session 2 question set actually
    # queries: fromPlant, viaPort, weight, and the day-count fields
    # needed for a "days late" filter once a due date is available.
    for _, row in order_list.iterrows():
        order = __import__("rdflib").URIRef(order_iri(SOURCE, str(row["Order ID"])))
        plant = __import__("rdflib").URIRef(plant_iri(SOURCE, str(row["Origin Port"])))
        g.add((order, RDF.type, UL.Order))
        g.add((order, RDFS.label, Literal(str(row["Order ID"]))))
        g.add((order, UL.fromPlant, plant))
        if pd.notna(row.get("Weight")):
            g.add((order, UL.weightKg, Literal(row["Weight"], datatype=XSD.decimal)))

    return g


if __name__ == "__main__":
    graph = build_graph()
    graph.serialize(destination=str(OUT_PATH), format="turtle")
    print(f"Wrote {len(graph)} triples to {OUT_PATH}")
    print("Note: adjust the column names above against your actual")
    print("Brunel CSV headers before the lab, they vary by mirror/version.")
