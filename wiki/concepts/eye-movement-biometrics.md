---
type: concept
tags: [biometrics, oculomotor, foundations]
aliases: [Eye-Movement Biometrics, Oculomotor Biometrics, Main Sequence, Scanpath Biometrics]
sources: [information-leakage-report, direction-1-study-protocol, prototype-code]
reviewed: false
updated: 2026-07-10
---

**Eye-movement biometrics** is the mature research field establishing that
oculomotor *dynamics* — fixation durations, saccade amplitudes/velocities, the
"main sequence," blinks, microsaccades — re-identify individuals. It is the
signal GazePry weaponizes as a [[person-bound-fingerprint]]; the project's job
is to show it survives the commodity webcam channel, not to prove the signal
exists.

## Key facts

- Research-grade ceiling: **Eye Know You Too** reaches EER ≈ 0.6% on reading
  [20]; George & Routray EER ≈ 5.8% at 320 subjects [31]; deep micro-movement
  ID (Deep Eyedentification [33], DeepEyedentificationLive [34]).
- These are **IR-hardware, cooperative-enrollment upper bounds**, not the
  webcam threat — cite as "the signal is real and individual," then show the
  commodity gap ([[ceiling-vs-commodity]]).
- Two modeling routes (Protocol §7): (a) hand-crafted features + classifier
  (the prototype's [[gaze-feature-extraction|16-feature]] route, robust at small
  N); (b) end-to-end deep model (Eye Know You Too-style) — the ceiling.
- The "main-sequence" peak-velocity-vs-amplitude relationship is highly
  individual and appears as `main_seq_slope` in the feature set.

## Related

- [[gaze-feature-extraction]] — route (a), as implemented.
- [[ceiling-vs-commodity]] — the IR-vs-webcam gap this ceiling defines.
- [[gazebase]] — public data for the deep/ceiling model.
- [[related-work-direction-1]] — the full biometrics lineage [30]–[37].

## Mentions in sources

- Report §3.2, §6 [20]; Protocol §7 (features/models), §15.1;
  `prototype/reid-core.js` (FEATURE_NAMES, main_seq_slope).
