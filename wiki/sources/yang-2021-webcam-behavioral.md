---
type: source
tags: [paper, webcam-eye-tracking, validation, jspsych, temporal-resolution]
aliases: [Yang and Krajbich 2021, Webcam-based online eye-tracking for behavioral research]
sources: [yang-2021-webcam-behavioral]
reviewed: false
updated: 2026-07-11
---

Yang & Krajbich — *Webcam-based online eye-tracking for behavioral research*,
**Judgment and Decision Making 2021**. Integrates [[webgazer]] into the widely
used **jsPsych** library and tunes it for behavioral experiments — part of the
[[webcam-tracking-validation]] argument, and the source of the ~30 Hz
temporal-resolution figure. *Not in plan §21 — cite author-year.*
(`raw/Webcam-based online eye-tracking for behavioral research...-2021.pdf`)

## Key facts

- Cut WebGazer's calibration/validation overhead and improved **temporal
  resolution from 100–1000 ms to 20–30 ms** (~30–50 Hz) — the practical webcam
  frame rate the plan's sampling-rate caveat assumes.
- Replicated in-lab gaze–choice relationships (attentional drift-diffusion) on
  MTurk with little spatial/temporal degradation.
- Concludes online webcam eye tracking is feasible for behavioral research.

## Related

- [[webcam-tracking-validation]] — the concept this feeds.
- [[ceiling-vs-commodity]] — the ~30 Hz webcam rate limits saccade-velocity
  features (plan §9 sampling-rate caveat).
- [[webgazer]] — the tracker integrated.

## Mentions in sources

- Report §5.1. Not enumerated in plan §21.
