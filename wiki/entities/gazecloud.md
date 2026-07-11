---
type: entity
subtype: system
tags: [eye-tracking, webcam, cloud, closed-source]
aliases: [GazeCloud, GazeRecorder, GazeCloud/GazeRecorder, gazecloud.js]
sources: [reid-research-plan, readme]
reviewed: false
updated: 2026-07-11
---

**GazeCloud / GazeRecorder** is a closed-source, hosted JavaScript gaze-tracking
API — the harness's **cloud contrast arm**. It is the high-accuracy,
self-calibrating drop-in option, but it **uploads webcam frames to
GazeRecorder's servers**. The plan includes it both as an accuracy contrast and
as a finding in its own right: for a paper about webcam gaze as a tracking
vector, *the most accurate drop-in option is also the one that exfiltrates the
face* (plan §9).

## Key facts

- Adapter `public/trackers/gazecloud.js`, family **`gazecloud`**; loads the
  hosted script (needs internet); calibration built-in (self-calibrating).
- Privacy class **cloud** — the only arm where camera data leaves the machine;
  results are reported **separately** from the on-device arms (plan §9, §15;
  README trackers table).
- Consent caveat (README): only use with participant consent covering
  third-party processing.
- Registry tests assert its capability flags: `cloud` + self-calibrating
  (`test/registry.test.js`).
- Related commercial option set aside: RealEye.io (SaaS study platform, not a
  drop-in library, also cloud) — plan §9.

## Related

- [[webgazer]], [[webeyetrack]], [[eyegestures]] — the on-device arms it is
  contrasted with.
- [[enabling-conditions]] — the camera-consent gap this arm illustrates
  concretely (a consented camera feed silently leaving the machine).
- [[ceiling-vs-commodity]] — the RQ3 comparison it joins as the cloud point.

## Mentions in sources

- `GazePry_ReID_Research_Plan.md` §6 (contribution 2), §9 (arm 5), §13, §15;
  `README.md` (Webcam trackers table, Caveats); `public/trackers/README-adapter.md`.
