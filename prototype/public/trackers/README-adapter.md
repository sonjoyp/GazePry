# GazePry tracker adapters

Each webcam gaze tracker is a small self-registering adapter in this folder. The
orchestrator (`../gazepry-tracker.js`) is tracker-agnostic: it handles identity,
the calibration overlay, capture, the watchdog, and submission, and drives
whichever adapter matches `GazePry.identity.tracker`. This is what lets the same
participant be recorded with several trackers and compared (study protocol RQ3).

## Load order

On every page: `gazepry-tracker.js` first, then the adapter files, then the page
logic (`task-runner.js` on task pages). Adapters call `GazePry.registerTracker`
at load; the orchestrator lazily `load()`s only the *selected* tracker's heavy
library, so listing all adapters on a page is cheap.

## The contract

```js
GazePry.registerTracker({
  id: "webgazer-3.5.3",   // full id, stored verbatim in session.tracker
  family: "webgazer",     // stable slug: UI value, filename part, gallery grouping
  label: "WebGazer 3.5.3",
  hint: "one-line description shown in the picker",
  privacy: "local",       // "local" (video stays in browser) | "cloud" (frames uploaded)
  needsCalibration: true, // true -> orchestrator shows the 9-point click grid
  available: true,        // false -> greyed in the picker; `setup` explains how to enable
  setup: "how to vendor/enable (only when available:false)",
  startTimeoutMs: 9000,   // outer safety timeout for start()
  noDataHint: "shown if the watchdog sees zero frames",

  async load(base) {},    // inject the library; `base` = public/ dir URL. Idempotent.
  async start() {},       // boot engine + camera; resolve when live (self-calibrating
                          //   trackers run their own calibration here). May race a timeout.
  onGaze(cb) {},          // register per-frame cb(sample|null, clockMs);
                          //   sample = { x, y } in VIEWPORT PIXELS (WebGazer contract);
                          //   null = blink / lost face / no valid gaze this frame
  offGaze() {},           // clear the listener
  recordCalibration(x, y) {}, // feed one calibration click (viewport px); no-op if none
  clearModel() {},        // reset the model/personalisation (fresh session + wipe demo)
  showPreview(show) {},   // optional camera/overlay preview toggle
  pause() {}, resume() {},// optional; enables the watchdog to restart a dead loop
});
```

Only `family`, `start`, and `onGaze` are strictly required; the rest are optional
and default sensibly. Coordinates **must** be viewport pixels so one feature
extractor (`../../reid-core.js` / `analysis/features.py`) serves every tracker.

## Registered adapters

| family | status | privacy | calibration | notes |
|---|---|---|---|---|
| `webgazer` | working (vendored) | local | click grid | v3.5.3, the deployed reality |
| `gazecloud` | working (remote script) | **cloud** | self (built-in) | high accuracy; frames leave the machine |
| `webeyetrack` | needs vendoring | local | few-shot (click grid) | head-pose-aware; protocol arm 3 |
| `eyegestures` | needs vendoring | local | moving-dot (click grid) | open-source Rust/WASM |

To add a tracker: copy the closest adapter, implement the contract, drop its
library under `../lib/<name>/`, add one `<script>` line to `_trackers.html`, and
it appears in the picker automatically.
