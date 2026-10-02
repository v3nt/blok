# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-10-02 06:52:51 refresh FAILED (exit 1)` |
| index.html modified | 2026-10-02 06:59:32 BST |
| Classes in index.html | 1376 |

## Last scrape failure

```
  - <launched> pid=42835
  - [pid=42835][err] Trying to load the allocator multiple times. This is *not* supported.
) - fell back to Chromium
  ! Clapton: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-clapton-london", waiting until "load"

  ! Shoreditch: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-shoreditch-london", waiting until "load"

  ! 8 reservation(s) had no matching class in the schedule
Third Space refresh 2026-10-02 06:52:46
  Islington -> 730 class(es)
  Moorgate -> 477 class(es)
  City -> 436 class(es)
  descriptions: 44 of 48 class type(s)
  no blurb for: Dance Fit, Reformer x Lift, Self, Yoga Workshop
  wrote /Users/danielcrabbe14/Sites/jynk/blok/3rdspace.html (222576 bytes, 1643 classes)
----- 2026-10-02 06:52:51 refresh FAILED (exit 1)
```

## Recent push errors

```
2026-10-02 07:20:26  BLOCKED: baseline regression
2026-10-02 07:30:55  BLOCKED: baseline regression
2026-10-02 07:41:21  BLOCKED: baseline regression
```
