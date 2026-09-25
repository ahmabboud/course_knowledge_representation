"""The same fact, two worlds: a database refuses it, OWL learns from it.

    python closed_world_demo.py

The slide "Domain and range infer, they do not reject" shows this run. A
relational database with a foreign key refuses a "handled by" row for a
shipment it has never heard of. OWL does the opposite: the domain of
ul:handledBy is Shipment, so the reasoner concludes the unknown thing is a
Shipment (see sample-shipments.ttl, the shipment of order 1447311670.7).
Only the Python standard library is needed. Output also goes to
reference-outputs/closed-world-demo.txt.
"""

import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    lines = [f"SQLite {sqlite3.sqlite_version}, foreign keys on"]
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("CREATE TABLE shipment (id TEXT PRIMARY KEY)")
    db.execute("CREATE TABLE carrier (id TEXT PRIMARY KEY)")
    db.execute("CREATE TABLE handled_by (shipment TEXT REFERENCES shipment(id), "
               "carrier TEXT REFERENCES carrier(id))")
    db.execute("INSERT INTO shipment VALUES ('1447291369.7')")
    db.execute("INSERT INTO carrier VALUES ('V444_1')")
    db.execute("INSERT INTO handled_by VALUES ('1447291369.7', 'V444_1')")
    lines.append("known shipment 1447291369.7, carrier V444_1: row accepted")

    # The shipment of order 1447311670.7 is not in the shipment table.
    stmt = "INSERT INTO handled_by VALUES ('1447311670.7', 'V444_1')"
    lines.append(stmt)
    try:
        db.execute(stmt)
        lines.append("accepted")
    except sqlite3.IntegrityError as err:
        lines.append(f"IntegrityError: {err}")
    lines.append("OWL, same fact: nothing is refused; the domain of ul:handledBy makes "
                 "the shipment a Shipment (sample-shipments.ttl).")

    text = "\n".join(lines)
    print(text)
    (HERE / "reference-outputs").mkdir(exist_ok=True)
    (HERE / "reference-outputs" / "closed-world-demo.txt").write_text(text + "\n")


if __name__ == "__main__":
    main()
