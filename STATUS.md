# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-08-19 23:11:05 refresh exit 3` |
| index.html modified | 2026-08-19 23:06:06 BST |
| Classes in index.html | 1943 |

## Last scrape failure

```
  File "/Users/danielcrabbe14/Sites/jynk/blok/scraper/refresh.py", line 214, in main
    from playwright.sync_api import sync_playwright
ModuleNotFoundError: No module named 'playwright'
----- 2026-08-19 07:11:05 refresh exit 0
----- 2026-08-19 11:11:05 refresh start (python: /usr/bin/python3)
FATAL: playwright not installed for /usr/bin/python3
       fix: /usr/bin/python3 -m pip install playwright && /usr/bin/python3 -m playwright install chromium
----- 2026-08-19 11:11:05 refresh exit 3
----- 2026-08-19 15:11:05 refresh start (python: /usr/bin/python3)
FATAL: playwright not installed for /usr/bin/python3
       fix: /usr/bin/python3 -m pip install playwright && /usr/bin/python3 -m playwright install chromium
----- 2026-08-19 15:11:05 refresh exit 3
----- 2026-08-19 19:11:05 refresh start (python: /usr/bin/python3)
FATAL: playwright not installed for /usr/bin/python3
       fix: /usr/bin/python3 -m pip install playwright && /usr/bin/python3 -m playwright install chromium
----- 2026-08-19 19:11:05 refresh exit 3
----- 2026-08-19 23:11:05 refresh start (python: /usr/bin/python3)
FATAL: playwright not installed for /usr/bin/python3
       fix: /usr/bin/python3 -m pip install playwright && /usr/bin/python3 -m playwright install chromium
----- 2026-08-19 23:11:05 refresh exit 3
```

## Recent push errors

```
2026-08-19 12:21:03  BLOCKED: FAIL: data array 'var D=[' not found
```
