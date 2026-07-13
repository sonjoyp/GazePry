---
type: source
tags: [eye-movement-biometrics, continuous-authentication, cross-task, low-sampling-rate, insider-threat, closest-prior-art]
aliases: [Eberz et al. 2016, Looks Like Eve, Insider Threats Eye Movement Biometrics, 50 Hz eye movement authentication]
sources: [eberz-2016-looks-like-eve]
reviewed: false
updated: 2026-07-13
---

Eberz, Rasmussen, Lenders & Martinovic (Oxford + Armasuisse) — *Looks Like Eve:
Exposing Insider Threats Using Eye Movement Biometrics*, **ACM Trans. Privacy &
Security 2016**. Ingested 2026-07-13; **added to the plan §21 as [50]** the same day —
cite **[50]**, *not* its `raw/related-papers.txt` index [64] (a different
numbering; see [[SCHEMA]]). **The closest external prior art to GazePry's central
claim**: it demonstrates
eye-movement biometrics that are (i) **cross-task** across everyday activities and
(ii) still work **at 50 Hz** consumer-rate. GazePry must position carefully
against it — see the three distinctions below. (`raw/Looks Like Eve Exposing
Insider Threats Using Eye Movement Biometrics-Eberz et al.-2016.pdf`)

## Key facts

- **Threat model:** continuous authentication as a second line of defense against
  the insider "lunchtime attack" (someone using an unlocked co-worker's
  workstation). **20 features**; open-set classifier.
- **Apparatus & cohorts:** high-end **Tobii at 500 Hz**, **30 subjects** (general
  public), two sessions **2 weeks apart** for time stability; a **second dataset
  of 10 subjects** for real-world tasks.
- **Headline accuracy:** single-session open-set **EER 1.00%**. In a
  never-reject-legitimate-users setting, the system detects an attacker in a
  **median 33.5 s** and catches **84.56%** of attackers.
- **Cross-task (the load-bearing result for GazePry):** a second dataset of
  **reading, writing, browsing (a Wikipedia game), and video** yields error rates
  **comparable to the artificial task set** — reliable authentication across
  everyday tasks. This is direct evidence that
  [[cross-task-generalization|cross-task]] eye-movement recognition is feasible.
- **Low sampling rate:** downsampling the 500 Hz data to 250 / 100 / **50 Hz**
  (the rate "commonly available with consumer-level devices") still supports
  reliable authentication; most of the loss happens by ~250 Hz and further
  reduction adds little. **But** features tied to **microsaccades degrade the most
  (statistically significant, p<0.05)** — the same class of high-frequency saccade
  detail GazePry expects to lose at ~30 Hz.
- **Task-knowledge does not help an impostor:** an adversary who knows the user's
  normal task cannot meaningfully improve impersonation.
- Uses **Relative Mutual Information (RMI)** to rank feature informativeness and
  quantify degradation.

## Three distinctions GazePry must state (why this is not the same paper)

1. **Downsampled clean IR ≠ native webcam.** Eberz *decimates* a clean 500 Hz
   Tobii signal to 50 Hz; a commodity webcam is **natively ~30 Hz with
   categorically different noise** and self-calibration error. "50 Hz works" is
   encouraging, not equivalent — the [[ceiling-vs-commodity]] gap is exactly this.
2. **Authentication ≠ covert re-identification.** Eberz verifies a **cooperating,
   enrolled** user (1:1, with consent) as a security *defense*; GazePry does
   **unconsented cross-site re-ID** (1:N tracking) as an *attack*
   ([[gaze-re-identification]], [[person-bound-fingerprint]]).
3. **Workstation ≠ open web.** No browser, no [[same-origin-policy]], no
   cross-site / [[unclearability|unclearable]] framing — the tracking-vector
   contribution is untouched.

## Related

- [[cross-task-generalization]] — Eberz's reading/writing/browsing result is the
  strongest external evidence cross-task works.
- [[ceiling-vs-commodity]] — the 50 Hz result and microsaccade degradation frame
  the webcam-rate discussion; downsampled-clean vs native-noisy is the caveat.
- [[eye-movement-biometrics]] — a low-rate, cross-task data point in the lineage.
- [[related-work-direction-1]] — position here as closest prior art, then invoke
  the three distinctions to preserve the gap.
- [[kinnunen-2010-task-independent]], [[liao-2022-wayfinding]] — the other
  cross-task / stimulus-independent anchors.

## Mentions in sources

- Plan **[50]**, cited in **§18.2** (closest prior art, with the three
  distinctions), **§18.8** (the gap), **§9** and **A.5** (50 Hz / microsaccade
  degradation), and **A.1** (the "just biometrics on a worse sensor" rebuttal).
  Added to §21 on 2026-07-13.
