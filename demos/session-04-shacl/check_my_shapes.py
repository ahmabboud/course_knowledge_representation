"""Check your part B shapes (my_shapes.ttl): right, or not yet with a hint.

    python check_my_shapes.py                                   # your file
    python check_my_shapes.py solutions/my_shapes_solutions.ttl

Each shape is run alone against part-b/test-orders.ttl (real Brunel orders,
four of them changed on purpose, see that file's header). The checker
compares which orders the shape flags with the orders it should flag. How
you write the shape does not matter; what it catches does.
"""

import sys
from pathlib import Path

from pyshacl import validate
from rdflib import RDF, BNode, Graph, Namespace, URIRef

HERE = Path(__file__).resolve().parent
SH = Namespace("http://www.w3.org/ns/shacl#")
MY = Namespace("https://ul.edu.lb/kr/shapes/my#")
ONTO = URIRef("https://ul.edu.lb/kr/shapes/my")
ORDER = "https://ul.edu.lb/kr/id/order/brunel/"
CONSTRAINTS = {SH.property, SH.sparql, SH["in"], SH.datatype, SH["class"], SH.minCount, SH.maxCount,
               SH.pattern, SH.minInclusive, SH.maxInclusive, SH["or"], SH["and"], SH["not"], SH.node}
EXPECTED = {
    "Y1": {"1447385217.7", "1447291369.7"},
    "Y2": {"1447311670.7"},
    "Y3": {"1447135386.7"},
}


def closure(g, start, out):
    for p, o in g.predicate_objects(start):
        out.add((start, p, o))
        if isinstance(o, BNode):
            closure(g, o, out)


def hint(y, got):
    want = EXPECTED[y]
    if y == "Y1" and got == {"1447291369.7"}:
        return "You catch the order with no customer, not the one with two. Add sh:maxCount 1."
    if y == "Y1" and got == {"1447385217.7"}:
        return "You catch the order with two customers, not the one with none. Add sh:minCount 1."
    if y == "Y2" and len(got) > 1:
        return ('Too many orders flagged. If your bounds are plain text like "2013-01-01", SHACL cannot compare '
                'a date with text, so every date fails: write "2013-01-01"^^xsd:date. Otherwise check that the '
                'bounds are inclusive and cover the whole of 2013.')
    if y == "Y2" and not got:
        return "Nothing flagged. The faulty order is dated 2031: is your upper bound 2013-12-31?"
    if y == "Y3" and "1447296446.7" in got:
        return ("You also flag 1447296446.7, a CRF order that IS carried by V44_3. Compare ?c with the carrier's IRI, "
                "<https://ul.edu.lb/kr/id/carrier/brunel/V44_3>, not with the text \"V44_3\".")
    if y == "Y3" and not got:
        return "Nothing flagged. Does your query SELECT $this, and match the service level exactly as \"CRF\"?"
    missing, extra = want - got, got - want
    parts = []
    if missing:
        parts.append("misses " + ", ".join(sorted(missing)))
    if extra:
        parts.append("also flags " + ", ".join(sorted(extra)) + ", which break no rule of this kind")
    return "Your shape " + " and ".join(parts) + ". The planted faults are listed at the top of part-b/test-orders.ttl."


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "my_shapes.ttl"
    try:
        mine = Graph().parse(path)
    except Exception as e:  # a Turtle syntax error: say where
        sys.exit(f"{path.name} is not valid Turtle yet: {e}")
    data = Graph().parse(HERE / "part-b" / "test-orders.ttl")
    orders = {s for c in (URIRef("https://ul.edu.lb/kr/scm#Order"), URIRef("https://ul.edu.lb/kr/scm#LateOrder"))
              for s in data.subjects(RDF.type, c)}
    right = 0
    for y in EXPECTED:
        shape = MY[f"{y}Shape"]
        one = Graph()
        closure(mine, shape, one)
        closure(mine, ONTO, one)
        if not any(p in CONSTRAINTS for p in one.predicates(shape)):
            print(f"{y}  not yet: not written yet (the shape has a target but no constraint).")
            continue
        targets = list(one.objects(shape, SH.targetClass))
        reached = {s for t in targets for s in data.subjects(RDF.type, t)} | set(one.objects(shape, SH.targetNode))
        if not reached & orders:
            print(f"{y}  not yet: your shape targets no order, so it checks nothing. Keep sh:targetClass ul:Order.")
            continue
        try:
            _, report, _ = validate(data, shacl_graph=one, inference="none", advanced=True)
        except Exception as e:
            print(f"{y}  not yet: the shape does not run: {str(e).splitlines()[0][:200]}")
            continue
        got = {str(report.value(r, SH.focusNode)).replace(ORDER, "")
               for r in report.subjects(RDF.type, SH.ValidationResult)}
        if got == EXPECTED[y]:
            right += 1
            print(f"{y}  right: flags exactly {', '.join(sorted(got))}.")
        else:
            print(f"{y}  not yet: {hint(y, got)}")
    print(f"\n{right} of {len(EXPECTED)} right.")


if __name__ == "__main__":
    main()
