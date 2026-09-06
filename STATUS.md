# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-06 18:47:51 refresh OK (exit 0)` |
| index.html modified | 2026-09-06 18:56:00 BST |
| Classes in index.html | 2095 |

## Last scrape failure

```
  Mission E1: consent banner - overlay removed x1
  Mission E1 -> 346 classes  [Sun, Sep 6:0 Mon, Sep 7:30 Tue, Sep 8:31 Wed, Sep 9:28 Thu, Sep 10:26 Fri, Sep 11:26 Sat, Sep 12:20 Sun, Sep 13:20 Mon, Sep 14:30 Tue, Sep 15:31 Wed, Sep 16:28 Thu, Sep 17:28 Fri, Sep 18:28 Sat, Sep 19:20]
  upcoming: consent banner - overlay removed x1
  upcoming reservations: 4
  browser closed
  marked 0 row(s) as booked
  wrote /Users/danielcrabbe14/Sites/jynk/blok/index.html (85748 bytes)
  346 classes  states={'bookable': 153, 'full': 28, 'soon': 165}
  categories: {'4BEAT': 21, 'Ashtanga': 2, 'Ashtanga Guided Self Practice': 16, 'Backbends and Splits': 2, 'Balance Kulture': 7, 'Bambu Bodies': 14, 'Beyond Asana': 2, 'Boxing': 4, 'Core Conditioning': 2, 'Daoist Flow': 2, 'Dharma': 11, 'Dynamic Vinyasa': 11, 'Full Body Mobility': 2, 'Functional Yoga: Strength & Intelligence': 2, 'Handstands': 11, 'Hot 26&2': 13, 'Hot 4BEAT': 4, 'Hot Flow': 4, 'Hot Hips': 9, 'Hot Rocket': 4, 'Hot Yin': 2, 'Hot Yoga': 15, 'Iyengar Yoga': 6, 'Katonah Yoga': 2, 'Kettlebells': 3, 'Kundalini': 4, 'Mission 200 Graduates Class': 2, 'Mobility Kulture': 7, 'MyoYin': 4, 'Philosophy & Flow': 6, 'Pilates': 15, 'Pilates Strength': 1, 'Reps Kulture': 27, 'Rings': 6, 'Rocket': 16, 'Rolling': 4, 'Shoulders & Spine Mobility': 1, 'Skills & Reps Kulture': 7, 'Skills Kulture': 8, 'Squat Kulture': 15, 'Statics Kulture': 2, 'Strength Kulture': 4, 'Total Reps Kulture': 6, 'Vinyasa Flow': 13, 'Warm Dynamic Vinyasa': 4, 'Warm Hips': 1, 'Yin': 10, 'Yoga': 5, 'Yoga Inversions': 5, 'Yoga for Athletes': 2}
  ! Clapton: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-clapton-london", waiting until "load"

  ! Shoreditch: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-shoreditch-london", waiting until "load"

  ! Mission E1: no schedule rows rendered. title='Mission E1: Read Reviews and Book Classes on ClassPass' body='ClassPass is even better in the app |  | Book everything from barre to beauty & spa all with one easy-to-use app. |  | Get personalized recommendations |  | Browse a custom home feed that’s adapted to your routin' saved=debug-mission-e1.html
  ! 4 reservation(s) had no matching class in the schedule
----- 2026-09-06 18:47:51 refresh OK (exit 0)
```

## Recent push errors

```
2026-09-06 11:58:27  BLOCKED: baseline regression
2026-09-06 14:45:35  BLOCKED: baseline regression
2026-09-06 18:56:00  BLOCKED: baseline regression
```
