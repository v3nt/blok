# -*- coding: utf-8 -*-
"""Your BLOK bookings, read from BLOK's own confirmation emails.

You book as a BLOK member now, not through ClassPass, so ClassPass has no
idea what you are booked into. BLOK emails every booking and cancellation
from no-reply@bloklondon.com; this reads those over IMAP and replays them in
order: the latest email about a class wins, so book -> cancel -> rebook
comes out booked.

No browser, no Claude. The Gmail app password lives in the macOS Keychain
(service "blok-gmail"), never in this repo. One-off setup, in Terminal:

    /usr/bin/python3 ~/Sites/jynk/blok/scraper/blok_mail.py --setup

Then `python3 blok_mail.py` on its own prints what it finds.

If the mailbox can't be reached, the last good result (blok-bookings.json)
is used instead, so one network blip never wipes your bookings off the page.
"""
import argparse, datetime, email, email.header, email.utils, getpass, html, imaplib
import json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "blok-bookings.json"
ACCOUNT = "dan@jynk.net"
SERVICE = "blok-gmail"
SENDER = "no-reply@bloklondon.com"
IMAP_HOST = "imap.gmail.com"
LOOKBACK_DAYS = 60

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], 1)}

def text_of(body):
    """Email HTML -> one line per visible text node."""
    t = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", body, flags=re.S | re.I)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = html.unescape(t).replace("’", "'").replace("\xa0", " ")
    return [re.sub(r"\s+", " ", l).strip() for l in t.splitlines() if l.strip()]

def _field(lines, name):
    for i, l in enumerate(lines[:-1]):
        if l.upper() == name:
            return lines[i + 1]
    return None

def _mins(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)

def parse(body):
    """One email -> an event dict, or None if it is not a booking email.

    Confirmation: CLASS / INSTRUCTOR / TIME / DATE / LOCATION blocks.
    Cancellation: "Your spot at <CLASS> for 08:40, September 28, 2026 has
    been cancelled." - no location, so a cancellation matches on
    date + time + class.
    """
    lines = text_of(body)
    flat = " ".join(lines)
    if "BOOKING CONFIRMED" in flat.upper():
        cls, tm, dt = _field(lines, "CLASS"), _field(lines, "TIME"), _field(lines, "DATE")
        m = re.match(r"\w+,\s*(\d{1,2})\s+(\w+)\s+(\d{4})$", dt or "")
        if not (cls and tm and m and re.match(r"^\d{1,2}:\d\d$", tm)):
            raise ValueError("confirmation email in an unexpected layout")
        d = datetime.date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1)))
        return {"kind": "booked", "cls": cls, "date": d.isoformat(), "mins": _mins(tm),
                "studio": _field(lines, "LOCATION") or "",
                "instructor": _field(lines, "INSTRUCTOR") or ""}
    # Waitlist: "You're on the waitlist for CALISTHENICS 60 at 11:10, Saturday,
    # 10 October 2026." / "You have been removed from the waitlist for ...".
    # Neither names the studio in the text (the .ics attachment may - see fetch).
    m = re.search(r"(You.re on|removed from) the waitlist for (.+?) at (\d{1,2}:\d\d), "
                  r"\w+, (\d{1,2}) (\w+) (\d{4})", flat)
    if m:
        d = datetime.date(int(m.group(6)), MONTHS[m.group(5).lower()], int(m.group(4)))
        return {"kind": "waitlist" if m.group(1).endswith("on") else "unwaitlisted",
                "cls": m.group(2).strip(), "date": d.isoformat(),
                "mins": _mins(m.group(3)), "studio": ""}
    m = re.search(r"Your spot at (.+?) for (\d{1,2}:\d\d), (\w+) (\d{1,2}), (\d{4}) "
                  r"has been cancelled", flat)
    if m:
        d = datetime.date(int(m.group(5)), MONTHS[m.group(3).lower()], int(m.group(4)))
        return {"kind": "cancelled", "cls": m.group(1).strip(), "date": d.isoformat(),
                "mins": _mins(m.group(2)), "studio": ""}
    return None

def replay(events):
    """Events (each with 'sent', an ISO timestamp) -> what you hold now.

    Keyed on date + time + class; the newest email for a key wins. Each result
    has kind "booked" or "waitlist".
      booked        -> booked (also how a waitlist spot that came through shows)
      cancelled     -> gone
      waitlist      -> on the waitlist, unless already booked
      unwaitlisted  -> off the waitlist; a booking for that class is kept,
                       because BLOK may send this when you are moved INTO it
    """
    state = {}
    for e in sorted(events, key=lambda e: e["sent"]):
        key = (e["date"], e["mins"], e["cls"])
        cur = state.get(key)
        if e["kind"] == "booked":
            state[key] = e
        elif e["kind"] == "cancelled":
            state.pop(key, None)
        elif e["kind"] == "waitlist":
            if not (cur and cur["kind"] == "booked"):
                state[key] = e
        elif e["kind"] == "unwaitlisted":
            if cur and cur["kind"] == "waitlist":
                state.pop(key)
    return sorted(state.values(), key=lambda e: (e["date"], e["mins"]))

