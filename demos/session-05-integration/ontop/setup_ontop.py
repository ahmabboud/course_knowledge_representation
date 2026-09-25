"""Download the Ontop command line tool and the PostgreSQL JDBC driver, once.

    python ontop/setup_ontop.py

Run from demos/session-05-integration/ (about 90 MB, needs the network once).
Needs Java: the JDK 21 from the Session 1 setup (`java -version`).

What lands where (both folders are ignored by git):
  ontop/ontop-cli/                 Ontop 5.5.0 (February 2026), from github.com/ontop/ontop
  ontop/ontop-cli/jdbc/postgresql-42.7.13.jar
                                   the driver Ontop uses to talk to PostgreSQL
"""

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
CLI_URL = "https://github.com/ontop/ontop/releases/download/ontop-5.5.0/ontop-cli-5.5.0.zip"
JDBC_URL = "https://github.com/pgjdbc/pgjdbc/releases/download/REL42.7.13/postgresql-42.7.13.jar"
CLI_DIR = HERE / "ontop-cli"


def download(url, dest):
    print(f"downloading {url.rsplit('/', 1)[-1]} ...")
    with urlopen(url, timeout=120) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)


def main():
    if shutil.which("java") is None:
        sys.exit("Java not found. Install the JDK 21 (demos/README.md, Session 1) and open a new terminal.")
    print(subprocess.run(["java", "-version"], capture_output=True, text=True).stderr.splitlines()[0])
    if not (CLI_DIR / "ontop").exists():
        z = HERE / "ontop-cli.zip"
        download(CLI_URL, z)
        with zipfile.ZipFile(z) as zf:
            zf.extractall(CLI_DIR)
        z.unlink()
        (CLI_DIR / "ontop").chmod(0o755)
    jar = CLI_DIR / "jdbc" / JDBC_URL.rsplit("/", 1)[-1]
    if not jar.exists():
        jar.parent.mkdir(exist_ok=True)
        download(JDBC_URL, jar)
    print(f"ready: {CLI_DIR.relative_to(HERE.parent)} with {jar.name}")


if __name__ == "__main__":
    main()
