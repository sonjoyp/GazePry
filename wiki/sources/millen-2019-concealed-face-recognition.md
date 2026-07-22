---
type: source
tags: [paper, concealed-information-test, countermeasures, auc, d7, peer-reviewed]
aliases: [Millen and Hancock 2019, Eye see through you, concealed face recognition despite countermeasures]
sources: [d7-recognition-knowledge-direction]
reviewed: false
updated: 2026-07-22
---

Millen & Hancock — *Eye see through you! Eye tracking unmasks concealed face
recognition despite countermeasures*, **Cognitive Research: Principles and
Implications 4, art. 23, 2019**, doi 10.1186/s41235-019-0169-0. Supplies the
[[ocular-concealed-information-test]]'s **AUC scale** and the
**temporal-vs-spatial feature split** that D7's RQ4 is built on. *Not in plan
§21 — cite author-year (doc-local [C3] in
[[d7-recognition-knowledge-direction]]).*

## Key facts

- **n = 48** (24 standard-guilty, 24 countermeasures), full-colour face photos
  595 × 420 px presented individually; four CIT blocks of 18 test images each
  (12 unfamiliar irrelevants, 3 probe-identity images to deny, 3 target-identity
  images to endorse).
- **AUCs — standard guilty:** mean fixation duration 0.67, first fixation 0.69,
  proportion of fixations to eyes 0.87. **Countermeasures:** mean fixation
  duration 0.74, inner regions 0.80, areas visited 0.76.
- **The load-bearing result for D7:** a fixed-sequence countermeasure strategy
  destroyed the *spatial* signal (eye-fixation effect d = 1.40 → **−0.12**) but
  **fixation duration got stronger** (d = 0.66 → **0.91**) and was detectable
  from the **first fixation**. Temporal measures survive concealment; fine
  spatial measures do not.
- **Webcam caveat:** the strongest single AUC (0.87) came from *within-face* AOIs
  (eyes vs nose vs mouth). That granularity is **not available** on a commodity
  webcam ([[thilderkvist-2024-limitations]]), so D7 designs to whole-tile AOIs
  plus the temporal family and does not claim the 0.87 figure.

## Related

- [[ocular-concealed-information-test]] — the paradigm.
- [[schwedes-2012-revealing-glance]] — independently finds fixation duration to be
  the intent-independent measure.
- [[nahari-2019-concealed-familiarity]] — same journal and volume, adjacent DOI
  (0162-7 vs 0169-0); easily confused.
- [[recognition-knowledge-leakage]] — D7 RQ4/H4 predicts this temporal-survives
  pattern will reproduce on a webcam, and RQ5 predicts spatial-only defenses
  therefore fail.
- [[gaze-perturbation-defense]] — the reason a coarsening-only defense is
  suspected insufficient against D7.

## Mentions in sources

- `GazePry_D7_Recognition_Knowledge_Direction.md` §1, §3, §5 (RQ1, RQ4), §7.2,
  §8, §9.2 [C3], §10, §11 (correction note).

## Open questions

- **Correction recorded:** initially mis-attributed in session to *Scientific
  Reports*; it is *Cognitive Research: Principles and Implications* 4(23).
- Page built from PMC full text (PMC6684707), not the publisher PDF.
