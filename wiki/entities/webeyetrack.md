---
type: entity
subtype: tool
tags: [eye-tracking, webcam, browser, head-pose]
aliases: [WebEyeTrack, WebEyeTrack [25]]
sources: [information-leakage-report, direction-1-study-protocol]
reviewed: false
updated: 2026-07-10
---

**WebEyeTrack** [25] is a recent head-pose-aware, in-browser gaze tracker that
calibrates from as few as nine samples and runs on-device. It is the project's
**near-future commodity ceiling** tracker arm — the evidence that the accuracy
objection to desktop in-browser attacks is weakening over time.

## Key facts

- ≈2.32 cm point-of-gaze error (GazeCapture); roughly **2× more accurate** than
  [[webgazer]]; real-time on an iPhone [25].
- Head-pose-aware with few-shot personalization — closes much of WebGazer's
  drift/head-motion gap.
- One of the three [[ceiling-vs-commodity]] tracker arms (Gazepoint ceiling →
  WebEyeTrack → WebGazer).
- Reference: Davalos et al., *WebEyeTrack: Scalable Eye-Tracking for the Browser
  via On-Device Few-Shot Personalization*, arXiv:2508.19544, 2025 [25].

## Related

- [[webgazer]] — the tracker it improves on.
- [[gazepoint]] — the IR ceiling it is measured against.
- [[ceiling-vs-commodity]] — the RQ3 comparison.

## Mentions in sources

- Report §5.1, §6 [25]; Protocol §4 (tracker arms), §16 [25].
