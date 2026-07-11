---
type: source
tags: [paper, webcam-eye-tracking, browser-extension, accessibility, webgazer]
aliases: [Razuman et al. 2025, Webcam Eye-Tracking Browser Extension]
sources: [razuman-2025-browser-extension]
reviewed: false
updated: 2026-07-11
---

Razuman, Mabala, Maulana (MSU-IIT) — *Webcam Eye-Tracking Browser Extension For
General Navigation*, **Procedia Computer Science 2025**. A **WebGazer.js**
browser extension for hands-free navigation — a concrete example of webcam gaze
running as a general-purpose browser component. *Not in plan §21 — cite
author-year.* (`raw/Webcam Eye-Tracking Browser Extension...-2025.pdf`)

## Key facts

- Built on **webgazer.js** plus four webcam-optimized web apps; accessibility
  tool for users with hand disabilities.
- User testing showed declining error rates over time (learning).
- Relevance to GazePry: demonstrates the deployment reality that a webcam
  gaze tracker can be a **browser extension running across arbitrary sites** —
  structurally the same "one tracker, many pages" position as the
  [[third-party-tracking-tag]], but benign here.

## Related

- [[webgazer]] — the library it wraps.
- [[third-party-tracking-tag]] — the same cross-site embedding structure,
  weaponized in GazePry's threat model.
- [[gaze-estimation]] — commodity webcam capability.

## Mentions in sources

- Context for browser-embedded webcam gaze. Not enumerated in plan §21.
