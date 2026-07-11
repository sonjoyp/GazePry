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
[[webgazer]]/[[searchgazer]] eye-tracking lineage as a *threat model*. The
project has three deliverables: the [[information-leakage-report]] (survey), the
[[direction-1-study-protocol]] (lead research plan), and a working
[[prototype-readme|prototype]].

## Key facts

- Repository: `github.com/sonjoyp/GazePry`, licensed **GPLv3**.
- Lead direction (Direction 1): [[gaze-re-identification|cross-site gaze
  re-identification]] as an unclearable web-tracking vector.
- Root still contains the deprecated **SearchGazer (2016/2017)** demo for
  historical reference; active work lives under `prototype/` on [[webgazer]]
  v3.5.3.
- IRB status per protocol: human-subjects; TAMU IRB filing is the critical
  path. Prototype README notes the analysis pipeline is IRB-exempt and `data/`
  is git-ignored (never commit raw participant gaze).

## Related

- [[information-leakage-report]], [[direction-1-study-protocol]],
  [[prototype-readme]] — the three deliverables.
- [[drive-by-web-adversary]] — the threat model that distinguishes GazePry from
  prior gaze-privacy work.

## Mentions in sources

- `README.md`; both report/protocol titles; `prototype/README.md`.
