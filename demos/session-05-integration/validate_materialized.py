"""Validate materialized.nt against Session 4's shapes.

Not a plain `python3 -m pyshacl ...` call, on purpose: Morph-KGC's
N-TRIPLES output carries no prefix declarations at all, so rdflib
parses it with its own auto-generated prefix (ns1:, typically) for the
ul: namespace. The shapes file's `sh:prefixes ul:` SPARQLConstraint
then fails to resolve with "Unknown namespace prefix: ul", every time,
not intermittently, this is not a fallback path. Binding the prefix
explicitly on the data graph before validating, as below, is the fix,
confirmed against real pyshacl 0.40.1 output while building this lab.

Run from this folder, in the repository's shared venv (pyshacl is
already a shared dependency, Session 4 onward):
    python3 validate_materialized.py
"""

import rdflib
import pyshacl

DATA = "materialized.nt"
SHAPES = "../session-04-shacl/shapes_template.ttl"
NAMESPACE = "https://ul.edu.lb/kr/scm#"


def main():
    data = rdflib.Graph()
    data.parse(DATA, format="nt")
    data.bind("ul", NAMESPACE)

    shapes = rdflib.Graph()
    shapes.parse(SHAPES, format="turtle")

    conforms, _, report = pyshacl.validate(data, shacl_graph=shapes)
    print(report)
    print(f"Conforms: {conforms}")


if __name__ == "__main__":
    main()
