#!/bin/bash
# Commits and pushes whatever the scheduled BLOK scrape wrote into this folder.
#
# All git operations happen HERE, on the Mac - never inside Claude's sandbox.
# The sandbox mount cannot delete files, so git's lock cleanup fails there and
# leaves stale .git/*.lock behind.
#
# Safe to run repeatedly: does nothing when there is nothing to do.
# Self-healing: a wedged rebase falls back to flattening onto origin rather
# than failing forever every 10 minutes.
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO"

log() { echo "$(date '+%F %T')  $*"; }

# ---------------------------------------------------------------- housekeeping

# Clear stale locks left by a sandbox-side git attempt.
for lock in .git/HEAD.lock .git/index.lock; do
  [ -e "$lock" ] && { log "clearing stale $lock"; rm -f "$lock"; }
done

# A rebase left half-finished by a previous run blocks everything after it.
if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
  log "found interrupted rebase, aborting it"
  git rebase --abort 2>/dev/null || git rebase --quit 2>/dev/null || true
fi

# .DS_Store must be excluded via .git/info/exclude, NOT .gitignore alone.
# .gitignore is versioned: during a rebase, git checks out OLD commits whose
# .gitignore predates the rule, and the untracked .DS_Store Finder just
# recreated then blocks the replay. info/exclude is unversioned, so it always
# applies. This was the cause of the repeated "REBASE FAILED" runs.
grep -qxF '.DS_Store' .git/info/exclude 2>/dev/null || echo '.DS_Store' >> .git/info/exclude
grep -qxF '.DS_Store' .gitignore 2>/dev/null || echo '.DS_Store' >> .gitignore
# Untrack every .DS_Store anywhere in the tree, not just the root one -
# a tracked _to_delete/.DS_Store collides during rebase exactly the same way.
TRACKED_DS=$(git ls-files '*.DS_Store' || true)
if [ -n "$TRACKED_DS" ]; then
  log "untracking $(echo "$TRACKED_DS" | wc -l | tr -d ' ') tracked .DS_Store file(s)"
  echo "$TRACKED_DS" | tr '\n' '\0' | xargs -0 git rm --cached -q -- 2>/dev/null || true
fi

# --------------------------------------------------------------- health report

write_status() {
  local scrape_tail scrape_state scrape_line idx_mtime rows push_err

  # Only ever judge the RECENT tail. Grepping the whole log resurrects errors
  # that were fixed hours ago and makes STATUS.md permanently look on fire.
  scrape_tail=$(tail -40 scraper/refresh.log 2>/dev/null || true)
  scrape_line=$(echo "$scrape_tail" | grep -E '^----- ' | tail -1 || true)

  if echo "$scrape_tail" | grep -q 'FATAL\|Traceback\|refresh FAILED'; then
    scrape_state="FAIL"
  elif echo "$scrape_tail" | grep -q 'refresh OK'; then
    scrape_state="OK"
  else
    # Legacy refresh.sh logged "exit 0" even on crash ($(date) reset $?), so an
    # old-format line proves nothing. Do not call it OK.
    scrape_state="UNKNOWN"
  fi

  idx_mtime=$(date -r index.html '+%F %T %Z' 2>/dev/null || echo unknown)
  rows=$(grep -oE '\["[0-9]{4}-[0-9]{2}-[0-9]{2}"' index.html 2>/dev/null | wc -l | tr -d ' ' || true)
  push_err=$(tail -200 push-blok.log 2>/dev/null | grep -E 'BLOCKED|FLATTENED|REBASE FAILED|^fatal:' | tail -3 || true)

  # NOTE: deliberately no commit sha and no "generated at" clock here. Anything
  # that changes on every run makes this file dirty every 10 minutes and floods
  # the history with empty status commits.
  {
    echo "# BLOK pipeline status"
    echo
    echo "Machine-written by \`push-blok.sh\`. Committed so it is readable from"
    echo "GitHub (and therefore from a phone) without touching the Mac."
    echo
    echo "| Field | Value |"
    echo "|---|---|"
    echo "| Scrape result | **$scrape_state** |"
    echo "| Last scrape log line | \`${scrape_line:-none}\` |"
    echo "| index.html modified | $idx_mtime |"
    echo "| Classes in index.html | ${rows:-0} |"
    echo
    if [ "$scrape_state" = "FAIL" ]; then
      echo "## Last scrape failure"
      echo
      echo '```'
      echo "$scrape_tail" | tail -20
      echo '```'
      echo
    fi
    if [ -n "$push_err" ]; then
      echo "## Recent push errors"
      echo
      echo '```'
      echo "$push_err"
      echo '```'
    fi
  } > STATUS.md
}

