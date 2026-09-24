"""Run queries.sparql's question set, printing each result and its timing.

    python run_queries.py            # against Fuseki, loaded by load_fuseki.py
    python run_queries.py oxigraph   # no Java needed: pyoxigraph, in this process

Oxigraph is the documented fallback when the JDK or Docker setup fails, and
the better choice above roughly a million triples, where rdflib is slow.
Timings go to reference-outputs/query-timings-<store>.txt.
"""

import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
FUSEKI_QUERY = "http://localhost:3030/kr/sparql"
QUERIES_PATH = HERE / "queries.sparql"


def load_queries():
    """Split queries.sparql on its '# --- ' markers."""
    blocks = QUERIES_PATH.read_text().split("# --- ")[1:]
    out = []
    for block in blocks:
        label, _, rest = block.partition(" ---\n")
        out.append((label.strip(), rest.strip()))
    return out


def fuseki(query):
    construct = "\nCONSTRUCT" in "\n" + query
    accept = "application/n-triples" if construct else "application/sparql-results+json"
    r = requests.post(FUSEKI_QUERY, data={"query": query}, headers={"Accept": accept}, timeout=300)
    r.raise_for_status()
    if construct:
        return [line for line in r.text.splitlines() if line.strip()]
    j = r.json()
    if "boolean" in j:
        return [j["boolean"]]
    cols = j["head"]["vars"]
    return [tuple(b.get(c, {}).get("value") for c in cols) for b in j["results"]["bindings"]]


def oxigraph_store():
    import pyoxigraph
    store = pyoxigraph.Store()
    store.load(path=str(HERE / "brunel.ttl"), format=pyoxigraph.RdfFormat.TURTLE)
    return store


def oxigraph(store, query):
    import pyoxigraph
    res = store.query(query)
    if isinstance(res, bool) or type(res).__name__ == "QueryBoolean":
        return [bool(res)]
    if type(res).__name__ == "QueryTriples":
        return list(res)
    cols = [v.value for v in res.variables]
    return [tuple(sol[c].value if sol[c] is not None else None for c in cols) for sol in res]


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "fuseki"
    store = oxigraph_store() if target == "oxigraph" else None
    lines = []
    for label, query in load_queries():
        start = time.perf_counter()
        rows = oxigraph(store, query) if store is not None else fuseki(query)
        ms = (time.perf_counter() - start) * 1000
        lines.append(f"[{label}] {len(rows)} rows in {ms:.1f} ms")
        for row in rows[:6]:
            lines.append(f"    {row}")
    text = "\n".join(lines)
    print(text)
    out = HERE / "reference-outputs"
    out.mkdir(exist_ok=True)
    (out / f"query-timings-{target}.txt").write_text(text + "\n")


if __name__ == "__main__":
    main()
