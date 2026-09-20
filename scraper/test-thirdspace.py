#!/usr/bin/env python3
"""
test-thirdspace.py - 3rdspace.html must behave like the BLOK page.

Run: python3 test-thirdspace.py [path]   (default ../3rdspace.html)
Exit 0 all good, 1 a check failed, 2 the page does not exist yet.
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

PATH = pathlib.Path(sys.argv[1] if len(sys.argv) > 1
                    else pathlib.Path(__file__).resolve().parent.parent / "3rdspace.html")
if not PATH.exists():
    print("SKIP: %s does not exist yet" % PATH.name)
    sys.exit(2)

fails, checks = [], 0
def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(name + (": " + str(detail) if detail else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1280, "height": 900})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(PATH.resolve().as_uri())
    page.wait_for_timeout(700)

    rows = lambda: page.evaluate("() => document.querySelectorAll('#tb tr:not(.day)').length")
    codes = page.evaluate("() => VENUES")
    check("the three clubs each get a filter group", len(codes) == 3, codes)
    for code in codes:
        for el in ("fav", "cats", "allFav", "allCat", "col"):
            check("venue %s has #%s%s" % (code, el, code),
                  page.evaluate("() => !!document.getElementById('%s%s')" % (el, code)))
    check("classes are listed", rows() > 20, rows())
    check("every row belongs to one of the clubs",
          page.evaluate("() => D.every(r => VENUES.indexOf(r[10]) > -1)"))
    check("no category is claimed by two clubs",
          page.evaluate("""() => {
            const seen = {};
            for (const v of VENUES) for (const c of ORDER[v]) {
              if (seen[c] && seen[c] !== v) return false; seen[c] = v; }
            return true; }"""))

    # storage must not collide with the BLOK page - same origin
    keys = page.evaluate("() => LS")
    check("its own storage keys", all(not str(v).startswith("blok")
          for v in list(keys.values()) if isinstance(v, str)), keys)
    check("a storage key per club", len(set(keys["t"].values())) == 3, keys["t"])

    # the filters actually filter
    before = rows()
    page.evaluate("() => {const x = document.getElementById('allCat' + VENUES[0]);"
                  " x.checked = false; x.dispatchEvent(new Event('change', {bubbles: true}))}")
    page.wait_for_timeout(300)
    check("unticking a club's classes removes them", rows() < before, "%d -> %d" % (before, rows()))
    page.evaluate("() => {const x = document.getElementById('allCat' + VENUES[0]);"
                  " x.checked = true; x.dispatchEvent(new Event('change', {bubbles: true}))}")
    page.wait_for_timeout(250)
    check("re-ticking brings them back", rows() == before, rows())

    # favourites survive a reload, like the other page
    has_star = page.evaluate("() => !!document.querySelector('#cats' + VENUES[0] + ' .star')")
    check("the first club has star buttons to favourite with", has_star)
    if has_star:
        page.evaluate("() => document.querySelector('#cats' + VENUES[0] + ' .star').click()")
        page.wait_for_timeout(200)
    if has_star:
        starred = page.evaluate("() => document.querySelectorAll('#fav' + VENUES[0] + ' .chip').length")
        check("a class type can be favourited", starred > 0, starred)
        page.reload(); page.wait_for_timeout(500)
        check("favourites are remembered",
              page.evaluate("() => document.querySelectorAll('#fav' + VENUES[0] + ' .chip').length") == starred)

    check("mobile menu is present",
          page.evaluate("() => !!document.getElementById('drawer') && !!document.getElementById('mnu')"))
    check("no JavaScript errors", not errors, "; ".join(errors[:3]))
    b.close()

if fails:
    print("FAIL: %d of %d Third Space checks failed" % (len(fails), checks))
    for f in fails: print("  x " + f)
    sys.exit(1)
print("OK: %d Third Space checks passed" % checks)
sys.exit(0)
