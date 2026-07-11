---
type: source
tags: [paper, webcam-eye-tracking, open-source, deep-learning]
aliases: [Zhu et al. 2025, GazeFollower]
sources: [zhu-2025-gazefollower]
reviewed: false
updated: 2026-07-11
---

Zhu et al. (Zhejiang University) — *GazeFollower: An open-source system for
deep learning-based gaze tracking with web cameras*, **Proc. ACM CGIT 2025**.
A Python open-source webcam tracker — another rising commodity-ceiling data
point for [[webcam-tracking-validation]]. *Not in plan §21 — cite author-year.*
(`raw/GazeFollower...-2025.pdf`)

## Key facts

- Core model trained on **32 million face images**; customizable in Python.
- Benchmark (N=31): **1.11 cm accuracy / 0.11 cm precision** with calibration;
  personalized fine-tuning → **0.92 cm / 0.08 cm** — on par with or better than
  budget commercial eye trackers. More accurate than the [[webgazer]]
  generation and comparable to [[webeyetrack]].
- Reinforces that open-source webcam gaze is closing on IR hardware — relevant
  to how tight the [[ceiling-vs-commodity]] gap is becoming.

## Related

- [[webcam-tracking-validation]] — the accuracy-trajectory argument.
- [[webeyetrack]], [[eyegestures]] — sibling modern open-source webcam trackers
  (GazeFollower is Python/desktop, not a browser arm, so it was not adopted as
  a harness arm).
- [[gaze-estimation]] — deep-learning appearance-based branch.

## Mentions in sources

- Context for the webcam accuracy trajectory. Not enumerated in plan §21.
