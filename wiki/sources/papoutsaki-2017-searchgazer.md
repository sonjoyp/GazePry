---
type: source
tags: [paper, webcam-eye-tracking, web-search, serp]
aliases: [SearchGazer paper, Papoutsaki et al. 2017, SearchGazer CHIIR 2017]
sources: [papoutsaki-2017-searchgazer]
reviewed: false
updated: 2026-07-11
---

Papoutsaki, Laskey, Huang — *SearchGazer: Webcam Eye Tracking for Remote
Studies of Web Search*, **CHIIR 2017** — bibliography **[4]**. The paper behind
the [[searchgazer]] library GazePry originally forked: [[webgazer]] extended
with a layer that maps predicted gaze onto **SERP DOM elements** (results,
snippets, ads) in real time — the origin of the D2 reading/search-intent
vector in [[leakage-vectors-d1-d6]] and of the [[task-suite]] SERP task.
(`raw/SearchGazer Webcam Eye Tracking...-2017.pdf`)

## Key facts

- Same engine as [[papoutsaki-2016-webgazer|WebGazer]]: clmtrackr eye
  detection, 120-D eye-patch feature, ridge regression (λ=1e-5), cursor
  samples valid ≤200 ms; plus a mapping from gaze coordinates to page AOIs
  via the DOM.
- Reported accuracy (carried from the WebGazer studies): mean error
  **128.9 px ≈ 4.17° ≈ 1.6 in** — coarse, but AOI-level attribution works.
- **Validation by replication**, remotely on Mechanical Turk: reproduced
  Cutrell & Guan's result-examination study (top-to-bottom scan, golden
  triangle; fixation-duration power-law exponent 0.79 vs original 0.72,
  ≈5% normalized difference), Buscher et al.'s ad-examination study
  (coarse patterns replicate, subtle ad-quality effects **missed**;
  ≈24–29% fixation-impact differences), and a ViewSer restricted-focus study.
- Take-away GazePry inherits: webcam gaze is good enough for **which element
  a user examines**, not for fine fixation analysis — and it runs in anyone's
  browser with no equipment.
- Privacy framing (2017): click history and model stay in the browser; only
  predictions leave. Again the on-device argument the re-ID thesis undercuts.
- For crowdworkers the authors added an *explicit* 5×3 click-grid calibration
  — the same grid pattern the harness's [[covert-calibration|calibration]]
  overlay uses.

## Related

- [[searchgazer]] — the tool entity (now archived in `legacy-searchgazer/`;
  its 2016-era SERP selectors are dead).
- [[papoutsaki-2016-webgazer]] — the engine paper this extends.
- [[papoutsaki-2018-eye-of-typer]] — the same group's typing benchmark.
- [[task-suite]] — the SERP task descends from this instrumentation.

## Mentions in sources

- Plan §2, §3.1 [4] (SearchGazer identifies which SERP AOI a visitor
  examines, in real time), §11, §18.7; report §2, §4 (D2).
