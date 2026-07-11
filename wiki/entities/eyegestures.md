---
type: entity
subtype: tool
tags: [eye-tracking, webcam, browser, open-source, on-device]
aliases: [EyeGestures, NativeSensors EyeGestures, eyegestures.js]
sources: [reid-research-plan, readme]
reviewed: false
updated: 2026-07-11
---

**EyeGestures** (NativeSensors) is an actively-maintained open-source webcam
gaze tracker whose web build the harness ships as its fourth tracker arm — the
"open-source second commodity arm" alongside [[webgazer]], [[webeyetrack]], and
the cloud contrast [[gazecloud]] (plan §9). Gaze inference runs **on-device**
in the browser (Rust/WASM engine), so no camera data leaves the machine.

## Key facts

- Adapter `public/trackers/eyegestures.js`, family **`eyegestures`**;
  self-calibrating (no click grid — it runs its own calibration in `start()`).
- Vendored by `scripts/vendor-trackers.sh` into `public/lib/eyegestures/`
  (WASM engine + shim + deps). Inference is local; MediaPipe assets are
  downloaded from CDNs at load (download-only).
- Expected RQ3 degradation ordering places it between the on-device extremes:
  WebEyeTrack → **EyeGestures** → WebGazer (plan §15).
- Registry tests assert it registers, meets the adapter contract, is `local`,
  and its vendored library is present on disk (`test/registry.test.js`).

## Related

- [[webgazer]], [[webeyetrack]], [[gazecloud]], [[gazepoint]] — the other
  tracker arms in [[ceiling-vs-commodity]].
- [[capture-harness]] — the tracker picker that selects it per session.
- [[gazepry-tracker]] — the tracker-agnostic orchestrator that drives it.

## Mentions in sources

- `GazePry_ReID_Research_Plan.md` §6 (contribution 2), §9 (arm 4), §15;
  `README.md` (Webcam trackers table, Credit); `public/trackers/README-adapter.md`.
