"""Virtualize: ask Ontop a SPARQL question. Ontop turns it into SQL, runs the
SQL on PostgreSQL, and turns the rows back into answers. No graph is stored.

    python ontop/run_ontop.py                        # Session 2's Q2
    python ontop/run_ontop.py --query my-question.sparql

Run from demos/session-05-integration/, after `docker compose up -d`,
`python load_database.py` and `python ontop/setup_ontop.py`.
Prints the answers and the SQL Ontop sent to the database, and keeps the
whole log in ontop/last-run.log.

No Docker or no Java? Read reference-outputs/ontop-q2.txt: the same run,
recorded on the instructor's machine.
"""

import argparse
import os
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
CLI = HERE / "ontop-cli" / ("ontop.bat" if platform.system() == "Windows" else "ontop")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--query", default=str(HERE / "q2-orders-per-carrier.sparql"))
    args = ap.parse_args()
    if not CLI.exists():
        sys.exit("Ontop is not installed yet: run python ontop/setup_ontop.py first. "
                 "No Java or Docker? Read reference-outputs/ontop-q2.txt instead.")
    # Ontop's command line inconsistently treats these inputs as file paths
    # and URIs.  Relative paths avoid both interpretations of the spaces in
    # the course's macOS location ("Mobile Documents").
    relative = lambda path: os.path.relpath(Path(path).resolve(), LAB)
    with tempfile.NamedTemporaryFile(prefix="ontop-results-", suffix=".csv", delete=False) as output:
        output_path = Path(output.name)
    cmd = [str(CLI), "query", "-m", "brunel-mapping.ttl", "-t", "vocabulary.ttl",
           "-p", "ontop/brunel.properties", "-q", relative(args.query),
           "-o", str(output_path)]
    env = dict(os.environ, ONTOP_LOG_LEVEL="DEBUG")
    try:
        run = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=LAB)
        log = run.stdout + "\n" + run.stderr
        (HERE / "last-run.log").write_text(log, encoding="utf-8")
        if run.returncode != 0 or "Exception:" in log:
            if "Connection refused" in log or "Operation not permitted" in log:
                sys.exit("PostgreSQL is not answering on 127.0.0.1:5432: run `docker compose up -d` and "
                         "`python load_database.py`.")
            sys.exit(f"Ontop stopped with code {run.returncode}; the full log is ontop/last-run.log.")
        answers = output_path.read_text(encoding="utf-8").splitlines()
    finally:
        output_path.unlink(missing_ok=True)
    print("Answers (CSV):")
    for line in answers:
        print("  " + line)
    sql = re.findall(r"(?is)(SELECT\s.+?)(?:\n\s*\n|\n\d\d:\d\d:\d\d)", log)
    sql = [s for s in sql if "FROM" in s.upper() and "orders" in s.lower()]
    print("\nThe SQL Ontop sent to PostgreSQL:" if sql else "\nNo SQL found in the log; see ontop/last-run.log.")
    if sql:
        print(max(sql, key=len).strip())


if __name__ == "__main__":
    main()
