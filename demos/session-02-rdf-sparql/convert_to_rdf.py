"""Convert Brunel's orders, plants, ports and carriers to RDF with rdflib,
using the cohort's IRI scheme from common/iri.py.

Writes, next to this file:

* brunel.ttl   every triple in one default graph, plus a small RDFS
               schema. This is what Fuseki, Oxigraph and Neo4j load.
* brunel.trig  the same triples, one named graph per source table
               (plus one for the schema), so
               each triple remembers which table it came from.
* sample/      one order in Turtle, N-Triples and JSON-LD, for the
               serialization slide.

Run from demos/session-02-rdf-sparql/:   python convert_to_rdf.py
"""

import sys
from pathlib import Path

import pandas as pd
from rdflib import BNode, Dataset, Graph, Literal, Namespace, RDF, RDFS, URIRef, XSD

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.data_paths import BRUNEL_TABLES  # noqa: E402
from common.iri import (VOCAB, carrier_iri, customer_iri, graph_iri,  # noqa: E402
                        order_iri, plant_iri, port_iri, product_iri)

UL = Namespace(VOCAB)
SOURCE = "brunel"
HERE = Path(__file__).resolve().parent


def schema(g: Graph) -> None:
    """A small RDFS schema: the words the data uses, with domain and range.
    RDFS draws conclusions from these; it never rejects data (Session 4 does)."""
    for cls, label in [(UL.Order, "Order"), (UL.LateOrder, "Late order"), (UL.Plant, "Plant"),
                       (UL.Port, "Port"), (UL.Carrier, "Carrier"), (UL.Customer, "Customer"),
                       (UL.Product, "Product"), (UL.RateBand, "Freight rate band")]:
        g.add((cls, RDF.type, RDFS.Class))
        g.add((cls, RDFS.label, Literal(label, lang="en")))
    g.add((UL.LateOrder, RDFS.subClassOf, UL.Order))
    props = [
        (UL.fromPlant, UL.Order, UL.Plant, "made at plant"),
        (UL.shipsFrom, UL.Order, UL.Port, "leaves from port"),
        (UL.shipsTo, UL.Order, UL.Port, "arrives at port"),
        (UL.carriedBy, UL.Order, UL.Carrier, "carried by"),
        (UL.orderedBy, UL.Order, UL.Customer, "ordered by"),
        (UL.ofProduct, UL.Order, UL.Product, "of product"),
        (UL.servesPort, UL.Plant, UL.Port, "ships through port"),
        (UL.makes, UL.Plant, UL.Product, "makes product"),
    ]
    for p, dom, rng, label in props:
        g.add((p, RDF.type, RDF.Property))
        g.add((p, RDFS.domain, dom))
        g.add((p, RDFS.range, rng))
        g.add((p, RDFS.label, Literal(label, lang="en")))


