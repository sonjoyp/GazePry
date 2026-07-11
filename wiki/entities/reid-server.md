---
type: entity
subtype: system
tags: [prototype, backend, node]
aliases: [reid-server, server.js, Collection Server, Re-ID Server]
sources: [readme, prototype-code]
reviewed: false
updated: 2026-07-11
---

**`server.js`** (repo root) is the harness's zero-dependency Node server: it
serves the [[capture-harness]], ingests captured sessions to `data/`, and
exposes a live nearest-neighbour [[gaze-re-identification|re-identification]]
endpoint that links a probe to an enrolled participant by gaze dynamics alone —
no cookie.

## Key facts

- Run: `node server.js [--port 8080] [--data ./data]` (or `npm start`) →
  `http://localhost:8080`.
- Endpoints:
  - `POST /ingest` — validate + store a session as
    `<participant>_<session>_<task>_<tracker>_<ts>.json` (the filename carries
    the **tracker family**; legacy records without one get their family
    inferred). 400 on bad input.
  - `GET /status?participant=&session=` — tasks already completed, scoped by
    tracker.
  - `GET /sessions` — gallery metadata for the demo UI.
  - `POST /identify` — extract probe features via [[gaze-feature-extraction]],
    rank enrolled participants, return `rank1` + top-5 `ranked`; **never
    matches across trackers**.
- **Permissive CORS** (`Access-Control-Allow-Origin: *`) so a cross-origin task
  page can POST to this collector — the literal cross-origin tracking demo.
- Feature cache keyed by filename + mtime; static file serving is path-jailed
  to `public/`.
- Body cap 60 MB; uses [[gaze-feature-extraction|reid-core.js]] for features
  and matching.

## Related

- [[gaze-feature-extraction]] — the `reid-core.js` module it calls.
- [[gazepry-tracker]] — the client that POSTs to `/ingest` and `/identify`.
- [[cross-origin-collector]] — the two-server cross-origin linkage recipe.

## Mentions in sources

- `server.js`; `README.md` (Quick start, Cross-origin demonstration, Tests);
  `test/server.test.js` (endpoint regression coverage).
