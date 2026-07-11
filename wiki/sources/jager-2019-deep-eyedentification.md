---
type: source
tags: [paper, eye-movement-biometrics, deep-learning, micro-movements]
aliases: [Jäger et al. 2019, Deep Eyedentification]
sources: [jager-2019-deep-eyedentification]
reviewed: false
updated: 2026-07-11
---

Jäger, Makowski, Prasse, Liehr, Seidler, Scheffer (Potsdam) — *Deep
Eyedentification: Biometric Identification Using Micro-movements of the Eye*,
**ECML PKDD 2019** — bibliography **[33]**. Establishes that **involuntary
ocular micro-movements** (not just engineered macro-movement features) identify
people via a deep CNN on the raw signal — a route-(b) ceiling predecessor to
[[lohr-2022-eye-know-you-too|EKYT]]. (`raw/Deep Eyedentification...-2019.pdf`)

## Key facts

- Deep convolutional architecture on the **raw eye-tracking signal**, versus
  prior work's engineered low-frequency macro-movement features.
- **One order of magnitude lower error rate** and **two orders of magnitude
  faster** than prior EMB — "identifies users accurately within seconds," a
  key input to the short-window threat.
- Reinforces the counterfeit-resistance / involuntariness argument (micro-
  movements are driven by oculomotor control below conscious control) — the
  physical grounding behind [[hardware-grounded-fingerprint]].
- Cites the >1000-participant finding that individual eye-movement
  characteristics are reliable and **persist across sessions** — the
  permanence GazePry's [[unclearability]] claim depends on.

## Related

- [[eye-movement-biometrics]] — the deep-model (route b) lineage.
- [[makowski-2021-deepeyedentification-live]] — the binocular + PAD successor.
- [[lohr-2022-eye-know-you-too]] — the DenseNet that surpasses it.

## Mentions in sources

- Plan §12 (route b micro-movement models), §18.1 [33]; protocol §7, §15.1.
