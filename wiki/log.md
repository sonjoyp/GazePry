# GazePry Wiki — Operation Log

Append-only, most-recent-last. Each entry: timestamp, operation, what changed.

---

## 2026-07-10 — INGEST (initial build)

Bootstrapped the wiki per [[SCHEMA]] from the repository's existing sources.

**Sources ingested (5):**
- `README.md` → [[readme]]
- `GazePry_Information_Leakage_Report.md` → [[information-leakage-report]]
- `GazePry_Direction1_ReID_Study_Protocol.md` → [[direction-1-study-protocol]]
- `prototype/README.md` → [[prototype-readme]]
- prototype code (`server.js`, `reid-core.js`, `gazepry-tracker.js`,
  `analysis/*.py`) → [[prototype-code]]

**Entities created (15):** [[webgazer]], [[webeyetrack]], [[gazepoint]],
[[searchgazer]], [[reid-server]], [[gazepry-tracker]], [[capture-harness]],
[[analysis-pipeline]], [[gaze-feature-extraction]], [[task-suite]], [[eyetell]],
[[gazerevealer]], [[gazebase]], [[target-venues]], [[gazepry]].

**Concepts created (27):** [[drive-by-web-adversary]], [[two-regimes-of-leakage]],
[[leakage-vectors-d1-d6]], [[gaze-re-identification]], [[person-bound-fingerprint]],
[[hardware-grounded-fingerprint]], [[same-origin-policy]], [[unclearability]],
[[survives-de-identification]], [[eye-movement-biometrics]],
[[cross-task-generalization]], [[ceiling-vs-commodity]], [[simultaneous-capture-rig]],
[[reid-protocols]], [[reid-metrics]], [[conditions-matrix]],
[[research-questions-rq1-rq5]], [[gaze-perturbation-defense]],
[[covert-calibration]], [[enabling-conditions]], [[form-factor-analysis]],
[[evidence-summary]], [[third-party-tracking-tag]], [[cross-origin-collector]],
[[gaze-estimation]], [[synthetic-data-results]], [[related-work-direction-1]].

**Infrastructure:** created `raw/` inbox; `wiki/SCHEMA.md`, `wiki/index.md`,
this log.

Page totals: 5 sources, 15 entities, 27 concepts (+ SCHEMA, index, log).

**Deduplication:** removed a stray `sources/project-readme.md` — a duplicate of
[[readme]] with dead links (`direction1-study-protocol`, `gazepry-prototype`)
that did not match the wiki's slugs.

**Open items for the next lint pass:**
- No page is `reviewed: true` yet — a human should verify claims and set the
  flag on load-bearing pages.
- Bibliography entry [38] (JuDo1000) is a reserved placeholder in the source;
  [[gazebase]] notes it as such.

---

## 2026-07-11 — INGEST (repo layer: research plan, prototype merge, corrections)

Triggered by "ingest". Repo-document changes since the initial build, processed
before the `raw/` paper backlog:

**New source:** `GazePry_ReID_Research_Plan.md` (c0329bc) → [[reid-research-plan]].
Merges the report (Part I) + protocol (Parts II–III) into the living blueprint.
Canonical bibliography is now plan §21, [1]–[49], with per-citation
verification/preprint status. Same numbering as the frozen docs — no
renumbering.

**Moves (content identical up to line endings):** the report and protocol left
the repo root for `raw/` (c0329bc); their source pages got frozen banners and
raw/ paths. The earlier `prototype/` → repo-root merge (888735c/9abca6d) had
not been reflected in the bootstrap pages: [[readme]] re-ingested (now front
door + harness manual), [[prototype-readme]] converted to a superseded pointer,
[[prototype-code]] updated to the root layout (adapters, tests, vendoring).

