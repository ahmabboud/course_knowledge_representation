"""Release the Session 3 ontology as version 1.0.0: add an owl:versionIRI and
an owl:versionInfo to its header, and write the release as a new file.

    python version_ontology.py            # writes workspace/scro-extension-1.0.0.ttl

Run from demos/session-04-shacl/. The Session 3 file itself is not changed.

Why: the ontology IRI (https://ul.edu.lb/kr/scm#) names the ontology across
all its versions; the version IRI names this one release. A team that
imports the ontology can import the version IRI instead, and so pin exactly
the release it validated against. A new release gets a new version IRI and
points back with owl:priorVersion.
"""

from pathlib import Path

from rdflib import OWL, Graph, URIRef

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "session-03-ontology" / "scro-extension-reference.ttl"
VERSION = "1.0.0"
VERSION_IRI = f"https://ul.edu.lb/kr/scm/{VERSION}"
HEADER = "<https://ul.edu.lb/kr/scm#> a owl:Ontology ;\n"


def main():
    text = SOURCE.read_text(encoding="utf-8")
    if text.count(HEADER) != 1:
        raise SystemExit("Could not find the ontology header in " + SOURCE.name)
    release = text.replace(HEADER, HEADER + f'    owl:versionIRI <{VERSION_IRI}> ;\n'
                                           f'    owl:versionInfo "{VERSION}" ;\n')
    out = HERE / "workspace" / f"scro-extension-{VERSION}.ttl"
    out.parent.mkdir(exist_ok=True)
    out.write_text(release, encoding="utf-8")

    before, after = Graph().parse(SOURCE), Graph().parse(out)
    onto = URIRef("https://ul.edu.lb/kr/scm#")
    print(f"{SOURCE.name}: {len(before)} triples, version IRI: {before.value(onto, OWL.versionIRI)}")
    print(f"{out.relative_to(HERE)}: {len(after)} triples, version IRI: {after.value(onto, OWL.versionIRI)}, "
          f"version info: {after.value(onto, OWL.versionInfo)}")
    print("\nThe new header:")
    start = release.index(HEADER)
    print(release[start: release.index(" .\n", start) + 2])


if __name__ == "__main__":
    main()
