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
                tipped: document.querySelectorAll('#tb .pill[data-desc]').length,
                nativeTitles: document.querySelectorAll('#tb .pill[title]').length,
                tipEl: !!el('tip'),
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
                defaults: (typeof DEFAULT_FAVS === 'undefined') ? [] : DEFAULT_FAVS,
                orderB: (typeof orderB === 'undefined') ? [] : orderB,
                orderM: (typeof orderM === 'undefined') ? [] : orderM,
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

        import datetime as _dt
        today = _dt.date.today().isoformat()
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
        # The invariant is "every default that exists on this page is starred" -
        # not a hardcoded list of names. A shorter date window legitimately
        # drops whole categories, and the test must not fail for that.
        for gid, order_key in (("B", "orderB"), ("M", "orderM")):
            want = {c for v, _, c in (d.partition("|") for d in s["defaults"])
                    if v == gid} & set(s[order_key])
            check(f"{'BLOK' if gid == 'B' else 'Mission E1'}: every default that "
                  f"exists is favourited",
                  want <= set(s["fav" + gid]),
                  f"missing {sorted(want - set(s['fav' + gid]))}")
        check("the defaults are the calisthenics/strength classes",
              any("CALISTHENICS" in d for d in s["defaults"])
              and any("Kulture" in d for d in s["defaults"]), str(s["defaults"][:4]))

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
        # Same invariant as the first-load check: whatever defaults this page
        # actually has must all be starred. Counting them hardcodes a data size.
        want_all = {(d.split("|")[0], d.split("|")[1]) for d in s["defaults"]}
        got = {("B", c) for c in seeded["favB"]} | {("M", c) for c in seeded["favM"]}
        check("defaults seed into a browser with a stale saved list",
              want_all <= got, f"missing {sorted(want_all - got)}")

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
        got_reset = {("B", c) for c in reset["favB"]} | {("M", c) for c in reset["favM"]}
        check("Reset filters restores the default favourites",
              want_all <= got_reset, f"missing {sorted(want_all - got_reset)}")

        # --- bookings ---------------------------------------------------------
        # Bookings come from /profile/upcoming, not from a "Cancel" button in the
        # schedule, which only appears while logged in and silently produced a
        # page with nothing marked.
        # The schedule is public; only booking status needs a session. A
        # signed-out build says so in the header, and must still publish - the
        # times and classes are exactly as right as ever. Requiring bookings
        # here would block every publish whenever the profile is signed out,
        # which is the opposite of what this page is for.
        signed_out = page.evaluate(
            "() => /booking status unavailable/i.test("
            "(document.querySelector('header p')||{}).textContent||'')")
        if signed_out:
            print("  note: signed-out build - booking status checks skipped")
        check("booked classes are marked in the table",
              signed_out or s["booked"], "none marked")
        check("the booked panel is shown when there are bookings",
              (not s["booked"]) or s["bookedPanel"] == "block", s["bookedPanel"])
        unknown_rows = page.evaluate(
            "() => document.querySelectorAll('tr[data-state=\"unknown\"]').length")
        check("a signed-out build says so on the page",
              (not signed_out) or unknown_rows > 0,
              "header claims signed out but no unknown-status rows")
        check("a signed-in build has real booking statuses",
              signed_out or unknown_rows == 0,
              f"{unknown_rows} rows have no status but the header does not say so")

        # No day that has already happened: a past row at the same time as a
        # future booking is how the wrong row gets read as "not booked".
        stale = [d for d in s["bookedDates"] if d < today]
        # Compare against the date the page was BUILT, not today: a page that was
        # correct when generated must not start failing overnight just because it
        # aged - that blocked every publish for a day.
        first = page.evaluate("() => (typeof D === 'undefined' || !D.length) ? '' : D[0][0]")
        built = page.evaluate("""() => {
          const m = (document.querySelector('header p') || {}).textContent || '';
          const d = m.match(/refreshed \\w+ (\\d+) (\\w+) (\\d{4})/);
          if (!d) return '';
          const mm = {Jan:1,Feb:2,Mar:3,Apr:4,May:5,Jun:6,Jul:7,Aug:8,Sep:9,Oct:10,Nov:11,Dec:12}[d[2]];
          return d[3] + '-' + String(mm).padStart(2,'0') + '-' + String(d[1]).padStart(2,'0');
        }""")
        check("the build dropped days already past when it ran",
              (not built) or first >= built,
              f"first day {first}, built {built}")
        if built and built < today:
            log_stale = f"note: page was built {built}, today is {today} - data is stale"
            print("  " + log_stale)

        # "Your booked classes" is a what's-next panel: a class you attended last
        # week must not sit at the top of the page as if it were coming up.
        past = [d for d in s["bookedDates"] if d < today]
        later = [d for d in s["bookedDates"] if d > today]
        todays = [d for d in s["bookedDates"] if d == today]
        # The panel also drops today's classes that have already started, so an
        # exact count is wrong: assert the invariant instead. Nothing already
        # past may appear, every future day must, and today's are optional.
        check("the panel lists no booking that has already been",
              not [d for d in s["panelDates"] if d < today],
              f"panel dates {sorted(s['panelDates'])}, today {today}")
        check("the panel lists only upcoming bookings",
              len(later) <= len(s["panelDates"]) <= len(later) + len(todays),
              f"panel shows {len(s['panelDates'])}, later {len(later)}, "
              f"today {len(todays)}, past in data: {len(past)}")

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
        # The description tooltip must actually appear, and must not double up
        # with the browser's own title= bubble.
        check("no native title tooltips (they double up with ours)",
              s["nativeTitles"] == 0,
              f"{s[chr(39)+chr(39)] if False else s['nativeTitles']} pill(s) still carry title=")
        check("the tooltip element exists", s["tipEl"])
        pill = page.locator("#tb .pill[data-desc]").first
        # Guard the interaction: with no tooltip element there is nothing to
        # hover into, and the checks above already reported that.
        if s["tipEl"] and s["tipped"] and act("a described class can be hovered",
                                              lambda: pill.hover()):
            tip = page.evaluate("() => { const t = document.getElementById('tip'); return {shown: getComputedStyle(t).display !== 'none', text: t.innerText}; }")
            want = pill.get_attribute("data-desc") or ""
            check("hovering shows the description", tip["shown"], "tooltip stayed hidden")
            check("the tooltip shows that class's description",
                  want[:40] in tip["text"], f"got {tip['text'][:60]!r}")
            page.mouse.move(2, 2)
            hidden = page.evaluate("() => getComputedStyle(document.getElementById('tip')).display === 'none'")
            check("the tooltip hides again on mouse out", hidden)

        check("class descriptions on hover",
              s["tipped"] > s["total"] * 0.5, f"{s['tipped']} of {s['total']} rows")

        # --- the working-hours filter cuts off at 5:15pm ----------------------
        # Inclusive: a class starting exactly at 5:15pm is inside the hidden
        # band, 5:20pm onwards is not.
        act("the work-hours filter is clickable", lambda: page.check("#hw"))
        page.wait_for_timeout(300)
        edges = page.evaluate("""() => {
          const mins = t => { const m = t.match(/^(\\d+):(\\d+)(AM|PM)$/); if (!m) return -1;
            return ((+m[1]) % 12 + (m[3] === 'PM' ? 12 : 0)) * 60 + (+m[2]); };
          const shown = [...document.querySelectorAll('#tb tr[data-wd]')]
            .filter(r => +r.dataset.wd < 5).map(r => +r.dataset.mins);
          const all = D.filter(r => r[9] < 5).map(r => r[1]);
          return {
            latestHidden: Math.max(...all.filter(m => !shown.includes(m) && m >= 480 && m <= 1200)),
            earliestEveningShown: Math.min(...shown.filter(m => m > 1000)),
            any515: all.includes(1035), any520plus: all.some(m => m > 1035 && m < 1100),
            shown515: shown.includes(1035)};
        }""")
        check("a weekday class at 5:15pm is hidden",
              (not edges["any515"]) or not edges["shown515"], str(edges))
        check("weekday classes after 5:15pm are still shown",
              (not edges["any520plus"]) or edges["earliestEveningShown"] > 1035, str(edges))
        act("restore the work-hours filter", lambda: page.uncheck("#hw"))
        page.wait_for_timeout(250)

        # --- the booked panel minimises, and stays that way -------------------
        # Same rule as the validator: a page built before this feature existed
        # is not a regression, it is just older. Skip rather than fail - and
        # never dereference an element that may not be there, which is how this
        # check took the whole pipeline down with a TypeError.
        has_toggle = page.evaluate("() => !!document.getElementById('bkt')")
        if s["booked"] and not has_toggle:
            print("  note: page predates the booked-panel toggle - checks skipped")
        if s["booked"] and has_toggle:
            listed = "() => {const u = document.getElementById('bkl');" \
                     " return !!u && u.getBoundingClientRect().height > 0}"
            check("the booked list starts open", page.evaluate(listed))
            act("the booked panel minimises", lambda: page.click("#bkt"))
            page.wait_for_timeout(200)
            check("minimising hides the list", not page.evaluate(listed))
            check("minimised, the heading and count still show",
                  page.evaluate("() => /booked classes \\(\\d+\\)/i.test("
                                "document.getElementById('bkt').textContent)"))
            check("the panel itself is still visible when minimised",
                  page.eval_on_selector("#booked", "e => e.getBoundingClientRect().height > 0"))
            page.reload(); page.wait_for_timeout(400)
            check("minimised is remembered across a reload", not page.evaluate(listed))
            act("the booked panel opens again", lambda: page.click("#bkt"))
            page.wait_for_timeout(200)
            check("opening it again works", page.evaluate(listed))
            page.reload(); page.wait_for_timeout(400)
            check("open is remembered too", page.evaluate(listed))

        # --- desktop: the filters scroll away and leave a strip ---------------
        # They used to be sticky, holding the top of the window for 2000 rows.
        if page.evaluate("() => !!document.getElementById('minibar')"):
            strip = "() => document.getElementById('minibar').classList.contains('on')"
            floating = "() => document.getElementById('filters').classList.contains('float')"
            page.evaluate("() => window.scrollTo(0, 0)"); page.wait_for_timeout(250)
            check("desktop: no filter strip at the top of the page",
                  not page.evaluate(strip))
            check("desktop: the filter bar is not sticky",
                  page.eval_on_selector("#filters",
                      "e => getComputedStyle(e).position !== 'sticky'"))
            page.evaluate("() => window.scrollTo(0, 1400)"); page.wait_for_timeout(300)
            check("desktop: the strip appears once the filters scroll away",
                  page.evaluate(strip))
            check("desktop: the filters really did scroll off",
                  page.eval_on_selector("#filters",
                      "e => e.getBoundingClientRect().bottom <= 0"))
            act("desktop: the strip expands", lambda: page.click("#mbt"))
            page.wait_for_timeout(300)
            check("desktop: expanding floats the real filter bar", page.evaluate(floating))
            check("desktop: the expanded panel is on screen",
                  page.eval_on_selector("#filters", "e => {const r = e.getBoundingClientRect();"
                                        "return r.top >= 0 && r.top < 120 && r.height > 40}"))
            rows_before = state()["rows"]
            act("desktop: filtering from the floating panel", lambda: page.evaluate(
                "() => {const x = document.getElementById('allCatB'); x.checked = false;"
                " x.dispatchEvent(new Event('change', {bubbles: true}))}"))
            page.wait_for_timeout(300)
            check("desktop: the floating panel still filters the table",
                  state()["rows"] < rows_before)
            check("desktop: the strip's count follows the table",
                  page.evaluate("() => (document.getElementById('mshown').textContent || '')"
                                ".indexOf(String(document.querySelectorAll("
                                "'#tb tr:not(.day)').length)) === 0"))
            act("desktop: restore", lambda: page.evaluate(
                "() => {const x = document.getElementById('allCatB'); x.checked = true;"
                " x.dispatchEvent(new Event('change', {bubbles: true}))}"))
            page.wait_for_timeout(250)
            page.keyboard.press("Escape"); page.wait_for_timeout(300)
            check("desktop: Escape closes the panel", not page.evaluate(floating))
            check("desktop: the strip stays while still scrolled down", page.evaluate(strip))
            page.evaluate("() => window.scrollTo(0, 0)"); page.wait_for_timeout(300)
            check("desktop: the strip goes away back at the top", not page.evaluate(strip))

        # --- mobile: one hamburger, everything else inside it ----------------
        # The controls are MOVED into the drawer, never copied: two copies of a
        # checkbox is two sources of truth, and they drift apart silently.
        page.set_viewport_size({"width": 390, "height": 844})
        page.wait_for_timeout(400)
        onscreen = lambda sel: page.eval_on_selector(sel, """e => {
          const r = e.getBoundingClientRect(), st = getComputedStyle(e);
          return r.width > 0 && r.height > 0 && st.visibility !== 'hidden'
                 && st.display !== 'none' && r.left < window.innerWidth && r.right > 0;
        }""")
        check("phone: the top bar with the menu button is shown", onscreen("#topbar"))
        check("phone: the desktop header is hidden", not onscreen("header"))
        check("phone: the filter bar is parked off-screen", not onscreen(".bar"))
        check("phone: the schedule is still the page", onscreen("#main table"))
        check("phone: the page never scrolls sideways",
              page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 1"),
              page.evaluate("() => [document.documentElement.scrollWidth, window.innerWidth]"))
        check("phone: the menu button is a real tap target",
              page.eval_on_selector("#mnu", "e => {const r = e.getBoundingClientRect();"
                                    "return r.width >= 44 && r.height >= 44}"))
        rows_before = state()["rows"]
        act("phone: the menu opens", lambda: page.click("#mnu"))
        page.wait_for_timeout(350)
        check("phone: the menu is open", onscreen("#drawer"))
        for label, sel in [("the filters", "#dbody .bar #catsB"),
                           ("the booked panel", "#dbody #booked"),
                           ("the legend", "#dbody #lg"),
                           ("the studio links and dates", "#dbody .sub"),
                           ("the favourites row", "#dbody #favB"),
                           ("the collapse toggle", "#dbody #colB")]:
            check("phone: %s is in the menu" % label,
                  page.evaluate("() => !!document.querySelector('%s')" % sel))
        check("phone: no control was duplicated",
              page.evaluate("() => document.querySelectorAll('.bar').length === 1"
                            " && document.querySelectorAll('#catsB').length === 1"))
        check("phone: the page behind does not scroll while the menu is open",
              page.evaluate("() => getComputedStyle(document.body).overflow === 'hidden'"))
        act("phone: a filter inside the menu is usable", lambda: page.evaluate(
            "() => {const x = document.getElementById('allCatB'); x.checked = false;"
            " x.dispatchEvent(new Event('change', {bubbles: true}))}"))
        page.wait_for_timeout(300)
        rows_filtered = state()["rows"]
        check("phone: filtering from the menu still filters the table",
              rows_filtered < rows_before, f"{rows_before} -> {rows_filtered}")
        act("phone: restore the filter", lambda: page.evaluate(
            "() => {const x = document.getElementById('allCatB'); x.checked = true;"
            " x.dispatchEvent(new Event('change', {bubbles: true}))}"))
        page.wait_for_timeout(250)
        act("phone: tapping outside closes the menu", lambda: page.mouse.click(8, 500))
        page.wait_for_timeout(350)
        closed = "() => !document.getElementById('drawer').classList.contains('open')"
        check("phone: tapping outside closed it", page.evaluate(closed))
        act("phone: reopen", lambda: page.click("#mnu")); page.wait_for_timeout(300)
        act("phone: Done closes it", lambda: page.click("#dclose")); page.wait_for_timeout(350)
        check("phone: Done closed it", page.evaluate(closed))
        act("phone: reopen again", lambda: page.click("#mnu")); page.wait_for_timeout(300)
        page.keyboard.press("Escape"); page.wait_for_timeout(350)
        check("phone: Escape closed it", page.evaluate(closed))
        check("phone: scrolling is restored after closing",
              page.evaluate("() => getComputedStyle(document.body).overflow !== 'hidden'"))

        # Back to desktop: every block must return to where it was.
        page.set_viewport_size({"width": 1280, "height": 900})
        page.wait_for_timeout(450)
        check("desktop: the top bar is gone", not onscreen("#topbar"))
        check("desktop: the header is back", onscreen("header"))
        check("desktop: the filter bar is back in the page", onscreen(".bar"))
        check("desktop: the booked panel sits above the table again",
              page.evaluate("() => !!(document.getElementById('booked')"
                            ".compareDocumentPosition(document.getElementById('main'))"
                            " & Node.DOCUMENT_POSITION_FOLLOWING)"))
        check("desktop: still one copy of every control",
              page.evaluate("() => document.querySelectorAll('#catsB').length === 1"))

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