# --- mailbox ---------------------------------------------------------------

def password():
    r = subprocess.run(["security", "find-generic-password", "-s", SERVICE,
                        "-a", ACCOUNT, "-w"], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("no Gmail app password in the Keychain - run: "
                           "/usr/bin/python3 %s --setup" % pathlib.Path(__file__).resolve())
    return r.stdout.strip()

def _body(msg):
    parts = msg.walk() if msg.is_multipart() else [msg]
    best = ""
    for p in parts:
        if p.get_content_type() in ("text/html", "text/plain"):
            raw = p.get_payload(decode=True) or b""
            txt = raw.decode(p.get_content_charset() or "utf-8", "replace")
            if p.get_content_type() == "text/html" or not best:
                best = txt
    return best

def _ics_studio(msg):
    """Clapton / Shoreditch from an attached calendar invite, or ""."""
    for p in (msg.walk() if msg.is_multipart() else [msg]):
        if p.get_content_type() == "text/calendar" or (p.get_filename() or "").endswith(".ics"):
            txt = (p.get_payload(decode=True) or b"").decode("utf-8", "replace")
            m = re.search(r"^LOCATION[^:]*:(.*)$", txt, re.M)
            for name in ("Clapton", "Shoreditch"):
                if m and name.lower() in m.group(1).lower():
                    return name
    return ""

def fetch(days=LOOKBACK_DAYS):
    since = (datetime.date.today() - datetime.timedelta(days=days)).strftime("%d-%b-%Y")
    im = imaplib.IMAP4_SSL(IMAP_HOST, timeout=30)
    try:
        im.login(ACCOUNT, password())
        # All Mail, so archived/labelled confirmations still count.
        ok, _ = im.select('"[Gmail]/All Mail"', readonly=True)
        if ok != "OK":
            im.select("INBOX", readonly=True)
        ok, data = im.search(None, "FROM", '"%s"' % SENDER, "SINCE", since)
        events, skipped = [], 0
        for num in (data[0].split() if ok == "OK" else []):
            ok, parts = im.fetch(num, "(RFC822)")
            if ok != "OK":
                continue
            msg = email.message_from_bytes(parts[0][1])
            try:
                ev = parse(_body(msg))
            except ValueError:
                skipped += 1
                continue
            if ev and not ev.get("studio"):
                ev["studio"] = _ics_studio(msg)
            if ev:
                sent = email.utils.parsedate_to_datetime(msg["Date"])
                ev["sent"] = sent.astimezone(datetime.timezone.utc).isoformat()
                events.append(ev)
        return events, skipped
    finally:
        try:
            im.logout()
        except Exception:
            pass

def bookings(log=print, warnings=None):
    """Current bookings. Falls back to the last good result on any failure."""
    warnings = warnings if warnings is not None else []
    try:
        events, skipped = fetch()
        current = replay(events)
        CACHE.write_text(json.dumps({
            "checked": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "emails": len(events), "bookings": current}, indent=1), encoding="utf-8")
        nw = sum(1 for b in current if b.get("kind") == "waitlist")
        log("  BLOK emails: %d booking/cancellation/waitlist email(s) -> %d booking(s), %d waitlist"
            % (len(events), len(current) - nw, nw))
        if skipped:
            warnings.append("%d BLOK email(s) in an unexpected layout were skipped" % skipped)
        return current
    except Exception as e:
        try:
            cached = json.loads(CACHE.read_text(encoding="utf-8"))
            warnings.append("BLOK mailbox unreachable (%s) - using bookings from %s"
                            % (e, cached.get("checked")))
            return cached.get("bookings", [])
        except Exception:
            warnings.append("BLOK mailbox unreachable (%s) and no saved bookings" % e)
            return []

def cached():
    """The last good result, without touching the network (for --rebuild)."""
    try:
        return json.loads(CACHE.read_text(encoding="utf-8")).get("bookings", [])
    except Exception:
        return []

def setup():
    print("Create an app password at https://myaccount.google.com/apppasswords")
    print("(name it 'blok'), then paste it here. It goes into your Keychain only.")
    pw = getpass.getpass("App password for %s: " % ACCOUNT).replace(" ", "")
    if not pw:
        sys.exit("nothing entered - no change")
    subprocess.run(["security", "add-generic-password", "-U", "-s", SERVICE,
                    "-a", ACCOUNT, "-w", pw], check=True)
    print("Saved. Checking the mailbox...")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--setup", action="store_true", help="store the Gmail app password")
    args = ap.parse_args()
    if args.setup:
        setup()
    w = []
    for b in bookings(warnings=w):
        print("  %s %02d:%02d  %-28s %-10s %s" % (b["date"], b["mins"] // 60, b["mins"] % 60,
                                                 b["cls"], b["studio"],
                                                 "WAITLIST" if b.get("kind") == "waitlist" else ""))
    for x in w:
        print("  ! " + x)
    return 1 if any("unreachable" in x for x in w) else 0

if __name__ == "__main__":
    sys.exit(main())
