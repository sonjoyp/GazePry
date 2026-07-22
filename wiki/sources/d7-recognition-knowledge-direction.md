---
type: source
tags: [project-doc, direction, d7, recognition, research-plan]
aliases: [D7 direction, GazePry_D7_Recognition_Knowledge_Direction.md, Recognition Oracle, D7 Recognition and Concealed-Knowledge Leakage]
sources: [d7-recognition-knowledge-direction]
reviewed: false
updated: 2026-07-22
---

`GazePry_D7_Recognition_Knowledge_Direction.md` — the research-direction
blueprint for **D7, recognition and concealed-knowledge leakage**
([[recognition-knowledge-leakage]]), titled *"The Recognition Oracle."* A
**new** vector beyond the [[leakage-vectors-d1-d6]] taxonomy: the leaked payload
is **memory contents** (what the visitor has seen or used before), which is
neither a biometric ([[gaze-re-identification]], D4) nor present-tense intent
([[reading-search-intent-leakage]], D2). Companion to, not a replacement for,
[[reid-research-plan]] and [[d2-reading-search-intent-direction]].

## Key facts

- **Thesis:** recognition is involuntary and moves the eyes
  ([[eye-movement-memory-effect]]); a first-party page holding a camera grant can
  render an ordinary-looking tile array and read **which items the visitor has
  seen before** from dwell asymmetry alone. Reframes the forensic
  [[ocular-concealed-information-test]] as a covert web extraction attack.
- **The key inversion:** the CIT literature's main limitation is *countermeasures*
  ([[nahari-2019-concealed-familiarity]],
  [[millen-2019-concealed-face-recognition]]), which assume a subject who **knows
  they are being tested**. A drive-by web visitor does not, so the covert setting
  is **strictly easier than the forensic one**. RQ4 quantifies that advantage.
- **Rhetorical anchor:** browsers killed `:visited` history sniffing
  ([[weinberg-2011-history-sniffing]] [5]) at the rendering layer; D7 relocates
  the capability one layer below, where **the side channel is the user**.
- **Why it is more tractable than D4 right now:** the effect is a
  within-participant, within-trial contrast **between AOIs on the same screen**,
  so calibration, lighting, tracker, and logging cadence are constant across the
  compared units. With item-level counterbalancing (each item familiar for half
  the participants), saliency and position are orthogonal to the contrast by
  construction. Needs **N ≈ 40, one session** — not D4's N ≥ 50 with ≥1-week
  separation ([[pilot-empirical-status]]).
- **Six RQs.** RQ0 is the gate (recognition vs item saliency vs position vs
  calibration; shuffled-label + saliency-only nulls). RQ1 mechanism/decay,
  RQ2 real-world familiarity (headline), RQ3 [[ceiling-vs-commodity]],
  RQ4 countermeasures, RQ5 [[gaze-perturbation-defense]].
- **Three experiments.** E1 lab-installed familiarity with delay manipulation
  (perfect ground truth, run first); E2 naturally acquired familiarity — which web
  services the visitor actually uses (the headline, and the weakest link);
  E3 sensitive-topic exposure, ethically scoped (no protected characteristics).
- **Sourced stimulus geometry:** 2 or 4 tiles, ≥ 400 × 300 px, ≥ 250 px apart —
  pinned by [[van-der-cruyssen-2024-validation]]'s working online geometry
  (472 × 331 px, 295 px apart) and the ≤ 4-AOI webcam bound
  ([[thilderkvist-2024-limitations]]).
- **New code required:** a probe-array task page, an **I-DT dispersion-threshold**
  fixation detector (the existing I-VT is too coarse at webcam rates and fixation
  *duration* is D7's load-bearing feature), a soft-assignment AOI feature
  extractor, and a per-trial/per-user classifier. Everything else reuses
  [[capture-harness]], [[gazepry-tracker]], [[reid-server]], and the
  [[simultaneous-capture-rig]].
- **Metrics:** per-trial AUC, **per-user AUC as a function of k trials** (the
  headline curve — *"how many tiles before a page knows which sites you use"*),
  TPR at FPR = 0.1, d′ per feature family.
- **Status: proposal only.** No D7 data exists. H0–H5 are pre-registered
  predictions, not findings.

## Related

- [[recognition-knowledge-leakage]] — the concept page for the direction.
- [[reid-research-plan]] — D4; shares the adversary, harness, and rig.
- [[d2-reading-search-intent-direction]] — D2; the same "tool → attack" reframe
  structure, applied to a different literature.
- [[ocular-concealed-information-test]] — the instrument being repurposed.
- [[drive-by-web-adversary]] — the threat model D7 inherits, minus the
  permission-free floor (D7 has **no** cursor equivalent; it needs gaze).

## Mentions in sources

- The document itself, all sections.

## Open questions

- **Three unverified citations** ([C6] Lancry-Dayan 2018, [C7] Van der Cruyssen
  2024 CIT-leakage, [P1] the decade privacy review) plus [W5]; §12 step 1.
- **Scoop risk** (§10): Van der Cruyssen, Ben-Shakhar, Pertzov & Verschuere hold
  both the CIT expertise and the webcam validation and are one reframing away.
- Bibliography merge into plan §21 as [55]–… is deferred until after the E1 pilot
  (§12 step 7), mirroring the [50]–[54] flow and the D2 doc's deferral.
