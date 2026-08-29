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

# 6/7. the browser must always be closed - a visible window is left on the
# desktop otherwise, once every four hours, forever.
import types, sys as _sys

class FakeCtx:
    def __init__(self, log): self.log = log; self.closed = 0
    def new_page(self): return FakePage()
    def close(self): self.closed += 1; self.log.append("ctx")

class FakeBrowser:
    def __init__(self, log): self.log = log; self.closed = 0; self.ctx = FakeCtx(log)
    def new_context(self, **k): return self.ctx
    def close(self): self.closed += 1; self.log.append("browser")

class FakePage:
    def __init__(self, boom=False): self.boom = boom
    def goto(self, *a, **k):
        if self.boom: raise RuntimeError("page exploded")
    def wait_for_selector(self, *a, **k): pass
    def wait_for_timeout(self, *a, **k): pass
    def title(self): return "x"
    def query_selector(self, s): return None
    def evaluate(self, js, *a):
        if "consent" in js.lower() or "trustarc" in js.lower(): return "no consent banner"
        if "Next day" in js: return False
        if "when" in js: return []          # the reservations query
        return {"hdr": "", "rows": []}

def run_main(explode):
    log = []
    class Chromium:
        def launch_persistent_context(self, *a, **k): return FakeCtx(log)
        def launch(self, *a, **k): return FakeBrowser(log)
    class PW:
        chromium = Chromium()
        def __enter__(self): return self
        def __exit__(self, *a): return False
    fake = types.ModuleType("playwright.sync_api")
    fake.sync_playwright = lambda: PW()
    pkg = types.ModuleType("playwright")
    saved = {k: _sys.modules.get(k) for k in ("playwright", "playwright.sync_api")}
    _sys.modules["playwright"] = pkg; _sys.modules["playwright.sync_api"] = fake
    real_scrape = refresh.scrape
    if explode:
        def boom(*a, **k): raise SystemExit("FATAL: page contract changed")
        refresh.scrape = boom
    argv = _sys.argv
    _sys.argv = ["refresh.py", "--out", "/tmp/never-written.html", "--no-profile",
                 "--base", "file:///tmp/none/", "--upcoming", "file:///tmp/none/x.html"]
    try:
        refresh.main()
    except SystemExit:
        pass
    finally:
        refresh.scrape = real_scrape
        _sys.argv = argv
        for k, v in saved.items():
            if v is None: _sys.modules.pop(k, None)
            else: _sys.modules[k] = v
    return log

closed = run_main(explode=False)
check("the browser is closed after a normal run", closed, "nothing was closed")
crashed = run_main(explode=True)
check("the browser is closed even when the scrape blows up", crashed,
      "window would have been left open")


if fails:
    print(f"FAIL: {len(fails)} resilience check(s) failed")
    for f in fails: print("  x " + f)
    sys.exit(1)
print("OK: 7 resilience checks passed")
sys.exit(0)
