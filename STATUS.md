# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-09 02:55:29 refresh FAILED (exit 1)` |
| index.html modified | 2026-09-08 22:08:41 BST |
| Classes in index.html | 2001 |

## Last scrape failure

```

  browser closed
FATAL: no rows scraped - leaving /Users/danielcrabbe14/Sites/jynk/blok/index.html untouched
  ! Clapton: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-clapton-london", waiting until "load"

  ! Shoreditch: scrape failed: Page.goto: net::ERR_CONNECTION_RESET at https://classpass.com/studios/blok-shoreditch-london
Call log:
  - navigating to "https://classpass.com/studios/blok-shoreditch-london", waiting until "load"

  ! Mission E1: scrape failed: Page.goto: Navigation to "https://classpass.com/studios/mission-e1-london" is interrupted by another navigation to "chrome-error://chromewebdata/"
Call log:
  - navigating to "https://classpass.com/studios/mission-e1-london", waiting until "load"

  ! could not read upcoming reservations: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/profile/upcoming", waiting until "load"

----- 2026-09-09 02:55:29 refresh FAILED (exit 1)
```

