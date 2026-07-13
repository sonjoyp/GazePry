---
type: source
tags: [eye-movement-biometrics, visual-search, texture-features, template-aging, foundations]
aliases: [Li et al. 2018, texture features eye movement, GWT eye movement biometrics, visual searching task biometrics]
sources: [li-2018-texture-features]
reviewed: false
updated: 2026-07-13
---

Li, Xue, Quan, Yue & Zhang (Beijing Institute of Radiation Medicine) —
*Biometric recognition via texture features of eye movement trajectories in a
visual searching task*, **PLOS ONE 2018**. Ingested 2026-07-13; **added to the plan §21 as [53]** the same
day — cite **[53]**, *not* its `raw/related-papers.txt` index [67] (a different
numbering; see [[SCHEMA]]). Relevant to GazePry on two axes: a **visual-search stimulus**
(the closest analogue to the harness's SERP/search [[task-suite|task]]) and an
explicit **template-aging** analysis (short-term vs long-term sets), the
degradation that GazePry's ≥1-week [[unclearability]] cell must confront.
(`raw/Biometric recognition via texture features of eye movement trajectories in
a visual searching task-Li et al.-2018 1.pdf`)

## Key facts

- **Apparatus & cohort:** **Tobii TX300 at 300 Hz**, **58 subjects** (24 M, 34 F,
  ages 21–33), a novel **visual search task** (number-length comparison) chosen
  for stimulus complexity and stimulus-independence-in-spirit.
- **New feature class:** *texture features* of the eye-movement trajectory via a
  **Gabor Wavelet Transform (GWT)** — treats the scanpath as an image and extracts
  multi-scale/orientation texture, distinct from the fixation/saccade-statistic
  lineage of [[gaze-feature-extraction]].
- **Best result:** GWT reaches **EER ≈0.89%** on the short-term set (STset);
  chance Rank-1 = 1/58 ≈ 1.72%. Compares four methods (GWT, LVD, FDM, CEM);
  **score-level fusion** wins in most cases (the [[george-2016-score-fusion]]
  lineage).
- **Template aging is severe:** on the long-term set (LTset), EER inflates by
  **74%–1075% (relative)** across parameter settings and Rank-1 drops sharply —
  the paper's own warning that *time interval significantly degrades* eye-movement
  recognition. GazePry's headline cell is precisely long-interval cross-session,
  so this is a caution, not just support.
- Argues eye trackers need **≥250 Hz and ≤0.5° accuracy** for reliable biometrics
  (citing Holland & Komogortsev) — a bar the commodity webcam does not clear,
  reinforcing [[ceiling-vs-commodity]].

## Related

- [[eye-movement-biometrics]] — a texture/scanpath feature family alongside the
  fixation/saccade statistics.
- [[task-suite]] — the visual-search stimulus mirrors GazePry's SERP task "site."
- [[unclearability]] / [[cross-task-generalization]] — template aging is the
  cross-session degradation these claims must survive.
- [[george-2016-score-fusion]] — the score-level fusion Li et al. also find best.
- [[ceiling-vs-commodity]] — the ≥250 Hz / ≤0.5° requirement the webcam misses.

## Mentions in sources

- Plan **[53]**, cited in **§18.1** (biometrics foundations — scanpath texture,
  template aging, visual-search task). Added to §21 on 2026-07-13.
