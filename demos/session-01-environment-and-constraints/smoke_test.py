"""Environment check for Session 1. Run this first, before assuming
anything else in the lab works. Matches the syllabus's own smoke-test
description: Python 3.12, JDK 21, Docker, and Protege, in one pass.
"""

import shutil
import subprocess
import sys


def check(label, ok, hint=""):
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}" + (f" — {hint}" if hint and not ok else ""))
    return ok


def check_python():
    ok = sys.version_info >= (3, 12)
    return check("Python 3.12 or newer", ok, f"found {sys.version.split()[0]}")


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
    # Protege has no reliable CLI entry point across platforms; check the
    # common install locations instead of assuming a command exists.
    import platform
    from pathlib import Path

    candidates = []
    system = platform.system()
    if system == "Darwin":
        candidates.append(Path("/Applications/Protege.app"))
    elif system == "Windows":
        candidates.append(Path("C:/Program Files/Protege-5.6.4"))
    else:
        candidates.append(Path.home() / "Protege-5.6.4")

    found = any(p.exists() for p in candidates)
    return check(
        "Protege installed",
        found,
        f"expected one of {[str(c) for c in candidates]}; install from protege.stanford.edu if missing",
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
