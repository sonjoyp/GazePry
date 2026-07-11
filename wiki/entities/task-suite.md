---
type: entity
subtype: system
tags: [stimuli, tasks, prototype, study-design]
aliases: [Task Suite, Five Tasks, Stimuli, Task Sites, tasks/]
sources: [direction-1-study-protocol, prototype-readme]
reviewed: false
updated: 2026-07-10
---

The **five tasks** that stand in for five distinct "sites." Different tasks
elicit different gaze dynamics, so enrolling on one and identifying on another
is the [[cross-task-generalization|cross-task]] tracking test — the study's
headline. Implemented as `prototype/public/tasks/*.html` in the
[[capture-harness]].

## Key facts

- The five: **reading** (text passage — reading-biometrics heritage [7], [22]),
  **SERP** scanning (search-results layout — the [[searchgazer]] core [4]),
  **images** (free viewing), **video** watching, **form**/typing.
- Each finished task POSTs one session `P01_S1_<task>_<ts>.json`.
- **Same-task** matching is an upper bound; **cross-task** is the real tracking
  threat — the protocol reports them separately.

## Related

- [[cross-task-generalization]] — the RQ2 test these tasks enable.
- [[searchgazer]] — the SERP task's AOI lineage.
- [[capture-harness]] — where these pages live.

## Mentions in sources

- Protocol §6 (Stimuli — the multi-"site" design); `prototype/public/tasks/`;
  `prototype/README.md`.
