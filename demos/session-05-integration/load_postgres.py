"""Create the schema and load a small purchase-order and carrier seed
into Session 5's Postgres container.

The rows are a small, hand-built set, not the full Kaggle DataCo CSV
(that download needs a Kaggle account and token, see data/README.md)
or the full Brunel CSVs (their direct Figshare download has been
unreliable from this repository's own tooling; see the note in
data/fetch_data.py). The columns are shaped the same way the real
datasets are: an order with dispatch and delivery dates plus a carrier
foreign key, the kind of row DataCo's order-level fields and Brunel's
FreightRates carrier field would together produce once joined. Swap
this loader's INSERT statements for real rows pulled from data/dataco/
and data/brunel/ once those are fetched, the schema and every
downstream mapping stay the same.

Run once, after `docker compose up -d` in this folder:
    python3 -m venv .venv-pg && source .venv-pg/bin/activate
    pip install psycopg2-binary
    python3 load_postgres.py

A separate small venv, not the repository's shared one, on purpose:
morph-kgc (below) pins rdflib<7.3.0, pyshacl (already in the shared
requirements.txt) needs rdflib>=7.3.0. The two cannot live in one
environment. See mapping_template.rml.ttl's own note for the rest of
that story.
"""

import psycopg2

DSN = "postgresql://kr:kr-labs-pw@localhost:5432/dataco"

SCHEMA = """
CREATE TABLE IF NOT EXISTS carriers (
    carrier_code TEXT PRIMARY KEY,
    carrier_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    po_id TEXT PRIMARY KEY,
    carrier_code TEXT REFERENCES carriers(carrier_code),
    dispatch_date DATE NOT NULL,
    delivery_date DATE NOT NULL
);
"""

# Two carriers this round, DHL Express actually serving orders and a
# second, unused one, so the mapping has more than one real row to
# join against.
CARRIERS = [
    ("dhl", "DHL Express"),
    ("aramex", "Aramex"),
]

# po99 carries the same lesson as Session 4's example: its real-world
# carrier code ("untracked") never appears in the carriers table. The
# foreign key constraint means Postgres itself would reject an unknown
# code outright, so it is loaded as NULL here to keep the row
# insertable, the RML mapping's join condition treats a NULL carrier
# code exactly the way it treats an orphan string value: no
# ul:hasCarrier triple comes out either way, and that silent gap is
# the whole point of Part 3 of the lecture.
PURCHASE_ORDERS = [
    ("po88", "dhl", "2026-03-10", "2026-03-14"),
    ("po99", None, "2026-03-20", "2026-03-18"),
    ("po101", "dhl", "2026-04-01", "2026-04-05"),
    ("po104", "aramex", "2026-04-03", "2026-04-06"),
]


def load():
    conn = psycopg2.connect(DSN)
    try:
        with conn, conn.cursor() as cur:
            cur.execute(SCHEMA)
            cur.executemany(
                "INSERT INTO carriers (carrier_code, carrier_name) VALUES (%s, %s) "
                "ON CONFLICT (carrier_code) DO UPDATE SET carrier_name = EXCLUDED.carrier_name",
                CARRIERS,
            )
            cur.executemany(
                "INSERT INTO purchase_orders (po_id, carrier_code, dispatch_date, delivery_date) "
                "VALUES (%s, %s, %s, %s) ON CONFLICT (po_id) DO UPDATE SET "
                "carrier_code = EXCLUDED.carrier_code, dispatch_date = EXCLUDED.dispatch_date, "
                "delivery_date = EXCLUDED.delivery_date",
                PURCHASE_ORDERS,
            )
    finally:
        conn.close()
    print(f"Loaded {len(CARRIERS)} carriers and {len(PURCHASE_ORDERS)} purchase orders.")


def confirm():
    conn = psycopg2.connect(DSN)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM purchase_orders WHERE carrier_code IS NULL")
            (orphans,) = cur.fetchone()
            cur.execute("SELECT count(*) FROM purchase_orders")
            (total,) = cur.fetchone()
    finally:
        conn.close()
    print(f"{total} purchase orders in Postgres, {orphans} with no resolvable carrier.")


if __name__ == "__main__":
    load()
    confirm()
