---
type: concept
tags: [methodology, rq3, evaluation]
aliases: [Ceiling vs Commodity, Ceiling vs. Commodity, RQ3, Hardware Gap]
sources: [reid-research-plan, readme]
reviewed: false
updated: 2026-07-11
---

**Ceiling vs commodity** is the RQ3 measurement: the EER/rank-1 gap between
research-grade IR hardware ([[gazepoint]]) and the commodity webcam channel
([[webgazer]], [[webeyetrack]], [[eyegestures]], with [[gazecloud]] as the
cloud contrast) on the **same subjects and sessions**. It is the direct payoff
of running both devices at once via the [[simultaneous-capture-rig]].

## Key facts

- Five tracker arms (plan §9). On-device, best → realistic: [[gazepoint]]
  (60/150 Hz IR, the ceiling) → [[webeyetrack]] (≈2.32 cm, head-pose aware,
  near-future commodity ceiling) → [[eyegestures]] (open-source second
  commodity arm) → [[webgazer]] (ridge regression, no head pose, deployed
  reality). The cloud arm [[gazecloud]] is reported **separately** — its
  accuracy is not comparable in privacy terms (frames leave the machine).
- The harness makes the comparison direct: adapters all emit the same
  `{t, x, y}` stream and `reid.py` reports **per tracker**, never matching
  across trackers — the per-tracker `cross_task_cross_session` EERs *are* the
  RQ3 gap.
- **No IR-label contamination (plan §9 critical control):** the webcam trackers
  are measured *as deployed* (native self-calibration); Gazepoint supplies an
  independent accuracy reference only and is **never** used to train or correct
  the webcam gaze. Otherwise the "gap" collapses artificially. See
  [[simultaneous-capture-rig]] and [[reid-confound-controls]].
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
- [[gazepoint]], [[webgazer]], [[webeyetrack]], [[eyegestures]], [[gazecloud]]
  — the five arms.
- [[eye-movement-biometrics]] — the IR ceiling literature.
- [[reid-metrics]] — the EER/rank-1 measured across arms.

## Mentions in sources

- Plan §6 (contribution 2), §8 (RQ3), §9 (apparatus + sampling-rate caveat),
  §15 (analysis plan); `README.md` (Gazepoint rig; Webcam trackers).
