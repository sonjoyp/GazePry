---
type: source
tags: [paper, identification, virtual-reality, motion-biometrics, scale]
aliases: [Nair et al. 2023, Unique Identification of 50000 VR Users, VR 50k]
sources: [nair-2023-vr-50k]
reviewed: false
updated: 2026-07-11
---

Nair, Guo, Mattern, Wang, O'Brien, Rosenberg, Song (UC Berkeley et al.) —
*Unique Identification of 50,000+ Virtual Reality Users from Head & Hand
Motion Data*, **USENIX Security 2023** — bibliography **[39]**. The definitive
"a commodity behavioral signal scales like a strong biometric" result — the
best external evidence that GazePry's **gallery-size axis** will not collapse
the threat. (`raw/Unique Identification of 50,000+...-2023.pdf`)

## Key facts

- Real-world dataset: **55,541 VR users** across 40+ hours of *Beat Saber*
  telemetry (not a lab task).
- **94.33% identification from 100 s** of head + hand motion; **73.20% from
  just 10 s** — accuracy stays high across a >50,000-person gallery.
- The "biomechanics scales like a strong biometric" precedent: analogous to
  gaze dynamics as a [[person-bound-fingerprint]], but in the VR motion
  modality — a *supporting analogy*, not the same setting (GazePry is desktop
  webcam gaze).

## Related

- [[person-bound-fingerprint]] — the scalable-behavioral-identifier framing.
- [[reid-metrics]] — evidence the gallery-size scaling curve stays high.
- [[miller-2020-vr-identifiability]], [[patergianakis-2026-xr-anonymity]] — the
  other VR-scale identification analogues.
- [[related-work-direction-1]] — §18.4, the tracking-vector analogue group.

## Mentions in sources

- Plan §18.4 (55,541 users, ≈94.3% from 100 s) [39]; protocol §15.4 [39].
