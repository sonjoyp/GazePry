---
type: source
tags: [paper, privacy, virtual-reality, eye-tracking, motion, defense-limits, preprint]
aliases: [Aziz and Komogortsev 2025, Uncoordinated Privacy Protections Eye Tracking VR Motion]
sources: [aziz-2025-uncoordinated-protections]
reviewed: false
updated: 2026-07-11
---

S. Aziz & Komogortsev (Texas State) — *Exploring the Uncoordinated Privacy
Protections of Eye Tracking and VR Motion Data for Unauthorized User
Identification*, **IEEE VR 2025** (arXiv:2411.12766) — bibliography **[41]**
(**preprint-flagged** in plan §21). Shows that **partial, uncoordinated**
defenses leak: unprotected motion undoes eye-tracking privacy and vice versa.
Scopes GazePry's RQ5 defense. (`raw/Exploring the Uncoordinated Privacy
Protections...-2025.pdf`)

## Key facts

- In VR, obfuscating one modality (e.g. eye tracking) while leaving another
  (body motion) unprotected still permits **user identification** — the two
  channels are correlated.
- Lesson GazePry inherits for [[gaze-perturbation-defense]] (RQ5): a defense
  must be scoped against *all* uncoordinated signals, or a second unprotected
  channel re-enables re-ID.
- Reinforces that person-bound behavioral identity is robust and hard to
  fully suppress — the same robustness the offense side exploits.

## Related

- [[gaze-perturbation-defense]] — RQ5 defense scoping (§16 of the plan cites
  this as the "partial protections can be undone" caveat).
- [[eye-movement-biometrics]] — the eye channel here.
- [[nair-2023-vr-50k]], [[miller-2020-vr-identifiability]] — VR motion identity.

## Mentions in sources

- Plan §16 (defense scoping: partial protections undone) [41], §18.4, §21
  (preprint flag) [41]; protocol §11, §15.4 [41].
