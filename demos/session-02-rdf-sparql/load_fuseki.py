"""Load brunel_slice.ttl into the running Fuseki container's `kr`
dataset, and confirm the endpoint answers.
"""

from pathlib import Path

import requests

FUSEKI_BASE = "http://localhost:3030"
DATASET = "kr"
TTL_PATH = Path(__file__).resolve().parent / "brunel_slice.ttl"


def load():
    data = TTL_PATH.read_bytes()
    resp = requests.post(
        f"{FUSEKI_BASE}/{DATASET}/data",
        data=data,
        headers={"Content-Type": "text/turtle"},
        auth=("admin", "admin"),
    )
    resp.raise_for_status()
    print(f"Loaded {TTL_PATH} into {FUSEKI_BASE}/{DATASET}")


def confirm():
    query = "SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }"
    resp = requests.get(
        f"{FUSEKI_BASE}/{DATASET}/sparql",
        params={"query": query},
        headers={"Accept": "application/sparql-results+json"},
    )
    resp.raise_for_status()
    n = resp.json()["results"]["bindings"][0]["n"]["value"]
    print(f"Endpoint answers: {n} triples loaded.")


if __name__ == "__main__":
    load()
    confirm()
