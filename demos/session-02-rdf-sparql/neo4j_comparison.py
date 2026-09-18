"""Load the same Brunel slice into Neo4j and run the equivalent
multi-hop Cypher query, for the side-by-side comparison the lecture's
closing segment uses. Not scored against SPARQL, the point is to show
the differences, per the lecture notes.
"""

import csv
from pathlib import Path

from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "kr-labs-pw")

BRUNEL_ORDER_LIST = Path(__file__).resolve().parents[1] / "data" / "brunel" / "OrderList.csv"


def load(tx, rows):
    for row in rows:
        tx.run(
            """
            MERGE (o:Order {id: $order_id})
            MERGE (p:Plant {id: $plant_id})
            MERGE (o)-[:FROM_PLANT]->(p)
            """,
            order_id=row["Order ID"],
            plant_id=row["Origin Port"],
        )


def multi_hop_query(tx):
    # The Cypher equivalent of queries.sparql's property-path question,
    # once a multi-hop relation exists in the slice (see that file's Q4
    # note). Cypher's variable-length path syntax, [:HAS_COMPONENT*1..],
    # is the direct counterpart to SPARQL's `+`.
    result = tx.run(
        """
        MATCH (good)-[:HAS_COMPONENT*1..]->(part)
        RETURN good.id AS good, part.id AS part
        LIMIT 20
        """
    )
    return list(result)


def main():
    with open(BRUNEL_ORDER_LIST) as f:
        rows = list(csv.DictReader(f))[:200]

    driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
    with driver.session() as session:
        session.execute_write(load, rows)
        print(f"Loaded {len(rows)} orders into Neo4j.")
        # Uncomment once HAS_COMPONENT relationships exist in the slice:
        # rows = session.execute_read(multi_hop_query)
        # for r in rows:
        #     print(r)
    driver.close()


if __name__ == "__main__":
    main()
