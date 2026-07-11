---
type: concept
tags: [re-identification, tracking, biometrics, core]
aliases: [Gaze Re-Identification, Re-ID, Re-identification, Cross-Site Re-ID, D4]
sources: [direction-1-study-protocol, information-leakage-report, prototype-code]
reviewed: false
updated: 2026-07-10
---

**Gaze re-identification** is the core mechanism of Direction 1: linking a
visitor's sessions across sites and over time by their eye-movement *dynamics*,
with no cookie or client-side state. It is vector D4 in the
[[leakage-vectors-d1-d6]], it is content-independent (so it
[[same-origin-policy|survives SOP]]), and it is the basis of the
[[person-bound-fingerprint]] thesis.

## Key facts

- Adversary embeds one [[third-party-tracking-tag|tag]] across many sites;
  matches a probe session to an enrolled gallery by
  [[gaze-feature-extraction|feature distance]] (standardize → Euclidean →
  nearest gallery session per participant).
- Content-independent: does not depend on knowing the screen, so
  [[same-origin-policy]] does **not** block it (unlike content peeking).
- The **hard case** is [[cross-task-generalization]] (enroll on site A, identify
  on site B) — the [[reid-protocols|cross_task_cross_session]] headline protocol.
- Measured with [[reid-metrics]] (rank-1/rank-5, CMC, EER).
- [[survives-de-identification|Survives face removal]] and
  [[unclearability|browser-state clearing]] — the two properties that make it a
  novel tracking channel.

## Related

- [[person-bound-fingerprint]] — the framing of what re-ID produces.
- [[cross-task-generalization]] — the differentiator vs prior biometrics work.
- [[unclearability]] — why it beats a clearable cookie.
- [[eye-movement-biometrics]] — the research-grade signal it rests on.

## Mentions in sources

- Protocol §1 (Thesis), §2 (Threat model); Report §8 (re-ID is the realistic
  cross-site risk); `prototype/reid-core.js` (`identify`).
