---
type: source
tags: [paper, web-tracking, fingerprinting, linkage, baseline]
aliases: [Vastel et al. 2018, FP-STALKER, browser fingerprint evolutions]
sources: [vastel-2018-fp-stalker]
reviewed: false
updated: 2026-07-11
---

Vastel, Laperdrix, Rudametkin, Rouvoy (Lille / Inria) — *FP-STALKER: Tracking
Browser Fingerprint Evolutions*, **IEEE S&P 2018** — bibliography **[45]**. The
state-of-the-art **stateless** linkage baseline: link *evolving* browser
fingerprints over time. The comparison gaze is contrasted against — fingerprints
drift and can be reset; gaze is person-bound. (`raw/FP-STALKER...-2018.pdf`)

## Key facts

- Browser fingerprinting is **stateless** (stores nothing on the device) but
  device-bound and **drifts over time**; FP-STALKER links successive
  fingerprints of the same browser despite that drift.
- The key contrast for GazePry's contribution 1: a fingerprint is stateless yet
  (a) tied to a *device/browser* and (b) defeated by anti-fingerprinting
  browsers / a fresh device — whereas gaze dynamics ride with the *person*
  across devices ([[person-bound-fingerprint]], RQ4 [[unclearability]]).

## Related

- [[person-bound-fingerprint]] — device-bound (this) vs person-bound (gaze).
- [[acar-2014-web-never-forgets]], [[zimmeck-2017-cross-device]] — sibling
  baselines.
- [[reid-metrics]] — the clearable/resettable comparison baseline.

## Mentions in sources

- Plan §6 (contribution 1), §14 (baseline), §18.5 [45]; protocol §15.5 [45].
