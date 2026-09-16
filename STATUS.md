# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-16 04:12:36 refresh start (python: /usr/bin/python3)` |
| index.html modified | 2026-09-15 22:10:50 BST |
| Classes in index.html | 2010 |

## Last scrape failure

```
  - navigating to "https://classpass.com/profile/upcoming", waiting until "load"

----- 2026-09-16 02:30:43 refresh FAILED (exit 1)
----- 2026-09-16 04:12:36 refresh start (python: /usr/bin/python3)
BLOK refresh 2026-09-16 04:12:36
  browser: chrome, visible window
  ! Chrome would not start (BrowserType.launch_persistent_context: Timeout 180000ms exceeded.
Call log:
  - <launching> /Applications/Google Chrome.app/Contents/MacOS/Google Chrome --disable-field-trial-config --disable-background-networking --disable-background-timer-throttling --disable-backgrounding-occluded-windows --disable-back-forward-cache --disable-breakpad --disable-client-side-phishing-detection --disable-component-extensions-with-background-pages --disable-component-update --no-default-browser-check --disable-default-apps --disable-dev-shm-usage --disable-edgeupdater --disable-extensions --disable-features=AvoidUnnecessaryBeforeUnloadCheckSync,BoundaryEventDispatchTracksNodeRemoval,DestroyProfileOnBrowserClose,DialMediaRouteProvider,GlobalMediaControls,HttpsUpgrades,LensOverlay,MediaRouter,PaintHolding,ThirdPartyStoragePartitioning,Translate,AutoDeElevate,RenderDocument,OptimizationHints,msForceBrowserSignIn,msEdgeUpdateLaunchServicesPreferredVersion --enable-features=CDPScreenshotNewSurface --allow-pre-commit-input --disable-hang-monitor --disable-ipc-flooding-protection --disable-popup-blocking --disable-prompt-on-repost --disable-renderer-backgrounding --force-color-profile=srgb --metrics-recording-only --no-first-run --password-store=basic --use-mock-keychain --no-service-autorun --export-tagged-pdf --disable-search-engine-choice-screen --unsafely-disable-devtools-self-xss-warnings --edge-skip-compat-layer-relaunch --disable-infobars --disable-search-engine-choice-screen --disable-sync --enable-unsafe-swiftshader --no-sandbox --disable-blink-features=AutomationControlled --window-position=40,40 --window-size=1440,1000 --user-data-dir=/Users/danielcrabbe14/Sites/jynk/blok/scraper/.chrome-profile --remote-debugging-pipe about:blank
  - <launched> pid=82174
  - [pid=82174][err] Trying to load the allocator multiple times. This is *not* supported.
); using bundled Chromium
  loaded 53 saved cookie(s)
  ! Clapton failed: Page.goto: Timeout 60000ms exceeded.
Call log:
  - navigating to "https://classpass.com/studios/blok-clapton-london", waiting until "load"

  Shoreditch: consent banner - overlay removed x1
  Shoreditch -> 407 classes  [Wed, Sep 16:36 Thu, Sep 17:35 Fri, Sep 18:30 Sat, Sep 19:20 Sun, Sep 20:25 Mon, Sep 21:36 Tue, Sep 22:36 Wed, Sep 23:36 Thu, Sep 24:35 Fri, Sep 25:30 Sat, Sep 26:26 Sun, Sep 27:25 Mon, Sep 28:36 Tue, Sep 29:1]
  Mission E1: consent banner - overlay removed x1
```

## Recent push errors

```
2026-09-15 19:54:33  BLOCKED: You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild -license' from within a Terminal window to review and agree to the Xcode and Apple SDKs license.
2026-09-15 20:04:34  BLOCKED: You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild -license' from within a Terminal window to review and agree to the Xcode and Apple SDKs license.
2026-09-15 20:14:36  BLOCKED: You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild -license' from within a Terminal window to review and agree to the Xcode and Apple SDKs license.
```
