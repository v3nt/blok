# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-17 00:29:26 refresh FAILED (exit 1)` |
| index.html modified | 2026-09-16 22:10:53 BST |
| Classes in index.html | 2009 |

## Last scrape failure

```
Call log:
  - navigating to "https://classpass.com/studios/blok-shoreditch-london", waiting until "load"

  ! Mission E1: scrape failed: Page.goto: net::ERR_TIMED_OUT at https://classpass.com/studios/mission-e1-london
Call log:
  - navigating to "https://classpass.com/studios/mission-e1-london", waiting until "load"

  ! RUMBLE Dalston (trial venue): Page.goto: Navigation to "https://classpass.com/studios/rumble-dalston-london" is interrupted by another navigation to "chrome-error://chromewebdata/"
Call log:
  - navigating to "https://classpass.com/studios/rumble-dalston-london", waiting until "load"

  ! Psycle Shoreditch (trial venue): Page.goto: Navigation to "https://classpass.com/studios/psycle-shoreditch-london" is interrupted by another navigation to "https://classpass.com/studios/rumble-dalston-london"
Call log:
  - navigating to "https://classpass.com/studios/psycle-shoreditch-london", waiting until "load"

  ! could not read upcoming reservations: Page.goto: Navigation to "https://classpass.com/profile/upcoming" is interrupted by another navigation to "https://classpass.com/studios/psycle-shoreditch-london"
Call log:
  - navigating to "https://classpass.com/profile/upcoming", waiting until "load"

----- 2026-09-17 00:29:26 refresh FAILED (exit 1)
```

