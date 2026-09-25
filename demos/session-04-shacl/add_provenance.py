"""Record, in PROV-O, where the Session 2 graph came from: for each named
graph in brunel.trig, which CSV file it was derived from, which run
generated it, which program ran, and when. Then answer one provenance
question with SPARQL: which table, file and run produced one given triple?

    python add_provenance.py

Run from demos/session-04-shacl/, after Session 2's convert_to_rdf.py.
Writes provenance.ttl next to this script (regenerate, do not edit).

PROV-O, the W3C provenance ontology (Recommendation, 2013), has three core
classes: an Entity (a thing: a file, a graph), an Activity (something that
happened: a conversion run), an Agent (who or what is responsible: here a
program). The IRIs follow the course convention (AGENTS.md 2d).
"""

import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

from rdflib import RDF, RDFS, XSD, Dataset, Graph, Literal, Namespace, URIRef

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from common.data_paths import BRUNEL_TABLES  # noqa: E402
from common.iri import DATA, graph_iri  # noqa: E402

TRIG = HERE.parent / "session-02-rdf-sparql" / "brunel.trig"
CONVERTER = HERE.parent / "session-02-rdf-sparql" / "convert_to_rdf.py"
PROV = Namespace("http://www.w3.org/ns/prov#")
DCT = Namespace("http://purl.org/dc/terms/")
VOID = Namespace("http://rdfs.org/ns/void#")
TABLE_FILE = {"OrderList": "order_list", "PlantPorts": "plant_ports",
              "ProductsPerPlant": "products_per_plant", "FreightRates": "freight_rates"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def when(path):
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0)


def main():
    if not TRIG.exists():
        sys.exit("brunel.trig not found: run python convert_to_rdf.py in demos/session-02-rdf-sparql/ first.")
    ds = Dataset()
    ds.parse(TRIG, format="trig")
    made = when(TRIG)

    g = Graph()
    for p, ns in (("prov", PROV), ("dcterms", DCT), ("void", VOID), ("xsd", XSD), ("rdfs", RDFS)):
        g.bind(p, ns)
    run = URIRef(f"{DATA}run/brunel/convert-{made.strftime('%Y%m%dT%H%M%SZ')}")
    program = URIRef(f"{DATA}software/course/convert_to_rdf.py")
    g.add((program, RDF.type, PROV.SoftwareAgent))
    g.add((program, RDFS.label, Literal("convert_to_rdf.py (Session 2)")))
    g.add((program, DCT.identifier, Literal("sha256:" + sha256(CONVERTER))))
    g.add((run, RDF.type, PROV.Activity))
    g.add((run, RDFS.label, Literal("Session 2 conversion of the Brunel tables to RDF")))
    g.add((run, PROV.wasAssociatedWith, program))
    g.add((run, PROV.endedAtTime, Literal(made.isoformat(), datatype=XSD.dateTime)))

    rows = []
    for table, key in TABLE_FILE.items():
        csv = BRUNEL_TABLES[key]
        f = URIRef(f"{DATA}file/brunel/{csv.name}")
        graph = URIRef(graph_iri("brunel", table))
        n = len(ds.graph(graph))
        g.add((f, RDF.type, PROV.Entity))
        g.add((f, DCT.title, Literal(csv.name)))
        g.add((f, DCT.identifier, Literal("sha256:" + sha256(csv))))
        g.add((run, PROV.used, f))
        g.add((graph, RDF.type, PROV.Entity))
        g.add((graph, PROV.wasDerivedFrom, f))
        g.add((graph, PROV.wasGeneratedBy, run))
        g.add((graph, PROV.generatedAtTime, Literal(made.isoformat(), datatype=XSD.dateTime)))
        g.add((graph, VOID.triples, Literal(n)))
        rows.append((table, csv.name, n))
    out = HERE / "provenance.ttl"
    g.serialize(out, format="turtle")
    print(f"provenance.ttl: {len(g)} triples about {len(rows)} named graphs, 1 run, 1 program")
    for table, name, n in rows:
        print(f"  graph {table:<17} {n:>7,} triples  derived from {name}")

    # The question provenance answers: where did this one fact come from?
    ds.graph(URIRef(f"{DATA}graph/brunel/provenance")).parse(out)
    q = """
    PREFIX ul: <https://ul.edu.lb/kr/scm#>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    SELECT ?g ?file ?run ?time WHERE {
      GRAPH ?g { <https://ul.edu.lb/kr/id/order/brunel/1447296446.7> ul:carriedBy ?c }
      GRAPH ?p { ?g prov:wasDerivedFrom ?f ; prov:wasGeneratedBy ?run .
                 ?f dcterms:title ?file . ?run prov:endedAtTime ?time } }"""
    for r in ds.query(q):
        print("\nWhere does 'order 1447296446.7 carried by V44_3' come from?")
        print(f"  named graph {r.g}\n  file        {r.file}\n  run         {r.run}\n  finished    {r.time}")


if __name__ == "__main__":
    main()
