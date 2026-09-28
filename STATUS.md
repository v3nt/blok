# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-28 14:05:13 refresh FAILED (exit 1)` |
| index.html modified | 2026-09-28 15:14:28 BST |
| Classes in index.html | 1766 |

## Last scrape failure

```
  - <launching> /Users/danielcrabbe14/Library/Caches/ms-playwright/chromium-1223/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing --disable-field-trial-config --disable-background-networking --disable-background-timer-throttling --disable-backgrounding-occluded-windows --disable-back-forward-cache --disable-breakpad --disable-client-side-phishing-detection --disable-component-extensions-with-background-pages --disable-component-update --no-default-browser-check --disable-default-apps --disable-dev-shm-usage --disable-edgeupdater --disable-extensions --disable-features=AvoidUnnecessaryBeforeUnloadCheckSync,BoundaryEventDispatchTracksNodeRemoval,DestroyProfileOnBrowserClose,DialMediaRouteProvider,GlobalMediaControls,HttpsUpgrades,LensOverlay,MediaRouter,PaintHolding,ThirdPartyStoragePartitioning,Translate,AutoDeElevate,RenderDocument,OptimizationHints,msForceBrowserSignIn,msEdgeUpdateLaunchServicesPreferredVersion --enable-features=CDPScreenshotNewSurface --allow-pre-commit-input --disable-hang-monitor --disable-ipc-flooding-protection --disable-popup-blocking --disable-prompt-on-repost --disable-renderer-backgrounding --force-color-profile=srgb --metrics-recording-only --no-first-run --password-store=basic --use-mock-keychain --no-service-autorun --export-tagged-pdf --disable-search-engine-choice-screen --unsafely-disable-devtools-self-xss-warnings --edge-skip-compat-layer-relaunch --disable-infobars --disable-search-engine-choice-screen --disable-sync --enable-unsafe-swiftshader --no-sandbox --disable-blink-features=AutomationControlled --window-position=40,40 --window-size=1440,1000 --user-data-dir=/Users/danielcrabbe14/Sites/jynk/blok/scraper/.chrome-profile --remote-debugging-pipe about:blank
  - <launched> pid=18380
  - [pid=18380][out] Opening in existing browser session.
  - [pid=18380] <gracefully close start>
  - [pid=18380] <kill>
  - [pid=18380] <will force kill>
  - [pid=18380] exception while trying to kill process: Error: kill EPERM
  - [pid=18380] <process did exit: exitCode=0, signal=null>
  - [pid=18380] starting temporary directories cleanup
  - [pid=18380] finished temporary directories cleanup
  - [pid=18380] <gracefully close end>

Third Space refresh 2026-09-28 14:05:07
  Islington -> 703 class(es)
  Moorgate -> 477 class(es)
  City -> 429 class(es)
  descriptions: 45 of 48 class type(s)
  no blurb for: Dance Fit, Self, Yoga Workshop
  wrote /Users/danielcrabbe14/Sites/jynk/blok/3rdspace.html (215054 bytes, 1609 classes)
----- 2026-09-28 14:05:13 refresh FAILED (exit 1)
```