def build() -> Dataset:
    ds = Dataset()
    ds.bind("ul", UL)
    g_schema = ds.graph(URIRef(graph_iri(SOURCE, "schema")))
    g_orders = ds.graph(URIRef(graph_iri(SOURCE, "OrderList")))
    g_ports = ds.graph(URIRef(graph_iri(SOURCE, "PlantPorts")))
    g_prod = ds.graph(URIRef(graph_iri(SOURCE, "ProductsPerPlant")))
    g_rates = ds.graph(URIRef(graph_iri(SOURCE, "FreightRates")))
    schema(g_schema)

    # Keys are read as text, so an ID such as 1447296446.7 keeps its exact form.
    orders = pd.read_csv(BRUNEL_TABLES["order_list"], dtype={"Order ID": str, "Product ID": str})
    plant_ports = pd.read_csv(BRUNEL_TABLES["plant_ports"])
    per_plant = pd.read_csv(BRUNEL_TABLES["products_per_plant"], dtype={"Product ID": str})
    rates = pd.read_csv(BRUNEL_TABLES["freight_rates"])

    # A rate band has no key of its own in the source: it is only its carrier,
    # lane, service and weight range. That makes it a blank node.
    for _, r in rates.iterrows():
        b = BNode()
        g_rates.add((b, RDF.type, UL.RateBand))
        g_rates.add((b, UL.bandCarrier, URIRef(carrier_iri(SOURCE, r["Carrier"]))))
        g_rates.add((b, UL.bandFrom, URIRef(port_iri(SOURCE, r["orig_port_cd"]))))
        g_rates.add((b, UL.bandTo, URIRef(port_iri(SOURCE, r["dest_port_cd"]))))
        g_rates.add((b, UL.bandService, Literal(r["svc_cd"])))
        g_rates.add((b, UL.minWeight, Literal(str(r["minm_wgh_qty"]), datatype=XSD.decimal)))
        g_rates.add((b, UL.maxWeight, Literal(str(r["max_wgh_qty"]), datatype=XSD.decimal)))
        g_rates.add((b, UL.rate, Literal(str(r["rate"]), datatype=XSD.decimal)))

    for _, r in plant_ports.iterrows():
        plant, port = URIRef(plant_iri(SOURCE, r["Plant Code"])), URIRef(port_iri(SOURCE, r["Port"]))
        g_ports.add((plant, RDF.type, UL.Plant))
        g_ports.add((port, RDF.type, UL.Port))
        g_ports.add((plant, UL.servesPort, port))

    for _, r in per_plant.iterrows():
        plant, prod = URIRef(plant_iri(SOURCE, r["Plant Code"])), URIRef(product_iri(SOURCE, r["Product ID"]))
        g_prod.add((plant, UL.makes, prod))
        g_prod.add((prod, RDF.type, UL.Product))

    for _, r in orders.iterrows():
        o = URIRef(order_iri(SOURCE, r["Order ID"]))
        late = int(r["Ship Late Day count"])
        # Late orders are typed only as LateOrder. RDFS, or a property path,
        # is what makes them count as orders too.
        g_orders.add((o, RDF.type, UL.LateOrder if late > 0 else UL.Order))
        g_orders.add((o, UL.orderId, Literal(r["Order ID"])))
        g_orders.add((o, UL.orderDate, Literal(str(r["Order Date"])[:10], datatype=XSD.date)))
        g_orders.add((o, UL.fromPlant, URIRef(plant_iri(SOURCE, r["Plant Code"]))))
        g_orders.add((o, UL.shipsFrom, URIRef(port_iri(SOURCE, r["Origin Port"]))))
        g_orders.add((o, UL.shipsTo, URIRef(port_iri(SOURCE, r["Destination Port"]))))
        g_orders.add((o, UL.carriedBy, URIRef(carrier_iri(SOURCE, r["Carrier"]))))
        g_orders.add((o, UL.orderedBy, URIRef(customer_iri(SOURCE, r["Customer"]))))
        g_orders.add((o, UL.ofProduct, URIRef(product_iri(SOURCE, r["Product ID"]))))
        g_orders.add((o, UL.serviceLevel, Literal(r["Service Level"])))
        g_orders.add((o, UL.unitQuantity, Literal(int(r["Unit quantity"]), datatype=XSD.integer)))
        g_orders.add((o, UL.weight, Literal(str(r["Weight"]), datatype=XSD.decimal)))
        g_orders.add((o, UL.lateDays, Literal(late, datatype=XSD.integer)))
        g_orders.add((URIRef(carrier_iri(SOURCE, r["Carrier"])), RDF.type, UL.Carrier))
        g_orders.add((URIRef(customer_iri(SOURCE, r["Customer"])), RDF.type, UL.Customer))
    return ds


def write(ds: Dataset) -> None:
    ds.serialize(HERE / "brunel.trig", format="trig")
    union = Graph()
    union.bind("ul", UL)
    for s, p, o, _ in ds.quads((None, None, None, None)):
        union.add((s, p, o))
    union.serialize(HERE / "brunel.ttl", format="turtle")

    # One order, three serializations.
    sample = HERE / "sample"
    sample.mkdir(exist_ok=True)
    first = URIRef(order_iri(SOURCE, "1447296446.7"))
    one = Graph()
    one.bind("ul", UL)
    for t in union.triples((first, None, None)):
        one.add(t)
    one.serialize(sample / "order.ttl", format="turtle")
    one.serialize(sample / "order.nt", format="nt", encoding="utf-8")
    one.serialize(sample / "order.jsonld", format="json-ld", context={"ul": VOCAB}, indent=2)
    named = [g for g in ds.graphs() if g.identifier != ds.default_graph.identifier]
    print(f"brunel.ttl: {len(union)} triples · brunel.trig: {len(named)} named graphs "
          f"· sample order: {len(one)} triples")


if __name__ == "__main__":
    write(build())
