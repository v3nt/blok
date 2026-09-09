# BLOK pipeline status

Machine-written by `push-blok.sh`. Committed so it is readable from
GitHub (and therefore from a phone) without touching the Mac.

| Field | Value |
|---|---|
| Scrape result | **FAIL** |
| Last scrape log line | `----- 2026-09-09 00:44:23 refresh FAILED (exit 1)` |
| index.html modified | 2026-09-08 22:08:41 BST |
| Classes in index.html | 2001 |

## Last scrape failure

```
  File "/Users/danielcrabbe14/Sites/jynk/blok/scraper/refresh.py", line 593, in main
    browser, ctx = start(None)
  File "/Users/danielcrabbe14/Sites/jynk/blok/scraper/refresh.py", line 566, in start
    c = p.chromium.launch_persistent_context(
  File "/Users/danielcrabbe14/Library/Python/3.9/lib/python/site-packages/playwright/sync_api/_generated.py", line 16570, in launch_persistent_context
    self._sync(
  File "/Users/danielcrabbe14/Library/Python/3.9/lib/python/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
  File "/Users/danielcrabbe14/Library/Python/3.9/lib/python/site-packages/playwright/_impl/_browser_type.py", line 166, in launch_persistent_context
    result = await self._channel.send_return_as_dict(
  File "/Users/danielcrabbe14/Library/Python/3.9/lib/python/site-packages/playwright/_impl/_connection.py", line 83, in send_return_as_dict
    return await self._connection.wrap_api_call(
  File "/Users/danielcrabbe14/Library/Python/3.9/lib/python/site-packages/playwright/_impl/_connection.py", line 559, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.TimeoutError: BrowserType.launch_persistent_context: Timeout 180000ms exceeded.
Call log:
  - <launching> /Users/danielcrabbe14/Library/Caches/ms-playwright/chromium-1223/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing --disable-field-trial-config --disable-background-networking --disable-background-timer-throttling --disable-backgrounding-occluded-windows --disable-back-forward-cache --disable-breakpad --disable-client-side-phishing-detection --disable-component-extensions-with-background-pages --disable-component-update --no-default-browser-check --disable-default-apps --disable-dev-shm-usage --disable-edgeupdater --disable-extensions --disable-features=AvoidUnnecessaryBeforeUnloadCheckSync,BoundaryEventDispatchTracksNodeRemoval,DestroyProfileOnBrowserClose,DialMediaRouteProvider,GlobalMediaControls,HttpsUpgrades,LensOverlay,MediaRouter,PaintHolding,ThirdPartyStoragePartitioning,Translate,AutoDeElevate,RenderDocument,OptimizationHints,msForceBrowserSignIn,msEdgeUpdateLaunchServicesPreferredVersion --enable-features=CDPScreenshotNewSurface --allow-pre-commit-input --disable-hang-monitor --disable-ipc-flooding-protection --disable-popup-blocking --disable-prompt-on-repost --disable-renderer-backgrounding --force-color-profile=srgb --metrics-recording-only --no-first-run --password-store=basic --use-mock-keychain --no-service-autorun --export-tagged-pdf --disable-search-engine-choice-screen --unsafely-disable-devtools-self-xss-warnings --edge-skip-compat-layer-relaunch --disable-infobars --disable-search-engine-choice-screen --disable-sync --enable-unsafe-swiftshader --no-sandbox --disable-blink-features=AutomationControlled --window-position=40,40 --window-size=1440,1000 --user-data-dir=/Users/danielcrabbe14/Sites/jynk/blok/scraper/.chrome-profile --remote-debugging-pipe about:blank
  - <launched> pid=23072

----- 2026-09-09 00:44:23 refresh FAILED (exit 1)
```

