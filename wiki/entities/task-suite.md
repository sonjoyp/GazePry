---
type: entity
subtype: system
tags: [stimuli, tasks, prototype, study-design]
aliases: [Task Suite, Five Tasks, Stimuli, Task Sites, tasks/]
sources: [reid-research-plan, readme]
reviewed: false
updated: 2026-07-11
---

The **five tasks** that stand in for five distinct "sites." Different tasks
elicit different gaze dynamics, so enrolling on one and identifying on another
is the [[cross-task-generalization|cross-task]] tracking test — the study's
headline. Implemented as `public/tasks/*.html` in the [[capture-harness]].

## Key facts

- The five: **reading** (text passage — reading-biometrics heritage [7], [22],
  [30]), **SERP** scanning (search-results layout — the [[searchgazer]] core
  [4]), **images** (free viewing), **video** watching, **form**/typing.
- Each finished task POSTs one session `P01_S1_<task>_<tracker>_<ts>.json` —
  the same five tasks are run under whichever tracker arm the session selected.
- **Same-task** matching is an upper bound; **cross-task** is the real tracking
  threat — the protocol reports them separately.

## Related

- [[cross-task-generalization]] — the RQ2 test these tasks enable.
- [[searchgazer]] — the SERP task's AOI lineage.
- [[capture-harness]] — where these pages live.
- [[reading-search-intent-leakage]] — the D2 direction makes the **SERP** task its
  headline surface (strongest cursor–gaze alignment); it needs click-required vs
  **zero-click/good-abandonment** SERP variants and a first-class
  [[cursor-tracking|cursor]] (move/hover/scroll) log, not just calibration clicks.
- [[recognition-knowledge-leakage]] — the D7 direction adds a **sixth** task page,
  a *recognition-probe array* (`public/tasks/probe.html`): 2–4 tiles of ≥ 400 ×
  300 px, ≥ 250 px apart, 4000 ms free viewing per trial, with the AOI rectangles
  logged alongside the gaze stream. Unlike the five existing tasks it is
  **trial-structured and adversary-designed** rather than a naturalistic "site,"
  and its cover task (low-demand vs memory-adjacent) is a manipulated factor.

## Mentions in sources

- Plan §11 (Stimuli — the multi-"site" design); `public/tasks/`; `README.md`
  (Quick start).
