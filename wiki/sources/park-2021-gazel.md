---
type: source
tags: [paper, gaze-tracking, smartphone, transfer-learning, head-pose]
aliases: [Park et al. 2021, GAZEL]
sources: [park-2021-gazel]
reviewed: false
updated: 2026-07-11
---

Park, Park, Cha (Yonsei) — *GAZEL: Runtime Gaze Tracking for Smartphones*,
**IEEE PerCom 2021**. A head-pose-resilient smartphone gaze tracker; supporting
context for the mobile form-factor arm of [[form-factor-analysis]] and the
cloud-vs-on-device latency point [[webeyetrack]] cites. *Not in plan §21 — cite
author-year.* (`raw/GAZEL Runtime Gaze Tracking for Smartphones...-2021.pdf`)

## Key facts

- **Tablet-to-smartphone transfer learning:** train a CNN on large-screen
  tablet data, transplant to the phone; head-pose-resilient, lightweight
  architecture; implicit calibration.
- ≈27.5% more accurate than prior smartphone gaze techniques; up to **18 fps**
  runtime on commercial phones.
- Data point for "on-device mobile gaze is practical," complementing the
  handheld-privacy literature ([[alsakar-2025-handheld-privacy]]).

## Related

- [[form-factor-analysis]] — the smartphone surface.
- [[webeyetrack]] — cites GAZEL on cloud-inference privacy/latency concerns.
- [[gaze-estimation]] — CNN appearance-based mobile branch.

## Mentions in sources

- Context for mobile gaze tracking. Not enumerated in plan §21.
