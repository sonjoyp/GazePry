---
type: entity
subtype: system
tags: [features, biometrics, oculomotor]
aliases: [Gaze Feature Extraction, reid-core.js, Feature Vector, Content-Independent Features]
sources: [prototype-code, direction-1-study-protocol]
reviewed: false
updated: 2026-07-13
---

The **content-independent gaze feature set** — the 16-dimensional vector that
turns a raw `{t, x, y}` stream into a [[person-bound-fingerprint]]. Defined once
and implemented twice: `reid-core.js` (JS, for the live demo) and `features.py`
(Python, the authoritative eval). The two **must stay in sync**.

## Key facts

- **16 features** (`FEATURE_NAMES`): fixation duration mean/median/std/p90;
  saccade amplitude mean/median/std/p90; saccade velocity mean/median/p90;
  fix_rate; sacc_rate; fix_ratio; gap_rate; **main_seq_slope** (the
  "main-sequence" peak-velocity-vs-amplitude relationship, highly individual).
- **I-VT segmentation:** `VEL_THRESHOLD = 2.0` screen-diagonal units/sec splits
  fixations from saccades; `MIN_FIX_MS = 80` discards sub-80 ms noise. The
  threshold is **coarse at ~30 Hz** and flagged for tuning against real data.
- Spatial features normalized by the **screen diagonal** → resolution/device
  independent.
- Gaps (`x=null`, blink/lost-face) segment runs and contribute `gap_rate`.
- **`resample(samples, hz)` (added 2026-07-12; `features.py` ↔ `reid-core.js`,
  parity-tested).** Equalizes capture cadence **before** feature extraction. This
  exists because trackers **log** at the browser `requestAnimationFrame` rate, not
  the true ~30 Hz camera rate, and that logged rate **varies by
  session/participant** (pilot: ~50 Hz P01 vs ~110 Hz P02) — so uncorrected,
  saccade-velocity / `main_seq_slope` features partly encode *logging cadence* and
  capture rate becomes a re-ID **confound correlated with identity**. Resampling to
  a common cadence + the rate-equalized control ([[reid-confound-controls]]) is the
  fix. See [[ceiling-vs-commodity]].
- Matching (in `identify`): column-wise standardize, Euclidean distance,
  nearest gallery session per participant, rank ascending by distance — i.e. a
  **diagonal-Mahalanobis nearest-neighbour** matcher. A learned metric
  (LDA / full-covariance Mahalanobis / score fusion) and richer distributional
  features are the **planned next step, deferred until N is large enough** to fit
  and validate them (at N=2 a learned metric overfits — the shuffle-null guards
  against it).
- Excludes raw face/appearance by design, so the
  [[survives-de-identification]] claim stays clean.

## Related

- [[analysis-pipeline]] — `features.py` is the Python twin; runs `resample` +
  the rate-equalized control.
- [[reid-server]] — calls this for live `/identify`.
- [[eye-movement-biometrics]] — the feature family's research lineage.
- [[reid-confound-controls]] — the rate-equalized negative control `resample`
  feeds; [[ceiling-vs-commodity]] — the logged-vs-true-rate caveat.

## Mentions in sources

- `reid-core.js` (`resample`, `FEATURE_NAMES`, `identify`);
  `analysis/features.py` (`resample`, `extract`); plan §9 (sampling-rate caveat)
  and §12 (route (a) features/models, deferred learned metric); Protocol §7.
