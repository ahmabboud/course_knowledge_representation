"""Check the queries you wrote in my_queries.sparql.

    python check_my_queries.py            # Oxigraph, inside Python (no Docker)
    python check_my_queries.py fuseki     # your Fuseki, loaded by load_fuseki.py

Your query is right when it returns the same answer as the real data,
whatever way you wrote it. Only values are compared: column names, column
order and, where the question does not ask for an order, row order do not
matter.
Run from demos/session-02-rdf-sparql/, after convert_to_rdf.py.
"""

import sys
from pathlib import Path

import requests

from run_queries import FUSEKI_DOWN, fuseki, oxigraph, oxigraph_store

HERE = Path(__file__).resolve().parent

# The reference answers (2026-09-24 run). IRIs are compared by their last part,
# so PLANT03 stands for https://ul.edu.lb/kr/id/plant/brunel/PLANT03.
EXPECTED = {
    "Y1": [("PLANT03", "8541"), ("PLANT12", "300"), ("PLANT16", "173"), ("PLANT08", "102"),
           ("PLANT13", "86"), ("PLANT09", "12"), ("PLANT04", "1")],
    "Y2": [("PORT01",), ("PORT02",), ("PORT03",), ("PORT06",), ("PORT07",), ("PORT08",),
           ("PORT10",), ("PORT11",)],
    "Y3": [("16",)],
}
ORDERED = {"Y1"}  # the question asks for largest first
WORKED = {"Y1"}  # shown in full before the student writes Y2 and Y3
HINTS = {
    "Y1": "One pattern, ?order ul:fromPlant ?plant, then GROUP BY ?plant and ORDER BY DESC.",
    "Y2": "Start from ?plant ul:servesPort ?port; drop ports that appear in ?order ul:shipsFrom ?port. "
          "Duplicates? Use DISTINCT.",
    "Y3": "Group orders by customer, keep groups with more than one distinct plant (HAVING), "
          "then count those customers in an outer SELECT.",
}


def short(value):
    """Last part of an IRI, or the literal as text."""
    return str(value).rstrip("/").rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def student_queries():
    """Split my_queries.sparql on its '# --- ' markers; skip unanswered ones."""
    text = (HERE / "my_queries.sparql").read_text(encoding="utf-8")
    out = {}
    for block in text.split("# --- ")[1:]:
        label, _, body = block.partition(" ---\n")
        key = label.split(" ", 1)[0]
        query = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("#")).strip()
        out[key] = query
    return out


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "oxigraph"
    store = oxigraph_store() if target == "oxigraph" else None
    right = 0
    practice_total = len(EXPECTED) - len(WORKED)
    for key, query in student_queries().items():
        if not query:
            print(f"{key}: not written yet.")
            continue
        try:
            rows = oxigraph(store, query) if store is not None else fuseki(query)
        except requests.ConnectionError:
            # Not the student's query: the server is not there.
            sys.exit(FUSEKI_DOWN.replace("run_queries.py oxigraph", "check_my_queries.py"))
        except Exception as err:  # a syntax error is the most common first result
            print(f"{key}: the query did not run: {err}")
            continue
        # Each row is compared as a set of values, so ?orders ?plant is as
        # right as ?plant ?orders.
        got = [tuple(sorted(short(v) for v in row)) for row in rows]
        want = [tuple(sorted(row)) for row in EXPECTED[key]]
        ok = got == want if key in ORDERED else sorted(got) == sorted(want)
        if ok:
            if key in WORKED:
                print(f"{key}: worked example confirmed ({len(got)} rows).")
            else:
                right += 1
                print(f"{key}: right ({len(got)} rows).")
        else:
            print(f"{key}: not yet. You returned {len(got)} rows, first ones: {got[:3]}")
            print(f"    Hint: {HINTS[key]}")
    print(f"\n{right} of {practice_total} practice queries right.")


if __name__ == "__main__":
    main()
