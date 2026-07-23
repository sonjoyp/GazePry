# The Recognition Oracle

**Extracting What a Visitor Already Knows from Commodity Webcam Gaze**

*A self-contained research plan for a security/privacy conference submission. It
develops a leakage vector whose payload is **memory contents**: what the visitor
has seen, used, or knows. The leak is not a biometric, and it is not the
visitor's current task or intent. It is what they already knew before they
arrived.*

*Within the GazePry project this direction is labelled **D7**. The label is an
internal index only; nothing in this document depends on any other GazePry plan,
and the bibliography in §12 is complete on its own.*

*Every load-bearing claim is attributed. §12 records the peer-reviewed status of
each source and which citations are **not yet verified**.*

---

## Contents

1. [One-paragraph thesis](#1-one-paragraph-thesis)
2. [What leaks, and what does not](#2-what-leaks-and-what-does-not)
3. [The research gap](#3-the-research-gap)
4. [Threat model](#4-threat-model)
5. [Research questions and hypotheses](#5-research-questions-and-hypotheses)
6. [Methodology: apparatus, stimuli, design, and ground truth](#6-methodology-apparatus-stimuli-design-and-ground-truth)
7. [Features, models, and metrics](#7-features-models-and-metrics)
8. [The implemented pipeline](#8-the-implemented-pipeline)
9. [The defense](#9-the-defense)
10. [Related work and the exact gap this fills](#10-related-work-and-the-exact-gap-this-fills)
11. [Risks, honest limitations, and the reviewer traps](#11-risks-honest-limitations-and-the-reviewer-traps)
12. [References and citation status](#12-references-and-citation-status)
13. [Immediate next steps](#13-immediate-next-steps)

---

## 1. One-paragraph thesis

Recognition is **involuntary and it moves the eyes**. Fifty years of memory
research establishes that a previously seen stimulus is sampled differently from
a novel one — the *eye-movement-based memory effect* — that the difference
appears within the **first five fixations** [1], that it does not require
conscious recollection [2], and that it **persists when the viewer is actively
trying to conceal it** [4], [6]. Forensic psychology has spent two decades
turning this into the *ocular Concealed Information Test*, reporting per-item
AUCs of roughly 0.67–0.87 on research-grade infrared hardware [6]. **This work
moves that measurement out of the interrogation room and onto the open web.** A
first-party page that holds a camera grant can render an ordinary-looking array
of tiles — faces, brand marks, photographs, document thumbnails — and read, from
dwell asymmetry alone, **which of them the visitor has seen before**. The
contribution is to reframe a mature *forensic assessment instrument* as a
*covert web extraction attack*, and to show that the covert setting is **strictly
easier than the forensic one**: the entire countermeasure literature that bounds
the CIT assumes a subject who knows they are being tested, and a drive-by web
visitor does not. The concrete harm is that a webpage learns which services you
use, which brands and people you have encountered, and which sensitive topics
you have prior exposure to — **with no click, no typing, no cookie, and no
stored state** — resurrecting, at the perception layer, exactly the capability
browsers spent a decade removing from the rendering layer [16].

---

## 2. What leaks, and what does not

The payload is **stored memory**. That is worth stating precisely, because gaze
is known to leak several different things and they are routinely conflated.

| | What it leaks | Tense | Does the adversary choose the stimulus? |
|---|---|---|---|
| Keystroke/PIN inference from gaze [21], [22], [23] | The secret being **entered right now** | Present | No — it watches a keyboard |
| Interest / intent profiling | What the visitor is **examining now** | Present | No — observational |
| Gaze biometrics and re-identification | A persistent **identity** | Timeless | No — observational |
| Demographic and trait inference [18] | A **property of the person** | Timeless | No — observational |
| **This work** | **Prior exposure and knowledge** | **Past** | **Yes — it designs the array** |

Two structural features separate this from all of the above.

**It is interventional, not observational.** Every attack in the table above
takes whatever the user happens to look at and infers from it. Here the adversary
**designs the stimulus**. That is what makes it an *oracle* rather than a
profiler: the attacker asks a specific question ("has this person seen this?"),
gets a per-item answer, and can ask many questions in sequence.

**It is not a biometric, and it is not clearable.** The leak is not an
identifier, so the usual mitigations (clearing storage, resetting a fingerprint,
declining a cookie) do not apply. There is nothing to clear: the state being read
is in the visitor's head.

**Why this is empirically tractable.** The effect is a **within-participant,
within-session, within-trial contrast between AOIs on the same screen**.
Calibration geometry, lighting, seating, screen size, tracker identity, and
logging cadence are all *constant across the AOIs being compared*, so none of
them can produce a familiar-versus-unfamiliar difference. With **item-level
counterbalancing** (§6.5) each stimulus serves as "familiar" for half the
participants and "unfamiliar" for the other half, so item saliency and screen
position are orthogonal to the contrast by construction. The unit of analysis is
the *AOI within a trial*, not the person, so N ≈ 40 participants × 40 trials is
1,600 observations from a **single** session per participant.

---

## 3. The research gap

Four literatures converge on this space and every one of them stops short of the
attack.

1. **The eye-movement-based memory effect (basic science).** Althoff & Cohen [1]
   showed distinct sampling of famous versus non-famous faces across processing
   tasks, emerging within the first five fixations. Hannula et al. [2] review the
   effect as an obligatory consequence of prior exposure that operates
   independently of conscious recollection. **Framed as a window into memory and
   hippocampal function — never as an extraction channel.**

2. **The ocular Concealed Information Test (forensic).** Schwedes & Wentura [4]
   detected concealed knowledge in 65% of relevant trials from fixation duration
   in a six-face array, *regardless of whether the participant intended to reveal
   or conceal*. Nahari et al. [5] (four-face arrays, n = 61) showed that **task
   demands decide whether the effect can be voluntarily suppressed**, and that
   memory-dependent tasks resist countermeasures. Millen & Hancock [6] reported
   AUC 0.67–0.87, with mean fixation duration surviving deliberate countermeasures
   (d = 0.91 under countermeasures, *higher* than the 0.66 without) even as the
   fine spatial signal collapsed (d = 1.40 → −0.12). Zangrossi et al. [8]
   detected week-old mock-crime memories at 75% from fixation topography alone.
   **All of it assumes a cooperative, institutionally-framed test of a subject
   who knows they are a suspect.**

3. **Webcam eye-tracking validation (methods).** Van der Cruyssen et al. [11]
   replicated the **novelty preference** — the recognition-memory looking
   asymmetry that is precisely this attack's signal — online with WebGazer.js,
   alongside the cascade effect and the visual world paradigm, with effect sizes
   shrinking 20–27%. **Framed as "can we move psychology experiments online," not
   "can a website do this to you."** Note the author list: it includes the same
   Ben-Shakhar and Pertzov who authored [5]. The forensic CIT community has
   already brought its instrument to the webcam. It has not brought it to a
   threat model.

4. **Eye-tracking privacy (security).** The decade review [17] finds that
   normative work flags *inference of identity and personal traits* as the
   unresolved risk while technical work treats privacy as a computational
   problem. The content-dependent gaze attacks in the literature — EyeTell [21],
   Wang et al.'s smartphone password inference [22], GAZEploit [23] — all target
   **secrets being entered right now**. **Nobody targets what is already in the
   visitor's head.**

**The gap = the intersection.** No published work (to our knowledge) (i) treats
the ocular recognition effect as an **adversarial extraction primitive** rather
than an assessment instrument; (ii) instantiates it against an **unwitting**
visitor, where the countermeasure literature that bounds the forensic test does
not apply; (iii) runs it on a **commodity in-browser webcam** as a deployable web
capability and measures the gap to an infrared ceiling on the same subjects; or
(iv) connects it to the **history-sniffing** threat model [16] that browsers have
already accepted as legitimate to defend against. Any one axis alone is prior
work. The stack is the contribution.

**Reframe to lead with:** browsers killed `:visited` history sniffing at the
rendering layer [16]. This attack reinstates the capability one layer below,
where **the side channel is the user rather than the renderer** — and where no
browser patch reaches, because the leak happens before the user decides to
disclose anything.

---

## 4. Threat model

- **Adversary.** A first-party page, or a first-party-included script, holding a
  camera grant. The realistic acquisition paths for that grant are the ones that
  already exist in production: accessibility gaze navigation, remote proctoring,
  attention analytics, WebXR, and gaze-conditioned AI features. The adversary
  needs no cross-origin access and no persistent storage.
- **What makes it *active*.** The adversary **chooses the probe set**. It renders
  an array that looks like ordinary web content (a product carousel, an image
  picker, a "choose your interests" onboarding step, an illustrated article) and
  measures gaze allocation across its own known AOIs. It never needs to ask a
  question or record an answer.
- **Goal.** For each probe item, output a posterior on "this visitor has prior
  exposure to this item." Aggregate into a knowledge profile: which services they
  use, which brands and public figures they have encountered, which sensitive
  topics they have prior exposure to, and — in the strongest form — whether they
  recognise a specific person, document, or place.
- **Why the covert setting is *stronger* than the forensic one.** The CIT
  literature's main limitation is countermeasures: [5] shows a motivated subject
  can suppress the effect in a visual-detection task, and [6] shows only the
  temporal measures survive. **A web visitor who does not know they are being
  tested applies no countermeasures at all.** The attack therefore operates in
  the naive regime, where effects are largest. This inversion is the single most
  important point in the threat model and should be stated in the abstract.
- **There is no permission-free variant.** Unlike attacks that degrade
  gracefully to cursor telemetry, this one needs gaze. State that plainly rather
  than implying a broader reach than the method has.
- **Explicitly out of scope.** Reading another origin's content (blocked by the
  same-origin policy). Word-level or fine-AOI reconstruction: webcam gaze is too
  coarse [14], and [11] bounds the practical design to roughly ≤ 4 well-separated
  regions. Any claim that this is a lie detector, a clinical instrument, or
  admissible evidence: it is a *privacy leak*, and the paper must not drift into
  forensic claims.
- **What the user can observe.** A camera indicator. Nothing else. No network
  request distinguishable from analytics, no storage, no click. Liebling &
  Preibusch [20] is the citation for the core asymmetry: webcam privacy loss is
  legible to users, but **gaze extraction is opaque** — and knowledge extraction
  from gaze is opaque twice over.

---

## 5. Research questions and hypotheses

Each RQ has a directional, falsifiable hypothesis (H) and a decision rule. Every
figure is reported with a confidence interval bootstrapped over **participants**;
δ denotes a pre-registered margin fixed before collection. The headline cell is
**E2, naive condition, on-device webcam, per-item AUC at k = 20 trials**.

- **RQ0 (the gate — is it recognition, or is it the picture?).** Does the
  discriminating signal reflect the *visitor's prior exposure*, rather than
  intrinsic **item saliency**, **screen position**, or a **calibration
  artifact**?
  - **H0.** Under item-level counterbalancing (§6.5), a classifier trained on AOI
    features separates familiar from unfamiliar above chance; under a **shuffled
    familiarity-label null** it collapses to AUC ≈ 0.5; and a
    **saliency-and-position-only** baseline (item identity + AOI position, no
    participant-specific familiarity) performs at chance.
  - **Decision rule.** *Confirmed* if the shuffled-label AUC CI includes 0.5
    **and** the saliency-only baseline CI includes 0.5 **and** the real per-AOI
    AUC CI lower bound > 0.5. **Refuted / stop** otherwise — the effect is a
    property of the images, not of the person, and nothing downstream stands.
    **Run this on E1 before collecting E2 or E3.**

- **RQ1 (mechanism — does the effect survive the commodity sensor?).** With
  experimenter-controlled familiarity (E1), does webcam gaze recover prior
  exposure, and how does accuracy decay with the study-to-probe delay?
  - **H1.** Per-AOI AUC is above chance at every delay, is highest immediately,
    and decays monotonically across immediate / 20-minute / 1-week probes. Webcam
    AUC is below the simultaneous infrared AUC by a positive gap.
  - **Decision rule.** *Confirmed* if the immediate-delay per-AOI AUC CI lower
    bound > 0.5 on at least the best on-device arm. Reference points for scale,
    **not** targets to match: IR per-item AUC 0.67–0.87 [6], and an expected
    20–27% effect-size shrinkage online [11].

- **RQ2 (the attack — does it work on real-world familiarity?).** Does the same
  pipeline recover **naturally acquired** familiarity (E2: the faces, brands, and
  places the visitor has actually encountered) rather than lab-installed
  familiarity?
  - **H2.** Per-item AUC over k = 20 trials exceeds chance and exceeds per-AOI
    AUC (aggregation helps), and the **k-to-threshold curve** reaches a usable
    operating point (TPR ≥ 0.7 at FPR ≤ 0.1) within a session a real site could
    plausibly hold.
  - **Decision rule.** *Confirmed* if the per-item AUC CI lower bound > 0.5 at
    some k ≤ 40. *Narrowed* if only high-salience item classes clear chance —
    still a scoped, meaningful threat. *Refuted* if per-item AUC ≈ 0.5 at every k.
  - This is the headline. It is also the riskiest cell, because lab-installed
    familiarity (E1) is a much stronger manipulation than "has an account at this
    bank."
  - **Secondary, and cheap because the design already carries it:** compare the
    three E2 item classes (§6.4). Faces, brand marks, and landmarks differ in how
    much visual detail they carry and in how many times a familiar viewer has
    seen them, so the per-class AUC ordering is a result in itself and tells an
    attacker which content types make a usable probe.

- **RQ3 (ceiling vs commodity).** What is the AUC gap between the infrared
  ceiling and the on-device webcam arms (WebGazer, WebEyeTrack [30],
  EyeGestures) on the **same** participants and trials, using simultaneous
  capture?
  - **H3.** IR AUC > webcam AUC in every matched cell, with the gap **narrowing**
    as k grows (aggregation absorbs sensor noise).
  - **Decision rule.** The gap magnitude is the deliverable regardless of the
    ordering among webcam trackers. This RQ quantifies; it does not fail.

- **RQ4 (countermeasures — quantifying the covert advantage).** How much does an
  *informed* visitor recover? Compare naive participants against participants
  explicitly instructed to conceal recognition and given a concealment strategy.
  - **H4.** AUC drops under instructed countermeasures but stays above chance,
    and the **surviving signal is temporal** (mean and first fixation duration)
    rather than spatial (dwell proportion) — the pattern [6] reports on infrared
    and [4] reports as intent-independent.
  - **Decision rule.** *Confirmed* if the (naive − countermeasure) AUC difference
    CI excludes 0 **and** the countermeasure-condition AUC CI lower bound > 0.5
    for at least the fixation-duration feature family. This RQ delivers the
    quotable number for the threat model: **the price of not knowing you are
    being measured.**

- **RQ5 (defense).** What client-side mitigation defeats the oracle at acceptable
  utility cost?
  - **H5.** There is an operating point — AOI-level spatial coarsening, temporal
    jitter of the gaze stream, or per-AOI dwell-proportion differential privacy
    [27], [28] — that pushes attacker AUC toward 0.5 while a legitimate
    gaze-navigation or attention-analytics utility task stays within a
    pre-registered bound.
  - **Decision rule.** *Confirmed* if some operating point reduces AUC by ≥ δ_priv
    with utility degradation ≤ δ_util. Report the full privacy–utility curve
    regardless. Note the structural asymmetry worth reporting: defenses that
    quantize **space** may leave the **fixation-duration** channel intact, which
    is exactly the channel [6] found countermeasure-resistant. A defense that
    only coarsens AOIs is likely insufficient, and demonstrating that is itself a
    result.

---

## 6. Methodology: apparatus, stimuli, design, and ground truth

### 6.1 Apparatus

A tracker-agnostic browser harness with self-registering adapters, a `{t, x, y}`
stream contract, and a zero-dependency ingest server. Four capture arms:

| Arm | Role |
|---|---|
| Gazepoint (infrared, 60 Hz) | **Ceiling.** A measurement instrument, never a training signal. |
| WebGazer.js | Commodity baseline; the tracker the published novelty-preference replication used [11]. |
| WebEyeTrack [30] | On-device few-shot personalisation arm. |
| EyeGestures | Second on-device arm. |

The infrared channel is captured **simultaneously** with a webcam arm on the same
participant and the same trials, so RQ3 is a within-subject contrast rather than
a comparison across cohorts. The one control that makes this legitimate: **the IR
stream is never used to train, calibrate, or correct the webcam features.** It is
only ever a second measurement of the same eye.

**Fixation segmentation is load-bearing and is not the usual algorithm.** A
velocity-threshold detector (I-VT) is unreliable at webcam sample rates, and [14]
introduced a **dispersion-threshold (I-DT)** algorithm specifically because none
existed for low-frequency webcam data. Fixation *duration* is this direction's
countermeasure-resistant feature, so the segmentation is validated against the
simultaneous infrared channel before any per-feature number is believed.

### 6.2 Stimulus geometry (sourced constraints, not guesses)

The array design is pinned by two published bounds:

- [11] replicated the novelty preference online with **two images of 472 × 331 px
  separated by 295 px**. That is the demonstrated-workable geometry on WebGazer.
- The practical webcam ceiling is roughly **≤ 4 well-separated regions of
  interest**; [14] is the counterexample showing what happens with small, densely
  packed AOIs.

Therefore: **2 or 4 tiles per trial, each ≥ 400 × 300 px, with ≥ 250 px
inter-tile gaps and a dead-zone margin at the array edges.** Array size (2 vs 4)
is a manipulated factor, since the 2-tile case is the highest-signal condition
and the 4-tile case is the more realistic web layout. Do not exceed 4. Do not use
within-image AOIs: the eyes-versus-nose contrast that carried much of [6]'s
spatial signal is **not** available at webcam resolution, and the paper should say
so rather than let a reviewer notice it.

The task page **refuses to run** below this geometry rather than silently
shrinking the tiles, because data collected outside the validated envelope is not
comparable to anything published.

**Tile shape is part of the geometry, not a detail of styling.** The tile is held
at the 4:3 aspect of the stimulus canvas and grown only until it hits the
limiting dimension; surplus viewport becomes outer margin, never a wider gap. A
tile of some other shape can only be filled by cropping the stimulus, and a
centre crop of a portrait photograph removes the face — the participant then
free-views a collar for 4000 ms and the trial scores as an ordinary null. Off-4:3
images are letterboxed inside the tile, and the drawn rectangle is recorded per
trial (`aois[].imageRect`) alongside the AOI rectangle itself.

### 6.3 Trial structure

```
fixation cross (500 ms, centre)
  → probe array (4000 ms free viewing, no response required)
  → cover-task prompt (self-paced)
  → blank (300 ms)
```

The 4000 ms window is chosen to span both phases of the effect: the early
orienting window (roughly 0.7–2 s) and the later window, which can **reverse in
sign**. Pre-register which window scores each feature. Averaging across the
reversal is the most likely way to null out a real effect.

**The cover task is a design variable, not decoration.** [5] establishes that
task demands determine whether familiarity-driven gaze can be suppressed, and
that memory-dependent tasks are the most robust. For a covert web attack the
cover task must additionally look like ordinary content. Two cover tasks are run
as a manipulated factor:

- **Low-demand / naturalistic:** *"Which image best fits the section you just
  read?"* — maximally plausible as web content, weaker per [5].
- **Memory-adjacent / naturalistic:** *"Which of these have you seen on this site
  before?"* — a plausible onboarding or preference prompt that happens to impose
  the memory demand [5] identifies as countermeasure-resistant.

Reporting the difference between them is a contribution in its own right: it
tells an attacker (and a defender) **which page designs make the oracle work**.

### 6.4 The stimulus packs

Three packs, described by a single manifest that the browser task page and the
offline analysis both read, so the item table cannot drift between what was shown
and what is scored.

**E1 — 24 generated Julia-set fractals.** Abstract *on purpose*. E1's validity
depends on the participant having **no prior exposure**, so that familiarity is
created only by the study phase and the ground truth is exact. Photographs of
real things fail that test: everyone has seen a beach, a dog, a keyboard, and the
"novel" items would carry uncontrolled pre-existing familiarity that no
counterbalancing removes. Richly detailed novel abstract images are the standard
stimulus class for recognition-memory work for this reason. The generator
enforces two properties a naive fractal dump lacks: histogram-equalised escape
time plus an orbit-trapped interior (so the images are detailed rather than a
dark field with a bright rim), and a **mutual-distinctiveness check in colour**
so that no "novel" tile resembles a studied one. The achieved minimum pairwise
distance is recorded in the manifest.

**E2 — 24 real images in three classes of eight.** These are things the
participant has or has not genuinely encountered in ordinary life:

| Class | Contents | Why it is in the set |
|---|---|---|
| `face` | Eight public figures, spanning globally famous to nationally or professionally famous | The stimulus class the entire ocular-CIT literature uses [1], [4], [5], [6]; maximum visual detail |
| `bank` | Eight retail-bank and payment wordmarks | The closest analogue to the history-sniffing payload [16]: *which financial services do you use* |
| `landmark` | Eight widely photographed places, spanning universal to regional | High-detail photographs whose exposure varies by travel and background rather than by account ownership |

Each class spans high, medium, and low expected penetration, recorded per item as
a `tier`. The tier is a **hypothesis about the cohort, not a label**; the ground
truth is always the post-hoc questionnaire (§6.6).

**Arrays are drawn within a class, never across it.** A trial showing one face
among three bank marks would let the probe be identified by *category* rather
than by familiarity, and would add category-driven saliency variance to a
contrast that is otherwise between four visually comparable tiles. The published
ocular-CIT arrays are all-faces for the same reason. This is enforced in the
trial builder and pinned by tests on both the browser and analysis sides.

Faces and marks carry **no on-tile caption**. A caption would let the participant
read the name instead of recognising the image, which is a different memory
system from the one the effect rests on.

**E3 — 16 topic cards across health, finance, legal, and civic.** Probing prior
exposure to a *topic* rather than to a specific image. Two things must be said
plainly about E3:

- **It is a weaker construct than E1 and E2, and not merely a weaker
  manipulation.** E1 and E2 rely on the participant having seen *that stimulus*,
  which is what the eye-movement memory effect actually predicts. A topic card
  the participant has never seen before cannot carry an episodic trace no matter
  how familiar the topic is; what it can carry is *semantic* familiarity with the
  subject matter. Treat E3 as a bounded demonstration that the oracle extends
  from specific items to topics, report it separately, and never let an E3 number
  stand in for the E1/E2 mechanism.
- **It excludes protected characteristics.** No sexual orientation, religion, or
  immigration status, even though the method would apply. The demonstration does
  not require them and including them converts a privacy paper into an ethics
  problem. The scoping is asserted by a test on each side so it cannot drift back
  in later.

E3 stimuli are **not sourced yet** and the task page therefore refuses to collect
E3. See §8 for what a valid E3 asset is.

### 6.5 Counterbalancing — the RQ0 control

Every item appears as **familiar for half the participants and unfamiliar for the
other half**, assigned by a Latin square over four counterbalance groups derived
from the participant number. This is the structural core of the design:

- Item saliency, colour, complexity, and semantic category are held constant
  across the familiarity contrast.
- Screen position is randomised per trial, so AOI position cannot carry
  familiarity.
- Calibration error, lighting, seating, tracker, and logging cadence are constant
  within a trial and therefore constant across the AOIs being compared.

Each trial pairs exactly **one** familiar-role item (the probe) with (arrayN − 1)
unfamiliar-role irrelevants, which is the array-CIT structure of [4] and [5].
Probe items are cycled rather than sampled with replacement, so every item is
used a near-equal number of times.

Two consequences that look like implementation detail and are not:

- **Participant IDs must be sequential** (`P01`, `P02`, …). The group is derived
  from the participant number, so sequential IDs spread the cohort evenly across
  the four groups. Non-numeric IDs fall back to a hash, group sizes drift apart
  at small N, the per-item marginal probability of "familiar" stops being 0.5
  across the cohort, and item identity starts carrying information about
  familiarity — which is exactly what the RQ0 saliency baseline exists to catch.
- **A class must be a contiguous block whose size is a multiple of the number of
  groups.** The square is applied over the global item index, so a block of eight
  splits exactly 4 familiar / 4 unfamiliar for *every* group, which is what
  guarantees each class can always fill a 4-tile array. A class that violates
  this fails to build a trial mid-session rather than at startup, so the
  stimulus checker enforces it.

The three RQ0 nulls (§5) are all computable from this design without extra
collection: the shuffled-label null permutes familiarity within participant; the
saliency-only baseline trains on item identity and position with familiarity
withheld.

### 6.6 Ground truth

**E1: the counterbalance assignment.** Familiarity is installed in the lab by a
study phase that runs *before* gaze capture starts, so familiarisation gaze never
enters the recording window. Ground truth is exact.

**E2 and E3: a post-hoc questionnaire, and nothing else.** Familiarity here is
whatever the participant brought with them; the counterbalance role is only a
slot-assignment device and scoring against it would be scoring a label the design
never controlled. The analysis **refuses to run** on E2/E3 without questionnaire
labels rather than falling back to the counterbalance flag.

The questionnaire is collected **after** all gaze data, never before: asking
first tells the participant what is being measured. It stores **raw ordinals**
(0–3), never a derived boolean, so the familiar/unfamiliar cut stays a reportable
analysis choice instead of an irreversible property of the data. The default cut
is ≥ 2, "has genuine prior exposure". Level 1 ("heard of it, never used it";
"looks familiar, cannot place them") is deliberately *below* the cut: brand
recognition without use, or a face that is vaguely familiar, is a much weaker
memory trace and lumping it in would inflate the positive class with cases the
mechanism does not predict.

Each E2 class gets its own wording, because "how do you use this service" is
meaningless for a face and wrong for a place, but the **ordinal semantics are
held constant across classes** so that one threshold applies to the whole
experiment. An unanswered item is **dropped, not defaulted to unfamiliar**: a
blank is participant fatigue, not evidence of unfamiliarity.

*Optional and only with separate explicit consent:* a voluntary browser-history
export of top visited domains gives an objective label for the `bank` class.
Treat self-report as primary and history as a validation subset — the export is a
real recruitment deterrent.

Counterbalancing in E2/E3 is **statistical rather than assigned**: the design
cannot control who banks where. E2 therefore leans on (a) the E1-validated
mechanism, (b) per-item random effects in the model, and (c) the item-level
shuffled-label null. **State this weakening explicitly; it is the honest gap
between E1 and E2.**

### 6.7 The three experiments

**E1 — Mechanism and internal validity (run first).** Experimenter-installed
familiarity. A study phase exposes the participant's familiar-role set; the probe
phase presents those items against matched novel ones. Delay is manipulated
**between participants** at immediate / ~20 minutes / ~1 week. This experiment
answers RQ0, RQ1, and RQ3, and produces the memory-decay curve. **If RQ0 fails
here, stop the direction.**
*Target N ≈ 40 (roughly 13 per delay cell), 40 trials each.*

**E2 — The attack: naturally acquired familiarity (the headline).** Faces, bank
marks, and landmarks, class-homogeneous arrays, ground truth from the post-hoc
questionnaire. Answers RQ2 and RQ4.
*Target N ≈ 40, 40 trials each.*

**E3 — Topic exposure (bounded demonstration).** Content cards spanning health,
finance, legal, and civic topics. Labels from consented self-report only. Report
as a bounded demonstration that the oracle generalises from items to topics,
with the construct caveat in §6.4 stated in the paper, not as a profiling system.
*Target N ≈ 40, 20 trials each.*

### 6.8 Conditions matrix

| Axis | Levels |
|---|---|
| Experiment | E1 lab-installed / E2 real-world / E3 topic |
| Tracker arm | Gazepoint IR (ceiling) / WebGazer / WebEyeTrack / EyeGestures |
| Array size | 2 tiles / 4 tiles |
| Cover task | low-demand / memory-adjacent |
| Awareness | naive / instructed countermeasures (RQ4) |
| Delay (E1 only) | immediate / ~20 min / ~1 week |
| E2 item class | face / bank / landmark |
| Aggregation | k = 1, 5, 10, 20, 40 trials |
| Defense (RQ5) | none / spatial coarsening / temporal jitter / dwell DP |

Headline cell: **E2, naive, on-device webcam, 4 tiles, memory-adjacent cover
task, k = 20.**

### 6.9 Participants and ethics

N ≈ 40 per experiment, single session, ~30 minutes. The study operates under an
existing institutional exempt determination. Two issues need operational
handling:

- **Deception.** The cover task conceals the measurement's purpose. This is
  standard in the CIT literature and necessary here — telling participants
  converts every session into the RQ4 countermeasure condition — but it obliges a
  **debriefing** that discloses what was measured and offers data withdrawal. The
  debrief script is written before collection starts, not after, and delivery is
  recorded on the participant log.
- **The E2/E3 labels are themselves sensitive.** Service usage and topic exposure
  are the very data the attack extracts. Labels are stored in a separate
  directory from the gaze streams, under a random participant code, and neither
  is ever committed. Recruit for demographic spread where possible: a narrow
  cohort makes it harder to argue the effect is individual recognition rather
  than shared cohort-level familiarity, which matters most in E2.

---

## 7. Features, models, and metrics

### 7.1 AOI assignment under gaze error

This is the methodological crux and deserves its own subsection in the paper.
With 2–4° of angular error, hard nearest-AOI assignment discards information and
injects bias. Use **soft assignment**: weight each gaze sample's contribution to
AOI *j* by a Gaussian kernel centred on the sample, with per-participant
bandwidth **estimated from that participant's own calibration residual**. Samples
falling in the inter-tile gap contribute partially to both neighbours rather than
being dropped or forced. Report results under both hard and soft assignment; if
the effect only survives under soft assignment, say so.

### 7.2 Feature set (AOI-anchored, coarse-spatial or purely temporal)

Per trial, per AOI:

- **Dwell proportion** — share of trial time allocated to the AOI (the
  novelty-preference measure [11]).
- **Mean fixation duration** and **first fixation duration** — the
  countermeasure-resistant family [4], [6]. Purely temporal; immune to spatial
  error.
- **First-fixation target and latency** — [1] locates the effect within the first
  five fixations, so an early-window feature is expected to carry
  disproportionate weight.
- **Number of AOI visits / revisits** and **number of distinct AOIs visited** —
  [6] found "areas visited" discriminative under countermeasures.
- **Time-to-first-fixation** on each AOI.
- **Early-window vs late-window dwell split** (0.7–2 s vs 2–4 s) — captures the
  sign reversal rather than averaging it away.
- **Scanpath entropy** across AOIs.

Features are computed **relative within trial** (each AOI's value normalised by
the trial's AOI mean), which cancels per-participant and per-session scale
differences, including differences in logged sample cadence between trackers.

### 7.3 Models

- **Primary:** mixed-effects logistic regression predicting familiarity from AOI
  features, with random intercepts for participant **and item**. Interpretable,
  appropriate at this N, and the random item intercept is what makes the E2
  saliency argument defensible.
- **Secondary:** gradient-boosted trees on the same features, evaluated with
  **leave-one-participant-out** cross-validation. Never split within participant:
  a model that has seen the same person's other trials is measuring memorisation
  of that person, not recognition.
- **Aggregation:** per-item score = mean per-trial score over k trials; sweep k.
- Deliberately **not** an end-to-end deep model. At ~1,600 trials it would
  overfit, and the interpretability of "which feature family survives" is the
  point of RQ4 and RQ5.

### 7.4 Metrics

- **Per-AOI AUC** (comparable to the CIT literature's per-item AUCs [6]).
- **Per-item AUC as a function of k** — the headline curve. Quotable form: *"how
  many tiles before a page knows which bank you use."*
- **Probe-identification accuracy** — top-1 within a trial, chance = 1/arrayN.
- **TPR at FPR = 0.1** — the security-relevant operating point. An attacker
  profiling a population cares about the low-false-positive regime, not balanced
  accuracy.
- **d′ per feature family**, for comparability with the psychology literature.
- **Baselines:** chance (0.5); the saliency-and-position-only baseline (RQ0); and,
  as the external contrast, a clearable canvas/UA fingerprint [24]–[26] — which
  reveals *device*, not *knowledge*, and resets on a clear.

**Report intervals, never point estimates**, and bootstrap them over
**participants**. Resampling rows would treat 40 trials from one person as 40
independent observations and produce an interval far too tight to believe.

### 7.5 Two failure modes that must never be silent

Both are pinned by regression tests, because both produce output that reads as a
negative result rather than as a bug:

- **A trial that cannot be scored returns null, not a zero-filled row**, and a
  metric with a missing class returns `nan`, not 0.5. Zeros masquerade as data
  and score as chance.
- **If the fixation detector finds no fixations** — which is what a lab-grade
  dispersion threshold does to webcam-noise data — every fixation-derived feature
  becomes constant and reports AUC 0.500, indistinguishable from "no effect". The
  analysis reports fixations-per-trial on every run and warns below 1.0.

---

## 8. The implemented pipeline

The harness, protocol, stimulus packs, and analysis exist and are test-covered.
This section is the reproducibility record: what runs, in what order, and which
parts refuse rather than degrade.

### 8.1 End-to-end order of operations

| # | Step | Command / page | Refuses when |
|---|---|---|---|
| 1 | Generate the packs and the manifest | `npm run d7:stimuli` | a class cannot fill an array for every counterbalance group |
| 2 | Install the real E2 assets | `npm run d7:stimuli:fetch` | a source is not on the free-licence allow-list |
| 3 | Validate the packs | `npm run d7:stimuli:check`, `npm run d7:stimuli:verify` | a file is missing, undersized, or no longer matches its lock hash |
| 4 | Verify the analysis end to end | `npm run d7:verify` | the synthetic effect dataset fails RQ0, or the null dataset passes it |
| 5 | Serve the harness | `node server.js` | — |
| 6 | Identify, calibrate, rate calibration | hub page | — |
| 7 | Run the probe | `tasks/probe.html` | the viewport is below the validated geometry, or the set still holds placeholders |
| 8 | **E2/E3 only:** collect the questionnaire | `questionnaire.html` | no probe session exists for that participant/session/experiment |
| 9 | Check the participant's quality flags | operator dashboard | — |
| 10 | Score | `analysis/recognition.py` | E2/E3 are scored without questionnaire labels |

Steps 7, 8, and 10 refuse rather than warn on purpose. A cohort collected against
placeholder stimuli, a questionnaire answered before the probe, or an E2 scored
against the counterbalance role are all unrecoverable after the fact, and by the
time anyone reads a warning the participants have gone home.

### 8.2 Everything exists twice, in JavaScript and Python

The browser needs the live task; the analysis needs the offline numbers. The
trial protocol, the fixation detector, and the feature extractor are therefore
implemented in both languages and held together by **parity tests** that run the
JavaScript through thin CLIs and compare the full result against the Python. The
PRNG is reproduced bit-identically in Python by explicit uint32 masking, so a
participant's entire trial plan — item ids, familiarity roles, slot order — is
reproducible from their participant ID alone, in either language.

If a feature, a threshold, or the protocol changes, **both sides change in the
same commit**. The parity tests fail otherwise, and that is the point.

### 8.3 Stimulus sourcing and provenance

E2's assets are real third-party images, which raises three problems that the
tooling handles rather than leaves to discipline:

- **Licensing.** Every asset is fetched from Wikimedia Commons and checked
  against an allow-list of free licences (public domain, CC0, CC BY, CC BY-SA,
  FAL) using the licence Commons itself reports. Anything else is **refused and
  not downloaded**. Most retail-bank wordmarks qualify because a plain wordmark is
  below the threshold of originality for copyright. This is a copyright test
  only: showing a mark to identify the thing it denotes is normally nominative
  use, but that is a judgement for the authors and their institution, not
  something a script settles.
- **Reproducibility.** A source list records *which person, brand, or place* each
  item denotes; a lock file records what was actually resolved, its licence, and
  the SHA-256 of the bytes written. A later fetch reuses the pinned file, and an
  offline verify re-checks the hashes. Two cohorts collected months apart
  therefore provably saw the same stimuli, or the discrepancy is surfaced.
- **Presentation uniformity.** Wordmarks have wildly different aspect ratios;
  dropped straight into a 4:3 tile the browser would scale each to a different
  apparent size, which is an item-saliency difference dressed up as a stimulus.
  Every mark is composited at the same margin onto the same canvas, so the only
  thing varying across a bank array is which bank it is.

Attribution is regenerated from the lock on every fetch, so the credit list
cannot drift from what is on disk. It is what a paper's stimulus figure cites.

**The images are never committed.** Only the design (item table, manifest),
the sources, the lock, and the attribution are. E1's fractals *are* committed:
they are generated from recorded seeds and carry no third-party rights.

### 8.4 What a valid E3 asset is

E3 remains unsourced and therefore blocked. The bar it has to clear, before
anyone spends a cohort on it:

The card must be something a person plausibly **encountered before**, not merely
something that depicts a familiar subject. A generated illustration of a mortgage
carries no episodic trace for anyone, so the contrast would rest entirely on
semantic familiarity with the phrase in the caption. Real, widely circulated
topic material clears the bar: standard government and agency forms, public
information posters, and the recognisable article-card formats of major outlets.
Whatever is chosen, the construct caveat in §6.4 still applies and belongs in the
paper.

### 8.5 Data handling

| What | Where | Committed? |
|---|---|---|
| Gaze streams | session directory | **never** |
| Questionnaire labels | a *separate* directory | **never** |
| Participant log (code ↔ consent/debrief) | offline, on paper | never in the repo |

Labels live outside the gaze directory deliberately: service usage and topic
exposure are exactly the information the attack claims to extract, so they are
the most sensitive thing the study holds, and the separation means a careless
bulk add of the data directory cannot sweep them in. Never put a participant's
name, email, or the code↔identity mapping in the repository.

---

## 9. The defense

Gaze-perturbation proposals [27], [28], [29] were designed against *identity*
leakage. RQ5 asks whether they hold against *knowledge* leakage, and §5 predicts
a specific failure: **spatial coarsening does not touch fixation duration**,
which is the channel [4] and [6] identify as intent-independent and
countermeasure-resistant.

**Showing that an existing gaze-privacy defense leaves the recognition channel
open is a clean, self-contained result** — and it is the right fallback if the
attack numbers underwhelm, because it does not depend on a strong attack number
to be publishable.

The mitigation surface worth evaluating, in increasing cost to legitimate uses:

1. **Spatial coarsening** — quantise reported gaze to a grid coarser than the
   AOIs. Cheap, and predicted insufficient on its own.
2. **Temporal jitter** — perturb sample timestamps, degrading fixation-duration
   estimates. Predicted to be the effective one, and the expensive one: dwell
   timing is what gaze-navigation dwell-click depends on.
3. **Per-AOI dwell-proportion differential privacy** [27], [28] — a principled
   budget, reported as a privacy–utility curve rather than a single operating
   point.
4. **Permission-level** — a rate-limited or coarse-by-default gaze permission,
   distinct from the camera permission, so that granting a camera for a video
   call does not silently grant gaze.

Report the full curve for each, and report the negative results.

---

## 10. Related work and the exact gap this fills

### 10.1 The eye-movement memory effect — the mechanism

- **Althoff & Cohen 1999 [1]** — the foundational demonstration: distinct
  sampling of famous versus non-famous faces across processing tasks, with the
  effect present **within the first five fixations**. This is the source of the
  attack's short-window feasibility.
- **Hannula et al. 2010 [2]** — the review establishing that the effect is an
  obligatory consequence of prior exposure, arises rapidly, and **does not
  require conscious recollection**. This is the citation for "involuntary", which
  is what makes it a leak rather than a disclosure.
- **Shimojo et al. 2003 [3]** — the gaze cascade effect: gaze shifts toward the
  eventually-chosen option in preference decisions. Adjacent rather than central;
  it is the basis of a possible *preference*-probing variant, and it is one of
  the three effects [11] replicated online.

### 10.2 The ocular Concealed Information Test — the instrument being repurposed

- **Schwedes & Wentura 2012 [4]** — six-face arrays; fixation duration revealed
  memory **regardless of the intention to reveal or conceal**; concealed
  knowledge detected in 65% of relevant trials. The cleanest "intent does not
  gate the signal" result.
- **Nahari, Lancry-Dayan, Ben-Shakhar & Pertzov 2019 [5]** — four-face parallel
  arrays, n = 61. **Task demands decide suppressibility:** in a visual detection
  task countermeasures worked; in a memory-dependent task, avoidance of the
  familiar face persisted *even under explicit instruction to conceal*. The
  direct source of §6.3's cover-task manipulation.
- **Millen & Hancock 2019 [6]** — AUC 0.67–0.87; mean fixation duration robust
  under countermeasures (d = 0.91) while the fine spatial signal collapsed
  (d = 1.40 → −0.12). Source of the RQ4 hypothesis and of the
  temporal-versus-spatial feature split.
- **Rosenzweig & Bonneh 2020 [7]** — 88% classification, AUC 0.84 in the
  target-unknown case. **Cite as a ceiling, never as a template:** it rests on
  microsaccade reaction times under 1 Hz RSVP with 10 ms flashes, which requires
  500–1000 Hz sampling and is categorically unavailable at webcam rates. Naming
  this explicitly pre-empts a reviewer asking why the webcam numbers are so much
  lower.
- **Zangrossi et al. 2024 [8]** — autobiographical IAT plus fixation topography;
  **75% accuracy from the eye measure alone** on memories one week old,
  mock-crime paradigm, n = 68. Evidence that the effect survives realistic
  delays.
- **Lancry-Dayan et al. 2018 [9]** and **Van der Cruyssen et al. 2024 (CIT
  leakage) [10]** — the same group's adjacent CIT work. *Citations not yet
  verified — see §12.*

### 10.3 Webcam feasibility — why this is deployable, not hypothetical

- **Van der Cruyssen et al. 2024 [11]** — replicated the **novelty preference**
  (n = 45) online with WebGazer.js against an EyeLink 1000 Plus reference,
  alongside the cascade effect (n = 134) and the visual world paradigm (n = 32).
  Effect sizes shrank **20–27%**; the lab-versus-online contrast in Study 3 was
  71% versus 52% fixations to target. The single most important feasibility
  citation here, and the source of the stimulus geometry in §6.2.
- **Semmelmann & Weigelt 2018 [12]**, **Yang & Krajbich 2021 [13]** — the broader
  webcam-validation argument: roughly 3.94° offset online, 20–30 ms temporal
  resolution.
- **Thilderkvist & Dobslaw 2024 [14]** — the honest counterpoint and the origin
  of the I-DT requirement (§6.1). Bounds fine-AOI reading, **not** the coarse
  array design used here. Address it directly in the paper rather than waiting
  for a reviewer to raise it.

### 10.4 Web and gaze privacy — the threat-model home

- **Weinberg et al. 2011 [16]** — history sniffing via `:visited` and interaction
  side channels. The rhetorical anchor: this attack is the same capability
  relocated below the layer browsers patched.
- **The decade privacy review [17]** — the source for "recognition and knowledge
  inference is not among the risks the field has systematically studied."
  *Author list unverified — see §12. Do not stake the §3 gap claim on this
  citation until the PDF is read.*
- **Kröger et al. 2020 [18]**, **Katsini et al. 2020 [19]**, **Liebling &
  Preibusch 2014 [20]** — the gaze-privacy framing and the opacity argument.
- **EyeTell [21]**, **Wang et al. 2020 [22]**, **GAZEploit [23]** — the
  content-dependent contrast class: all target a secret being **entered**, none
  targets a memory already **held**.
- **Acar et al. 2014 [24]**, **Vastel et al. 2018 [25]**, **Zimmeck et al. 2017
  [26]** — the fingerprinting contrast: device identity, and clearable.
- **Steil et al. 2019 [27]**, **Li et al. 2021 [28]**, **David-John et al. 2022
  [29]** — the gaze-privacy defenses evaluated in RQ5.

### 10.5 The gap, stated for the introduction

> The eye-movement memory effect is established in cognitive psychology; the
> ocular Concealed Information Test is an established forensic instrument on
> infrared hardware; webcam eye-tracking has been validated for exactly the
> recognition paradigm this attack uses. No prior work combines them into an
> **adversarial capability**: a webpage that silently determines what its visitor
> has seen before, on a commodity webcam, against an unwitting user who — unlike
> every subject in the CIT literature — applies no countermeasures because they
> do not know they are being tested. The novelty is the intersection of
> instrument (recognition oracle), sensor (commodity webcam), setting (covert
> drive-by web), and framing (knowledge extraction as a web privacy attack).

---

## 11. Risks, honest limitations, and the reviewer traps

| Risk | Severity | Mitigation |
|---|---|---|
| **Scoop risk from the CIT group.** Van der Cruyssen, Ben-Shakhar, Pertzov, and Verschuere have both the CIT expertise [5] and the webcam validation [11]. They are one reframing away from this paper. | **High** | Their venue and framing are psychology and forensic assessment; ours is security, with a threat model and a defense. Move on E1 quickly. Do not delay for a large N. |
| **E2 is much weaker than E1.** Lab-installed familiarity is a strong manipulation; "has an account at this bank" is weak, confounded with demographics and nationality, and cannot be assigned. | **High** | Per-item random effects; item-level shuffled null; report E1 and E2 separately and never let E1 numbers stand in for the attack claim. Pre-register the E2 fallback: high-salience item classes only. |
| **Cohort-level familiarity masquerading as individual recognition.** If every participant is a US student, the same bank marks are familiar to all of them and the "individual" signal is a cohort constant. | **High** | The item classes are chosen to span nationality (US, UK, Nordic, Spanish banks; regional landmarks; nationally-famous faces), and recruitment targets demographic spread. Report per-class variance in the self-report labels as evidence the contrast actually varies within the cohort. |
| Effect sizes shrink 20–27% online [11], on top of an IR ceiling of AUC 0.67–0.87 [6]. Per-AOI webcam AUC may land near 0.60. | Medium | The per-item aggregation curve (§7.4) is the answer, and it is the honest one: a weak per-trial signal integrated over 20 tiles is still an oracle. Frame absolute numbers as a lower bound. |
| **Sign reversal.** Familiarity produces *preference* in some paradigms and *avoidance* in others ([5] reports avoidance), and the early/late windows can differ. | Medium | Pre-register per-window, per-feature directional predictions. Use two-sided tests and report direction as a finding. Do not average across the reversal. |
| **E3's construct is weaker than E1/E2's**, in kind and not only in degree (§6.4). | Medium | Report E3 separately, with the episodic-versus-semantic caveat stated. Do not let an E3 number support the mechanism claim. Leave E3 blocked until its stimuli clear the bar in §8.4. |
| Microsaccade-based CIT results [7] are unreachable at 30 Hz. | Low | State it in the paper before a reviewer does; it is a sensor bound, not a flaw. |
| Cover-task ecological validity: a lab array may not resemble real web content. | Medium | The two-level cover-task manipulation (§6.3) *is* the ecological-validity test. Report both. |
| Deception plus sensitive labels. | Medium | Debrief script written before collection, separated label storage, no protected characteristics in E3. |
| Third-party marks and portraits as stimuli. | Low | Free-licence-only sourcing with a machine-checked allow-list, per-item provenance, and generated attribution (§8.3). Images are not redistributed with the code. |
| **"This is just the CIT on a worse sensor."** | **The likely reviewer one-liner** | Answer it on the page: the contribution is the *covert, unwitting, adversary-chosen* setting where countermeasures do not apply (RQ4 quantifies exactly this), plus the commodity sensor, plus the defense. |

**Fallback ladder.** If E2 underwhelms: (1) lead with E1's mechanism-plus-decay
result and the RQ4 countermeasure-advantage number, framed as "the capability
exists and the covert setting is where it is strongest"; (2) lead with RQ5's
negative result — existing gaze-privacy defenses do not close the recognition
channel — which is self-contained and does not depend on a strong attack number;
(3) narrow E2 to its highest-penetration class, which is a scoped but real
advertising- and finance-privacy threat.

---

## 12. References and citation status

This bibliography is **complete and local to this document**. Numbers are not
shared with any other plan.

**Verification status.** [1]–[8] and [11] were retrieved and bibliographically
verified by web lookup on 2026-07-22 (authors, venue, volume, DOI). They are
grounded in **abstracts, PMC full text, and publisher metadata — not a full PDF
read** in every case; a deep-read pass is a follow-up (§13). [9], [10], [15], and
[17] are **unverified** and are marked inline. **Do not quote an unverified entry
in a draft.**

**Correction recorded during verification:** Millen & Hancock [6] was initially
attributed in session to *Scientific Reports*. It is **Cognitive Research:
Principles and Implications** 4(23). Note that [5] and [6] are both in that
journal, volume 4, with adjacent DOIs (0162-7 and 0169-0) — an easy pair to
confuse.

### Memory and gaze

- **[1]** R. R. Althoff and N. J. Cohen, "Eye-Movement-Based Memory Effect: A
  Reprocessing Effect in Face Perception," *Journal of Experimental Psychology:
  Learning, Memory, and Cognition*, vol. 25, no. 4, pp. 997–1010, Jul. 1999.
  *(Peer-reviewed. Effect within the first five fixations.)*
- **[2]** D. E. Hannula, R. R. Althoff, D. E. Warren, L. Riggs, N. J. Cohen, and
  J. D. Ryan, "Worth a Glance: Using Eye Movements to Investigate the Cognitive
  Neuroscience of Memory," *Frontiers in Human Neuroscience*, vol. 4, art. 166,
  2010, doi: 10.3389/fnhum.2010.00166. *(Peer-reviewed review. Effect does not
  require conscious recollection.)*
- **[3]** S. Shimojo, C. Simion, E. Shimojo, and C. Scheier, "Gaze bias both
  reflects and influences preference," *Nature Neuroscience*, vol. 6, no. 12,
  pp. 1317–1322, 2003, doi: 10.1038/nn1150. *(Peer-reviewed. The gaze cascade
  effect.)*

### Ocular Concealed Information Test

- **[4]** L. Schwedes and D. Wentura, "The revealing glance: Eye gaze behavior to
  concealed information," *Memory & Cognition*, 2012,
  doi: 10.3758/s13421-011-0173-1. *(Peer-reviewed. Fixation duration reveals
  memory regardless of intent to conceal; concealed knowledge detected in 65% of
  relevant trials; six-face arrays.)*
- **[5]** T. Nahari, O. Lancry-Dayan, G. Ben-Shakhar, and Y. Pertzov, "Detecting
  concealed familiarity using eye movements: the role of task demands,"
  *Cognitive Research: Principles and Implications*, vol. 4, art. 10, 2019,
  doi: 10.1186/s41235-019-0162-7. *(Peer-reviewed. n = 61; four-face parallel
  arrays; memory-dependent tasks resist countermeasures.)*
- **[6]** A. E. Millen and P. J. B. Hancock, "Eye see through you! Eye tracking
  unmasks concealed face recognition despite countermeasures," *Cognitive
  Research: Principles and Implications*, vol. 4, art. 23, 2019,
  doi: 10.1186/s41235-019-0169-0. *(Peer-reviewed. n = 48; AUC 0.67–0.87;
  fixation duration survives countermeasures at d = 0.91.)*
- **[7]** G. Rosenzweig and Y. S. Bonneh, "Concealed information revealed by
  involuntary eye movements on the fringe of awareness in a mock terror
  experiment," *Scientific Reports*, vol. 10, art. 14355, 2020,
  doi: 10.1038/s41598-020-71487-9. *(Peer-reviewed. n = 25; 88% classification,
  AUC 0.84 target-unknown. **Microsaccades at RSVP rates — an IR ceiling, not
  reproducible on a webcam.**)*
- **[8]** A. Zangrossi, L. C. Gatto, V. Lanfranchi, C. Scarpazza, M. Celli, and
  G. Sartori, "Autobiographical implicit association test and eye movements:
  fixations topography enables detection of autobiographical memories,"
  *Frontiers in Psychology*, vol. 15, art. 1268256, 2024,
  doi: 10.3389/fpsyg.2024.1268256. *(Peer-reviewed. n = 68; eye measure alone 75%
  accuracy; one-week-old mock-crime memories.)*
- **[9]** O. Lancry-Dayan, T. Nahari, G. Ben-Shakhar, and Y. Pertzov, *(2018,
  title and venue to verify)* — countermeasure instructions attenuate initial
  orienting to familiar faces but concealed recognition is detected via overt
  avoidance. **⚠ CITATION UNVERIFIED — retrieve before citing.**
- **[10]** I. Van der Cruyssen, G. Ben-Shakhar, Y. Pertzov, and B. Verschuere,
  "Detecting Concealed Familiarity Using Eye Movements: The Effect of Leakage of
  Mock Crime Details to Innocents," *(2024, venue and DOI to verify)*.
  **⚠ CITATION UNVERIFIED — retrieve before citing.** Directly relevant to the
  scoop risk in §11.

### Webcam eye-tracking feasibility

- **[11]** I. Van der Cruyssen, G. Ben-Shakhar, Y. Pertzov, N. Guy, Q. Cabooter,
  L. J. Gunschera, and B. Verschuere, "The validation of online webcam-based
  eye-tracking: The replication of the cascade effect, the novelty preference,
  and the visual world paradigm," *Behavior Research Methods*, vol. 56, no. 5,
  pp. 4836–4849, 2024, doi: 10.3758/s13428-023-02221-2. *(Peer-reviewed. Novelty
  preference n = 45; effect sizes shrank 20–27%; stimulus geometry 472 × 331 px,
  295 px apart.)*
- **[12]** T. Semmelmann and S. Weigelt, "Online webcam-based eye tracking in
  cognitive science: A first look," *Behavior Research Methods*, 2018.
  *(Peer-reviewed.)*
- **[13]** X. Yang and I. Krajbich, "Webcam-based online eye-tracking for
  behavioral research," *Judgment and Decision Making*, 2021. *(Peer-reviewed.)*
- **[14]** A. Thilderkvist and F. Dobslaw, "On current limitations of online
  eye-tracking to study the visual processing of source code," *Information and
  Software Technology*, 2024. *(Peer-reviewed. Origin of the I-DT requirement.)*
- **[15]** "What Paradigms Can Webcam Eye-Tracking Be Used For? Attempted
  Replications of Five Cognitive Science Experiments," *Collabra: Psychology*,
  vol. 11, no. 1, 2025. **⚠ AUTHORS, ARTICLE NUMBER, AND DOI UNVERIFIED**
  (publisher returned 403). Worth retrieving: a five-paradigm replication attempt
  directly bounds which designs webcam gaze supports.

### Web and eye-tracking privacy

- **[16]** Z. Weinberg, E. Y. Chen, P. R. Jayaraman, and C. Jackson, "I Still Know
  What You Visited Last Summer: Leaking Browsing History via User Interaction and
  Side Channel Attacks," in *2011 IEEE Symp. Security and Privacy*, IEEE,
  May 2011, pp. 147–161, doi: 10.1109/SP.2011.23.
- **[17]** "A Data-Driven Review of a Decade of Privacy Research in Eye Tracking,"
  *Proceedings of the ACM on Human-Computer Interaction*, 2025,
  doi: 10.1145/3806024. **⚠ AUTHOR LIST UNVERIFIED** (ACM DL returned 403).
  Reviews 78 papers, 2015–2025, via ensemble topic modelling; reports that
  normative work emphasises inference of identity and personal traits as the
  unresolved risk while technical work treats privacy as a computational problem.
  **Retrieve the PDF through the university library before using it to support
  the §3 gap claim.**
- **[18]** J. L. Kröger, O. H.-M. Lutz, and F. Müller, "What Does Your Gaze Reveal
  About You? On the Privacy Implications of Eye Tracking," in *Privacy and
  Identity Management. Data for Better Living: AI and Privacy*, Springer, 2020,
  pp. 226–241, doi: 10.1007/978-3-030-42504-3_15.
- **[19]** C. Katsini, Y. Abdrabou, G. E. Raptis, M. Khamis, and F. Alt, "The Role
  of Eye Gaze in Security and Privacy Applications: Survey and Future HCI
  Research Directions," in *Proc. 2020 CHI Conf. Human Factors in Computing
  Systems*, CHI '20, ACM, Apr. 2020, pp. 1–21, doi: 10.1145/3313831.3376840.
- **[20]** D. J. Liebling and S. Preibusch, "Privacy considerations for a
  pervasive eye tracking world," in *Proc. 2014 ACM Int. Joint Conf. Pervasive
  and Ubiquitous Computing: Adjunct Publication*, ACM, Sep. 2014, pp. 1169–1177,
  doi: 10.1145/2638728.2641688.

### Content-dependent gaze attacks (the contrast class)

- **[21]** Y. Chen, T. Li, R. Zhang, Y. Zhang, and T. Hedgpeth, "EyeTell:
  Video-Assisted Touchscreen Keystroke Inference from Eye Movements," in *2018
  IEEE Symp. Security and Privacy (SP)*, IEEE, May 2018, pp. 144–160,
  doi: 10.1109/SP.2018.00010.
- **[22]** Y. Wang, W. Cai, T. Gu, and W. Shao, "Your Eyes Reveal Your Secrets: An
  Eye Movement Based Password Inference on Smartphone," *IEEE Trans. Mobile
  Computing*, vol. 19, no. 11, pp. 2714–2730, Nov. 2020,
  doi: 10.1109/TMC.2019.2934690.
- **[23]** H. Wang, Z. Zhan, H. Shan, S. Dai, M. Panoff, and S. Wang, "GAZEploit:
  Remote Keystroke Inference Attack by Gaze Estimation from Avatar Views in VR/MR
  Devices," in *Proc. 2024 ACM SIGSAC Conf. Computer and Communications
  Security*, CCS '24, ACM, Dec. 2024, pp. 1731–1745,
  doi: 10.1145/3658644.3690285.

### Fingerprinting (the clearable contrast)

- **[24]** G. Acar, C. Eubank, S. Englehardt, M. Juarez, A. Narayanan, and
  C. Diaz, "The Web Never Forgets: Persistent Tracking Mechanisms in the Wild,"
  in *Proc. 2014 ACM SIGSAC Conf. Computer and Communications Security*, CCS '14,
  ACM, Nov. 2014, pp. 674–689, doi: 10.1145/2660267.2660347.
- **[25]** A. Vastel, P. Laperdrix, W. Rudametkin, and R. Rouvoy, "FP-STALKER:
  Tracking Browser Fingerprint Evolutions," in *2018 IEEE Symp. Security and
  Privacy (SP)*, IEEE, May 2018, pp. 728–741, doi: 10.1109/SP.2018.00008.
- **[26]** S. Zimmeck, J. S. Li, H. Kim, S. M. Bellovin, and T. Jebara, "A Privacy
  Analysis of Cross-device Tracking," in *Proc. 26th USENIX Security Symp.
  (USENIX Security 17)*, USENIX Association, Aug. 2017, pp. 1391–1408.

### Gaze-privacy defenses (RQ5)

- **[27]** J. Steil, I. Hagestedt, M. X. Huang, and A. Bulling, "Privacy-aware eye
  tracking using differential privacy," in *Proc. 11th ACM Symp. Eye Tracking
  Research & Applications*, ETRA '19, ACM, Jun. 2019, pp. 1–9,
  doi: 10.1145/3314111.3319915.
- **[28]** J. Li, A. Roy Chowdhury, K. Fawaz, and Y. Kim, "Kalεido: Real-Time
  Privacy Control for Eye-Tracking Systems," in *Proc. 30th USENIX Security Symp.
  (USENIX Security 21)*, USENIX Association, Aug. 2021, pp. 1793–1810.
- **[29]** B. David-John, D. Hosfelt, K. Butler, and E. Jain, "For Your Eyes Only:
  Privacy-preserving eye-tracking datasets," in *Proc. 2022 Symp. Eye Tracking
  Research and Applications*, ETRA '22, ACM, Jun. 2022, pp. 1–6,
  doi: 10.1145/3517031.3529618.

### Tracker used as a capture arm

- **[30]** *(arXiv preprint — flagged as such)* E. Davalos et al., "WebEyeTrack:
  Scalable Eye-Tracking for the Browser via On-Device Few-Shot Personalization,"
  arXiv:2508.19544, Aug. 2025, doi: 10.48550/arXiv.2508.19544.

---

## 13. Immediate next steps

1. **Run the E1 mechanism pilot at N ≈ 12** — immediate delay only, 2-tile
   arrays, WebGazer plus simultaneous infrared. The single question: does RQ0
   clear? Nothing else matters until it does. Everything this needs is built and
   test-covered (§8).
2. **Retrieve and verify the four unverified citations** — [9], [10], [15], and
   [17] — through the university library. [10] and [17] are the two that change
   how §3 and §11 are written.
3. **Deep-read the verified CIT papers** ([4]–[8]) end to end. This document is
   built on abstracts, PMC full text, and publisher metadata; the effect
   directions, exact windows, and per-measure AUCs must come from the papers' own
   tables before anything is pre-registered.
4. **Pre-register** the conditions matrix (§6.8), the per-window directional
   predictions (§11, sign-reversal risk), and the metrics (§7.4) before E2.
5. **Validate the I-DT thresholds against the infrared channel** on the pilot
   data, before trusting any fixation-duration number. The pilot is the only
   chance to catch a segmentation threshold that is wrong for this sensor.
6. **Source the E3 stimuli, or drop E3** against the bar in §8.4. It is currently
   blocked, and leaving it blocked is a better outcome than collecting it against
   material that cannot carry the effect.
7. **Write the recruitment plan for demographic spread** before E2, since
   cohort-level familiarity is the highest-severity threat to the headline claim
   (§11).
