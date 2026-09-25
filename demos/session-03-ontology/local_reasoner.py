"""Run the HermiT reasoner on one of this lab's files, fully offline.

Protégé and ROBOT find the imported ontologies (SCRO, IOF Core, BFO) through
workspace/catalog-v001.xml. This module does the same by hand: it follows
every owl:imports through that catalog, merges everything into one graph,
and hands it to HermiT (bundled with owlready2; it needs the JDK from the
Session 1 setup). check_my_axioms.py uses it, and so can you:

    python local_reasoner.py workspace/scro-extension-v0.ttl
    python local_reasoner.py workspace/sample-shipments.ttl

Run from demos/session-03-ontology/, after fetch_ontologies.py.
"""

import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from rdflib import OWL, Graph

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE / "workspace"
CATALOG = WORKSPACE / "catalog-v001.xml"
UL = "https://ul.edu.lb/kr/scm#"


def catalog_map(catalog=CATALOG):
    """IRI -> local file, read from the Protégé catalog (and the catalogs it names)."""
    ns = {"c": "urn:oasis:names:tc:entity:xmlns:xml:catalog"}
    found, todo, seen = {}, [catalog], set()
    while todo:
        cat = todo.pop()
        if cat in seen or not cat.exists():
            continue
        seen.add(cat)
        root = ET.parse(cat).getroot()
        for u in root.iter("{%s}uri" % ns["c"]):
            found.setdefault(u.get("name"), (cat.parent / u.get("uri")).resolve())
        for n in root.iter("{%s}nextCatalog" % ns["c"]):
            todo.append((cat.parent / n.get("catalog")).resolve())
    return found


def _parse(g, path):
    fmt = "turtle" if path.suffix == ".ttl" else "xml"
    g.parse(path, format=fmt)


def merged_graph(start):
    """One graph holding the start file and everything it imports, with no owl:imports left."""
    cmap = catalog_map()
    g, todo, done = Graph(), [Path(start).resolve()], set()
    while todo:
        path = todo.pop()
        if path in done:
            continue
        done.add(path)
        part = Graph()
        _parse(part, path)
        for _, _, imp in part.triples((None, OWL.imports, None)):
            key = str(imp)
            target = cmap.get(key) or cmap.get(key.rstrip("/#")) or cmap.get(key + "/")
            if target is None:
                raise SystemExit(f"Import not found in the catalog: {key}. Run python fetch_ontologies.py first.")
            todo.append(target)
        part.remove((None, OWL.imports, None))
        g += part
    return g


def reason(start):
    """Load the start file with its imports into owlready2, run HermiT, return the world."""
    import owlready2
    g = merged_graph(start)
    tmp = Path(tempfile.mkdtemp()) / "merged.nt"
    g.serialize(tmp, format="nt", encoding="utf-8")
    world = owlready2.World()
    onto = world.get_ontology(tmp.as_uri()).load()
    try:
        with onto:
            owlready2.sync_reasoner_hermit(world, infer_property_values=False, debug=0)
    except owlready2.OwlReadyInconsistentOntologyError:
        world.inconsistent = True
        return world
    world.inconsistent = False
    return world


def label(entity):
    """The English label if there is one, else the IRI's last part."""
    for lab in entity.label:
        return str(lab)
    return entity.iri.rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def summary(world):
    """Impossible classes of ours, and the inferred classes of every individual of ours."""
    if world.inconsistent:
        return {"inconsistent": True, "impossible": [], "types": {}}
    impossible = sorted(label(c) for c in world.inconsistent_classes()
                        if c.iri.startswith(UL))
    types = {}
    for ind in world.individuals():
        if ind.iri.startswith(UL) or "/kr/id/" in ind.iri:
            types[label(ind)] = sorted(label(c) for c in ind.is_a if hasattr(c, "iri"))
    return {"inconsistent": False, "impossible": impossible, "types": types}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    s = summary(reason(sys.argv[1]))
    if s["inconsistent"]:
        print("The ontology is inconsistent: it contradicts itself, so every answer is worthless.")
    print("Impossible classes (equivalent to owl:Nothing):", ", ".join(s["impossible"]) or "none")
    for name, cls in sorted(s["types"].items()):
        print(f"  {name}: {', '.join(cls)}")
