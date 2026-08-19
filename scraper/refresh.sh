#!/bin/bash
# Scrape ClassPass and rebuild index.html. Run by launchd every 4 hours.
# push-blok.sh (every 10 min) commits and pushes whatever this writes.
#
# Do NOT put a command substitution between the python call and the exit-code
# read: $(date) resets $?. That bug made every failure log as "exit 0".
set -uo pipefail
cd "$(dirname "$0")"

PY="${BLOK_PYTHON:-$(command -v python3)}"

echo "----- $(date '+%F %T') refresh start (python: $PY)"

if [ -z "$PY" ]; then
  echo "FATAL: no python3 on PATH"
  echo "----- $(date '+%F %T') refresh exit 127"
  exit 127
fi

if ! "$PY" -c 'import playwright' 2>/dev/null; then
  echo "FATAL: playwright not installed for $PY"
  echo "       fix: $PY -m pip install playwright && $PY -m playwright install chromium"
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