**Corrections applied from plan §21:** George & Routray [31] = EER ≈2.59%
(BioEye 2015 random-stimulus), replacing the withdrawn "≈5.8%, 320 subjects"
([[eye-movement-biometrics]]); EyeTell [27] ≈70% = Android lock-pattern top-5,
not 6-digit PIN ([[eyetell]], [[evidence-summary]]); EKYT [20] EER now always
quoted with its window (≈0.58% @ 60 s → ≈3.66% @ 5 s); JuDo1000 [38] is a real
citation (Makowski 2020, OSF; 150 subjects, 4 sessions ≥1 wk, 1000 Hz) —
[[gazebase]] updated.

**New entities (2):** [[eyegestures]], [[gazecloud]] — tracker arms 4 and 5.
Five-arm facts threaded through [[capture-harness]], [[gazepry-tracker]],
[[reid-server]], [[analysis-pipeline]], [[task-suite]], [[webgazer]],
[[webeyetrack]], [[searchgazer]], [[ceiling-vs-commodity]],
[[conditions-matrix]], [[research-questions-rq1-rq5]],
[[related-work-direction-1]], [[target-venues]], [[gazepry]].

**SCHEMA updates (registry, logged):** current-sources list now reflects the
root layout + raw/; citation convention points at plan §21 as canonical, with
an explicit warning that `raw/related-papers.txt` ([1]–[62], a collection
export) uses numbering that does NOT match project citations.

**Non-paper raw/ files, disposition:** `raw/README.md` = inbox infrastructure
(no page); `raw/related-papers.txt` = bibliography export (no page; SCHEMA
warning instead); `raw/GazePry_*.md` = the frozen moved docs (already
ingested). The ScienceDirect HTML files are web mirrors of two PDFs and will be
logged with their papers.

**Flagged for humans** (Open questions on [[gazepry]], [[readme]],
[[reid-research-plan]], [[gazebase]]): IRB contradiction (plan §10/§20: file
TAMU IRB now, critical path — vs README Caveats: "IRB-exempt"); participant
data policy breach (29 real `data/*.json` session logs are git-tracked, the
`.gitignore` rules are commented out, contradicting CLAUDE.md); README still
links the moved research docs at dead root paths; GazeBaseVR and Al Zaidawi
DOI discrepancies to verify at PDF ingest.

---

## 2026-07-11 — INGEST (raw/ paper backlog: 58 PDFs + 1 web clip)

