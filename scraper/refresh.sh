#!/bin/bash
# Scrape ClassPass and rebuild index.html. Run by launchd every 4 hours.
# push-blok.sh (every 10 min) commits and pushes whatever this writes.
#
# Do NOT put a command substitution between the python call and the exit-code
# read: $(date) resets $?. That bug made every failure log as "exit 0".
set -uo pipefail
cd "$(dirname "$0")"

# There is more than one python3 on this Mac and only one of them has
# playwright: launchd runs with a minimal PATH and gets /usr/bin/python3,
# while an interactive shell gets Homebrew's. Picking "the first python3 on
# PATH" therefore worked from launchd and failed by hand. Pick the first one
# that can actually import playwright instead.
PY=""
for CANDIDATE in "${BLOK_PYTHON:-}" "$(command -v python3 || true)" \
                 /usr/bin/python3 /opt/homebrew/bin/python3 /usr/local/bin/python3; do
  [ -n "$CANDIDATE" ] || continue
  [ -x "$CANDIDATE" ] || continue
  if "$CANDIDATE" -c 'import playwright' 2>/dev/null; then PY="$CANDIDATE"; break; fi
done

echo "----- $(date '+%F %T') refresh start (python: ${PY:-none with playwright})"

if [ -z "$PY" ]; then
  echo "FATAL: no python3 with playwright. Tried BLOK_PYTHON, PATH, /usr/bin,"
  echo "       /opt/homebrew/bin, /usr/local/bin."
  echo "       fix: /usr/bin/python3 -m pip install playwright && \\"
  echo "            /usr/bin/python3 -m playwright install chromium"
  echo "----- $(date '+%F %T') refresh exit 3"
  exit 3
fi

"$PY" refresh.py
RC=$?

NOW=$(date '+%F %T')
if [ "$RC" -eq 0 ]; then
  echo "----- $NOW refresh OK (exit 0)"
else
  echo "----- $NOW refresh FAILED (exit $RC)"
fi
exit "$RC"
