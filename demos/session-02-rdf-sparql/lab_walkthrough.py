"""Session 2 lab, presented stage by stage.

A presentation layer, not another copy of the pipeline: every stage below
imports and calls the real functions from convert_to_rdf.py, load_fuseki.py,
run_queries.py and neo4j_comparison.py, the same code `python <file>.py` runs
on its own. It adds result tables and one chart.

Run as a script (`python lab_walkthrough.py`, after `docker compose up -d`
from demos/) or cell by cell in JupyterLab or VS Code (the `# %%` markers
are Jupytext cells).
"""

# %% [markdown]
# # Session 2: RDF conversion, SPARQL, and a Neo4j comparison
#
# Four stages: convert Brunel to RDF, load it into Fuseki, answer the
# question set with timings, then ask the same questions in Neo4j.

# %%
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
sys.path.insert(0, str(HERE))

try:
    from IPython.display import display
except ImportError:  # running as a plain script
    def display(obj):
        print(obj)

# %% [markdown]
# ## Stage 1: tables to triples
# `convert_to_rdf.py` mints one IRI per real thing with `common/iri.py`, and
# writes brunel.ttl (one graph) and brunel.trig (one named graph per table).

# %%
from convert_to_rdf import build, write  # noqa: E402

start = time.perf_counter()
dataset = build()
write(dataset)
print(f"Converted in {time.perf_counter() - start:.1f} s")
print((HERE / "sample" / "order.ttl").read_text())

# %% [markdown]
# ## Stage 2: load Fuseki (TDB2) and check it answers
# If Java or Docker fails, skip this stage and use Oxigraph in Stage 3.

# %%
from load_fuseki import confirm, load  # noqa: E402

try:
    load()
    confirm()
    STORE = "fuseki"
except Exception as exc:  # noqa: BLE001
    print(f"Fuseki not reachable ({exc.__class__.__name__}); using Oxigraph instead.")
    STORE = "oxigraph"

# %% [markdown]
# ## Stage 3: the question set, with timings

# %%
from run_queries import fuseki, load_queries, oxigraph, oxigraph_store  # noqa: E402

store = oxigraph_store() if STORE == "oxigraph" else None
timings = []
for label, query in load_queries():
    t0 = time.perf_counter()
    rows = oxigraph(store, query) if store is not None else fuseki(query)
    ms = (time.perf_counter() - t0) * 1000
    timings.append({"question": label.split(" · ")[0], "rows": len(rows), "ms": round(ms, 1)})
    print(label)
    display(pd.DataFrame(rows[:6]))

df = pd.DataFrame(timings)
display(df)
ax = df.plot.barh(x="question", y="ms", legend=False, logx=True, title=f"Query time on {STORE} (log scale)")
ax.set_xlabel("milliseconds")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Stage 4: the same questions in Neo4j and Cypher

# %%
from neo4j_comparison import main as neo4j_main  # noqa: E402

try:
    neo4j_main()
except Exception as exc:  # noqa: BLE001
    print(f"Neo4j not reachable ({exc.__class__.__name__}). Start it with docker compose up -d.")
