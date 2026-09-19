"""Run the two ROBOT commands this lab needs:

    robot reason --input scro-extension.ttl --reasoner ELK --output reasoned.ttl
    robot report --input reasoned.ttl --output report.tsv --fail-on none

ROBOT (robot.obolibrary.org) is a Java command-line tool. This script
is a thin, documented wrapper, not a reimplementation, it shells out to
the real `robot` command so the report is the real ROBOT report.

`--profile QC` was on an earlier version of this file and the lecture's
own lab brief slide, run once against the real tool and fixed, it is
not a real ROBOT report profile. `robot report --profile` takes a path
to a custom rules file, not a named preset; with no `--profile` flag,
ROBOT already runs its own bundled default rule set, which is what a
"QC report" means here. `--fail-on none` is real too, and necessary:
ROBOT's report command exits non-zero whenever it finds an ERROR-level
violation, which for an in-progress student ontology is the normal,
expected case, not a crash. Without it, this script would abort right
after writing a perfectly good report.tsv, on the ontology's own
findings.

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
    parser.add_argument("--profile", default=None, help="path to a custom ROBOT report rules file (default: ROBOT's own bundled rules)")
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
    print(f"Step 2: report ({'custom rules: ' + args.profile if args.profile else 'ROBOT default rules'})")
    report_cmd = robot_cmd + [
        "report",
        "--input", str(reasoned_path),
        "--output", str(report_path),
        "--fail-on", "none",
    ]
    if args.profile:
        report_cmd += ["--profile", args.profile]
    run(report_cmd)

    print()
    print(f"Wrote {reasoned_path} and {report_path}.")
    print("ERROR and WARN rows in report.tsv are normal for a file you have not")
    print("finished yet, that is what the report is for. Read them, do not chase")
    print("zero rows before the lab is done.")
    print("Record which OWL profile you ended up in (see the profile-check")
    print("cell on the lecture's lab brief slide), and push all three files:")
    print(f"{input_path.name}, {reasoned_path.name}, {report_path.name}.")


if __name__ == "__main__":
    main()
