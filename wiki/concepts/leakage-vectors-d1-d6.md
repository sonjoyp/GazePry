---
type: concept
tags: [threat-model, leakage, taxonomy]
aliases: [Leakage Vectors, D1-D6, D1, D2, D3, D4, D5, D6, Six Directions]
sources: [information-leakage-report]
reviewed: false
updated: 2026-07-10
---

The six **leakage vectors** the project organizes gaze attacks into, mapped to
the [[two-regimes-of-leakage]]. D1–D2 are content-dependent; D3–D5 are
content-independent; D6 covers defenses.

## Key facts

| ID | Vector | Regime | What leaks | Evidence |
|---|---|---|---|---|
| **D1** | On-screen keyboard / PIN inference | content-dependent | PINs, passwords, unlock codes | [8], [12], [27] |
| **D2** | Reading content & search intent | content-dependent | what the user reads, queries, attends to | [4], [7] |
| **D3** | Cognitive & affective state | content-independent | attention, confusion, mind-wandering, engagement, load | [1], [2], [22], [26] |
| **D4** | Behavioral-biometric [[gaze-re-identification|re-ID]] & cross-site tracking | content-independent | persistent identity, linkage across sessions/sites/devices | [20], [29] |
| **D5** | Attribute & demographic inference | content-independent | gender, age, geographic origin | [10], [21] |
| **D6** | Defenses & drive-by detection | — | mitigations: differential privacy, on-device processing, consent design | [13], [23], [24] |

- **Codebase status:** D2 is closest to fully implemented (inherits
  [[searchgazer]] AOI instrumentation); D1 is the natural content-dependent
  demonstrator; D3 partially exploitable via dwell-time/pupil; D4–D5 need a
  matching/attribute model on the per-frame feature stream.
- **D4 is Direction 1** — see [[direction-1-study-protocol]].

## Related

- [[two-regimes-of-leakage]] — the two-way split this table refines.
- [[gaze-re-identification]] — vector D4, the project's lead direction.
- [[evidence-summary]] — the quantitative backing for these vectors.

## Mentions in sources

- Report §4 (Leakage Vectors D1–D6).
