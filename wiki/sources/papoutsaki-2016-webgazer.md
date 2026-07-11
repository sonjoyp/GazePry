---
type: source
tags: [paper, webcam-eye-tracking, browser, self-calibration]
aliases: [WebGazer paper, Papoutsaki et al. 2016, WebGazer IJCAI 2016]
sources: [papoutsaki-2016-webgazer]
reviewed: false
updated: 2026-07-11
---

Papoutsaki, Sangkloy, Laskey, Daskalova, Huang, Hays — *WebGazer: Scalable
Webcam Eye Tracking Using User Interactions*, **IJCAI 2016** (Brown / Georgia
Tech). The founding paper of the [[webgazer]] tracker and the origin of the
[[covert-calibration]] mechanism GazePry's threat model leans on:
self-calibration from ordinary clicks and cursor movements, no explicit
calibration step. *Not in the plan's §21 bibliography — cite author-year.*
(`raw/Webgazer scalable webcam eye tracking...-2016.pdf`)

## Key facts

- **Method:** browser-JS only. Eye patch per eye → 6×10 grayscale,
  histogram-equalized → 120-D feature → **ridge regression** to screen
  coordinates (λ=1e-5, following TurkerGaze). Pluggable face/eye detectors
  (clmtrackr, js-objectdetect, tracking.js). No 3-D head-pose reasoning — the
  weakness [[webeyetrack]] later fixes.
- **Self-calibration assumption:** gaze ≈ cursor at click moments (prior work:
  gaze–cursor distance averages ≈74 px at click). Variants: RR+F adds samples
  from a 500 ms fixation buffer (≤72 px); **RR+C** weights recent cursor
  positions (weight 0.5, decaying 0.05/20 ms → ≈200 ms lifetime).
- **Accuracy (online study, N=82 recruited / 76 analyzed, 20,251 clicks):**
  simple linear 256.9 px; RR 232.4 px; **RR+C best, 174.9 px** mean error
  (best library+model ≈104–130 px). In-lab vs Tobii EyeX (N=4): RR+C 169 px,
  ≈**4.17° visual angle**. Quiz-task error *grows* with scrolling/movement —
  the drift the harness's caveats echo.
- **Privacy stance (2016):** opt-in camera permission; "local processing is a
  critical requirement — otherwise users risk sending private information out
  of their control." GazePry's thesis is precisely that on-device processing
  does **not** neutralize the identity leak — the features themselves are the
  [[person-bound-fingerprint]].
- Predecessors compared: TurkerGaze (offline, explicit calibration; source of
  the RR formulation), PACE (desktop app, ≈2.56° after hundreds of
  interactions).

## Related

- [[webgazer]] — the tool this paper introduced (v3.5.3 is the harness arm).
- [[covert-calibration]] — the click/cursor self-calibration this paper
  invented, reframed by GazePry as an attack enabler.
- [[papoutsaki-2017-searchgazer]] — the follow-up that instrumented SERPs.
- [[gaze-estimation]] — the capability class this democratized.

## Mentions in sources

- Cited unnumbered in report §1/§5 and plan §2, §5 ("WebGazer and its
  derivatives"); the harness vendors its v3.5.3 build.
