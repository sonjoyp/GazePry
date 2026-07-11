---
type: concept
tags: [eye-tracking, webcam, foundations]
aliases: [Gaze Estimation, Webcam Eye Tracking, Point-of-Gaze]
sources: [information-leakage-report, prototype-code]
reviewed: false
updated: 2026-07-10
---

**Gaze estimation** here means software that estimates where a person is looking
using only the ordinary RGB camera built into a laptop, phone, or tablet — no IR
eye tracker, headset, or external hardware. It is the channel every GazePry
attack runs over.

## Key facts

- Reference implementations: [[webgazer]] (and its [[searchgazer]] derivative),
  the head-pose-aware [[webeyetrack]] — all run entirely in the browser.
- Output the project uses: a per-frame stream `{t, x, y}` in viewport pixels,
  with `x=null` marking a blink / lost-face gap.
- Accuracy is the honest weak link on commodity webcams (WebGazer drifts ≈5→10
  cm over 20 min); the [[gaze-feature-extraction|content-independent features]]
  are chosen to survive that degradation and low (~30 Hz) frame rates.
- Contrast with the research-grade IR ceiling ([[gazepoint]]) in
  [[ceiling-vs-commodity]].

## Related

- [[webgazer]], [[webeyetrack]], [[gazepoint]] — the estimators.
- [[gaze-feature-extraction]] — what the raw stream is turned into.
- [[eye-movement-biometrics]] — what the dynamics reveal.

## Mentions in sources

- Report §2 (Scope and Definitions); `prototype/reid-core.js` (input format).
