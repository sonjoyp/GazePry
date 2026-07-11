---
type: entity
subtype: system
tags: [prototype, frontend, harness]
aliases: [Capture Harness, public/, Task Harness, Harness]
sources: [readme, prototype-code, reid-research-plan]
reviewed: false
updated: 2026-07-11
---

The **capture harness** is the browser front-end under `public/` (repo root
since the 2026-07-10 merge): a consent + identity + **tracker picker** +
calibration hub, five task "sites" that all embed the same
[[gazepry-tracker|orchestrator]], and a live re-ID page. It is
**tracker-agnostic** — one self-registering adapter per webcam tracker, chosen
per session, so the same participant can be recorded on several trackers and
compared (RQ3).

## Key facts

- Files: `index.html` (consent + identity + tracker picker + calibration +
  task hub), `tasks/*.html` (the five [[task-suite]] pages), `reid.html` (live
  re-ID + wipe-state demo), `task-runner.js` (shared boot code), `tracker.css`,
  the [[gazepry-tracker]] orchestrator, `trackers/` (adapters for
  [[webgazer]], [[gazecloud]], [[webeyetrack]], [[eyegestures]]), `lib/`
  (vendored tracker libraries, lazy-loaded per selection), `web/` (WebEyeTrack
  BlazeGaze model), and vendored MediaPipe FaceMesh under `mediapipe/`.
- Must be served over a secure context — use `localhost` (`getUserMedia`
  requires it; a bare LAN IP would need HTTPS).
- Flow: participant/session → **pick a tracker** → consent →
  [[covert-calibration|calibration]] (click grid for click-trained trackers;
  self-calibrating trackers run their own) → five tasks; each finished task
  POSTs `P01_S1_<task>_<tracker>_<ts>.json`.
- Different content per task page stands in for a different "site";
  **cross-task** matching is the real tracking test.
- `reid.html`: *Capture 20 s probe & identify* and *Wipe all browser state*
  (the [[unclearability]] demonstration); matches only against gallery
  sessions from the **same** tracker.

## Related

- [[gazepry-tracker]] — the orchestrator embedded on every page.
- [[task-suite]] — the five task pages.
- [[reid-server]] — where sessions are POSTed.
- [[ceiling-vs-commodity]] — the multi-tracker comparison this design enables.

## Mentions in sources

- `public/` (index.html, tasks/, reid.html, task-runner.js, trackers/, lib/);
  `README.md` (What's here, Quick start, Webcam trackers); plan §9 ("Harness
  status").