Swept the entire `raw/` inbox — all 58 PDFs and `www.pygaze.org.html`, none
previously in the log. Extracted text with a scratchpad PyMuPDF venv (the Read
tool's PDF path needs poppler, absent here) and read each. One `sources/` page
per paper (slug = author-year-shortname), grounded in the actual PDF, not the
plan's summary. Grouped by role for the reader — see [[index]].

**Source pages created (59):** 58 paper pages + [[pygaze-site]].
- *Webcam-tracker lineage & validation (15):* [[papoutsaki-2016-webgazer]],
  [[papoutsaki-2017-searchgazer]], [[papoutsaki-2018-eye-of-typer]],
  [[davalos-2025-webeyetrack]], [[hutt-2024-mind-wandering]],
  [[semmelmann-2018-online-webcam-et]], [[yang-2021-webcam-behavioral]],
  [[van-der-cruyssen-2024-validation]], [[kaduk-2024-webcam-vs-eyelink]],
  [[thilderkvist-2024-limitations]], [[falch-2024-webcam-gaze-estimation]],
  [[molina-cantero-2024-review]], [[zhu-2025-gazefollower]], [[park-2021-gazel]],
  [[razuman-2025-browser-extension]].
- *Eye-movement biometrics & datasets (10):* [[holland-2011-scanpath-biometrics]],
  [[kinnunen-2010-task-independent]], [[george-2016-score-fusion]],
  [[jager-2019-deep-eyedentification]], [[makowski-2021-deepeyedentification-live]],
  [[lohr-2022-eye-know-you-too]], [[al-zaidawi-2022-multi-dataset]],
  [[aziz-2026-gaze-offset-fusion]], [[griffith-2021-gazebase]],
  [[lohr-2023-gazebasevr]].
- *Content-dependent attacks (6):* [[chen-2018-eyetell]],
  [[wang-2020-gazerevealer]], [[wang-2024-gazeploit]],
  [[slocum-2023-arvr-keylogging]], [[long-2023-private-eye]],
  [[weinberg-2011-history-sniffing]].
- *VR/XR identification & anonymity (4):* [[nair-2023-vr-50k]],
  [[miller-2020-vr-identifiability]], [[aziz-2025-uncoordinated-protections]],
  [[patergianakis-2026-xr-anonymity]].
- *Gaze privacy defenses (6):* [[steil-2019-gaze-dp]], [[li-2021-kaleido]],
  [[david-john-2022-for-your-eyes-only]], [[david-john-2021-streaming-privacy]],
  [[du-2024-privategaze]], [[wilson-2024-vr-gaze-streaming]].
- *Web tracking & keystroke biometrics (4):* [[acar-2014-web-never-forgets]],
  [[vastel-2018-fp-stalker]], [[zimmeck-2017-cross-device]],
  [[acien-2022-typenet]].
- *Privacy attitudes, HCI & gaze-AI (13):* [[katsini-2020-gaze-security-survey]],
  [[kroger-2020-gaze-privacy]], [[liebling-2014-pervasive-privacy]],
  [[alsakar-2025-handheld-privacy]], [[bozkir-2025-privacy-concerns]],
  [[abdrabou-2025-gaze-to-data]], [[bukhari-2025-privacy-indicators]],
  [[yang-2025-gazellm]], [[pham-2026-gazeqwen]], [[mathew-2026-gazevlm]],
  [[danry-2026-gaze-to-guidance]], [[dmello-2012-gaze-tutor]],
  [[dmello-2012-autotutor]].

**Concepts created (2):** [[webcam-tracking-validation]] (the "accuracy
objection is weakening" argument, tying the four cognitive-science validation
studies), [[gaze-conditioned-ai]] (gaze fed to LLMs/VLMs — why collection is
proliferating).

**Corrections verified against the papers themselves (not just plan §21):**
- **EyeTell [27]** ([[chen-2018-eyetell]]): from the paper's abstract — 4-digit
  PIN top-5 65% / top-50 90%; Android lock-pattern top-5 70.3%; words top-5
  38.43%. Confirms the ≈70% figure is *lock-pattern*, and reveals the old "PIN
  top-1 ≈39%" was a misread of the *word* top-5 (38.43%). [[eyetell]] and
  [[evidence-summary]] now state the resolved numbers.
- **George & Routray [31]** ([[george-2016-score-fusion]]): EER ≈2.59% on
  **153 subjects** (BioEye 2015), template-aging EER ≈10.96% — the old
  "≈5.8%, 320 subjects" fails on both figures.
- **EKYT [20]** ([[lohr-2022-eye-know-you-too]]): 0.58% EER at 60 s → 3.66% at
  5 s on GazeBase (322 subjects) — exact, from the paper's Table I comparison.
- **GazeBaseVR DOI** ([[lohr-2023-gazebasevr]]): the PDF's own DOI is
  **10.1038/s41597-023-02075-5**; plan §21 [37]'s "…02073-7" is a **typo**
  (flagged for a human to fix in the source; wiki cannot edit sources).

**Citation hygiene:** papers in the plan's §21 canonical list are cited by
bracket number; ~11 webcam-validation / lineage papers **not** in §21
([[papoutsaki-2016-webgazer]], [[semmelmann-2018-online-webcam-et]],
[[kaduk-2024-webcam-vs-eyelink]], [[yang-2021-webcam-behavioral]],
[[van-der-cruyssen-2024-validation]], [[thilderkvist-2024-limitations]],
[[falch-2024-webcam-gaze-estimation]], [[molina-cantero-2024-review]],
[[zhu-2025-gazefollower]], [[park-2021-gazel]], [[razuman-2025-browser-extension]],
[[pygaze-site]]) are cited **author-year**, each page saying so, per the SCHEMA
trap note.

**Non-PDF raw handling:** `www.pygaze.org.html` → [[pygaze-site]]. The two
ScienceDirect HTML mirrors once in `raw/` (Gaze-tutor [1], Thilderkvist) were
deleted in commit 9185c26 and are noted as such on the affected pages, not
treated as live sources.

**Lint (post-ingest):** Python sweep over 114 pages — **1041 resolved
`[[links]]`, 0 dead links, 0 orphans** (the only raw matches were SCHEMA's
literal `[[wiki-links]]` examples and `\|`-escaped pipes inside Markdown
tables, both valid).

**Still open for a human** (unchanged from the Phase-1 entry): IRB
exempt-vs-critical-path contradiction; 29 real `data/*.json` participant logs
tracked in git against `CLAUDE.md` policy; README's dead links to the moved
research docs; the GazeBaseVR and Al Zaidawi DOI fixes in the plan source.

---

## 2026-07-11 — INGEST (research-plan reviewer-hardening pass)

Re-ingested `GazePry_ReID_Research_Plan.md` after a reviewer-facing hardening
pass that added **Appendix A** and three surgical corrections. Folded the
changes into the wiki.

**Source updated:** [[reid-research-plan]] — new-material summary now records the
§7/§9/§12 corrections, the §20 next-steps additions, and the Appendix A map.

**Concept created (1):** [[reid-confound-controls]] — the calibration/session
artifact confound (a webcam tracker self-calibrates per session, so a match may
reflect calibration geometry, not the person) and the control battery that rules
it out: calibration-swap, cross-tracker generalization, shuffled-label null,
appearance ablation, lighting/time/device negative controls, within-session
leakage bound. This is Appendix A.3 and the plan's #1 acceptance risk.

**Concept pages updated to match the corrected plan:**
- [[third-party-tracking-tag]] — corrected the web-platform mechanism: provider
  script runs **first-party** on many sites (each with its own camera grant),
  linked **server-side**; camera permission is per-top-level-origin and *not*
  silently shared across origins (a cross-origin iframe needs `Permissions-Policy`
  delegation). The prior "each embedding inherits the host page's camera
  permission" was technically wrong and is now fixed.
- [[cross-origin-collector]] — added the permission-model caveat: what crosses
  the origin boundary is the *linkage* (server-side), not the camera grant.
- [[enabling-conditions]] — added the consent-realism argument (grant is a real
  friction, but gaze-request contexts proliferate: accessibility, proctoring,
  WebXR, gaze-AI) and elevated covert calibration = no explicit step.
- [[simultaneous-capture-rig]] — fixed the same IR-label-contamination language
  the plan corrected ("train/validate the webcam estimate" → Gazepoint is a
  measurement instrument only, never a training signal for re-ID).
- [[ceiling-vs-commodity]] — added the RQ3 anti-contamination control.
- [[eye-movement-biometrics]] — added the route-(b) domain-gap caveat (IR
  250–1000 Hz ↛ webcam ~30 Hz without domain adaptation).
- [[gaze-perturbation-defense]] — for top-tier, treat the defense as
  non-optional + add responsible disclosure (browser vendors / W3C).
- [[target-venues]] — added the venue-tuning guidance (PoPETs first with defense
  included; USENIX/CCS need the cross-origin demo + crisp cross-task number +
  disclosure; SOUPS consent companion).
- [[related-work-direction-1]] — added the "just biometrics on a worse sensor"
  rebuttal and pointer to the Appendix A.9 novelty statement.

**Novelty verdict recorded (Appendix A.1):** no fatal novelty issue — the
intersection {commodity webcam × desktop web × cross-task/cross-site × unclearable
tracking} is unoccupied. The decisive risks are empirical (does webcam cross-task
re-ID beat chance?), threat-model realism (camera consent + cross-origin
mechanics), and confounds ([[reid-confound-controls]]) — not novelty.

**Lint:** re-ran the Python sweep — 0 dead links, 0 orphans across the vault
(now 115 pages; the only raw matches are `\|`-escaped table pipes, which
Obsidian resolves).

---

## 2026-07-13 — INGEST (5 new biometrics papers + research-plan confounds pass)

Triggered by "ingest". Two bodies of new material since the 2026-07-11 passes:
**(A)** five PDFs added to `raw/` (commit c25ac14), and **(B)** a research-plan
update (commit 4c616bb, 2026-07-12) that landed after
[[reid-research-plan]]'s `updated` date. Text extracted with the scratchpad
PyMuPDF venv (Read's PDF path lacks poppler here) and read end-to-end.

**A — Source pages created (5).** All five are **eye-movement biometrics** papers.
At first ingest none was in the plan's §21, so they were written up author-year;
later in this same session they were **added to the plan §21 as [50]–[54]** (see
the "Plan document updated" subsection below), and the pages now cite those
numbers — never their `raw/related-papers.txt` numbers ([63]–[67], a
collection-export index that does not match project citations; SCHEMA trap):
- [[eberz-2016-looks-like-eve]] — *Looks Like Eve* (Oxford, ACM TOPS 2016).
  **Closest external prior art:** cross-task auth (reading/writing/browsing) that
  still works at **50 Hz**, 2-week stable, EER ≈1.0%. Recorded the three
  distinctions that keep GazePry's gap open (downsampled clean IR ≠ native webcam;
  authentication ≠ covert re-ID; workstation ≠ open web).
- [[liao-2022-wayfinding]] — stimulus-independent ID in real-world wayfinding
  (SMI ETG 60 Hz, 39 subjects; 78%/EER 6.3%, leave-one-route-out 64%). The
  real-world analogue of [[cross-task-generalization]].
- [[rigas-2016-saccadic-vigor]] — saccadic vigor + acceleration into CEM-B
  (EyeLink 1000, 322 subjects; final EER ≈11.92%). Vigor sits in a **>75 Hz
  band** → literature support for "which saccade features survive the webcam rate."
- [[li-2018-texture-features]] — GWT scanpath-texture features (Tobii TX300, 58
  subjects; EER ≈0.89% short-term) with **template aging inflating EER
  74–1075%** — a caution for the long-interval cross-session cell.
- [[galdi-2016-critical-survey]] — critical survey; **resolves a standing
  correction**: attributes the "Rank-1 88.6% / EER 5.8% / 320 subjects" figure
  (once misattributed to George & Routray, withdrawn in plan §21) to a **Rigas
  multi-stimulus fusion scheme**. Noted on [[reid-research-plan]] §21 and the
  Galdi/[[rigas-2016-saccadic-vigor]] pages (exact Rigas paper still to pin —
  Open question).

*(The evidence-summary Eberz/Liao rows and the related-work / cross-task mentions
were first written author-year, then renumbered to [50]/[51] in the plan-update
subsection below.)*

**A — Concepts updated (5):** [[eye-movement-biometrics]] (low-rate/cross-task
evidence + vigor/texture feature families), [[evidence-summary]] (added Eberz +
Liao rows, author-year), [[related-work-direction-1]] (Eberz as closest prior
art with the three distinctions; Liao under task-independence),
[[cross-task-generalization]] (Eberz/Liao as external evidence),
[[ceiling-vs-commodity]] (which features die at low rate: Eberz microsaccade
degradation, Rigas >75 Hz band).

**B — Research-plan re-ingest (commit 4c616bb).** Folded the plan's confounds/
empirical-status pass into [[reid-research-plan]] and the affected pages:
- **New concept [[pilot-empirical-status]]** (plan §19a): the "read before quoting
  any number" state — **N=2 pilot**, WebGazer cross-task/cross-session rank-1
  ≈0.75 (chance 0.5), EER ≈0.32, shuffled-null ≈0.50; all sessions same-sitting
  (≥1-week cells empty); a **rate confound** (P01 ≈50 Hz vs P02 ≈110 Hz logged);
  RQ0 unanswered. Linked from [[gazepry]], [[evidence-summary]],
  [[synthetic-data-results]], [[research-questions-rq1-rq5]],
  [[reid-confound-controls]], [[analysis-pipeline]].
- **RQ4 corrected** ([[unclearability]], [[research-questions-rq1-rq5]]): split
  into *(a) web-state clearing* (genuine unclearable point, server-side matching)
  vs *(b) calibration-model clearing* (degrades the sensor, silently re-trains —
  a wipe "buys time, not anonymity"; deliverable = recovery curve). The earlier
  "wipe everything, match still lands" demo description was **wrong** and is fixed.
- **Rate confound / resample** ([[gaze-feature-extraction]], [[analysis-pipeline]],
  [[ceiling-vs-commodity]], [[reid-confound-controls]]): logged rate =
  `requestAnimationFrame` cadence, not true ~30 Hz, and varies by participant →
  confound correlated with identity. New `features.resample`/`reid-core.js
  resample` (JS↔Py parity-tested) + rate-equalized negative control (`reid.py`
  default), plus data-quality guard and returning-visitor `min_gap_days` gate.
- **RQ0 elevated to the gate** ([[reid-confound-controls]],
  [[research-questions-rq1-rq5]]); **modeling status** recorded (16 features +
  diagonal-Mahalanobis NN; learned metric deferred until N supports it).

**Plan document updated ([50]–[54], user-requested).** On request, the five
papers were woven into `GazePry_ReID_Research_Plan.md` itself — the "add a
genuinely new reference to the source document first, then reflect it in the
wiki" flow (SCHEMA). Added **§21 entries [50]–[54]** (Eberz, Liao, Rigas, Li,
Galdi — all peer-reviewed, details verified from the PDFs), continuing the plan's
own numbering (**not** the `related-papers.txt` [63]–[67]). Cited in **§18.1**
(Rigas/Li foundations + Galdi survey), **§18.2** (Eberz as closest prior art with
three distinctions; Liao stimulus-independence), **§18.8** and **A.1** (the gap /
"just a worse sensor" rebuttal), **§9** and **A.5** (Eberz 50 Hz + microsaccade
degradation, Rigas >75 Hz band), and the **§21 [31] verification note** (Galdi
names the Rigas-fusion source of the withdrawn 88.6%/5.8%/320-subject figure).
Re-synced the wiki to the new numbers: [[SCHEMA]] ([1]–[54]; related-papers now
[1]–[67]), the five `sources/` pages, [[eye-movement-biometrics]],
[[evidence-summary]], [[related-work-direction-1]], [[cross-task-generalization]],
[[ceiling-vs-commodity]], [[reid-research-plan]], and [[index]].

**Non-paper raw handling:** `raw/related-papers.txt` grew to [1]–[67] (commit
c25ac14) — still a collection export, still **not** the project numbering (SCHEMA
trap unchanged; no page).

**Lint (post-ingest):** Python sweep over **121 pages — 1309 resolved
`[[links]]`, 0 dead links, 0 orphans**. The only raw regex hits are SCHEMA/log's
literal `[[links]]` examples and `\|`-escaped table pipes (both valid); a second
normalized pass confirmed 0 real dead links.

**Still open for a human** (carried forward): IRB exempt-vs-critical-path
contradiction; participant `data/*.json` logs tracked in git against `CLAUDE.md`
policy (now P01 S1–S3 + P02 S1–S2); README dead links to moved docs; GazeBaseVR
and Al Zaidawi DOI fixes in the plan source; pin the exact Rigas fusion paper
behind the 88.6%/5.8%/320-subject figure.
