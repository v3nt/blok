#!/bin/bash
# One-time setup of the BLOK pipeline on the home server (Ubuntu 24.04, user
# `server`). Run from the repo checkout at /srv/apps/blok:
#
#   bash deploy/install-linux.sh            # install everything, timers OFF
#   bash deploy/install-linux.sh --enable   # ...and switch the timers on
#
# Leave the timers off until the Mac's launchd jobs are unloaded: two machines
# pushing index.html to the same branch overwrite each other.
set -euo pipefail
REPO=/srv/apps/blok
cd "$REPO"
[ "$(pwd)" = "$REPO" ] || { echo "run from $REPO"; exit 1; }

echo "== system packages (Xvfb for the headed browser, venv for playwright)"
sudo apt-get update -qq
sudo apt-get install -y -qq xvfb python3-venv git >/dev/null

echo "== python venv + playwright"
[ -x .venv/bin/python ] || python3 -m venv .venv
.venv/bin/pip install -q --upgrade pip playwright
# Google Chrome (the scraper prefers it: ClassPass renders in Chrome, not
# always in bundled Chromium) plus Chromium for the test suites, with OS deps.
sudo .venv/bin/python -m playwright install-deps chromium
sudo .venv/bin/python -m playwright install chrome || echo "  ! Chrome install failed - the scraper falls back to Chromium"
.venv/bin/python -m playwright install chromium

echo "== git identity for the automatic commits"
git config user.name  >/dev/null || git config user.name  "nab9 BLOK bot"
git config user.email >/dev/null || git config user.email "dan@jynk.net"

echo "== Gmail app password (your bookings)"
if [ -s "$HOME/.config/blok/gmail-app-password" ]; then
  echo "  already set"
else
  echo "  not set - run:  .venv/bin/python scraper/blok_mail.py --setup"
fi

echo "== systemd units"
sudo cp deploy/systemd/blok-*.service deploy/systemd/blok-*.timer /etc/systemd/system/
sudo systemctl daemon-reload
touch scraper/refresh.log push-blok.log

if [ "${1:-}" = "--enable" ]; then
  sudo systemctl enable --now blok-scrape.timer blok-push.timer
  echo "  timers ON"
else
  echo "  timers installed but OFF. When the Mac jobs are unloaded:"
  echo "    sudo systemctl enable --now blok-scrape.timer blok-push.timer"
fi
systemctl list-timers 'blok-*' --all --no-pager || true
