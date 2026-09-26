"""For the instructor, once: run every model call the lab and the slides use,
live, and save each answer, so that LLM_MODE=replay works for students whose
key fails and the reference outputs hold a real run.

    python record_llm.py          about 60 to 80 calls, 5 to 10 minutes

Needs GOOGLE_API_KEY in demos/.env. Writes reference-outputs/llm-cache.json
and the ask, evaluate and serve outputs next to it.
"""
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

from access_layer import RULES_ID

HERE = Path(__file__).resolve().parent
OUT = HERE / "reference-outputs"
RUNS = [
    ("ask-v44-3.txt", ["ask.py", "How many orders did carrier V44_3 carry?"]),
    ("ask-beirut.txt", ["ask.py", "Which customers are located in Beirut?"]),
    ("evaluate.txt", ["evaluate.py"]),
    ("evaluate-class-check.txt", ["evaluate.py", "--setting", "repair", "--add-class-check",
                                  "--class-check-from", "solutions/my_access_solutions.py", "--questions", "solutions/my_questions_solutions.yaml"]),
]


def main():
    env = dict(os.environ, LLM_MODE="record", LLM_DELAY=os.environ.get("LLM_DELAY", "4"))
    OUT.mkdir(exist_ok=True)
    for name, args in RUNS:
        print(f"recording {name} ...", flush=True)
        r = subprocess.run([sys.executable, *args], cwd=HERE, env=env, capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"{name} failed:\n{r.stderr[-2000:]}")
        head = (f"python {' '.join(args)}   (recorded {date.today()}, model "
                f"{os.environ.get('LLM_MODEL', 'gemini-3.5-flash-lite')}, rules {RULES_ID})\n")
        (OUT / name).write_text(head + r.stdout)
        print(r.stdout.splitlines()[-1] if r.stdout else "", flush=True)
    print("done: reference-outputs/llm-cache.json and the four outputs. Commit them.")


if __name__ == "__main__":
    main()
