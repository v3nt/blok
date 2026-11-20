# -*- coding: utf-8 -*-
"""Class focus and workout-type tagging, shared by 3rdspace.html and index.html.

Both pages show the same things on a class: a workout TYPE (Strength, Pilates,
Combat...) and a body FOCUS (Legs, Upper, Full body...), which drive the Legs
filter, the tooltip's top line and the type labels in the schedule. The logic
lives here ONCE so the two pages cannot drift apart; each page only supplies
its own hand-kept file (thirdspace-focus.json, blok-focus.json) and its own
class names.

Setting "focus": "Untagged" in the file records that a class was reviewed and has
no single body focus, which also stops the keyword guess from tagging it.

A hand-kept file maps a class name (lowercased, without the duration or colon
suffix) to {"focus": ..., "type": ..., "why": ...}. The hand file always wins.
"""
import html, json, re

FOCUS_TAGS = ("Legs", "Upper", "Full body", "Core", "Cardio", "Mobility-Recovery")

LEG_WORDS = re.compile(r"\b(legs?|glutes?|quads?|quadriceps|hamstrings?|squats?|lunges?|"
                       r"lower[- ]body|calves|calf)\b", re.I)

def norm(name):
    """Compare class names loosely: 'Lift - Weightlifting Classes' is 'Lift'."""
    n = html.unescape(name).lower()
    n = re.split(r"[–—|:]", n)[0]
    n = re.sub(r"[^a-z0-9 ]", " ", n)
    return re.sub(r"\s+", " ", n).strip()

def norm_full(name):
    """Like norm(), but keeps everything after a colon: 'BLOKSTRENGTH: LOWER BODY' stays whole."""
    n = html.unescape(name).lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", n)).strip()

def page_nodes(page):
    """A web page as a list of its visible text nodes."""
    page = re.sub(r"<(script|style|svg|noscript)[^>]*>.*?</\1>", "", page, flags=re.S)
    page = re.sub(r"<!--.*?-->", "", page, flags=re.S)
    return [re.sub(r"\s+", " ", html.unescape(p)).strip()
            for p in re.split(r"<[^>]+>", page) if p.strip()]

def order_locations(names, facilities, class_counts):
    """Most facilities first, then most classes, then name."""
    return sorted(names, key=lambda c: (-len(facilities.get(c, [])), -class_counts.get(c, 0), c))

def load_focus(path, normalize=None):
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    normalize = normalize or norm
    return {normalize(k): v for k, v in raw.items() if not k.startswith("_")}

def _entry(hand, category, alias_key="", normalize=None):
    return hand.get((normalize or norm)(category)) or hand.get(alias_key or "")

def type_tags(categories, site_type_of, aliases, path, log=print, normalize=None):
    """{category: short workout type}: the hand file's "type", else site_type_of(category)."""
    hand = load_focus(path, normalize)
    out, unknown = {}, []
    for c in categories:
        e = _entry(hand, c, aliases.get(c, ""), normalize)
        t = (e.get("type") if isinstance(e, dict) else None) or site_type_of(c)
        if t:
            out[c] = t
        else:
            unknown.append(c)
    if unknown:
        log("  no workout type for: %s" % ", ".join(sorted(unknown)))
    return out

def focus_tags(categories, tagtext, aliases, path, log=print, filename="the focus file", normalize=None):
    """{category: focus}. The hand file wins; else a keyword guess on the text; else Untagged.

    Anything not in the file is logged, so a new class type never goes
    unnoticed - correct it by adding it to the page's focus file.
    """
    hand = load_focus(path, normalize)
    out, guessed, untagged = {}, [], []
    for c in categories:
        e = _entry(hand, c, aliases.get(c, ""), normalize)
        tag = e.get("focus") if isinstance(e, dict) else e
        if tag in FOCUS_TAGS:
            out[c] = tag
        elif tag == "Untagged":                 # reviewed by hand: no single body focus
            out[c] = "Untagged"
        elif tagtext.get(c) and LEG_WORDS.search(tagtext[c]):
            out[c] = "Legs"
            guessed.append(c)
        else:
            out[c] = "Untagged"
            untagged.append(c)
    legs = sorted(c for c, f in out.items() if f == "Legs")
    log("  focus: %d class type(s) tagged Legs: %s" % (len(legs), ", ".join(legs) or "none"))
    if guessed:
        log("  focus guessed from the text (add to %s to confirm): %s"
            % (filename, ", ".join(sorted(guessed))))
    if untagged:
        log("  focus Untagged (add to %s): %s" % (filename, ", ".join(sorted(untagged))))
    return out
