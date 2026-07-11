---
type: concept
tags: [biometrics, oculomotor, foundations]
aliases: [Eye-Movement Biometrics, Oculomotor Biometrics, Main Sequence, Scanpath Biometrics]
sources: [information-leakage-report, reid-research-plan, prototype-code]
reviewed: false
updated: 2026-07-11
---

**Eye-movement biometrics** is the mature research field establishing that
oculomotor *dynamics* — fixation durations, saccade amplitudes/velocities, the
"main sequence," blinks, microsaccades — re-identify individuals. It is the
signal GazePry weaponizes as a [[person-bound-fingerprint]]; the project's job
is to show it survives the commodity webcam channel, not to prove the signal
exists.

## Key facts

- Research-grade ceiling: **Eye Know You Too** reaches EER ≈0.58% on a reading
  task **with a 60 s window, rising to ≈3.66% at 5 s** [20] — always state the
  window (plan §21); cite the published IEEE TIFS 2022 version, not the arXiv
  preprint. George & Routray score-level fusion: **EER ≈2.59%** on the BioEye
  2015 random-stimulus task [31] — an earlier "≈5.8% at 320 subjects"
  attribution failed verification and was withdrawn (plan §21). Deep
  micro-movement ID: Deep Eyedentification [33], DeepEyedentificationLive [34].
- These are **IR-hardware, cooperative-enrollment upper bounds**, not the
  webcam threat — cite as "the signal is real and individual," then show the
  commodity gap ([[ceiling-vs-commodity]]).
- Task-independence is the weak spot the plan exploits: Kinnunen et al. [32] is
  the canonical task-independent authentication attempt (honest failure modes:
  small pool, high error) — the anchor for [[cross-task-generalization]].
- Two modeling routes (plan §12): (a) hand-crafted features + classifier
  (the harness's [[gaze-feature-extraction|16-feature]] route, robust at small
  N; interpretable score-fusion lineage [31]); (b) end-to-end deep model
  (Eye Know You Too-style [20]; micro-movement models [33], [34]) — the
  ceiling, trained on public data.
- The "main-sequence" peak-velocity-vs-amplitude relationship is highly
  individual and appears as `main_seq_slope` in the feature set.

## Related

- [[gaze-feature-extraction]] — route (a), as implemented.
- [[ceiling-vs-commodity]] — the IR-vs-webcam gap this ceiling defines.
- [[gazebase]] — public data for the deep/ceiling model.
- [[related-work-direction-1]] — the full biometrics lineage [30]–[37].

## Mentions in sources

- Report §3.2, §6 [20]; plan §3.2, §12 (features/models), §18.1–§18.2, §21
  (verification notes); `reid-core.js` (FEATURE_NAMES, main_seq_slope).
