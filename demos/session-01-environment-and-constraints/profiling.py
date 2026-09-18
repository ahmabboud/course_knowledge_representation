"""Profile DataCo and Brunel with ydata-profiling.

Run as a script (`python profiling.py`) or cell by cell in an
interactive Python session / Jupyter (the `# %%` markers are Jupytext /
VS Code cell separators, so this file opens as a notebook there without
needing a separate .ipynb).
"""

# %%
import sys
from pathlib import Path

import pandas as pd
from ydata_profiling import ProfileReport

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.data_paths import DATACO_CSV, BRUNEL_TABLES  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent

# %% Profile DataCo — one wide table
print(f"Loading DataCo from {DATACO_CSV}")
dataco = pd.read_csv(DATACO_CSV, encoding="latin-1")
print(f"DataCo: {dataco.shape[0]} rows, {dataco.shape[1]} columns")

dataco_report = ProfileReport(
    dataco, title="DataCo Supply Chain — Profile", minimal=True
)
dataco_report.to_file(OUT_DIR / "profiling_report_dataco.html")
print("Wrote profiling_report_dataco.html")

# %% Profile each of the seven Brunel tables
for name, path in BRUNEL_TABLES.items():
    print(f"Loading Brunel/{name} from {path}")
    df = pd.read_csv(path)
    print(f"  {name}: {df.shape[0]} rows, {df.shape[1]} columns")
    report = ProfileReport(df, title=f"Brunel — {name}", minimal=True)
    report.to_file(OUT_DIR / f"profiling_report_brunel_{name}.html")

print()
print("Done. Open the HTML reports and start the constraint inventory:")
print("look for cardinalities that do not match what the column name")
print("implies, and value pairs that always co-occur.")
