# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-10-07 18:05:05 refresh start (python: /usr/bin/python3)` |
| index.html modified | 2026-10-07 06:07:13 BST |
| Classes in index.html | 1830 |

## Last scrape failure

```
  - navigating to "https://classpass.com/studios/blok-clapton-london", waiting until "load"

  ! Shoreditch failed: Page.goto: net::ERR_INTERNET_DISCONNECTED at https://classpass.com/studios/blok-shoreditch-london
Call log:
  - navigating to "https://classpass.com/studios/blok-shoreditch-london", waiting until "load"

  browser closed
  marked 0 row(s) as booked
FATAL: no rows scraped - leaving /Users/danielcrabbe14/Sites/jynk/blok/index.html untouched
  ! Clapton: scrape failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-clapton-london", waiting until "load"

  ! Shoreditch: scrape failed: Page.goto: net::ERR_INTERNET_DISCONNECTED at https://classpass.com/studios/blok-shoreditch-london
Call log:
  - navigating to "https://classpass.com/studios/blok-shoreditch-london", waiting until "load"

  ! BLOK mailbox unreachable ([Errno 8] nodename nor servname provided, or not known) - using bookings from 2026-10-07T06:07:13+01:00
  ! 11 reservation(s) had no matching class in the schedule
Third Space refresh 2026-10-07 18:06:37
```

## Recent push errors

```
fatal: unable to access 'https://github.com/v3nt/blok.git/': Could not resolve host: github.com
fatal: unable to access 'https://github.com/v3nt/blok.git/': Could not resolve host: github.com
fatal: unable to access 'https://github.com/v3nt/blok.git/': Could not resolve host: github.com
```
