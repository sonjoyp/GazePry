---
type: source
tags: [paper, eye-movement-biometrics, deep-learning, densenet, ceiling]
aliases: [Lohr and Komogortsev 2022, Eye Know You Too, EKYT, EKY2]
sources: [lohr-2022-eye-know-you-too]
reviewed: false
updated: 2026-07-11
---

Lohr & Komogortsev (Texas State) — *Eye Know You Too: Toward Viable End-to-End
Eye Movement Biometrics for User Authentication*, **IEEE TIFS 2022**
(arXiv:2201.02110) — bibliography **[20]**. The **research-grade ceiling** for
GazePry's route (b): a DenseNet on raw eye-tracking signal, the first EMB model
"acceptable for real-world use." Source of the headline window-dependent EER
the plan quotes everywhere. (`raw/Eye Know You Too...-2022.pdf`)

## Key facts

- **DenseNet** end-to-end on the raw gaze signal (metric-learning embeddings),
  evaluated on **GazeBase** (322 college-age subjects, TEX reading task).
- **The window-dependence claim (always state the window):** **EER ≈0.58%**
  when aggregating **5×12 s ≈ 60 s**, rising to **EER ≈3.66%** for a single
  **5 s** window (same enroll/probe rounds). This steep curve is exactly why
  GazePry's accuracy-vs-observation-window curve ([[reid-metrics]]) is expected
  to be informative.
- Beats prior SOTA: original Eye Know You 14.88% (60 s) / 18.75% (10 s);
  DeepEyedentificationLive ([[makowski-2021-deepeyedentification-live]]) ~10%;
  statistical Friedman et al. 2.01%.
- Studies test–retest interval (GazeBase rounds R2–R4), degraded sampling
  rates, and template aging — the same robustness axes GazePry's
  [[conditions-matrix]] varies.
- **Cite the published IEEE TIFS 2022 version**, not the arXiv preprint (plan
  §21). This is a *ceiling*, not the drive-by webcam threat — it defines what
  RQ3 ([[ceiling-vs-commodity]]) measures the commodity gap against.

## Related

- [[eye-movement-biometrics]] — route (b), the deep ceiling.
- [[gazebase]] — the dataset it is trained/evaluated on.
- [[ceiling-vs-commodity]] — the IR ceiling the webcam channel is compared to.
- [[reid-metrics]] — the observation-window curve this motivates.
- [[jager-2019-deep-eyedentification]], [[makowski-2021-deepeyedentification-live]]
  — the deep-EMB predecessors it surpasses.

## Mentions in sources

- Plan §3.2, §12 (route b ceiling), §14 (window-dependent EER), §18.1, §21
  (window caveat; cite published TIFS) [20]; report §3.2, §6 [20].
