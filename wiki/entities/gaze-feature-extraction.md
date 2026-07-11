---
type: entity
subtype: system
tags: [features, biometrics, oculomotor]
aliases: [Gaze Feature Extraction, reid-core.js, Feature Vector, Content-Independent Features]
sources: [prototype-code, direction-1-study-protocol]
reviewed: false
updated: 2026-07-10
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
- Matching (in `identify`): column-wise standardize, Euclidean distance,
  nearest gallery session per participant, rank ascending by distance.
- Excludes raw face/appearance by design, so the
  [[survives-de-identification]] claim stays clean.

## Related

- [[analysis-pipeline]] — `features.py` is the Python twin.
- [[reid-server]] — calls this for live `/identify`.
- [[eye-movement-biometrics]] — the feature family's research lineage.

## Mentions in sources

- `prototype/reid-core.js`; `prototype/analysis/features.py`; Protocol §7
  (features and models).
