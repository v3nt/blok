#!/usr/bin/env python3
"""Gate: refuse to publish an index.html whose <script> block cannot parse.

The 19 Aug 2026 outage was a generated index.html with one unclosed '{'.
The browser threw "Unexpected end of input", D was never defined, and the
page rendered an empty table. Nothing in the pipeline noticed, because the
file was well-formed HTML and the commit counted rows via grep on the raw
text - which happily counts rows inside broken JavaScript.

Exit 0 = safe to publish. Exit 1 = do not commit.
"""
import json
import os
import re
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "index.html"

try:
    html = open(PATH, encoding="utf-8").read()
except OSError as e:
    print(f"FAIL: cannot read {PATH}: {e}")
    sys.exit(1)

blocks = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
if not blocks:
    print("FAIL: no <script> block found")
    sys.exit(1)

js = "\n".join(blocks)

# Balance check that ignores brackets inside string literals and comments.
stack, i, n = [], 0, len(js)
pairs = {")": "(", "]": "[", "}": "{"}
while i < n:
    c = js[i]
    if c in "\"'`":
        quote, i = c, i + 1
        while i < n and js[i] != quote:
            i += 2 if js[i] == "\\" else 1
        i += 1
        continue
    if c == "/" and i + 1 < n and js[i + 1] == "/":
        i = js.find("\n", i)
        if i == -1:
            break
        continue
    if c == "/" and i + 1 < n and js[i + 1] == "*":
        i = js.find("*/", i)
        if i == -1:
            print("FAIL: unterminated block comment")
            sys.exit(1)
        i += 2
        continue
    if c in "([{":
        stack.append(c)
    elif c in ")]}":
        if not stack or stack[-1] != pairs[c]:
            print(f"FAIL: unbalanced '{c}' at offset {i}")
            sys.exit(1)
        stack.pop()
    i += 1

if stack:
    print(f"FAIL: {len(stack)} unclosed {' '.join(stack[-5:])} - "
          "browser will throw 'Unexpected end of input' and render nothing")
    sys.exit(1)

# The data array must exist and be non-trivial.
m = re.search(r"var\s+D\s*=\s*\[", js)
if not m:
    print("FAIL: data array 'var D=[' not found")
    sys.exit(1)

rows = len(re.findall(r'\["\d{4}-\d{2}-\d{2}",', js))
if rows < 20:
    print(f"FAIL: only {rows} class rows in D - refusing to publish an empty schedule")
    sys.exit(1)

# --------------------------------------------------------------- UI contract
# The schedule UI has been silently replaced more than once by a generator that
# drops features nobody re-described. These markers ARE the agreed UI: two
# filter groups (Mission E1 and BLOK), each with its own favourites row above
# its non-favourites, and a select/deselect-all per group. A page missing any
# of them is a regression, not a refresh - reject it and keep the last good
# version live.
REQUIRED = {
    "DEFAULT_FAVS=": "default favourites on first load",
    "DESC=":         "class descriptions for the hover tooltip",
    "STUDIO_URL=":   "studio names linking out",
    "VENUES=":       "the venue codes the filters are built from",
    "ORDER=":        "per-venue category order",
    # mobile: the hamburger and the drawer it fills must survive every rebuild
    'id="topbar"': "mobile top bar",
    'id="mnu"':    "mobile hamburger button",
    'id="drawer"': "mobile menu drawer",
    'id="dbody"':  "mobile menu contents",
    'id="scrim"':  "mobile menu backdrop",
    'class="sub"': "header line the drawer moves into the menu",
    'id="minibar"':  "collapsed filter strip",
    'id="mbt"':      "filter strip expand button",
    'id="bkt"':      "booked panel minimise toggle",
}

# Per-venue controls are checked against the page's OWN venue list, so this
# gate works for any page the builder makes - index.html (BLOK / Mission E1)
# and 3rdspace.html (Islington / Moorgate / City) alike.
venues = re.search(r'VENUES=(\[[^\]]*\])', html)
if venues:
    try:
        for code in json.loads(venues.group(1)):
            for tpl, what in (('id="fav%s"', "favourites row"),
                              ('id="cats%s"', "filter list"),
                              ('id="allFav%s"', "favourites select-all"),
                              ('id="allCat%s"', "non-favourites select-all"),
                              ('id="col%s"', "collapse toggle")):
                REQUIRED[tpl % code] = "%s for venue %s" % (what, code)
    except Exception as e:
        print("FAIL: cannot read VENUES out of the page (%s)" % e)
        sys.exit(1)
else:
    print("FAIL: no VENUES list - the filters cannot have been built")
    sys.exit(1)

# The page must save its settings somewhere, and each venue must have its own
# key: index.html and 3rdspace.html share an origin, so a shared key would let
# one page's filters overwrite the other's.
ls = re.search(r'var LS=(\{.*?\});', html, re.S)
if not ls:
    print("FAIL: no LS key map - nothing would be remembered")
    sys.exit(1)
try:
    keys = json.loads(ls.group(1))
    missing_keys = [k for k in ("a", "f", "w", "t", "v", "vv", "c", "bk") if k not in keys]
    if missing_keys:
        print("FAIL: LS is missing %s" % ", ".join(missing_keys)); sys.exit(1)
    per_venue = keys["t"]
    if len(set(per_venue.values())) != len(per_venue):
        print("FAIL: two venues share a storage key: %r" % per_venue); sys.exit(1)
except SystemExit:
    raise
except Exception as e:
    print("FAIL: cannot read the LS key map (%s)" % e); sys.exit(1)
missing = [(marker, what) for marker, what in REQUIRED.items() if marker not in html]

# A marker missing from this page is only a REGRESSION if the published page
# has it. When a feature is added to the generator, the page on disk predates
# it until the next scrape rebuilds - and failing there blocks every publish
# of a schedule that is otherwise perfectly good. That has now cost three
# separate outages, all self-inflicted by a gate that was too eager:
#   - the whole point of this gate is "do not go backwards"
#   - "not built yet" is not backwards
def published():
    """index.html as last committed, or None when git cannot say."""
    try:
        import subprocess
        r = subprocess.run(["git", "show", "HEAD:index.html"],
                           capture_output=True, text=True, timeout=20,
                           cwd=os.path.dirname(os.path.abspath(__file__)) or ".")
        return r.stdout if r.returncode == 0 and r.stdout else None
    except Exception:
        return None

if missing:
    live = published()
    if live is None:
        # No baseline to compare against: fall back to the strict rule rather
        # than waving a page through on a git failure.
        print("FAIL: UI regression - missing " +
              "; ".join(w for _, w in missing) + " (no published page to compare)")
        sys.exit(1)
    regressed = [w for mk, w in missing if mk in live]
    pending   = [w for mk, w in missing if mk not in live]
    if regressed:
        print("FAIL: UI regression - the published page has these and this one "
              "does not: " + "; ".join(regressed))
        sys.exit(1)
    print("note: not built yet (waiting on the next scrape): " + "; ".join(pending))

print(f"OK: script parses, {rows} class rows, UI contract intact")
sys.exit(0)

