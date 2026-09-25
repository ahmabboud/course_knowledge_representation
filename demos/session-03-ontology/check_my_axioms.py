"""Check the axioms you wrote in my_axioms.ttl.

    python check_my_axioms.py
    python check_my_axioms.py solutions/my_axioms_solutions.ttl   (the instructor's version)

Run from demos/session-03-ontology/, after fetch_ontologies.py. The checker
never compares your text. It adds a few test classes of its own, runs the
HermiT reasoner (about 20 seconds), and asks the reasoner whether your class
means exactly what the question asks. So any correct way of writing it
passes.
"""

import sys
import tempfile
from pathlib import Path

from rdflib import Graph

import local_reasoner as lr

HERE = Path(__file__).resolve().parent

# Test classes the checker adds. Each is the meaning a question asks for, or
# a common near miss, written once here so the reasoner can compare.
PROBES = """
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ioc:  <https://spec.industrialontologies.org/ontology/construct/> .
@prefix ul:   <https://ul.edu.lb/kr/scm#> .
ul:ProbeY1 a owl:Class ; rdfs:label "probe Y1" ; rdfs:subClassOf ul:Plant , ul:Port .
ul:ProbeY2 a owl:Class ; rdfs:label "probe Y2" ; owl:equivalentClass [ owl:intersectionOf ( ul:LateShipment ul:AtRiskShipment ) ] .
ul:ProbeY3 a owl:Class ; rdfs:label "probe Y3" ; owl:equivalentClass [ owl:intersectionOf ( ioc:Shipment
    [ a owl:Restriction ; owl:onProperty ul:handledBy ; owl:someValuesFrom ul:SanctionedCarrier ]
    [ a owl:Restriction ; owl:onProperty ul:handledBy ; owl:allValuesFrom ul:SanctionedCarrier ] ) ] .
ul:ProbeY3NoSome a owl:Class ; rdfs:label "probe Y3 without some" ; owl:equivalentClass [ owl:intersectionOf ( ioc:Shipment
    [ a owl:Restriction ; owl:onProperty ul:handledBy ; owl:allValuesFrom ul:SanctionedCarrier ] ) ] .
ul:ProbeY3NoOnly a owl:Class ; rdfs:label "probe Y3 without only" ; owl:equivalentClass [ owl:intersectionOf ( ioc:Shipment
    [ a owl:Restriction ; owl:onProperty ul:handledBy ; owl:someValuesFrom ul:SanctionedCarrier ] ) ] .
"""

HINTS = {
    "Y1": "One triple: ul:Plant owl:disjointWith ul:Port .",
    "Y2": "Write ul:LateAtRiskShipment owl:equivalentClass [ owl:intersectionOf ( ... ) ] with the two classes inside.",
    "Y3": "Inside one owl:intersectionOf: ioc:Shipment, a someValuesFrom restriction and an allValuesFrom restriction on ul:handledBy.",
}


def written(path):
    """Which questions have something under their marker, not only comments."""
    text = Path(path).read_text(encoding="utf-8")
    out = {}
    for block in text.split("# --- ")[1:]:
        key = block.split(" ", 1)[0]
        body = block.partition(" ---\n")[2]
        out[key] = any(line.strip() and not line.lstrip().startswith("#") for line in body.splitlines())
    return out


def reasoned_world(path):
    """The student's file, its imports and the probes, classified by HermiT."""
    import owlready2
    g = lr.merged_graph(path)
    probes = Graph()
    probes.parse(data=PROBES, format="turtle")
    g += probes
    tmp = Path(tempfile.mkdtemp()) / "check.nt"
    g.serialize(tmp, format="nt", encoding="utf-8")
    world = owlready2.World()
    onto = world.get_ontology(tmp.as_uri()).load()
    try:
        with onto:
            owlready2.sync_reasoner_hermit(world, infer_property_values=False, debug=0)
    except owlready2.OwlReadyInconsistentOntologyError:
        return None
    return world


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else HERE / "my_axioms.ttl"
    done = written(path)
    if not any(done.values()):
        for key in ("Y1", "Y2", "Y3"):
            print(f"{key}: not written yet.")
        print("\n0 of 3 right.")
        return
    try:
        world = reasoned_world(path)
    except Exception as err:  # a Turtle typo is the most common first result
        raise SystemExit(f"Your file did not load: {err}\nCheck for a missing '.' or ';' at the end of a line.")
    if world is None:
        raise SystemExit("Your axioms make the ontology inconsistent: it now contradicts itself. "
                         "Look for an axiom that puts one thing in two disjoint classes.")

    ul = "https://ul.edu.lb/kr/scm#"
    c = {name: world[ul + name] for name in (
        "ProbeY1", "ProbeY2", "ProbeY3", "ProbeY3NoSome", "ProbeY3NoOnly",
        "LateAtRiskShipment", "SanctionedOnlyShipment")}
    impossible = set(world.inconsistent_classes())

    def below(a, b):
        """True when the reasoner concluded that every a is a b."""
        return a in impossible or b in a.ancestors()

    def same(a, b):
        return below(a, b) and below(b, a)

    results = {}
    # Y1: a thing in both classes must be impossible.
    if not done.get("Y1"):
        results["Y1"] = (False, "not written yet.")
    elif c["ProbeY1"] in impossible:
        results["Y1"] = (True, "right.")
    else:
        results["Y1"] = (False, "not yet. The reasoner still accepts something that is both a plant and a port.")

    # Y2 and Y3: the student's class must mean exactly the probe.
    for key, mine, probe in (("Y2", c["LateAtRiskShipment"], c["ProbeY2"]),
                             ("Y3", c["SanctionedOnlyShipment"], c["ProbeY3"])):
        if not done.get(key):
            results[key] = (False, "not written yet.")
        elif mine in impossible:
            results[key] = (False, "not yet. Your class can never have a member (it is equivalent to owl:Nothing).")
        elif same(mine, probe):
            results[key] = (True, "right.")
        elif below(mine, probe):
            results[key] = (False, "not yet. You wrote a one way door (SubClassOf): the reasoner will never put a "
                                   "shipment into your class by itself. Use owl:equivalentClass.")
        elif key == "Y3" and same(mine, c["ProbeY3NoSome"]):
            results[key] = (False, "not yet. only never says a carrier exists, so a shipment with no carrier at "
                                   "all gets in. Add the someValuesFrom part.")
        elif key == "Y3" and same(mine, c["ProbeY3NoOnly"]):
            results[key] = (False, "not yet. some lets in a shipment that also has a carrier that is not "
                                   "sanctioned. Add the allValuesFrom part.")
        elif below(probe, mine):
            results[key] = (False, "not yet. Your class lets in shipments the question does not ask for.")
        else:
            results[key] = (False, "not yet. Your class means something different from the question.")

    right = 0
    for key in ("Y1", "Y2", "Y3"):
        ok, msg = results[key]
        right += ok
        print(f"{key}: {msg}")
        if not ok and msg != "not written yet.":
            print(f"    Hint: {HINTS[key]}")
    print(f"\n{right} of 3 right.")


if __name__ == "__main__":
    main()
