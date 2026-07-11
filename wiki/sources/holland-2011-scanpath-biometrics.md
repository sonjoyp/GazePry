---
type: source
tags: [paper, eye-movement-biometrics, scanpath, reading, foundations]
aliases: [Holland and Komogortsev 2011, scanpath biometrics reading]
sources: [holland-2011-scanpath-biometrics]
reviewed: false
updated: 2026-07-11
---

Holland & Komogortsev (Texas State) — *Biometric Identification via Eye
Movement Scanpaths in Reading*, **IJCB 2011** — bibliography **[30]**. The
origin of the hand-crafted eye-movement feature family GazePry's route (a)
uses: fixation/saccade statistics plus the "main sequence" relationship. Grounds
[[eye-movement-biometrics]] and the [[gaze-feature-extraction]] feature set.
(`raw/Biometric identification via eye movement scanpaths in reading...-2011.pdf`)

## Key facts

- Biometric candidates enumerated here → the harness's 16-feature vector:
  fixation count, average fixation duration, saccade amplitudes, saccade
  velocities and **peak velocities**, scanpath length/area, regions of
  interest, scanpath inflections, the amplitude–duration and **main-sequence**
  relationships, pairwise fixation distances.
- Argues eye movements are **counterfeit-resistant** (complex neurological +
  extraocular-muscle generation) — the "hardware-grounded" intuition GazePry
  formalizes as a [[hardware-grounded-fingerprint]] / [[person-bound-fingerprint]].
- Information-fusion method combining the metrics → EER **≈27%** with limited
  testing (an early, weak result; later work drives EER far lower — see
  [[george-2016-score-fusion]], [[lohr-2022-eye-know-you-too]]).

## Related

- [[eye-movement-biometrics]] — the field this helped found.
- [[gaze-feature-extraction]] — the feature set descends from this list.
- [[george-2016-score-fusion]], [[lohr-2022-eye-know-you-too]] — the lineage
  that lowers the EER.
- [[related-work-direction-1]] — §18.1 cites [30] as the feature-family origin.

## Mentions in sources

- Plan §12 (fixation/saccade + main-sequence features), §18.1 [30]; report §3.2.
