---
type: concept
tags: [threat-model, evidence, literature]
aliases: [Evidence Summary, Evidence Table, Quantitative Findings]
sources: [information-leakage-report, reid-research-plan]
reviewed: false
updated: 2026-07-13
---

The consolidated quantitative evidence from the literature that grounds the
[[leakage-vectors-d1-d6]]. Two cautions: the biometric EER is a research-grade
*upper bound* (good eye tracker, not a webcam), and keystroke-inference
accuracies were obtained under controlled capture (feasibility/order-of-magnitude,
not in-the-wild guarantees). Numbers below incorporate the
[[reid-research-plan]] §21 verification corrections. The Eberz [50] and Liao [51]
rows are eye-movement-biometrics ceilings added to plan §21 on 2026-07-13 (cite by
those numbers, **not** their `raw/related-papers.txt` indices [64]/[63]; see
[[SCHEMA]]).

## Key facts

| Finding | Device & channel | Result | Src |
|---|---|---|---|
| [[eyetell\|EyeTell]] PIN/keystroke inference | touchscreen; camera video of face | 4-digit PIN top-5 65%, top-50 90%; Android lock-pattern top-5 70.3%; words top-5 38.4% | [27] |
| [[gazerevealer\|GazeRevealer]] password inference | smartphone front camera | single digit ≈77.9%; 6-digit ≈84.4% (ideal) | [8] |
| Handheld gaze privacy leakage (N=35) | smartphone front camera | ≈65.5% of private attributes inferable; DP cuts leakage ≈10–28% | [10] |
| Eye-movement biometrics (Eye Know You Too) | research IR, reading (upper bound) | EER ≈0.58% at a 60 s window → ≈3.66% at 5 s | [20] |
| [[eberz-2016-looks-like-eve\|Eberz "Looks Like Eve"]] cross-task auth | Tobii 500 Hz **downsampled to 50 Hz**; reading/writing/browsing | EER ≈1.0% single-session; cross-task error ≈ fixed-task; still reliable at 50 Hz | [50] |
| [[liao-2022-wayfinding\|Liao]] stimulus-independent, real-world | SMI ETG glasses 60 Hz, outdoor wayfinding | identification 78% (EER 6.3%); leave-one-route-out 64% (EER 12.1%) | [51] |
| Mind-wandering & comprehension-error detection | browser webcam | above-chance | [22] |
| [[webgazer\|WebGazer]] accuracy drift | laptop webcam, in-browser | ≈5 cm → ≈10 cm over 20 min | [7], [25] |
| [[webeyetrack\|WebEyeTrack]] | browser; laptop & phone | ≈2.32 cm; ≈2× WebGazer; real-time on iPhone | [25] |

## Related

- [[leakage-vectors-d1-d6]] — the vectors these numbers support.
- [[eye-movement-biometrics]] — context for the EER upper bound.
- [[ceiling-vs-commodity]] — the webcam drift vs IR ceiling gap; where the Eberz
  50 Hz result and its microsaccade-degradation caveat land.

## Mentions in sources

- Report §6 (Evidence Summary); plan §3, §21 (verification notes);
  [[chen-2018-eyetell]], [[wang-2020-gazerevealer]] (papers).
