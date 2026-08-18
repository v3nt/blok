# BLOK schedule scraper (Playwright)

Scrapes BLOK Clapton + Shoreditch schedules from ClassPass into `data.txt`,
matching the format `build.py` in your v3nt/blok repo already expects.

## Setup

```bash
pip install playwright
playwright install chromium
```

## 1. Log in once

```bash
python login_setup.py
```

A real browser window opens. Log into ClassPass yourself (handles any
2FA/captcha), then press Enter in the terminal. This saves `auth_state.json`
so the scraper doesn't need to log in every run and can see your actual
booking availability (credits, full/waitlist, etc.) rather than the generic
"See pricing" prompt logged-out users see.

## 2. Run the scraper

```bash
python scrape.py
```

Writes `data.txt` — feed straight into your existing `build.py` (just point
`BASE` at wherever this file lives, or copy it over).

## If it doesn't parse anything (likely, first run)

I wrote `scrape.py` by parsing the schedule area's plain text with regex,
since I couldn't inspect ClassPass's live rendered DOM/selectors directly —
sites like this often use obfuscated/hashed class names anyway, so text
parsing is usually more durable than guessing CSS selectors.

Set `DEBUG = True` at the top of `scrape.py` and re-run. This will:
- run the browser headed so you can watch what's happening
- dump each day's raw scraped text to `debug_output/CLAPTON_day0.txt` etc.

Paste me the contents of one of those debug files and I'll fix up
`parse_day()` / `classify_availability()` to match exactly what the page is
actually giving us — the current regex is my best guess based on the
snippet ClassPass served to a plain fetch, not a verified live extraction.

## Notes

- `NUM_DAYS` defaults to 14 to match your existing 2-week window.
- Availability codes map to your existing format: `R` (reservable/available),
  `F` (full/waitlist), or a bare number (credits) — see
  `classify_availability()` to tune this once you see real output.
- Respect ClassPass's terms of service — this is for your own personal
  schedule viewing, run at a reasonable frequency (your build.py comment
  mentions a 3-hour refresh interval, which is plenty).
