---
type: source
tags: [paper, defense, streaming, gaze, spatial-privacy]
aliases: [David-John et al. 2021, privacy-preserving streaming eye-tracking data]
sources: [david-john-2021-streaming-privacy]
reviewed: false
updated: 2026-07-11
---

David-John, Hosfelt, Butler, Jain (University of Florida) — *A
privacy-preserving approach to streaming eye-tracking data*, **IEEE TVCG 2021**
— bibliography **[24]**. A **streaming** gaze-privacy method (perturb gaze as
it flows to the application) — part of the RQ5 defense landscape and a template
for real-time, low-latency perturbation. (`raw/A privacy-preserving approach to
streaming eye-tracking data...-2021.pdf`)

## Key facts

- Operates on the **streaming** gaze signal (event detection → spatial
  perturbation) so gaze utility for VR interactions (e.g. foveated rendering,
  redirected walking) survives while identity/attribute leakage is reduced.
- The "streaming-DP approach" the plan lists among perturbations to evaluate —
  closest to GazePry's need to perturb a live per-frame stream before submit.

## Related

- [[gaze-perturbation-defense]] — RQ5; the streaming-perturbation option.
- [[david-john-2022-for-your-eyes-only]] — the same group's re-ID-targeted
  dataset defense.
- [[wilson-2024-vr-gaze-streaming]] — a robustness/UX study of this streaming
  approach.

## Mentions in sources

- Plan §16 (streaming-DP), §18.6 [24]; report §7 [24]; protocol §11, §15.6 [24].
