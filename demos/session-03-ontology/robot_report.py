"""Run the two ROBOT commands this lab needs, exactly as shown on the
lecture's own lab brief slide:

    robot reason --input scro-extension.ttl --reasoner ELK --output reasoned.ttl
    robot report --input reasoned.ttl --output report.tsv --profile QC

ROBOT (robot.obolibrary.org) is a Java command-line tool. This script
is a thin, documented wrapper, not a reimplementation, it shells out to
the real `robot` command so the report is the real ROBOT report.

Requires: a JDK (checked by Session 1's smoke test) and ROBOT itself,
either `robot` on PATH (see robot.obolibrary.org/#installing), or a
`robot.jar` next to this script (run with `java -jar robot.jar` in
that case, pass --jar path/to/robot.jar).
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def find_robot(jar_path: str | None):
    if jar_path:
        jar = Path(jar_path)
        if not jar.exists():
            sys.exit(f"--jar given but {jar} does not exist.")
        return ["java", "-jar", str(jar)]

    robot = shutil.which("robot")
    if robot:
        return [robot]

    local_jar = HERE / "robot.jar"
    if local_jar.exists():
        return ["java", "-jar", str(local_jar)]

    sys.exit(
        "robot not found on PATH and no robot.jar next to this script.\n"
        "Install: see https://robot.obolibrary.org/#installing (a robot.jar\n"
        "plus a robot.sh/.bat wrapper is the fastest path), or download\n"
        "robot.jar next to this script and pass --jar robot.jar."
    )


def run(cmd: list[str]):
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(f"robot exited with status {result.returncode}, see output above.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", default="scro-extension.ttl", help="your extension file (default: scro-extension.ttl)")
    parser.add_argument("--reasoner", default="ELK", choices=["ELK", "HermiT"], help="reasoner for the reason step (default: ELK)")
    parser.add_argument("--profile", default="QC", help="ROBOT report profile (default: QC)")
    parser.add_argument("--jar", default=None, help="path to robot.jar, if robot is not on PATH")
    args = parser.parse_args()

    robot_cmd = find_robot(args.jar)

    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"{input_path} not found. Run this from your session-03-ontology working copy, next to your own scro-extension.ttl.")

    reasoned_path = input_path.with_name("reasoned.ttl")
    report_path = input_path.with_name("report.tsv")

    print(f"Step 1: reason ({args.reasoner}), read the inferred hierarchy for unsatisfiable")
    print("classes, unintended equivalences, and subsumptions you did not mean.")
    run(robot_cmd + [
        "reason",
        "--input", str(input_path),
        "--reasoner", args.reasoner,
        "--output", str(reasoned_path),
    ])

    print()
    print(f"Step 2: report (profile {args.profile})")
    run(robot_cmd + [
        "report",
        "--input", str(reasoned_path),
        "--output", str(report_path),
        "--profile", args.profile,
    ])

    print()
    print(f"Wrote {reasoned_path} and {report_path}.")
    print("Record which OWL profile you ended up in (see the profile-check")
    print("cell on the lecture's lab brief slide), and push all three files:")
    print(f"{input_path.name}, {reasoned_path.name}, {report_path.name}.")


if __name__ == "__main__":
    main()
