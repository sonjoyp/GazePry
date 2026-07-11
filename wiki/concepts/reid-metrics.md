---
type: concept
tags: [evaluation, metrics, methodology]
aliases: [Re-ID Metrics, Metrics, rank-1, rank-5, EER, CMC, ROC]
sources: [direction-1-study-protocol, prototype-code]
reviewed: false
updated: 2026-07-10
---

The metrics used to quantify [[gaze-re-identification|re-ID]] performance,
split into identification and verification.

## Key facts

- **Identification:** rank-1 / rank-5 accuracy; **CMC** curve (identification
  rate vs rank k).
- **Verification:** **EER** (equal error rate); ROC / AUC. In `reid.py` EER is
  computed by sweeping thresholds on genuine/impostor *distances* (smaller
  distance = more similar) and taking the point where FAR and FRR are closest.
- **Two headline curves** (Protocol §9): accuracy vs **observation window**
  ("how many seconds of viewing links you") and accuracy vs **gallery size**
  (how the threat scales to a large tracked population).
- **Baselines:** chance; a conventional canvas/UA fingerprint as the
  *clearable* comparison (gaze persists where those reset — see
  [[unclearability]]).
- Report confidence intervals over subject splits, not a single split.

## Related

- [[reid-protocols]] — the protocols these metrics are computed under.
- [[conditions-matrix]] — observation-window and gallery-size are matrix axes.
- [[ceiling-vs-commodity]] — metrics compared across tracker arms.

## Mentions in sources

- Protocol §9 (Metrics), §10 (Analysis plan); `prototype/analysis/reid.py`
  (compute_eer, cmc_curve).
