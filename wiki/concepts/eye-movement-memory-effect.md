---
type: concept
tags: [memory, mechanism, d7, phenomenon, recognition]
aliases: [Eye-Movement-Based Memory Effect, EMME, novelty preference, recognition looking asymmetry, reprocessing effect]
sources: [d7-recognition-knowledge-direction]
reviewed: false
updated: 2026-07-22
---

The **eye-movement-based memory effect** is the finding that a previously seen
stimulus is *visually sampled differently* from a novel one. It is the mechanism
[[recognition-knowledge-leakage]] (D7) exploits and the reason
[[ocular-concealed-information-test|the ocular CIT]] works at all. Its
privacy-relevant property is that it is **involuntary**: it is an obligatory
consequence of prior exposure, not a decision to disclose.

## Key facts

- **Foundational demonstration:** [[althoff-1999-eye-movement-memory-effect]] —
  famous vs non-famous faces elicit different eye-movement patterns across a range
  of processing tasks, on multiple measures.
- **It is fast.** The effect emerges **within the first five fixations**
  [[althoff-1999-eye-movement-memory-effect]], which is why D7 needs only a short
  observation window per probe rather than a long dwell.
- **It does not require conscious recollection** [[hannula-2010-worth-a-glance]] —
  gaze expresses memory whether or not the viewer reports, or notices,
  recognizing anything. This is the load-bearing "leak, not disclosure" claim.
- **Direction of the asymmetry is not fixed.** In the *novelty preference*
  formulation ([[van-der-cruyssen-2024-validation]]) viewers look **more** at the
  novel item; in the concealed-familiarity arrays of
  [[nahari-2019-concealed-familiarity]] the pattern is **avoidance** of the
  familiar item; and dwell can **reverse sign** between an early window
  (~0.7–2 s) and a later one. Any design that averages across the reversal risks
  nulling a real effect.
- **It survives a commodity webcam.** [[van-der-cruyssen-2024-validation]]
  replicated the novelty preference online with WebGazer.js (n = 45), with effect
  sizes shrinking **20–27%** relative to lab studies.
- **It survives delay.** [[zangrossi-2024-aiat-eye-movements]] detected
  week-old mock-crime memories at 75% from fixation topography alone.
- **The measure that survives concealment is temporal.** Fixation duration reveals
  memory regardless of the intention to conceal
  ([[schwedes-2012-revealing-glance]]) and strengthens under deliberate
  countermeasures ([[millen-2019-concealed-face-recognition]], d = 0.66 → 0.91)
  even as fine spatial measures collapse.

## Related

- [[recognition-knowledge-leakage]] — the D7 attack built on this effect.
- [[ocular-concealed-information-test]] — the forensic operationalization.
- [[shimojo-2003-gaze-cascade]] — a distinct gaze-bias phenomenon (preference, not
  memory) that D7 could probe as a variant.
- [[webcam-tracking-validation]] — why the effect is measurable in a browser.
- [[gaze-feature-extraction]] — D7 needs an AOI-anchored extractor and an **I-DT**
  fixation detector, since fixation *duration* is the load-bearing feature and the
  existing I-VT threshold is coarse at webcam rates.

## Mentions in sources

- `GazePry_D7_Recognition_Knowledge_Direction.md` §1, §3, §7.2, §9.1.

## Open questions

- The sign-and-window instability above is the biggest methodological hazard in
  D7. Which window and which direction hold for *tile arrays of logos* (rather
  than faces) is genuinely unknown and must come from the E1 pilot.
