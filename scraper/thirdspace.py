#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thirdspace.py - build 3rdspace.html from the Third Space public timetable.

No browser and no login, unlike the ClassPass scraper: the timetable page
ships its own data as a JSON blob in a <script> tag, so this is plain HTTP.

    https://www.thirdspace.london/timetable/?fromDate=&toDate=&location_id=

returns a page containing `let timetable = {"<date>": {"<club>": [classes]}}`,
four days at a time. Class descriptions come from /classes/, which lists every
class with its category and a one-line blurb - the same thing the tooltips on
the BLOK page use.

    python3 thirdspace.py            # write ../3rdspace.html
    python3 thirdspace.py --days 7
    python3 thirdspace.py --dump     # save the raw JSON next to it, for tests

Exit codes: 0 ok, 1 nothing scraped (the page is left untouched).
"""
import argparse, datetime, html, json, pathlib, re, sys, urllib.request, urllib.error

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
OUT = REPO / "3rdspace.html"
CACHE = HERE / "thirdspace-classes.json"

BASE = "https://www.thirdspace.london"
TIMETABLE = BASE + "/timetable/"
CLASSES = BASE + "/classes/"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36")

# Third Space's own club ids, read out of the timetable page's `clubs` array.
# Venue codes are single letters because they key the filter element ids.
CLUBS = [
    ("I", "Islington", 123),
    ("G", "Moorgate",  177),
    ("C", "City",       43),
]
CHUNK = 4          # days per request - the site's own step
DAYS = 14

# Category colours, from the site's activityCategories.
CAT_COLOUR = {
    "Cycle": "#7a8182", "Cycling": "#7a8182",
    "Mind & Body": "#6d9fcd", "Yoga": "#6d9fcd",
    "Pilates": "#669bcc", "Pilates & Reformer": "#669bcc",
    "Strength & Conditioning": "#3f7a27",
    "Combat": "#6cbecc", "HYROX": "#b0521f",
    "Sports & Performance": "#b0521f", "Running": "#b0521f",
    "Recovery": "#75b396", "Barre": "#a28ed2", "Dance": "#6fce6f",
}
GREY = "#8a8a8f"

def log(msg):
    print(msg, flush=True)

def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Language": "en-GB,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def blob(page, name):
    """Pull `let <name> = <json>;` out of the page."""
    m = re.search(r"let\s+%s\s*=\s*([\[{].*?[\]}])\s*;\s*\n" % re.escape(name), page, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None

def day_chunks(start, days, size=CHUNK):
    d = 0
    while d < days:
        a = start + datetime.timedelta(days=d)
        b = start + datetime.timedelta(days=min(d + size - 1, days - 1))
        yield a, b
        d += size

def fetch_club(code, club, club_id, start, days, warnings):
    """Every class for one club, as {(iso, start, title, trainer, mins)}."""
    seen, got = {}, 0
    for a, b in day_chunks(start, days):
        url = "%s?fromDate=%s&toDate=%s&location_id=%d" % (TIMETABLE, a, b, club_id)
        try:
            page = get(url)
        except Exception as e:
            warnings.append("%s %s..%s: %s" % (club, a, b, e))
            continue
        data = blob(page, "timetable")
        if data is None:
            warnings.append("%s %s..%s: no timetable data in the page" % (club, a, b))
            continue
        for iso, payload in data.items():
            # A day with no classes comes back as [] rather than {}, which is
            # what crashed the first run. Anything that is not a club->classes
            # map is simply a day with nothing on.
            if isinstance(payload, dict):
                groups = list(payload.items())
            elif isinstance(payload, list) and payload:
                groups = [(club, payload)]
            else:
                continue
            for name, classes in groups:
                if name.strip().lower() != club.lower():
                    continue          # the page can carry a default club too
                for c in classes:
                    if (c.get("location_name") or club).strip().lower() != club.lower():
                        continue      # belt and braces: trust the row's own club
                    key = (iso, c.get("start_time"), c.get("service_title"))
                    if key in seen:
                        continue
                    seen[key] = c
                    got += 1
    log("  %s -> %d class(es)" % (club, got))
    return seen

def descriptions(warnings):
    """{class name: blurb} and {class name: category} from /classes/."""
    desc, cat = {}, {}
    for page_no in range(1, 6):
        url = CLASSES if page_no == 1 else "%spage/%d/" % (CLASSES, page_no)
        try:
            page = get(url)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                break                        # ran off the end of the listing
            warnings.append("classes page %d: %s" % (page_no, e)); break
        except Exception as e:
            warnings.append("classes page %d: %s" % (page_no, e)); break
        cards = re.findall(
            r'class="tag-primary[^"]*">([^<]+)</div>.*?'
            r'class="font-medium heading-four[^"]*">([^<]+)</div>.*?'
            r'class="post__excerpt[^"]*">\s*(.*?)\s*</div>', page, re.S)
        if not cards:
            break
        for c, name, blurb in cards:
            name = html.unescape(name).strip()
            blurb = html.unescape(re.sub(r"<[^>]+>", "", blurb)).strip()
            if name and blurb and len(blurb) > len(desc.get(name, "")):
                desc[name] = blurb
                cat[name] = html.unescape(c).strip().title()
    log("  descriptions: %d class(es)" % len(desc))
    if not desc:
        warnings.append("no class descriptions found - tooltips will be empty")
    return desc, cat

def category(title):
    """Collapse 'Just Ride 30' / 'Just Ride: 90s Club Classics' to 'Just Ride'."""
    c = re.sub(r"\s*[:–-]\s*.*$", "", title.strip())
    c = re.sub(r"\s+\d{2,3}$", "", c).strip()
    return c or title.strip()

def to_rows(code, club, classes):
    rows = []
    for (iso, start, title), c in classes.items():
        if not (iso and start and title):
            continue
        try:
            date = datetime.date.fromisoformat(iso)
            hh, mm = (int(x) for x in start.split(":")[:2])
        except Exception:
            continue
        mins = hh * 60 + mm
        dur = int(c.get("duration_hours") or 0) * 60 + int(c.get("duration_minutes") or 0)
        disp = "%d:%02d%s" % ((hh % 12) or 12, mm, "PM" if hh >= 12 else "AM")
        rows.append([iso, mins, disp, dur, category(title),
                     (c.get("trainer_name") or "").strip() or "-", club,
                     "open", "In the timetable", date.weekday(), code])
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--days", type=int, default=DAYS)
    ap.add_argument("--from-json", metavar="FILE",
                    help="build from rows captured earlier instead of fetching "
                         "(the same JSON --dump writes)")
    ap.add_argument("--dump", action="store_true",
                    help="also write the scraped rows next to the page")
    args = ap.parse_args()

    sys.path.insert(0, str(HERE))
    import refresh                                   # template + page builder

    log("Third Space refresh %s" % datetime.datetime.now().strftime("%F %T"))
    start, warnings, rows = datetime.date.today(), [], []
    if args.from_json:
        raw = json.loads(pathlib.Path(args.from_json).read_text(encoding="utf-8"))
        rows = raw["rows"] if isinstance(raw, dict) else raw
        log("  loaded %d class(es) from %s" % (len(rows), args.from_json))
    else:
        for code, club, club_id in CLUBS:
            rows += to_rows(code, club, fetch_club(code, club, club_id, start,
                                                   args.days, warnings))
    if not rows:
        log("FATAL: no classes scraped - leaving %s untouched" % args.out)
        for w in warnings: log("  ! " + w)
        return 1

    desc_by_name, cat_by_name = descriptions(warnings)
    cats = {r[4] for r in rows}
    desc = {c: desc_by_name[c] for c in cats if c in desc_by_name}
    palette = {c: CAT_COLOUR.get(cat_by_name.get(c, ""), GREY) for c in cats}

    venues = [(code, club, "tsTypes" + code) for code, club, _ in CLUBS]
    ls_keys = {"a": "tsAvailOnly", "f": "tsHideFull", "w": "tsHideWorkHours",
               "v": "tsFavs", "vv": "tsFavsSeed", "c": "tsCollapse",
               "bk": "tsBookedCol"}
    html_out, states, counts = refresh.build(
        rows, refresh.TEMPLATE, venues=venues, ls_keys=ls_keys, palette=palette,
        desc=desc, studio_url={club: BASE + "/timetable/" for _, club, _ in CLUBS},
        title="Class schedule — Third Space",
        sub_html=('<p class="sub">Third Space · '
                  + " &amp; ".join(club for _, club, _ in CLUBS)
                  + ' · %d classes · auto-updated every 2 hours · '
                    'refreshed %s</p>'))
    pathlib.Path(args.out).write_text(html_out, encoding="utf-8")
    log("  wrote %s (%d bytes, %d classes)" % (args.out, len(html_out.encode()), len(rows)))
    if args.dump:
        CACHE.write_text(json.dumps({"scraped": datetime.datetime.now().isoformat(
            timespec="seconds"), "rows": rows}, indent=1), encoding="utf-8")
    for w in warnings: log("  ! " + w)
    return 0

if __name__ == "__main__":
    sys.exit(main())
