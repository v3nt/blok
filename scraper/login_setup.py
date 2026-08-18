"""
Run this ONCE to log into ClassPass in a real (headed) browser window and
save the session so scrape.py can reuse it without logging in every time.

Usage:
    python login_setup.py

A Chromium window will open. Log into ClassPass manually (this lets you
handle 2FA / captchas / cookie banners yourself). Once you can see your
account (e.g. credits balance) in the top nav, come back to the terminal
and press Enter. Your session will be saved to auth_state.json.
"""
from playwright.sync_api import sync_playwright

OUTPUT = "auth_state.json"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://classpass.com/login")

        input(
            "\nLog into ClassPass in the opened browser window.\n"
            "Once logged in and you can see your account, press Enter here to save the session...\n"
        )

        context.storage_state(path=OUTPUT)
        print(f"Saved session to {OUTPUT}")
        browser.close()

if __name__ == "__main__":
    main()
