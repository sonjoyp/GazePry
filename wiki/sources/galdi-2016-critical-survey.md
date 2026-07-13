---
type: source
tags: [eye-movement-biometrics, survey, evaluation-standards, provenance]
aliases: [Galdi et al. 2016, Eye movement analysis for human authentication critical survey, GANT survey, gaze authentication survey]
sources: [galdi-2016-critical-survey]
reviewed: false
updated: 2026-07-13
---

Galdi, Nappi, Riccio & Wechsler (EURECOM / Salerno / Napoli / George Mason) —
*Eye movement analysis for human authentication: a critical survey*, **Pattern
Recognition Letters 2016**. Ingested 2026-07-13; **added to the plan §21 as [54]** the same
day — cite **[54]**, *not* its `raw/related-papers.txt` index [65] (a different
numbering; see [[SCHEMA]]). A survey of gaze-for-authentication methods that (a) critiques the
field's lack of standards / uncontrolled-setting problem, relevant to GazePry's
in-the-wild threat model, and (b) **independently resolves a provenance question
the plan flagged** — see below. (`raw/Eye movement analysis for human
authentication a critical survey-Galdi et al.-2016.pdf`)

## Key facts

- **Scope:** surveys stimulus / eye-tracker / gaze-descriptor design, then
  comparatively re-evaluates three graph-based techniques (**Rigas et al., GAS,
  GANT**) on one common, larger dataset — arguing that cross-paper comparison is
  otherwise meaningless (different databases, no shared protocol).
- **Standards critique:** the field lacks common databases and evaluation
  protocols; performance under **uncontrolled settings** (remote trackers, and
  even a plain **webcam**) is the open hard case — the exact regime GazePry
  operates in (weak commodity sensor, real conditions).
- **Provenance resolution (the useful bit).** The plan's §21 withdrew an
  "EER ≈5.8%, 320 subjects" figure once misattributed to
  [[george-2016-score-fusion|George & Routray]]. Galdi attributes exactly
  *"Rank-1 IR 88.6%, EER 5.8%, 320 subjects"* to **a Rigas et al. multi-stimulus,
  multi-biometric fusion scheme** (jumping-point-of-light + text + video, weighted
  fusion) — a sibling of [[rigas-2016-saccadic-vigor]]. So the number is real but
  belongs to a **Rigas fusion paper, not George & Routray**; the plan's
  correction stands and this survey names the true source family.
- Recommends richer, task-dependent stimuli and profiles, and points beyond
  authentication to medical, marketing, and privacy applications.

## Related

- [[eye-movement-biometrics]] — survey-level map of the biometric signal.
- [[rigas-2016-saccadic-vigor]] — the Rigas lineage Galdi credits with the
  88.6%/5.8%/320-subject fusion result.
- [[george-2016-score-fusion]] / [[reid-research-plan]] — the §21 correction this
  survey corroborates (the number was never George & Routray's).
- [[ceiling-vs-commodity]] — the "uncontrolled settings / webcam" hard case the
  survey flags is GazePry's home turf.

## Mentions in sources

- Plan **[54]**, cited in **§18.1** (survey / uncontrolled-settings critique) and
  the **§21 [31] verification note** (names the Rigas-fusion source of the
  withdrawn 88.6%/5.8%/320-subject figure). Added to §21 on 2026-07-13.

## Open questions

- Galdi cites the fusion result via its own reference numbering; pin the **exact
  Rigas fusion paper** (year/venue) before putting the corrected attribution in
  the related-work draft, so the citation is to the primary source, not the
  survey.
