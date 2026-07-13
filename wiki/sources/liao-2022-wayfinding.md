---
type: source
tags: [eye-movement-biometrics, stimulus-independent, real-world, mobile-eye-tracking, foundations]
aliases: [Liao et al. 2022, Wayfinding eye movement biometrics, stimulus-independent real-world biometrics, SMI ETG wayfinding]
sources: [liao-2022-wayfinding]
reviewed: false
updated: 2026-07-13
---

Liao, Zhao, Zhang & Dong (Hunan Normal + Beijing Normal) — *Exploring Eye
Movement Biometrics in Real-World Activities: A Case Study of Wayfinding*,
**Sensors 2022**. Ingested 2026-07-13; **added to the plan §21 as [51]** the same
day — cite **[51]**, *not* its `raw/related-papers.txt` index [63] (a different
numbering; see [[SCHEMA]]). The strongest external evidence for GazePry's core methodological bet:
**implicit, stimulus-independent** eye-movement recognition works **in the wild**,
not just on fixed lab stimuli — the real-world analogue of
[[cross-task-generalization]]. (`raw/Exploring Eye Movement Biometrics in
Real-World Activities A Case Study of Wayfinding-Liao et al.-2022.pdf`)

## Key facts

- **Apparatus & cohort:** **SMI Eye Tracking Glasses (ETG) at 60 Hz, binocular**,
  worn during **real-world outdoor pedestrian wayfinding** — a mobile,
  already-low-rate sensor (not a lab EyeLink), and no controlled stimulus.
- **Five feature sets:** basic statistical, pupillary response, fixation density,
  **fixation semantic**, and saccade encoding; classifier is a **random forest**.
- **Results (identification):** best **78% accuracy (EER 6.3%)** under 10-fold
  cross-validation, dropping to **64% (EER 12.1%)** under **leave-one-route-out** —
  the route-independent split is the direct analogue of GazePry's enroll-on-A /
  identify-on-B [[cross-task-generalization|cross-task]] test.
- **Results (verification):** best **89% accuracy (EER 9.1%)**; verification
  accuracy was **insensitive to time-window size** — a useful counterpoint to
  window-length dependence (cf. [[reid-metrics]] accuracy-vs-window curve).
- Framed as the **first** demonstration of implicit + stimulus-independent
  biometric recognition in real-world settings via wearable eye tracking.
- **Honest caveat the authors raise:** mobile trackers (Tobii Pro Glasses
  50–100 Hz, SMI ETG 60 Hz) run below the ≥250 Hz Holland–Komogortsev
  recommendation, so low rate limits the micro-characteristics available — the
  same constraint as [[ceiling-vs-commodity]], here at 60 Hz rather than 30 Hz.

## Related

- [[cross-task-generalization]] — leave-one-route-out is the real-world twin of
  the cross-task/cross-site split.
- [[eye-movement-biometrics]] — evidence the signal survives outside the lab.
- [[kinnunen-2010-task-independent]] — the earlier task-independence anchor; Liao
  extends it to real-world, higher-N, stimulus-free capture.
- [[ceiling-vs-commodity]] — 60 Hz mobile rate degrades micro-features, the same
  low-rate limit the webcam faces.

## Mentions in sources

- Plan **[51]**, cited in **§18.2** (stimulus-independent, real-world, alongside
  [[kinnunen-2010-task-independent]] [32] and [[eberz-2016-looks-like-eve]] [50])
  and **§18.8** (the gap). Added to §21 on 2026-07-13.
