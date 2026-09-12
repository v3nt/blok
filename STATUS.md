# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-12 08:42:11 refresh OK (exit 0)` |
| index.html modified | 2026-09-12 08:44:54 BST |
| Classes in index.html | 2020 |

## Last scrape failure

```
  Mission E1: consent banner - overlay removed x1
  Mission E1: Fri, Sep 25 empty -> end of published schedule
  Mission E1 -> 339 classes  [Sat, Sep 12:19 Sun, Sep 13:19 Mon, Sep 14:30 Tue, Sep 15:30 Wed, Sep 16:28 Thu, Sep 17:28 Fri, Sep 18:27 Sat, Sep 19:20 Sun, Sep 20:20 Mon, Sep 21:30 Tue, Sep 22:32 Wed, Sep 23:28 Thu, Sep 24:28]
  upcoming: consent banner - overlay removed x1
  upcoming reservations: 6
  browser closed
  marked 0 row(s) as booked
  wrote /Users/danielcrabbe14/Sites/jynk/blok/index.html (84981 bytes)
  339 classes  states={'full': 32, 'bookable': 169, 'soon': 138}
  categories: {'4BEAT': 18, 'Ashtanga': 1, 'Ashtanga Guided Self Practice': 18, 'Backbends and Splits': 1, 'Balance Kulture': 8, 'Bambu Bodies': 12, 'Beyond Asana': 2, 'Boxing': 5, 'Core Conditioning': 2, 'Daoist Flow': 3, 'Dharma': 12, 'Dynamic Vinyasa': 13, 'Full Body Mobility': 2, 'Functional Yoga: Strength & Intelligence': 2, 'Handstands': 10, 'Hot 26&2': 13, 'Hot 4BEAT': 2, 'Hot Flow': 6, 'Hot Hips': 8, 'Hot Rocket': 4, 'Hot Yin': 2, 'Hot Yoga': 17, 'Iyengar Yoga': 5, 'Katonah Yoga': 2, 'Kettlebells': 1, 'Kundalini': 4, 'Mission 200 Graduates Class': 2, 'Mobility Kulture': 7, 'MyoYin': 4, 'Philosophy & Flow': 6, 'Pilates': 15, 'Pilates Strength': 2, 'Reps Kulture': 25, 'Rings': 5, 'Rocket': 16, 'Rolling': 4, 'Shoulders & Spine Mobility': 1, 'Skills & Reps Kulture': 7, 'Skills Kulture': 8, 'Squat Kulture': 15, 'Statics Kulture': 2, 'Strength Kulture': 4, 'Total Reps Kulture': 6, 'Vinyasa Flow': 15, 'Warm Dynamic Vinyasa': 4, 'Yin': 9, 'Yoga': 3, 'Yoga Inversions': 5, 'Yoga for Athletes': 1}
  ! Clapton: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-clapton-london", waiting until "load"

  ! Shoreditch: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-shoreditch-london", waiting until "load"

  ! 6 reservation(s) had no matching class in the schedule
----- 2026-09-12 08:42:11 refresh OK (exit 0)
```

## Recent push errors

```
2026-09-11 19:58:18  BLOCKED: baseline regression
2026-09-12 04:53:38  BLOCKED: baseline regression
2026-09-12 08:44:54  BLOCKED: baseline regression
```
