---
type: source
tags: [project-doc, direction, d7, recognition, research-plan]
aliases: [D7 direction, GazePry_D7_Recognition_Knowledge_Direction.md, Recognition Oracle, D7 Recognition and Concealed-Knowledge Leakage]
sources: [d7-recognition-knowledge-direction]
reviewed: false
updated: 2026-07-23
---

`GazePry_D7_Recognition_Knowledge_Direction.md` — the research-direction
blueprint for **D7, recognition and concealed-knowledge leakage**
([[recognition-knowledge-leakage]]), titled *"The Recognition Oracle."* A
**new** vector beyond the [[leakage-vectors-d1-d6]] taxonomy: the leaked payload
is **memory contents** (what the visitor has seen or used before), which is
neither a biometric ([[gaze-re-identification]], D4) nor present-tense intent
([[reading-search-intent-leakage]], D2).

**Standalone since 2026-07-23.** It was previously a companion to
[[reid-research-plan]] and [[d2-reading-search-intent-direction]]; it now
carries its own apparatus, ethics, data-handling and bibliography sections and
contrasts itself against *classes* of gaze attack rather than against the
sibling plans. The D1–D6 placement is still true and still recorded in the wiki
([[leakage-vectors-d1-d6]]) — it is simply no longer stated in the document.

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
  (perfect ground truth, run first); E2 naturally acquired familiarity — public
  figures, retail bank marks, and widely photographed places (the headline, and
  the weakest link); E3 sensitive-topic exposure, ethically scoped (no protected
  characteristics), and explicitly a **weaker construct** rather than merely a
  weaker manipulation.
- **E2 arrays are class-homogeneous** (§6.4): four faces, or four bank marks,
  never a mix, because a mixed array lets the probe be identified by category
  instead of by familiarity.
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
- **§8 documents the implemented pipeline** — the end-to-end order of
  operations, which steps *refuse* rather than warn, the JS↔Python parity
  requirement, and the stimulus sourcing/provenance machinery.
- **Status: instrumented, not run.** No D7 data exists. H0–H5 are pre-registered
  predictions, not findings.

## Citation numbering — local, and it collides

**Since 2026-07-23 this document carries its own complete bibliography,
renumbered [1]–[30], which does *not* match the shared project numbering in
`GazePry_ReID_Research_Plan.md` §21.** The overlaps are silent: [5] is Weinberg
(history sniffing) in the shared scheme but Nahari et al. 2019 here; [6] is
Liebling & Preibusch there and Millen & Hancock here; Weinberg is [16] here.
The doc-local `[M1]`/`[C1]`/`[W1]`/`[P1]` labels of the previous draft are gone.

Wiki pages continue to cite the **shared** numbering. Resolve any claim traced
to this document by author-year, never by carrying its bracket number across.
See [[SCHEMA]] and [[2026-07-23-d7-standalone-and-e2-stimuli]].

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

- **Four unverified citations** — Lancry-Dayan 2018, Van der Cruyssen 2024
  CIT-leakage, the *Collabra* five-paradigm replication, and the decade privacy
  review (doc-local [9], [10], [15], [17]; formerly [C6], [C7], [W5], [P1]);
  §13 step 2.
- **Scoop risk** (§11): Van der Cruyssen, Ben-Shakhar, Pertzov & Verschuere hold
  both the CIT expertise and the webcam validation and are one reframing away.
- **The bibliography merge into plan §21 as [55]–… no longer applies** as
  written: the document was made standalone instead, so its references now
  duplicate rather than extend the shared list. If the two are ever
  reconciled, the local [1]–[30] must be mapped, not appended.
- **E3 is unsourced and blocked** (§8.4) — a construct problem, not a sourcing
  one.
