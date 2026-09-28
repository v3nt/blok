# -*- coding: utf-8 -*-
"""Offline checks for blok_mail.py - no network, no Keychain.

The fixtures copy the text layout of BLOK's real emails (Sep 2026) without
their tracking links. The sequence mirrors the real inbox: four bookings,
one of them (Mon 28 Sep 08:40) cancelled afterwards.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import blok_mail as bm
import refresh

def confirm(cls, who, tm, date, loc):
    return ("<html><head><style>p{margin:0}</style></head><body>"
            "<h1><span>BOOKING CONFIRMED. </span></h1><p>Hi Daniel,</p>"
            "<p>You&#39;re signed up to %s.</p>"
            "<table><tr><td>CLASS</td><td>%s</td></tr><tr><td>INSTRUCTOR</td><td>%s</td></tr>"
            "<tr><td>TIME</td><td>%s</td></tr><tr><td>DATE</td><td>%s</td></tr>"
            "<tr><td>LOCATION</td><td>%s</td></tr><tr><td>STUDIO</td><td>Studio 1</td></tr>"
            "</table><p>ARRIVE FASHIONABLY EARLY</p></body></html>"
            % (cls, cls, who, tm, date, loc))

def cancel(cls, tm, mdy):
    return ("<h1><span class=\"x\">RESERVATION CANCELLED. </span></h1>"
            "<p>Hi Daniel, <br><br>Your spot at %s for %s, %s has been cancelled. </p>"
            % (cls, tm, mdy))

MAIL = [
    ("2026-09-24T09:32:41+00:00", confirm("BLOKSTRENGTH: FULL BODY", "John Aiwone", "18:35", "Wednesday, 30 September 2026", "Clapton")),
    ("2026-09-24T09:33:05+00:00", confirm("CALISTHENICS 60", "Samuel Deschamps", "19:40", "Wednesday, 30 September 2026", "Clapton")),
    ("2026-09-24T09:34:26+00:00", confirm("CALISTHENICS 60", "Manu Beja da Costa", "08:40", "Monday, 28 September 2026", "Clapton")),
    ("2026-09-24T09:44:17+00:00", confirm("CALISTHENICS 60", "Daniel Zivatovic", "11:10", "Saturday, 3 October 2026", "Clapton")),
    ("2026-09-24T09:48:34+00:00", confirm("BLOKSTRENGTH: LOWER BODY", "Karmen Ledgister", "12:20", "Friday, 2 October 2026", "Shoreditch")),
    ("2026-09-27T09:24:38+00:00", cancel("CALISTHENICS 60", "08:40", "September 28, 2026")),
    ("2026-01-07T18:46:03+00:00", "<h1>YOUR PASSWORD RESET LINK</h1><p>Hi Daniel</p>"),
]

checks = fails = 0
def check(name, ok, detail=""):
    global checks, fails
    checks += 1
    if not ok:
        fails += 1
    print(("  ok   " if ok else "  FAIL ") + name + ("" if ok else "  -- " + detail))

events = []
for sent, body in MAIL:
    e = bm.parse(body)
    if e:
        e["sent"] = sent
        events.append(e)
check("a confirmation parses", events[0] == {**events[0], "kind": "booked",
      "cls": "BLOKSTRENGTH: FULL BODY", "date": "2026-09-30", "mins": 18 * 60 + 35,
      "studio": "Clapton", "instructor": "John Aiwone"}, str(events[0]))
check("a cancellation parses", events[5]["kind"] == "cancelled"
      and (events[5]["date"], events[5]["mins"], events[5]["cls"]) == ("2026-09-28", 520, "CALISTHENICS 60"),
      str(events[5]))
check("non-booking BLOK emails are ignored", len(events) == 6)

cur = bm.replay(events)
got = {(b["date"], b["mins"], b["cls"], b["studio"]) for b in cur}
want = {("2026-09-30", 1115, "BLOKSTRENGTH: FULL BODY", "Clapton"),
        ("2026-09-30", 1180, "CALISTHENICS 60", "Clapton"),
        ("2026-10-03", 670, "CALISTHENICS 60", "Clapton"),
        ("2026-10-02", 740, "BLOKSTRENGTH: LOWER BODY", "Shoreditch")}
check("cancelled class is dropped, the other four remain", got == want, str(sorted(got)))

rebook = dict(events[2], sent="2026-09-27T10:00:00+00:00")
check("book -> cancel -> rebook ends booked",
      any(b["date"] == "2026-09-28" for b in bm.replay(events + [rebook])))
check("replay does not depend on arrival order",
      bm.replay(list(reversed(events))) == cur)

try:
    bm.parse("<h1>BOOKING CONFIRMED.</h1><p>something else entirely</p>")
    check("a changed email layout is reported, not guessed", False, "no error")
except ValueError:
    check("a changed email layout is reported, not guessed", True)

# The keys the page matches on: class names collapse the same way the
# schedule collapses them ("CALISTHENICS 60" is the CALISTHENICS row).
row = lambda d, m, cat, st: [d, m, "", 60, cat, "", st, "unknown", "Check on ClassPass", "", "B"]
rows = [row("2026-09-30", 1180, "CALISTHENICS", "Clapton"),
        row("2026-09-30", 1180, "OPEN GYM", "Clapton"),          # same time, other class
        row("2026-09-28", 520, "CALISTHENICS", "Clapton"),       # cancelled
        row("2026-10-02", 740, "BLOKSTRENGTH: LOWER BODY", "Shoreditch")]
keys = {(b["date"], b["mins"], b["studio"], refresh.categorise(b["cls"], "B")) for b in cur}
w = []
hit = refresh.mark_booked(rows, keys, w, today="2026-09-28")
check("emails mark exactly the booked rows",
      [r[7] for r in rows] == ["booked", "unknown", "unknown", "booked"], str([r[7] for r in rows]))

print(("OK: %d BLOK email checks passed" % checks) if not fails
      else "FAIL: %d of %d BLOK email checks failed" % (fails, checks))
sys.exit(1 if fails else 0)
