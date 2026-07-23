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

---

## 2026-07-16 — INGEST (Direction 2 blueprint + 12 reading/search/cursor papers)

Triggered by a user request to (a) write a full D2 — *reading content & search
intent* — direction and (b) "always update the wiki based on the new relevant
papers." D2 was previously only a row in [[leakage-vectors-d1-d6]]; it is now a
developed direction. The user's brief: webcam **eye-tracking + mouse-tracking**
that leaks **non-gaze-biometric** information — satisfied by D2 (payload =
content/intent, not identity) with the mouse promoted to a first-class channel.

**New source doc:** `GazePry_D2_Reading_Search_Intent_Direction.md` (repo root) →
[[d2-reading-search-intent-direction]]. *"No Clicks, No Privacy"* — first-party,
within-site reconstruction of considered-but-unclicked / zero-click / re-read
intent from webcam gaze + permission-free cursor; **surveillance surplus** over
the clickstream; **cursor floor vs gaze ceiling** (the D2 analogue of
[[ceiling-vs-commodity]]). Confronts the two D2 killers head-on: the same-origin
objection ([[same-origin-policy]] — scoped within-site, no cross-site claim) and
webcam coarseness ([[thilderkvist-2024-limitations]] — coarse-AOI only).

**New paper source pages (12).** Retrieved and bibliographically **verified via web
search 2026-07-16** (venue/DOI/pages/authors); each page is grounded in the
retrieved **abstract/metadata, not a full-PDF read** (flagged on the page — a
deep-read pass is the follow-up). These fill the **mouse-cursor + search-behavior
gap** the project bibliography entirely lacked. Cited **author-year** per the
SCHEMA trap (not in plan §21); the D2 doc's local labels **G/B/A/Q/R** are
doc-local, *not* shared numbering:
- *Cursor-as-gaze-proxy (G):* [[guo-2010-gaze-from-cursor]] [G1],
  [[huang-2011-no-clicks-no-problem]] [G2] (the paper D2 inverts),
  [[huang-2012-gaze-cursor-alignment]] [G3] (alignment strongest on SERPs),
  [[leiva-2020-attentive-cursor]] [G4], [[latifzadeh-2025-serp-mouse-eye]] [G5]
  (**preprint** — simultaneous mouse+eye SERP dataset).
- *Reading/relevance (B, R):* [[buscher-2008-implicit-relevance]] [B1],
  [[buscher-2012-attentive-documents]] [B2], [[rayner-1998-reading-eye-movements]]
  [R1].
- *Zero-click / good abandonment (A):* [[li-2009-good-abandonment]] [A1],
  [[williams-2016-good-abandonment]] [A2] (**DOL to verify**).
- *Query-log / web-search privacy (Q):* [[jones-2007-query-log-privacy]] [Q1],
  [[gervais-2014-web-search-privacy]] [Q2] (CCS '14 — the top-venue precedent;
  **author list to verify**).

**New concepts (2):** [[reading-search-intent-leakage]] (vector D2 as a direction:
examination-surplus, zero-click intent, extends query-log privacy, RQ0 saliency-
prior gate) and [[cursor-tracking]] (permission-free mouse-as-gaze-proxy; distinct
from [[covert-calibration]], which uses clicks only to train the regression).

