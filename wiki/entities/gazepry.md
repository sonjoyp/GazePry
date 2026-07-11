---
type: entity
subtype: system
tags: [project, security, privacy, eye-tracking]
aliases: [GazePry, GazePry Project]
sources: [readme, information-leakage-report, direction-1-study-protocol]
reviewed: false
updated: 2026-07-10
---

**GazePry** is a security/privacy research project studying what a
[[drive-by-web-adversary]] can infer about a user from commodity, in-browser
webcam [[gaze-estimation]] — no special hardware. It reframes the
[[webgazer]]/[[searchgazer]] eye-tracking lineage as a *threat model*. Since
2026-07-11 the project has two living deliverables: the consolidated
[[reid-research-plan]] (which merged the [[information-leakage-report]] and the
[[direction-1-study-protocol]], both now frozen in `raw/`) and the runnable
multi-tracker harness documented in [[readme]].

## Key facts

- Repository: `github.com/sonjoyp/GazePry`, licensed **GPLv3**.
- Lead direction: [[gaze-re-identification|cross-site gaze re-identification]]
  as an unclearable web-tracking vector (vector D4).
- Active code lives at the **repo root** (post 2026-07-10 merge): a
  tracker-agnostic [[capture-harness]] with four webcam arms ([[webgazer]]
  v3.5.3, [[webeyetrack]], [[eyegestures]], [[gazecloud]]) plus the
  [[gazepoint]] IR ceiling. The deprecated SearchGazer demo is archived in
  `legacy-searchgazer/`.
- Institution context: TAMU (the plan's IRB gate is a TAMU protocol).

## Related

- [[reid-research-plan]] — the living blueprint (thesis, apparatus, metrics,
  bibliography §21).
- [[information-leakage-report]], [[direction-1-study-protocol]] — the frozen
  predecessor documents.
- [[drive-by-web-adversary]] — the threat model that distinguishes GazePry from
  prior gaze-privacy work.

## Mentions in sources

- `README.md`; `GazePry_ReID_Research_Plan.md`; the frozen docs in `raw/`.

## Open questions

- **IRB status is contradicted across sources:** plan §10/§20 say filing the
  TAMU IRB is the critical-path gate; `README.md` Caveats say "this project is
  IRB-exempt". A human should reconcile.
- **Participant-data policy vs repo state:** `CLAUDE.md` says never commit raw
  participant gaze data, but `.gitignore`'s `data/*.json` rule is commented
  out and real `P01` session logs are tracked in git (README Caveats admit
  this). Needs a human decision; the wiki must not reproduce that data either
  way.
