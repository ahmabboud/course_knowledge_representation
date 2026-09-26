"""Check your part B work: right, or not yet with a hint.

    python check_my_access.py                    your files
    python check_my_access.py solutions          the solutions

Y1 my_examples.ttl, Y2 my_access.py, Y3 my_questions.yaml. Each is checked
by what it does (the query runs and answers, the function finds the right
problems), not by how it is written. No model is called.
"""
import importlib.util
import sys
from pathlib import Path

from access_layer import check_query, load_examples, load_void, open_store, run
from questions_utils import load_questions
from score_utils import answer_set

HERE = Path(__file__).resolve().parent


def files(where):
    if where == "solutions":
        s = HERE / "solutions"
        return s / "my_examples_solutions.ttl", s / "my_access_solutions.py", s / "my_questions_solutions.yaml"
    return HERE / "my_examples.ttl", HERE / "my_access.py", HERE / "my_questions.yaml"


def taken_questions():
    return {e["question"].strip().lower() for e in load_examples()} | \
           {q["question"].strip().lower() for q in load_questions(HERE / "questions.yaml")}


def check_y1(path, store):
    try:
        mine = load_examples(path)
    except Exception as e:
        return f"{path.name} is not valid Turtle: {str(e).splitlines()[0][:120]}"
    if not mine:
        return "no example yet. Copy ex:3 from examples.ttl (a new IRI, rdfs:comment, sh:select)."
    for e in mine:
        if e["query"] == "None":
            return f"{e['id']} has no sh:select. Keep ex:3's three parts."
        if e["question"].strip().lower() in taken_questions():
            return f"'{e['question']}' is already a question of examples.ttl or questions.yaml."
        problems = check_query(e["query"])
        if problems:
            return f"{e['id']}: {problems[0][:140]}"
        rows = run(store, e["query"])
        if not rows:
            return f"{e['id']} runs but returns nothing. Does PLANT08 appear as the subject, and ul:servesPort as the property?"
    return None


def check_y2(path):
    spec = importlib.util.spec_from_file_location("my_access", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    classes, props = load_void()
    f = mod.unknown_classes
    got = f("SELECT ?s WHERE { ?s a ul:Shipment ; ul:shippedBy ?c }", classes, props)
    if len(got) != 1 or "Shipment" not in got[0]:
        if any("shippedBy" in g for g in got):
            return "it reports ul:shippedBy, a property. Keep only names that start with a capital (t[0].isupper())."
        return f"for a query using ul:Shipment it should report 1 problem naming ul:Shipment, got {got}."
    if f("SELECT ?s WHERE { ?s a ul:Order ; ul:carriedBy ?c }", classes, props):
        return "it reports ul:Order, which is a class of the graph. Compare with the classes, not the properties."
    if not f("SELECT ?s WHERE { ?s a <https://ul.edu.lb/kr/scm#Warehouse> }", classes, props):
        return "it misses <https://ul.edu.lb/kr/scm#Warehouse> written in full. Use ul_terms(query), as unknown_properties does."
    return None


def check_y3(path, store):
    try:
        mine = load_questions(path)
    except Exception as e:
        return f"{path.name} does not read as a questions file: {str(e).splitlines()[0][:120]}"
    if not mine:
        return "no question yet. Copy question 5 of questions.yaml (id, question: {en: ...}, gold)."
    for q in mine:
        if q["id"] in range(1, 16):
            return f"id {q['id']} is taken by questions.yaml. Use 101."
        if q["question"].strip().lower() in taken_questions():
            return f"'{q['question']}' is already in examples.ttl or questions.yaml: a test question must be new."
        if not q["gold"]:
            return f"question {q['id']} has no gold query."
        problems = check_query(q["gold"])
        if problems:
            return f"question {q['id']}'s gold query: {problems[0][:140]}"
        if not answer_set(run(store, q["gold"])):
            return f"question {q['id']}'s gold query returns nothing, so no answer could ever score."
    return None


def main():
    where = sys.argv[1] if len(sys.argv) > 1 else "mine"
    y1, y2, y3 = files(where)
    store, right = open_store(), 0
    for name, fn in (("Y1", lambda: check_y1(y1, store)), ("Y2", lambda: check_y2(y2)), ("Y3", lambda: check_y3(y3, store))):
        try:
            problem = fn()
        except NotImplementedError:
            problem = "not written yet (the TODO is still there)."
        except Exception as e:
            problem = f"it stops with {type(e).__name__}: {str(e)[:120]}"
        right += problem is None
        print(f"{name}  " + ("right." if problem is None else f"not yet: {problem}"))
    print(f"\n{right} of 3 right.")


if __name__ == "__main__":
    main()
