"""Load the same Brunel orders into Neo4j and ask the Session 2 questions in
Cypher, next to their SPARQL versions. The point is to see the differences,
not to score one against the other.

Start Neo4j first: `docker compose up -d` from demos/ (user neo4j, password
kr-labs-pw). Run from demos/session-02-rdf-sparql/:  python neo4j_comparison.py
Output also goes to reference-outputs/neo4j-comparison.txt.
"""

import sys
import time
from pathlib import Path

import pandas as pd
from neo4j import GraphDatabase

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.data_paths import BRUNEL_TABLES  # noqa: E402

NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "kr-labs-pw")
HERE = Path(__file__).resolve().parent

LOAD_SIMPLE = """
UNWIND $rows AS r
FOREACH (_ IN CASE WHEN r.late > 0 THEN [1] ELSE [] END | MERGE (:LateOrder {id: r.id}))
FOREACH (_ IN CASE WHEN r.late = 0 THEN [1] ELSE [] END | MERGE (:Order {id: r.id}))
WITH r
MATCH (o {id: r.id})
SET o.name = r.id, o.weight = r.weight, o.service = r.service, o.lateDays = r.late
MERGE (p:Plant {id: r.plant})     MERGE (o)-[:FROM_PLANT]->(p)
MERGE (f:Port {id: r.origin})     MERGE (o)-[:SHIPS_FROM]->(f)
MERGE (c:Carrier {id: r.carrier}) MERGE (o)-[:CARRIED_BY]->(c)
"""
LINKS = """
UNWIND $rows AS r
MERGE (p:Plant {id: r.plant}) MERGE (t:Port {id: r.port}) MERGE (p)-[:SERVES_PORT]->(t)
"""

QUESTIONS = [
    ("Q2 · orders and late orders per carrier",
     """MATCH (o)-[:CARRIED_BY]->(c:Carrier)
        RETURN c.id AS carrier, count(o) AS orders, sum(CASE WHEN o.lateDays > 0 THEN 1 ELSE 0 END) AS lateOrders
        ORDER BY orders DESC"""),
    ("Q4 · any order leaving through a port its plant does not serve?",
     """MATCH (o)-[:SHIPS_FROM]->(port:Port), (o)-[:FROM_PLANT]->(p:Plant)
        WHERE NOT (p)-[:SERVES_PORT]->(port)
        RETURN count(o) > 0 AS answer"""),
    ("Q5a · MATCH (o:Order): the label alone",
     """MATCH (o:Order) RETURN count(o) AS orders"""),
    ("Q5b · every kind of order: the hierarchy must be written into the query",
     """MATCH (o) WHERE o:Order OR o:LateOrder RETURN count(o) AS orders"""),
    ("Path of any length, Cypher's counterpart to SPARQL's +",
     """MATCH (o:Order {id: '1447296446.7'})-[*1..3]->(n) RETURN count(DISTINCT n) AS reachable"""),
]


def main():
    orders = pd.read_csv(BRUNEL_TABLES["order_list"], dtype={"Order ID": str})
    rows = [{"id": r["Order ID"], "plant": r["Plant Code"], "origin": r["Origin Port"],
             "carrier": r["Carrier"], "service": r["Service Level"], "weight": float(r["Weight"]),
             "late": int(r["Ship Late Day count"])} for _, r in orders.iterrows()]
    links = [{"plant": r["Plant Code"], "port": r["Port"]}
             for _, r in pd.read_csv(BRUNEL_TABLES["plant_ports"]).iterrows()]
    lines = []
    driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
    with driver.session() as s:
        s.run("MATCH (n) DETACH DELETE n").consume()
        for label in ("Order", "LateOrder", "Plant", "Port", "Carrier"):
            s.run(f"CREATE INDEX IF NOT EXISTS FOR (n:{label}) ON (n.id)").consume()
        start = time.perf_counter()
        for i in range(0, len(rows), 1000):
            s.run(LOAD_SIMPLE, rows=rows[i:i + 1000]).consume()
        s.run(LINKS, rows=links).consume()
        lines.append(f"Loaded {len(rows)} orders and {len(links)} plant to port links "
                     f"in {time.perf_counter() - start:.1f} s")
        for label, cypher in QUESTIONS:
            s.run(cypher).consume()  # warm up once, then time
            start = time.perf_counter()
            records = list(s.run(cypher))
            ms = (time.perf_counter() - start) * 1000
            lines.append(f"[{label}] {len(records)} rows in {ms:.1f} ms")
            lines.extend(f"    {dict(r)}" for r in records[:4])
    driver.close()
    text = "\n".join(lines)
    print(text)
    (HERE / "reference-outputs").mkdir(exist_ok=True)
    (HERE / "reference-outputs" / "neo4j-comparison.txt").write_text(text + "\n")


if __name__ == "__main__":
    from neo4j.exceptions import AuthError, ServiceUnavailable
    try:
        main()
    except ServiceUnavailable:
        raise SystemExit("Neo4j is not answering on localhost:7687. Start it from demos/ with "
                         "`docker compose up -d`. This step is optional: every other step works without it.")
    except AuthError:
        raise SystemExit("Neo4j refused the course password (neo4j / kr-labs-pw). The Neo4j on port 7687 "
                         "is not the course's container, or its data volume was created with another "
                         "password. See the README, 'If Neo4j refuses the password'.")
