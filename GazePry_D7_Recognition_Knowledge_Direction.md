# GazePry — Direction D7: Recognition & Concealed-Knowledge Leakage

**"The Recognition Oracle": Extracting What a Visitor Already Knows from Commodity
Webcam Gaze**

*A research-direction blueprint for a security/privacy conference submission. This
document develops a **new** leakage vector — **D7**, recognition and concealed-knowledge
leakage — that the existing GazePry taxonomy (`wiki/concepts/leakage-vectors-d1-d6.md`)
does not cover. The leaked payload is **memory contents**: what the visitor has seen,
used, or knows. It is **not** a biometric and **not** current-task intent.*

*Companion to, not a replacement for,
[`GazePry_ReID_Research_Plan.md`](GazePry_ReID_Research_Plan.md) (**D4**, identity) and
[`GazePry_D2_Reading_Search_Intent_Direction.md`](GazePry_D2_Reading_Search_Intent_Direction.md)
(**D2**, examination and intent). D4 leaks **who you are**; D2 leaks **what you are doing
now**; D7 leaks **what you already knew before you arrived**. All three share an adversary,
a harness, and a confound-control discipline, and they compose (§8).*

*Every load-bearing claim is attributed. §11 records the peer-reviewed / preprint status of
each source, which are **new** to the project bibliography, and which citations are **not
yet verified**.*

---

## Contents

