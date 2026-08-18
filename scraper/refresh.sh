#!/bin/bash
# Scrape ClassPass and rebuild index.html. Run by launchd every 4 hours.
# push-blok.sh (every 10 min) commits and pushes whatever this writes.
set -uo pipefail
cd "$(dirname "$0")"
PY=$(command -v python3)
echo "----- $(date '+%F %T') refresh start"
"$PY" refresh.py
echo "----- $(date '+%F %T') refresh exit $?"
