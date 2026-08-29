"""
Scrapes the BLOK Clapton and BLOK Shoreditch class schedules from ClassPass
for the next NUM_DAYS days and writes them to data.txt in the same
pipe-delimited format your build.py already expects:

    CLAPTON
    Aug 17|7:30 PM|50|REFORMER PILATES L2|Bella Wilson|R
    ...
    SHOREDITCH
    Aug 18|7:40 PM|60|YIN YANG FLOW 60|Javi Martinez|5

Prereqs:
    pip install playwright
    playwright install chromium
    python login_setup.py      # once, to create auth_state.json

Usage:
    python scrape.py

IMPORTANT: I (Claude) could not inspect the live rendered DOM of the
ClassPass schedule widget directly, so this script parses the schedule
section's plain innerText with regex rather than relying on guessed CSS
selectors, which tend to be fragile/obfuscated on sites like this anyway.

If parsing comes up empty or wrong, run with DEBUG=True first — it dumps
the raw innerText for each day to debug_output/ so you can see exactly
what the page is giving us and adjust the regex in parse_day() below.
"""
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

STUDIOS = {
    "CLAPTON": "https://classpass.com/studios/blok-clapton-london",
    "SHOREDITCH": "https://classpass.com/studios/blok-shoreditch-london",
}

NUM_DAYS = 14
AUTH_STATE = "auth_state.json"
OUTPUT_FILE = "data.txt"
DEBUG = False
DEBUG_DIR = Path("debug_output")

# One block per class looks roughly like (as plain text, order may vary
# slightly with whitespace):
#   7:30 PM GMT+1
#   50 min
#   REFORMER PILATES L2
#   Bella Wilson
#   <price/availability text>
#
# This regex finds a time, then a duration, then treats the next two
# non-empty lines as name + instructor, and the following line(s) up to
# the next time as the availability/price text.
TIME_RE = re.compile(r"^\s*(\d{1,2}:\d{2}\s*[AP]M)\b")
DUR_RE = re.compile(r"(\d+)\s*min")
DAY_HEADING_RE = re.compile(
    r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s*([A-Za-z]{3})\s*(\d{1,2})\s*$"
)


def classify_availability(text):
    """Map whatever the booking button/price text says into the R/F/credits
    codes build.py expects. Adjust this mapping once you see real logged-in
    output (run with DEBUG=True and check debug_output/)."""
    t = text.strip().lower()
    if not t:
        return "R"
    if "full" in t or "waitlist" in t or "sold out" in t:
        return "F"
    if "book" in t or "reserve" in t or "see pricing" in t:
        return "R"
    m = re.search(r"(\d+)\s*credit", t)
    if m:
        return m.group(1)
    m = re.match(r"^(\d+)$", t)
    if m:
        return m.group(1)
    return "R"


def parse_day(raw_text, month, day):
    """Parse the innerText of the schedule area for a single day into
    (time, dur, name, instructor, avail) tuples."""
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    rows = []
    i = 0
    while i < len(lines):
        m = TIME_RE.match(lines[i])
        if not m:
            i += 1
            continue
        time_str = m.group(1)
        rest_of_line = lines[i][m.end():]
        i += 1

        dur_m = DUR_RE.search(rest_of_line)
        if not dur_m and i < len(lines):
            dur_m = DUR_RE.search(lines[i])
            if dur_m:
                i += 1
        dur = dur_m.group(1) if dur_m else ""

        name = lines[i] if i < len(lines) else ""
        i += 1
        name = re.sub(r"^\*+|\*+$", "", name).strip()

        instructor = lines[i] if i < len(lines) else ""
        i += 1

        avail_parts = []
        while i < len(lines) and not TIME_RE.match(lines[i]):
            avail_parts.append(lines[i])
            i += 1
        avail_text = " ".join(avail_parts)
        avail_code = classify_availability(avail_text)

        if name and time_str:
            rows.append((f"{month} {day}", time_str, dur, name, instructor, avail_code))
    return rows


def scrape_studio(page, location, url):
    print(f"--- {location} ---")
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(1500)

    all_rows = []
    for d in range(NUM_DAYS):
        schedule_locator = page.get_by_text("Schedule", exact=True).first
        try:
            container = schedule_locator.locator(
                "xpath=ancestor::section[1] | xpath=ancestor::div[contains(@class,'schedule')][1]"
            ).first
            raw_text = container.inner_text(timeout=5000)
        except Exception:
            raw_text = page.inner_text("body")

        heading_m = None
        for line in raw_text.splitlines():
            hm = DAY_HEADING_RE.match(line.strip())
            if hm:
                heading_m = hm
                break

        if DEBUG:
            DEBUG_DIR.mkdir(exist_ok=True)
            fname = DEBUG_DIR / f"{location}_day{d}.txt"
            fname.write_text(raw_text, encoding="utf-8")

        if heading_m:
            month, day = heading_m.group(2), heading_m.group(3)
        else:
            month, day = "???", "??"

        rows = parse_day(raw_text, month, day)
        print(f"  {month} {day}: {len(rows)} classes")
        all_rows.extend(rows)

        next_day_btn = page.get_by_text("See next day", exact=False)
        if next_day_btn.count() == 0:
            print("  No 'See next day' button found — stopping early.")
            break
        try:
            next_day_btn.first.click()
            page.wait_for_timeout(1200)
        except Exception as e:
            print(f"  Couldn't click next day: {e} — stopping early.")
            break

    return all_rows


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not DEBUG)
        state_path = AUTH_STATE if Path(AUTH_STATE).exists() else None
        if state_path is None:
            print(
                "WARNING: no auth_state.json found — run login_setup.py first "
                "if you need availability/credit info. Continuing logged out."
            )
        context = browser.new_context(storage_state=state_path)
        page = context.new_page()

        with open(OUTPUT_FILE, "w") as f:
            for location, url in STUDIOS.items():
                rows = scrape_studio(page, location, url)
                f.write(location + "\n")
                for r in rows:
                    f.write("|".join(r) + "\n")

        browser.close()
    print(f"\nDone. Wrote data to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
