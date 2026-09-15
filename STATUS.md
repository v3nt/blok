# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-15 20:05:05 refresh exit 3` |
| index.html modified | 2026-09-15 08:08:38 BST |
| Classes in index.html | 1989 |

## Last scrape failure

```
            /usr/bin/python3 -m playwright install chromium
----- 2026-09-15 14:05:05 refresh exit 3
----- 2026-09-15 16:05:03 refresh start (python: none with playwright)
FATAL: no python3 with playwright. Tried BLOK_PYTHON, PATH, /usr/bin,
       /opt/homebrew/bin, /usr/local/bin.
       fix: /usr/bin/python3 -m pip install playwright && \
            /usr/bin/python3 -m playwright install chromium
----- 2026-09-15 16:05:03 refresh exit 3
----- 2026-09-15 18:05:05 refresh start (python: none with playwright)
FATAL: no python3 with playwright. Tried BLOK_PYTHON, PATH, /usr/bin,
       /opt/homebrew/bin, /usr/local/bin.
       fix: /usr/bin/python3 -m pip install playwright && \
            /usr/bin/python3 -m playwright install chromium
----- 2026-09-15 18:05:05 refresh exit 3
----- 2026-09-15 20:05:05 refresh start (python: none with playwright)
FATAL: no python3 with playwright. Tried BLOK_PYTHON, PATH, /usr/bin,
       /opt/homebrew/bin, /usr/local/bin.
       fix: /usr/bin/python3 -m pip install playwright && \
            /usr/bin/python3 -m playwright install chromium
----- 2026-09-15 20:05:05 refresh exit 3
```

## Recent push errors

```
2026-09-15 19:54:33  BLOCKED: You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild -license' from within a Terminal window to review and agree to the Xcode and Apple SDKs license.
2026-09-15 20:04:34  BLOCKED: You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild -license' from within a Terminal window to review and agree to the Xcode and Apple SDKs license.
2026-09-15 20:14:36  BLOCKED: You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild -license' from within a Terminal window to review and agree to the Xcode and Apple SDKs license.
```
