---
type: concept
tags: [threat-model, form-factor, devices]
aliases: [Form-Factor Analysis, Laptop, Desktop, Smartphone, Tablet, Device Classes]
sources: [information-leakage-report]
reviewed: false
updated: 2026-07-10
---

The leakage profile differs by device class even though the underlying gaze
signal is the same physical phenomenon. The report analyzes three:
**laptop/desktop**, **smartphone**, **tablet**.

## Key facts

- **Laptop / desktop — the primary novel surface.** Fixed distance, stable head
  pose, large screen → most favorable for content-dependent inference; in-browser
  trackers run with no install. **Least characterized as a security threat** →
  the project's strongest contribution angle. [[webgazer]] drifts ≈5→10 cm over
  20 min; [[webeyetrack]] closes much of the gap (≈2.32 cm), so the accuracy
  objection is *weakening* over time.
- **Smartphone — the best-evidenced surface.** Concrete attacks exist:
  [[eyetell]], [[gazerevealer]]; handheld privacy leakage well developed [10].
  The gaze-coordinate channel is the weak link, so the **camera-permission grant
  itself becomes the dominant leakage vector** — content-independent signal
  (identity, demographics, state) survives poor pointing accuracy.
- **Tablet — the least-studied surface.** Inherits the smartphone touchscreen
  threat with a larger display; assessment is an interpolation between
  well-evidenced phone results and desktop in-browser tooling. A sensible second
  device precisely because it is under-measured.

## Related

- [[two-regimes-of-leakage]] — the regime that dominates flips by form factor.
- [[eyetell]], [[gazerevealer]] — the mobile content-dependent attacks.
- [[drive-by-web-adversary]] — the desktop in-browser case the project targets.

## Mentions in sources

- Report §5 (Form-Factor Analysis), §5.1–§5.3.
