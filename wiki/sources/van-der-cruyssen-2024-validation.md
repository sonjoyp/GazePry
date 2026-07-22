---
type: source
tags: [paper, webcam-eye-tracking, validation, replication, novelty-preference, d7, peer-reviewed]
aliases: [Van der Cruyssen et al. 2024, Van der Cruyssen et al. 2023, validation of online webcam-based eye-tracking, novelty preference replication, cascade effect replication]
sources: [van-der-cruyssen-2024-validation, d7-recognition-knowledge-direction]
reviewed: false
updated: 2026-07-22
---

Van der Cruyssen, Ben-Shakhar, Pertzov, Guy, Cabooter, Gunschera & Verschuere —
*The validation of online webcam-based eye-tracking: The replication of the
cascade effect, the novelty preference, and the visual world paradigm*,
**Behavior Research Methods 56(5), 4836–4849, 2024**, doi
10.3758/s13428-023-02221-2. Replicates three classic eye-tracking effects with
**WebGazer.js** — part of the [[webcam-tracking-validation]] argument, and **the
single most important feasibility citation for
[[recognition-knowledge-leakage]]** (D7). *Not in plan §21 — cite author-year
(doc-local [W1] in [[d7-recognition-knowledge-direction]]).*
(`raw/The validation of online webcam-based eye-tracking...-2024.pdf`)

## Key facts

- All three effects — **cascade effect** (n = 134,
  [[shimojo-2003-gaze-cascade]]), **novelty preference** (n = 45), **visual world
  paradigm** (n = 32) — replicated online, but effect sizes **shrank 20–27%**; a
  same-participant lab-vs-online comparison confirmed the shrinkage is partly
  webcam noise, not just replication. Reference tracker: **EyeLink 1000 Plus**;
  in Study 3 lab fixations to target reached **71% vs 52% online**.
- **Novelty preference is the D7 signal.** Familiarization showed *two identical
  images* for **5000 ms**, then a display pairing the seen image with a novel one.
  This is the recognition-memory looking asymmetry
  ([[eye-movement-memory-effect]]) that D7 weaponizes — already demonstrated to
  survive a commodity webcam.
- **Stimulus geometry (D7 §6.2 is pinned to this):** images **472 × 331 px,
  295 px apart**. Authors state that studies "requiring high precision and
  accuracy" with "small or intricate areas of interest" remain unsuitable.
- Practical bound: webcam gaze works for effects that don't need high precision —
  roughly **≤ 4 large regions of interest**. Directly bounds what
  content-*dependent* AOI reading (D2) and tile-array probing (D7) can expect.
- **Author overlap worth noting:** Ben-Shakhar and Pertzov also authored
  [[nahari-2019-concealed-familiarity]], and Verschuere is a deception-detection
  researcher. The forensic [[ocular-concealed-information-test]] community has
  **already brought its instrument to the webcam** — the scoop risk recorded in
  [[d7-recognition-knowledge-direction]] §10.

## Related

- [[webcam-tracking-validation]] — the concept this feeds.
- [[recognition-knowledge-leakage]] — D7; this paper supplies both its feasibility
  evidence and its stimulus geometry.
- [[leakage-vectors-d1-d6]] — the ≤ 4-AOI bound constrains D2 reading/search and
  caps D7 arrays at four tiles.
- [[thilderkvist-2024-limitations]] — the harder counterpoint on fine AOIs.
- [[webgazer]] — the tracker validated.

## Mentions in sources

- Report §5.1. `GazePry_D7_Recognition_Knowledge_Direction.md` §3, §5 (H1), §6.2,
  §9.3 [W1], §10. Not enumerated in plan §21.

## Open questions

- Year ambiguity: online-first **2023**, journal issue **2024**. The wiki slug and
  the D7 doc both use *2024*; keep that consistent and cite the issue year.
- Page deepened 2026-07-22 from verified publisher metadata and PMC full text
  (PMC11289066); the underlying `raw/` PDF has still not been read end to end.
