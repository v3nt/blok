# BLOK schedule

One page listing every upcoming class at **BLOK Clapton**, **BLOK Shoreditch**
and **Mission E1**, with real booking status, published to
<https://v3nt.github.io/blok/>.

Filters are grouped per gym, favourites sit above non-favourites in each group,
your own bookings are marked, and hovering a class shows its description.

## How it runs

Two launchd jobs, one file of truth (`index.html`), no Claude in the loop:

```
scraper/refresh.sh ──► scraper/refresh.py ──► writes index.html      every 4 hours
push-blok.sh ────────► validate ──► test ──► commit ──► push         every 10 min
```

`refresh.py` scrapes the three studios, reads your reservations from
`/profile/upcoming`, and writes `index.html`. `push-blok.sh` never publishes a
page that fails the gates below, and reverts to the last good commit instead.

| Job | Plist | Interval |
|---|---|---|
| scrape + rebuild | `net.jynk.blokscrape.plist` | 4 hours |
| validate + push | `net.jynk.blokpush.plist` | 10 minutes |

## Setup

Only needed once, on the Mac that runs the jobs:

```bash
/usr/bin/python3 -m pip install playwright
/usr/bin/python3 -m playwright install chromium

cd ~/Sites/jynk/blok/scraper
/usr/bin/python3 login_setup.py     # log in; saves auth_state.json
./refresh.sh                        # first real run

cp ../net.jynk.blokscrape.plist ~/Library/LaunchAgents/
cp ../net.jynk.blokpush.plist  ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/net.jynk.blok{scrape,push}.plist
```

There is more than one `python3` on a Mac and usually only one has playwright.
`refresh.sh` probes candidates and picks the first that can import it, so it
behaves the same from your shell as from launchd.

**Schedules do not need a login. Your bookings do.** They are separate steps:
if `auth_state.json` is missing or stale the schedule still publishes in full,
and only the booking marks are skipped, with a warning in the log.

## The gates

Nothing reaches GitHub without passing both:

| Gate | What it protects |
|---|---|
| `validate-index.py` | the JS parses, the data array exists, and the agreed UI is present — filter groups, favourites rows, the four select-alls, default favourites, descriptions, studio links |
| `scraper/test-baseline.py` | 47 checks driving the real page in a browser: favouriting, select-all scoping, collapse persistence, booking marks, tooltips, no past days, no JS errors |
| `scraper/test-resilience.py` | 5 checks with a stubbed page: an overlay cannot stop a scrape, no real mouse clicks, one bad day does not lose the run |

Run them by hand any time:

```bash
python3 validate-index.py index.html
python3 scraper/test-baseline.py index.html
python3 scraper/test-resilience.py
```

`refresh.py --base file:///path/to/fixture/` runs the whole pipeline against a
local fixture, so the scraper is testable without the live site.

## Files

| Path | Role |
|---|---|
| `index.html` | the published page — generated, never hand-edited |
| `scraper/refresh.py` | scrape → categorise → mark bookings → build the page |
| `scraper/refresh.sh` | launchd wrapper; picks a python that has playwright |
| `scraper/login_setup.py` | one-off: saves `auth_state.json` so bookings can be read |
| `scraper/class-descriptions.py` | one-off: rebuilds `class-descriptions.json` (hover text) |
| `scraper/class-descriptions.json` | class blurbs, keyed by class name |
| `scraper/CLASS-TYPES.md` | the same blurbs, readable |
| `push-blok.sh` | validate, test, commit, rebase, push |
| `validate-index.py` | static gate (see above) |
| `STATUS.md` | machine-written health summary, readable from GitHub on a phone |

## When something looks wrong

`STATUS.md` first — it carries the last scrape result and any push errors.
Then `scraper/refresh.log` (scrape detail) and `push-blok.log` (publish detail).

Known failure modes, all of which now report rather than fail silently:

- **zero classes scraped** — the page is left untouched rather than blanked;
  the log names the studio, the page title it got, and saves `debug-<studio>.html`
- **bookings missing** — `auth_state.json` expired; rerun `login_setup.py`
- **push rejected** — someone else pushed; `push-blok.sh` rebases, this folder wins
- **baseline regression** — a build dropped part of the UI; the publish is
  blocked and `index.html` reverts to the last good commit
