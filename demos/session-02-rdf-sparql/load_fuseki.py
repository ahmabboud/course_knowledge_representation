"""Load brunel.ttl into Fuseki's `kr` dataset (TDB2) and confirm the
endpoint answers.

Uses HTTP PUT on the default graph, so running it twice replaces the data
instead of loading every triple a second time.

Start Fuseki first: `docker compose up -d` from demos/ (Fuseki 5.5, no login),
or without Docker, from Apache's Fuseki download:
    java -jar fuseki-server.jar --tdb2 --loc=tdb2 --update /kr
"""

import time
from pathlib import Path

import requests

FUSEKI_BASE = "http://localhost:3030"
DATASET = "kr"
TTL_PATH = Path(__file__).resolve().parent / "brunel.ttl"


def load():
    start = time.perf_counter()
    resp = requests.put(
        f"{FUSEKI_BASE}/{DATASET}/data?default",
        data=TTL_PATH.read_bytes(),
        headers={"Content-Type": "text/turtle"},
        timeout=600,
    )
    resp.raise_for_status()
    print(f"Loaded {TTL_PATH.name} into {FUSEKI_BASE}/{DATASET} in {time.perf_counter() - start:.1f} s")


def confirm():
    resp = requests.get(
        f"{FUSEKI_BASE}/{DATASET}/sparql",
        params={"query": "SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }"},
        headers={"Accept": "application/sparql-results+json"},
        timeout=60,
    )
    resp.raise_for_status()
    n = resp.json()["results"]["bindings"][0]["n"]["value"]
    print(f"Endpoint answers: {n} triples loaded.")


if __name__ == "__main__":
    try:
        load()
        confirm()
    except requests.ConnectionError:
        raise SystemExit("Fuseki is not answering on http://localhost:3030. Start it from demos/ "
                         "with `docker compose up -d`, or skip this step and use Oxigraph: "
                         "python run_queries.py oxigraph")
