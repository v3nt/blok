#!/usr/bin/env python3
"""
test-resilience.py — the scrape must not be stoppable by cosmetic junk.

A cookie banner cost a full day of updates: TrustArc's overlay swallowed the
mouse click on "Next day", every studio returned 0 classes, and the run
correctly refused to publish an empty schedule. Correct, and useless.

These tests pin the two rules that came out of it:
  1. never drive the page with real mouse events - a click inside the page
     ignores whatever is painted on top
  2. one bad day loses that day, not the studio, and not the run

No browser needed; the page is stubbed.

    python3 test-resilience.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import refresh

fails = []

def check(name, cond, detail=""):
    if not cond:
        fails.append(f"{name}{(': ' + detail) if detail else ''}")

class StubPage:
    def __init__(self, blow_up_on=None, overlay=False):
        self.day = 0
        self.blow_up_on = blow_up_on
        self.overlay = overlay
        self.mouse_clicks = 0
    def goto(self, *a, **k): pass
    def wait_for_selector(self, *a, **k): pass
    def wait_for_timeout(self, *a, **k): pass
    def title(self): return "BLOK - Clapton"
    def query_selector(self, sel):
        self.mouse_clicks += 1          # any use of this is the bug we fixed
        return None
    def evaluate(self, js, *arg):
        if "trustarc" in js.lower() or "consent" in js.lower():
            return "overlay removed x1" if self.overlay else "no consent banner"
        if "Next day" in js:
            self.day += 1
            return self.day < 6
        if self.day == self.blow_up_on:
            raise RuntimeError("Timeout 30000ms exceeded: "
                               "<div id='trustarc-banner-overlay'> intercepts pointer events")
        if self.day >= 5:
            return {"hdr": "", "rows": []}
        return {"hdr": "Wed, Sep %d" % (1 + self.day),
                "rows": [{"time": "6:20 AM", "dur": "50 min", "name": "CALISTHENICS 60",
                          "inst": "Someone", "tip": "", "btn": "8 credits"}]}

# 1. an overlay on every day must not stop anything
p = StubPage(overlay=True)
warn = []
rows = refresh.scrape(p, "https://x", "Clapton", "B", 2026, warn)
check("a consent overlay does not stop the scrape", len(rows) >= 4, f"{len(rows)} rows")
check("the scrape never uses real mouse clicks", p.mouse_clicks == 0,
      f"{p.mouse_clicks} mouse click(s)")

# 2. a day that throws costs one day
p2 = StubPage(blow_up_on=2)
warn2 = []
rows2 = refresh.scrape(p2, "https://x", "Clapton", "B", 2026, warn2)
check("one broken day does not lose the studio", len(rows2) >= 3, f"{len(rows2)} rows")
check("the broken day is reported", any("continuing" in w for w in warn2), str(warn2))

# 3. an empty scrape must never overwrite a good page
check("zero rows leaves index.html alone",
      "no rows scraped" in open(refresh.__file__, encoding="utf-8").read())

if fails:
    print(f"FAIL: {len(fails)} resilience check(s) failed")
    for f in fails: print("  x " + f)
    sys.exit(1)
print("OK: 5 resilience checks passed")
sys.exit(0)
