---
type: entity
subtype: system
tags: [prototype, client, sdk, tracking-tag]
aliases: [gazepry-tracker, gazepry-tracker.js, Tracker SDK, GazePry tag, Orchestrator]
sources: [readme, prototype-code, reid-research-plan]
reviewed: false
updated: 2026-07-11
---

**`public/gazepry-tracker.js`** is the client-side "**third-party analytics
tag**" ([[third-party-tracking-tag]]) — and, since the multi-tracker refactor,
a **tracker-agnostic orchestrator**: it handles identity, the calibration
overlay, capture, the watchdog, and submission, and drives whichever
`public/trackers/*.js` adapter matches the selected tracker. One provider
observing a visitor across different content pages, linking them by gaze — the
structural core of the study — regardless of which gaze engine runs underneath.

## Key facts

- **Adapter registry:** adapters self-register via `GazePry.registerTracker`
  at load; the orchestrator lazily `load()`s only the *selected* tracker's
  heavy library. Contract minimum: `family`, `start()`, `onGaze(cb)` emitting
  `{x, y}` **viewport pixels** (`null` = blink/lost face); optional
  `recordCalibration`, `clearModel`, `pause`/`resume` (watchdog restart),
  `privacy: "local" | "cloud"` (see `public/trackers/README-adapter.md`).
- Logs `{t, x, y}` per frame; `x=null` encodes a blink / lost-face gap — the
  same stream for every adapter, so one feature pipeline serves all arms.
- **Identity** resolution: URL query → `localStorage` (`gp_participant`,
  `gp_session`) → default; the chosen tracker family is stored with the
  session and threaded into the filename.
- `config.server` — empty = same-origin; set to a full URL for the
  [[cross-origin-collector|cross-origin demo]].
- Fresh sessions re-calibrate and clear the prior model (`clearModel`) — an
  honest cross-session test; the wipe-state demo also goes through it.
- WebGazer-specific notes live in its adapter: `saveAcrossSessions` persists
  the regression model across page loads; vendored MediaPipe FaceMesh assets
  resolve relative to the *script* URL (the fix for task pages one level deep
  404ing the WASM/model).
- Fallback: if the server is unreachable it downloads the session JSON for
  manual drop into `data/`.
- RQ5 hook: a [[gaze-perturbation-defense|defense]] would perturb the stream
  here before submit — one place, every tracker.

## Related

- [[reid-server]] — the collector it POSTs to.
- [[webgazer]], [[webeyetrack]], [[eyegestures]], [[gazecloud]] — the adapters
  it drives.
- [[capture-harness]] — the pages it runs inside.

## Mentions in sources

- `public/gazepry-tracker.js`; `public/trackers/README-adapter.md`;
  `README.md` (What's here); plan §9 ("Harness status").
