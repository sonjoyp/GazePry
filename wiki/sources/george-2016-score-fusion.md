---
type: source
tags: [eye-movement-biometrics, score-fusion, interpretable, foundations]
aliases: [George and Routray 2016, score level fusion eye movement biometrics, GRBFN]
sources: [george-2016-score-fusion]
reviewed: false
updated: 2026-07-11
---

George & Routray (IIT Kharagpur) — *A Score-level Fusion Method for Eye
Movement Biometrics*, **Pattern Recognition Letters 2016** — bibliography
**[31]**. The interpretable hand-crafted baseline for GazePry's route (a)
([[gaze-feature-extraction]]); source of the corrected EER figure in the plan's
§21 verification notes. (`raw/A score level fusion method...-2016.pdf`)

## Key facts

- **Gaussian RBF network** on features split into fixations and saccades, with
  score-level fusion in the output layer; forward feature selection by EER.
- **Corrected numbers (plan §21):** EER **≈2.59%** and high rank-1 on the
  **BioEye 2015** database (**153 subjects**, ages 18–43; random-dot-following
  and text-reading stimuli). The earlier draft's "EER ≈5.8%, 320 subjects" did
  **not** check out — quote 2.59% and the paper's own 153 subjects.
- **Template aging** (third session ~1 year later, 37 subjects): average EER
  **≈10.96%**, rank-1 ≈81.08% — a concrete cross-session degradation number
  directly relevant to GazePry's ≥1-week [[unclearability]] / test–retest claim.
- Reiterates the counterfeit-resistance argument (oculomotor plant is hard to
  spoof with mechanical replicas).

## Related

- [[eye-movement-biometrics]] — the interpretable ceiling for route (a).
- [[gaze-feature-extraction]] — the fixation/saccade feature lineage.
- [[reid-research-plan]] — §21 records the 2.59% / 153-subject correction.
- [[holland-2011-scanpath-biometrics]] — the feature-family predecessor.
- [[al-zaidawi-2022-multi-dataset]] — related template-aging analysis.

## Mentions in sources

- Plan §12 (route (a) score-fusion lineage), §18.1, **§21 (correction)** [31].

## Open questions

- Quote the paper's per-task EERs (random-stimulus vs text-reading) directly
  when writing the related-work section — the plan flags text-reading as the
  higher-EER condition; confirm from the paper's tables.
