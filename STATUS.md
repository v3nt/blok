# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-08-19 07:11:05 refresh exit 0` |
| index.html modified | 2026-08-19 08:30:42 BST |
| Classes in index.html | 1924 |

## Last scrape failure

```
----- 2026-08-19 07:11:04 refresh start
Traceback (most recent call last):
  File "/Users/danielcrabbe14/Sites/jynk/blok/scraper/refresh.py", line 246, in <module>
    sys.exit(main())
  File "/Users/danielcrabbe14/Sites/jynk/blok/scraper/refresh.py", line 214, in main
    from playwright.sync_api import sync_playwright
ModuleNotFoundError: No module named 'playwright'
----- 2026-08-19 07:11:05 refresh exit 0
```

## Recent push errors

```
2026-08-19 04:22:58  REBASE FAILED - manual fix needed
2026-08-19 07:10:30  REBASE FAILED - manual fix needed
2026-08-19 08:30:42  BLOCKED: FAIL: 3 unclosed { ( [ - browser will throw 'Unexpected end of input' and render nothing
```
