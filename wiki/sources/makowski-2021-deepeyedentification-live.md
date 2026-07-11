---
type: source
tags: [paper, eye-movement-biometrics, deep-learning, presentation-attack, binocular]
aliases: [Makowski et al. 2021, DeepEyedentificationLive, DEL]
sources: [makowski-2021-deepeyedentification-live]
reviewed: false
updated: 2026-07-11
---

Makowski, Prasse, Reich, Krakowczyk, Jäger, Scheffer (Potsdam) —
*DeepEyedentificationLive: Oculomotoric Biometric Identification and
Presentation-Attack Detection Using Deep Neural Networks*, **IEEE T-BIOM 2021**
— bibliography **[34]**. Extends [[jager-2019-deep-eyedentification|Deep
Eyedentification]] to **binocular** signals plus **presentation-attack
detection** — a route-(b) ceiling with a liveness component.
(`raw/DeepEyedentificationLive...-2021.pdf`)

## Key facts

- Deep CNN on **both eyes'** micro- + saccadic macro-movements for identity
  verification; substantially lower error than prior work.
- **Presentation-attack / replay detection:** movements are modeled as a
  *response to a controlled, randomized stimulus*, so replays are detectable
  from the stimulus–response coupling — a liveness idea relevant to any
  deployed EMB defense.
- New dataset: **150 participants, 4 sessions each**; studies how training
  population size, data volume, stimulus type, number of enrollment sessions,
  and **enrollment–probe interval** affect performance — the cross-session
  axes GazePry's [[conditions-matrix]] mirrors.
- DEL's ~10% EER (5 s, cross-round) is one of the benchmarks
  [[lohr-2022-eye-know-you-too|EKYT]] compares against.

## Related

- [[eye-movement-biometrics]] — route (b) ceiling with liveness.
- [[jager-2019-deep-eyedentification]] — the monocular predecessor.
- [[lohr-2022-eye-know-you-too]] — the successor SOTA.
- [[conditions-matrix]] — shares the enroll-interval / population-size axes.

## Mentions in sources

- Plan §12 (route b, micro-movement + PAD), §18.1 [34]; protocol §7, §15.1.
