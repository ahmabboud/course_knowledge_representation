"""Count the triples in each named graph of brunel.trig, and find the graph
the rate bands live in. These are the numbers on the named graphs slide.

    python named_graphs.py      (after convert_to_rdf.py; Oxigraph, no Docker)

Fuseki's lab dataset holds brunel.ttl, one graph with no names, so this
runs on Oxigraph, which loads the named graphs from brunel.trig.
Output also goes to reference-outputs/named-graphs-oxigraph.txt.
"""

import time
from pathlib import Path

import pyoxigraph

HERE = Path(__file__).resolve().parent

PER_GRAPH = """
SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } }
GROUP BY ?g ORDER BY DESC(?n)
"""
BANDS_LIVE_IN = """
PREFIX ul: <https://ul.edu.lb/kr/scm#>
SELECT DISTINCT ?g WHERE { GRAPH ?g { ?band a ul:RateBand } }
"""


def main():
    """Load the named graphs, run both queries, print and record the result."""
    store = pyoxigraph.Store()
    store.load(path=str(HERE / "brunel.trig"), format=pyoxigraph.RdfFormat.TRIG)

    start = time.perf_counter()
    rows = [(sol["g"].value, sol["n"].value) for sol in store.query(PER_GRAPH)]
    ms = (time.perf_counter() - start) * 1000
    lines = [f"[named graphs: triples per source table] {len(rows)} rows in {ms:.1f} ms"]
    lines += [f"    {g} {n}" for g, n in rows]
    for sol in store.query(BANDS_LIVE_IN):
        lines.append(f"   rate bands live in: {sol['g'].value}")

    text = "\n".join(lines)
    print(text)
    out = HERE / "reference-outputs"
    out.mkdir(exist_ok=True)
    (out / "named-graphs-oxigraph.txt").write_text(text + "\n")


if __name__ == "__main__":
    main()
