---
type: entity
subtype: tool
tags: [eye-tracking, webcam, browser, head-pose]
aliases: [WebEyeTrack, WebEyeTrack [25]]
sources: [information-leakage-report, reid-research-plan, readme]
reviewed: false
updated: 2026-07-11
---

**WebEyeTrack** [25] is a recent head-pose-aware, in-browser gaze tracker that
calibrates from as few as nine samples and runs on-device. It is the project's
**near-future commodity ceiling** tracker arm (plan §9 arm 3) — the evidence
that the accuracy objection to desktop in-browser attacks is weakening over
time. The harness vendors it (RedForestAI, MIT license).

## Key facts

- ≈2.32 cm point-of-gaze error (GazeCapture); roughly **2× more accurate** than
  [[webgazer]]; real-time on an iPhone [25].
- Head-pose-aware CNN with few-shot personalization — closes much of WebGazer's
  drift/head-motion gap.
- In the harness: adapter `public/trackers/webeyetrack.js`, family
  `webeyetrack`; few-shot click-grid calibration; UMD bundle vendored by
  `scripts/vendor-trackers.sh` into `public/lib/webeyetrack/`; its BlazeGaze
  TF.js model is served at the origin root `public/web/` because the loader
  hardcodes `${origin}/web/model.json`. Inference on-device (model/WASM assets
  download from CDNs at load).
- One of the [[ceiling-vs-commodity]] arms; expected on-device ordering
  Gazepoint → **WebEyeTrack** → [[eyegestures]] → [[webgazer]] (plan §15).
- Under the hood ([[davalos-2025-webeyetrack]]): MediaPipe mesh → metric
  head pose → **BlazeGaze** (670 KB CNN); MAML few-shot; TF.js on-device.
  Drift over 20 min: ≈20% rise vs WebGazer's ≈49%.
- Reference: Davalos et al., *WebEyeTrack: Scalable Eye-Tracking for the Browser
  via On-Device Few-Shot Personalization*, arXiv:2508.19544, 2025 [25] —
  **preprint-flagged** in plan §21; re-check numbers against a published
  version before submission.

## Related

- [[webgazer]] — the tracker it improves on.
- [[gazepoint]] — the IR ceiling it is measured against.
- [[eyegestures]], [[gazecloud]] — the other commodity arms.
- [[ceiling-vs-commodity]] — the RQ3 comparison.

## Mentions in sources

- Report §5.1, §6 [25]; plan §5, §9 (arm 3), §15, §21; `README.md` (Webcam
  trackers); `public/trackers/webeyetrack.js`.
