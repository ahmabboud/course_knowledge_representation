"""Fetch the two course datasets into demos/data/dataco/ and demos/data/brunel/.

Run once, from the demos/ folder:  python data/fetch_data.py

No account or API token needed. Both sources are public, CC BY 4.0:

- DataCo SMART SUPPLY CHAIN (Constante, Silva and Pereira), Mendeley Data,
  DOI 10.17632/8gx2fvg2k6.5. One wide CSV, 180,519 order lines, 53 columns,
  plus a data dictionary CSV describing every column.
- Supply Chain Logistics Problem Dataset (Brunel University London),
  Figshare article 7558679, version 2. One Excel workbook holding the
  seven related tables. This script also writes each sheet out as its own
  CSV, so every later lab can read plain CSV files.

Every download is checked against the checksum the publisher lists, so a
truncated or substituted file fails loudly instead of silently.
Files already present with the right checksum are not downloaded again.

History: an earlier version downloaded DataCo through the Kaggle CLI (needs
an account and token) and Brunel through Figshare's "download all as zip"
endpoint, which answers HTTP 202 ("archive being prepared") with an empty
body, so it silently saved a 0 byte zip. Both were replaced on 2026-09-22
by the direct file URLs below, verified the same day.
"""

import csv
import hashlib
import sys
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
DATACO_DIR = DATA_DIR / "dataco"
BRUNEL_DIR = DATA_DIR / "brunel"

MENDELEY = "https://data.mendeley.com/public-files/datasets/8gx2fvg2k6/files/{}/file_downloaded"

FILES = [
    # (target path, url, algorithm, expected hash)
    (
        DATACO_DIR / "DataCoSupplyChainDataset.csv",
        MENDELEY.format("72784be5-36d3-44fe-b75d-0edbf1999f65"),
        "sha256",
        "fa6d022ed437155e1a2f0378710602848703c8a7f203f7ff5d77805bf8480aa6",
    ),
    (
        DATACO_DIR / "DescriptionDataCoSupplyChain.csv",
        MENDELEY.format("29dc7b05-dda6-4834-8354-5b5cc44430df"),
        "sha256",
        "9828e34669bd6d77e3b4463364cc44a5d52446b5e246fc258758cfe592566c4b",
    ),
    (
        BRUNEL_DIR / "Supply chain logistics problem.xlsx",
        "https://ndownloader.figshare.com/files/20162015",
        "md5",
        "2a05e8f60a6dda8ac318084f4183b29f",
    ),
]


def file_hash(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(path: Path, url: str, algorithm: str, expected: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and file_hash(path, algorithm) == expected:
        print(f"ok, already present: {path.name}")
        return
    print(f"downloading {path.name} ...")
    tmp = path.with_suffix(path.suffix + ".part")
    urllib.request.urlretrieve(url, tmp)
    got = file_hash(tmp, algorithm)
    if got != expected:
        tmp.unlink()
        sys.exit(f"checksum mismatch for {path.name}: expected {expected}, got {got}")
    tmp.replace(path)
    print(f"ok, {path.name} ({path.stat().st_size:,} bytes, {algorithm} verified)")


def export_brunel_sheets() -> None:
    """Write each of the seven Brunel sheets to its own CSV."""
    try:
        import openpyxl
    except ImportError:
        print("openpyxl not installed, skipping the CSV export (pip install openpyxl)")
        return
    wb = openpyxl.load_workbook(BRUNEL_DIR / "Supply chain logistics problem.xlsx", read_only=True)
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        header = rows[0]
        # Some sheets carry trailing empty columns in the workbook; drop them.
        keep = [i for i, name in enumerate(header) if name is not None]
        out = BRUNEL_DIR / f"{ws.title}.csv"
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for row in rows:
                if all(row[i] is None for i in keep):
                    continue
                w.writerow([row[i] for i in keep])
        print(f"ok, {out.name}: {len(rows) - 1} rows")


if __name__ == "__main__":
    for spec in FILES:
        fetch(*spec)
    export_brunel_sheets()
    print("\nDone. See data/README.md for what each file contains.")
