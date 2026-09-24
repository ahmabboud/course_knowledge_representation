"""Fetch the real ontologies this lab runs against, into workspace/, so
Protege opens with IOF SCRO already loaded and every import resolved
offline. Also copies in the finished reference ontology
(scro-extension-reference.ttl) this session's walkthrough opens,
reasons over, and reports on. Nothing fetched or copied here is meant
to be edited; this is a run-and-observe lab, not a build-it-yourself
one, see README.md.

Sources, verified before writing this script (see workspace/LICENCES.md
for the full citations once this has run):

- IOF Core and Supply Chain (SCRO): github.com/iofoundry/ontology,
  tag Release_202603, MIT licensed. We take core/, supplychain/, the
  repo's own catalog-v001.xml, and just the two cache/ subtrees SCRO's
  own catalog actually points at (cache/bfo and cache/CMNS), not the
  other domains (biopharma, maintenance, ...) this course does not use.
- GS1 Web Vocabulary: ref.gs1.org/voc/data/gs1Voc.ttl, Apache 2.0 per
  the schema:license triple embedded in the file itself, with a GS1 IP
  Policy patent caveat alongside it (recorded verbatim in LICENCES.md,
  not paraphrased). Fetched for completeness and for the licensing
  exercise; scro-extension-reference.ttl checked it and did not end up
  needing anything from it, worth showing live if it comes up, reuse
  search coming up empty is a real, honest outcome too.

Run once before Session 3, and again if IOF cuts a new release: `python
fetch_ontologies.py`.
"""

import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

IOF_REPO = "https://github.com/iofoundry/ontology.git"
IOF_TAG = "Release_202603"
GS1_VOC_URL = "https://ref.gs1.org/voc/data/gs1Voc.ttl"

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE / "workspace"

# Paths inside the IOF repo we actually need. Everything else in that
# repo (biopharma, maintenance, certification, ...) is real too, just
# not used by this course, and skipping it keeps workspace/ small.
IOF_PATHS_TO_COPY = [
    "catalog-v001.xml",
    "AboutIOFDev.rdf",
    "AboutIOFProd.rdf",
    "LICENSE",
    "core",
    "supplychain",
    "cache/bfo",
    "cache/CMNS",
]


def run(cmd, **kwargs):
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True, **kwargs)


def fetch_iof():
    if shutil.which("git") is None:
        sys.exit("git is required to fetch the IOF ontologies; install it and rerun.")

    with tempfile.TemporaryDirectory() as tmp:
        clone_dir = Path(tmp) / "iof"
        run(["git", "clone", "--depth", "1", "--branch", IOF_TAG, IOF_REPO, str(clone_dir)])

        for rel in IOF_PATHS_TO_COPY:
            src = clone_dir / rel
            dst = WORKSPACE / rel
            if not src.exists():
                print(f"  WARNING: expected {rel} in the IOF repo, not found, skipping.")
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            print(f"  copied {rel}")


def fetch_gs1():
    """Best-effort. GS1 is only needed for the licensing exercise, not
    to open Protege or to run the reasoners and ROBOT. A network hiccup
    here (flaky wifi, a proxy having a bad day) should not take out the
    rest of the script, so this warns and returns rather than raising:
    main() still runs write_licences_note(), copy_reference(), and
    verify_catalog() either way. Re-run this script later, or fetch the
    one file by hand from the URL below, if this warns.
    """
    dst_dir = WORKSPACE / "gs1"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / "gs1Voc.ttl"
    print(f"Downloading {GS1_VOC_URL}")
    try:
        urllib.request.urlretrieve(GS1_VOC_URL, dst)
    except OSError as e:
        print(f"  WARNING: could not download GS1 Web Vocabulary ({e}).")
        print(f"  Not fatal, only the licensing exercise needs it.")
        print(f"  Retry later with: python fetch_ontologies.py")
        print(f"  or fetch it by hand from {GS1_VOC_URL} into {dst}")
        return
    size_kb = dst.stat().st_size / 1024
    print(f"  wrote {dst} ({size_kb:.0f} KB)")


