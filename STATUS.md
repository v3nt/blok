# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-20 20:05:05 refresh start (python: /usr/bin/python3)` |
| index.html modified | 2026-09-20 19:05:19 BST |
| Classes in index.html | 2065 |

## Last scrape failure

```
    sys.exit(main())
  File "/Users/danielcrabbe14/Sites/jynk/blok/scraper/thirdspace.py", line 179, in main
    rows += to_rows(code, club, fetch_club(code, club, club_id, start,
  File "/Users/danielcrabbe14/Sites/jynk/blok/scraper/thirdspace.py", line 99, in fetch_club
    for name, classes in clubs.items():
AttributeError: 'list' object has no attribute 'items'
  ! thirdspace.py exited 1 (3rdspace.html left as it was)
----- 2026-09-20 18:10:03 refresh OK (exit 0)
----- 2026-09-20 20:05:05 refresh start (python: /usr/bin/python3)
BLOK refresh 2026-09-20 20:05:05
  browser: chrome, visible window
  loaded 53 saved cookie(s)
  Clapton: consent banner - overlay removed x1
  Clapton -> 1297 classes  [Sun, Sep 20:0 Mon, Sep 21:108 Tue, Sep 22:105 Wed, Sep 23:108 Thu, Sep 24:104 Fri, Sep 25:102 Sat, Sep 26:79 Sun, Sep 27:85 Mon, Sep 28:108 Tue, Sep 29:105 Wed, Sep 30:108 Thu, Oct 1:104 Fri, Oct 2:102 Sat, Oct 3:79]
  Shoreditch: consent banner - overlay removed x1
  Shoreditch -> 423 classes  [Sun, Sep 20:0 Mon, Sep 21:36 Tue, Sep 22:36 Wed, Sep 23:36 Thu, Sep 24:35 Fri, Sep 25:30 Sat, Sep 26:26 Sun, Sep 27:25 Mon, Sep 28:36 Tue, Sep 29:36 Wed, Sep 30:36 Thu, Oct 1:35 Fri, Oct 2:30 Sat, Oct 3:26]
  Mission E1: consent banner - overlay removed x1
  Mission E1 -> 341 classes  [Sun, Sep 20:0 Mon, Sep 21:30 Tue, Sep 22:32 Wed, Sep 23:28 Thu, Sep 24:28 Fri, Sep 25:28 Sat, Sep 26:20 Sun, Sep 27:20 Mon, Sep 28:30 Tue, Sep 29:32 Wed, Sep 30:27 Thu, Oct 1:23 Fri, Oct 2:23 Sat, Oct 3:20]
  RUMBLE Dalston: consent banner - overlay removed x1
  RUMBLE Dalston -> 483 classes  [Sun, Sep 20:0 Mon, Sep 21:45 Tue, Sep 22:43 Wed, Sep 23:43 Thu, Sep 24:40 Fri, Sep 25:38 Sat, Sep 26:23 Sun, Sep 27:19 Mon, Sep 28:45 Tue, Sep 29:43 Wed, Sep 30:43 Thu, Oct 1:40 Fri, Oct 2:38 Sat, Oct 3:23]
```

