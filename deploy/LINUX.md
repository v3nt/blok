# Running the BLOK pipeline on the home server

Same two jobs as the Mac, as systemd timers on `nab9` (Ubuntu 24.04, user `server`):

| Mac (launchd) | Server (systemd) | When |
|---|---|---|
| `net.jynk.blokscrape` → `scraper/refresh.sh` | `blok-scrape.timer` → `blok-scrape.service` | every 2 h at :05 |
| `net.jynk.blokpush` → `push-blok.sh` | `blok-push.timer` → `blok-push.service` | every 10 min |

What differs from the Mac, and why:

- **Headed Chrome in a virtual display.** ClassPass serves an empty schedule to
  headless Chrome, so `blok-scrape.service` runs `refresh.sh` under `xvfb-run`.
- **Python is a venv** at `/srv/apps/blok/.venv` (playwright installed there). The
  units put it first on `PATH`, so `python3` in `push-blok.sh` is the venv too.
- **Gmail app password** lives in `~/.config/blok/gmail-app-password` (mode 600)
  instead of the Keychain. `blok_mail.py` checks `$BLOK_GMAIL_APP_PASSWORD`, then
  that file, then the Keychain, so the Mac keeps working unchanged.
- **Pushes use a deploy key** with write access to `v3nt/blok` only.

## Setup (once)

```bash
# 1. Deploy key (write access to this repo only)
ssh-keygen -t ed25519 -N '' -C 'nab9 blok' -f ~/.ssh/blok_deploy
cat ~/.ssh/blok_deploy.pub
#    GitHub → v3nt/blok → Settings → Deploy keys → Add → paste, tick "Allow write access"

# 2. Clone with that key
sudo mkdir -p /srv/apps && sudo chown server:server /srv/apps
GIT_SSH_COMMAND='ssh -i ~/.ssh/blok_deploy -o IdentitiesOnly=yes' \
  git clone git@github.com:v3nt/blok.git /srv/apps/blok
cd /srv/apps/blok
git config core.sshCommand 'ssh -i ~/.ssh/blok_deploy -o IdentitiesOnly=yes'

# 3. Install (timers stay OFF)
bash deploy/install-linux.sh

# 4. Gmail app password for your bookings
.venv/bin/python scraper/blok_mail.py --setup

# 5. Test runs by hand
xvfb-run -a bash scraper/refresh.sh && tail -20 scraper/refresh.log
bash push-blok.sh; tail -20 push-blok.log
```

## Cut over

Only one machine may push. On the **Mac**:

```bash
launchctl unload ~/Library/LaunchAgents/net.jynk.blok{scrape,push}.plist
```

Then on the **server**:

```bash
sudo systemctl enable --now blok-scrape.timer blok-push.timer
systemctl list-timers 'blok-*'
```

## Day to day

```bash
systemctl list-timers 'blok-*'               # next runs
tail -f /srv/apps/blok/scraper/refresh.log   # scrape detail
tail -f /srv/apps/blok/push-blok.log         # publish detail
sudo systemctl start blok-scrape.service     # scrape now
journalctl -u blok-scrape -u blok-push -n 50 # if a unit itself failed
```

`STATUS.md` on GitHub still carries the health summary.
