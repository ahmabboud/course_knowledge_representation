"""Materialize: run the R2RML mapping over the database with Morph-KGC and
write every triple it produces to a file.

    python materialize.py                  # PostgreSQL, writes brunel-mapped.nt
    python materialize.py --sqlite         # the brunel.db file instead
    python materialize.py --mapping my_mapping.ttl --out my-mapped.nt

Run from demos/session-05-integration/ with demos/.venv active, after
load_database.py. Morph-KGC comes from demos/requirements-nodeps.txt.

"Materialize" means: read the tables once, now, and store the resulting
graph. The file is a snapshot; if the database changes, run this again.
Compare ontop/, which answers queries from the database directly.
"""

import argparse
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
POSTGRES_URL = "postgresql+psycopg2://kr:kr-labs-pw@127.0.0.1:5432/brunel"


def config(mapping, db_url):
    return (f"[CONFIGURATION]\nlogging_level=WARNING\n\n"
            f"[Brunel]\nmappings={mapping}\ndb_url={db_url}\n")


def run(mapping, sqlite, out):
    try:
        import morph_kgc
    except ImportError:
        sys.exit("Morph-KGC is not installed. In demos/, with .venv active, run:\n"
                 "  python -m pip install --no-deps -r requirements-nodeps.txt")
    if sqlite and not (HERE / "brunel.db").exists():
        sys.exit("brunel.db not found: run python load_database.py --sqlite first.")
    db_url = f"sqlite:///{HERE / 'brunel.db'}" if sqlite else POSTGRES_URL
    t0 = time.time()
    try:
        graph = morph_kgc.materialize(config(mapping, db_url))
    except Exception as e:
        if not sqlite and ("Connection refused" in str(e) or "could not connect" in str(e).lower()):
            sys.exit("PostgreSQL is not answering on 127.0.0.1:5432. Start it with `docker compose up -d`, "
                     "or use --sqlite.")
        raise
    secs = time.time() - t0
    graph.serialize(out, format="nt", encoding="utf-8")
    return secs, len(graph)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sqlite", action="store_true", help="read brunel.db instead of PostgreSQL")
    ap.add_argument("--mapping", default=str(HERE / "brunel-mapping.ttl"))
    ap.add_argument("--out", default=str(HERE / "brunel-mapped.nt"))
    args = ap.parse_args()
    secs, n = run(args.mapping, args.sqlite, args.out)
    print(f"{Path(args.mapping).name} over {'brunel.db' if args.sqlite else 'PostgreSQL'}: "
          f"{n:,} triples in {secs:.1f} s -> {Path(args.out).name}")


if __name__ == "__main__":
    main()
