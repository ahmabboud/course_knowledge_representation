"""Run ROBOT on the Session 3 ontology, the same way the lab does, and
print a plain summary of what came back.

Run from the workspace/ folder (so the offline import catalog is found):

    python ../robot_report.py                               # fixed reference file
    python ../robot_report.py --input scro-extension-v0.ttl # the buggy start file

What it runs, in order:

1. robot reason   Classifies the ontology (ELK by default). If any class is
                  unsatisfiable (impossible, shown under owl:Nothing in
                  Protege), ROBOT stops with an error. This script then runs
                  step 1b instead of step 2.
1b. robot explain Only when step 1 found impossible classes: writes
                  explain.md, the chain of axioms that makes each class
                  impossible, the same chain Protege shows behind the "?"
                  button.
2. robot report   The quality report, written to report.tsv, one line per
                  finding: ERROR, WARN or INFO.

Two choices here were made after running the real tool, not guessed:

- The report runs on the SOURCE file, not on reasoned.ttl. Run on
  reasoned.ttl, ROBOT reports 515 findings, of which 481 are "missing
  label" and "missing definition" for IOF and BFO terms: their labels live
  in the imported files, which the report does not read. Run on the source
  file it reports 34, all about our own file.
- --catalog is passed automatically when catalog-v001.xml sits next to the
  input, so every import resolves offline instead of from the web.

Expected result on the fixed reference (verified 2026-09-22, ROBOT 1.9.10):
    reason: no impossible classes
    report: 3 ERROR, 28 WARN, 3 INFO. See README.md, "Reading the report",
            for what each line means and which ones are real problems.
Expected result on scro-extension-v0.ttl:
    reason: 1 impossible class with ELK (OrderForSoleSourcedGood),
            2 with HermiT (also SoleSourcedComponent).

Requires a JDK and ROBOT: `robot` on PATH, or robot.jar next to this
script, or --jar path/to/robot.jar. Install: https://robot.obolibrary.org
"""

import argparse
import csv
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def find_robot(jar_path):
    if jar_path:
        jar = Path(jar_path)
        if not jar.exists():
            sys.exit(f"--jar given but {jar} does not exist.")
        return ["java", "-Xmx3g", "-jar", str(jar)]
    robot = shutil.which("robot")
    if robot:
        return [robot]
    for candidate in (HERE / "robot.jar", HERE / "workspace" / "robot.jar"):
        if candidate.exists():
            return ["java", "-Xmx3g", "-jar", str(candidate)]
    sys.exit(
        "ROBOT not found: no `robot` on PATH and no robot.jar next to this script.\n"
        "Download robot.jar from https://github.com/ontodev/robot/releases (v1.9.10\n"
        "was used to build this lab) and pass --jar path/to/robot.jar."
    )


def run(cmd):
    print("$ " + " ".join(cmd))
    return subprocess.run(cmd).returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", default="scro-extension-reference.ttl")
    parser.add_argument("--reasoner", default="ELK", choices=["ELK", "HermiT"])
    parser.add_argument("--jar", default=None, help="path to robot.jar if robot is not on PATH")
    args = parser.parse_args()

    robot = find_robot(args.jar)
    src = Path(args.input).resolve()
    if not src.exists():
        sys.exit(f"{src} not found. Run from workspace/ after fetch_ontologies.py.")
    catalog = src.parent / "catalog-v001.xml"
    base = robot + (["--catalog", str(catalog)] if catalog.exists() else [])
    if not catalog.exists():
        print("WARNING: no catalog-v001.xml next to the input, imports will be fetched from the web.")

    reasoned = src.with_name("reasoned.ttl")
    print(f"\nStep 1: reason with {args.reasoner}")
    code = run(base + ["reason", "--input", str(src), "--reasoner", args.reasoner, "--output", str(reasoned)])

    if code != 0:
        explain = src.with_name("explain.md")
        print("\nROBOT found impossible (unsatisfiable) classes. Step 1b: explain why.")
        run(base + ["explain", "--input", str(src), "--reasoner", args.reasoner,
                    "--mode", "unsatisfiability", "--unsatisfiable", "all", "--explanation", str(explain)])
        print(f"\nWrote {explain.name}. Each block is one impossible class and the axioms that")
        print("together make it impossible. Fix the model, then run this script again.")
        sys.exit(1)

    report = src.with_name("report.tsv")
    print("\nStep 2: quality report on the source file")
    run(base + ["report", "--input", str(src), "--output", str(report), "--fail-on", "none"])

    with report.open() as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    print(f"\nWrote {reasoned.name} and {report.name}: {len(rows)} findings")
    for (level, rule), n in sorted(Counter((r["Level"], r["Rule Name"]) for r in rows).items()):
        print(f"  {level:5}  {rule:30} {n}")
    print("\nRead them with README.md, 'Reading the report': which lines are real problems,")
    print("which are a naming convention ROBOT expects, and which are fine as they are.")


if __name__ == "__main__":
    main()
