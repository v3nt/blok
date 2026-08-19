#!/usr/bin/env python3
"""Gate: refuse to publish an index.html whose <script> block cannot parse.

The 19 Aug 2026 outage was a generated index.html with one unclosed '{'.
The browser threw "Unexpected end of input", D was never defined, and the
page rendered an empty table. Nothing in the pipeline noticed, because the
file was well-formed HTML and the commit counted rows via grep on the raw
text - which happily counts rows inside broken JavaScript.

Exit 0 = safe to publish. Exit 1 = do not commit.
"""
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
    'id="favM"':  "Mission E1 favourites row",
    'id="catsM"': "Mission E1 filter list",
    'id="favB"':  "BLOK favourites row",
    'id="catsB"': "BLOK filter list",
    'id="allM"':  "Mission E1 select-all",
    'id="allB"':  "BLOK select-all",
    "orderB":     "BLOK category order",
    "orderM":     "Mission E1 category order",
    "blokFavs":   "saved favourites key",
    "DEFAULT_FAVS": "default favourites (calisthenics / strength) on first load",
}
missing = [what for marker, what in REQUIRED.items() if marker not in html]
if missing:
    print("FAIL: UI regression - missing " + "; ".join(missing))
    sys.exit(1)

print(f"OK: script parses, {rows} class rows, UI contract intact")
sys.exit(0)

