---
type: entity
subtype: system
tags: [prototype, frontend, harness]
aliases: [Capture Harness, public/, Task Harness, Harness]
sources: [prototype-readme, prototype-code]
reviewed: false
updated: 2026-07-10
---

The **capture harness** is the browser front-end under `prototype/public/`: a
consent + identity + calibration hub plus five task "sites" that all embed the
same [[gazepry-tracker|tracking tag]], and a live re-ID page. It is how sessions
are collected for the [[analysis-pipeline]] and the live demo.

## Key facts

- Files: `index.html` (consent + identity + calibration + task hub),
  `tasks/*.html` (the five [[task-suite]] pages: reading, serp, images, video,
  form), `reid.html` (live re-ID + wipe-state demo), `task-runner.js` (shared
  boot code), `tracker.css`, and the [[gazepry-tracker]] SDK. WebGazer's
  MediaPipe FaceMesh runtime is vendored under `mediapipe/face_mesh/`.
- Must be served over a secure context — use `localhost` (`getUserMedia`
  requires it; a bare LAN IP would need HTTPS).
- Flow: enter participant/session → consent → click [[covert-calibration|
  calibration]] → complete five tasks; each finished task POSTs a session JSON.
- Different content per task page stands in for a different "site";
  **cross-task** matching is the real tracking test.
- `reid.html` offers *Capture 20 s probe & identify* and *Wipe all browser
  state* (the [[unclearability]] demonstration).

## Related

- [[gazepry-tracker]] — the SDK embedded on every page.
- [[task-suite]] — the five task pages.
- [[reid-server]] — where sessions are POSTed.

## Mentions in sources

- `prototype/public/` (index.html, tasks/, reid.html, task-runner.js);
  `prototype/README.md` (What's here, Quick start).
