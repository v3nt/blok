# Schedule refresh — standalone, no Claude

Two launchd jobs, one file of truth.

```
scraper/refresh.py   scrapes ClassPass (3 studios) and writes ../index.html
scraper/refresh.sh   wrapper launchd calls
push-blok.sh         commits + pushes index.html, every 10 min
```

`refresh.py` is self-contained: scrape, categorise, and page template all in one
file. Nothing else generates `index.html` any more.

## One-time setup

```bash
cd ~/Sites/jynk/blok/scraper
pip3 install playwright
python3 -m playwright install chromium
python3 login_setup.py          # log in; saves auth_state.json
python3 refresh.py              # verify it works, prints a summary
```

Without `auth_state.json` everything still works except your own bookings —
they show as "Bookable" rather than "You're booked".

## Schedule it every 4 hours

```bash
cp net.jynk.blokscrape.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/net.jynk.blokscrape.plist
launchctl start net.jynk.blokscrape
tail -f scraper/refresh.log
```

Timeline: refresh writes `index.html` → within 10 min `push-blok.sh` commits and
pushes → GitHub Pages serves it. Nothing to click.

## What it prints

```
  Clapton -> 127 classes  [Tue, Aug 19:14 Wed, Aug 20:10 ...]
  wrote /Users/.../index.html (75593 bytes)
  551 classes  states={'bookable': 312, 'full': 51, 'soon': 187, 'booked': 1}
  ! Mission E1: uncategorised class 'Something New: All Levels'
```

Failure behaviour, deliberately:

- a studio that breaks is logged and skipped; the other two still publish
- zero rows scraped → `index.html` is left untouched rather than blanked
- a BLOK class that matches the filter but has no category is a hard error
- an unrecognised Mission E1 class lands in an "Other" category and warns —
  it is never silently dropped
- an unreadable booking status warns rather than guessing (`CLOSED` must not
  become "Bookable (LOSED credits)")

## Two writers, one branch

Something else has pushed to `origin/main` from its own clone (commit
`ba2283a`, "1612 classes"). That made every `push-blok.sh` push fail
non-fast-forward for hours. `push-blok.sh` now rebases onto origin first and
keeps this folder's `index.html` on conflict. If the other writer is a
scheduled Cowork task, turn it off — otherwise the two keep overwriting
each other every few hours.
