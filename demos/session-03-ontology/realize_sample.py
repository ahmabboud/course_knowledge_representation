"""Ask ELK which classes the sample shipments belong to, twice: with At-risk
shipment as a defined class (EquivalentTo, as shipped) and as a primitive
class (the same axiom turned into SubClassOf). This produces the table on
the slide "SubClassOf and EquivalentTo".

    python realize_sample.py                 # robot on PATH, or robot.jar next to this script
    python realize_sample.py --jar ~/tools/robot.jar

Run from demos/session-03-ontology/, after fetch_ontologies.py. Needs ROBOT
and a JDK, like robot_report.py. Writes reference-outputs/realized-sample.txt.
"""

import argparse
import subprocess
import tempfile
from pathlib import Path

from rdflib import OWL, RDF, RDFS, Graph, URIRef

import local_reasoner as lr
from robot_report import find_robot

HERE = Path(__file__).resolve().parent
AT_RISK = URIRef(lr.UL + "AtRiskShipment")


def realize(robot, merged, out):
    """ELK, inferred class assertions only; returns {individual label: [class labels]}."""
    subprocess.run(robot + ["reason", "--input", str(merged), "--reasoner", "ELK",
                            "--axiom-generators", "ClassAssertion", "--output", str(out)], check=True)
    g = Graph()
    g.parse(out, format="xml" if out.suffix == ".owl" else "turtle")

    def name(x):
        return str(g.value(x, RDFS.label) or str(x).rsplit("#", 1)[-1])
    result = {}
    for ind in set(g.subjects(RDF.type, OWL.NamedIndividual)):
        if "/kr/id/" in str(ind):
            result[name(ind)] = sorted(name(c) for c in g.objects(ind, RDF.type)
                                       if c != OWL.NamedIndividual)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", default=None, help="path to robot.jar if robot is not on PATH")
    robot = find_robot(parser.parse_args().jar)
    tmp = Path(tempfile.mkdtemp())

    shipped = lr.merged_graph(HERE / "workspace" / "sample-shipments.ttl")
    shipped.serialize(tmp / "shipped.ttl", format="turtle")
    primitive = Graph()
    primitive += shipped
    for cls in list(primitive.objects(AT_RISK, OWL.equivalentClass)):
        primitive.remove((AT_RISK, OWL.equivalentClass, cls))
        primitive.add((AT_RISK, RDFS.subClassOf, cls))
    primitive.serialize(tmp / "primitive.ttl", format="turtle")

    lines = ["ROBOT reason, ELK, inferred class assertions (direct types) for the sample shipments."]
    for title, src in (("At-risk shipment as EquivalentTo (as shipped)", tmp / "shipped.ttl"),
                       ("At-risk shipment as SubClassOf (primitive)", tmp / "primitive.ttl")):
        lines.append(f"\n{title}:")
        for ind, classes in sorted(realize(robot, src, tmp / ("out-" + src.name)).items()):
            lines.append(f"  {ind}: {', '.join(classes)}")
    text = "\n".join(lines)
    print(text)
    (HERE / "reference-outputs").mkdir(exist_ok=True)
    (HERE / "reference-outputs" / "realized-sample.txt").write_text(text + "\n")


if __name__ == "__main__":
    main()
