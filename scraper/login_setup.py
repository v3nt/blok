#!/usr/bin/env python3
"""
Sign the SCRAPER's browser profile into ClassPass. Run this once.

    /usr/bin/python3 login_setup.py

Why this is needed even though you are signed in in Chrome: the scheduled
scrape does not use your everyday Chrome profile. It drives Chrome with its
own profile directory (scraper/.chrome-profile) so it can never disturb,
log out, or be disturbed by the browser you are actually using. That profile
is a separate cookie jar, and it has never been signed in - so ClassPass
served it the signed-out page, where every class shows "See pricing" instead
of a booking control and the whole run is discarded.

A Chrome window opens on classpass.com/login. Sign in yourself (so 2FA,
captchas and the cookie banner are all yours to handle), then press Enter
here. The session is saved two ways:

  - in .chrome-profile, which every scheduled run uses
  - in auth_state.json, used by runs started with --no-profile

Both persist across reboots. You only need to redo this if ClassPass signs
the profile out.
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PROFILE = HERE / ".chrome-profile"
AUTH = HERE / "auth_state.json"
CHECK = "https://classpass.com/studios/blok-clapton-london"

SIGNED_OUT_JS = """() => {
  const cta = document.querySelector('.Schedule__rows section [data-qa="Schedule.cta"]');
  if (!cta) return 'no schedule rows on the page';
  const href = cta.getAttribute('href') || '';
  const text = (cta.innerText || '').trim();
  return /walkthrough/i.test(href) || /see pricing/i.test(text)
    ? 'SIGNED OUT (' + text + ' -> ' + href + ')' : '';
}"""

def main():
    PROFILE.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        try:
            ctx = p.chromium.launch_persistent_context(
                str(PROFILE), channel="chrome", headless=False,
                viewport={"width": 1440, "height": 1000},
                args=["--disable-blink-features=AutomationControlled"])
        except Exception as e:
            print("Chrome would not start (%s); using bundled Chromium" % e)
            ctx = p.chromium.launch_persistent_context(
                str(PROFILE), headless=False,
                viewport={"width": 1440, "height": 1000})
        try:
            page = ctx.new_page()
            page.goto("https://classpass.com/login", timeout=60000)
            input("\nSign in to ClassPass in the window that just opened.\n"
                  "When you can see your account, come back here and press Enter...\n")

            # Verify against a studio page, not the nav: the schedule CTA is
            # exactly what the scrape reads, so this proves the fix.
            page.goto(CHECK, timeout=60000)
            page.wait_for_timeout(4000)
            try:
                page.wait_for_selector(".Schedule__rows section", timeout=25000)
            except Exception:
                pass
            verdict = page.evaluate(SIGNED_OUT_JS)
            ctx.storage_state(path=str(AUTH))
            if verdict:
                print("\nStill not signed in for the schedule: %s" % verdict)
                print("Nothing lost - just run this again and complete the login.")
                return 1
            print("\nSigned in. The schedule shows real booking controls.")
            print("Saved: %s and the profile at %s" % (AUTH.name, PROFILE.name))
            print("The next scheduled run (00:05/04:05/08:05/12:05/16:05/20:05)"
                  " will publish on its own.")
            return 0
        finally:
            try:
                ctx.close()
            except Exception:
                pass

if __name__ == "__main__":
    sys.exit(main())
