---
type: entity
subtype: tool
tags: [eye-tracking, webcam, browser]
aliases: [WebGazer, brownhci/WebGazer, WebGazer v3.5.3]
sources: [information-leakage-report, reid-research-plan, readme, prototype-code]
reviewed: false
updated: 2026-07-11
---

**WebGazer** is the commodity, in-browser webcam [[gaze-estimation]] library the
project builds on — ridge-regression gaze estimation with no head-pose
awareness, self-calibrating from ordinary cursor interaction. It is the
"deployed reality" tracker arm (plan §9 arm 2) and the
[[searchgazer|SearchGazer]] lineage. The harness vendors the current **brownhci
build v3.5.3** (adapter `public/trackers/webgazer.js`, family `webgazer`,
9-point click grid, video stays in-browser).

## Key facts

- By the Brown HCI Group (webgazer.cs.brown.edu). Uses [[covert-calibration]]:
  correlates mouse clicks with gaze to build a model without an explicit
  calibration step [4].
- **Accuracy limitation:** point-of-gaze error rises from ≈5 cm to ≈10 cm over
  a 20-minute session; no head-pose model [7], [25]. This is the "honest risk"
  the prototype flags — treat webcam re-ID numbers as a *lower bound*.
- [[webeyetrack|WebEyeTrack]] closes much of this gap (≈2.32 cm, head-pose
  aware) and is the near-future commodity ceiling.
- In the harness its adapter is driven by the [[gazepry-tracker]] orchestrator
  and streams `{t, x, y}`; its bundled MediaPipe FaceMesh assets are vendored
  under `public/mediapipe/` (resolved relative to the script URL).
- **Do not** use the stale 2016 [[searchgazer]] fork — its SERP DOM selectors
  are dead; the archived demo lives in `legacy-searchgazer/`.

## Related

- [[gazepoint]], [[webeyetrack]], [[eyegestures]], [[gazecloud]] — the other
  tracker arms in [[ceiling-vs-commodity]].
- [[covert-calibration]] — the self-calibration mechanism it enables.
- [[searchgazer]] — the 2016 ancestor.

## Mentions in sources

- Report §5.1, §6 (accuracy drift [7], [25]); plan §5, §9 (arm 2), §15;
  `README.md` (Webcam trackers); `public/trackers/webgazer.js`.
