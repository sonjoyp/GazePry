---
type: source
tags: [paper, eye-movement-biometrics, cross-dataset, template-aging]
aliases: [Al Zaidawi et al. 2022, extensive study user identification eye movements multiple datasets]
sources: [al-zaidawi-2022-multi-dataset]
reviewed: false
updated: 2026-07-11
---

Al Zaidawi, Prinzler, Lührs, Maneth (University of Bremen) — *An Extensive
Study of User Identification via Eye Movements across Multiple Datasets*,
**Signal Processing: Image Communication 2022** — bibliography **[35]**. A
cross-dataset, **template-aging** study built on an improved
[[george-2016-score-fusion|George & Routray]] method — directly relevant to
GazePry's cross-session stability (RQ4) and honest degradation reporting.
(`raw/An extensive study of user identification...-2022.pdf`)

## Key facts

- Evaluates identification across multiple datasets: two **BioEye 2015** sets,
  a visual-search task (**58** participants), and **Gaze-on-Faces** (**378**
  participants) — larger-N than most prior work.
- Ablations with a positive impact: optimal **I-VT parameters**, **higher-order
  derivative** features, and a dedicated **blink classifier** — up to **+9%**
  identification accuracy on one dataset. (I-VT parameter sensitivity echoes the
  harness's `VEL_THRESHOLD` tuning caveat.)
- Explicit **template-aging**, age, and gender analyses — the cross-session /
  demographic robustness GazePry needs for RQ4 and D5.
- **Cite the published Signal Processing: Image Communication version**, not the
  arXiv preprint (plan §21).

## Related

- [[george-2016-score-fusion]] — the method it improves and extends.
- [[eye-movement-biometrics]] — the hand-crafted lineage.
- [[unclearability]] — template-aging bears on cross-session survival (RQ4).
- [[gaze-feature-extraction]] — I-VT parameter and blink-feature relevance.

## Mentions in sources

- Plan §18.1 (cross-dataset + template aging), §21 (cite published; preprint
  flag) [35]; protocol §15.1.

## Open questions

- DOI discrepancy: plan §21 [35] prints 10.1016/j.image.2022.**116746**;
  `raw/related-papers.txt` prints …**116804**. Verify from the PDF/publisher.
