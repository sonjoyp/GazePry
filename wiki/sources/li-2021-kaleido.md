---
type: source
tags: [paper, defense, differential-privacy, real-time, system]
aliases: [Li et al. 2021, Kaleido, Kalεido, Real-Time Privacy Control Eye-Tracking]
sources: [li-2021-kaleido]
reviewed: false
updated: 2026-07-11
---

Li, Roy Chowdhury, Fawaz, Kim (Wisconsin–Madison) — *Kalεido: Real-Time
Privacy Control for Eye-Tracking Systems*, **USENIX Security 2021** —
bibliography **[48]**. A real-time **gaze differential-privacy system** with
formal guarantees — the deployment-shaped defense to benchmark GazePry's
in-browser perturbation layer against. (`raw/Kalεido...-2021.pdf`)

## Key facts

- Provides **real-time**, formally-guaranteed DP over the gaze stream between
  the eye-tracking platform and applications — a *system*, not just a feature
  transform (contrast [[steil-2019-gaze-dp]]).
- The closest architectural template for GazePry's proposed client-side
  perturbation layer (perturb the stream before it leaves
  [[gazepry-tracker|the tag]]) — same "sit between capture and consumer"
  position, but here in-browser and re-ID-targeted.

## Related

- [[gaze-perturbation-defense]] — RQ5 benchmark system.
- [[steil-2019-gaze-dp]] — the feature-level DP foundation it operationalizes.
- [[gazepry-tracker]] — where GazePry's version would live.

## Mentions in sources

- Plan §16 (real-time gaze-DP system to benchmark against), §18.6 [48];
  protocol §11, §15.6 [48].
