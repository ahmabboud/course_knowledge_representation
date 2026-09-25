"""Load the four Brunel tables Session 2 converted into a relational
database: the "live operational database" of Session 5.

    python load_database.py            # PostgreSQL from docker-compose.yml
    python load_database.py --sqlite   # no Docker: a file, brunel.db, here

Run from demos/session-05-integration/ with demos/.venv active.

Tables (one per CSV, columns renamed to lower case with underscores):
  orders              OrderList.csv          9,215 rows, key order_id
  plant_ports         PlantPorts.csv            22 rows
  products_per_plant  ProductsPerPlant.csv   2,036 rows
  freight_rates       FreightRates.csv       1,540 rows, plus rate_id: the
                      row number, because the source has no key of its own
Keys and decimal numbers are loaded exactly as the CSV writes them (as text,
so 1447296446.7 stays 1447296446.7 and a weight keeps all its digits); the
mapping gives them their datatype. Loading again replaces the tables.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from common.data_paths import BRUNEL_TABLES  # noqa: E402

POSTGRES_URL = "postgresql+psycopg2://kr:kr-labs-pw@127.0.0.1:5432/brunel"
SQLITE_URL = f"sqlite:///{HERE / 'brunel.db'}"
TABLES = {"orders": "order_list", "plant_ports": "plant_ports",
          "products_per_plant": "products_per_plant", "freight_rates": "freight_rates"}
# Keys, and decimal numbers, are kept exactly as the CSV writes them. Read as
# floating point, 329 weights and 21 rate band values would change in their
# 16th or 17th digit, and the graph would no longer equal Session 2's.
TEXT_COLUMNS = {"Order ID": str, "Product ID": str, "Weight": str,
                "minm_wgh_qty": str, "max_wgh_qty": str, "rate": str}


def frame(key):
    df = pd.read_csv(BRUNEL_TABLES[key], dtype=TEXT_COLUMNS)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    if key == "freight_rates":
        df.insert(0, "rate_id", range(1, len(df) + 1))
    return df


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sqlite", action="store_true", help="write brunel.db here instead of using PostgreSQL")
    url = SQLITE_URL if ap.parse_args().sqlite else POSTGRES_URL
    try:
        engine = create_engine(url)
        with engine.connect() as c:
            c.execute(text("SELECT 1"))
    except Exception:
        sys.exit("PostgreSQL is not answering on 127.0.0.1:5432. Start it with `docker compose up -d` "
                 "in this folder, or run `python load_database.py --sqlite` to use a file instead.")
    for table, key in TABLES.items():
        df = frame(key)
        df.to_sql(table, engine, if_exists="replace", index=False)
        print(f"{table:<19} {len(df):>6,} rows  from {BRUNEL_TABLES[key].name}")
    print(f"\nloaded into {url.split('@')[-1] if '@' in url else 'brunel.db'}")


if __name__ == "__main__":
    main()
