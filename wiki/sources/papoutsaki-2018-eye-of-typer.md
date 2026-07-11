---
type: source
tags: [paper, webcam-eye-tracking, typing, dataset, benchmark]
aliases: [Eye of the Typer, Papoutsaki et al. 2018, EOTT dataset]
sources: [papoutsaki-2018-eye-of-typer]
reviewed: false
updated: 2026-07-11
---

Papoutsaki, Gokaslan, Tompkin, He, Huang — *The Eye of the Typer: A Benchmark
and Analysis of Gaze Behavior during Typing*, **ETRA 2018** — bibliography
**[7]**. Two things GazePry uses it for: it is a source for the
[[webgazer]]-drift claim and gaze-during-typing behavior, and it released a
51-participant **benchmark dataset** (webcam video + Tobii ground truth + full
interaction logs across calibration/pointing/search/writing tasks) — the
lineage of the multi-task [[task-suite]] design.
(`raw/The eye of the typer...-2018.pdf`)

## Key facts

- **Dataset:** 64 recruited / 51 analyzed; per participant: webcam face video,
  screen recording, mouse+keyboard logs, and **Tobii Pro X3-120** gaze
  (120 Hz, 0.4° accuracy) as ground truth. Tasks: 2 calibration, 1 Fitts
  pointing, 4 search (TREC 2014 queries → real Google SERPs), 4 creative
  writing; two lighting conditions; heads free to move. 4.5M gaze predictions.
- **The drift/accuracy figure GazePry cites:** the "Final Dot Test" runs
  ≈20 min after calibration specifically to measure drift; WebGazer's ≈4.17°
  accuracy is quoted here versus PACE's 2.56° (after >1000 interactions).
- **Gaze–interaction alignment (grounds [[covert-calibration]]):** gaze–click
  mean distance 137 px (closest 110 px, 480 ms *before* the click — the eye
  leads then drifts); gaze–cursor 206 px; gaze–typing 192 px overall but
  160 px for touch typists vs 352 px for non-touch.
- Touch vs non-touch typists separable from gaze glances at **92% accuracy**;
  adding typing as a WebGazer cue improves accuracy 16% (touch) / 8%
  (non-touch) — evidence that keystroke timing is itself a gaze-correlated,
  person-varying signal.
- **Web-timestamp limitation** the harness inherits: browser frame capture has
  a ≈1/30 s variable gap, so *saccades* get wrong instantaneous webcam gaze
  but *fixations* are ~correct — exactly why the plan warns 30 Hz limits
  saccade-velocity features ([[ceiling-vs-commodity]] sampling-rate caveat).
- Notes GazeCapture (Krafka et al., 2.5 M frames / 1450 users) as the
  large-N appearance-model dataset — the same one [[webeyetrack]] reports
  ≈2.32 cm on.

## Related

- [[webgazer]] — the tracker whose drift and accuracy this paper documents.
- [[papoutsaki-2017-searchgazer]], [[papoutsaki-2016-webgazer]] — same lineage.
- [[task-suite]] — the multi-task (reading/SERP/writing) design descends here.
- [[covert-calibration]] — the gaze-leads-click timing it quantifies.

## Mentions in sources

- Plan §3.1 (Eye-of-the-Typer characterizes gaze during typing), §5 (WebGazer
  drift [7]), §11 (reading task heritage [7]); report §6 [7].
