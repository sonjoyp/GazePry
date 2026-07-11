---
type: entity
subtype: tool
tags: [eye-tracking, webcam, deprecated, legacy]
aliases: [SearchGazer, SearchGazer 2016, SearchGazer 2017]
sources: [readme, information-leakage-report, direction-1-study-protocol]
reviewed: false
updated: 2026-07-10
---

**SearchGazer** (Papoutsaki, Laskey, Huang, CHIIR 2017 [4]) is the webcam
eye-tracking-for-web-search library that GazePry originally forked. It
instruments a search-results page to identify in real time which area of
interest a visitor examines — the ancestor of the D2 [[leakage-vectors-d1-d6|
reading/search vector]] and the SERP stimulus in the [[task-suite]]. It is now
**deprecated** within the project.

## Key facts

- The original SearchGazer demo is archived under **`legacy-searchgazer/`**
  (moved off the repo root in the 2026-07-10 merge) for historical reference
  only — deprecated and unused.
- **Stale:** its bundled Google/Bing DOM selectors date from 2016 and no longer
  match live SERPs — so an attacker-controlled page, not live-SERP
  instrumentation, is the realistic demonstrator substrate.
- Superseded by current [[webgazer]] v3.5.3 for all new work.

## Related

- [[webgazer]] — the current engine that replaces it.
- [[task-suite]] — the SERP task inherits SearchGazer's AOI instrumentation.

## Mentions in sources

- `README.md` (Credit — archived demo); Report §2, §4 (dead selectors); plan
  §2, §9 ("do not use the stale fork"; set aside with TurkerGaze), §18.7 [4].
