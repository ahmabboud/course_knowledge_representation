"""The cohort's IRI scheme, agreed at the end of Session 2's discussion
block. Import this from Session 3 onward instead of re-deciding the
scheme per session.

Fill in BASE and the minting functions once the cohort has actually
agreed the convention (see Session 2's lab brief and discussion). This
stub uses the scheme argued for on the Session 2 slides, the source
system is part of the name, as the default so the file is usable
before the room formally agrees one; overwrite it with whatever the
room actually decides.
"""

BASE = "https://ul.edu.lb/kr/scm#"


def supplier_iri(source_system: str, source_key: str) -> str:
    """One IRI per real thing, not per row. Two systems' idea of the
    same supplier get two IRIs (a Session 5 entity-resolution decision),
    not a silent merge here.
    """
    return f"{BASE}supplier/{source_system}/{source_key}"


def plant_iri(source_system: str, source_key: str) -> str:
    return f"{BASE}plant/{source_system}/{source_key}"


def port_iri(source_system: str, source_key: str) -> str:
    return f"{BASE}port/{source_system}/{source_key}"


def carrier_iri(source_system: str, source_key: str) -> str:
    return f"{BASE}carrier/{source_system}/{source_key}"


def order_iri(source_system: str, source_key: str) -> str:
    return f"{BASE}order/{source_system}/{source_key}"
