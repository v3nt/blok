# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-06 11:12:38 refresh OK (exit 0)` |
| index.html modified | 2026-09-06 11:58:27 BST |
| Classes in index.html | 2071 |

## Last scrape failure

```
Call log:
  - navigating to "https://classpass.com/studios/mission-e1-london", waiting until "load"

  browser closed
  wrote /Users/danielcrabbe14/Sites/jynk/blok/index.html (86363 bytes)
  380 classes  states={'closed': 3, 'full': 24, 'bookable': 352, 'booked': 1}
  categories: {'BARRE': 16, 'BLOKBREATH': 2, 'BLOKCORE': 4, 'BLOKFIT': 9, 'BLOKMOBILITY': 4, 'BLOKPOWER': 4, 'BLOKSCULPT': 8, 'BLOKSOUND': 1, 'BLOKSTRENGTH: FULL BODY': 11, 'BLOKSTRENGTH: LOWER BODY': 5, 'BLOKSTRENGTH: UPPER BODY': 3, 'BOXCON': 2, 'CALISTHENICS': 5, 'DYNAMIC VINYASA': 8, 'HANDSTANDS': 2, 'HOT + COLD': 59, 'HOT + COLD GUIDED: Energise': 1, 'HOT + COLD GUIDED: Recover': 1, 'HOT + COLD GUIDED: Unwind': 2, 'HOT + COLD QUIET': 7, 'MAT PILATES': 13, 'OPEN GYM': 118, 'POWER REFORMER L2': 7, 'POWER YOGA': 7, 'REFORMER PILATES L1': 11, 'REFORMER PILATES L2': 48, 'REFORMER PILATES L3': 14, 'SMALL GROUP PT: FULL BODY': 1, 'SMALL GROUP PT: LOWER BODY': 2, 'SMALL GROUP PT: UPPER BODY': 1, 'YIN YANG FLOW': 1, 'YIN YOGA': 2, 'YOGA WITH MEDITATION': 1}
  ! Shoreditch: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-shoreditch-london", waiting until "load"

  ! Mission E1: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/mission-e1-london", waiting until "load"

  ! could not read upcoming reservations: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/profile/upcoming", waiting until "load"

----- 2026-09-06 11:12:38 refresh OK (exit 0)
```

## Recent push errors

```
2026-09-06 10:13:37  BLOCKED: baseline regression
2026-09-06 11:58:27  BLOCKED: baseline regression
```
