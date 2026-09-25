"""Compare the mapped graph with Session 2's graph, triple by triple.

    python compare_with_session2.py                       # brunel-mapped.nt
    python compare_with_session2.py --mapped my-mapped.nt

Run from demos/session-05-integration/ after materialize.py (and Session 2's
convert_to_rdf.py, for demos/session-02-rdf-sparql/brunel.ttl).

Two programs built the same graph from the same tables: Session 2's Python
converter and today's R2RML mapping. This script shows every difference.
Values are compared by meaning (14.3 and 14.30 are the same decimal). Rate
bands are blank nodes, which have no name to compare, so a band is compared
by everything said about it. Decimals are compared as numbers, to 12
significant digits: Session 2 read the CSV with pandas' fast number parser,
which can miss a long decimal by one unit in its last digit (it wrote
1.462970094059406 for the CSV's 1.4629700940594061); the mapping keeps the
CSV's digits exactly. Session 2's small schema (the vocabulary's
labels, domains and ranges, 49 triples) is not data and is left out: the
mapping produces data only.
"""

import argparse
from collections import Counter
from pathlib import Path

from rdflib import RDF, XSD, BNode, Graph, Literal, URIRef

HERE = Path(__file__).resolve().parent
SESSION2 = HERE.parent / "session-02-rdf-sparql" / "brunel.ttl"
VOCAB = "https://ul.edu.lb/kr/scm#"


def value(term):
    if not isinstance(term, Literal):
        return ("iri", str(term))
    if term.datatype == XSD.decimal:
        return ("num", float(f"{float(term):.12g}"))  # equal to 12 significant digits
    return ("lit", term.toPython() if term.datatype else str(term))


def split(g):
    """Named triples as comparable tuples; blank node bands as sorted property lists."""
    named, bands = Counter(), Counter()
    for s, p, o in g:
        if isinstance(s, URIRef) and str(s).startswith(VOCAB):
            continue  # the schema: classes and properties describing themselves
        if isinstance(s, BNode):
            continue
        named[(str(s), str(p), value(o))] += 1
    for b in set(g.subjects(RDF.type, URIRef(VOCAB + "RateBand"))):
        bands[tuple(sorted((str(p), value(o)) for p, o in g.predicate_objects(b)))] += 1
    return named, bands


def short(t):
    s, p, (_, o) = t
    cut = lambda x: str(x).replace("https://ul.edu.lb/kr/id/", "").replace(VOCAB, "ul:").replace(str(RDF), "rdf:")
    return f"{cut(s)}  {cut(p)}  {cut(o)}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mapped", default=str(HERE / "brunel-mapped.nt"))
    args = ap.parse_args()
    s2 = Graph().parse(SESSION2)
    mapped = Graph().parse(args.mapped, format="nt")
    n2, b2 = split(s2)
    nm, bm = split(mapped)
    schema = len(s2) - sum(n2.values()) - sum(sum(1 for _ in s2.predicate_objects(b)) for b in s2.subjects(RDF.type, URIRef(VOCAB + "RateBand")))
    print(f"Session 2 graph   {len(s2):>8,} triples  ({schema} schema triples left out)")
    print(f"mapped graph      {len(mapped):>8,} triples")
    only2, onlym = n2 - nm, nm - n2
    print(f"\nnamed triples in both          {sum((n2 & nm).values()):>7,}")
    print(f"only in Session 2's graph      {sum(only2.values()):>7,}")
    print(f"only in the mapped graph       {sum(onlym.values()):>7,}")
    print(f"rate bands in both             {sum((b2 & bm).values()):>7,} of {sum(b2.values()):,} and {sum(bm.values()):,}")
    for title, diff in (("\nOnly in Session 2's graph:", only2), ("\nOnly in the mapped graph:", onlym)):
        if diff:
            print(title)
            for t in sorted(diff)[:12]:
                print("  " + short(t))
            if sum(diff.values()) > 12:
                print(f"  ... and {sum(diff.values()) - 12} more")


if __name__ == "__main__":
    main()
