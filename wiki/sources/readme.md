---
type: source
tags: [overview, entry-point]
aliases: [README, Repo README, Project README]
sources: [readme]
reviewed: false
updated: 2026-07-10
---

The repository's front-door document. Frames [[gazepry]] as a security/privacy
research project on **information leakage from webcam-based eye tracking**, and
points to the three substantive deliverables: the [[information-leakage-report]],
the [[direction-1-study-protocol]], and the working [[prototype-readme|prototype]].

## Key facts

- Threat framing: a [[drive-by-web-adversary]] — a first- or third-party script
  that obtains camera access and runs [[gaze-estimation]] client-side on
  commodity laptops/desktops, no special hardware.
- Lineage: builds on the [[webgazer]] / [[searchgazer]] line but reframes it as
  a threat model. The repo root still holds the original **SearchGazer
  (2016/2017)** demo files (`searchgazer.js`, `index.html`, `examples/`) for
  historical reference; those are **out of date** (dead 2016 SERP selectors).
  New work uses current [[webgazer]] v3.5.3, bundled in the prototype.
- Quick start (two paths):
  - `cd prototype && node server.js` → `http://localhost:8080` (capture harness
    + live re-ID demo).
  - `cd prototype/analysis && python simulate.py --out ../data_sim && python
    reid.py --data ../data_sim --plot ../data_sim/cmc.png` (verify the analysis
    pipeline with no webcam).
- License: **GPLv3** (`LICENSE.md` / `gplv3.md`). Engine credit: [[webgazer]]
  by the Brown HCI Group; instrumentation derives from [[searchgazer]]
  (Papoutsaki, Laskey, Huang, CHIIR 2017 [4]).

## Related

- [[information-leakage-report]] — the broad threat-model survey the README
  lists first.
- [[direction-1-study-protocol]] — the lead research direction.
- [[prototype-readme]] — the runnable artifact.

## Mentions in sources

- `README.md` — entire file (Contents, Quick start, Credit & license).