**Bidirectional links added** to [[leakage-vectors-d1-d6]] (D2 row now links the
direction; new "D2 is a developed direction" note + Related), [[two-regimes-of-leakage]]
(content-dependent regime hosts a real within-site threat), [[searchgazer]] (its
benign AOI tool is what D2 weaponizes), [[task-suite]] (SERP = D2 headline surface;
needs zero-click variants + first-class cursor logging), [[gaze-feature-extraction]]
(D2 adds a separate AOI-anchored cursor extractor — content-*anchored*, vs D4's
content-*independent* 16-D). [[index]] updated (new source doc, a "Reading,
search-behavior & cursor tracking (D2)" paper group, a "reading/search-intent
thesis (Direction 2)" concept block).

**Citation-convention decision (SCHEMA-compliant):** the 12 papers are **not**
added to the canonical plan §21 numbering — that shared-bib merge is a flagged
next step (D2 doc §12 step 6) requiring a source-doc edit the user has not asked
for. Until then, wiki cites them author-year, exactly as the ~11 non-§21
webcam-validation papers are handled.

**Lint (post-ingest):** Python sweep over **136 pages — 1509 `[[links]]`, 0 real
dead links, 0 orphaned new pages**. The sweep first caught **2 genuine bugs** — a
`[[reading-search-intent-leakage]]` link split across a line break in
[[jones-2007-query-log-privacy]] and [[li-2009-good-abandonment]] (Obsidian won't
resolve a newline inside a link) — both **fixed**, then re-verified clean. Remaining
regex hits are the known `\|`-escaped table pipes (Obsidian-valid).

**Open for a human / next passes:** (1) deep-read the 12 PDFs to deepen each source
page beyond the abstract (Open questions flag the specifics — e.g. Guo & Agichtein's
cursor feature set, the datasets' licensing); (2) verify the [A2] Williams DOI and
[Q2] Gervais author list against the ACM DL; (3) if D2 advances, **merge G/B/A/Q/R
into plan §21** as new shared-bib numbers ([55]–…), then re-sync the wiki (the
[50]–[54] flow). Prior open items unchanged.

## [2026-07-22] ingest + note | Direction D7 — recognition & concealed-knowledge leakage

**Trigger.** User asked for a **non-biometric** gaze-leakage direction on the webcam
harness that is practical and publishable, and asked that any new papers be ingested
and a note filed.

**Outcome: a new vector, D7.** `GazePry_D7_Recognition_Knowledge_Direction.md`
(*"The Recognition Oracle"*) — a first-party page renders an adversary-chosen tile
array and reads **which items the visitor has seen before** from dwell asymmetry and
fixation timing. The payload is **memory contents**: not a biometric
([[gaze-re-identification]], D4), not present-tense intent
([[reading-search-intent-leakage]], D2), not a demographic attribute (D5). D7 is
**appended to** [[leakage-vectors-d1-d6]] (the report defines only D1–D6) and is the
project's **third** developed direction, alongside D4 and D2. Tense is the taxonomy:
D4 = who you are, D2 = what you are doing now, D7 = what you already knew.

**Why D7 over the other non-biometric options.** D1 is ruled out by
[[thilderkvist-2024-limitations]] (sub-degree pointing on packed AOIs) and is already
owned by [[eyetell]] / [[gazerevealer]]; D3 is largely done by
[[hutt-2024-mind-wandering]] [22]; D5 is derivative of
[[alsakar-2025-handheld-privacy]] [10] and needs large N. The decisive argument is
methodological: **D7 structurally cancels the confound that gates D4**
([[reid-confound-controls]], [[pilot-empirical-status]]) because the effect is a
within-participant, within-trial contrast **between AOIs on the same screen**, with
item-level counterbalancing making saliency and position orthogonal to the contrast.
N ≈ 40 in one session, versus D4's N ≥ 50 with ≥1-week separation.

**New paper source pages (9).** Retrieved and bibliographically **verified via web
lookup 2026-07-22** (authors/venue/volume/DOI); each page is grounded in **publisher
metadata or PMC full text, not a full-PDF read** (flagged on every page — a deep-read
pass is the follow-up, D7 §12 step 2). Cited **author-year** per the SCHEMA trap (not
in plan §21); the doc-local labels **M/C/W/P** are *not* shared numbering:
- *Mechanism (M):* [[althoff-1999-eye-movement-memory-effect]] [M1] (effect within
  the first five fixations), [[hannula-2010-worth-a-glance]] [M2] (no conscious
  recollection required), [[shimojo-2003-gaze-cascade]] [M3] (gaze cascade; a
  possible preference-probe variant).
- *Ocular CIT (C):* [[schwedes-2012-revealing-glance]] [C1] (fixation duration
  reveals memory regardless of intent; 65% of relevant trials),
  [[nahari-2019-concealed-familiarity]] [C2] (n=61, four-face arrays; task demands
  decide suppressibility), [[millen-2019-concealed-face-recognition]] [C3] (AUC
  0.67–0.87; fixation duration **strengthens** under countermeasures, d 0.66→0.91,
  while the spatial signal collapses, d 1.40→−0.12),
  [[rosenzweig-2020-mock-terror]] [C4] (88%/AUC 0.84 — **an IR ceiling via
  microsaccades at RSVP rates, not webcam-reachable**),
  [[zangrossi-2024-aiat-eye-movements]] [C5] (75% from the eye measure alone on
  week-old memories).
- *Privacy (P):* [[et-privacy-decade-review-2025]] [P1] — **⚠ AUTHOR LIST
  UNVERIFIED**, ACM DL returned 403; page is a flagged placeholder and the D7 §3 gap
  claim must not rest on it.

**Source page deepened (1).** [[van-der-cruyssen-2024-validation]] — promoted from a
general accuracy datum to **D7's feasibility keystone**. Full verified citation added
(*Behavior Research Methods* 56(5), 4836–4849, 2024, doi 10.3758/s13428-023-02221-2,
seven authors), plus the fact that one of its three replicated effects **is** the
recognition signal (novelty preference, n=45, effect sizes shrinking 20–27%) and its
working stimulus geometry (472 × 331 px, 295 px apart), which now pins D7 §6.2. Also
recorded: the author overlap with [C2] (Ben-Shakhar, Pertzov) plus Verschuere — the
**scoop risk** in D7 §10.

**New concepts (3):** [[recognition-knowledge-leakage]] (the D7 direction — the
interventional/adversary-chosen distinction, the covert-vs-forensic inversion, the
structural confound cancellation), [[eye-movement-memory-effect]] (the involuntary
mechanism, including the **sign/window instability** hazard), and
[[ocular-concealed-information-test]] (the instrument, its performance scale, and why
countermeasures — its binding limitation — do not apply on the open web).

**Bidirectional links added** to [[leakage-vectors-d1-d6]] (D7 row, the "why a new
row" rationale, the tense framing, codebase status, Related),
[[webcam-tracking-validation]] (the novelty-preference replication is D7's direct
feasibility evidence), [[thilderkvist-2024-limitations]] (D7 takes *both* halves — the
I-DT algorithm becomes a hard requirement, the accuracy verdict caps AOI granularity),
and [[task-suite]] (a **sixth** task page: the trial-structured, adversary-designed
probe array). [[index]] updated with the new source doc, a "Memory, recognition & the
ocular CIT (Direction 7)" paper group, a "recognition thesis (Direction 7)" concept
block, and a new **Notes** section.

**Correction recorded.** [C3] Millen & Hancock was initially attributed in session to
*Scientific Reports*; it is *Cognitive Research: Principles and Implications* 4(23),
doi 10.1186/s41235-019-0169-0. Note [C2] and [C3] share journal and volume with
adjacent DOIs (0162-7 / 0169-0) — an easy pair to confuse. Logged on the page and in
D7 §11.

**Citation-convention decision (SCHEMA-compliant).** The 10 papers are **not** added
to the canonical plan §21 numbering; that merge is deferred to after the E1 pilot (D7
§12 step 7), mirroring both the [50]–[54] flow and the D2 doc's identical deferral.
Until then the wiki cites them author-year.

**Note filed.** `notes/2026-07-22-d7-recognition-direction.md` — the decision record:
options weighed, evidence gathered, the confound argument, the four risks, and the
next action.

**Open for a human / next passes:** (1) verify **[C6]** Lancry-Dayan 2018, **[C7]**
Van der Cruyssen 2024 CIT-leakage, **[P1]** the decade privacy review, and **[W5]** the
Collabra five-paradigm replication — [C7] and [P1] change how D7 §3 and §10 are
written; (2) deep-read [C1]–[C5] for effect directions, scoring windows, and
per-measure AUCs before pre-registration; (3) build the probe-array page + I-DT
detector, then run E1 at N ≈ 12 asking only *does RQ0 clear?*; (4) the D4 §20 step 8
data-hygiene blocker (29 participant sessions tracked in git) must be resolved before
any D7 collection. Prior open items unchanged.

---

## [2026-07-22] note | Building the D7 probe: four things the design document did not anticipate

**Filed** `notes/2026-07-22-d7-instrumentation-findings.md`, the follow-on to
[[2026-07-22-d7-recognition-direction]]. That note recorded the *decision*; this one
records what building the collection and analysis pipeline changed about it. Four
findings, each of which would otherwise have produced a plausible-looking number that
meant nothing:

1. **The lab I-DT threshold does not transfer.** At webcam noise a 0.045-diagonal
   dispersion window segments **zero** fixations, flattening every fixation feature to
   a constant — which scores AUC 0.500, so the pipeline reports "no effect" rather
   than "the segmenter did not run". Now 0.10 diagonals with 5-sample smoothing, plus
   a *fixations per trial* diagnostic. Refines [[thilderkvist-2024-limitations]]: the
   I-DT *algorithm* is required, but its parameters are sensor-specific.
2. **LOPO folds break the saliency control.** The RQ0 baseline read 0.101, which looks
   like broken counterbalancing; it is the held-out participant's group being
   under-represented by one, with consistent sign across folds. Group-balancing the
   training folds moved it to 0.488. A below-chance control is fold structure, not a
   broken design.
3. **The RQ0 gate was verified by sabotage.** With counterbalancing deliberately
   flattened, the headline reads **AUC 0.935** off item identity alone while the
   saliency control hits 1.000 and RQ0 FAILs. The gate catches exactly what it exists
   for. Null data (0.525, FAIL) and effect data (0.918, PASS) behave correctly.
4. **E1 stimuli were near-duplicates, and the check could not see it.** Minimum
   pairwise difference 1.3; the distinctiveness test compared *greyscale* thumbnails,
   passing pairs that differed only in hue. Colour comparison and a ≥ 22 rejection
   threshold give 34.14, recorded in the manifest.

**Concept page updated.** [[recognition-knowledge-leakage]] gains an *Instrumentation
constraints* section and its status moves from "proposal only" to "instrumented, not
yet run" — the pipeline exists and passes its nulls, but **no human D7 data has been
collected** and every number above is synthetic.

**Verification:** `npm test` 147 pass / 0 fail (71 JS + 76 Python); `npm run
d7:verify` effect PASS + null FAIL as designed; `npm run d7:stimuli:check` 3 sets,
56 items, all present. JS↔Python parity asserted by three tests.

**Open for a human / next passes:** (1) the data-hygiene blocker is now **44** tracked
participant sessions and is the one thing gating collection — untracking is a git-index
operation, a history scrub is a separate destructive decision; (2) real E2/E3 assets
are not installed, so only E1 can be run; (3) the four unverified citations from the
prior note are unchanged; (4) run the E1 pilot at N ≈ 12 asking only *does RQ0 clear on
real eyes?*. Prior open items otherwise unchanged.

## [2026-07-23] note | D7 made standalone, and E2 stimuli sourced for real

Filed [[2026-07-23-d7-standalone-and-e2-stimuli]] from a session that did two jobs:
made `GazePry_D7_Recognition_Knowledge_Direction.md` independent of the other two
direction plans, and closed the E2 stimulus gap the 2026-07-22 note left open.

**Wiki-affecting change first.** The D7 document now carries its **own** bibliography,
renumbered **[1]–[30] local to that file**, which does *not* match the shared project
numbering. The collisions are silent: [5] is Weinberg (history sniffing) in the shared
scheme but Nahari et al. 2019 in D7; [6] is Liebling & Preibusch there and Millen &
Hancock here; Weinberg is [16] in D7. Recorded as **Trap 2** in [[SCHEMA]]'s citation
convention, alongside the existing `raw/related-papers.txt` trap. Wiki pages keep the
shared numbering; D7 claims resolve by author-year.

**What changed in the direction.**

1. **E2 is collectable.** 24 real items in three classes of eight — public figures,
   retail bank wordmarks, widely photographed places — each class spanning universal
   to niche recognition. All fetched and hash-verified from Wikimedia Commons under
   free licences (the eight bank wordmarks all public domain as plain wordmarks).
2. **Arrays are class-homogeneous**, a protocol change made on both the JS and Python
   sides in one commit. A mixed array would let the probe be identified by *category*
   rather than by familiarity. This exposed a non-obvious invariant: the counterbalance
   square runs over the **global** item index, so a class must be a contiguous block
   sized a multiple of `N_GROUPS`, or a group cannot fill an array — and it fails
   *mid-session*, not at startup. Now checked and tested on both sides.
3. **E3 stays blocked, and the reason changed.** The prior note treated E2 and E3 as
   symmetric ("both need real assets"). They are not: E1/E2 rest on the participant
   having seen *that stimulus*, which is what the [[eye-movement-memory-effect]]
   predicts, while a topic card carries only *semantic* familiarity. E2's gap was
   closable by sourcing; E3's is not. §5 of the note supersedes that framing.
4. **Two dead ends worth not repeating.** Wikipedia lead images resolve well for people
   (12/12) and places (14/14) but return **headquarters buildings** for banks; Commons
   free-text search for topic photographs returns digitised books, not images.
5. **A gotcha:** MediaWiki snaps `iiurlwidth` to standard buckets (720 and 900 both
   returned 960), which broke the logo letterbox until the fit was done against what
   arrived rather than what was requested.
6. **Provenance is machine-enforced**: licence allow-list that refuses rather than
   downloads, a lock file pinning resolved file + SHA-256 per asset, and generated
   attribution. Two cohorts months apart provably saw the same stimuli, or it surfaces.
7. **An ethics-scoping bug, fixed.** E3 shipped `t_imm` ("Visa paperwork") while both
   the plan and the stimulus README exclude immigration status as a protected
   characteristic. The scoping test asserts the *category* vocabulary, and `t_imm` was
   categorised `legal`, so it passed. Replaced with `t_claims`.

**Pages updated.** [[recognition-knowledge-leakage]] — status moves to "instrumented
and stimulus-complete for E1/E2"; gains the class-homogeneity control, the
contiguous-block invariant, the E2/E3 construct asymmetry, and cohort-level
familiarity as the top threat to the headline. Its D2/D4 comparison is kept but now
labelled as the *wiki's* synthesis, since the document no longer carries it.
[[d7-recognition-knowledge-direction]] — standalone status, E2 composition, the local
citation numbering, and the now-void plan-§21 merge item. [[SCHEMA]] — Trap 2.

**Verification:** `npm test` **162 pass / 0 fail** (74 JS + 88 Python), up from 147;
`npm run d7:verify` effect PASS + null FAIL as designed; `npm run d7:stimuli:check`
3 sets, 64 items, 1 expected warning; `npm run d7:stimuli:verify` 24 locked assets
present and unmodified.

**Open for a human / next passes:** (1) the data-hygiene blocker is **unchanged** —
still 44 tracked participant sessions, still the one thing gating collection; (2) E3
unsourced by choice; (3) the four unverified citations are still unverified, now
numbered [9], [10], [15], [17] in D7's local scheme; (4) every D7 number remains
synthetic — the E1 pilot at N ≈ 12 still asks only *does RQ0 clear on real eyes?*;
(5) noticed outside D7's scope: `README.md`'s header links to
`GazePry_Direction1_ReID_Study_Protocol.md` and `GazePry_Information_Leakage_Report.md`
at the repo root, but both live in `raw/`, so the links are dead.
