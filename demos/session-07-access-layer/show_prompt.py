"""Show the exact prompt the model gets for a question, without calling it.

    python show_prompt.py "How many orders did carrier V44_3 carry?"

Nothing here is secret or magic: the rules, the schema from void.ttl, the
three closest example queries from examples.ttl, and the question.
"""
import sys

from access_layer import build_prompt, load_examples, pick_examples, schema_text


def main():
    question = " ".join(sys.argv[1:]) or "How many orders did carrier V44_3 carry?"
    shots = pick_examples(question, load_examples())
    prompt = build_prompt(question, schema_text(), shots)
    print(prompt)
    print("\n" + "-" * 60)
    print(f"examples picked: {', '.join(e['id'] for e in shots)}  ({', '.join(e['question'] for e in shots)})")
    print(f"prompt: {len(prompt):,} characters, {len(prompt.splitlines())} lines")


if __name__ == "__main__":
    main()
