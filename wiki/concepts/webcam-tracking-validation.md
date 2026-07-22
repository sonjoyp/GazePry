---
type: concept
tags: [webcam-eye-tracking, validation, accuracy, methodology]
aliases: [Webcam Tracking Validation, Accuracy Objection, Webcam vs Lab, Online Eye-Tracking Validation]
sources: [reid-research-plan]
reviewed: false
updated: 2026-07-11
---

**The accuracy objection is weakening.** A recurring reviewer objection to a
desktop webcam gaze-tracking threat is "webcam gaze is too imprecise to
matter." A decade of cognitive-science validation studies of [[webgazer]] and
newer systems is the standing rebuttal GazePry leans on (plan §5): webcam gaze
has moved from "rough" toward "close to laboratory standards," and it keeps
improving. None of these papers is in the plan's §21 canonical bibliography —
cite them **author-year** as supporting context, not by bracket number.

## Key facts

- **Semmelmann & Weigelt 2018** ([[semmelmann-2018-online-webcam-et]]) — the
  "first look": WebGazer online fixation offset ≈207 px (≈18% of screen,
  ≈3.9°) vs ≈172 px in-lab; replicates free-viewing gaze patterns. Usable but
  noisy — the early, honest baseline.
- **Yang & Krajbich 2021** ([[yang-2021-webcam-behavioral]]) — WebGazer wired
  into jsPsych; **temporal resolution improved from 100–1000 ms to 20–30 ms**;
  replicates gaze–choice effects. The ~30 Hz ceiling GazePry's sampling-rate
  caveat assumes.
- **Van der Cruyssen et al. 2024** ([[van-der-cruyssen-2024-validation]]) —
  replicates three classic effects with WebGazer.js; effect sizes shrink
  20–27%; verdict: fine for ≤4 large AOIs. Bounds what content-*dependent* AOI
  reading can expect. One of the three is the **novelty preference** (n = 45),
  i.e. the [[eye-movement-memory-effect]] itself — so this paper is not only a
  general accuracy datum but the **direct feasibility evidence** for
  [[recognition-knowledge-leakage]] (D7), along with its working stimulus
  geometry (472 × 331 px images, 295 px apart).
- **Kaduk et al. 2024** ([[kaduk-2024-webcam-vs-eyelink]]) — the strongest
  point: a webcam system (Labvanced) **simultaneously** vs EyeLink 1000 hits
  **1.4° accuracy / 1.1° precision**, only ≈0.5° worse, ~90% raw-sample
  correlation. "Close to laboratory standards."
- Trajectory continues with [[webeyetrack]] (≈2.32 cm, head-pose aware) — so
  the objection erodes *over time*, which is why the plan frames webcam re-ID
  numbers as a **lower bound** ([[ceiling-vs-commodity]]).

## Related

- [[webgazer]] — the tracker all four studies validate.
- [[ceiling-vs-commodity]] — why even a degraded webcam channel is a threat.
- [[gaze-estimation]] — the capability class being validated.
- [[recognition-knowledge-leakage]] — D7 depends on this literature twice over:
  for the coarse-AOI bound, and because one validated effect *is* its attack
  signal.
- Caveat: these validate *pointing accuracy*; GazePry's re-ID threat is
  content-*independent* and does not need pointing precision, so this is a
  floor, not the mechanism. D7 sits in between — it needs coarse pointing (which
  tile) plus **fixation timing**, and the timing half is what
  [[thilderkvist-2024-limitations]]'s I-DT contribution addresses.

## Mentions in sources

- Plan §5 (accuracy objection weakening; WebGazer drift vs WebEyeTrack);
  report §5.1.
