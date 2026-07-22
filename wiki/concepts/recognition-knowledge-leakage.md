---
type: concept
tags: [d7, recognition, memory, content-dependent, leakage, direction, core]
aliases: [D7, Recognition Knowledge Leakage, Recognition Oracle, Concealed-Knowledge Leakage, Knowledge Extraction, What You Already Know]
sources: [d7-recognition-knowledge-direction]
reviewed: false
updated: 2026-07-22
---

**Recognition & concealed-knowledge leakage** is **D7**, a *new* vector beyond the
[[leakage-vectors-d1-d6]] taxonomy, developed by
[[d7-recognition-knowledge-direction]] (*"The Recognition Oracle"*). A first-party
page holding a camera grant renders an ordinary-looking array of tiles and reads,
from dwell asymmetry and fixation timing alone, **which items the visitor has seen
before**. The leaked payload is **memory contents** — not a biometric
([[gaze-re-identification]], D4), not present-tense intent
([[reading-search-intent-leakage]], D2), not a demographic attribute. It
reframes the forensic [[ocular-concealed-information-test]] as a covert web
extraction attack, resting on the [[eye-movement-memory-effect]].

## Key facts

- **Tense is the taxonomy.** D4 leaks *who you are* (timeless); D2 leaks *what you
  are doing now* (present); D7 leaks *what you already knew before you arrived*
  (past). The three [[third-party-tracking-tag|compose]] into one adversary.
- **D7 is *interventional*, not observational.** D2 and D4 take whatever the user
  happens to look at; **D7's adversary designs the stimulus**, so it can ask a
  specific question ("has this person seen this?") and get a per-item answer. That
  is what makes it an *oracle*.
- **The covert setting is strictly easier than the forensic one.** The CIT
  literature's binding limitation is countermeasures
  ([[nahari-2019-concealed-familiarity]],
  [[millen-2019-concealed-face-recognition]]) — which presuppose a subject who
  **knows they are being tested**. A drive-by visitor
  ([[drive-by-web-adversary]]) does not, so the attack runs in the naive regime
  where effects are largest. RQ4 quantifies this advantage.
- **Rhetorical anchor:** browsers killed `:visited` history sniffing
  ([[weinberg-2011-history-sniffing]] [5]) at the *rendering* layer. D7 reinstates
  the capability one layer below, where **the side channel is the user**, and no
  browser patch reaches it.
- **The confound structurally cancels.** Unlike D4's person-vs-apparatus problem
  ([[reid-confound-controls]]), the D7 effect is a within-participant,
  within-trial contrast **between AOIs on the same screen**: calibration geometry,
  lighting, seating, tracker, and logging cadence are constant across the compared
  units. **Item-level counterbalancing** (each item familiar for half the
  participants) makes saliency and position orthogonal to the contrast.
- **Scale, needing N ≈ 40 and one session** — not D4's N ≥ 50 with ≥ 1-week
  separation ([[pilot-empirical-status]]) — because the unit of analysis is the
  *trial*, not the identity pair.
- **Sourced sensor bounds:** the recognition signal (novelty preference) already
  replicates on WebGazer with effect sizes shrinking **20–27%**
  ([[van-der-cruyssen-2024-validation]]); arrays are capped at **≤ 4 tiles**,
  ≥ 400 × 300 px, ≥ 250 px apart. Within-image AOIs (the eyes-vs-nose contrast
  carrying [[millen-2019-concealed-face-recognition]]'s best AUC 0.87) are **not**
  available on a webcam ([[thilderkvist-2024-limitations]]).
- **The countermeasure-resistant channel is temporal, not spatial** — mean and
  first fixation duration ([[schwedes-2012-revealing-glance]],
  [[millen-2019-concealed-face-recognition]]). This predicts that a
  [[gaze-perturbation-defense]] which only coarsens *space* will leave D7 open —
  a self-contained result even if the attack numbers underwhelm.
- **RQ0 is the gate:** the classifier must beat a **saliency-and-position-only**
  baseline and collapse under a **shuffled familiarity-label null** — the D7
  analogue of [[reid-confound-controls]] and of D2's saliency-prior gate.
- **Status: proposal only** — no D7 result exists; H0–H5 are pre-registered
  predictions ([[pilot-empirical-status]]).

## Related

- [[ocular-concealed-information-test]] — the forensic instrument being repurposed.
- [[eye-movement-memory-effect]] — the involuntary mechanism underneath.
- [[reading-search-intent-leakage]] — the D2 sibling; same "tool → attack" reframe
  structure, different literature and different tense.
- [[gaze-re-identification]] — the D4 sibling; D7 (knowledge) + D2 (intent) +
  D4 (identity) compose into a profile the user can neither see nor clear.
- [[ceiling-vs-commodity]] — RQ3 reuses the D4 rig to measure the IR-vs-webcam gap
  on recognition instead of identity.
- [[simultaneous-capture-rig]] — the Gazepoint + webcam apparatus, unchanged.
- [[task-suite]] — D7 adds a sixth task page (the probe array).
- [[same-origin-policy]] — D7 is first-party and makes **no** cross-site claim.
- [[target-venues]] — PETS/PoPETs primary, SOUPS companion, WPES hedge.

## Mentions in sources

- `GazePry_D7_Recognition_Knowledge_Direction.md` (all sections); plan §4 (the
  D1–D6 table D7 extends).

## Open questions

- **Scoop risk:** Van der Cruyssen, Ben-Shakhar, Pertzov & Verschuere hold both the
  CIT expertise and the webcam validation ([[van-der-cruyssen-2024-validation]],
  [[nahari-2019-concealed-familiarity]]) and are one reframing away from this
  paper. Their venues are psychology/forensic, not security.
- **E2 is much weaker than E1:** naturally acquired familiarity ("has an account
  on this site") cannot be assigned, so the counterbalancing that protects E1 is
  statistical rather than structural. This is the honest gap in the direction.
- **Sign instability:** familiarity produces *preference* in some paradigms and
  *avoidance* in others ([[nahari-2019-concealed-familiarity]] reports avoidance),
  and the early/late viewing windows can differ in direction. Directional
  predictions must be pre-registered per window.
