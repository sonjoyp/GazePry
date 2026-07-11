---
type: entity
subtype: system
tags: [prototype, client, sdk, tracking-tag]
aliases: [gazepry-tracker, gazepry-tracker.js, Tracker SDK, GazePry tag]
sources: [prototype-readme, prototype-code]
reviewed: false
updated: 2026-07-10
---

**`gazepry-tracker.js`** is the prototype's client-side "**third-party analytics
tag**" ([[third-party-tracking-tag]]): a single script embedded in every task
page that boots [[webgazer]], runs a click [[covert-calibration|calibration]],
logs the raw per-frame gaze stream, and POSTs the session to the
[[reid-server]]. One provider observing a visitor across different content
pages, linking them by gaze — the structural core of the study.

## Key facts

- Requires `webgazer.js` loaded first (`window.webgazer`); `TRACKER_ID =
  "webgazer-3.5.3"`.
- Logs `{t, x, y}` per frame; `x=null` encodes a blink / lost-face gap.
- **Identity** from URL query or `localStorage` (`gp_participant`,
  `gp_session`).
- `config.server` — empty = same-origin; set to a full URL for the
  [[cross-origin-collector|cross-origin demo]].
- `saveAcrossSessions` persists the WebGazer regression model across page loads
  (one calibration on the hub carries to every task page); a new session
  re-calibrates with `{fresh:true}`, clearing the prior model — an honest
  cross-session test.
- **FaceMesh asset fix:** resolves vendored MediaPipe assets relative to the
  *script* URL, not the page. Without it, task pages one level deep 404 the
  WASM/model, the prediction loop dies, and capture yields 0 samples.
- Fallback: if the server is unreachable it downloads the session JSON for
  manual drop into `data/`.

## Related

- [[reid-server]] — the collector it POSTs to.
- [[webgazer]] — the engine it boots.
- [[capture-harness]] — the pages it runs inside.
- [[gaze-perturbation-defense]] — RQ5 would perturb the stream here before
  submit.

## Mentions in sources

- `prototype/public/gazepry-tracker.js`; `prototype/README.md` (What's here).
