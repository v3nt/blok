# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-06 17:08:45 refresh FAILED (exit 1)` |
| index.html modified | 2026-09-06 14:45:35 BST |
| Classes in index.html | 2095 |

## Last scrape failure

```

  browser closed
FATAL: no rows scraped - leaving /Users/danielcrabbe14/Sites/jynk/blok/index.html untouched
  ! Clapton: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-clapton-london", waiting until "load"

  ! Shoreditch: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-shoreditch-london", waiting until "load"

  ! Mission E1: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/mission-e1-london", waiting until "load"

  ! could not read upcoming reservations: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/profile/upcoming", waiting until "load"

----- 2026-09-06 17:08:45 refresh FAILED (exit 1)
```

## Recent push errors

```
2026-09-06 10:13:37  BLOCKED: baseline regression
2026-09-06 11:58:27  BLOCKED: baseline regression
2026-09-06 14:45:35  BLOCKED: baseline regression
```
