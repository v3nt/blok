# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-08-26 23:25:50 refresh FAILED (exit 1)` |
| index.html modified | 2026-08-26 23:24:51 BST |
| Classes in index.html | 1943 |

## Last scrape failure

```
----- 2026-08-26 11:25:36 refresh start (python: /usr/bin/python3)
FATAL: playwright not installed for /usr/bin/python3
       fix: /usr/bin/python3 -m pip install playwright && /usr/bin/python3 -m playwright install chromium
----- 2026-08-26 11:25:36 refresh exit 3
----- 2026-08-26 15:25:36 refresh start (python: /usr/bin/python3)
FATAL: playwright not installed for /usr/bin/python3
       fix: /usr/bin/python3 -m pip install playwright && /usr/bin/python3 -m playwright install chromium
----- 2026-08-26 15:25:36 refresh exit 3
----- 2026-08-26 19:25:36 refresh start (python: /usr/bin/python3)
FATAL: playwright not installed for /usr/bin/python3
       fix: /usr/bin/python3 -m pip install playwright && /usr/bin/python3 -m playwright install chromium
----- 2026-08-26 19:25:36 refresh exit 3
----- 2026-08-26 23:25:36 refresh start (python: /usr/bin/python3)
BLOK refresh 2026-08-26 23:25:36
  ! no auth_state.json - your booked classes will not be marked. Run login_setup.py once.
  Clapton -> 0 classes  []
  Shoreditch -> 0 classes  []
  Mission E1 -> 0 classes  []
FATAL: no rows scraped - leaving /Users/danielcrabbe14/Sites/jynk/blok/index.html untouched
----- 2026-08-26 23:25:50 refresh FAILED (exit 1)
```

## Recent push errors

```
2026-08-26 16:20:26  BLOCKED: FAIL: data array 'var D=[' not found
2026-08-26 23:21:42  BLOCKED: baseline regression
```