write_status

# ------------------------------------------------------------------- validate

# NEVER publish an index.html whose JavaScript cannot parse. On 19 Aug 2026 a
# generated file had one unclosed '{'; the page loaded, threw "Unexpected end
# of input", and rendered an empty table for hours. HTML validity is not
# enough - the whole schedule lives inside one <script> block.
if [ -f validate-index.py ]; then
  if ! VALIDATION=$(python3 validate-index.py index.html 2>&1); then
    log "BLOCKED: $VALIDATION"
    log "index.html left uncommitted; last good version stays live"
    git checkout -- index.html 2>/dev/null || true
    write_status
    git add -A -- ':!index.html'
    if ! git diff --cached --quiet; then
      git commit -q -m "Pipeline status: index.html rejected by validator"
      git push origin main 2>/dev/null || true
    fi
    exit 1
  fi
  log "validated: $VALIDATION"
fi

# -------------------------------------------------------------------- commit

git add -A

if ! git diff --cached --quiet; then
  # Count class rows. Matches both layouts: date-first (["2026-08-17","4:30pm")
  # and the older time-first (["4:30PM"). Never let a zero count abort the
  # commit: grep exits 1 on no match, and set -euo pipefail would kill us here.
  ROWS=$(grep -oE '\["[0-9]{4}-[0-9]{2}-[0-9]{2}"|\["[0-9]*:[0-9]*[AP]M"' index.html 2>/dev/null | wc -l | tr -d ' ' || true)
  ROWS=${ROWS:-0}
  git commit -q -m "Refresh BLOK schedule $(date '+%a %-d %b %Y, %H:%M %Z') - ${ROWS} classes"
  log "committed $(git log --oneline -1)"
fi

git fetch origin main --quiet

# ------------------------------------------------------------------ reconcile

# Another writer (a Cowork run using its own clone) can push to origin, leaving
# us behind so push fails non-fast-forward. This folder is the source of truth
# for index.html, so replay our commits on top of origin, ours winning.
flatten_onto_origin() {
  log "FLATTENED onto origin/main (rebase could not be completed)"
  git rebase --abort 2>/dev/null || true
  # Never silently drop a file that only exists on origin.
  local only_on_origin
  only_on_origin=$(comm -13 <(git ls-files | sort) \
                            <(git ls-tree -r --name-only origin/main | sort) \
                   | grep -v '^\.DS_Store$\|/\.DS_Store$' || true)
  if [ -n "$only_on_origin" ]; then
    log "restoring origin-only files: $(echo "$only_on_origin" | tr '\n' ' ')"
    echo "$only_on_origin" | tr '\n' '\0' | xargs -0 git checkout origin/main -- 2>/dev/null || true
  fi
  git reset --soft origin/main
  git add -A
  if ! git diff --cached --quiet; then
    git commit -q -m "Refresh BLOK schedule $(date '+%a %-d %b %Y, %H:%M %Z') (flattened onto origin)"
  fi
}

BEHIND=$(git rev-list --count main..origin/main)
if [ "$BEHIND" != "0" ]; then
  log "behind origin by $BEHIND, rebasing (ours wins)"
  git add -A
  git diff --cached --quiet || git commit -q -m "Local changes before rebase"
  rm -f .DS_Store
  if ! git rebase -X theirs origin/main; then
    flatten_onto_origin
  fi
fi

# ---------------------------------------------------------------------- push

if [ "$(git rev-parse main)" = "$(git rev-parse origin/main)" ]; then
  log "up to date ($(git log --oneline -1 main))"
  exit 0
fi

log "pushing $(git rev-list --count origin/main..main) commit(s)"
git push origin main
log "pushed -> $(git log --oneline -1 main)"

# Keep the log from growing without bound.
if [ "$(wc -c < push-blok.log 2>/dev/null || echo 0)" -gt 262144 ]; then
  tail -500 push-blok.log > push-blok.log.tmp && mv push-blok.log.tmp push-blok.log
fi
