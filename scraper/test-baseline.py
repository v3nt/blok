#!/usr/bin/env python3
"""
test-baseline.py — the agreed schedule UI, asserted in a real browser.

Every check here exists because that exact thing broke at least once:

  * the whole grouped UI was replaced by another generator          (19 Aug)
  * favouriting a chip silently deselected it and its classes vanished
  * a favourited chip appeared in both the ★ row and the list below
  * one select-all per gym instead of one per row
  * default favourites never reached a browser with a saved list
  * a regex holding a quote broke the publish-time JS parser check

Run it against a built page:

    python3 test-baseline.py ../index.html

Exit 0 = the baseline holds. Exit 1 = a regression, with the failure named.
Needs playwright (same dependency as refresh.py). If it is missing this exits
2 - "could not verify" - which is not the same as passing.
"""
import sys, json, pathlib

PATH = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html").resolve()
GROUPS = [("M", "Mission E1"), ("B", "BLOK")]
fails, checks = [], 0

def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name}{(': ' + detail) if detail else ''}")

def act(name, fn):
    """Run an interaction. A missing element must read as a named failure,
    not a 30s timeout and a traceback - a test that throws is unreadable."""
    global checks
    checks += 1
    try:
        fn()
        return True
    except Exception as e:
        first = str(e).strip().splitlines()[0]
        fails.append(f"{name}: {first}")
        return False

