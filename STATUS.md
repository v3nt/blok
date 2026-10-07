# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-10-07 16:05:05 refresh start (python: /usr/bin/python3)` |
| index.html modified | 2026-10-07 06:07:13 BST |
| Classes in index.html | 1830 |

## Last scrape failure

```
  ! Islington 2026-10-11..2026-10-14: <urlopen error [Errno 8] nodename nor servname provided, or not known>
  ! Islington 2026-10-15..2026-10-18: <urlopen error [Errno 8] nodename nor servname provided, or not known>
  ! Islington 2026-10-19..2026-10-20: <urlopen error [Errno 8] nodename nor servname provided, or not known>
  ! Moorgate 2026-10-07..2026-10-10: <urlopen error [Errno 8] nodename nor servname provided, or not known>
  ! Moorgate 2026-10-11..2026-10-14: <urlopen error [Errno 8] nodename nor servname provided, or not known>
  ! Moorgate 2026-10-15..2026-10-18: <urlopen error [Errno 8] nodename nor servname provided, or not known>
  ! Moorgate 2026-10-19..2026-10-20: <urlopen error [Errno 8] nodename nor servname provided, or not known>
  ! City 2026-10-07..2026-10-10: <urlopen error [Errno 8] nodename nor servname provided, or not known>
  ! City 2026-10-11..2026-10-14: <urlopen error [Errno 8] nodename nor servname provided, or not known>
  ! City 2026-10-15..2026-10-18: <urlopen error [Errno 8] nodename nor servname provided, or not known>
  ! City 2026-10-19..2026-10-20: <urlopen error [Errno 8] nodename nor servname provided, or not known>
  ! thirdspace.py exited 1 (3rdspace.html left as it was)
----- 2026-10-07 14:13:38 refresh FAILED (exit 1)
----- 2026-10-07 16:05:05 refresh start (python: /usr/bin/python3)
BLOK refresh 2026-10-07 16:05:05
  browser: chrome, visible window
  loaded 53 saved cookie(s)
  ! Clapton failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-clapton-london", waiting until "load"
```

## Recent push errors

```
fatal: unable to access 'https://github.com/v3nt/blok.git/': Could not resolve host: github.com
fatal: unable to access 'https://github.com/v3nt/blok.git/': Could not resolve host: github.com
fatal: unable to access 'https://github.com/v3nt/blok.git/': Could not resolve host: github.com
```
