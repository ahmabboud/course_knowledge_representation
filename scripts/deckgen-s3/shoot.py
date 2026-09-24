import sys, json
from playwright.sync_api import sync_playwright
url, deck, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
slides = [int(x) for x in sys.argv[4].split(",")]
reveal = len(sys.argv) > 5 and sys.argv[5] == "reveal"
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg = b.new_page(viewport={"width": 1600, "height": 900})
    pg.goto(f"http://localhost:8643/lectures/{url}?cb=1")
    pg.wait_for_timeout(700)
    pg.evaluate(f"() => Object.keys(localStorage).filter(k=>k.startsWith('lu:{deck}')).forEach(k=>localStorage.removeItem(k))")
    for n in slides:
        pg.goto(f"http://localhost:8643/lectures/{url}?cb=1#/{n}")
        pg.wait_for_timeout(500)
        if reveal:
            for _ in range(8):
                pg.keyboard.press("ArrowDown")
            pg.wait_for_timeout(200)
        pg.screenshot(path=f"/tmp/{prefix}-{n}.png")
    b.close()
print("ok")
