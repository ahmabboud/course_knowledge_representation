import json, os, sys
# Audit every KR deck with scripts/audit-deck.js. Serve the repo root first:
#   python3 -m http.server 8660   then   python3 scripts/audit-all.py [1 2 ...]
PORT = os.environ.get("PORT", "8660")
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
    for n in sys.argv[1:] or "123456":
        pg=b.new_page(viewport={"width":1600,"height":900})
        pg.goto(f"http://localhost:{PORT}/lectures/kr-session-0{n}.html?cb=g1"); pg.wait_for_timeout(500)
        pg.evaluate("() => Object.keys(localStorage).filter(k=>k.startsWith('lu:')).forEach(k=>localStorage.removeItem(k))")
        pg.reload(); pg.wait_for_timeout(800)
        r=pg.evaluate(open("scripts/audit-deck.js").read())
        out={k:r.get(k) for k in ["overflow","revealedOverflow","collisions","hiddenLeaks"] if r.get(k)}
        out["stray"]=[s for s in (r.get("strayChars") or []) if "2212" not in json.dumps(s)]
        print(f"S{n}", json.dumps(out)[:1500]); pg.close()
    b.close()
