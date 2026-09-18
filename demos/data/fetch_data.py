"""Fetch DataCo and Brunel into data/dataco/ and data/brunel/.

Run once, from the repository root: `python data/fetch_data.py`

DataCo needs a Kaggle account and API token (~/.kaggle/kaggle.json);
this script checks for one and prints setup instructions rather than
failing silently if it is missing. Brunel downloads directly from
Figshare, no account needed.
"""

import shutil
import zipfile
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
DATACO_DIR = DATA_DIR / "dataco"
BRUNEL_DIR = DATA_DIR / "brunel"

DATACO_KAGGLE_DATASET = "shashwatwork/dataco-smart-supply-chain-for-big-data-analysis"
BRUNEL_FIGSHARE_URL = (
    "https://brunel.figshare.com/ndownloader/articles/7558679/versions/1"
)


def fetch_dataco():
    if shutil.which("kaggle") is None:
        print("Kaggle CLI not found. Install it (pip install kaggle), then")
        print("place your API token at ~/.kaggle/kaggle.json, per")
        print("https://www.kaggle.com/docs/api. Skipping DataCo for now.")
        return
    DATACO_DIR.mkdir(parents=True, exist_ok=True)
    import subprocess

    subprocess.run(
        ["kaggle", "datasets", "download", "-d", DATACO_KAGGLE_DATASET, "-p", str(DATACO_DIR), "--unzip"],
        check=True,
    )
    print(f"DataCo fetched into {DATACO_DIR}")


def fetch_brunel():
    import urllib.request

    BRUNEL_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = BRUNEL_DIR / "brunel.zip"
    print("Downloading Brunel dataset from Figshare...")
    urllib.request.urlretrieve(BRUNEL_FIGSHARE_URL, zip_path)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(BRUNEL_DIR)
    zip_path.unlink()
    print(f"Brunel fetched into {BRUNEL_DIR}")


if __name__ == "__main__":
    fetch_dataco()
    fetch_brunel()
    print()
    print("Done. See data/README.md if either fetch was skipped or failed.")
