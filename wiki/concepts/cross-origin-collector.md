---
type: concept
tags: [tracking, demo, cross-origin, prototype]
aliases: [Cross-Origin Collector, Cross-Origin Demo, Two-Server Demo]
sources: [prototype-readme, prototype-code]
reviewed: false
updated: 2026-07-10
---

The **cross-origin collector** demo makes the [[third-party-tracking-tag|
cross-origin linkage]] literal: run the task pages on one origin and the
tracking collector on another, and show it re-identify across them with **no
cookie and no shared storage**.

## Key facts

- Recipe:
  ```bash
  node server.js --port 8080                 # site A (task pages)
  node server.js --port 9090 --data ./data   # the tracking collector
  ```
  In a task page set `GazePry.config.server = "http://localhost:9090"` before
  capture.
- The [[reid-server|collector]] is CORS-enabled (`Access-Control-Allow-Origin:
  *`), so it receives sessions from any origin and re-identifies across them.
- Demonstrates [[unclearability]] at the origin boundary: linkage without any
  client-side state that clearing could remove.
- Supports RQ4 (unclearability) from the [[research-questions-rq1-rq5|RQ mapping]].
- **Permission-model caveat (plan §7 / Appendix A.4):** what crosses the origin
  boundary here is the *linkage* (server-side), **not** the camera grant. Each
  site obtains its own camera permission for its first-party
  [[third-party-tracking-tag|tag]]; the demo deliberately does not rely on a
  cross-origin iframe silently inheriting the camera (the platform forbids
  that). Keep the demo's framing to "same provider, server-side linkage," which
  is the realistic threat.

## Related

- [[third-party-tracking-tag]] — the model this makes literal.
- [[reid-server]] — the CORS-enabled collector.
- [[unclearability]] — the property demonstrated.

## Mentions in sources

- `prototype/README.md` (Cross-origin / third-party-tag demonstration);
  `prototype/server.js` (CORS); `prototype/public/gazepry-tracker.js`
  (config.server).
