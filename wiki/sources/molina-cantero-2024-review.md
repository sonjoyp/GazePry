---
type: source
tags: [paper, review, visible-light-eye-tracking, low-cost-camera]
aliases: [Molina-Cantero et al. 2024, visible-light eye-tracking review]
sources: [molina-cantero-2024-review]
reviewed: false
updated: 2026-07-11
---

Molina-Cantero et al. — *A review on visible-light eye-tracking methods based
on a low-cost camera*, **J. Ambient Intelligence and Humanized Computing
2024**. A scoping review of webcam/visible-light gaze estimation methods —
background taxonomy for [[gaze-estimation]] and [[webcam-tracking-validation]].
*Not in plan §21 — cite author-year.*
(`raw/A review on visible-light eye-tracking methods...-2024.pdf`)

## Key facts

- Scoping review (>500 studies screened → 44 selected, κ=0.86). Three method
  families for visible-light trackers: **appearance-based, feature-based,
  model-based**; none significantly outperformed the others on reported
  accuracy (KW p=0.14), though appearance-based (deep-learning) is growing.
- **Head movement worsens accuracy**; few methods correct head pose — the exact
  gap [[webeyetrack]] targets. Only 5 chin-rest-free studies reached <2°
  accuracy (one illuminance-invariant).
- Framed for an ALS assistive eye-tracker build (Part 1 of a two-part study).

## Related

- [[gaze-estimation]] — the method taxonomy this reviews.
- [[webcam-tracking-validation]] — corroborates head-pose as the limiting
  factor and the <2° achievable ceiling.
- [[webeyetrack]] — the head-pose-aware answer to this review's main caveat.

## Mentions in sources

- Background taxonomy. Not enumerated in plan §21.
