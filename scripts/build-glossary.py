#!/usr/bin/env python3
"""Build assets/glossary.js from GLOSSARY.md.

GLOSSARY.md is the single source of truth. Each table row
    | **Term** | Plain definition |
becomes one entry. assets/lu-glossary.js then turns the first use of each
term on a slide into a clickable definition, so no deck needs hand-written
popovers for course vocabulary.

Run after every edit to GLOSSARY.md:
    python3 scripts/build-glossary.py
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "GLOSSARY.md"
OUT = ROOT / "assets" / "glossary.js"

# Plain English words that are also glossary terms. Linking them would put a
# definition on "order" in "in order to". They stay in GLOSSARY.md (handouts,
# search) but are never linked automatically.
SKIP = {
    "Subject", "Object", "Variable", "Distribution", "Process", "Quality",
    "Role", "Null", "Constraint", "Target", "Order", "Port", "Customer",
    "Supplier", "Plant", "Warehouse", "Carrier", "Shipment", "Domain", "Range",
    "Satisfiable class", "Cardinality (of a column)", "Supply chain",
}

# Common words that are also technical terms: linked once per deck, and only
# from the session that introduces them onwards. Every other term is linked
# at its first use on every slide, so a student who jumps to any slide can
# still click it.
ONCE_PER_DECK = {
    "Graph", "Node", "Edge", "Class", "Individual", "Inference", "Baseline",
    "Mapping", "Blocking", "Severity", "Literal", "Prefix", "Precision",
    "Recall", "Schema", "Ontology", "Triple", "Axiom", "Subclass", "Shape",
    "Embedding", "Provenance", "Alignment", "Namespace", "Predicate",
    "Endpoint", "Aggregation", "Federation", "Datatype", "Classification",
    "Entailment", "Union", "Complement", "Intersection (and)", "Union (or)",
    "Complement (not)", "Decidable", "Punning", "Continuant", "Occurrent",
    "Business rule", "Relational database",
}

# Extra spellings that should open the same definition.
ALIASES = {
    "Open world assumption": ["open world", "OWA"],
    "Closed world assumption": ["closed world", "CWA"],
    "GNN": ["graph neural network"],
    "KGE": [],
    "Knowledge graph": ["KG"],
    "Unsatisfiable class": ["unsatisfiable"],
    "Triple store": ["triplestore"],
    "Materialization": ["materialisation", "materialize", "materialise", "materialized", "materialised"],
    "Virtualization": ["virtualisation"],
    "Realization": ["realisation"],
    "Temporal leakage": ["leakage"],
    "Train/test split": ["train/test"],
    "Entity resolution": [],
    "Protégé": ["Protege"],
    "Bill of materials": ["BOM"],
    "Knowledge graph embedding": ["KG embedding"],
    "Message passing": [],
    "Consistency check": ["consistency checking"],
    "Competency question": ["CQ"],
    "IOF Core": [],
    "Upper ontology": ["top-level ontology"],
    "Data profiling": ["profiling"],
    "WHERE clause": ["WHERE"],
    "GROUP BY": [],
}

# Names written with a fixed case. Everything else matches whatever the
# capitalisation of its first letter per word.
PROPER = {
    "DataCo", "Brunel", "Turtle", "Fuseki", "Cypher", "Neo4j", "Docker",
    "Protégé", "Protege", "Ontop", "Manchester syntax", "TransE", "XGBoost",
    "PyKEEN", "PyTorch Geometric", "HermiT", "Morph-KGC", "PostgreSQL",
}

ROW = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*$")
HEAD = re.compile(r"^##\s+Session\s+(\d+)")


def md_inline(text):
    """The tiny bit of Markdown the glossary uses: `code` and **bold**."""
    out = html.escape(text, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    return out


def is_fixed_case(name):
    if name in PROPER:
        return True
    letters = [c for c in name if c.isalpha()]
    # Acronyms and prefixed names: ERP, SHACL, rdf:type, owl:Thing, OWL 2 EL
    return ":" in name or sum(c.isupper() for c in letters) >= 2 or any(c.isdigit() for c in name)


def spellings(name):
    """Visible forms a slide may use for this entry."""
    m = re.match(r"^(.*?)\s*\((.+)\)$", name)
    forms = []
    if m:
        base, paren = m.group(1).strip(), m.group(2).strip()
        if re.fullmatch(r"[A-Z0-9-]{2,}", paren):
            forms += [base, paren]           # Term (ACRONYM)
        elif base in {"some", "only"}:
            forms += [paren]                 # some (existential restriction)
        elif paren in {"and", "or", "not"}:
            forms += [base]                  # Intersection (and)
        else:
            forms += [base]                  # Justification (explanation)
    else:
        forms.append(name)
    forms += ALIASES.get(name, [])
    return forms


def display(name):
    m = re.match(r"^(.*?)\s*\((.+)\)$", name)
    if m and m.group(1).strip() in {"some", "only"}:
        return name
    return name


def main():
    if not SRC.exists():
        sys.exit("GLOSSARY.md not found")
    entries, session = [], 0
    for line in SRC.read_text(encoding="utf-8").splitlines():
        h = HEAD.match(line)
        if h:
            session = int(h.group(1))
            continue
        r = ROW.match(line)
        if not r or not session:
            continue
        name, definition = r.group(1).strip(), r.group(2).strip()
        entry = {
            "term": display(name),
            "def": md_inline(definition),
            "session": session,
        }
        if name in SKIP:
            entry["link"] = False
        else:
            if name in ONCE_PER_DECK:
                entry["scope"] = "deck"
            entry["forms"] = [
                {"text": f, "fixed": is_fixed_case(f)} for f in dict.fromkeys(spellings(name))
            ]
        entries.append(entry)

    body = "[\n" + ",\n".join(json.dumps(e, ensure_ascii=False) for e in entries) + "\n]"
    OUT.write_text(
        "/* Generated by scripts/build-glossary.py from GLOSSARY.md. Do not edit by hand. */\n"
        "window.LU_GLOSSARY = " + body + ";\n",
        encoding="utf-8",
    )
    linked = sum(1 for e in entries if e.get("link", True))
    print(f"{len(entries)} terms, {linked} linked automatically -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
