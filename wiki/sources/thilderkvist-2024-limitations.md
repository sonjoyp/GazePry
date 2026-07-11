---
type: source
tags: [paper, webcam-eye-tracking, limitations, code-reading, counterpoint]
aliases: [Thilderkvist and Dobslaw 2024, limitations of online eye-tracking source code]
sources: [thilderkvist-2024-limitations]
reviewed: false
updated: 2026-07-11
---

Thilderkvist & Dobslaw (Mid Sweden University) — *On current limitations of
online eye-tracking to study the visual processing of source code*,
**Information and Software Technology 2024**. The honest **counterpoint** to
[[webcam-tracking-validation]]: for fine-grained tasks, consumer webcam gaze is
still not good enough. *Not in plan §21 — cite author-year.*
(`raw/On current limitations of online eye-tracking...-2024.pdf`. A ScienceDirect
HTML mirror, `S0950584924001071.html`, was in `raw/` but deleted in commit
9185c26.)

## Key facts

- 40 participants, code-reading experiment, client-side ridge-regression
  tracker (WebGazer-style), no video saved.
- Introduced a **dispersion-threshold fixation algorithm** for low-frequency
  webcam data (there was none) — relevant to the harness's I-VT choice
  (`VEL_THRESHOLD`) and the plan's caveat that ~30 Hz coarsens fixation/saccade
  segmentation.
- **Verdict: accuracy and precision too low** for code-reading (small, densely
  packed AOIs) despite extensive calibration/guidance. Bounds the
  content-*dependent* D2 vector: webcam gaze does not resolve token-level
  reading.
- Useful honesty for GazePry: it does *not* threaten the re-ID thesis, which is
  content-*independent* and needs distributional dynamics, not fine pointing.

## Related

- [[webcam-tracking-validation]] — the counterweight to the optimistic studies.
- [[gaze-feature-extraction]] — low-frequency fixation detection challenge.
- [[leakage-vectors-d1-d6]] — bounds D2 (fine reading) on a webcam.

## Mentions in sources

- Context on webcam limits. Not enumerated in plan §21.
