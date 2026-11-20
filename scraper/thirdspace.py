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
    ("W", "Canary Wharf", 39),
    ("B", "Tower Bridge", 63),
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

def norm(name):
    """Compare class names loosely: 'Lift - Weightlifting Classes' is 'Lift'."""
    n = html.unescape(name).lower()
    n = re.split(r"[\u2013\u2014|:]", n)[0]
    n = re.sub(r"[^a-z0-9 ]", " ", n)
    return re.sub(r"\s+", " ", n).strip()

# The timetable and the classes listing do not use the same words. These are
# the ones no amount of tidying will connect.
ALIAS = {"brazilian jiu jitsu": "bjj fundamentals",
         "triathlon swim": "triathlon swim training",
         "swim": "skills drills"}
# Prefixes the timetable adds to a class that the listing does not carry.
MODIFIERS = ("hot ", "candlelit ", "warm ", "power ")

def match(cat, listing):
    """Find the blurb for a timetable category in the /classes/ listing."""
    k = match_key(cat, listing)
    return listing[k] if k else None

def match_key(cat, listing):
    """The /classes/ listing key for a timetable category, or None."""
    key = norm(cat)
    for candidate in (key, ALIAS.get(key, "")):
        if candidate and candidate in listing:
            return candidate
    stripped = key
    for m in MODIFIERS:                       # Hot Vinyasa Yoga -> Vinyasa Yoga
        if stripped.startswith(m):
            stripped = stripped[len(m):].strip()
    if stripped != key and stripped in listing:
        return stripped
    # Boxing Padwork -> Boxing; HYROX -> HYROX Train. Longest wins, so
    # "Muay Thai Padwork" prefers "Muay Thai" over nothing.
    best = None
    for name in listing:
        if stripped.startswith(name + " ") or name.startswith(stripped + " "):
            if best is None or len(name) > len(best):
                best = name
    return best

PAGES = HERE / "thirdspace-class-pages.json"     # slug + long description per class type
FOCUS_FILE = HERE / "thirdspace-focus.json"      # hand-kept body-focus tag per class type
NO_DESC = "No description on Third Space's site."
FOCUS_TAGS = ("Legs", "Upper", "Full body", "Core", "Cardio", "Mobility-Recovery")

def page_nodes(page):
    page = re.sub(r"<(script|style|svg|noscript)[^>]*>.*?</\1>", "", page, flags=re.S)
    page = re.sub(r"<!--.*?-->", "", page, flags=re.S)
    return [re.sub(r"\s+", " ", html.unescape(p)).strip()
            for p in re.split(r"<[^>]+>", page) if p.strip()]

def page_text(page):
    """The longer description on a /class/<slug>/ page: intro, then the feature blurbs.

    Pages differ: some are just a title and one paragraph, others add a
    "Book Now" button, three titled feature blocks and a trainer quote. The
    content is whatever sits between the site menu (ends at "Journal") and
    the "<name> upcoming classes" heading.
    """
    n = page_nodes(page)
    end = next((i for i, x in enumerate(n) if x.endswith("upcoming classes")), None)
    if end is None:
        return ""
    start = max((i for i in range(end) if n[i] == "Journal"), default=-1) + 1
    body = [x for x in n[start:end] if x != "Book Now"][1:]      # [0] is the page title
    out, i = [], 0
    while i < len(body):
        x = body[i]
        if x[:1] in "“\"":               # trainer quote, then its byline
            i += 2
            continue
        out.append(x)
        i += 1
    # intro first, then feature blocks as "Heading. text" pairs; cap at a sentence
    text = out[0] if out else ""
    for j in range(1, len(out) - 1, 2):
        text += "\n" + out[j].rstrip(".:") + ": " + out[j + 1]
    if len(text) > 650:
        cut = max(text.rfind("\n", 0, 650), text.rfind(". ", 0, 650) + 1)
        text = text[:cut].rstrip() if cut > 200 else text[:650].rstrip() + "…"
    return text