def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("SKIP: playwright not installed - baseline NOT verified")
        print("      /usr/bin/python3 -m pip install playwright")
        return 2
    if not PATH.exists():
        print(f"FAIL: {PATH} does not exist")
        return 1

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.set_default_timeout(5000)
        page.goto(PATH.as_uri())

        def state():
            # Defensive: a page that dropped the UI entirely must produce a
            # readable failure, not a traceback.
            return page.evaluate("""() => {
              const ids = g => ([...document.querySelectorAll(g + ' input[data-c]')].map(e => e.dataset.c));
              const el = i => document.getElementById(i);
              const txt = i => (el(i) || {}).textContent || '';
              return {
                favM: ids('#favM'), catM: ids('#catsM'),
                favB: ids('#favB'), catB: ids('#catsB'),
                toggles: ['allFavM','allCatM','allFavB','allCatB']
                  .map(i => { const e = document.getElementById(i);
                              return e ? (e.disabled ? 'disabled' : (e.indeterminate ? 'mixed' : e.checked)) : null; }),
                rows: document.querySelectorAll('#tb tr:not(.day)').length,
                total: (typeof D === 'undefined' ? 0 : D.length),
                shown: txt('shown'),
                tipped: document.querySelectorAll('#tb .pill[title]').length,
                collapsed: {M: el('catsM').classList.contains('collapsed'),
                            B: el('catsB').classList.contains('collapsed')},
                chipVisible: {M: !!(el('catsM').querySelector('.chip') || {}).offsetParent,
                              B: !!(el('catsB').querySelector('.chip') || {}).offsetParent},
                favVisible: !!(el('favB').querySelector('.chip') || {}).offsetParent,
                booked: [...document.querySelectorAll('#tb tr[data-state="booked"]')]
                  .map(tr => tr.cells[0].textContent + ' ' + tr.cells[4].textContent),
                bookedPanel: (el('booked') || {}).style ? el('booked').style.display : 'missing',
                panelDates: [...document.querySelectorAll('#booked li .bt')].map(e => e.textContent),
                bookedDates: (typeof D === 'undefined' ? [] :
                  D.filter(r => r[7] === 'booked').map(r => r[0])),
                studioCells: document.querySelectorAll('#tb tr:not(.day) td:nth-child(5)').length,
                studioLinks: [...document.querySelectorAll('#tb tr:not(.day) td:nth-child(5) a')]
                  .map(a => a.textContent + ' -> ' + a.getAttribute('href')),
                saved: JSON.parse(localStorage.getItem('blokFavs') || 'null'),
                favRowFirst: ['M','B'].every(v => {
                  const row = el('fav'+v);
                  if (!row) return false;
                  const kids = [...row.parentNode.querySelectorAll('.row')];
                  return kids[0].id === 'fav'+v;    // ★ row must sit above the rest
                }),
              };
            }""")

        s = state()

        # If the grouped UI is absent this is not a subtle regression - it is a
        # different page. Report it plainly instead of failing 15 ways.
        missing = [i for i in ("favM", "catsM", "favB", "catsB",
                               "allFavM", "allCatM", "allFavB", "allCatB")
                   if not page.query_selector("#" + i)]
        if missing:
            print("FAIL: this is not the agreed UI - missing #" + ", #".join(missing))
            browser.close()
            return 1

        # --- structure -----------------------------------------------------
        check("two filter groups, one per gym",
              len(page.query_selector_all(".grp")) == 2)
        for gid, label in GROUPS:
            check(f"{label}: has a favourites row and a list",
                  page.query_selector(f"#fav{gid}") and page.query_selector(f"#cats{gid}"))
        check("favourites row sits above the non-favourites", s["favRowFirst"])
        check("four select-all toggles, one per row",
              all(t is not None for t in s["toggles"]), str(s["toggles"]))

        # --- every row rendered -------------------------------------------
        check("every class is rendered", s["rows"] == s["total"], f"{s['rows']} of {s['total']}")
        check("shown counter agrees", s["shown"].startswith(f"{s['total']} of {s['total']}"), s["shown"])

        # --- default favourites -------------------------------------------
        check("BLOK starts with calisthenics/strength favourited",
              {"CALISTHENICS", "BLOKSTRENGTH: FULL BODY", "BLOKSTRENGTH: LOWER BODY",
               "BLOKSTRENGTH: UPPER BODY"} <= set(s["favB"]), str(s["favB"]))
        check("Mission starts with its strength stream favourited",
              {"Reps Kulture", "Squat Kulture", "Statics Kulture"} <= set(s["favM"]), str(s["favM"]))

        # --- no chip in two places ----------------------------------------
        for gid, label in GROUPS:
            fav, cat = s["fav" + gid], s["cat" + gid]
            check(f"{label}: no chip duplicated across rows",
                  not (set(fav) & set(cat)), str(sorted(set(fav) & set(cat))))

        # --- each toggle drives only its own row ---------------------------
        act("BLOK list toggle is operable", lambda: page.uncheck("#allCatB"))
        after = state()
        check("BLOK list toggle leaves BLOK favourites alone",
              set(after["favB"]) == set(s["favB"]) and after["rows"] < s["total"])
        act("BLOK list toggle re-checks", lambda: page.check("#allCatB"))

        # --- favouriting must not deselect (the bug that hid classes) ------
        before_rows = state()["rows"]
        starred = act("a Mission chip has a star to click",
                      lambda: page.locator("#catsM > .chip").first.locator(".star").click())
        moved = state()
        check("favouriting a type does not hide its classes",
              moved["rows"] == before_rows, f"{moved['rows']} vs {before_rows}")
        check("favouriting moves the chip, not copies it",
              not (set(moved["favM"]) & set(moved["catM"])))
        if starred:
            act("the favourited chip can be un-starred",
                lambda: page.locator("#favM > .chip").first.locator(".star").click())

        # --- defaults reach a browser that already saved a list ------------
        page.evaluate("() => { localStorage.setItem('blokFavs','[]');"
                      " localStorage.removeItem('blokFavsSeed'); }")
        page.reload()
        seeded = state()
        check("defaults seed into a browser with a stale saved list",
              len(seeded["favB"]) >= 4 and len(seeded["favM"]) >= 3,
              f"favB={seeded['favB']} favM={seeded['favM']}")

        # --- but a deliberate clear must stick -----------------------------
        page.evaluate("() => document.querySelectorAll('#favB .star,#favM .star')"
                      ".forEach(b => b.click())")
        page.reload()
        cleared = state()
        check("clearing every favourite stays cleared",
              not cleared["favB"] and not cleared["favM"],
              f"favB={cleared['favB']} favM={cleared['favM']}")

        # --- reset gets you back -------------------------------------------
        act("Reset filters is clickable", lambda: page.click("#reset"))
        reset = state()
        check("Reset filters restores the default favourites",
              len(reset["favB"]) >= 4 and len(reset["favM"]) >= 3)

        # --- bookings ---------------------------------------------------------
        # Bookings come from /profile/upcoming, not from a "Cancel" button in the
        # schedule, which only appears while logged in and silently produced a
        # page with nothing marked.
        check("booked classes are marked in the table", s["booked"], "none marked")
        check("the booked panel is shown when there are bookings",
              (not s["booked"]) or s["bookedPanel"] == "block", s["bookedPanel"])

        # "Your booked classes" is a what's-next panel: a class you attended last
        # week must not sit at the top of the page as if it were coming up.
        import datetime as _dt
        today = _dt.date.today().isoformat()
        past = [d for d in s["bookedDates"] if d < today]
        check("the panel lists only upcoming bookings",
              len(s["panelDates"]) == len([d for d in s["bookedDates"] if d >= today]),
              f"panel shows {len(s['panelDates'])}, upcoming are "
              f"{len([d for d in s['bookedDates'] if d >= today])}, past in data: {len(past)}")

        # --- collapsible non-favourites --------------------------------------
        # Collapsing hides chips only. It must not change the selection, so the
        # table underneath stays exactly as it was.
        check("non-favourites start expanded",
              not s["collapsed"]["M"] and s["chipVisible"]["M"])
        before = state()["rows"]
        act("BLOK collapse toggle is clickable", lambda: page.click("#colB"))
        col = state()
        check("collapsing hides the BLOK non-favourite chips",
              col["collapsed"]["B"] and not col["chipVisible"]["B"])
        check("collapsing leaves the favourites row visible", col["favVisible"])
        check("collapsing does not change what is listed",
              col["rows"] == before, f"{col['rows']} vs {before}")
        check("the other gym is unaffected", not col["collapsed"]["M"])
        page.reload()
        kept = state()
        check("collapsed state is remembered",
              kept["collapsed"]["B"] and not kept["collapsed"]["M"])
        act("BLOK collapse toggle expands again", lambda: page.click("#colB"))
        page.reload()
        check("expanding again is remembered",
              not state()["collapsed"]["B"])

        # --- studio links ----------------------------------------------------
        # Every studio cell links to that studio on ClassPass. Checked as
        # name -> href pairs, so a link pointing at the wrong studio fails too.
        EXPECTED = {
            "Clapton":    "https://classpass.com/studios/blok-clapton-london",
            "Shoreditch": "https://classpass.com/studios/blok-shoreditch-london",
            "Mission E1": "https://classpass.com/studios/mission-e1-london",
        }
        pairs = set(s["studioLinks"])
        check("every studio cell is a link",
              len(s["studioLinks"]) == s["studioCells"],
              f"{len(s['studioLinks'])} links for {s['studioCells']} cells")
        seen = {p.split(" -> ")[0] for p in pairs}
        check("all three studios appear", seen == set(EXPECTED), str(sorted(seen)))
        wrong = [p for p in pairs if EXPECTED.get(p.split(" -> ")[0]) != p.split(" -> ")[1]]
        check("each studio links to its own ClassPass page", not wrong, str(wrong[:3]))

        # --- descriptions ---------------------------------------------------
        check("class descriptions on hover",
              s["tipped"] > s["total"] * 0.5, f"{s['tipped']} of {s['total']} rows")

        check("no JavaScript errors", not errors, "; ".join(errors[:3]))
        browser.close()

    if fails:
        print(f"FAIL: {len(fails)} of {checks} baseline checks failed")
        for f in fails:
            print("  x " + f)
        return 1
    print(f"OK: {checks} baseline checks passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
