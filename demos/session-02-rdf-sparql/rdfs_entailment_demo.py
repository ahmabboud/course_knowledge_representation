"""Entailment against constraint, on our own data (Session 2, Part 3).

RDFS never rejects data. It adds the facts that follow from the schema.
This script counts orders before and after RDFS reasoning, then adds one
deliberately careless triple and shows what RDFS concludes from it.

    pip install owlrl        (not in requirements.txt: only this demo uses it)
    python rdfs_entailment_demo.py
"""

import time
from pathlib import Path

import owlrl
from rdflib import Graph, Namespace, RDF, URIRef

HERE = Path(__file__).resolve().parent
UL = Namespace("https://ul.edu.lb/kr/scm#")
Q = "SELECT (COUNT(DISTINCT ?o) AS ?n) WHERE { ?o a <https://ul.edu.lb/kr/scm#Order> }"

full = Graph()
full.parse(HERE / "brunel.ttl")
# Reason over what matters here, so the demo runs in seconds instead of minutes:
# the schema and every type triple. (The whole graph gives the same counts in
# about 4.5 minutes.)
g = Graph()
for t in full.triples((None, RDF.type, None)):
    g.add(t)
schema_ns = ("http://www.w3.org/2000/01/rdf-schema#",)
for s, p, o in full:
    if str(p).startswith(schema_ns):
        g.add((s, p, o))
# One careless triple: a carrier is said to be carried by a carrier.
mistake = URIRef("https://ul.edu.lb/kr/id/carrier/brunel/V444_0")
g.add((mistake, UL.carriedBy, URIRef("https://ul.edu.lb/kr/id/carrier/brunel/V444_1")))

before = int(list(g.query(Q))[0][0])
start = time.perf_counter()
owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)
secs = time.perf_counter() - start
after = int(list(g.query(Q))[0][0])
print(f"Orders before RDFS reasoning: {before}")
print(f"Orders after RDFS reasoning:  {after}  ({secs:.1f} s)")
print(f"Is carrier V444_0 now an Order?  {(mistake, RDF.type, UL.Order) in g}")
print("No error was raised. The domain of ul:carriedBy is ul:Order, so RDFS concluded it.")
