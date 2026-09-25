"""Time each node shape of brunel-shapes.ttl on its own, on the Session 2
graph: what a SPARQL constraint costs next to a core one. This produces the
numbers on the slide "The cost of reaching for SPARQL too early".

    python shape_timings.py                  # every shape (about 2 minutes)
    python shape_timings.py --shape OrderShape

Run from demos/session-04-shacl/. Writes nothing; copy the output into
reference-outputs/shape-timings.txt when you rerun it for the deck.
"""

import argparse
import time

from pyshacl import validate
from rdflib import RDF, BNode, Graph, Namespace, URIRef

from validate import DEFAULT_DATA, HERE, SH

ULS = Namespace("https://ul.edu.lb/kr/shapes#")


def closure(g, start, out):
    """Copy start's triples, following blank nodes (property shapes, lists)."""
    for p, o in g.predicate_objects(start):
        out.add((start, p, o))
        if isinstance(o, BNode):
            closure(g, o, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shape", help="local name of one node shape, e.g. OrderShape")
    ap.add_argument("--shapes", default=str(HERE / "brunel-shapes.ttl"))
    args = ap.parse_args()
    data = Graph().parse(DEFAULT_DATA)
    shapes = Graph().parse(args.shapes)
    onto = URIRef("https://ul.edu.lb/kr/shapes")
    names = sorted(str(s).rsplit("#", 1)[-1] for s in shapes.subjects(RDF.type, SH.NodeShape))
    for name in [args.shape] if args.shape else names:
        one = Graph()
        closure(shapes, ULS[name], one)
        closure(shapes, onto, one)
        kind = "SPARQL" if (ULS[name], SH.sparql, None) in shapes else "core"
        t0 = time.time()
        _, report, _ = validate(data, shacl_graph=one, inference="none", advanced=True)
        n = len(set(report.subjects(RDF.type, SH.ValidationResult)))
        print(f"{name:<24} {kind:<6} {time.time() - t0:6.1f} s   {n:,} results")


if __name__ == "__main__":
    main()
