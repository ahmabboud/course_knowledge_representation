"""Check your part B mapping (my_mapping.ttl): right, or not yet with a hint.

    python check_my_mapping.py                                  # your file
    python check_my_mapping.py solutions/my_mapping_solutions.ttl

Uses PostgreSQL if it is running, otherwise brunel.db (python load_database.py
--sqlite). Runs your mapping with Morph-KGC and compares the triples each new
rule makes with the ones it should make, computed straight from the tables.
"""

import sys
from pathlib import Path

from rdflib import RDF, XSD, Graph, Literal, Namespace, URIRef
from sqlalchemy import create_engine, text

import materialize

HERE = Path(__file__).resolve().parent
UL = Namespace("https://ul.edu.lb/kr/scm#")
ID = "https://ul.edu.lb/kr/id/"


def source():
    try:
        with create_engine(materialize.POSTGRES_URL).connect() as c:
            c.execute(text("SELECT 1"))
        return materialize.POSTGRES_URL, False
    except Exception:
        if (HERE / "brunel.db").exists():
            return f"sqlite:///{HERE / 'brunel.db'}", True
        sys.exit("No database: start PostgreSQL (docker compose up -d, python load_database.py) "
                 "or run python load_database.py --sqlite.")


def main():
    mapping = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "my_mapping.ttl"
    url, sqlite = source()
    with create_engine(url).connect() as c:
        rows = c.execute(text("SELECT order_id, customer, product_id, unit_quantity FROM orders")).fetchall()
    order = lambda k: URIRef(f"{ID}order/brunel/{k}")
    want = {
        "Y1": {(URIRef(f"{ID}customer/brunel/{r[1]}"), RDF.type, UL.Customer) for r in rows},
        "Y2": {(order(r[0]), UL.ofProduct, URIRef(f"{ID}product/brunel/{r[2]}")) for r in rows},
        "Y3": {(order(r[0]), UL.unitQuantity, Literal(int(r[3]), datatype=XSD.integer)) for r in rows},
    }
    out = HERE / "my-mapped.nt"
    try:
        materialize.run(str(mapping), sqlite, str(out))
    except SystemExit:
        raise
    except Exception as e:
        sys.exit(f"Your mapping does not run yet: {str(e).splitlines()[0][:300]}\n"
                 "Check the Turtle: every [ ] and every ; in the right place, a . at the end of each map.")
    g = Graph().parse(out, format="nt")
    got = {
        "Y1": set(g.triples((None, RDF.type, UL.Customer))),
        "Y2": set(g.triples((None, UL.ofProduct, None))),
        "Y3": set(g.triples((None, UL.unitQuantity, None))),
    }
    hints = {
        "Y1": "Copy <#Carriers>: SELECT DISTINCT customer, the template .../id/customer/brunel/{customer}, and rr:class ul:Customer.",
        "Y2": "Copy the ul:carriedBy rule: rr:template .../id/product/brunel/{product_id}. A template makes a link; rr:column would make text.",
        "Y3": "Copy the ul:weight rule: rr:column \"unit_quantity\" with rr:datatype xsd:integer.",
    }
    right = 0
    for y in ("Y1", "Y2", "Y3"):
        if got[y] == want[y]:
            right += 1
            print(f"{y}  right: {len(got[y]):,} triples, exactly the expected ones.")
        elif not got[y]:
            print(f"{y}  not yet: no triples from this rule. {hints[y]}")
        else:
            sample = next(iter(got[y] - want[y]), None)
            short = lambda x: x.n3().replace(ID, "").replace(str(UL), "ul:").replace(str(RDF), "rdf:")
            shown = f" For example you made: {' '.join(short(x) for x in sample)}." if sample else ""
            print(f"{y}  not yet: {len(got[y] & want[y]):,} of {len(want[y]):,} expected triples, "
                  f"{len(got[y] - want[y]):,} unexpected.{shown} {hints[y]}")
    print(f"\n{right} of 3 right.")


if __name__ == "__main__":
    main()
