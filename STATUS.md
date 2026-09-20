# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-20 18:10:03 refresh OK (exit 0)` |
| index.html modified | 2026-09-20 18:52:37 BST |
| Classes in index.html | 2065 |

## Last scrape failure

```
  browser closed
  trial venues: 634 class(es) -> extra-venues.json
  marked 4 row(s) as booked
  wrote /Users/danielcrabbe14/Sites/jynk/blok/index.html (301032 bytes)
  2065 classes  states={'closed': 3, 'bookable': 1450, 'full': 77, 'booked': 4, 'soon': 531}
  categories: {'4BEAT': 22, 'Ashtanga': 2, 'Ashtanga Guided Self Practice': 18, 'BARRE': 103, 'BLOKBREATH': 6, 'BLOKCORE': 14, 'BLOKFIT': 36, 'BLOKMOBILITY': 15, 'BLOKPOWER': 23, 'BLOKSCULPT': 55, 'BLOKSOUND': 5, 'BLOKSTRENGTH: FULL BODY': 48, 'BLOKSTRENGTH: LOWER BODY': 32, 'BLOKSTRENGTH: UPPER BODY': 22, 'BOXCON': 15, 'Backbends and Splits': 2, 'Balance Kulture': 7, 'Bambu Bodies': 14, 'Beyond Asana': 2, 'Boxing': 5, 'CALISTHENICS': 36, 'Core Conditioning': 1, 'DYNAMIC VINYASA': 61, 'Daoist Flow': 1, 'Dharma': 11, 'Dynamic Vinyasa': 11, 'FLOOR BARRE': 4, 'Full Body Mobility': 2, 'Functional Yoga: Strength & Intelligence': 2, 'HANDSTANDS': 13, 'HOT + COLD': 223, 'HOT + COLD GUIDED: Energise': 2, 'HOT + COLD GUIDED: Recover': 6, 'HOT + COLD GUIDED: Unwind': 5, 'HOT + COLD QUIET': 24, 'Handstands': 10, 'Hot 26&2': 12, 'Hot 4BEAT': 4, 'Hot Flow': 4, 'Hot Hips': 9, 'Hot Rocket': 4, 'Hot Yin': 2, 'Hot Yoga': 16, 'Iyengar Yoga': 5, 'Kettlebells': 3, 'Kundalini': 3, 'MAT PILATES': 84, 'Mission 200 Graduates Class': 2, 'Mobility Kulture': 7, 'MyoYin': 4, 'OPEN GYM': 382, 'POWER REFORMER L2': 42, 'POWER YOGA': 47, 'Philosophy & Flow': 6, 'Pilates': 15, 'Pilates Strength': 2, 'REFORMER PILATES L1': 54, 'REFORMER PILATES L2': 235, 'REFORMER PILATES L3': 84, 'ROCKET YOGA': 2, 'Reps Kulture': 27, 'Rings': 4, 'Rocket': 15, 'Rolling': 3, 'SMALL GROUP PT: FULL BODY': 5, 'SMALL GROUP PT: LOWER BODY': 8, 'SMALL GROUP PT: UPPER BODY': 4, 'Shoulders & Spine Mobility': 1, 'Skills & Reps Kulture': 7, 'Skills Kulture': 8, 'Squat Kulture': 15, 'Statics Kulture': 2, 'Strength Kulture': 4, 'Total Reps Kulture': 6, 'Vinyasa Flow': 16, 'Warm Dynamic Vinyasa': 4, 'YIN YANG FLOW': 4, 'YIN YOGA': 16, 'YOGA WITH MEDITATION': 8, 'Yin': 10, 'Yoga': 4, 'Yoga Inversions': 6, 'Yoga for Athletes': 2}
  ! Shoreditch: no schedule rows rendered. title='BLOK - Shoreditch: Read Reviews and Book Classes on ClassPass' body='Refer 3 friends and get £300 | ClassPass | Gifts | Videos | Upcoming | 4 | Get £300 | 3 credits | Info | Schedule | BLOK - Shoreditch | 4.8 | (30,000+) | This studio offers Yoga, Power Yoga, Strength Training, and HIIT classes' saved=debug-shoreditch.html
  ! RUMBLE Dalston: no schedule rows rendered. title='RUMBLE - Dalston: Read Reviews and Book Classes on ClassPass' body='Refer 3 friends and get £300 | ClassPass | Gifts | Videos | Upcoming | 4 | Get £300 | 3 credits | Info | Schedule | RUMBLE - Dalston | 4.8 | (30,000+) | This studio offers Cycling, Strength Training, and Bootcamp classes. |  | We ' saved=debug-rumble-dalston.html
  ! Psycle Shoreditch: no schedule rows rendered. title='Psycle - Shoreditch: Read Reviews and Book Classes on ClassPass' body='Refer 3 friends and get £300 | ClassPass | Gifts | Videos | Upcoming | 4 | Get £300 | 3 credits | Info | Schedule | Psycle - Shoreditch | 4.8 | (30,000+) | This studio offers Yoga, Cycling, Barre, and Strength Training classes' saved=debug-psycle-shoreditch.html
Third Space refresh 2026-09-20 18:10:01
Traceback (most recent call last):
  File "/Users/danielcrabbe14/Sites/jynk/blok/scraper/thirdspace.py", line 212, in <module>
    sys.exit(main())
  File "/Users/danielcrabbe14/Sites/jynk/blok/scraper/thirdspace.py", line 179, in main
    rows += to_rows(code, club, fetch_club(code, club, club_id, start,
  File "/Users/danielcrabbe14/Sites/jynk/blok/scraper/thirdspace.py", line 99, in fetch_club
    for name, classes in clubs.items():
AttributeError: 'list' object has no attribute 'items'
  ! thirdspace.py exited 1 (3rdspace.html left as it was)
----- 2026-09-20 18:10:03 refresh OK (exit 0)
```