def descriptions(categories, warnings):
    """({category: text}, {category: site category}, {category: long text for tagging}).

    Text comes from the /classes/ listing (one-line blurb) and from each
    class's own /class/<slug>/ page (longer). Both are cached: a page that
    cannot be fetched should cost us a refresh of the text, not a tooltip.
    A type the site has no page for gets NO_DESC so hovering always works.
    """
    listing, slugs = {}, {}
    for page_no in range(1, 11):
        url = CLASSES if page_no == 1 else "%spage/%d/" % (CLASSES, page_no)
        try:
            page = get(url)
        except urllib.error.HTTPError as e:
            if e.code != 404:
                warnings.append("classes page %d: %s" % (page_no, e))
            break
        except Exception as e:
            warnings.append("classes page %d: %s" % (page_no, e))
            break
        cards = re.findall(
            r'class="tag-primary[^"]*">([^<]+)</div>.*?'
            r'class="font-medium heading-four[^"]*">([^<]+)</div>.*?'
            r'class="post__excerpt[^"]*">\s*(.*?)\s*</div>', page, re.S)
        if not cards:
            break
        for c, name, blurb in cards:
            blurb = html.unescape(re.sub(r"<[^>]+>", "", blurb))
            blurb = re.sub(r"\s+", " ", blurb).strip()
            key = norm(name)
            if key and blurb and len(blurb) > len(listing.get(key, ("", ""))[1]):
                listing[key] = (html.unescape(c).strip(), blurb)
        for blk in re.split(r'(?=href="https://www\.thirdspace\.london/class/)', page)[1:]:
            h = re.match(r'href="https://www\.thirdspace\.london/class/([^/"]+)/"', blk)
            nm = re.search(r'class="font-medium heading-four[^"]*">([^<]+)</div>', blk)
            if h and nm:
                slugs[norm(nm.group(1))] = h.group(1)

    if listing:
        try:
            CACHE.write_text(json.dumps({k: list(v) for k, v in listing.items()},
                                        ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception as e:
            warnings.append("could not cache the class listing: %s" % e)
    elif CACHE.exists():
        listing = {k: tuple(v) for k, v in json.loads(
            CACHE.read_text(encoding="utf-8")).items()}
        warnings.append("could not read /classes/ - using the cached blurbs")

    # Longer text from each class page. A failed fetch keeps the cached copy.
    try:
        pages = json.loads(PAGES.read_text(encoding="utf-8")) if PAGES.exists() else {}
    except Exception:
        pages = {}
    wanted = {match_key(c, listing) for c in categories} - {None}
    fetched = 0
    for key in sorted(wanted):
        slug = slugs.get(key) or pages.get(key, {}).get("slug")
        if not slug:
            continue
        try:
            text = page_text(get("%s/class/%s/" % (BASE, slug)))
        except Exception as e:
            warnings.append("class page %s: %s" % (slug, e))
            continue
        if text:
            pages[key] = {"slug": slug, "long": text}
            fetched += 1
    if fetched:
        try:
            PAGES.write_text(json.dumps(pages, ensure_ascii=False, indent=1,
                                        sort_keys=True), encoding="utf-8")
        except Exception as e:
            warnings.append("could not cache the class pages: %s" % e)

    desc, cat_of, tagtext, keyof, missing = {}, {}, {}, {}, []
    for c in categories:
        key = match_key(c, listing)
        if key:
            keyof[c] = key
            cat_of[c] = listing[key][0]
            long = pages.get(key, {}).get("long", "")
            desc[c] = long if len(long) > len(listing[key][1]) else listing[key][1]
            tagtext[c] = (listing[key][1] + " " + long).strip()
        else:
            desc[c] = NO_DESC
            missing.append(c)
    log("  descriptions: %d of %d class type(s)" % (len(categories) - len(missing), len(categories)))
    if missing:
        log("  no description on Third Space's site for: %s" % ", ".join(sorted(missing)))
    return desc, cat_of, tagtext, keyof

CLUBS_CACHE = HERE / "thirdspace-clubs.json"

def club_hours(warnings):
    """{club: 'Mon-Fri 05:30-22:00 / Sat-Sun 08:00-20:00'} from each club's page.

    Cached, like the descriptions: a club page that cannot be read costs us
    the hours, never the schedule.
    """
    try:
        cached = json.loads(CLUBS_CACHE.read_text(encoding="utf-8"))
    except Exception:
        cached = {}
    out = {}
    for _, club, _ in CLUBS:
        slug = club.lower().replace(" ", "-")
        try:
            nodes = page_nodes(get("%s/clubs/%s/" % (BASE, slug)))
            lines = [x for x in nodes if re.match(r"^(Monday|Saturday)\b.*\d\d:\d\d\s*[\u2013-]\s*\d\d:\d\d$", x)]
            parts = []
            for x in lines:
                m = re.match(r"^(\w+)\s*[\u2013-]\s*(\w+)\s+(\d\d:\d\d)\s*[\u2013-]\s*(\d\d:\d\d)$", x)
                if m:
                    days = (m.group(1)[:3], m.group(2)[:3])
                    label = {("Mon", "Fri"): "WD", ("Sat", "Sun"): "WK"}.get(
                        days, "%s\u2013%s" % days)          # WD weekdays, WK weekend
                    parts.append("%s %s\u2013%s" % (label, m.group(3).lstrip("0"),
                                                    m.group(4).lstrip("0")))
            if parts:
                out[club] = " \u00b7 ".join(parts)
                continue
            warnings.append("%s: no opening hours found on the club page" % club)
        except Exception as e:
            warnings.append("%s club page: %s" % (club, e))
        if cached.get(club):
            out[club] = cached[club]
    if out:
        try:
            CLUBS_CACHE.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception as e:
            warnings.append("could not cache the club hours: %s" % e)
    return out

# What the site's own categories are called here. Per-class overrides ("type" in
# thirdspace-focus.json) beat this, because the site files Pulse under Mind & Body
# and Kettlebells under Sports & Performance.
SITE_TYPE = {"Strength & Conditioning": "Strength", "Sports & Performance": "Conditioning",
             "Mind & Body": "Yoga / mind", "Pilates": "Pilates", "Combat": "Combat",
             "Cycle": "Cycling", "Recovery": "Recovery", "Barre": "Barre",
             "Dance": "Dance", "Running": "Running", "HYROX": "Conditioning"}

def type_tags(categories, cat_of, keyof, warnings):
    """{category: short workout type}: the focus file's "type", else from the site category."""
    hand = load_focus()
    out, unknown = {}, []
    for c in categories:
        entry = hand.get(norm(c)) or hand.get(keyof.get(c, ""))
        t = entry.get("type") if isinstance(entry, dict) else None
        t = t or SITE_TYPE.get(cat_of.get(c, ""))
        if t:
            out[c] = t
        else:
            unknown.append(c)
    if unknown:
        log("  no workout type for: %s" % ", ".join(sorted(unknown)))
    return out

def load_focus():
    try:
        raw = json.loads(FOCUS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {norm(k): v for k, v in raw.items() if not k.startswith("_")}

LEG_WORDS = re.compile(r"\b(legs?|glutes?|quads?|quadriceps|hamstrings?|squats?|lunges?|"
                       r"lower[- ]body|calves|calf)\b", re.I)

def focus_tags(categories, tagtext, keyof, warnings):
    """{category: focus}. The hand-kept file wins; else a keyword guess; else Untagged.

    Anything not in the file is logged, so a new class type never goes
    unnoticed - correct it by adding it to thirdspace-focus.json.
    """
    hand = load_focus()
    out, guessed, untagged = {}, [], []
    for c in categories:
        # 'Hot Yin Yoga' has no entry of its own: it is the listing's Yin Yoga
        entry = hand.get(norm(c)) or hand.get(keyof.get(c, ""))
        tag = entry.get("focus") if isinstance(entry, dict) else entry
        if tag in FOCUS_TAGS:
            out[c] = tag
        elif tagtext.get(c) and LEG_WORDS.search(tagtext[c]):
            out[c] = "Legs"
            guessed.append(c)
        else:
            out[c] = "Untagged"
            untagged.append(c)
    legs = sorted(c for c, f in out.items() if f == "Legs")
    log("  focus: %d class type(s) tagged Legs: %s" % (len(legs), ", ".join(legs) or "none"))
    if guessed:
        log("  focus guessed from the text (add to thirdspace-focus.json to confirm): %s"
            % ", ".join(sorted(guessed)))
    if untagged:
        log("  focus Untagged (add to thirdspace-focus.json): %s" % ", ".join(sorted(untagged)))
    return out

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
        disp = "%02d:%02d" % (hh, mm)                 # 24-hour, shorter than 7:20AM
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

    cats = sorted({r[4] for r in rows})
    desc, cat_by_name, tagtext, keyof = descriptions(cats, warnings)
    focus = focus_tags(cats, tagtext, keyof, warnings)
    types = type_tags(cats, cat_by_name, keyof, warnings)
    hours = club_hours(warnings)
    palette = {c: CAT_COLOUR.get(cat_by_name.get(c, ""), GREY) for c in cats}

    # ONE set of class filters covering all three clubs, with the clubs
    # switched on and off separately - so a single venue group, and the club
    # lives on in each row (r[6]) for the location switches to work on.
    for r in rows:
        r[10] = "T"
    venues = [("T", "Class types", "tsTypes")]
    ls_keys = {"a": "tsAvailOnly", "f": "tsHideFull", "w": "tsHideWorkHours",
               "lo": "tsLocations", "v": "tsFavs", "vv": "tsFavsSeed",
               "c": "tsCollapse", "bk": "tsBookedCol", "l": "tsLegsOnly"}
    html_out, states, counts = refresh.build(
        rows, refresh.TEMPLATE, venues=venues, ls_keys=ls_keys, palette=palette,
        desc=desc, studio_url={club: BASE + "/timetable/" for _, club, _ in CLUBS},
        title="Class schedule — Third Space",
        # Third Space: teal "3S", so the two tabs never look alike.
        icon=refresh.favicon("3S", "#0f6e6e", size=30),
        locations=[club for _, club, _ in CLUBS], focus=focus, location_info=hours, types=types,
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
