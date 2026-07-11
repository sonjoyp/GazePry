---
type: source
tags: [paper, keystroke-biometrics, deep-learning, scale, analogue]
aliases: [Acien et al. 2022, TypeNet]
sources: [acien-2022-typenet]
reviewed: false
updated: 2026-07-11
---

Acien, Morales, Monaco, Vera-Rodriguez, Fierrez — *TypeNet: Deep Learning
Keystroke Biometrics*, **IEEE T-BIOM 2022** — bibliography **[43]**. A
non-gaze precedent that a **commodity behavioral channel remains a viable
identifier at web scale** — supporting the plan's argument that behavioral
biometrics don't collapse as the gallery grows. (`raw/TypeNet...-2022.pdf`)

## Key facts

- LSTM keystroke-biometric authentication in **free-text** at large scale, with
  a moderate number of keystrokes per identity; softmax/contrastive/triplet
  losses; physical vs touchscreen keyboards.
- **Scaling result:** EER stays low with only a **moderate increase in error as
  subjects scale from 100 up to 100,000** (≈2.2%–9.2% EER regimes) — the
  keystroke analogue of the gallery-size curve GazePry needs to hold for gaze.
- Supports contribution/RQ framing: a behavioral channel can identify at
  web-population scale — external evidence the gaze gallery-size axis
  ([[reid-metrics]]) won't collapse the threat.

## Related

- [[person-bound-fingerprint]] — behavioral biometric as a scalable identifier.
- [[reid-metrics]] — the gallery-size scaling curve analogue.
- [[nair-2023-vr-50k]] — the VR-motion counterpart at 50k users.

## Mentions in sources

- Plan §18.4 (keystroke biometrics scaling toward 100k) [43]; protocol §15.4
  [43].
