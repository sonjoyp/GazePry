---
type: concept
tags: [methodology, rq3, evaluation]
aliases: [Ceiling vs Commodity, Ceiling vs. Commodity, RQ3, Hardware Gap]
sources: [direction-1-study-protocol, prototype-readme]
reviewed: false
updated: 2026-07-10
---

**Ceiling vs commodity** is the RQ3 measurement: the EER/rank-1 gap between
research-grade IR hardware ([[gazepoint]]) and the deployed webcam channel
([[webgazer]], [[webeyetrack]]) on the **same subjects and sessions**. It is the
direct payoff of running both devices at once via the
[[simultaneous-capture-rig]].

## Key facts

- Three tracker arms, best → realistic: [[gazepoint]] (60/150 Hz IR, the
  ceiling) → [[webeyetrack]] (≈2.32 cm, head-pose aware, near-future commodity
  ceiling) → [[webgazer]] (ridge regression, no head pose, deployed reality).
- **Sampling-rate caveat:** webcam ≈30 Hz vs Gazepoint 60–150 Hz; down-sample
  Gazepoint to the webcam rate for the *fair* arm, and report which
  saccade-velocity features survive 30 Hz.
- Analysis distinguishes channels by the `tracker` field; both feed the same
  [[gaze-feature-extraction|features.py]].
- **Honest framing:** even a degraded-but-non-random webcam EER is a publishable
  tracking threat when the comparison is "a cookie the user *can* clear." Treat
  webcam numbers as a lower bound.

## Related

- [[simultaneous-capture-rig]] — how the same-subject comparison is captured.
- [[gazepoint]], [[webgazer]], [[webeyetrack]] — the three arms.
- [[eye-movement-biometrics]] — the IR ceiling literature.
- [[reid-metrics]] — the EER/rank-1 measured across arms.

## Mentions in sources

- Protocol §1 (contribution 2), §3 (RQ3), §4 (apparatus), §10 (analysis plan);
  `prototype/README.md` (Gazepoint rig).
