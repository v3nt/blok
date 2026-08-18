# BLOK schedule tracker — build brief

Spec for any Cowork project/session that regenerates `index.html` for
https://v3nt.github.io/blok/. Written 18 Aug 2026 after a run that silently
regressed the page. **Read all of section 6 before writing any code.**

---

## 1. Goal

A single self-contained `index.html` listing every upcoming class in eight
categories at BLOK's two London studios, with real booking status, for as far
ahead as ClassPass publishes (~12–13 days).

## 2. Sources

| Studio | URL |
|---|---|
| Clapton | https://classpass.com/studios/blok-clapton-london |
| Shoreditch | https://classpass.com/studios/blok-shoreditch-london |

Public pages — no login step required. **But** the browser profile must be
signed in to ClassPass for `BOOKED` rows to appear. If nothing ever comes back
as booked, suspect the session, not the parser.

## 3. Scrape method

Chrome tools only. Rows live in `.Schedule__rows` as `<section>` elements;
advance with `button[aria-label="Next day"]`.

- Expand every "See more" before reading (loop, ~180ms apart).
- One day takes ~18s; the CDP bridge times out at 45s. **Two days per
  `javascript_tool` call, never three.**
- End every call with the accumulated rows so they land in context
  immediately. A run that dies mid-scrape must not lose what it collected.
- If a call times out, the page keeps running — probe collected day headers
  before continuing or you'll skip a day.
- Reset the accumulator when switching studios.
- Day 1 returning 0 rows just means today's classes have finished. Keep going.
  Stop at 14 days or when a *future* day returns 0.

**Filter to these class names.** Scraping unfiltered pulls BLOK's entire
timetable (Open Gym, Reformer Pilates, Barre, Hot + Cold, BLOKFIT…) and will
overflow the output limit:

```
/CALISTHENICS|BLOKSTRENGTH|HANDSTAND|POWER YOGA|MOBILITY|YIN/i
```

## 4. Categories (all eight — do not trim)

| ClassPass name | Category | Colour |
|---|---|---|
| `CALISTHENICS 60` / `50` | Calisthenics | `#7c5cff` |
| `BLOKSTRENGTH: UPPER BODY` | Strength: Upper | `#2e9e5b` |
| `BLOKSTRENGTH: LOWER BODY` | Strength: Lower | `#c77d0a` |
| `BLOKSTRENGTH: FULL BODY` | Strength: Full Body | `#1f7fd1` |
| `HANDSTANDS 60` / `50` | Handstands | `#d6336c` |
| `POWER YOGA` (+ `50`/`75`) | Power | `#e8590c` |
| `BLOKMOBILITY` | Mobility | `#0ca678` |
| `YIN YOGA`, `YIN YANG FLOW 60` | Yin | `#7048e8` |

Fail loudly on any class that matches the regex but no category — silent
dropping is how the page loses content.

## 5. Availability — read the tooltip, not the label

Status comes from `button[data-tooltip]`. "Reserve" is displayed for several
different states, so visible text alone is unreliable.

| Signal | State | Label | Colour |
|---|---|---|---|
| no tooltip + "N credits" | `bookable` | Bookable (N credits) | `#1f8a3c` |
| "There are no spots left…" | `full` | Full — no spots left | `#c0392b` |
| "The booking window opens on X" | `soon` | Books open X | `#b06a00` |
| visible "Cancel RESERVED" | `booked` | You're booked | `#1f7fd1` |
| "The booking window is now closed." | `closed` | Booking closed | `#8a8a8f` |

Match credits with `/^C\d+$/`, **not** `startswith("C")` — `CLOSED` also starts
with C and renders as "Bookable (LOSED credits)".

Assert the five state counts sum to the row count before publishing.

## 6. Output — the page already has features. Do not rebuild from scratch blind.

**The single biggest failure mode: regenerating from a stale spec and
amputating features nobody re-described.** Before writing the generator, open
the current live page (or `git show HEAD:index.html`) and inventory what it
has. Anything present there is in scope whether or not this brief mentions it.

Required as of 18 Aug 2026:

- Title `BLOK — class schedule`; subtitle: studio links · date range · class
  count · refreshed timestamp.
- Legend with per-state counts and colour dots.
- Filter bar: "Bookable now only", "Hide full", "Hide weekday 8:00am–5:25pm",
  one checkbox per category with counts, and a **Reset filters** button.
- **"Your booked classes" panel** above the table, soonest first, showing
  `Day D Mon, TIME · Category · Studio · Instructor · N min`. Hidden when empty.
- Sticky filter bar; day-divider rows; category pills; coloured status text;
  full rows dimmed via `tbody tr[data-state="full"] td:not(:last-child){opacity:.55}`.
- Rendered `<tr>` must carry `data-cat`, `data-state`, `data-avail` (1 only for
  bookable), `data-wd`, `data-mins`.
- Sort by date, then time, then studio. Last column header "Booking status".

**localStorage** keys: `blokAvailOnly`, `blokHideFull`, `blokHideWorkHours`,
`blokTypes`. Wrap all access in try/catch, and **validate `blokTypes` against
the current category list** — drop unknown entries, fall back to all if nothing
survives. A stale saved filter from an older category naming scheme will
otherwise blank the entire table with no error.

Emit rows as a compact JS array plus a render function, not static markup.
Target ~30KB. Generate via a script; never hand-write the HTML. Print row
count, state counts, category counts and byte size at the end.

## 7. Publishing

Order matters — do GitHub first, artifact last; whichever runs last is what
gets dropped when a run runs out of room.

1. **Local folder.** Copy `index.html` into `~/Sites/jynk/blok/`. That's all.
   **Never run `git add/commit/push` in that folder** — through the mount git
   can't clean up its lock files and leaves `.git/index.lock` jamming the
   user's own commands. Read-only git (`log`, `show`, `status`) is fine and is
   useful for diffing against the previous version. A launchd agent runs
   `push-blok.sh` every 10 min and does the commit/push on the Mac.
2. **GitHub API.** Currently returns 403 "Resource not accessible by
   integration" on `create_or_update_file`. The token authenticates as `v3nt`
   and reads fine; it lacks Contents:write. The user reports the GitHub App
   permissions route does not fix it — **don't suggest it again**. Skip this
   step.
3. **Artifact.** `update_artifact` with id `blok-2week-schedule` — update, never
   create a new one.

**Scheduled runs get no folder mount.** `~/Sites/jynk/blok` is only present if
a human approves `request_cowork_directory`, which nobody can do at 4am. Every
run does write `index.html` to its own outputs directory on the Mac, so the
durable unattended fix is for `push-blok.sh` to glob for the newest one:

```bash
SRC=$(ls -t ~/Library/Application\ Support/Claude/local-agent-mode-sessions/*/*/*/outputs/index.html 2>/dev/null | head -1)
[ -n "$SRC" ] && cp "$SRC" ~/Sites/jynk/blok/index.html
```

## 8. Browser hygiene

The browser is needed **only** for scraping. Close the tab when switching
studios and again the instant scraping ends; confirm with a follow-up context
call. If you bail out early for any reason, close tabs on the way out. If a JS
call times out, close first, then decide whether to resume.

Note: you can only see and close tabs in your *own* session's tab group.
Orphans left by a crashed earlier run are invisible and unclosable — they
accumulate until the user clears them by hand. Prevention is the only control
you have.

## 9. Reporting

State row count, breakdown by booking state, date range, and the status of each
destination **separately**. Never imply the live page updated — only the
launchd agent can make that true. If a studio page or button flow broke, say
which and why, and still publish what was collected.
