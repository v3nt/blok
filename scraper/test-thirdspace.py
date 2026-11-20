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
    check("a switch for each club", sorted(locs) == ["Canary Wharf", "City", "Islington", "Marylebone", "Moorgate", "Soho", "Tower Bridge"], locs)
    for el in ("fav", "cats", "allFav", "allCat", "col"):
        check("the class list has #%s%s" % (el, codes[0]),
              page.evaluate("() => !!document.getElementById('%s%s')" % (el, codes[0])))
    check("the location switches are on the page",
          page.evaluate("() => document.querySelectorAll('#locs input[data-loc]').length") == 7)
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


    # --- favouriting from the schedule row --------------------------------
    # The star after a class tag is the same act as the star on its filter
    # chip: one list, one key, both views in step.
    star = "document.querySelector('#tb tr[data-cat] .rstar')"
    check("every class row has a star", page.evaluate(
        "() => document.querySelectorAll('#tb tr[data-cat]').length ==="
        " document.querySelectorAll('#tb tr[data-cat] .rstar').length"))
    cat = page.evaluate("() => {const r = document.querySelector('#tb tr[data-cat]');"
                        " return r && r.dataset.cat}")
    was = page.evaluate("() => %s.getAttribute('aria-pressed')" % star)
    act("the row star is clickable", lambda: page.evaluate("() => %s.click()" % star))
    page.wait_for_timeout(300)
    now = page.evaluate("() => %s.getAttribute('aria-pressed')" % star)
    check("clicking the row star flips it", now != was, "%s -> %s" % (was, now))
    check("the filter chip agrees with the row star",
          page.evaluate("""(c) => {
            const chip = [...document.querySelectorAll('.chip .star')].find(b =>
              (b.title || '').indexOf(c) > -1);
            return !!chip && chip.getAttribute('aria-pressed') === '%s';
          }""" % now, cat))
    check("favouriting from a row does not hide any class",
          page.evaluate("() => document.querySelectorAll('#tb tr[data-cat]').length") > 0)
    page.reload(); page.wait_for_timeout(500)
    check("a row favourite is remembered",
          page.evaluate("() => %s.getAttribute('aria-pressed')" % star) == now)
    act("put it back", lambda: page.evaluate("() => %s.click()" % star))
    page.wait_for_timeout(250)

    # --- legs focus + club hours + descriptions ------------------------------
    check("the Legs filter exists and is on show",
          page.evaluate("() => { const l = document.getElementById('legs');"
                        " return !!l && l.closest('label').style.display !== 'none' }"))
    check("LGA is tagged Legs", page.evaluate("() => FOCUS['LGA'] === 'Legs'"),
          page.evaluate("() => FOCUS['LGA']"))
    check("every class type has a focus entry, even if Untagged",
          page.evaluate("() => ORDER[VENUES[0]].every(c => !!FOCUS[c])"))
    check("Untagged types are not silently hidden by being absent",
          page.evaluate("() => ORDER[VENUES[0]].every(c => typeof FOCUS[c] === 'string')"))
    check("every class type has a tooltip, even if only the fallback",
          page.evaluate("() => ORDER[VENUES[0]].every(c => !!DESC[c])"))
    n_all = rows()
    page.evaluate("() => { const l = document.getElementById('legs'); l.checked = true;"
                  " l.dispatchEvent(new Event('change', {bubbles: true})) }")
    page.wait_for_timeout(300)
    n_legs = rows()
    check("Legs only shows fewer classes", 0 < n_legs < n_all, "%d -> %d" % (n_all, n_legs))
    check("every row left is a Legs class",
          page.evaluate("() => [...document.querySelectorAll('#tb tr[data-cat]')]"
                        ".every(r => FOCUS[r.dataset.cat] === 'Legs')"))
    check("those rows carry the LEGS marker",
          page.evaluate("() => [...document.querySelectorAll('#tb tr[data-cat]')]"
                        ".every(r => !!r.querySelector('.legsb'))"))
    page.reload(); page.wait_for_timeout(500)
    check("Legs only is remembered", rows() == n_legs, rows())
    page.evaluate("() => document.getElementById('reset').click()")
    page.wait_for_timeout(300)
    check("Reset filters clears Legs only", rows() == n_all, "%d vs %d" % (rows(), n_all))
    check("hours are written WD ..., WE ...",
          page.evaluate("() => [...document.querySelectorAll('#locs label')]"
                        ".every(l => /WD \\d+:\\d\\d.\\d+:\\d\\d, WE \\d+:\\d\\d.\\d+:\\d\\d/.test(l.textContent))"))
    act("hover a location", lambda: page.hover("#locs label >> nth=0"))
    page.wait_for_timeout(250)
    check("a location's tooltip lists its main facilities as bullets",
          page.evaluate("() => { const t = document.getElementById('tip').textContent;"
                        " return t.indexOf('Main facilities') > -1 && (t.match(/\\u2022/g) || []).length >= 3 }"))
    page.mouse.move(5, 5)
    check("locations are ordered by facilities, most first",
          page.evaluate("() => { const n = [...document.querySelectorAll('#locs label')].map(l => (l.getAttribute('data-desc') || '').split('\\u2022').length);"
                        " return n.every((v, i) => i === 0 || n[i - 1] >= v) }"))
    check("each club shows its opening hours next to its name",
          page.evaluate("() => [...document.querySelectorAll('#locs label')]"
                        ".every(l => /\\d\\d:\\d\\d/.test(l.textContent))"))

    check("a class-type filter shows its description on hover",
          page.evaluate("() => { const i = document.querySelector('#cats' + VENUES[0] + ' input[data-desc], #fav' + VENUES[0] + ' input[data-desc]');"
                        " return !!i && !!i.getAttribute('data-desc') }"))
    act("hovering a filter shows the description", lambda: page.hover("%s input[data-desc]" % ("#cats" + codes[0])))
    page.wait_for_timeout(200)
    check("the tooltip shows the description",
          page.evaluate("() => { const t = document.getElementById('tip');"
                        " return t.style.display === 'block' && t.textContent.length > 20 }"))
    check("'more' and 'all' sit together on their own line above the chips",
          page.evaluate("""() => { const row = document.getElementById('cats' + VENUES[0]);
            const col = row.querySelector('.col').getBoundingClientRect(), all = row.querySelector('.all').getBoundingClientRect();
            const first = row.querySelector('.chip').getBoundingClientRect();
            return Math.abs(col.top - all.top) < 4 && first.top > all.bottom - 2 }"""))
    check("the filter checkboxes carry the class colour and there are no colour dots",
          page.evaluate("() => { const i = document.querySelector('#cats' + VENUES[0] + ' input[data-c]');"
                        " return !!i.style.getPropertyValue('--c') && !document.querySelector('.grp .chip .dot') }"))
    page.mouse.move(5, 5)
    page.hover("#cats" + codes[0] + " label.chip > span")      # the name, not the checkbox
    page.wait_for_timeout(200)
    check("hovering the name does not show the tooltip",
          page.evaluate("() => document.getElementById('tip').style.display !== 'block'"))
    page.hover("#cats" + codes[0] + " input[data-desc]")
    page.wait_for_timeout(200)
    check("the tooltip gives the class length",
          page.evaluate("() => /Length: \\d+/.test(document.getElementById('tip').textContent)"))
    check("the tooltip says which clubs run the class",
          page.evaluate("() => /Islington|Moorgate|City|Canary Wharf|Tower Bridge|Soho/.test(document.getElementById('tip').textContent) && document.getElementById('tip').textContent.indexOf('At: ') === -1"))
    page.mouse.move(5, 5)
    # --- keyword search: name, type, focus and description text ---------------
    n0 = rows()
    page.fill("#q", "lower body")
    page.wait_for_timeout(300)
    n1 = rows()
    check("searching the descriptions narrows the schedule", 0 < n1 < n0, "%d -> %d" % (n0, n1))
    check("every class left matches the words",
          page.evaluate("() => [...document.querySelectorAll('#tb tr[data-cat]')].every(r => qmatch(r.dataset.cat))"))
    check("the class-type filters narrow too",
          page.evaluate("() => { const c = [...document.querySelectorAll('#cats' + VENUES[0] + ' .chip, #fav' + VENUES[0] + ' .chip')];"
                        " return c.some(x => x.style.display === 'none') && c.some(x => x.style.display !== 'none') }"))
    page.fill("#q", "zzzznothing")
    page.wait_for_timeout(250)
    check("a search with no match shows nothing", rows() == 0, rows())
    page.fill("#q", "")
    page.wait_for_timeout(250)
    check("clearing the search brings everything back", rows() == n0, "%d vs %d" % (rows(), n0))
    page.fill("#q", "squat")
    page.wait_for_timeout(250)
    page.evaluate("() => document.getElementById('reset').click()")
    page.wait_for_timeout(250)
    check("Reset filters clears the search",
          page.evaluate("() => document.getElementById('q').value") == "" and rows() == n0)

    # --- filters that your other filters make useless move to a disabled section ---
    check("the disabled section starts hidden",
          page.evaluate("() => document.getElementById('dis').style.display === 'none'"))
    n_cats = page.evaluate("() => document.querySelectorAll('#cats' + VENUES[0] + ' input[data-c]').length"
                           " + document.querySelectorAll('#fav' + VENUES[0] + ' input[data-c]').length")
    page.evaluate("() => { const l = document.getElementById('legs'); l.checked = true;"
                  " l.dispatchEvent(new Event('change', {bubbles: true})) }")
    page.wait_for_timeout(300)
    check("with Legs only, class types with no leg classes move to the disabled section",
          page.evaluate("() => document.getElementById('dis').style.display !== 'none'"
                        " && document.querySelectorAll('#disrow input[data-c]').length > 0"))
    check("the section is collapsed by default and shows how many are in it",
          page.evaluate("() => document.getElementById('disbody').style.display === 'none'"
                        " && /\\(\\d+\\)/.test(document.getElementById('disbtn').textContent)"))
    check("the count matches what is inside",
          page.evaluate("() => document.getElementById('disn').textContent ==="
                        " '(' + document.getElementById('disrow').children.length + ')'"))
    page.click("#disbtn")
    page.wait_for_timeout(200)
    check("the section opens and the count is still shown",
          page.evaluate("() => document.getElementById('disbody').style.display !== 'none'"
                        " && /\\(\\d+\\)/.test(document.getElementById('disbtn').textContent)"))
    check("the reason is not printed on the chips",
          page.evaluate("() => !document.querySelector('#disrow .why') && ![...document.querySelectorAll('#disrow .chip')]"
                        ".some(c => /Legs only/.test(c.textContent))"))
    check("each one carries its reason for the hover",
          page.evaluate("() => [...document.querySelectorAll('#disrow label.chip')]"
                        ".every(l => l.getAttribute('data-why') === 'Legs only')"))
    page.hover("#disrow label.chip >> nth=0")
    page.wait_for_timeout(250)
    check("hovering a disabled one shows why",
          page.evaluate("() => { const t = document.getElementById('tip');"
                        " return t.style.display === 'block' && t.textContent.indexOf('Not available: Legs only') > -1 }"))
    tip_txt = lambda: page.evaluate("() => document.getElementById('tip').textContent")
    label_tip = tip_txt()
    check("an unavailable item's tooltip has no description, just the top line and reason",
          "Not available: Legs only" in label_tip and "Soho" in label_tip and "Length: " in label_tip
          and len(label_tip) < 220, label_tip[:120])
    page.evaluate("() => document.getElementById('tip').style.display = 'none'")
    page.evaluate("""() => { const i = document.querySelector('#disrow input[data-c]');
        i.dispatchEvent(new MouseEvent('mouseover', {bubbles: true, clientX: 50, clientY: 50})) }""")
    page.wait_for_timeout(150)
    check("hovering its checkbox shows the same tooltip as its label", tip_txt() == label_tip,
          tip_txt()[:120])
    page.mouse.move(5, 5)
    check("the heading is not bold",
          page.evaluate("() => parseInt(getComputedStyle(document.getElementById('disbtn')).fontWeight) < 600"))
    check("those checkboxes are disabled",
          page.evaluate("() => [...document.querySelectorAll('#disrow input[data-c]')].every(i => i.disabled)"))
    check("the Legs classes stay in the normal list",
          page.evaluate("() => [...document.querySelectorAll('#cats' + VENUES[0] + ' label.chip, #fav' + VENUES[0] + ' label.chip')]"
                        ".some(l => /LGA/.test(l.textContent))"))
    check("no class type is lost between the lists",
          page.evaluate("() => document.querySelectorAll('input[data-c]').length") == n_cats)
    page.evaluate("() => { const l = document.getElementById('legs'); l.checked = false;"
                  " l.dispatchEvent(new Event('change', {bubbles: true})) }")
    page.wait_for_timeout(300)
    check("clearing the filter brings them back and hides the section",
          page.evaluate("() => document.getElementById('dis').style.display === 'none'"
                        " && document.querySelectorAll('#disrow input[data-c]').length === 0"))
    check("their ticks survive the round trip",
          page.evaluate("() => [...document.querySelectorAll('input[data-c]')].every(i => i.checked)"))

    check("the header is just the title with a human-friendly update time",
          page.evaluate("() => { const h = document.querySelector('header');"
                        " return !((h.querySelector('p.sub') || {textContent: ''}).textContent.trim()) && /updated (just now|\\d+ (minute|hour|day)s? ago)/.test(h.querySelector('h1').textContent)"
                        " && !/In the timetable/.test(h.textContent) }"))
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
