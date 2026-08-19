#!/usr/bin/env python3
"""
class-descriptions.py — ONE-OFF. Not part of the 4-hourly refresh.

Walks each studio's schedule, collects the link behind every class name, then
reads that class page's og:description (what ClassPass shows as the class
blurb). Writes class-descriptions.json and CLASS-TYPES.md next to this file.

Run it by hand when the studios add new class types:

    python3 class-descriptions.py            # all three studios
    python3 class-descriptions.py --days 8   # walk fewer days (faster)

Deliberately NOT wired into launchd: descriptions change maybe twice a year,
and each run costs ~100 page fetches.
"""
import json, re, sys, datetime, pathlib, argparse

HERE = pathlib.Path(__file__).resolve().parent
AUTH = HERE / "auth_state.json"
STUDIOS = [("BLOK (Clapton & Shoreditch)", ["blok-clapton-london", "blok-shoreditch-london"]),
           ("Mission E1",                  ["mission-e1-london"])]

COLLECT_JS = r"""
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  for (let i = 0; i < 80; i++) {
    const b = [...document.querySelectorAll('button')].find(x => /see more/i.test(x.textContent));
    if (!b) break;
    b.click();
    await sleep(150);
  }
  const out = {};
  document.querySelectorAll('.Schedule__rows section h3 a').forEach(a => {
    const n = a.textContent.trim();
    if (!out[n]) out[n] = a.getAttribute('href').split('#')[0];
  });
  return out;
}
"""

def log(*a): print(*a, flush=True)

def collect(page, slug, days):
    page.goto("https://classpass.com/studios/" + slug, timeout=60000)
    page.wait_for_timeout(4000)
    links = {}
    for _ in range(days):
        links.update(page.evaluate(COLLECT_JS))
        nxt = page.query_selector('button[aria-label="Next day"]')
        if not nxt: break
        nxt.click()
        page.wait_for_timeout(2400)
    log("  %s: %d class types" % (slug, len(links)))
    return links

def describe(page, href):
    """Read og:description off the class page. Empty string = studio never wrote one."""
    js = """async (u) => {
      const t = await (await fetch(u, {credentials: 'include'})).text();
      const og = new DOMParser().parseFromString(t, 'text/html')
        .querySelector('meta[property="og:description"]');
      return og ? og.content.trim() : '';
    }"""
    try:
        return page.evaluate(js, "https://classpass.com" + href)
    except Exception as e:
        return "ERROR: %s" % e

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=13)
    args = ap.parse_args()
    from playwright.sync_api import sync_playwright
    merged = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(storage_state=str(AUTH) if AUTH.exists() else None)
        page = ctx.new_page()
        for label, slugs in STUDIOS:
            links = {}
            for slug in slugs:
                links.update(collect(page, slug, args.days))
            entry = {}
            for i, (name, href) in enumerate(sorted(links.items()), 1):
                entry[name] = {"description": describe(page, href),
                               "url": "https://classpass.com" + href}
                if i % 10 == 0: log("    %d/%d described" % (i, len(links)))
            merged[label] = entry
            got = sum(1 for v in entry.values() if v["description"])
            log("  %s: %d types, %d with a description" % (label, len(entry), got))
        browser.close()

    (HERE / "class-descriptions.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")

    out = ["# Class type descriptions", "",
           "Scraped from ClassPass class pages (`og:description`) on %s."
           % datetime.date.today().strftime("%-d %b %Y"), ""]
    for label, classes in merged.items():
        have = [(n, c) for n, c in classes.items() if c["description"]]
        miss = [n for n, c in classes.items() if not c["description"]]
        out += ["## %s" % label, "",
                "%d class types, %d with a description on ClassPass." % (len(classes), len(have)), ""]
        for n, c in have:
            out += ["### %s" % n, "", c["description"], ""]
        if miss:
            out += ["### No description published", "",
                    "ClassPass has no `og:description` for these — the studio has not written one:", ""]
            out += ["- %s" % m for m in miss] + [""]
    (HERE / "CLASS-TYPES.md").write_text("\n".join(out), encoding="utf-8")
    log("wrote class-descriptions.json and CLASS-TYPES.md")

if __name__ == "__main__":
    sys.exit(main())
