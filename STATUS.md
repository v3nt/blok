# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-15 22:05:04 refresh start (python: /usr/bin/python3)` |
| index.html modified | 2026-09-15 08:08:38 BST |
| Classes in index.html | 1989 |

## Last scrape failure

```
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
----- 2026-09-15 22:05:04 refresh start (python: /usr/bin/python3)
BLOK refresh 2026-09-15 22:05:05
  browser: chrome, visible window
  loaded 53 saved cookie(s)
  Clapton: consent banner - overlay removed x1
  Clapton -> 1265 classes  [Tue, Sep 15:0 Wed, Sep 16:108 Thu, Sep 17:104 Fri, Sep 18:102 Sat, Sep 19:67 Sun, Sep 20:85 Mon, Sep 21:108 Tue, Sep 22:105 Wed, Sep 23:108 Thu, Sep 24:104 Fri, Sep 25:102 Sat, Sep 26:79 Sun, Sep 27:85 Mon, Sep 28:108]
  Shoreditch: consent banner - overlay removed x1
```

## Recent push errors

```
2026-09-15 19:54:33  BLOCKED: You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild -license' from within a Terminal window to review and agree to the Xcode and Apple SDKs license.
2026-09-15 20:04:34  BLOCKED: You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild -license' from within a Terminal window to review and agree to the Xcode and Apple SDKs license.
2026-09-15 20:14:36  BLOCKED: You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild -license' from within a Terminal window to review and agree to the Xcode and Apple SDKs license.
```
