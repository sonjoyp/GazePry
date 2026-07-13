---
type: source
tags: [eye-movement-biometrics, saccades, main-sequence, foundations, komogortsev-lineage]
aliases: [Rigas et al. 2016, Saccadic Vigor and Acceleration Cues, Rigas Komogortsev Shadmehr 2016, CEM-B saccadic dynamics]
sources: [rigas-2016-saccadic-vigor]
reviewed: false
updated: 2026-07-13
---

Rigas, Komogortsev & Shadmehr (Texas State + Johns Hopkins) — *Biometric
Recognition via Eye Movements: Saccadic Vigor and Acceleration Cues*, **ACM
Trans. Applied Perception 2016**. Ingested 2026-07-13; **added to the plan §21 as
[52]** the same day — cite **[52]**, *not* its `raw/related-papers.txt` index [66]
(a different numbering; see [[SCHEMA]]). Adds
*dynamic* saccade features (saccadic vigor + acceleration) to the CEM-B
framework, the same Komogortsev lineage as [[gazebase]] and
[[lohr-2022-eye-know-you-too|EKYT]]. Load-bearing for GazePry because the
features it exploits are exactly the ones a ~30 Hz webcam **cannot** capture —
see [[ceiling-vs-commodity]]. (`raw/Biometric Recognition via Eye Movements
Saccadic Vigor and Acceleration Cues-Rigas et al.-2016.pdf`)

## Key facts

- **Apparatus & data:** SR Research **EyeLink 1000 at 1000 Hz**, **322 subjects** —
  a large, high-rate IR ceiling. Three stimulus types: **random dot, text,
  video**, so improvements are shown to be stimulus-robust.
- **Saccadic vigor** = the individual's idiosyncratic peak-velocity-vs-amplitude
  ("main sequence") relationship; acceleration cues add the accel/decel profile.
  Motivated by Choi et al. 2014 (vigor correlates with impulsivity /
  decision-making), i.e. a neuro-individual trait. These are the
  `main_seq_slope`-family features of [[gaze-feature-extraction]], measured at
  their native ceiling.
- **Result:** integrating both new feature types (condition C4) into CEM-B gives
  a final **EER ≈11.92%** and **Rank-1 IR ≈55.56%**; the new dynamic features
  yield a **relative improvement of 31.6–33.5% (verification)** and **22.3–53.1%
  (identification)** over the CEM-B baseline.
- **Sampling-rate relevance (the GazePry hook):** the paper notes that at 1000 Hz
  the achieved velocity-signal −3 dB cutoff is **>75 Hz** — i.e. the vigor /
  acceleration information lives in a band a commodity webcam (~30 Hz true rate)
  cannot resolve. This is direct literature support for "report *which*
  saccade-velocity features survive the webcam rate" ([[ceiling-vs-commodity]]).

## Related

- [[eye-movement-biometrics]] — the main-sequence / saccade-dynamics signal, here
  at its IR ceiling.
- [[ceiling-vs-commodity]] — the high-Hz saccade features that degrade toward the
  webcam rate; Rigas quantifies the >75 Hz band they occupy.
- [[gaze-feature-extraction]] — `main_seq_slope` and saccade-velocity features
  are the commodity echo of these cues.
- [[gazebase]], [[lohr-2022-eye-know-you-too]] — same Komogortsev CEM lineage.
- [[galdi-2016-critical-survey]] — attributes the "88.6% Rank-1 / 5.8% EER / 320
  subjects" figure to a Rigas multi-stimulus *fusion* scheme (a sibling of this
  work), resolving the number the plan withdrew from George & Routray.

## Mentions in sources

- Plan **[52]**, cited in **§18.1** (biometrics foundations), **§18.8** (the gap),
  **§9** and **A.5** (the >75 Hz vigor band / which features survive low rate).
  Added to §21 on 2026-07-13.