LICENCES_MD = """\
# Third-party ontologies and vocabularies in this workspace

Fetched by `fetch_ontologies.py`, regenerate rather than hand-edit.
Every one of these belongs in the licence list your final report is
required to carry, per this session's lecture.

## IOF Core and Supply Chain (SCRO)

- Source: https://github.com/iofoundry/ontology, tag `Release_202603`.
- Licence: **MIT**, `LICENSE` in that repository, "Copyright (c) 2022
  Industrial Ontologies Foundry".
- What we took: `core/` (the mid-level ontology SCRO imports) and
  `supplychain/` (SCRO itself), plus the repo's own `catalog-v001.xml`
  and the `cache/bfo` and `cache/CMNS` subtrees that catalog resolves
  to, so Protege opens fully offline.

## GS1 Web Vocabulary

- Source: https://ref.gs1.org/voc/data/gs1Voc.ttl
- Licence: **Apache License, Version 2.0**, declared as a
  `schema:license` triple inside the file itself, copyright 2015-2019
  GS1 AISBL. The same triple carries a GS1 IP Policy notice about
  patent claims not covered by the licence grant, quoted here
  verbatim rather than summarised, because the room's job is to read
  licences like this one, not trust a paraphrase of them:

  > GS1, under its IP Policy, seeks to avoid uncertainty regarding
  > intellectual property claims by requiring the participants in the
  > Work Groups that developed this vocabulary to agree to grant to
  > GS1 members a royalty-free licence or a RAND licence to Necessary
  > Claims [...] Licensed under the Apache License, Version 2.0 [...]

## SCORVoc, the licensing exercise, not pre-solved here

This session's lab brief has the room resolve a real licence conflict
live: https://github.com/vocol/scor's `scor.ttl` declares
`dct:license` as the ODC PDDL (public domain dedication), while that
same repository's `README.md` carries "© APICS 2015 [...] All rights
reserved." Both statements were confirmed live when this lab was
built; if IOF has fixed the conflict upstream by the time you teach
this, say so and let the room verify it fixed rather than silently
swapping in a different example.

This is the documented, honest reason the course builds on IOF SCRO
(MIT, unambiguous) rather than SCORVoc for the base ontology, per the
lecture's own reveal panel.
"""


def write_licences_note():
    dst = WORKSPACE / "LICENCES.md"
    dst.write_text(LICENCES_MD)
    print(f"Wrote {dst}")


LAB_FILES = [
    "scro-extension-v0.ttl",          # the lab's starting point, contains the errors the reasoner finds
    "scro-extension-reference.ttl",   # the fixed version
    "sample-shipments.ttl",           # a few individuals, imports the fixed version
]
COURSE_CATALOG_ENTRY = (
    '    <uri id="Course reference ontology" name="https://ul.edu.lb/kr/scm#" '
    'uri="./scro-extension-reference.ttl"/>\n'
)


def copy_reference():
    """Copy the three lab files into workspace/ (Protege only finds the
    offline catalog when the opened file sits next to it), and register
    the course ontology in that catalog so sample-shipments.ttl can import
    it offline."""
    for name in LAB_FILES:
        shutil.copy2(HERE / name, WORKSPACE / name)
        print(f"Copied {name} into workspace/")
    catalog = WORKSPACE / "catalog-v001.xml"
    text = catalog.read_text()
    if "https://ul.edu.lb/kr/scm#" not in text:
        catalog.write_text(text.replace("</catalog>", COURSE_CATALOG_ENTRY + "</catalog>"))
        print("Registered https://ul.edu.lb/kr/scm# in catalog-v001.xml")


def verify_catalog():
    """Confirm the import chain this lab actually needs resolves to a
    real local file, so a broken fetch fails loudly here rather than
    as a mysterious unresolved import inside Protege.
    """
    needed = {
        "https://spec.industrialontologies.org/ontology/supplychain/SupplyChain/": None,
        "https://spec.industrialontologies.org/ontology/core/Core/": None,
        "http://purl.obolibrary.org/obo/bfo/2020/bfo.owl": None,
    }
    catalog_text = (WORKSPACE / "catalog-v001.xml").read_text()
    ok = True
    for iri in needed:
        m = re.search(r'name="' + re.escape(iri) + r'" uri="([^"]+)"', catalog_text)
        if not m:
            print(f"  WARNING: {iri} not found in catalog-v001.xml")
            ok = False
            continue
        target = (WORKSPACE / m.group(1)).resolve()
        if not target.exists():
            print(f"  WARNING: catalog points {iri} at {m.group(1)}, which does not exist")
            ok = False
    if ok:
        print("Catalog check: the SupplyChain / Core / BFO import chain resolves offline.")
    else:
        print("Catalog check FAILED, see warnings above. IOF may have restructured a")
        print("release; open an issue against this lab or adjust IOF_PATHS_TO_COPY.")


def main():
    WORKSPACE.mkdir(exist_ok=True)
    fetch_iof()
    # Order matters: copy_reference() and write_licences_note() are what
    # this walkthrough needs to open Protege, so they run before the
    # GS1 fetch, which is only needed for the licensing exercise, not
    # to open the file. That way a GS1 network failure (handled inside
    # fetch_gs1 itself, see there) never blocks the part of this script
    # Protege actually depends on.
    copy_reference()
    write_licences_note()
    fetch_gs1()
    verify_catalog()
    print()
    print("Done. In Protege: Open File, browse to")
    print(f"  {WORKSPACE / 'scro-extension-reference.ttl'}")
    print("This file is finished, nothing to edit or Save As. Run ELK,")
    print("then HermiT, and read the inferred hierarchy, per README.md.")


if __name__ == "__main__":
    main()
