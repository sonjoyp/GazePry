# GazePry — Direction D2: Reading Content & Search-Intent Leakage

**"No Clicks, No Privacy": Reconstructing Latent Reading and Search Intent from
Commodity Webcam Gaze and Permission-Free Cursor Tracking**

*A research-direction blueprint for a reputable security/privacy (or HCI-privacy)
conference submission. This document develops the **D2** leakage vector from the GazePry
taxonomy — "reading content & search intent" — into a self-contained, publishable plan,
with the eye-tracking **and** mouse-tracking fusion the project asked for and a bibliography
that fills the mouse/search-behavior gap the existing plan does not cover.*

*Companion to, not a replacement for, [`GazePry_ReID_Research_Plan.md`](GazePry_ReID_Research_Plan.md)
(the D4 re-identification plan). D2 leaks **what you are doing and thinking about**; D4 leaks
**who you are**. They share an adversary, a harness, and a confound-control discipline, and
they **compose** (§8). Every load-bearing claim is attributed; §11 records the peer-reviewed /
preprint status of each source and which are **new** to the project bibliography.*

---

## Contents

1. [One-paragraph thesis](#1-one-paragraph-thesis)
2. [Why D2, and how this differs from D4](#2-why-d2-and-how-this-differs-from-d4)
3. [The research gap (the part that makes it publishable)](#3-the-research-gap-the-part-that-makes-it-publishable)
4. [Threat model](#4-threat-model)
5. [Research questions and hypotheses](#5-research-questions-and-hypotheses)
6. [Apparatus, stimuli, and ground truth](#6-apparatus-stimuli-and-ground-truth)
7. [Features, models, and metrics](#7-features-models-and-metrics)
8. [Composition with D4, and the defense](#8-composition-with-d4-and-the-defense)
9. [Related work and the exact gap this fills](#9-related-work-and-the-exact-gap-this-fills)
10. [Risks, honest limitations, and the reviewer traps](#10-risks-honest-limitations-and-the-reviewer-traps)
11. [References and citation status](#11-references-and-citation-status)
12. [Immediate next steps](#12-immediate-next-steps)

---

## 1. One-paragraph thesis

A content or search site that embeds a first-party gaze/cursor analytics tag can reconstruct a
visitor's **latent information interest and intent** — the results, products, and passages the
visitor *seriously considered, re-read, or answered their need from* **without ever clicking or
typing** — at a granularity the clickstream cannot reach. The "examination" layer of Web
browsing has always been private in practice because it leaves no click trail; commodity webcam
gaze (à la SearchGazer [4], WebGazer [14]) and, crucially, **permission-free mouse-cursor
tracking** (a proven Web-scale proxy for gaze on search-results pages — Guo & Agichtein 2010
[G1]; Huang, White & Dumais 2011 [G2]; Huang, White & Buscher 2012 [G3]) turn that layer into a
logged, profilable signal. **The contribution is to reframe a decade of "cursor/gaze as an
implicit-feedback tool for better ranking" as a privacy attack, and to quantify the
*surveillance surplus* of the examination channel over the click/query baseline — separating the
permission-free cursor *floor* from the camera-gated gaze *ceiling* on the same users and the
same pages.** The harm is concrete: it recovers the health symptom you researched and rejected,
the political or legal reading you did without clicking, and the answer you read straight off the
results page (a *zero-click* / good-abandonment search — now the majority of searches [A1], [A2])
— considerations the user reasonably believed left no trace, and the cursor half needs **no
camera permission and shows no indicator**.

---

## 2. Why D2, and how this differs from D4

The GazePry taxonomy (`wiki/concepts/leakage-vectors-d1-d6.md`) places D2 — *reading content &
search intent* — in the **content-dependent** regime, and the D4 plan deliberately set D2 aside
in favor of content-independent re-identification (D4) for one reason: **content-dependent
attacks are blocked cross-site by the same-origin policy** (D4 plan §5). That reasoning is
correct and this direction does **not** try to overturn it. Instead it accepts the constraint
and finds the threat that lives *inside* it:

| | **D4 (existing plan)** | **D2 (this document)** |
|---|---|---|
| What leaks | Persistent **identity** (who you are) | **Interest / intent / content** (what you are doing) |
| Regime | Content-**independent** dynamics | Content-**dependent**, first-party layout |
| Cross-site? | Yes — survives same-origin | **No** — scoped to the embedding site (§4) |
| Biometric? | Yes (gaze biometric) | **No** — the leaked signal is not a biometric |
| Adversary needs | A camera grant | **Nothing** for the cursor floor; a camera grant for the gaze ceiling |
| Novelty axis | Sensor × setting × transfer × unclearability | **Examination-surplus over clicks × permission-free cursor floor × zero-click intent recovery** |

The user's brief — *"webcam eye-tracking **and** mouse-tracking that leaks some
**non-gaze-biometric** information"* — is satisfied exactly by D2: the leaked payload is
content/intent (non-biometric), and the mouse is not a calibration afterthought (as it is in the
WebGazer lineage, where clicks merely train the regression — see `wiki/concepts/covert-calibration.md`)
but a **first-class, permission-free examination channel** fused with gaze.

---

## 3. The research gap (the part that makes it publishable)

Three literatures each touch this space and each stops one step short of the privacy attack:

1. **Cursor/gaze as an implicit-feedback *tool*.** A mature IR line shows the mouse cursor is a
   usable, Web-scale proxy for gaze on search-results pages, and that examination behavior
   predicts relevance and result quality — Guo & Agichtein 2010 [G1] (predicting gaze from
   cursor), Huang, White & Dumais 2011 [G2] ("No clicks, no problem" — cursor reveals examination
   at scale where gaze cannot), Huang, White & Buscher 2012 [G3] (gaze–cursor alignment is
   *strongest on SERPs*), the Attentive-Cursor dataset [G4], and a 2025 public dataset of
   *simultaneous mouse and eye* movements on Google SERPs [G5]. **All of this is framed for the
   search engine's benefit** — better ranking, better metrics. None reframes it as a covert
   examination-surveillance channel or measures how much *private* intent it exposes.

2. **Eye movements as reading/relevance feedback.** Buscher, Dengel & van Elst 2008 [B1] and the
   *Attentive Documents* line [B2] recover, from gaze, which paragraphs a reader found relevant,
   at sub-document granularity — again as an assistive/IR tool. Rayner 1998 [R1] is the reading
   eye-movement foundation. **The leakage reframing — "what within the content mattered to you,
   recovered without your knowledge" — is absent.**

3. **Query-log privacy.** Jones et al. 2007 [Q1] ("I know what you did last summer") and Gervais
   et al. 2014 [Q2] ("Quantifying Web-Search Privacy," CCS) study what leaks from **queries and
   clicks** in logs. **They assume the log is queries + clicks. No one has extended the
   query-log privacy threat model to include the pre-click *examination* signal** — which is
   strictly more revealing, because it captures considered-but-unclicked and zero-click intent
   that never enters a conventional log.

**The gap = the intersection.** No published work (to our knowledge) (i) treats gaze/cursor
examination on real content/SERPs as a **privacy attack** rather than an IR tool; (ii) quantifies
the **surveillance surplus** of that channel over the click/query baseline; (iii) separates the
**permission-free cursor floor** from the **camera-gated gaze ceiling** on the *same* users and
pages; or (iv) shows it recovers **zero-click / good-abandonment intent** [A1], [A2] that the
clickstream by construction cannot. Any one axis alone is prior work; the stack is the
contribution. This is the D2 analogue of the D4 plan's "ceiling-vs-commodity on the same
subjects" (`wiki/concepts/ceiling-vs-commodity.md`).

**Reframe to lead with:** turn Huang/White/Dumais's *"No clicks, no problem"* [G2] (a
search-quality result) into ***"No clicks, no privacy"*** (a security result). Same signal,
inverted stakes.

---

## 4. Threat model

- **Adversary.** A first-party analytics / search / recommendation tag — the same structural
  position as an ordinary analytics tag — embedded on a content site (search engine, news
  portal, health/finance information site, e-commerce catalog). It **controls or knows its own
  layout**, so it can map gaze/cursor coordinates onto its own AOIs. This is the drive-by web
  adversary of `wiki/concepts/drive-by-web-adversary.md`, restricted to first-party content.
- **What it collects.** (a) **Cursor stream** — move / hover / scroll / dwell / click — available
  on *every* visitor with **no permission prompt and no indicator** (the permission-free floor).
  (b) **Webcam gaze** — where a camera grant exists (the camera-gated ceiling); grants are
  increasingly available in the legitimate contexts catalogued in the D4 plan (accessibility
  navigation, proctoring, attention analytics, gaze-conditioned AI).
- **Goal.** Recover the visitor's **examination and latent intent** on the site's own content:
  which results/products/passages were seriously considered, re-read, or used to satisfy the need
  *without a click*; and the **topic/sensitivity** of that interest.
- **Explicitly out of scope (state it plainly, pre-empt the reviewer).** Reading **another
  origin's** content is blocked by the same-origin policy (D4 plan §5) and this attack does **not**
  claim it. Word-level reconstruction is out of scope too — webcam gaze is too coarse for
  fine AOIs (Thilderkvist & Dobslaw 2024 [45]); the attack operates at **coarse semantic
  granularity** (which of ~10 SERP rows, which of a handful of paragraphs, which topic), which is
  exactly the granularity at which the sensitive inference lives. Scoping to coarse AOIs is not a
  weakness — it is what makes the threat robust to the sensor's real resolution.
- **Why it is realistic despite being first-party.** It needs no defeat of same-origin, no
  physically present camera, no headset. It is the privacy-escalated version of instrumentation
  sites *already run*. The novelty is not a new capability channel; it is showing that the
  examination layer — long assumed private because clicks are the only thing logged — is now
  loggable, and measuring how much that discloses.

---

## 5. Research questions and hypotheses

Conventions mirror the D4 plan: every RQ has a directional, falsifiable hypothesis (H) and a
decision rule; every accuracy figure is reported with a confidence interval over
**subject/session splits**; "chance" and the **click baseline** are both stated for each cell.

- **RQ0 (confound — examination, or a saliency/position prior?).** *Precondition for every other
  RQ.* Does recovered "the visitor examined result 3 / paragraph 2" reflect the *individual's*
  actual examination, or merely a population prior (everyone looks at the top result / first
  paragraph — an F-pattern) [G2], [R1]?
  - **H0.** The attack beats a **position-prior baseline** (predict top-ranked / top-of-page) and
    a **shuffled-label null** collapses it to that prior.
  - **Decision rule.** *Confirmed* if per-AOI examination recovery exceeds the position-prior
    baseline with non-overlapping CIs, **and** shuffled labels collapse to the prior. *Refuted /
    stop* otherwise — then the "signal" is layout saliency, not the user's examination.

- **RQ1 (per-channel examination recovery).** How accurately does each channel — **clicks**,
  **cursor-only**, **gaze-only**, **cursor+gaze fusion** — recover which AOIs the visitor examined,
  scored against **IR-tracker fixation ground truth** (§6)?
  - **H1.** Recovery ordering clicks < cursor-only < gaze-only ≤ fusion, with cursor-only already
    **well above** the click baseline (clicks recover only clicked AOIs; examination is broader).
  - **Decision rule.** *Confirmed* if the cursor-only examination-AUC CI lower bound exceeds the
    click baseline in the headline (SERP) cell.

- **RQ2 (latent-intent surplus — the headline).** How much intent that the clickstream **cannot**
  contain is recovered: (a) **considered-but-unclicked** results/products, (b) **zero-click /
  good-abandonment** satisfied intent [A1], [A2], (c) **re-read / difficulty** passages [B1]?
  - **H2.** Gaze/cursor recover considered-but-unclicked and zero-click intent far above the click
    baseline (which recovers *none* of it by construction), at coarse-AOI granularity.
  - **Decision rule.** *Confirmed* if, on queries the user satisfied without clicking, the attack
    identifies the target-of-interest AOI with CI lower bound > chance and > the (empty) click
    baseline. This is the number the paper leads with.

- **RQ3 (permission-free floor vs. camera ceiling).** Quantify cursor-only (no permission) vs.
  gaze-only vs. fusion on the *same* users and pages — the ceiling-vs-commodity analogue.
  - **H3.** Cursor-only leaks a substantial, quotable fraction of examination with **zero
    permission**; the camera adds a measured increment; fusion is best; the gaze increment is
    largest exactly where cursor–gaze alignment is weak (non-SERP reading) [G3].
  - **Decision rule.** Reports the gap regardless of ordering; the deliverable is the two curves
    (floor, ceiling) and their difference.

- **RQ4 (topic / sensitivity inference).** From examination patterns + the adversary's own known
  content, can it infer the **topic/sensitivity category** (health, finance, political, legal) of
  what was examined, *including for zero-click sessions*?
  - **H4.** Topic/sensitivity of the examined content is inferable above chance even when no click
    or query term discloses it.
  - **Decision rule.** *Confirmed* if category recovery CI lower bound > chance on zero-click
    sessions.

- **RQ5 (defense, optional).** What client-side countermeasure — cursor–gaze decoupling, dwell
  quantization, examination-rate limiting, or gaze perturbation
  (`wiki/concepts/gaze-perturbation-defense.md`) — suppresses examination recovery at bounded
  search-utility cost?
  - **H5 / decision rule.** There exists an operating point that drives examination recovery
    toward the position prior while a utility metric (e.g., relevance-feedback quality [B2]) stays
    within a pre-registered bound; report the full privacy–utility curve.

---

## 6. Apparatus, stimuli, and ground truth

**Rig — reuse the D4 simultaneous-capture harness** (`wiki/concepts/simultaneous-capture-rig.md`).
Record **Gazepoint IR** (per-frame gaze → **fixation-on-AOI ground truth**, the hard label for
"examined"), **commodity webcam gaze** (WebGazer / WebEyeTrack), and a **full mouse-event stream**
simultaneously and time-aligned. The one harness delta that matters: today the harness logs mouse
*clicks* only, as WebGazer calibration input; D2 needs **move / hover / scroll / dwell** logging
promoted to a first-class recorded stream (`wiki/entities/gaze-feature-extraction.md` gains a
cursor-feature extractor alongside the gaze one).

**Critical control (do not contaminate the commodity arm).** As in the D4 plan §9, the webcam and
cursor channels are the *attack*; Gazepoint IR is the **measurement instrument** supplying
examination ground truth only — it must never label-supervise or correct the webcam/cursor
recovery, or the attack number is inflated.

**Stimuli — real content surfaces, with examination ground truth built in.** Reuse and extend the
five-task suite (`wiki/entities/task-suite.md`); the SERP task inherits SearchGazer's AOI
instrumentation:

1. **SERP scanning (headline surface).** Controlled result sets. Split queries into
   **click-required** (answer behind a result) and **zero-click / good-abandonment** (answer
   present on the SERP as a snippet/answer box — the [A1], [A2] case). SERPs are the surface where
   cursor–gaze alignment is strongest [G3] and AOIs (rows) are large enough for webcam resolution.
2. **Reading passages** with target information at **known paragraphs** (sub-document relevance
   ground truth, à la Buscher [B1], [B2]) — recover which passages were read vs. skimmed vs.
   re-read.
3. **E-commerce / product grid** — considered-but-unclicked products (the clearest
   "interest-without-a-click" case).
4. **News / feed scanning** — topic/sensitivity inference (RQ4).

**Ground truth.** (a) *Examination* = IR fixation dwell on each AOI (hard label). (b) *Intent* =
post-task probes ("which result answered your question?", "which product were you considering?")
and, for zero-click, a comprehension probe on the snippet — softer labels, used for the intent
interpretation layer, never for the primary examination score. (c) *Content/topic* = the known
layout the first-party adversary controls.

**Public data for a large-N feasibility ceiling.** The 2025 SERP dataset with **simultaneous
mouse and eye** movements (47 participants, 2,776 Google-SERP queries) [G5] and the Attentive-Cursor
dataset [G4] let the cursor-floor and gaze–cursor-alignment analyses be prototyped and a
feasibility ceiling estimated *before* fresh collection — the D2 analogue of using GazeBase for the
D4 ceiling. (Flag [G5] as a preprint; verify licensing before use.)

---

## 7. Features, models, and metrics

**A key structural difference from D4 to state explicitly.** D4's features are
content-*independent* distributional dynamics (fixation/saccade statistics — see
`wiki/entities/gaze-feature-extraction.md`, the 16-D vector). D2's features are
**AOI-/content-anchored**: they live in the coordinate frame of the adversary's known layout.
This is why D2 is content-dependent and first-party-scoped, and why it is a *different* pipeline,
not a re-parameterization of the D4 one.

- **Gaze-on-AOI features:** per-AOI dwell time, fixation count, time-to-first-fixation, revisits /
  regressions [R1], scan-path order over results, gaze transition matrix between AOIs.
- **Cursor features (permission-free):** per-AOI hover time and cursor dwell, cursor path length /
  curvature, cursor-to-AOI proximity over time, scroll depth and reversals, and **clicks (the
  baseline)** [G1], [G2].
- **Fusion features:** cursor–gaze alignment / offset / lead time (strongest signal on SERPs [G3]).
- **Models.** (a) Per-AOI **examination classifier** (was this AOI examined? — hard IR label),
  reported as AUC per channel. (b) **Target-of-interest ranker** over AOIs (which result/product
  did the visitor care about?), reported as rank-1 / rank-k and mean reciprocal rank against the
  intent probe. (c) **Topic/sensitivity classifier** (RQ4). Start with interpretable models
  (logistic / gradient-boosted trees on the features above) at small N; defer any deep model until
  N and the public datasets [G4], [G5] support it — the same discipline as the D4 plan §12.
- **Metrics — the headline is a *surplus curve*:**
  - **Surveillance-surplus:** information recovered by {clicks} ⊂ {cursor} ⊂ {gaze} ⊂ {fusion} on
    the same sessions — the crisp, quotable deliverable ("clicks recover X% of examined AOIs;
    cursor alone recovers Y%; fusion recovers Z% — all with no query-term disclosure").
  - **Zero-click intent-recovery rate** (RQ2) — recovery on sessions with an *empty* clickstream.
  - **Recovery vs. observation window** — "how many seconds of scanning reveal which result you
    cared about" (the D2 analogue of the D4 window curve).
  - **Baselines:** chance; the **position/saliency prior** (RQ0); the **click baseline** (the bar
    the surplus is measured over).

---

## 8. Composition with D4, and the defense

**Composition (state it, but keep D2's claim scoped).** D2 yields a per-visit **interest profile**;
D4 (`GazePry_ReID_Research_Plan.md`) yields a **persistent, person-bound, unclearable identifier**
from the same gaze stream. Together: the tag attaches *what you were interested in* (D2) to *a
stable pseudonymous you* (D4), across visits and — via D4's cross-site linkage — across the sites
the tag is on. This is a genuinely alarming end state and worth one paragraph, but the D2 paper's
own contribution should stay bounded to the **within-site examination surplus** so it stands
independently of D4's cross-site claim surviving review.

**Defense (RQ5, pairs the attack with a mitigation — reviewers reward this).** Options on a
privacy–utility curve: **cursor–gaze decoupling** (inject cursor motion uncorrelated with gaze, or
suppress hover logging), **dwell quantization / examination-rate limiting** (coarsen the temporal
resolution below what examination recovery needs), and client-side **gaze perturbation**
(`wiki/concepts/gaze-perturbation-defense.md`; feature-level DP [47], Kalεido-style real-time
control [48]). Utility is measured by a legitimate task the same signal supports — relevance
feedback quality [B2] or accessibility navigation. A browser-level countermeasure (an
examination-privacy budget on cursor/gaze event rates) is a natural responsible-disclosure ask to
vendors/W3C, mirroring the D4 disclosure surface.

---

## 9. Related work and the exact gap this fills

**Webcam-search lineage (the sensor + the AOI framing this weaponizes).** SearchGazer [4] (the
project's own ancestor — real-time SERP AOI identification, benign research-tool framing);
Eye-of-the-Typer [7] (gaze during typing); WebGazer [14] (the tracker + covert click
calibration). Webcam-gaze validity is improving (Kaduk 2024; WebEyeTrack [25]) but bounded at
fine AOIs by Thilderkvist & Dobslaw 2024 [45] — which is why D2 is a **coarse-AOI** attack.

**Cursor as a Web-scale gaze proxy (the permission-free floor).** Guo & Agichtein 2010 [G1];
Huang, White & Dumais 2011 [G2] ("No clicks, no problem"); Huang, White & Buscher 2012 [G3]
(alignment strongest on SERPs); Attentive-Cursor dataset [G4]; simultaneous mouse+eye SERP
dataset [G5]. **Tool-framed, for ranking — never as covert surveillance.**

**Eye movements as reading/relevance feedback (the finer recovery).** Buscher, Dengel & van Elst
2008 [B1]; *Attentive Documents* [B2]; Rayner 1998 [R1]. **Assistive/IR-framed — the leakage
reframing is absent.**

**Zero-click / good abandonment (the intent the clickstream hides — the RQ2 target).** Li,
Huffman & Tokuda 2009 [A1]; Williams et al. 2016 [A2]. Establish that satisfied intent
increasingly leaves *no click*; D2 shows gaze/cursor **recover** that hidden intent.

**Query-log privacy (the threat model this extends).** Jones et al. 2007 [Q1]; Gervais et al.
2014 [Q2] (CCS — precedent that search privacy belongs at a top security venue). **Both stop at
queries + clicks; neither includes the examination layer.**

**Privacy framing / adjacent leakage.** Kröger 2020 [21] and Katsini 2020 [3] (what gaze reveals /
gaze in security); Liebling & Preibusch 2014 [6] (gaze extraction is *opaque* even when the camera
is consented — directly supports the "no indicator" harm); Weinberg 2011 [5] (history sniffing —
the "recover what you looked at" side-channel analogue); Alsakar 2025 [10] (mobile attribute
inference); Hutt 2024 [22] (webcam gaze → comprehension errors — reading-state precedent).
Content-*dependent* keystroke attacks EyeTell [27] and GazeRevealer [8] delimit the contrast class
(they recover *typed secrets*; D2 recovers *examined interest*).

**One-sentence gap statement (reuse in the intro):** *Gaze and cursor examination signals are
established as tools for the search engine's own ranking, and query-log privacy is established for
queries and clicks — but no prior work treats commodity webcam-gaze-plus-permission-free-cursor
examination on real content as a privacy attack, quantifies its surveillance surplus over the
clickstream, separates the permission-free cursor floor from the camera-gated gaze ceiling on the
same users, or shows it recovers the zero-click intent the clickstream cannot contain.*

---

## 10. Risks, honest limitations, and the reviewer traps

- **The same-origin objection (the #1 trap).** A reviewer will say "content-dependent → blocked
  cross-site → not a Web threat." **Answer on the page (§4):** the threat is *first-party and
  within-site*, needs no same-origin defeat, and is alarming because of *zero-click / considered-
  but-unclicked* intent and the *permission-free cursor* — not because of cross-site peeking.
  Do not overclaim cross-site content recovery.
- **Webcam coarseness (Thilderkvist [45]).** Concede it; scope to coarse AOIs (SERP rows,
  paragraphs, topics). Lean on the SERP surface where AOIs are large and cursor–gaze alignment is
  strongest [G3].
- **Soft ground truth for "intent."** Examination has a *hard* label (IR fixations); intent does
  not (self-report probes are noisy). **Lead with examination recovery (hard) and the surplus
  curve; treat intent/topic as the interpretation layer**, reported with its uncertainty.
- **Not everyone moves the cursor.** Cursor–gaze coupling varies across users and tasks. Report the
  *distribution* of cursor-floor recovery, not just the mean; the gaze ceiling is what covers the
  low-cursor users (that is the point of measuring both).
- **RQ0 confound (saliency prior).** The strongest attack on this paper is "you just predicted the
  top result." The position-prior baseline and shuffled-label null (RQ0) are non-negotiable
  preconditions, exactly as the calibration/session battery is for D4
  (`wiki/concepts/reid-confound-controls.md`).
- **"First-party feels less scary than cross-site."** Counter with the sensitivity of the recovered
  considerations (health/finance/legal researched-but-unclicked) and the no-permission /
  no-indicator cursor floor [6].
- **Ethics / hygiene (carry over from the D4 plan A.6).** IRB-exempt determination on file; never
  commit participant gaze/cursor logs (`prototype/data/` is git-ignored); responsible disclosure to
  browser/W3C on the cursor-and-gaze examination surface; pair the attack with the RQ5 defense.

---

## 11. References and citation status

*Peer-reviewed venues preferred; **preprints flagged**; DOIs to re-verify against the published
version before submission are marked **(verify)**. Items reused from the shared project bibliography
(`GazePry_ReID_Research_Plan.md` §21) keep their existing bracket number; items **new to the
project** are lettered by group and must be **added to the shared bibliography on ingest**.*

**Reused from the shared bibliography (already vetted in the D4 plan §21):**

- **[3]** Katsini et al., "The Role of Eye Gaze in Security and Privacy Applications," *CHI '20*,
  doi:10.1145/3313831.3376840.
- **[4]** Papoutsaki, Laskey & Huang, "SearchGazer: Webcam Eye Tracking for Remote Studies of Web
  Search," *CHIIR '17*, doi:10.1145/3020165.3020170.
- **[5]** Weinberg et al., "I Still Know What You Visited Last Summer," *IEEE S&P 2011*,
  doi:10.1109/SP.2011.23.
- **[6]** Liebling & Preibusch, "Privacy considerations for a pervasive eye tracking world,"
  *UbiComp '14 Adjunct*, doi:10.1145/2638728.2641688.
- **[7]** Papoutsaki et al., "The eye of the typer," *ETRA '18*, doi:10.1145/3204493.3204552.
- **[8]** Wang et al., "GazeRevealer" (*IEEE TMC* 2020), doi:10.1109/TMC.2019.2934690.
- **[10]** Alsakar et al., "Assessing and Mitigating the Privacy Implications of Eye Tracking on
  Handheld Mobile Devices," *ACM TOPS* 2025, doi:10.1145/3746452.
- **[14]** Papoutsaki et al., "WebGazer," *IJCAI '16*.
- **[21]** Kröger, Lutz & Müller, "What Does Your Gaze Reveal About You?," Springer 2020,
  doi:10.1007/978-3-030-42504-3_15.
- **[22]** Hutt et al., "Webcam-based eye tracking to detect mind wandering and comprehension
  errors," *Behav. Res.* 2024, doi:10.3758/s13428-022-02040-x.
- **[25]** Davalos et al., "WebEyeTrack," 2025 — **arXiv:2508.19544 (preprint)**.
- **[27]** Chen et al., "EyeTell," *IEEE S&P 2018*, doi:10.1109/SP.2018.00010.
- **[45]** Thilderkvist & Dobslaw, "On current limitations of online eye-tracking to study the
  visual processing of source code," *Inf. Softw. Technol.* 2024, doi:10.1016/j.infsof.2024.107502.
- **[47]** Steil et al., "Privacy-aware eye tracking using differential privacy," *ETRA '19*,
  doi:10.1145/3314111.3319915.
- **[48]** Li et al., "Kalεido: Real-Time Privacy Control for Eye-Tracking Systems," *USENIX
  Security 21*.

**New — cursor-as-gaze-proxy in Web search (group G):**

- **[G1]** Q. Guo and E. Agichtein, "Towards predicting web searcher gaze position from mouse
  movements," *CHI '10 Extended Abstracts (CHI EA '10)*, pp. 3601–3606,
  doi:10.1145/1753846.1754025. *(Extended abstract — note the venue type.)*
- **[G2]** J. Huang, R. W. White, and S. Dumais, "No clicks, no problem: using cursor movements to
  understand and improve search," *CHI '11*, pp. 1225–1234, doi:10.1145/1978942.1979125.
- **[G3]** J. Huang, R. W. White, and G. Buscher, "User see, user point: gaze and cursor alignment
  in web search," *CHI '12*, pp. 1341–1350, doi:10.1145/2207676.2208591.
- **[G4]** L. A. Leiva and I. Arapakis, "The Attentive Cursor Dataset," *Frontiers in Human
  Neuroscience*, vol. 14, art. 565664, 2020, doi:10.3389/fnhum.2020.565664.
- **[G5]** K. Latifzadeh, J. Gwizdka, and L. A. Leiva, "A Versatile Dataset of Mouse and Eye
  Movements on Search Engine Results Pages," 2025 — **arXiv:2507.08003 (preprint)**. *(Simultaneous
  mouse + eye on Google SERPs; 47 participants, 2,776 queries; verify license before use.)*

**New — eye movements as reading / relevance feedback (group B):**

- **[B1]** G. Buscher, A. Dengel, and L. van Elst, "Eye movements as implicit relevance feedback,"
  *CHI '08 Extended Abstracts*, pp. 2991–2996, doi:10.1145/1358628.1358796. *(Extended abstract.)*
- **[B2]** G. Buscher, A. Dengel, R. Biedert, and L. van Elst, "Attentive documents: Eye tracking
  as implicit feedback for information retrieval and beyond," *ACM Trans. Interact. Intell. Syst.
  (TiiS)*, vol. 1, no. 2, art. 9, 2012, doi:10.1145/2070719.2070722.
- **[R1]** K. Rayner, "Eye movements in reading and information processing: 20 years of research,"
  *Psychological Bulletin*, vol. 124, no. 3, pp. 372–422, 1998, doi:10.1037/0033-2909.124.3.372.

**New — zero-click / good abandonment (group A):**

- **[A1]** J. Li, S. Huffman, and A. Tokuda, "Good abandonment in mobile and PC internet search,"
  *SIGIR '09*, pp. 43–50, doi:10.1145/1571941.1571951.
- **[A2]** K. Williams, J. Kiseleva, A. C. Crook, I. Zitouni, A. H. Awadallah, and M. Khabsa,
  "Detecting good abandonment in mobile search," *WWW '16*, doi:10.1145/2872427.2883074. **(verify
  DOI/pages)**

**New — query-log / Web-search privacy (group Q):**

- **[Q1]** R. Jones, R. Kumar, B. Pang, and A. Tomkins, "'I know what you did last summer': query
  logs and user privacy," *CIKM '07*, pp. 909–914, doi:10.1145/1321440.1321573.
- **[Q2]** A. Gervais, R. Shokri, A. Singla, S. Capkun, and V. Lenders, "Quantifying Web-Search
  Privacy," *ACM CCS '14*, doi:10.1145/2660267.2660367.

*Retrieved and verified 2026-07-16 via web search; **[A2]** DOI still to confirm against the ACM
DL record before submission. A SIGIR '08 companion to [B1] (Buscher, van Elst & Dengel, "Query
expansion using gaze-based feedback on the subdocument level") and Kumar et al. 2007 (WWW,
token-based query-log hashing) are candidates to add if the related-work section needs them —
retrieve and verify before citing.*

---

## 12. Immediate next steps

1. **Decide the headline surface.** Recommend **SERP + zero-click** as the lead (sharpest privacy
   stakes, strongest cursor–gaze alignment [G3], AOIs large enough for webcam) with reading
   passages as the second surface. Confirm before building stimuli.
2. **Harness delta:** promote mouse **move/hover/scroll/dwell** to a first-class recorded stream
   (currently only clicks are logged, for calibration) and add a **cursor-feature extractor**
   beside the gaze one; add **IR-fixation-on-AOI** ground-truth export from the Gazepoint arm.
3. **Prototype the cursor floor on public data first** ([G4], [G5]) — estimate cursor-only
   examination recovery and the gaze–cursor alignment gap *before* fresh collection, the D2
   analogue of using GazeBase for the D4 ceiling.
4. **Author the SERP stimuli** with click-required vs. zero-click/good-abandonment variants and
   embedded AOI/topic ground truth; author reading passages with sub-document relevance labels.
5. **Pre-register RQ0** (position-prior baseline + shuffled-label null) as the gating pilot — no
   downstream number is meaningful until the examination signal beats the saliency prior.
6. **Ingest this document into the wiki** (`wiki/sources/` page + update `wiki/index.md` and
   `wiki/log.md`), and **merge groups G/B/A/Q/R into the shared bibliography** so D2 and D4 share
   one numbered reference list.
7. Before submission, re-verify every **(verify)**-flagged and preprint citation against its
   published version.

---

*Status: proposal / blueprint — no D2 empirical result exists yet. Treat all H0–H5 as
pre-registered predictions, with RQ0 as the gate, exactly as the D4 plan treats its hypotheses
(`wiki/concepts/pilot-empirical-status.md`).*
