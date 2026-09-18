"""Session 2 lab, presented stage by stage.

This is a presentation layer, not a fifth copy of the pipeline: every
stage below imports and calls the real functions from
convert_to_rdf.py, load_fuseki.py, run_queries.py and
neo4j_comparison.py, the same code `python <file>.py` runs on its own.
This file adds narration, result tables, and a couple of charts, so
the room sees each stage's output without reading terminal text.

Run as a script (`python lab_walkthrough.py`, prerequisite: `docker
compose up -d` from the repo root) or cell by cell in Jupyter /
JupyterLab / VS Code (the `# %%` markers are Jupytext cell
separators).
"""

# %% [markdown]
# # Session 2: RDF conversion, SPARQL, and a Neo4j comparison
#
# Four stages, run in order: convert a Brunel slice to RDF, load it
# into Fuseki, answer the question set with timings, then load the
# same slice into Neo4j for a side by side look. Each stage's own
# `.py` file is still the thing to run outside a notebook, or to
# adapt for your own team project; this file just narrates it.

# %%
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    IN_NOTEBOOK = get_ipython() is not None  # noqa: F821
except NameError:
    IN_NOTEBOOK = False

if IN_NOTEBOOK:
    from IPython.display import display
else:
    def display(obj):  # running as a plain script: fall back to print
        print(obj)

# %% [markdown]
# ## Stage 1 — Convert the Brunel slice to RDF

# %%
from convert_to_rdf import build_graph, OUT_PATH, SLICE_SIZE, SOURCE  # noqa: E402

print(f"Building a {SLICE_SIZE}-row slice from source system '{SOURCE}'")
graph = build_graph()
graph.serialize(destination=str(OUT_PATH), format="turtle")
print(f"Wrote {len(graph)} triples to {OUT_PATH}")

# %% [markdown]
# ### A sample of the triples, as a table

# %%
sample = pd.DataFrame(
    [(str(s), str(p), str(o)) for s, p, o in list(graph)[:15]],
    columns=["subject", "predicate", "object"],
)
sample

# %% [markdown]
# ### What the graph actually looks like
#
# A small drawing of a corner of it, the plant/port/order structure
# the Session 1 constraint and this session's Q3 are both about.
# Needs `networkx`; skipped with a note if it is not installed.

# %%
try:
    import networkx as nx

    g_nx = nx.DiGraph()
    shown = 0
    for s, p, o in graph:
        if p.endswith("servesPort") or p.endswith("fromPlant"):
            g_nx.add_edge(str(s).rsplit("/", 1)[-1], str(o).rsplit("/", 1)[-1], label=str(p).rsplit("#", 1)[-1])
            shown += 1
        if shown >= 25:
            break

    fig, ax = plt.subplots(figsize=(7, 5))
    pos = nx.spring_layout(g_nx, seed=7)
    nx.draw(g_nx, pos, ax=ax, with_labels=True, node_size=600, font_size=7, arrowsize=12)
    edge_labels = nx.get_edge_attributes(g_nx, "label")
    nx.draw_networkx_edge_labels(g_nx, pos, edge_labels=edge_labels, font_size=6, ax=ax)
    ax.set_title(f"{shown} servesPort / fromPlant edges from the slice")
    fig.tight_layout()
    plt.show()
except ImportError:
    print("networkx not installed, skipping the graph drawing (pip install networkx).")

# %% [markdown]
# ## Stage 2 — Load into Fuseki

# %%
from load_fuseki import load, confirm  # noqa: E402

load()
confirm()

# %% [markdown]
# ## Stage 3 — Run the question set, with results as tables
#
# `run_queries.py` prints row counts and timings; here each query's
# actual result renders as a table, and the timings become one chart
# at the end.

# %%
from run_queries import load_queries, run_fuseki  # noqa: E402


def bindings_to_df(result: dict) -> pd.DataFrame:
    """SPARQL JSON results, as a table. Empty results get an empty
    frame rather than a KeyError, a query that matches nothing is
    still a valid answer to show the room.
    """
    bindings = result["results"]["bindings"]
    if not bindings:
        return pd.DataFrame()
    cols = list(bindings[0].keys())
    return pd.DataFrame([{c: b[c]["value"] for c in b} for b in bindings])[cols]


timings = []
for label, query in load_queries():
    start = time.perf_counter()
    result = run_fuseki(query)
    elapsed_ms = (time.perf_counter() - start) * 1000
    df = bindings_to_df(result)
    timings.append((label, len(df), elapsed_ms))
    print(f"\n[{label}] {len(df)} rows in {elapsed_ms:.1f} ms")
    display(df.head(10))

# %% [markdown]
# ### Query timings, side by side

# %%
timing_df = pd.DataFrame(timings, columns=["query", "rows", "ms"])
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.bar(timing_df["query"], timing_df["ms"])
ax.set_ylabel("ms")
ax.set_title("Session 2 question set — timings against Fuseki")
ax.tick_params(axis="x", rotation=20)
fig.tight_layout()
plt.show()
timing_df

# %% [markdown]
# Fuseki or the JDK misbehaving live in the room is the documented
# failure mode here, per the lecture's own fallback guidance: set
# `TRIPLESTORE = "oxigraph"` at the top of `run_queries.py` and rerun
# this stage with `run_oxigraph` in place of `run_fuseki`, rather than
# debugging Java in front of the class.

# %% [markdown]
# ## Stage 4 — Neo4j comparison
#
# Loads the same slice into Neo4j and runs the equivalent Cypher, not
# scored against SPARQL, the point is to show the differences.

# %%
import csv  # noqa: E402

from neo4j import GraphDatabase  # noqa: E402
from neo4j_comparison import BRUNEL_ORDER_LIST, NEO4J_AUTH, NEO4J_URI  # noqa: E402
from neo4j_comparison import load as neo4j_load  # noqa: E402

with open(BRUNEL_ORDER_LIST) as f:
    neo4j_rows = list(csv.DictReader(f))[:200]

driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
with driver.session() as session:
    session.execute_write(neo4j_load, neo4j_rows)
    counts = session.run(
        "MATCH (o:Order) OPTIONAL MATCH (o)-[r:FROM_PLANT]->(p:Plant) "
        "RETURN count(DISTINCT o) AS orders, count(DISTINCT p) AS plants, count(r) AS edges"
    ).single()
driver.close()

print(f"Neo4j now holds {counts['orders']} Order nodes, {counts['plants']} Plant nodes, {counts['edges']} FROM_PLANT edges.")
print("The HAS_COMPONENT multi-hop comparison (queries.sparql Q4) is commented")
print("out in neo4j_comparison.py until a multi-hop relation exists in the slice.")

# %% [markdown]
# ## Where this goes
#
# A loaded endpoint answering every question in `queries.sparql`, a
# documented IRI scheme (`common/iri.py`, update it once the room
# agrees its final form), and the timings above recorded somewhere the
# cohort can see them next session. Session 3 onward imports
# `common/iri.py` as given, get it right here.
