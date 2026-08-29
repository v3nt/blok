# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-08-29 16:05:05 refresh FAILED (exit 1)` |
| index.html modified | 2026-08-29 12:00:33 BST |
| Classes in index.html | 1754 |

## Last scrape failure

```

  Shoreditch -> 0 classes  []
  Mission E1 -> 0 classes  []
FATAL: no rows scraped - leaving /Users/danielcrabbe14/Sites/jynk/blok/index.html untouched
----- 2026-08-28 20:00:40 refresh FAILED (exit 1)
----- 2026-08-29 00:00:40 refresh start (python: /usr/bin/python3)
BLOK refresh 2026-08-29 00:00:41
  ! no auth_state.json - your booked classes will not be marked. Run login_setup.py once.
  Clapton: consent banner - declined: Reject
  Clapton -> 0 classes  []
  Shoreditch -> 0 classes  []
  Mission E1 -> 0 classes  []
FATAL: no rows scraped - leaving /Users/danielcrabbe14/Sites/jynk/blok/index.html untouched
----- 2026-08-29 00:01:43 refresh FAILED (exit 1)
----- 2026-08-29 12:54:50 refresh start (python: /usr/bin/python3)
SyntaxError: Non-UTF-8 code starting with '\xe2' in file /Users/danielcrabbe14/Sites/jynk/blok/scraper/refresh.py on line 2, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details
----- 2026-08-29 12:54:50 refresh FAILED (exit 1)
----- 2026-08-29 16:05:05 refresh start (python: /usr/bin/python3)
SyntaxError: Non-UTF-8 code starting with '\xe2' in file /Users/danielcrabbe14/Sites/jynk/blok/scraper/refresh.py on line 2, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details
----- 2026-08-29 16:05:05 refresh FAILED (exit 1)
```

## Recent push errors

```
2026-08-29 16:53:16  BLOCKED: baseline regression
2026-08-29 17:03:21  BLOCKED: baseline regression
2026-08-29 17:13:25  BLOCKED: baseline regression
```
