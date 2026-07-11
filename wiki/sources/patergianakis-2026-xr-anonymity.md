---
type: source
tags: [paper, identification, extended-reality, eye-movement-biometrics, anonymity]
aliases: [Patergianakis and Lambrinoudakis 2026, Through the looking glass, XR loss of anonymity]
sources: [patergianakis-2026-xr-anonymity]
reviewed: false
updated: 2026-07-11
---

Patergianakis & Lambrinoudakis (University of Piraeus) — *Through the looking
glass: eye tracking biometrics and the loss of anonymity in extended reality*,
**Int. J. Information Security 2026** — bibliography **[42]**. The closest
recent framing GazePry adopts: eye-movement biometrics as an explicit **loss of
anonymity**. (`raw/Through the looking glass...-2026.pdf`)

## Key facts

- Uses the **GazeBaseVR** dataset ([[lohr-2023-gazebasevr]], 400+ users);
  extracts fixation, saccade, Savitzky–Golay velocity, and position/task
  features; a **simple MLP** classifier.
- **96.61% identification** while users watch a **video** in a VR environment —
  a near-perfect re-ID with a *simple* model on a large population.
- Frames the stake as **anonymity loss**, not authentication — the exact stance
  GazePry adopts for its "unclearable identifier" thesis (identity is the
  stake, and it is taken without consent).

## Related

- [[lohr-2023-gazebasevr]] — the dataset it identifies on.
- [[person-bound-fingerprint]] — anonymity-loss framing.
- [[eye-movement-biometrics]] — the signal; note a *simple* MLP suffices at
  scale, tempering the "you need a deep model" assumption.
- [[related-work-direction-1]] — §18.4, the "anonymity is the stake" analogue.

## Mentions in sources

- Plan §18.4 (≈96.6% on GazeBaseVR video-watching; "loss of anonymity"
  framing) [42]; protocol §15.4 [42].
