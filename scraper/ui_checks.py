# -*- coding: utf-8 -*-
"""UI checks that must hold on BOTH index.html (BLOK) and 3rdspace.html (Third Space).

The two pages are built from one template (refresh.py), so every filter, finder,
tooltip and disabled-filter behaviour is meant to be identical. This module is
the single place those behaviours are asserted, and test-baseline.py and
test-thirdspace.py both call run(). To keep the pages in sync, a new shared
feature gets ONE check here; it then runs against both.

Nothing here names a particular class or club: it works from whatever the page
holds, so BLOK and Third Space can differ in content and still share the checks.
page-specific facts go in the cfg dict:
    cfg["locations"]  True when the page has location switches (Third Space, BLOK)
"""

ROWS = "() => document.querySelectorAll('#tb tr[data-cat]').length"

def run(page, check, act, cfg=None):
    cfg = cfg or {}
    rows = lambda: page.evaluate(ROWS)
    ev = page.evaluate
    # saved choices (collapsed sections, ticks, favourites) must not leak between checks
    ev("() => { try { localStorage.clear() } catch (e) {} }")
    page.reload()
    page.wait_for_timeout(700)
    n_all = rows()

    # --- the filter bar ---------------------------------------------------
    check("shared: a keyword search box", ev("() => !!document.getElementById('q')"))
    check("shared: Locations (when present) has an 'all' toggle on its title",
          ev("() => { const m = document.getElementById('allLoc'); const l = document.getElementById('locs');"
             " return !l || (!!m && !!m.closest('h3')) }"))
    check("shared: 'more' and 'all' share a line above the class chips",
          ev("""() => { const row = document.getElementById('cats' + VENUES[0]);
            const h = row.querySelector('.hd').getBoundingClientRect(), c = row.querySelector('.chip');
            return !c || c.getBoundingClientRect().top >= h.bottom - 2 }"""))
    check("shared: filter checkboxes carry the class colour, with no colour dots",
          ev("() => { const i = document.querySelector('input[data-c]');"
             " return !!i.style.getPropertyValue('--c') && !document.querySelector('.grp .chip .dot') }"))
    check("shared: the Not available section starts hidden",
          ev("() => document.getElementById('dis').style.display === 'none'"))

    # --- search ------------------------------------------------------------
    word = ev("""() => { const c = Object.keys(DESC).find(k => DESC[k] && DESC[k].length > 40);
      if (!c) return null; const w = DESC[c].toLowerCase().split(/[^a-z]+/).filter(x => x.length > 5); return w[0] || null }""")
    if word:
        page.fill("#q", word)
        page.wait_for_timeout(300)
        n = rows()
        check("shared: searching description text narrows the schedule (%s)" % word, 0 < n < n_all, "%d -> %d" % (n_all, n))
        check("shared: the class-type filters narrow with it",
              ev("() => [...document.querySelectorAll('#cats' + VENUES[0] + ' .chip, #fav' + VENUES[0] + ' .chip')]"
                 ".some(c => c.style.display === 'none')"))
    page.fill("#q", "zzzznothing")
    page.wait_for_timeout(250)
    check("shared: a search with no match shows nothing", rows() == 0, rows())
    page.fill("#q", "")
    page.wait_for_timeout(250)
    check("shared: clearing the search restores the schedule", rows() == n_all, "%d vs %d" % (rows(), n_all))

    # --- Legs only + the Not available section ----------------------------
    has_legs = ev("() => Object.keys(FOCUS).some(c => FOCUS[c] === 'Legs')")
    check("shared: some class is tagged Legs", has_legs)
    if has_legs:
        check("shared: the Legs filter is on show",
              ev("() => document.getElementById('legsl').style.display !== 'none'"))
        n_cat = ev("() => document.querySelectorAll('input[data-c]').length")
        page.evaluate("() => { const l = document.getElementById('legs'); l.checked = true;"
                      " l.dispatchEvent(new Event('change', {bubbles: true})) }")
        page.wait_for_timeout(350)
        check("shared: Legs only leaves only Legs classes",
              ev("() => { const r = [...document.querySelectorAll('#tb tr[data-cat]')];"
                 " return r.length > 0 && r.every(x => FOCUS[x.dataset.cat] === 'Legs') }"))
        check("shared: Legs rows carry the LEGS marker",
              ev("() => [...document.querySelectorAll('#tb tr[data-cat]')].every(r => !!r.querySelector('.legsb'))"))
        check("shared: filters it makes useless move into Not available, collapsed, with a count",
              ev("() => { const d = document.getElementById('dis');"
                 " return d.style.display !== 'none' && document.getElementById('disbody').style.display === 'none'"
                 " && /\\(\\d+\\)/.test(document.getElementById('disbtn').textContent) }"))
        check("shared: the count equals what the section holds",
              ev("() => document.getElementById('disn').textContent === '(' + document.getElementById('disrow').children.length + ')'"))
        check("shared: no class type is lost or duplicated as a live checkbox",
              ev("() => document.querySelectorAll('input[data-c]').length") == n_cat)
        check("shared: unavailable checkboxes are disabled",
              ev("() => [...document.querySelectorAll('#disrow > .chip:not(.ghost) input[data-c]')].every(i => i.disabled)"))
        if ev("() => document.getElementById('disbody').style.display === 'none'"):
            page.click("#disbtn")
        page.wait_for_timeout(200)
        check("shared: the section opens and still shows its count",
              ev("() => document.getElementById('disbody').style.display !== 'none' && /\\(\\d+\\)/.test(document.getElementById('disbtn').textContent)"))
        check("shared: the heading is not bold",
              ev("() => parseInt(getComputedStyle(document.getElementById('disbtn')).fontWeight) < 600"))
        check("shared: reasons are not printed on the chips",
              ev("() => ![...document.querySelectorAll('#disrow > .chip')].some(c => /Legs only/.test(c.textContent))"))
        first = ev("() => { const c = document.querySelector('#disrow > .chip:not(.ghost) label.chip'); return !!c }")
        if first:
            page.hover("#disrow > .chip:not(.ghost) label.chip >> nth=0")
            page.wait_for_timeout(250)
            tip = ev("() => document.getElementById('tip').textContent")
            check("shared: an unavailable item's tooltip gives the reason and no description",
                  "Not available: Legs only" in tip and len(tip) < 260, tip[:120])
            check("shared: the reason is the second thing on the card, right after the title",
                  ev("() => { const c = document.getElementById('tip').children;"
                     " return c.length > 1 && c[0].tagName === 'B' && c[1].classList.contains('wy') }"))
            page.mouse.move(5, 5)

        # a starred class that becomes unavailable stays in favourites and is listed again below
        name = ev("() => { const c = document.querySelector('#disrow > .chip:not(.ghost) .star'); return c ? c.title.replace(/^Favourite /, '') : null }")
        if name:
            page.evaluate("(n) => { const b = [...document.querySelectorAll('#disrow .star')].find(s => s.title === 'Favourite ' + n); b.click() }", name)
            page.wait_for_timeout(300)
            check("shared: an unavailable favourite stays in the favourites row, greyed",
                  ev("(n) => [...document.querySelectorAll('#fav' + VENUES[0] + ' > .chip.off')].some(c => c.textContent.indexOf(n) === 0)", name))
            check("shared: ...and is listed again in Not available",
                  ev("(n) => [...document.querySelectorAll('#disrow > .ghost')].some(c => c.textContent.indexOf(n) === 0)", name))
            check("shared: the copy is not a second live checkbox",
                  ev("(n) => [...document.querySelectorAll('input[data-c]')].filter(i => i.dataset.c === n).length", name) == 1)
            page.evaluate("(n) => { const b = [...document.querySelectorAll('#fav' + VENUES[0] + ' .star')].find(s => s.title === 'Unfavourite ' + n); b.click() }", name)
            page.wait_for_timeout(300)
            check("shared: un-starring it leaves no duplicate behind",
                  ev("(n) => [...document.querySelectorAll('#disrow > .chip')].filter(c => c.textContent.indexOf(n) === 0).length", name) == 1)
        page.evaluate("() => { const l = document.getElementById('legs'); l.checked = false;"
                      " l.dispatchEvent(new Event('change', {bubbles: true})) }")
        page.wait_for_timeout(350)
        check("shared: relaxing the filter brings everything back and hides the section",
              ev("() => document.getElementById('dis').style.display === 'none' && document.getElementById('disrow').children.length === 0")
              and rows() == n_all)
        check("shared: every tick survives the round trip",
              ev("() => [...document.querySelectorAll('input[data-c]')].every(i => i.checked)"))

    # --- tooltips ----------------------------------------------------------
    page.mouse.move(5, 5)
    page.hover("#cats%s input[data-desc] >> nth=0" % ev("() => VENUES[0]"))
    page.wait_for_timeout(250)
    tip = ev("() => document.getElementById('tip').textContent")
    check("shared: a filter's tooltip has a title, the clubs/studios and the description", len(tip) > 40, tip[:100])
    check("shared: the tooltip never says 'Length' or 'At:'", "Length" not in tip and "At: " not in tip, tip[:100])
    check("shared: the tooltip gives the class length in minutes", ev("() => /\\d+( \\/ \\d+|\\u2013\\d+)? min/.test(document.getElementById('tip').textContent)"))
    page.mouse.move(5, 5)
    page.hover("#cats%s label.chip > span >> nth=0" % ev("() => VENUES[0]"))
    page.wait_for_timeout(200)
    check("shared: hovering a filter's NAME shows no tooltip (only the checkbox does)",
          ev("() => document.getElementById('tip').style.display !== 'block'"))
    page.mouse.move(5, 5)

    # --- neighbours of a class in the timetable ----------------------------
    pick = ev("""() => { const rows = [...document.querySelectorAll('#tb tr[data-cat]')];
      for (const tr of rows) { const st = +tr.dataset.mins, du = +tr.dataset.dur, club = tr.dataset.club, d = tr.dataset.d;
        const nx = D.filter(r => r[0] === d && r[6] === club && r[1] >= st + du && r[1] <= st + du + 90);
        if (nx.length) return rows.indexOf(tr); } return null }""")
    check("shared: some class has a class straight after it to test with", pick is not None)
    if pick is not None:
        page.hover("#tb tr[data-cat] .pill >> nth=%d" % pick)
        page.wait_for_timeout(300)
        t = ev("() => document.getElementById('tip').textContent")
        check("shared: hovering a class lists what runs straight after it at that club",
              "Straight after" in t and ("gap" in t or "back to back" in t), t[:120])
        check("shared: the before/after block is the last thing in the tooltip",
              ev("() => { const tip = document.getElementById('tip'); return tip.lastElementChild.classList.contains('ttn') }"))
        both = ev("() => { const h = [...document.querySelectorAll('#tip .ttn i.tt')].map(i => i.textContent); return h }")
        if len(both) == 2:
            check("shared: the 'before' section sits above the 'after' section",
                  both[0].startswith("Just before") and both[1].startswith("Straight after"), both)
        page.mouse.move(5, 5)

    # --- locations ---------------------------------------------------------
    if ev("() => !!document.getElementById('locs')"):
        check("shared: every location has a facilities badge with a number",
              ev("() => [...document.querySelectorAll('#locs label')].every(l => /^\\d+$/.test(((l.querySelector('.fbadge') || {}).textContent || '')))")
              or not cfg.get("facilities", True))
        page.fill("#q", "")
        n_loc = rows()
        page.evaluate("() => { const m = document.getElementById('allLoc'); m.checked = false; m.dispatchEvent(new Event('change', {bubbles: true})) }")
        page.wait_for_timeout(300)
        check("shared: untick all switches every location off", rows() == 0, rows())
        page.evaluate("() => { const m = document.getElementById('allLoc'); m.checked = true; m.dispatchEvent(new Event('change', {bubbles: true})) }")
        page.wait_for_timeout(300)
        check("shared: tick all brings every location back", rows() == n_loc, "%d vs %d" % (rows(), n_loc))
        check("shared: opening hours (when the site has them) sit on a new line under the name",
              ev("""() => [...document.querySelectorAll('#locs label')].every(l => { const h = l.querySelector('.n'); if (!h) return true;
                 const n = l.querySelector('span').getBoundingClientRect(), r = h.getBoundingClientRect(); return r.top > n.bottom - 2 })"""))

    # --- the header --------------------------------------------------------
    check("shared: the title carries a human-friendly 'updated' time when the build time is known",
          ev("() => !BUILT || /updated (just now|\\d+ (minute|hour|day)s? ago)/.test(document.querySelector('header h1').textContent)"))
