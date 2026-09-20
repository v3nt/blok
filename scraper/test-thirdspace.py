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
def act(name, fn):
    """Run an interaction; a failure becomes a named check, not a traceback."""
    global checks
    checks += 1
    try:
        fn()
        return True
    except Exception as e:
        fails.append("%s: %s" % (name, str(e).splitlines()[0][:120]))
        return False

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
    locs = page.evaluate("() => LOCS")
    # One list of class types covering every club, and the clubs switched on
    # and off separately - not a filter group per club.
    check("one set of class filters", len(codes) == 1, codes)
    check("a switch for each club", sorted(locs) == ["City", "Islington", "Moorgate"], locs)
    for el in ("fav", "cats", "allFav", "allCat", "col"):
        check("the class list has #%s%s" % (el, codes[0]),
              page.evaluate("() => !!document.getElementById('%s%s')" % (el, codes[0])))
    check("the location switches are on the page",
          page.evaluate("() => document.querySelectorAll('#locs input[data-loc]').length") == 3)
    check("classes are listed", rows() > 20, rows())
    check("all three clubs are in the one list",
          page.evaluate("() => new Set(D.map(r => r[6])).size === LOCS.length"))
    check("a class type appears once, not once per club",
          page.evaluate("() => new Set(ORDER[VENUES[0]]).size === ORDER[VENUES[0]].length"))

    # switching a club off must remove exactly that club's classes
    all_rows = rows()
    per_club = page.evaluate("() => {const t = {};"
                             " D.forEach(r => t[r[6]] = (t[r[6]] || 0) + 1); return t}")
    toggle = ("(on) => {const x = document.querySelector('#locs input[data-loc=\"Moorgate\"]');"
              " x.checked = on; x.dispatchEvent(new Event('change', {bubbles: true}))}")
    act("a club can be switched off", lambda: page.evaluate(toggle, False))
    page.wait_for_timeout(300)
    check("switching a club off drops only its classes",
          rows() == all_rows - per_club["Moorgate"],
          "%d -> %d, Moorgate has %d" % (all_rows, rows(), per_club["Moorgate"]))
    check("no Moorgate row is left behind",
          page.evaluate("() => ![...document.querySelectorAll('#tb tr[data-cat]')]"
                        ".some(r => r.innerText.indexOf('Moorgate') > -1)"))
    page.reload(); page.wait_for_timeout(500)
    check("a club left off stays off", rows() == all_rows - per_club["Moorgate"], rows())
    act("switch it back on", lambda: page.evaluate(toggle, True))
    page.wait_for_timeout(300)
    check("switching it back on restores them", rows() == all_rows, rows())

    # The same class runs at more than one club - Just Ride is taught at all
    # three - so names are shared on purpose. What must hold is that the
    # COUNTS are per club, or a chip would claim another club's classes.
    check("counts match the data",
          page.evaluate("""() => {
            const v = VENUES[0], tally = {};
            D.forEach(r => tally[r[4]] = (tally[r[4]] || 0) + 1);
            return ORDER[v].every(c => (CATS[v] || {})[c] === tally[c]);
          }"""))
    shown = page.evaluate("() => ORDER[VENUES[0]].filter(c => DESC[c]).length")
    total = page.evaluate("() => ORDER[VENUES[0]].length")
    check("most class types carry a description for the hover",
          shown >= total * 0.8, "%d of %d" % (shown, total))
    # storage must not collide with the BLOK page - same origin
    keys = page.evaluate("() => LS")
    check("its own storage keys", all(not str(v).startswith("blok")
          for v in list(keys.values()) if isinstance(v, str)), keys)
    check("the class filters have their own key", len(keys["t"]) == 1, keys["t"])
    check("the locations have their own key", bool(keys.get("lo")), keys)

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
