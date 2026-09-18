"""Profile DataCo and Brunel with ydata-profiling.

Run as a script (`python profiling.py`) or cell by cell in Jupyter /
JupyterLab / VS Code (the `# %%` markers are Jupytext cell separators,
so this file opens as a notebook there without needing a separate
.ipynb — see the repo root README's "Conventions" section).

In a notebook, this also renders a quick missingness chart and the
full DataCo profile inline, so the room sees the findings without
alt-tabbing to a browser. Every profile is still written to an HTML
file too, for the tables that are easier to read full-screen.
"""

# %% [markdown]
# # Session 1: profiling DataCo and Brunel
#
# Goal: find the constraints nobody wrote down, before Session 3 asks
# you to model them. Run each cell in order. The quick-look chart below
# each dataset is for spotting candidates live; the full profile
# (written to HTML, and shown inline for DataCo) is where you confirm
# them.

# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from ydata_profiling import ProfileReport

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.data_paths import DATACO_CSV, BRUNEL_TABLES  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent

try:
    IN_NOTEBOOK = get_ipython() is not None  # noqa: F821
except NameError:
    IN_NOTEBOOK = False


def quality_summary(df: pd.DataFrame) -> pd.DataFrame:
    """One row per column: dtype, how many distinct values, and percent
    missing. Sorted worst-missingness first, this is what a live room
    scans to pick candidates before opening the full profile.
    """
    return (
        pd.DataFrame(
            {
                "dtype": df.dtypes.astype(str),
                "n_unique": df.nunique(),
                "pct_missing": (df.isna().mean() * 100).round(1),
            }
        )
        .sort_values("pct_missing", ascending=False)
    )


def plot_missingness(summary: pd.DataFrame, title: str, top_n: int = 15):
    """Horizontal bar chart of the worst top_n columns by percent
    missing. Skips the plot entirely if nothing is missing, an empty
    chart is not a finding.
    """
    worst = summary[summary["pct_missing"] > 0].head(top_n)
    if worst.empty:
        print(f"{title}: no missing values in any column.")
        return
    fig, ax = plt.subplots(figsize=(7, max(2, 0.35 * len(worst))))
    ax.barh(worst.index[::-1], worst["pct_missing"][::-1])
    ax.set_xlabel("% missing")
    ax.set_title(title)
    fig.tight_layout()
    plt.show()


# %% [markdown]
# ## DataCo — one wide table

# %%
print(f"Loading DataCo from {DATACO_CSV}")
dataco = pd.read_csv(DATACO_CSV, encoding="latin-1")
print(f"DataCo: {dataco.shape[0]} rows, {dataco.shape[1]} columns")

dataco_summary = quality_summary(dataco)
dataco_summary.head(15)

# %%
plot_missingness(dataco_summary, "DataCo — worst missingness by column")

# %% [markdown]
# ### Full profile
#
# Renders inline below when run in a notebook; always written to
# `profiling_report_dataco.html` next to this file either way.

# %%
dataco_report = ProfileReport(
    dataco, title="DataCo Supply Chain — Profile", minimal=True
)
dataco_report.to_file(OUT_DIR / "profiling_report_dataco.html")
print("Wrote profiling_report_dataco.html")
if IN_NOTEBOOK:
    dataco_report.to_notebook_iframe()

# %% [markdown]
# ## The seven Brunel tables
#
# Same quick-look pass per table, plus one chart comparing row counts
# across all seven, a fast way to notice a table that is suspiciously
# small or large next to the others. Full profiles are written to HTML
# for each table; only shown inline on request, seven iframes in one
# room is more scrolling than signal.

# %%
brunel_summaries = {}
brunel_rowcounts = {}

for name, path in BRUNEL_TABLES.items():
    print(f"Loading Brunel/{name} from {path}")
    df = pd.read_csv(path)
    print(f"  {name}: {df.shape[0]} rows, {df.shape[1]} columns")
    brunel_summaries[name] = quality_summary(df)
    brunel_rowcounts[name] = df.shape[0]

    report = ProfileReport(df, title=f"Brunel — {name}", minimal=True)
    report.to_file(OUT_DIR / f"profiling_report_brunel_{name}.html")

# %%
fig, ax = plt.subplots(figsize=(7, 3.5))
names = list(brunel_rowcounts.keys())
ax.bar(names, [brunel_rowcounts[n] for n in names])
ax.set_ylabel("rows")
ax.set_title("Brunel tables — row count, side by side")
ax.tick_params(axis="x", rotation=30)
fig.tight_layout()
plt.show()

# %% [markdown]
# To look at one Brunel table's full profile inline, run e.g.
# `ProfileReport(pd.read_csv(BRUNEL_TABLES["plant_ports"]), minimal=True).to_notebook_iframe()`
# in a new cell, or just open that table's HTML report from the file
# browser.

# %% [markdown]
# ## Where this goes
#
# Open the HTML reports (or the inline one above) and start the
# constraint inventory: look for cardinalities that do not match what
# the column name implies, and value pairs that always co-occur.