1. [One-paragraph thesis](#1-one-paragraph-thesis)
2. [Why D7, and how it differs from D2 and D4](#2-why-d7-and-how-it-differs-from-d2-and-d4)
3. [The research gap (the part that makes it publishable)](#3-the-research-gap-the-part-that-makes-it-publishable)
4. [Threat model](#4-threat-model)
5. [Research questions and hypotheses](#5-research-questions-and-hypotheses)
6. [Methodology: apparatus, stimuli, design, and ground truth](#6-methodology-apparatus-stimuli-design-and-ground-truth)
7. [Features, models, and metrics](#7-features-models-and-metrics)
8. [Composition with D2/D4, and the defense](#8-composition-with-d2d4-and-the-defense)
9. [Related work and the exact gap this fills](#9-related-work-and-the-exact-gap-this-fills)
10. [Risks, honest limitations, and the reviewer traps](#10-risks-honest-limitations-and-the-reviewer-traps)
11. [References and citation status](#11-references-and-citation-status)
12. [Immediate next steps](#12-immediate-next-steps)

---

## 1. One-paragraph thesis

Recognition is **involuntary and it moves the eyes**. Fifty years of memory research
establishes that a previously seen stimulus is sampled differently from a novel one — the
*eye-movement-based memory effect* — that the difference appears within the **first five
fixations** [M1], that it does not require conscious recollection [M2], and that it **persists
when the viewer is actively trying to conceal it** [C1], [C3]. Forensic psychology has spent
two decades turning this into the *ocular Concealed Information Test*, reporting per-item AUCs
of roughly 0.67–0.87 on research-grade infrared hardware [C3]. **This direction moves that
measurement out of the interrogation room and onto the open web.** A first-party page that
holds a camera grant can render an ordinary-looking array of tiles — site logos, product
photos, faces, document thumbnails — and read, from dwell asymmetry alone, **which of them
the visitor has seen before**. The contribution is to reframe a mature *forensic assessment
instrument* as a *covert web extraction attack*, and to show that the covert setting is
**strictly easier than the forensic one**: the entire countermeasure literature that bounds
the CIT assumes a subject who knows they are being tested, and a drive-by web visitor does
not. The concrete harm is that a webpage learns which sites you use, which brands and
products you have encountered, and which sensitive topics you have prior exposure to —
**with no click, no typing, no cookie, and no stored state** — resurrecting, at the
perception layer, exactly the capability browsers spent a decade removing from the
rendering layer [5].

---

## 2. Why D7, and how it differs from D2 and D4

The GazePry taxonomy runs D1–D6. Recognition leakage fits none of them cleanly: it is
content-*dependent* (the adversary chooses and knows the stimulus) like D1/D2, but what it
extracts is neither the current secret being typed (D1), nor the visitor's present interest
(D2), nor a persistent identity (D4), nor a demographic attribute (D5). It extracts
**stored memory**. It therefore gets its own vector.

| | **D4** (ReID plan) | **D2** (Reading/Intent) | **D7** (this document) |
|---|---|---|---|
| What leaks | Persistent **identity** | **Interest / intent**, now | **Prior exposure / knowledge**, before now |
| Tense | Timeless | Present | **Past** |
| Regime | Content-independent | Content-dependent | Content-dependent, **adversary-chosen** |
| Cross-site? | Yes | No (first-party) | No (first-party) |
| Biometric? | Yes | No | **No** |
| Adversary role | Passive observer | Passive observer | **Active — it picks the probes** |
| Sensor demand | Distributional dynamics | Coarse AOI | **Coarse AOI + fixation timing** |
| Novelty axis | Sensor × setting × transfer × unclearability | Examination surplus over clicks | **Forensic instrument → covert web attack; countermeasure-free setting; commodity sensor** |

The decisive structural difference is the last-but-one row. D2 and D4 are *observational*:
the adversary takes whatever the user happens to look at. **D7 is *interventional*: the
adversary designs the stimulus.** That is what makes it an oracle rather than a profiler —
the attacker can ask a specific question ("has this person seen this?") and get a per-item
answer, and can ask many questions in sequence.

**Why this direction is more tractable than D4 right now.** The D4 plan is gated by RQ0, the
person-versus-apparatus confound (`wiki/concepts/reid-confound-controls.md`), and by an
empirical status of N=2 with no true cross-session separation (D4 plan §19a). D7 sidesteps
both structurally, not by hand-waving:

- The D7 effect is a **within-participant, within-session, within-trial contrast between
  AOIs on the same screen**. Calibration geometry, lighting, seating, screen size, tracker
  identity, and logging cadence are all *constant across the AOIs being compared*. They
  cannot produce a familiar-versus-unfamiliar difference.
- With **item-level counterbalancing** (§6.4), each stimulus serves as "familiar" for half
  the participants and "unfamiliar" for the other half, so item saliency and screen position
  are orthogonal to the contrast by construction.
- It needs **N ≈ 40**, not N ≥ 50 with a populated gallery, because the unit of analysis is
  the *trial*, not the *identity pair*. Forty participants × 40 trials is 1,600 observations.
- It needs **one session**, not two sessions ≥ 1 week apart. (A delay condition is a bonus
  in E1, not a prerequisite.)

---

## 3. The research gap (the part that makes it publishable)

Four literatures converge on this space and every one of them stops short of the attack.

1. **The eye-movement-based memory effect (basic science).** Althoff & Cohen [M1] showed
   distinct sampling of famous versus non-famous faces across processing tasks, emerging
   within the first five fixations. Hannula et al. [M2] review the effect as an obligatory
   consequence of prior exposure that operates independently of conscious recollection.
   **Framed as a window into memory and hippocampal function — never as an extraction
   channel.**

2. **The ocular Concealed Information Test (forensic).** Schwedes & Wentura [C1] detected
   concealed knowledge in 65% of relevant trials from fixation duration in a six-face array,
   *regardless of whether the participant intended to reveal or conceal*. Nahari et al. [C2]
   (four-face arrays, n=61) showed that **task demands decide whether the effect can be
   voluntarily suppressed**, and that memory-dependent tasks resist countermeasures. Millen
   & Hancock [C3] reported AUC 0.67–0.87, with mean fixation duration surviving deliberate
   countermeasures (d = 0.91 under countermeasures, *higher* than the 0.66 without) even as
   the fine spatial signal collapsed (d = 1.40 → −0.12). Zangrossi et al. [C5] detected
   week-old mock-crime memories at 75% from fixation topography alone. **All of it assumes a
   cooperative, institutionally-framed test of a subject who knows they are a suspect.**

3. **Webcam eye-tracking validation (methods).** Van der Cruyssen et al. [W1] replicated
   the **novelty preference** — the recognition-memory looking asymmetry that is precisely
   this attack's signal — online with WebGazer.js, alongside the cascade effect and the
   visual world paradigm, with effect sizes shrinking 20–27%. **Framed as "can we move
   psychology experiments online," not "can a website do this to you."** Note the author
   list: it includes the same Ben-Shakhar and Pertzov who authored [C2]. The forensic CIT
   community has already brought its instrument to the webcam. It has not brought it to a
   threat model.

4. **Eye-tracking privacy (security).** The decade review [P1] finds that normative work
   flags *inference of identity and personal traits* as the unresolved risk while technical
   work treats privacy as a computational problem. The GazePry bibliography's own
   content-dependent attacks — EyeTell [27], GazeRevealer [8], GAZEploit [14] — all target
   **secrets being entered right now**. **Nobody targets what is already in the visitor's
   head.**

**The gap = the intersection.** No published work (to our knowledge) (i) treats the ocular
recognition effect as an **adversarial extraction primitive** rather than an assessment
instrument; (ii) instantiates it against an **unwitting** visitor, where the countermeasure
literature that bounds the forensic test does not apply; (iii) runs it on a **commodity
in-browser webcam** as a deployable web capability and measures the gap to an infrared
ceiling on the same subjects; or (iv) connects it to the **history-sniffing** threat model
[5] that browsers have already accepted as legitimate to defend against. Any one axis alone
is prior work. The stack is the contribution.

**Reframe to lead with:** browsers killed `:visited` history sniffing at the rendering layer
[5]. This attack reinstates the capability one layer below, where **the side channel is the
user rather than the renderer** — and where no browser patch reaches, because the leak
happens before the user decides to disclose anything.

---

## 4. Threat model

- **Adversary.** A first-party page or first-party-included script with a camera grant — the
  same structural position as the D4 adversary (`wiki/concepts/drive-by-web-adversary.md`
  and D4 plan §7), and the same realistic acquisition path: accessibility gaze navigation,
  proctoring, attention analytics, WebXR, or gaze-conditioned AI (D4 plan A.4). Unlike D2's
  cursor floor, D7 has **no permission-free variant** — it needs gaze. State that plainly.
- **What makes it *active*.** The adversary **chooses the probe set**. It renders an array
  that looks like ordinary web content (a product carousel, an image picker, a
  "choose your interests" onboarding step, an illustrated article) and measures gaze
  allocation across its own known AOIs. It never needs to ask a question or record an answer.
- **Goal.** For each probe item, output a posterior on "this visitor has prior exposure to
  this item." Aggregate into a knowledge profile: which services they use, which brands and
  products they have encountered, which sensitive topics they have prior exposure to, and —
  in the strongest form — whether they recognize a specific person, document, or place.
- **Why the covert setting is *stronger* than the forensic one.** The CIT literature's main
  limitation is countermeasures: [C2] shows a motivated subject can suppress the effect in a
  visual-detection task, and [C3] shows only the temporal measures survive. **A web visitor
  who does not know they are being tested applies no countermeasures at all.** The attack
  therefore operates in the naive regime, where effects are largest. This inversion is the
  single most important point in the threat model and should be stated in the abstract.
- **Explicitly out of scope.** Reading another origin's content (blocked by the same-origin
  policy — D4 plan §5). Word-level or fine-AOI reconstruction (webcam gaze is too coarse —
  [W4], and [W1] bounds the practical design to roughly ≤4 well-separated regions). Any
  claim that this is a lie detector, a clinical instrument, or admissible evidence: it is a
  *privacy leak*, and the paper must not drift into forensic claims.
- **What the user can observe.** A camera indicator. Nothing else. No network request
  distinguishable from analytics, no storage, no click. Liebling & Preibusch [6] is the
  citation for the core asymmetry: webcam privacy loss is legible to users, but **gaze
  extraction is opaque** — and knowledge extraction from gaze is opaque twice over.

---

## 5. Research questions and hypotheses

Conventions mirror the D4 and D2 plans: each RQ has a directional, falsifiable hypothesis
(H) and a decision rule; every figure is reported with a confidence interval over
participant splits; δ denotes a pre-registered margin fixed before collection. The headline
cell is **E2, naive condition, on-device webcam, per-user AUC at k = 20 trials**.

- **RQ0 (the gate — is it recognition, or is it the picture?).** Does the discriminating
  signal reflect the *visitor's prior exposure*, rather than intrinsic **item saliency**,
  **screen position**, or a **calibration artifact**?
  - **H0.** Under item-level counterbalancing (§6.4), a classifier trained on AOI features
    separates familiar from unfamiliar above chance; under a **shuffled familiarity-label
    null** it collapses to AUC ≈ 0.5; and a **saliency-and-position-only** baseline
    (item identity + AOI position, no participant-specific familiarity) performs at chance.
  - **Decision rule.** *Confirmed* if the shuffled-label AUC CI includes 0.5 **and** the
    saliency-only baseline CI includes 0.5 **and** the real per-trial AUC CI lower bound
    > 0.5. **Refuted / stop** otherwise — the effect is a property of the images, not of the
    person, and nothing downstream stands. **Run this on E1 before collecting E2 or E3.**

- **RQ1 (mechanism — does the effect survive the commodity sensor?).** With
  experimenter-controlled familiarity (E1), does webcam gaze recover prior exposure, and how
  does accuracy decay with the study-to-probe delay?
  - **H1.** Per-trial AUC is above chance at every delay, is highest immediately, and decays
    monotonically across immediate / 20-minute / 1-week probes. Webcam AUC is below the
    simultaneous infrared AUC by a positive gap.
  - **Decision rule.** *Confirmed* if the immediate-delay per-trial AUC CI lower bound > 0.5
    on at least the best on-device arm. Reference points for scale, **not** targets to match:
    IR per-item AUC 0.67–0.87 [C3], and an expected 20–27% effect-size shrinkage online [W1].

- **RQ2 (the attack — does it work on real-world familiarity?).** Does the same pipeline
  recover **naturally acquired** familiarity (E2: which web services the visitor actually
  uses) rather than lab-installed familiarity?
  - **H2.** Per-user AUC over k = 20 trials exceeds chance and exceeds per-trial AUC (
    aggregation helps), and the **k-to-threshold curve** reaches a usable operating point
    (TPR ≥ 0.7 at FPR ≤ 0.1) within a session a real site could plausibly hold.
  - **Decision rule.** *Confirmed* if the per-user AUC CI lower bound > 0.5 at some k ≤ 40.
    *Narrowed* if only high-salience item classes (major-brand logos) clear chance — still a
    scoped, meaningful threat. *Refuted* if per-user AUC ≈ 0.5 at every k.
  - This is the headline. It is also the riskiest cell, because lab-installed familiarity
    (E1) is a much stronger manipulation than "has an account on this site."

- **RQ3 (ceiling vs commodity).** What is the AUC gap between the Gazepoint infrared ceiling
  and the on-device webcam arms (WebGazer, WebEyeTrack, EyeGestures) on the **same**
  participants and trials, using the simultaneous-capture rig already specified in D4 plan §9?
  - **H3.** IR AUC > webcam AUC in every matched cell, ordered WebEyeTrack ≤ EyeGestures ≤
    WebGazer in error, with the gap **narrowing** as k grows (aggregation absorbs sensor noise).
  - **Decision rule.** The gap magnitude is the deliverable regardless of ordering. This RQ
    quantifies; it does not fail.

- **RQ4 (countermeasures — quantifying the covert advantage).** How much does an *informed*
  visitor recover? Compare naive participants against participants explicitly instructed to
  conceal recognition and given a concealment strategy.
  - **H4.** AUC drops under instructed countermeasures but stays above chance, and the
    **surviving signal is temporal** (mean and first fixation duration) rather than spatial
    (dwell proportion) — the pattern [C3] reports on infrared and [C1] reports as
    intent-independent.
  - **Decision rule.** *Confirmed* if (naive − countermeasure) AUC difference CI excludes 0
    **and** the countermeasure-condition AUC CI lower bound > 0.5 for at least the
    fixation-duration feature family. This RQ delivers the quotable number for the threat
    model: **the price of not knowing you are being measured.**

- **RQ5 (defense).** What client-side mitigation defeats the oracle at acceptable utility cost?
  - **H5.** There is an operating point — AOI-level spatial coarsening, temporal jitter of
    the gaze stream, or per-AOI dwell-proportion differential privacy [47], [48] — that pushes
    attacker AUC toward 0.5 while a legitimate gaze-navigation or attention-analytics utility
    task stays within a pre-registered bound.
  - **Decision rule.** *Confirmed* if some operating point reduces AUC by ≥ δ_priv with
    utility degradation ≤ δ_util. Report the full privacy–utility curve regardless. Note the
    structural asymmetry worth reporting: defenses that quantize **space** may leave the
    **fixation-duration** channel intact, which is exactly the channel [C3] found
    countermeasure-resistant. A defense that only coarsens AOIs is likely insufficient, and
    demonstrating that is itself a result.

---

## 6. Methodology: apparatus, stimuli, design, and ground truth

### 6.1 Apparatus

Reuse the existing harness unchanged wherever possible: the tracker-agnostic orchestrator
and the four self-registering adapters (`public/trackers/`), the `{t, x, y}` stream contract,
the ingest server (`server.js`), and the simultaneous Gazepoint rig described in D4 plan §9
with its critical control (**IR is a measurement instrument, never a training signal**).

New components required:

| Component | Where | Effort |
|---|---|---|
| Recognition-probe array task page | `public/tasks/probe.html` | new, small |
| Trial sequencer + AOI geometry logger (emits AOI rects with the gaze stream) | `public/task-runner.js` | extend |
| I-DT (dispersion-threshold) fixation detector | `analysis/features.py`, `reid-core.js` | new, parity-tested |
| AOI-anchored feature extractor | `analysis/aoi_features.py` | new |
| Per-trial / per-user classifier + AUC reporting | `analysis/recognition.py` | new |

The I-DT detector is not optional. The existing I-VT velocity threshold is acknowledged in
the D4 plan as coarse at webcam rates, and [W4] introduced a dispersion-threshold algorithm
specifically because none existed for low-frequency webcam data. Fixation **duration** is
this direction's countermeasure-resistant feature, so the segmentation algorithm is
load-bearing and must be validated against the simultaneous Gazepoint channel.

### 6.2 Stimulus geometry (sourced constraints, not guesses)

The array design is pinned by two published bounds:

- [W1] replicated the novelty preference online with **two images of 472 × 331 px separated
  by 295 px**. That is the demonstrated-workable geometry on WebGazer.
- The practical webcam ceiling is roughly **≤ 4 well-separated regions of interest**
  (`wiki/sources/van-der-cruyssen-2024-validation.md`); [W4] is the counterexample showing
  what happens with small, densely packed AOIs.

Therefore: **2 or 4 tiles per trial, each ≥ 400 × 300 px, with ≥ 250 px inter-tile gaps and a
dead-zone margin at the array edges.** Array size (2 vs 4) is a manipulated factor, since the
2-tile case is the highest-signal condition and the 4-tile case is the more realistic web
layout. Do not exceed 4. Do not use within-image AOIs (the eyes-versus-nose contrast that
carried much of [C3]'s spatial signal is **not** available at webcam resolution — say so).

### 6.3 Trial structure

```
fixation cross (500 ms, centre)
  → probe array (4000 ms free viewing, no response required)
  → cover-task prompt (self-paced)
```

The 4000 ms window is chosen to span both phases of the effect: the early orienting window
(roughly 0.7–2 s) and the later window, which can **reverse in sign**. Pre-register which
window scores each feature. Averaging across the reversal is the most likely way to null out
a real effect.

**The cover task is a design variable, not decoration.** [C2] establishes that task demands
determine whether familiarity-driven gaze can be suppressed, and that memory-dependent tasks
are the most robust. For a covert web attack the cover task must additionally look like
ordinary content. Run two cover tasks as a manipulated factor:

- **Low-demand / naturalistic:** "pick the image that best fits this article" — maximally
  plausible as web content, weaker per [C2].
- **Memory-adjacent / naturalistic:** "which of these have you seen on this site before?" —
  a plausible onboarding or preference prompt that happens to impose the memory demand [C2]
  identifies as countermeasure-resistant.

Reporting the difference between them is a contribution in its own right: it tells an
attacker (and a defender) **which page designs make the oracle work**.

### 6.4 Counterbalancing — the RQ0 control

Every item appears as **familiar for half the participants and unfamiliar for the other
half**, assigned by Latin square. This is the structural core of the design:

- Item saliency, colour, complexity, and semantic category are held constant across the
  familiarity contrast.
- Screen position is randomized per trial, so AOI position cannot carry familiarity.
- Calibration error, lighting, seating, tracker, and logging cadence are constant within a
  trial and therefore constant across the AOIs being compared.

The three RQ0 nulls (§5) are all computable from this design without extra collection: the
shuffled-label null permutes familiarity within participant; the saliency-only baseline
trains on item identity and position with familiarity withheld.

### 6.5 The three experiments

**E1 — Mechanism and internal validity (run first).**
Experimenter-installed familiarity. A study phase exposes item set A; a probe phase presents
A-items against matched novel items. Delay is manipulated **between participants** at
immediate / ~20 minutes / ~1 week. Ground truth is perfect and the manipulation is strong.
This experiment answers RQ0, RQ1, and RQ3, and produces the memory-decay curve. If RQ0 fails
here, stop the direction.
*Target N ≈ 40 (roughly 13 per delay cell), 40 trials each.*

**E2 — The attack: naturally acquired familiarity (the headline).**
Probe items are logos and homepage screenshots of real web services spanning high, medium,
and low expected penetration. Ground truth comes from a **post-hoc questionnaire** collected
*after* all gaze data ("which of these do you have an account with / visit at least monthly /
have never used"), so the labels cannot contaminate the viewing. Optionally, and only with
separate explicit consent, a **voluntary browser-history export** of top visited domains
gives an objective label; treat self-report as primary and history as a validation subset,
since the history export is a real recruitment deterrent.
Counterbalancing here is *statistical rather than assigned* — the design cannot control who
uses which service — so E2 leans on (a) the E1-validated mechanism, (b) per-item random
effects in the model, and (c) the item-level shuffled-label null. **State this weakening
explicitly; it is the honest gap between E1 and E2.**
*Target N ≈ 40, 40 trials each.*

**E3 — Sensitive-category exposure (the punchline, ethically scoped).**
Content cards spanning health, finance, legal, and civic topics, probing prior exposure to a
topic rather than to a specific document. Labels from consented self-report only. **Do not
probe protected characteristics** (sexual orientation, religion, immigration status) even
though the method would apply: the demonstration does not require them, and including them
converts a privacy paper into an ethics problem. Report E3 as a bounded demonstration that
the oracle generalizes from brands to topics, not as a profiling system.
*Target N ≈ 40, 20 trials each.*

### 6.6 Conditions matrix

| Axis | Levels |
|---|---|
| Experiment | E1 lab-installed / E2 real-world / E3 topic |
| Tracker arm | Gazepoint IR (ceiling) / WebGazer / WebEyeTrack / EyeGestures |
| Array size | 2 tiles / 4 tiles |
| Cover task | low-demand / memory-adjacent |
| Awareness | naive / instructed countermeasures (RQ4) |
| Delay (E1 only) | immediate / ~20 min / ~1 week |
| Aggregation | k = 1, 5, 10, 20, 40 trials |
| Defense (RQ5) | none / spatial coarsening / temporal jitter / dwell DP |

Headline cell: **E2, naive, on-device webcam, 4 tiles, memory-adjacent cover task, k = 20.**

### 6.7 Participants and ethics

N ≈ 40 per experiment, single session, ~30 minutes. The study operates under the existing
TAMU IRB-exempt determination (D4 plan A.6), but D7 raises two issues D4 does not:

- **Deception.** The cover task conceals the measurement's purpose. This is standard in the
  CIT literature but requires a **debriefing** that discloses what was measured and offers
  data withdrawal. Write the debrief script before collection.
- **The E2/E3 labels are themselves sensitive.** Service usage and topic exposure are the
  very data the attack extracts. Store labels separately from gaze streams under a random
  participant code, never in `data/`, and never in the wiki. Note that D4 plan §20 step 8
  already flags an unresolved data-hygiene problem: **29 real participant sessions tracked in
  git with the `.gitignore` rule commented out.** Resolve that before D7 collection starts,
  not after.

---

## 7. Features, models, and metrics

### 7.1 AOI assignment under gaze error

This is the methodological crux and deserves its own subsection in the paper. With 2–4° of
angular error, hard nearest-AOI assignment discards information and injects bias. Use
**soft assignment**: weight each gaze sample's contribution to AOI *j* by a Gaussian kernel
centred on the sample, with per-participant bandwidth **estimated from that participant's own
calibration residual**. Samples falling in the inter-tile gap contribute partially to both
neighbours rather than being dropped or forced. Report results under both hard and soft
assignment; if the effect only survives under soft assignment, say so.

### 7.2 Feature set (AOI-anchored, coarse-spatial or purely temporal)

Per trial, per AOI:

- **Dwell proportion** — share of trial time allocated to the AOI (the novelty-preference
  measure [W1]).
- **Mean fixation duration** and **first fixation duration** — the countermeasure-resistant
  family [C1], [C3]. Purely temporal; immune to spatial error.
- **First-fixation target and latency** — [M1] locates the effect within the first five
  fixations, so an early-window feature is expected to carry disproportionate weight.
- **Number of AOI visits / revisits** and **number of distinct AOIs visited** — [C3] found
  "areas visited" discriminative under countermeasures.
- **Time-to-first-fixation** on each AOI.
- **Early-window vs late-window dwell split** (0.7–2 s vs 2–4 s) — captures the sign
  reversal rather than averaging it away.
- **Scanpath entropy** across AOIs.

Features are computed **relative within trial** (each AOI's value normalized by the trial's
AOI mean), which cancels per-participant and per-session scale differences — including the
logged-cadence confound that contaminates D4 (D4 plan §9).

### 7.3 Models

- **Primary:** mixed-effects logistic regression predicting familiarity from AOI features,
  with random intercepts for participant **and item**. Interpretable, appropriate at this N,
  and the random item intercept is what makes the E2 saliency argument defensible.
- **Secondary:** gradient-boosted trees on the same features, evaluated with
  **leave-one-participant-out** cross-validation. Never split within participant.
- **Aggregation:** per-user score = mean per-trial score over k trials; sweep k.
- Deliberately **not** an end-to-end deep model. At 1,600 trials it would overfit, and the
  interpretability of "which feature family survives" is the point of RQ4 and RQ5.

### 7.4 Metrics

- **Per-trial AUC** (comparable to the CIT literature's per-item AUCs [C3]).
- **Per-user AUC as a function of k** — the headline curve, and the D7 analogue of D4's
  accuracy-versus-observation-window curve. Quotable form: *"how many tiles before a page
  knows which sites you use."*
- **TPR at FPR = 0.1** — the security-relevant operating point. An attacker profiling a
  population cares about the low-false-positive regime, not balanced accuracy.
- **d′** per feature family, for comparability with the psychology literature.
- **Baselines:** chance (0.5); the saliency-and-position-only baseline (RQ0); and, as the
  external contrast, a clearable canvas/UA fingerprint [44]–[46] — which reveals *device*, not
  *knowledge*, and resets on a clear.

---

## 8. Composition with D2/D4, and the defense

The three directions compose into a single adversary that is more than the sum of its parts,
and the composition is worth one figure and one paragraph in whichever paper lands first:

- **D4** supplies a stateless, person-bound pseudonymous identity that survives clearing.
- **D2** supplies what that person is examining and considering right now.
- **D7** supplies what that person already knew when they arrived.

A tracker holding all three has a persistent identifier attached to both a live intent
signal and a prior-knowledge profile, none of which the user can clear, and only one of
which (the camera indicator) they can observe. **Stating the composition is free; the paper
should not attempt to demonstrate all three at once.**

For the defense (RQ5), the composition also sharpens the mitigation argument. Gaze
perturbation proposals [47], [48], [49] were designed against *identity* leakage. D7 asks
whether they hold against *knowledge* leakage, and §5 RQ5 predicts a specific failure:
spatial coarsening does not touch fixation duration, which is the channel [C1] and [C3]
identify as intent-independent and countermeasure-resistant. **Showing that an existing
gaze-privacy defense leaves the recognition channel open is a clean, self-contained result**
and a good fallback if the attack numbers underwhelm.

---

## 9. Related work and the exact gap this fills

### 9.1 The eye-movement memory effect — the mechanism

- **Althoff & Cohen 1999 [M1]** — the foundational demonstration: distinct sampling of
  famous versus non-famous faces across processing tasks, with the effect present **within
  the first five fixations**. This is the source of the attack's short-window feasibility.
- **Hannula et al. 2010 [M2]** — the review establishing that the effect is an obligatory
  consequence of prior exposure, arises rapidly, and **does not require conscious
  recollection**. This is the citation for "involuntary," which is what makes it a leak
  rather than a disclosure.
- **Shimojo et al. 2003 [M3]** — the gaze cascade effect: gaze shifts toward the
  eventually-chosen option in preference decisions. Adjacent rather than central; it is the
  basis of a possible *preference*-probing variant, and it is one of the three effects [W1]
  replicated online.

### 9.2 The ocular Concealed Information Test — the instrument being repurposed

- **Schwedes & Wentura 2012 [C1]** — six-face arrays; fixation duration revealed memory
  **regardless of the intention to reveal or conceal**; concealed knowledge detected in 65%
  of relevant trials. The cleanest "intent does not gate the signal" result.
- **Nahari, Lancry-Dayan, Ben-Shakhar & Pertzov 2019 [C2]** — four-face parallel arrays,
  n = 61. **Task demands decide suppressibility:** in a visual detection task countermeasures
  worked; in a memory-dependent task, avoidance of the familiar face persisted *even under
  explicit instruction to conceal*. This paper is the direct source of §6.3's cover-task
  manipulation.
- **Millen & Hancock 2019 [C3]** — AUC 0.67–0.87; mean fixation duration robust under
  countermeasures (d = 0.91) while the fine spatial signal collapsed (d = 1.40 → −0.12).
  Source of the RQ4 hypothesis and of the temporal-versus-spatial feature split.
- **Rosenzweig & Bonneh 2020 [C4]** — 88% classification, AUC 0.84 in the target-unknown
  case. **Cite as a ceiling, never as a template:** it rests on microsaccade reaction times
  under 1 Hz RSVP with 10 ms flashes, which requires 500–1000 Hz sampling and is
  categorically unavailable at webcam rates. Naming this explicitly pre-empts a reviewer
  asking why the webcam numbers are so much lower.
- **Zangrossi et al. 2024 [C5]** — autobiographical IAT plus fixation topography; **75%
  accuracy from the eye measure alone** on memories one week old, mock-crime paradigm,
  n = 68. Evidence that the effect survives realistic delays.
- **Lancry-Dayan et al. 2018 [C6]** and **Van der Cruyssen et al. 2024 (CIT leakage) [C7]** —
  the same group's adjacent CIT work. *Citations not yet verified — see §11.*

### 9.3 Webcam feasibility — why this is deployable, not hypothetical

- **Van der Cruyssen et al. 2024 [W1]** — replicated the **novelty preference** (n = 45)
  online with WebGazer.js against an EyeLink 1000 Plus reference, alongside the cascade
  effect (n = 134) and the visual world paradigm (n = 32). Effect sizes shrank **20–27%**;
  the lab-versus-online contrast in Study 3 was 71% versus 52% fixations to target. This is
  the single most important feasibility citation in the direction, and it also defines the
  workable stimulus geometry (§6.2). **It is already in the wiki** as
  `sources/van-der-cruyssen-2024-validation.md`.
- **Semmelmann & Weigelt 2018 [W2]**, **Yang & Krajbich 2021 [W3]** — the broader
  webcam-validation argument (`wiki/concepts/webcam-tracking-validation.md`): ~3.94° offset
  online, 20–30 ms temporal resolution.
- **Thilderkvist & Dobslaw 2024 [W4]** — the honest counterpoint and the origin of the I-DT
  requirement (§6.1). Bounds fine-AOI reading, **not** the coarse-array design used here.
  Address it directly in the paper rather than waiting for a reviewer to raise it.

### 9.4 Web privacy — the threat-model home

- **Weinberg et al. 2011 [5]** — history sniffing via `:visited` and interaction side
  channels. Already in the project bibliography, and the rhetorical anchor: D7 is the same
  capability relocated below the layer browsers patched.
- **The decade privacy review [P1]** — the source for "recognition and knowledge inference
  is not among the risks the field has systematically studied." *Author list unverified — see
  §11. Do not stake the gap claim on this citation until the PDF is read.*
- **Kröger et al. 2020 [21]**, **Katsini et al. 2020 [3]**, **Liebling & Preibusch 2014 [6]**
  — the gaze-privacy framing and the opacity argument.
- **EyeTell [27]**, **GazeRevealer [8]**, **GAZEploit [14]** — the content-dependent contrast
  class: all target a secret being **entered**, none targets a memory already **held**.

### 9.5 The gap, stated for the introduction

> The eye-movement memory effect is established in cognitive psychology; the ocular
> Concealed Information Test is an established forensic instrument on infrared hardware;
> webcam eye-tracking has been validated for exactly the recognition paradigm this attack
> uses. No prior work combines them into an **adversarial capability**: a webpage that
> silently determines what its visitor has seen before, on a commodity webcam, against an
> unwitting user who — unlike every subject in the CIT literature — applies no
> countermeasures because they do not know they are being tested. The novelty is the
> intersection of instrument (recognition oracle), sensor (commodity webcam), setting
> (covert drive-by web), and framing (knowledge extraction as a web privacy attack).

---

## 10. Risks, honest limitations, and the reviewer traps

| Risk | Severity | Mitigation |
|---|---|---|
| **Scoop risk from the CIT group.** Van der Cruyssen, Ben-Shakhar, Pertzov, and Verschuere have both the CIT expertise [C2] and the webcam validation [W1]. They are one reframing away from this paper. | **High** | Their venue and framing are psychology and forensic assessment; ours is security and a threat model with a defense. Move on E1 quickly. Do not delay for a large N. |
| **E2 is much weaker than E1.** Lab-installed familiarity is a strong manipulation; "has an account on this site" is weak, confounded with demographics, and cannot be assigned. | **High** | Per-item random effects; item-level shuffled null; report E1 and E2 separately and never let E1 numbers stand in for the attack claim. Pre-register the E2 fallback: high-salience item classes only. |
| Effect sizes shrink 20–27% online [W1], on top of an IR ceiling of AUC 0.67–0.87 [C3]. Per-trial webcam AUC may land near 0.60. | Medium | The per-user aggregation curve (§7.4) is the answer, and it is the honest one: a weak per-trial signal integrated over 20 tiles is still an oracle. Frame absolute numbers as a lower bound, as the D4 plan does. |
| **Sign reversal.** Familiarity produces *preference* in some paradigms and *avoidance* in others ([C2] reports avoidance), and the early/late windows can differ. | Medium | Pre-register per-window, per-feature directional predictions. Use two-sided tests and report direction as a finding. Do not average across the reversal. |
| Microsaccade-based CIT results [C4] are unreachable at 30 Hz. | Low | State it in the paper before a reviewer does; it is a sensor bound, not a flaw. |
| Cover-task ecological validity: a lab array may not resemble real web content. | Medium | The two-level cover-task manipulation (§6.3) *is* the ecological-validity test. Report both. |
| Deception plus sensitive labels. | Medium | Debrief script, separated label storage, no protected characteristics in E3, and fix the D4 plan §20 step 8 data-hygiene issue first. |
| "This is just the CIT on a worse sensor." | **The likely reviewer one-liner** | Answer on the page, as the D4 plan does in A.1: the contribution is the *covert, unwitting, adversary-chosen* setting where countermeasures do not apply (RQ4 quantifies exactly this), plus the commodity sensor, plus the defense. |

**Fallback ladder.** If E2 underwhelms: (1) lead with E1's mechanism-plus-decay result and
the RQ4 countermeasure-advantage number, framed as "the capability exists and the covert
setting is where it is strongest"; (2) lead with RQ5's negative result — existing gaze-privacy
defenses do not close the recognition channel — which is self-contained and does not depend
on a strong attack number; (3) narrow E2 to high-salience brand recognition, which is a
scoped but real advertising-privacy threat.

---

## 11. References and citation status

*Per `wiki/SCHEMA.md`, the canonical shared bibliography is `GazePry_ReID_Research_Plan.md`
§21, entries [1]–[54]. Bracket numbers below in the plain `[n]` form refer to that shared
numbering. The **M / C / W / P labels are doc-local** to this document — they are **not**
shared numbering and must not be cited as such elsewhere. Merging them into §21 as [55]–…
is a deliberate follow-up step (§12), matching how [50]–[54] were added.*

**Verification status.** Citations [M1]–[M3], [C1]–[C5], and [W1] were retrieved and
bibliographically verified by web lookup on 2026-07-22 (authors, venue, volume, DOI). They
are grounded in **abstracts, PMC full text, and publisher metadata — not a full PDF read** in
every case; a deep-read pass is a follow-up. [C6], [C7], and [P1] are **unverified** and are
marked inline. **Do not quote an unverified entry in a draft.**

**Correction recorded during verification:** Millen & Hancock [C3] was initially attributed
in session to *Scientific Reports*. It is **Cognitive Research: Principles and
Implications** 4(23). Note that [C2] and [C3] are both in that journal, volume 4, with
adjacent DOIs (0162-7 and 0169-0) — an easy pair to confuse.

### Memory and gaze (new to the project)

- **[M1]** R. R. Althoff and N. J. Cohen, "Eye-Movement-Based Memory Effect: A Reprocessing
  Effect in Face Perception," *Journal of Experimental Psychology: Learning, Memory, and
  Cognition*, vol. 25, no. 4, pp. 997–1010, Jul. 1999. *(Peer-reviewed. Effect within the
  first five fixations.)*
- **[M2]** D. E. Hannula, R. R. Althoff, D. E. Warren, L. Riggs, N. J. Cohen, and J. D. Ryan,
  "Worth a Glance: Using Eye Movements to Investigate the Cognitive Neuroscience of Memory,"
  *Frontiers in Human Neuroscience*, vol. 4, art. 166, 2010, doi: 10.3389/fnhum.2010.00166.
  *(Peer-reviewed review. Effect does not require conscious recollection.)*
- **[M3]** S. Shimojo, C. Simion, E. Shimojo, and C. Scheier, "Gaze bias both reflects and
  influences preference," *Nature Neuroscience*, vol. 6, no. 12, pp. 1317–1322, 2003,
  doi: 10.1038/nn1150. *(Peer-reviewed. The gaze cascade effect.)*

### Ocular Concealed Information Test (new to the project)

- **[C1]** L. Schwedes and D. Wentura, "The revealing glance: Eye gaze behavior to concealed
  information," *Memory & Cognition*, 2012, doi: 10.3758/s13421-011-0173-1.
  *(Peer-reviewed. Fixation duration reveals memory regardless of intent to conceal;
  concealed knowledge detected in 65% of relevant trials; six-face arrays.)*
- **[C2]** T. Nahari, O. Lancry-Dayan, G. Ben-Shakhar, and Y. Pertzov, "Detecting concealed
  familiarity using eye movements: the role of task demands," *Cognitive Research: Principles
  and Implications*, vol. 4, art. 10, 2019, doi: 10.1186/s41235-019-0162-7. *(Peer-reviewed.
  n = 61; four-face parallel arrays; memory-dependent tasks resist countermeasures.)*
- **[C3]** A. E. Millen and P. J. B. Hancock, "Eye see through you! Eye tracking unmasks
  concealed face recognition despite countermeasures," *Cognitive Research: Principles and
  Implications*, vol. 4, art. 23, 2019, doi: 10.1186/s41235-019-0169-0. *(Peer-reviewed.
  n = 48; AUC 0.67–0.87; fixation duration survives countermeasures at d = 0.91.)*
- **[C4]** G. Rosenzweig and Y. S. Bonneh, "Concealed information revealed by involuntary eye
  movements on the fringe of awareness in a mock terror experiment," *Scientific Reports*,
  vol. 10, art. 14355, 2020, doi: 10.1038/s41598-020-71487-9. *(Peer-reviewed. n = 25;
  88% classification, AUC 0.84 target-unknown. **Microsaccades at RSVP rates — an IR ceiling,
  not reproducible on a webcam.**)*
- **[C5]** A. Zangrossi, L. C. Gatto, V. Lanfranchi, C. Scarpazza, M. Celli, and G. Sartori,
  "Autobiographical implicit association test and eye movements: fixations topography enables
  detection of autobiographical memories," *Frontiers in Psychology*, vol. 15, art. 1268256,
  2024, doi: 10.3389/fpsyg.2024.1268256. *(Peer-reviewed. n = 68; eye measure alone 75%
  accuracy; one-week-old mock-crime memories.)*
- **[C6]** O. Lancry-Dayan, T. Nahari, G. Ben-Shakhar, and Y. Pertzov, *(2018, title and venue
  to verify)* — countermeasure instructions attenuate initial orienting to familiar faces but
  concealed recognition is detected via overt avoidance. **⚠ CITATION UNVERIFIED — retrieve
  before citing.**
- **[C7]** I. Van der Cruyssen, G. Ben-Shakhar, Y. Pertzov, and B. Verschuere, "Detecting
  Concealed Familiarity Using Eye Movements: The Effect of Leakage of Mock Crime Details to
  Innocents," *(2024, venue and DOI to verify)*. **⚠ CITATION UNVERIFIED — retrieve before
  citing.** Directly relevant to the scoop risk in §10.

### Webcam feasibility (already in the project wiki; cite author-year)

- **[W1]** I. Van der Cruyssen, G. Ben-Shakhar, Y. Pertzov, N. Guy, Q. Cabooter,
  L. J. Gunschera, and B. Verschuere, "The validation of online webcam-based eye-tracking:
  The replication of the cascade effect, the novelty preference, and the visual world
  paradigm," *Behavior Research Methods*, vol. 56, no. 5, pp. 4836–4849, 2024,
  doi: 10.3758/s13428-023-02221-2. *(Peer-reviewed. Wiki page:
  `sources/van-der-cruyssen-2024-validation.md`. Novelty preference n = 45; effect sizes
  shrank 20–27%; stimulus geometry 472 × 331 px, 295 px apart.)*
- **[W2]** T. Semmelmann and S. Weigelt, "Online webcam-based eye tracking in cognitive
  science: A first look," *Behavior Research Methods*, 2018. *(In the wiki.)*
- **[W3]** X. Yang and I. Krajbich, "Webcam-based online eye-tracking for behavioral
  research," *Judgment and Decision Making*, 2021. *(In the wiki.)*
- **[W4]** A. Thilderkvist and F. Dobslaw, "On current limitations of online eye-tracking to
  study the visual processing of source code," *Information and Software Technology*, 2024.
  *(In the wiki. Origin of the I-DT requirement.)*
- **[W5]** "What Paradigms Can Webcam Eye-Tracking Be Used For? Attempted Replications of Five
  Cognitive Science Experiments," *Collabra: Psychology*, vol. 11, no. 1, 2025. **⚠ AUTHORS,
  ARTICLE NUMBER, AND DOI UNVERIFIED** (publisher returned 403). Worth retrieving: a
  five-paradigm replication attempt directly bounds which designs webcam gaze supports.

### Eye-tracking privacy (new to the project)

- **[P1]** "A Data-Driven Review of a Decade of Privacy Research in Eye Tracking,"
  *Proceedings of the ACM on Human-Computer Interaction*, 2025, doi: 10.1145/3806024.
  **⚠ AUTHOR LIST UNVERIFIED** (ACM DL returned 403). Reviews 78 papers, 2015–2025, via
  ensemble topic modelling; reports that normative work emphasizes inference of identity and
  personal traits as the unresolved risk while technical work treats privacy as a
  computational problem. **Retrieve the PDF through the university library before using it to
  support the §3 gap claim.**

### From the shared bibliography (`GazePry_ReID_Research_Plan.md` §21)

[3] Katsini et al. 2020 · [5] Weinberg et al. 2011 · [6] Liebling & Preibusch 2014 ·
[8] Wang et al. 2020 · [14] Wang et al. 2024 · [21] Kröger et al. 2020 · [25] Davalos et al.
2025 · [27] Chen et al. 2018 · [44]–[46] Acar 2014 / Vastel 2018 / Zimmeck 2017 ·
[47]–[49] Steil 2019 / Li 2021 / David-John 2022.

---

## 12. Immediate next steps

1. **Retrieve and verify the three unverified citations** — [C6], [C7], and [P1], plus [W5] —
   through the university library. [C7] and [P1] are the two that change how §3 and §10 are
   written.
2. **Deep-read the five verified CIT papers** ([C1]–[C5]) end to end. This document is built
   on abstracts, PMC full text, and publisher metadata; the effect directions, exact windows,
   and per-measure AUCs must come from the papers' own tables before anything is
   pre-registered.
3. **Build the probe-array task page and the I-DT detector** (§6.1), with JS↔Python parity
   tests matching the existing `test/features-cli.js` pattern.
4. **Run E1 at N ≈ 12 as a mechanism pilot** — immediate delay only, 2-tile arrays, WebGazer
   plus Gazepoint simultaneous. The single question: does RQ0 clear? Nothing else matters
   until it does.
5. **Pre-register** the conditions matrix (§6.6), the per-window directional predictions
   (§10, sign-reversal risk), and the metrics (§7.4) before E2.
6. **Resolve the data-hygiene blocker** (D4 plan §20 step 8) before any D7 collection.
7. **Decide the bibliography merge:** if D7 advances past the E1 pilot, promote [M1]–[M3],
   [C1]–[C7], and [P1] into the shared §21 numbering as [55]–…, then re-sync the wiki — the
   same flow used for [50]–[54].
8. **Write the debrief script** and the separated-label storage procedure (§6.7) before
   recruiting.
