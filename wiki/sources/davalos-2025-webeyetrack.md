---
type: source
tags: [paper, webcam-eye-tracking, browser, head-pose, few-shot, preprint]
aliases: [WebEyeTrack paper, Davalos et al. 2025, WEBEYETRACK]
sources: [davalos-2025-webeyetrack]
reviewed: false
updated: 2026-07-11
---

Davalos et al. (Trinity / St. Mary's / Vanderbilt) — *WEBEYETRACK: Scalable
Eye-Tracking for the Browser via On-Device Few-Shot Personalization*, arXiv
2508.19544, Aug 2025 — bibliography **[25]** (**preprint-flagged** in plan
§21). The paper behind the [[webeyetrack]] tracker arm: a head-pose-aware,
in-browser CNN with few-shot on-device personalization — the "near-future
commodity ceiling." (`raw/WEBEYETRACK...-2025.pdf`)

## Key facts

- **Pipeline:** MediaPipe facial-landmark mesh → metric head pose (3-D face
  reconstruction + iris-diameter scaling + radial Procrustes) → **BlazeGaze**,
  a 670 KB / 0.16 M-param BlazeBlock CNN → 2-D point-of-gaze. Eye-aspect-ratio
  blink suppression; clickstream calibration; WebFixRT fixation detection.
- **Accuracy:** ≈**2.32 cm** PoG error on GazeCapture (Table 1; also 4.56 cm
  MPIIFaceGaze, 7.53 cm EyeDiap). Real-time — 0.88 ms delay / ~1137 FPS on an
  i7; the paper cites 2.4 ms on an iPhone 14.
- **The "≈2× WebGazer" / drift claim, sourced here and in [7]:** WebGazer's
  error rises **≈49% (7.79→11.62 cm)** over a 20-min session; WebEyeTrack rises
  only **≈20% (7.24→8.72 cm)**, significantly lower final error (p<0.05). The
  gap is WebGazer's lack of head-pose modeling and its reliance on click
  recalibration that fails during uninterrupted typing.
- **Few-shot:** MAML meta-learner adapts from **k ≤ 9** calibration samples;
  gaze normalized to device-agnostic [−0.5,0.5]².
- **On-device / privacy:** Python + TensorFlow.js (LayersModel) so training
  and inference run in-browser and *user data never leaves the device* — the
  same on-device stance GazePry argues does not stop identity leakage.
- Positions closed-source browser tools (RealEye, iMotions WebET,
  **GazeCloudAPI** = [[gazecloud]]) as opaque/unbenchmarked; open-source
  WebGazer as the ridge-regression incumbent it improves on.

## Related

- [[webeyetrack]] — the tool entity / tracker arm 3.
- [[webgazer]] — the incumbent it doubles in accuracy and out-drifts.
- [[gaze-estimation]] — the appearance-based-CNN branch it advances.
- [[ceiling-vs-commodity]] — it is the near-future commodity ceiling in RQ3.

## Mentions in sources

- Plan §2, §5 (≈2.32 cm, ≈2× WebGazer, drift), §9 (arm 3), §21 (preprint flag,
  re-check before submission); report §5.1, §6 [25].

## Open questions

- Preprint numbers are indicative (plan §21) — re-verify the 2.32 cm and drift
  figures against any published version before the paper quotes them.
