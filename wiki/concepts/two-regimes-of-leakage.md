---
type: concept
tags: [threat-model, leakage, taxonomy, core]
aliases: [Two Regimes, Two Regimes of Leakage, Content-Dependent, Content-Independent]
sources: [information-leakage-report]
reviewed: false
updated: 2026-07-10
---

Gaze leakage splits into **two regimes** with different prerequisites,
defenses, and form-factor behavior. This split organizes the whole project: the
[[leakage-vectors-d1-d6]], the [[form-factor-analysis]], and the choice of
[[gaze-re-identification|re-identification]] (content-independent) as
Direction 1 all follow from it.

## Key facts

- **Content-dependent** — the adversary controls or knows the on-screen layout
  and maps gaze coordinates onto it to recover what the user interacts with
  (PINs on a known keypad, reading/search AOIs). Depends on a known layout, so
  an attacker-controlled page is the natural delivery vehicle. Vectors D1–D2.
- **Content-independent** — the adversary needs to know nothing about the
  screen; the *dynamics* of eye movement (fixation durations, saccade
  velocities/amplitudes, blinks, pupil) carry information about the person.
  Leaks cognitive/affective state, stable traits, and identity. Vectors D3–D5.
- **Why it matters for Direction 1:** [[same-origin-policy]] blocks
  content-dependent cross-site peeking but **not** content-independent re-ID —
  so the cross-site threat is re-identification, not reading another site.
- The content-independent regime is "the more dangerous one for privacy because
  it cannot be defeated by changing what the page displays."

## Related

- [[leakage-vectors-d1-d6]] — the six vectors, mapped to these two regimes.
- [[gaze-re-identification]] — the content-independent vector Direction 1 uses.
- [[reading-search-intent-leakage]] — the **content-dependent** vector (D2)
  developed as a direction: it shows the content-dependent regime still hosts a
  real threat *within a site* (first-party, zero-click intent) even though
  [[same-origin-policy]] blocks it cross-site.
- [[survives-de-identification]] — a property specific to the content-independent
  regime.

## Mentions in sources

- Report §3 (Two Regimes of Gaze-Based Information Leakage), §3.1, §3.2.
