---
type: concept
tags: [enabling-condition, calibration, webgazer]
aliases: [Covert Calibration, Click Calibration, Self-Calibration]
sources: [information-leakage-report, prototype-code]
reviewed: false
updated: 2026-07-10
---

**Covert calibration** is the [[webgazer]]-class trick that makes drive-by gaze
capture practical: the tracker self-calibrates by correlating ordinary cursor
clicks with gaze, so a page can build a usable gaze model through normal
interaction **without ever presenting a calibration step** [4]. One of the three
[[enabling-conditions]].

## Key facts

- Confirmed present and functional in GazePry's lineage (mouse-event listeners
  feeding the ridge regression).
- In the prototype, [[gazepry-tracker]] runs a short *click* calibration; the
  model persists across page loads (`saveAcrossSessions`), and a new session
  re-calibrates fresh (clearing the prior model) — an honest cross-session test.
- Consequence: no explicit consent moment tied to gaze modeling; the user need
  not know eye-movement analysis is occurring.

## Related

- [[enabling-conditions]] — one of three conditions that make the threat
  practical.
- [[webgazer]] — the tracker whose self-calibration this is.
- [[gazepry-tracker]] — the prototype's calibration flow.

## Mentions in sources

- Report §7 (Covert calibration); Protocol §2 (capability);
  `prototype/public/gazepry-tracker.js`.
