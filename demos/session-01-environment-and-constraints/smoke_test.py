"""Environment check for Session 1. Run this first, before assuming
anything else in the lab works. Matches the syllabus's own smoke-test
description: Python 3.12 or 3.13, JDK 21, Docker, and Protege, in one pass.
"""

import os
import platform
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path


def check(label, ok, hint=""):
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}" + (f" — {hint}" if hint and not ok else ""))
    return ok


def check_python():
    ok = (3, 12) <= sys.version_info[:2] < (3, 14)
    return check("Python 3.12 or 3.13", ok, f"found {sys.version.split()[0]}")


def check_jdk():
    java = shutil.which("java")
    if not java:
        return check("JDK 21 on PATH", False, "install a JDK 21 distribution")
    result = subprocess.run(["java", "-version"], capture_output=True, text=True)
    version_output = result.stderr or result.stdout
    ok = '"21' in version_output or "version 21" in version_output
    return check("JDK 21 on PATH", ok, version_output.splitlines()[0] if version_output else "")


def check_docker():
    docker = shutil.which("docker")
    if not docker:
        return check("Docker on PATH", False, "install Docker Desktop or the Docker Engine")
    result = subprocess.run(["docker", "info"], capture_output=True, text=True)
    ok = result.returncode == 0
    return check("Docker daemon reachable", ok, "start Docker Desktop / the docker service")


def check_protege():
    # Protégé has no consistent CLI entry point. Find its app or installation
    # directory without pinning the check to one release number or spelling.
    # Unicode normalization handles macOS's ``Protégé.app`` filename.
    if shutil.which("protege"):
        return check("Protege installed", True)

    system = platform.system()
    if system == "Darwin":
        roots = [Path("/Applications"), Path.home() / "Applications"]
    elif system == "Windows":
        roots = [
            Path(os.environ.get("ProgramFiles", "C:/Program Files")),
            Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")),
            Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")),
        ]
    else:
        roots = [Path("/opt"), Path.home()]

    def is_protege_install(path):
        name = unicodedata.normalize("NFKD", path.name)
        name = "".join(char for char in name if not unicodedata.combining(char))
        return name.casefold().startswith("protege")

    candidates = []
    for root in roots:
        try:
            candidates.extend(path for path in root.iterdir() if is_protege_install(path))
        except OSError:
            continue

    found = any(path.is_dir() for path in candidates)
    return check(
        "Protege installed",
        found,
        "looked in standard application locations; install from protege.stanford.edu if missing",
    )


def main():
    results = [check_python(), check_jdk(), check_docker(), check_protege()]
    print()
    if all(results):
        print("Environment ready.")
        sys.exit(0)
    print("Fix the FAIL lines above before the lab starts.")
    sys.exit(1)


if __name__ == "__main__":
    main()
