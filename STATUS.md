# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-08-28 15:59:07 refresh FAILED (exit 1)` |
| index.html modified | 2026-08-27 23:20:32 BST |
| Classes in index.html | 840 |

## Last scrape failure

```
    - waiting 500ms
    - waiting for element to be visible, enabled and stable
    - element is visible, enabled and stable
    - scrolling into view if needed
    - done scrolling
    - <div id="truste-consent-text" class="truste-messageColumn">…</div> from <div lang="en" id="consent_blackbar">…</div> subtree intercepts pointer events
  - retrying click action
    - waiting 500ms
    - waiting for element to be visible, enabled and stable
    - element is visible, enabled and stable
    - scrolling into view if needed
    - done scrolling
    - <div id="trustarc-banner-overlay"></div> from <div lang="en" id="consent_blackbar">…</div> subtree intercepts pointer events
  - retrying click action
    - waiting 500ms

  Shoreditch -> 0 classes  []
  Mission E1 -> 0 classes  []
FATAL: no rows scraped - leaving /Users/danielcrabbe14/Sites/jynk/blok/index.html untouched
----- 2026-08-28 15:59:07 refresh FAILED (exit 1)
```

## Recent push errors

```
2026-08-28 18:08:56  BLOCKED: baseline regression
2026-08-28 18:19:00  BLOCKED: baseline regression
2026-08-28 18:29:03  BLOCKED: baseline regression
```
