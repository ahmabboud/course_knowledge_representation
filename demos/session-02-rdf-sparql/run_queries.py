"""Run queries.sparql's question set against the loaded endpoint,
printing each result and its timing. Switch TRIPLESTORE to "oxigraph"
if Fuseki or the JDK setup fails during the lab, per the lecture's own
fallback guidance, rather than debugging Java live in the room.
"""

import time
from pathlib import Path

from SPARQLWrapper import JSON, SPARQLWrapper

TRIPLESTORE = "fuseki"  # or "oxigraph"

FUSEKI_ENDPOINT = "http://localhost:3030/kr/sparql"
QUERIES_PATH = Path(__file__).resolve().parent / "queries.sparql"


def load_queries():
    """Split queries.sparql on its '# --- Qn' comment markers."""
    text = QUERIES_PATH.read_text()
    blocks = text.split("# --- ")[1:]
    queries = []
    for block in blocks:
        label, _, rest = block.partition("---\n")
        queries.append((label.strip(), rest.strip()))
    return queries


def run_fuseki(query: str):
    sparql = SPARQLWrapper(FUSEKI_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def run_oxigraph(query: str):
    import pyoxigraph

    store = pyoxigraph.Store("oxigraph_store")  # persisted next to this script
    return list(store.query(query))


def main():
    for label, query in load_queries():
        start = time.perf_counter()
        if TRIPLESTORE == "fuseki":
            result = run_fuseki(query)
            n_rows = len(result["results"]["bindings"])
        else:
            result = run_oxigraph(query)
            n_rows = len(result)
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"[{label}] {n_rows} rows in {elapsed_ms:.1f} ms")


if __name__ == "__main__":
    main()
