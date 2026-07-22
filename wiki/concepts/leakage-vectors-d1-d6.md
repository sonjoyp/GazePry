---
type: concept
tags: [threat-model, leakage, taxonomy]
aliases: [Leakage Vectors, D1-D6, D1-D7, D1, D2, D3, D4, D5, D6, D7, Six Directions, Seven Directions]
sources: [information-leakage-report, d7-recognition-knowledge-direction]
reviewed: false
updated: 2026-07-22
---

The **leakage vectors** the project organizes gaze attacks into, mapped to
the [[two-regimes-of-leakage]]. D1–D2 are content-dependent; D3–D5 are
content-independent; D6 covers defenses. **D7 was appended 2026-07-22** and is
content-dependent and *adversary-chosen*; the original report defines only D1–D6.

## Key facts

| ID | Vector | Regime | What leaks | Evidence |
|---|---|---|---|---|
| **D1** | On-screen keyboard / PIN inference | content-dependent | PINs, passwords, unlock codes | [8], [12], [27] |
| **D2** | [[reading-search-intent-leakage\|Reading content & search intent]] | content-dependent | what the user reads, queries, attends to | [4], [7] |
| **D3** | Cognitive & affective state | content-independent | attention, confusion, mind-wandering, engagement, load | [1], [2], [22], [26] |
| **D4** | Behavioral-biometric [[gaze-re-identification|re-ID]] & cross-site tracking | content-independent | persistent identity, linkage across sessions/sites/devices | [20], [29] |
| **D5** | Attribute & demographic inference | content-independent | gender, age, geographic origin | [10], [21] |
| **D6** | Defenses & drive-by detection | — | mitigations: differential privacy, on-device processing, consent design | [13], [23], [24] |
| **D7** | [[recognition-knowledge-leakage\|Recognition & concealed knowledge]] | content-dependent, **adversary-chosen** | what the visitor has **seen or used before** (memory contents) | Althoff & Cohen 1999; Schwedes & Wentura 2012; Nahari 2019; Millen & Hancock 2019 |

- **Why D7 is a new row rather than a fit into an old one:** recognition leakage is
  content-dependent like D1/D2, but what it extracts is neither an entered secret
  (D1), nor present-tense interest (D2), nor identity (D4), nor a demographic
  attribute (D5). It extracts **stored memory**.
- **Tense distinguishes the three developed directions:** D4 leaks *who you are*
  (timeless), D2 leaks *what you are doing now* (present), D7 leaks *what you
  already knew before you arrived* (past). D7 is also the only one whose adversary
  is **interventional** — it designs the stimulus rather than observing whatever
  the user happens to look at.
- **Codebase status:** D2 is closest to fully implemented (inherits
  [[searchgazer]] AOI instrumentation); D1 is the natural content-dependent
  demonstrator; D3 partially exploitable via dwell-time/pupil; D4–D5 need a
  matching/attribute model on the per-frame feature stream; D7 needs a new
  probe-array task page, an **I-DT** fixation detector, and an AOI-anchored
  extractor ([[d7-recognition-knowledge-direction]] §6.1).
- **D4 is Direction 1** — see [[direction-1-study-protocol]] and
  [[gaze-re-identification]].
- **D2 is now a developed direction** — see
  [[reading-search-intent-leakage]] and [[d2-reading-search-intent-direction]]
  (*"No Clicks, No Privacy"*): first-party reading/search-intent leakage via webcam
  gaze + permission-free [[cursor-tracking]]. Content-dependent, so scoped
  within-site (not cross-site), but hosts a real threat via zero-click intent.
- **D7 is now a developed direction** — see [[recognition-knowledge-leakage]] and
  [[d7-recognition-knowledge-direction]] (*"The Recognition Oracle"*): a
  first-party page probes with an adversary-chosen tile array and reads which
  items the visitor has seen before, repurposing the forensic
  [[ocular-concealed-information-test]]. Unlike D2 it has **no permission-free
  floor** — it needs gaze.

## Related

- [[two-regimes-of-leakage]] — the two-way split this table refines.
- [[gaze-re-identification]] — vector D4, the project's lead direction.
- [[reading-search-intent-leakage]] — vector D2, developed as the second direction.
- [[cursor-tracking]] — the permission-free mouse modality D2 adds.
- [[recognition-knowledge-leakage]] — vector D7, developed as the third direction.
- [[eye-movement-memory-effect]] — the involuntary mechanism D7 rests on.
- [[evidence-summary]] — the quantitative backing for these vectors.

## Mentions in sources

- Report §4 (Leakage Vectors D1–D6); D7 has no report entry — it originates in
  `GazePry_D7_Recognition_Knowledge_Direction.md` §2.
