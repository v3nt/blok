# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-06 10:13:20 refresh start (python: /usr/bin/python3)` |
| index.html modified | 2026-09-06 10:13:37 BST |
| Classes in index.html | 2071 |

## Last scrape failure

```
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

----- 2026-09-06 09:03:00 refresh FAILED (exit 1)
----- 2026-09-06 10:13:20 refresh start (python: /usr/bin/python3)
BLOK refresh 2026-09-06 10:13:20
  browser: chrome, visible window
  loaded 53 saved cookie(s)
  Clapton: consent banner - overlay removed x1
```

## Recent push errors

```
2026-09-06 10:13:37  BLOCKED: baseline regression
```
