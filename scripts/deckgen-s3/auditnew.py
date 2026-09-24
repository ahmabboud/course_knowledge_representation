import json, sys
from playwright.sync_api import sync_playwright
url = sys.argv[1] if len(sys.argv)>1 else "kr-s3-new.html"
deck = sys.argv[2] if len(sys.argv)>2 else "kr-s03"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium"); pg=b.new_page(viewport={"width":1600,"height":900})
    pg.goto(f"http://localhost:8643/lectures/{url}?cb=3"); pg.wait_for_timeout(600)
    pg.evaluate(f"() => Object.keys(localStorage).filter(k=>k.startsWith('lu:{deck}')).forEach(k=>localStorage.removeItem(k))")
    pg.reload(); pg.wait_for_timeout(800)
    r=pg.evaluate(open("scripts/audit-deck.js").read())
    out={k:r.get(k) for k in ["overflow","revealedOverflow","collisions","strayChars","hiddenLeaks","gridEscapes","deadSandboxes"]}
    out["tinyTextCount"]=len(r.get("tinyText",[]))
    print(json.dumps(out))
    b.close()
