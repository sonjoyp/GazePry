# GazePry — Cross-Site Gaze Re-Identification Research Plan

**Cross-Site Gaze Re-Identification as an Unclearable Web Tracking Vector**

*The blueprint for a security/privacy conference submission. This document merges the
GazePry information-leakage threat-model assessment (the background and motivation) with
the Direction-1 re-identification study protocol (the research plan proper) into a single
self-contained plan. Every load-bearing quantitative claim below is attributed to a
specific reference; §21 records the peer-reviewed/preprint status of each and the
corrections made during verification.*

---

## Contents

**Part I — Motivation and background (why re-identification is the contribution)**
1. [Overview](#1-overview)
2. [Scope and definitions](#2-scope-and-definitions)
3. [Two regimes of gaze-based information leakage](#3-two-regimes-of-gaze-based-information-leakage)
4. [Leakage vectors (D1–D6) and why D4 is the target](#4-leakage-vectors-d1d6-and-why-d4-is-the-target)
5. [What tightens and what loosens the threat model](#5-what-tightens-and-what-loosens-the-threat-model)

**Part II — The research plan (cross-site gaze re-identification)**
6. [Thesis and contributions](#6-thesis-and-contributions)
7. [Threat model](#7-threat-model)
8. [Research questions and hypotheses](#8-research-questions-and-hypotheses)
9. [Apparatus and tracker arms](#9-apparatus-and-tracker-arms)
10. [Participants and sessions](#10-participants-and-sessions)
11. [Stimuli — the multi-"site" design](#11-stimuli--the-multi-site-design)
12. [Features and models](#12-features-and-models)
13. [Conditions matrix](#13-conditions-matrix)
14. [Metrics](#14-metrics)
15. [Analysis plan](#15-analysis-plan)
16. [Defense (optional)](#16-defense-optional)
17. [Risks and mitigations](#17-risks-and-mitigations)

**Part III — Positioning and execution**
18. [Related work and the gap this plan fills](#18-related-work-and-the-gap-this-plan-fills)
19. [Target venues and timeline](#19-target-venues-and-timeline)
- [19a. Current empirical status (read before quoting any number)](#19a-current-empirical-status-read-before-quoting-any-number)
20. [Immediate next steps](#20-immediate-next-steps)
21. [References and citation status](#21-references-and-citation-status)
- [Appendix A — Novelty positioning, threat-model realism, and threats to validity](#appendix-a--novelty-positioning-threat-model-realism-and-threats-to-validity)

---

# Part I — Motivation and background

## 1. Overview

A webcam-based eye tracker leaks a substantial amount of sensitive information, and it
does so on laptops, smartphones, and tablets alike. The leakage is not incidental. Gaze is
a physically grounded signal produced by largely involuntary eye movements, so it carries
information that ordinary software-level privacy defenses — anti-fingerprinting
countermeasures, sandboxing, or value spoofing — do not touch. Because gaze coordinates
derive from physical eye behavior rather than from JavaScript-reported values, they behave
as a hardware-grounded signal that bypasses defenses operating at the script layer. This
is the central premise of GazePry.

Across the published literature, gaze data leaks at least three broad classes of
information: (i) on-screen secrets such as PINs, passwords, and the content a user reads or
searches for [4], [7], [8], [12], [27]; (ii) cognitive and affective state such as
attention, confusion, mind-wandering, and engagement [1], [2], [22], [26]; and (iii)
stable personal attributes and identity such as biometric identity, gender, age, and
geographic origin [10], [20], [21], [29]. A 2020 survey of eye gaze in security and privacy
applications [3] and a dedicated review of the privacy implications of eye tracking [21]
both treat these as well-established, not hypothetical, risk categories.

**This plan commits to one of those classes: behavioral-biometric re-identification (the
"D4" vector below), reframed for the open desktop web.** The reasoning is developed across
Part I and stated as a thesis in §6. In brief: the same-origin policy blocks a script from
reading gaze on *another* site, so the most alarming content-peeking scenarios are not
feasible on the web. But re-identification is *content-independent* — it is carried by
movement dynamics, not by what is on screen — so the same-origin policy does not touch it.
Two first-party sites that embed the same tracking script can link the same visitor by
their gaze, with no cookie and no client-side state. That turns the threat model's own
limitation into the paper's thesis: **gaze as a stateless, person-bound, unclearable web
re-identifier**, and the gap between the research-grade ceiling and the commodity webcam
channel measured on the *same* subjects.

## 2. Scope and definitions

This plan concerns webcam-based eye tracking: software that estimates where a person is
looking using only the ordinary RGB camera built into a laptop, smartphone, or tablet, with
no specialized infrared eye tracker, head-mounted display, or external hardware. The
reference implementations are WebGazer and its derivatives (SearchGazer [4]) and the more
recent, head-pose-aware WebEyeTrack [25], all of which run entirely in the browser.

"Information leakage" means any case in which the gaze signal allows an observer to infer
something the user did not intend to disclose — a secret being typed, the content being
read, a transient mental state, a stable demographic attribute, or a persistent identity.
The assumed adversary is a *drive-by web adversary*: a first-party page or an embedded
third-party script that obtains camera access and runs gaze estimation client-side. This is
deliberately weaker than the adversaries assumed in much of the adjacent literature, which
often presupposes a physically present attacker filming the victim [27], a VR/MR avatar
feed [14], or eyeglass reflections in a video call [19]. The drive-by web setting is what
distinguishes the GazePry threat model and is the gap the project targets.

## 3. Two regimes of gaze-based information leakage

It is useful to separate gaze leakage into two regimes, because they have different
prerequisites, different defenses, and different behavior across form factors.

### 3.1 Content-dependent leakage

In the content-dependent regime, the adversary controls or knows the on-screen layout and
maps gaze coordinates onto that layout to recover what the user is interacting with. If the
page renders a numeric keypad at known coordinates, a fixation sequence over those
coordinates reconstructs the entered digits. EyeTell demonstrated this for touchscreen soft
keyboards from a video of the user's eyes, identifying the correct 4-digit PIN within its
top-5 candidates roughly 65% of the time and within its top-50 roughly 90% of the time, and
the correct Android lock pattern within its top-5 candidates roughly 70% of the time [27].
GazeRevealer achieved comparable results from the smartphone front camera alone, around
77.9% per single digit and 84.4% for a full 6-digit password under ideal conditions [8].
The same principle extends to gaze-based graphical passwords entered via webcam [12], and
to reading and search behavior: SearchGazer was built specifically to identify which area
of interest on a search-results page a visitor is examining in real time [4], and the
Eye-of-the-Typer benchmark characterizes gaze behavior during typing in fine detail [7].
Because this regime depends on a known layout, an attacker-controlled page is the natural
delivery vehicle — **but it is not the direction this plan pursues** (see §5).

### 3.2 Content-independent leakage — the direction this plan takes

In the content-independent regime, the adversary does not need to know what is on screen at
all. The dynamics of eye movement — fixation durations, saccade velocities and amplitudes,
blink patterns, and pupil response — carry information about the person independent of
on-screen content. These dynamics leak cognitive and affective state: webcam-grade eye
tracking has detected mind-wandering and reading-comprehension errors above chance [22], and
gaze has long been used to infer confusion, engagement, and cognitive load in affective
tutoring systems [1], [2] and gaze-aware AI assistants [26]. The same dynamics encode stable
traits and identity. Eye-movement biometrics re-identify individuals: research-grade systems
such as Eye Know You Too reach an equal error rate of about 0.58% on a reading task **when
60 seconds of eye movement are available, rising to about 3.66% with only 5 seconds** [20] —
a window dependence this plan exploits directly (§14). Gaze also leaks demographics: on
handheld devices, gender, age, and geographic origin are inferable from front-camera gaze
data [10], [21]. This regime is the more dangerous one for privacy because it cannot be
defeated by changing what the page displays, and re-identification is the vector within it
that the same-origin policy does not neutralize.

## 4. Leakage vectors (D1–D6) and why D4 is the target

The project organizes specific leakage vectors into six directions. D1–D2 are
content-dependent; D3–D5 are content-independent; D6 covers defenses.

| ID | Leakage vector | Regime | What leaks | Evidence |
|---|---|---|---|---|
| **D1** | On-screen keyboard / PIN inference | Content-dependent | PINs, passwords, unlock codes | [8], [12], [27] |
| **D2** | Reading content & search intent | Content-dependent | What the user reads, queries, attends to | [4], [7] |
| **D3** | Cognitive & affective state | Content-independent | Attention, confusion, mind-wandering, engagement, load | [1], [2], [22], [26] |
| **D4** | **Behavioral-biometric re-identification & cross-site tracking** | **Content-independent** | **Persistent identity and linkage across sessions, sites, and devices** | **[20], [29], [30]–[37]** |
| **D5** | Attribute & demographic inference | Content-independent | Gender, age, geographic origin, related traits | [10], [21] |
| **D6** | Defenses & drive-by detection | — | Differential privacy, on-device processing, consent design | [13], [23], [24], [47]–[49] |

**This plan is a deep dive on D4.** The reasons are laid out in §5 and §6, but the short
version is that D4 is the only content-independent vector that (a) survives the same-origin
policy, (b) survives clearing every piece of client-side state, and (c) has a mature
research-grade literature to measure a commodity-webcam realization against. D1–D2 are
content-dependent and blocked cross-site; D3 and D5 are real but weaker framings (state and
attributes are fuzzier stakes than identity, and D5 is already well evidenced on mobile
[10]). Re-identification framed as an *unclearable tracking channel* is the sharpest,
least-studied, and most defensible contribution.

## 5. What tightens and what loosens the threat model

Three findings from the background assessment shape — and justify — the choice of D4.

**Cross-tab / cross-site content peeking is not feasible.** The same-origin policy and
browser site isolation prevent a script in one origin from reading the gaze stream
associated with another. The adversary sees gaze only on pages where its own script runs.
This rules out the most alarming scenario — a background page silently reading what the user
looks at on their bank's site — and means the realistic cross-site risk is
*re-identification through behavioral biometrics* [20], [29], not content peeking. This is a
tightening of the threat model, and it is exactly why the paper's thesis is re-identification
and not content inference.

**Research-grade references are ceilings, not the threat.** High-accuracy IR-hardware and
offline-compute biometric results (for example, the EER in [20]) define what is achievable
with good hardware. They are not consistent with the drive-by, commodity, in-browser model
that is the project's contribution, and conflating the two would overstate the in-browser
attacker. They belong in the paper as ceilings against which the realistic webcam channel is
measured — which is precisely what RQ3 (§8) quantifies.

**Identity survives de-facing.** Stripping facial identity from the video does not remove the
eye-movement biometric, which is carried by movement dynamics rather than appearance [20],
[29]. A defense or consent notice premised on "we do not store your face" therefore does not
prevent re-identification. This *loosens* the threat model — the signal is more robust than a
naive reading suggests — and it is one of the headline claims RQ4 tests.

A form-factor note carries over from the background assessment: on desktop/laptop, favorable
head pose and a large screen make the gaze-coordinate channel most tractable, and in-browser
trackers run with no installation. WebGazer self-calibrates from ordinary cursor
interactions but its ridge-regression model lacks head-pose awareness and its accuracy
degrades over a session [7], [25]; WebEyeTrack closes much of that gap — head-pose-aware,
calibrating from as few as nine samples, about 2.32 cm error on GazeCapture and roughly twice
as accurate as WebGazer [25]. The accuracy objection to desktop in-browser attacks is
weakening over time, not strengthening. The desktop, commodity, in-browser case is the least
characterized surface in the literature and the strongest contribution angle — the plan's
subject.

---

# Part II — The research plan

## 6. Thesis and contributions

**Thesis.** Eye-movement dynamics captured by a commodity, in-browser webcam gaze tracker
form a *stateless, person-bound* re-identification signal that browser privacy controls do
not remove — clearing cookies, incognito mode, storage partitioning, and even switching
devices leave it intact — and that survives removal of the face from the video, because it
is carried by *movement dynamics*, not appearance.

**Why this is the right contribution.** The same-origin policy and site isolation block a
script from reading gaze on *another* site (content peeking is not feasible — §5).
Re-identification is *content-independent*, so the same-origin policy does not touch it: two
first-party sites that embed the same tracking script can link the same visitor by their
gaze. This turns Part I's limitation into the paper's thesis.

**Three contributions:**

1. **A new tracking channel.** Gaze as a cookieless, cache-proof, incognito-surviving,
   cross-device re-identifier — a *person-bound* fingerprint, unlike canvas/font/device
   fingerprints, which are device-bound and defeated by anti-fingerprinting browsers
   ([44]–[46]).
2. **Ceiling vs. commodity.** The gap between research-grade hardware (Gazepoint) and the
   deployed webcam channel (WebGazer / WebEyeTrack / EyeGestures, with GazeCloud as a cloud
   contrast), measured on the *same* subjects. This is the direct payoff of having both
   devices.
3. **(Optional) A defense.** An in-browser perturbation layer that raises attacker EER at
   bounded utility cost, plotted as a privacy–utility curve.

## 7. Threat model

- **Adversary:** a tracking/analytics provider whose JavaScript runs **first-party** on many
  independent sites — the same structural position as an analytics or ad tag included via
  `<script src>`. Because the script executes in each host site's *own* origin, it uses *that
  site's* camera permission; the provider then links visitors **server-side** across every site
  it is embedded on. **State the web-platform mechanism precisely (reviewers will check):**
  camera permission is granted per top-level origin and is **not** silently shared across
  origins. A cross-origin tracker *iframe* would need explicit `Permissions-Policy` camera
  delegation from each top frame *and* its own per-origin grant — so the realistic, and still
  alarming, model is the **first-party-included script**, not a third-party iframe silently
  inheriting the camera. Each site prompts for the camera once (see Appendix A.4 for the
  consent-realism argument).
- **Goal:** link a visitor's sessions across sites and over time to a persistent pseudonymous
  identity **without cookies or client-side state**.
- **Capability:** client-side JS only; gaze estimation in-browser; covert calibration from
  ordinary mouse clicks (present in the WebGazer/GazePry lineage — the code review confirmed
  mouse-event listeners feeding the regression). Features can be computed client-side, so the
  adversary never needs to store the raw face.
- **Out of scope (and stated as such):** reading another origin's content (blocked by the
  same-origin policy), physically-present cameras, VR/MR headsets. This is a *drive-by
  desktop web* adversary — the gap in the literature.

**Delta from prior work (state this in Related Work):**

| Prior work | Setting | What makes ours different |
|---|---|---|
| Eye Know You Too [20], GazeBase biometrics [36] | Research IR hardware, cooperative enrollment, same task, *authentication* | Adversarial webcam, cross-task, cross-site *tracking*, unclearable-identifier framing |
| Alsakar et al. handheld privacy [10] | Mobile front camera, *attribute* inference, single site | Desktop, cross-site *linkage*, *identity* not attributes |
| Canvas/font/device fingerprinting [44]–[46] | Stateless but device-bound; defeated by anti-FP browsers | Physically grounded, *person*-bound, survives fresh device + face removal |
| EyeTell [27], GAZEploit [14] | Content-*dependent* keystroke inference | Content-*independent*; identity, not secrets |

## 8. Research questions and hypotheses

Each research question is paired with a **directional, falsifiable hypothesis (H)** and a
**decision rule** stating what result confirms, narrows, or refutes it. This is the
pre-registration target (§20 step 5). Conventions: metrics are defined in §14; **chance** rank-1
= 1/(gallery size); every accuracy/EER figure is reported with a **confidence interval (CI) over
subject splits** (§15), never a single split; δ denotes a pre-registered margin (a specific
number fixed at pre-registration, not post-hoc). Unless stated otherwise, "the webcam channel"
means the best-performing *on-device* arm, and the headline cell is **cross-task, cross-session,
dynamics-only** (§13).

- **RQ0 (confound — the person, or the apparatus?).** *This is the precondition for every other
  RQ* (Appendix A.2–A.3). Does a webcam re-ID match reflect the individual's *eye-movement
  dynamics*, rather than a shared *calibration geometry, session, tracker, capture condition, or
  demographic stratum*?
  - **H0.** Under a shuffled-label null, rank-1 collapses to chance and EER to ≈0.5; and the
    signal *survives* independent re-calibration (calibration-swap), a change of lighting/seating
    and device, and enroll-on-one-tracker/identify-on-another (cross-tracker), all at
    above-chance accuracy.
  - **Decision rule.** *Confirmed* if shuffled-label rank-1 ≤ 2× chance with its CI including
    chance, **and** the calibration-swap cross-session rank-1 CI lower bound > chance. **Refuted
    / stop** if the signal disappears once calibration or session is held independent — then the
    "biometric" is an apparatus artifact and no downstream claim stands. Run this pilot *first*
    (§20 step 7).

- **RQ1 (baseline — returning-user re-ID).** How reliably does the webcam channel re-identify a
  returning user *same-task, cross-session* (test–retest ≥1 week apart)?
  - **H1.** Same-task cross-session rank-1 ≫ chance and EER ≪ 0.5.
  - **Decision rule.** *Confirmed* if the rank-1 CI lower bound > chance **and** the EER CI upper
    bound < 0.5 for at least the best on-device arm.

- **RQ2 (the tracking threat — cross-task transfer).** How much does re-ID degrade *cross-task /
  cross-stimulus* — enroll on site A's content, identify on site B's? This is the headline
  result; biometrics papers usually skip it. The closest prior framing is task-independent
  authentication [32].
  - **H2.** Cross-task cross-session re-ID stays above chance (a real tracking threat) but is
    *weaker* than same-task (rank-1_cross-task < rank-1_same-task).
  - **Decision rule.** *Confirmed* if the cross-task cross-session rank-1 CI lower bound > chance.
    *Narrowed* (fallback ladder, A.7) if only *same-genre* transfer (e.g. reading→reading) clears
    chance — still a scoped, meaningful threat. *Refuted* if cross-task ≈ chance.

- **RQ3 (ceiling vs. commodity).** What is the EER / rank-1 gap between the IR ceiling
  (Gazepoint) and the commodity webcam trackers — WebGazer, WebEyeTrack, EyeGestures, and the
  cloud option GazeCloud — on the *same* subjects and sessions? (Report on-device webcam arms
  separately from the cloud arm.)
  - **H3.** IR EER < on-device webcam EER in every matched cell, ordered WebEyeTrack ≤ EyeGestures
    ≤ WebGazer (head-pose-aware sits closest to the ceiling); the gap *shrinks* at longer
    observation windows.
  - **Decision rule.** *Confirmed* if the IR-vs-webcam EER gap is positive with non-overlapping
    CIs in the headline cell. The gap *magnitude* is the deliverable regardless of the ordering,
    so this RQ does not fail — it quantifies.

- **RQ4 (unclearability).** Does re-ID survive cookie/cache clear, incognito, a fresh profile, a
  different day/lighting, a *different device webcam*, and *face de-identification*?
  - **Separate two axes that the naive "wipe everything" demo conflates.** *(a) Web-state clearing*
    — cookies, cache, storage, incognito, fresh profile — removes **no** identity, because nothing
    person-bound is stored client-side (matching is server-side); re-ID after this clear is the
    genuine unclearable point. *(b) Calibration-model clearing* — wiping the tracker's click-trained
    model — also stores/removes no identity, but it **degrades the sensor**: an immediate probe is
    captured through an uncalibrated tracker and can miss until the model **silently re-trains from
    ordinary clicks/cursor motion**. A post-model-wipe miss is therefore a *calibration artifact,
    not identity loss* — a wipe **buys time, not anonymity**. The two must be reported as distinct
    conditions (the harness now exposes them as separate actions; the `intervention`/`calibQuality`
    metadata records which was cleared), or a recoverable sensor transient will be mis-read as the
    identifier being cleared. *(This is the same calibration confound as RQ0/A.3.)*
  - **H4.** Re-ID accuracy under each **web-state-clearing** / cross-device / face-removed condition
    is *statistically indistinguishable from baseline* (no drop beyond δ), because identity is
    carried by movement dynamics and no client-side state. Under **calibration-model clearing**,
    accuracy drops transiently and **recovers as the tracker re-calibrates** — the deliverable is
    the recovery curve (accuracy vs. clicks/seconds since wipe), which quantifies how little time a
    wipe buys. **Face de-identification is satisfied *by construction***: the primary pipeline never
    records appearance (only the `{t,x,y}` stream, §12), so removing the face cannot reduce accuracy.
  - **Decision rule.** *Confirmed* per web-state condition if the (baseline − intervention) rank-1
    difference CI includes 0, or the drop is < δ. For the model-clear condition, *confirmed* if
    accuracy recovers to within δ of baseline after a bounded recalibration budget. Contrast: a
    clearable canvas/UA fingerprint (§14) is shown to *reset to chance* under the same clears — the
    whole point.

- **RQ5 (defense, optional).** What perturbation of the gaze stream defeats re-ID at acceptable
  utility cost?
  - **H5.** There exists a perturbation operating point that raises attacker EER toward 0.5 while
    a utility task (reading-AOI detection or an accessibility metric) stays within a
    pre-registered bound — a usable point on the privacy–utility curve.
  - **Decision rule.** *Confirmed* if some operating point raises EER by ≥ δ_priv while utility
    degradation stays ≤ δ_util; report the full privacy–utility curve regardless of whether such
    a point exists.

## 9. Apparatus and tracker arms

**Recommended rig — simultaneous capture.** Record the webcam video *while* Gazepoint tracks.
The Gazepoint IR gives a per-frame ground-truth gaze label for every webcam frame, so you get
(a) an **independent** accuracy reference for the webcam estimate and (b) matched per-subject
data across both channels in one session. This is the cleanest way to answer RQ3.

**Critical control (do not contaminate the commodity arm).** The webcam trackers must be
evaluated *exactly as an attacker would deploy them* — running their own native
self-calibration — and their gaze output must **never be retrained, corrected, or
label-supervised using the Gazepoint signal**. Using IR labels to improve the webcam estimate
would leak the ceiling into the commodity arm and make both the RQ3 gap *and* the headline
re-ID result unrealistically strong. In this rig Gazepoint is a **measurement instrument, not
part of the attack pipeline**: it supplies ground truth for the accuracy comparison only,
never a training signal for re-identification.

**Tracker arms.** One IR ceiling plus a *pluggable* set of commodity in-browser webcam
trackers (the capture harness is tracker-agnostic — one adapter per tracker, selected per
session, all emitting the same gaze stream — so the same subject can be recorded on several
and compared directly):

1. **Gazepoint GP3 / GP3 HD** (60/150 Hz IR) — the ceiling / ground truth.
2. **WebGazer** (current brownhci build) — ridge regression, no head pose; the deployed
   reality and the GazePry lineage. *Do not use the stale GazePry/SearchGazer fork — its
   2016 SERP selectors are dead.* Video stays on-device.
3. **WebEyeTrack** [25] — CNN + few-shot personalization, head-pose-aware (~2.32 cm error on
   GazeCapture, calibrates from as few as nine samples); the near-future commodity ceiling.
   On-device.
4. **EyeGestures** (NativeSensors, open-source; web build) — an actively-maintained
   open-source second commodity arm; on-device.
5. **GazeCloud / GazeRecorder** (hosted JS API) — the *high-accuracy, self-calibrating*
   commodity option, but **closed-source and cloud-based: webcam frames are uploaded to a
   third party.** Include it as an accuracy contrast *and* as a finding in its own right —
   for a webcam-gaze *tracking-vector* paper, the most accurate drop-in option is also the
   one that exfiltrates the face. Report it separately from the on-device arms.

Other options considered and set aside: **RealEye.io** (commercial SaaS study platform, not a
drop-in library, also cloud); classic **TurkerGaze**/**SearchGazer** (WebGazer predecessors,
superseded); appearance-CNN research models (**iTracker/GazeCapture**, **L2CS-Net**) that
would need porting to TF.js and give no calibration/UX out of the box. The four webcam arms
above (2–5) cover the deployable open-source reality (WebGazer, EyeGestures), the near-future
on-device ceiling (WebEyeTrack), and the cloud high-accuracy point (GazeCloud).

**Sampling-rate caveat (methodological, state it — and mind the logged-vs-true-rate trap):**
the *true* independent frame rate of a commodity webcam is ~30 Hz, but the trackers **log** gaze
at their prediction cadence, which is the browser's requestAnimationFrame rate — in the pilot,
WebGazer records at **~50–120 Hz**, not 30 Hz, by interpolating/repeating predictions over a
lower true camera rate. Two consequences: (a) saccade-velocity and main-sequence features computed
on the logged stream partly encode *logging cadence*, not oculomotor dynamics; and (b) the logged
rate **differs across sessions and participants** (in the pilot, P01 ≈ 50 Hz vs P02 ≈ 110 Hz),
which makes capture rate a re-identification **confound that is correlated with identity**.
Mitigation, now implemented in `analysis/`: **resample every session to a common cadence before
feature extraction** (`features.resample` / `reid-core.js resample`, JS↔Py parity-tested) and run
the **rate-equalized negative control** (`reid.py`, printed by default) — if re-ID collapses once
rate is equalized, the "signal" was cadence. Down-sample Gazepoint to the same common rate for the
*fair* comparison arm, and report which features survive it. The literature predicts the
casualties: Eberz [50] shows authentication survives to 50 Hz but **microsaccade-tied features
degrade most**, and Rigas [52] locates saccadic vigor in a **>75 Hz band** — but note Eberz
*decimates a clean 500 Hz IR* stream, so it bounds the best case, not the natively noisy webcam.

**Harness status (implementation).** The capture harness is built and in this repo: a
*tracker-agnostic* orchestrator drives one self-registering adapter per tracker (WebGazer,
WebEyeTrack, EyeGestures on-device; GazeCloud cloud), selected per session from the hub, all
emitting the same per-frame `{t, x, y}` stream — so one feature pipeline
(`reid-core.js` / `analysis/features.py`) and one evaluation (`analysis/reid.py`, which
reports **per tracker** and never matches across trackers) serve every arm. The tracker
family is recorded in each session and threaded through storage and the live re-ID server. A
zero-dependency regression suite (`npm test`) covers features, the matcher, the
registry/adapters, the server endpoints, and JS↔Python feature parity. Gazepoint IR capture
is external and time-aligned to the webcam stream per the simultaneous-capture rig above. See
the repo `README.md` and `public/trackers/README-adapter.md`.

## 10. Participants and sessions

- **N:** target **50–60** for a first paper, with a **floor of ≥50** so the largest gallery-size
  cell in §13 (gallery = 50) is actually populated — 40 cannot fill it. More strengthens the
  verification (EER) claim. Use public datasets (below) to back the large-N *feasibility ceiling*.
- **Precision / power (do before scaling):** the headline deliverable is an *interval*, not a
  point — report the cross-task cross-session EER with a CI over subject splits (§15). Run a
  precision check first: bootstrap from the pilot (or simulate) to confirm N≈50 yields a CI tight
  enough to separate the webcam EER from **both** chance **and** the IR ceiling (RQ3). If it does
  not, raise N or lengthen the observation window rather than over-reading a single split.
- **Sessions:** **≥2–3 per participant, separated by ≥1 week.** Within-session re-ID is
  trivially easy and not the threat; *cross-session, time-separated* re-ID is the real
  "returning visitor" test and the number reviewers will look for. (The ≥1-week separation
  mirrors the design of longitudinal biometric datasets such as JuDo1000 [38] and GazeBase
  [36].)
- **Realistic-variation conditions:** at least one session under different lighting / seating;
  if a second laptop is available, one session on a *different webcam* to support the
  cross-device claim.
- **IRB:** the study operates under a **TAMU IRB-exempt determination** (on file) — IRB is
  **not** a gating item. Still plan consent language carefully: it remains good practice, is
  needed for the artifact/data-handling statement, and is material for a possible SOUPS
  companion study.
- **Public datasets for the ceiling / large-N feasibility:** GazeBase [36] (322 subjects, 9
  rounds over 37 months), GazeBaseVR [37], JuDo1000 [38] (150 subjects, 4 sessions ≥1 week
  apart). Use these for the deep-model biometric ceiling; reserve *fresh* simultaneous capture
  for the webcam claim.

## 11. Stimuli — the multi-"site" design

Different tasks elicit different gaze dynamics, so distinct tasks stand in for distinct
"sites." Enroll on one, identify on another to test cross-site generalization.

1. **Reading** — a text passage (reading biometrics heritage, [7], [22], [30]).
2. **SERP scanning** — a search-results layout (the SearchGazer core, [4]).
3. **Free image viewing.**
4. **Video watching.**
5. **Form / typing task.**

Report **same-task** (upper bound) and **cross-task** (the tracking threat) separately.

## 12. Features and models

- **Content-independent features (primary):** fixation durations, saccade amplitudes and
  velocities (the "main sequence" relationship is highly individual [30]), blink rate, pupil
  dynamics, microsaccades if resolvable. These are the classic eye-movement biometric
  features.
- **Two modeling routes:**
  - **(a) Hand-crafted features + classifier** — interpretable, robust at small N. Start
    here. The interpretable score-fusion lineage ([31]) is the model here. *Implementation status:*
    the pipeline currently uses the 16 hand-crafted features with a nearest-neighbour matcher in
    per-feature-standardized space (i.e. a diagonal-Mahalanobis distance). A **learned metric**
    (LDA / full-covariance Mahalanobis / [31]'s score fusion) and a richer distributional feature
    set are the planned next step — but deliberately **deferred until N is large enough to fit and
    validate them**: at the pilot's N=2 a learned metric has nothing to generalize across and would
    overfit, which the shuffle-null guardrail (A.3) is designed to catch. Add it once a real cohort
    exists, and gate every accuracy gain on the shuffle-null and the rate-equalized control.
  - **(b) End-to-end deep model** (DenseNet-style, à la Eye Know You Too [20]; see also the
    micro-movement models [33], [34]) — the ceiling; train/validate on public data, fine-tune
    on yours. **Domain-gap caveat (state it):** the public biometric datasets are IR at
    250–1000 Hz ([36]–[38]); the webcam channel has a ~30 Hz *true* frame rate (logged at a higher,
    variable cadence — see the §9 sampling-rate caveat) with categorically different noise, so a
    model pretrained on IR will **not** transfer to webcam without explicit **domain adaptation**
    (down-sample IR to a common rate, inject webcam-like noise, and fine-tune on the
    simultaneous-capture data). Treat route (b) on the *webcam* channel as a research risk,
    not a drop-in; route (a) hand-crafted features is the safer primary for the webcam claim,
    with route (b) reserved for the IR ceiling and the large-N feasibility argument.
- **Critical control:** the primary condition **excludes the raw face image / appearance
  features**, so the "survives de-identification" claim is clean — in fact the capture harness
  never records appearance at all (only the `{t, x, y}` stream), so face removal holds *by
  construction*, not by post-hoc masking (this is exactly what RQ4/H4 asserts). Consequently the
  appearance-*including* arm — an upper bound quantifying how much signal is dynamics vs.
  appearance — is **contingent on first adding an appearance-embedding channel to the harness**;
  treat it as optional, and report the dynamics-only result as the primary, clean claim. Decide
  explicitly whether to build that channel: if not, drop the ablation and lean on the
  by-construction argument rather than implying an ablation that cannot run.

## 13. Conditions matrix

The experimental cells (each × the tracker arms in §9 — the Gazepoint IR ceiling plus four
webcam trackers: WebGazer, WebEyeTrack, EyeGestures, and the cloud contrast GazeCloud):

| Axis | Levels |
|---|---|
| Task pairing | same-task / cross-task |
| Session | same-session / cross-session (≥1 wk) |
| Observation window | 5 s / 15 s / 30 s / 60 s / full |
| Gallery size | 10 / 25 / 50 / full (scaling to a tracked population) |
| Intervention | none / cookie-cache clear / incognito / new profile / new device / face-blur |
| Features | dynamics-only / dynamics+appearance |

Headline cell: **cross-task, cross-session, dynamics-only, webcam** — the real-world tracking
threat.

## 14. Metrics

- **Identification:** rank-1 / rank-5 accuracy; CMC curve.
- **Verification:** EER; ROC / AUC.
- **Two key curves:**
  - Accuracy vs. **observation window** — "how many seconds of viewing links you" (a
    practical, quotable result). The research-grade ceiling already shows a steep window
    dependence — Eye Know You Too falls from ≈0.58% EER at 60 s to ≈3.66% at 5 s [20] — so
    this curve is expected to be informative, and the commodity channel's version of it is a
    core deliverable.
  - Accuracy vs. **gallery size** — how the threat scales to a large tracked population.
- **Baselines:** chance; a conventional fingerprint (canvas/UA) as the *clearable* comparison
  [44]–[46] — the point is gaze persists where those reset after a clear.

## 15. Analysis plan

- Report degradation from the IR ceiling (Gazepoint) down the on-device webcam arms
  (WebEyeTrack → EyeGestures → WebGazer) for each cell; report the cloud arm (GazeCloud)
  **separately**, since it is not on-device and its accuracy is not comparable in privacy
  terms.
- Statistical treatment of cross-session stability (test–retest), including explicit
  template-aging analysis in the manner of [35]; report confidence intervals over subject
  splits, not a single split.
- Honest headline: even a **degraded-but-non-random** webcam EER is a publishable tracking
  threat when the comparison is "a cookie the user *can* clear." Frame webcam numbers as a
  *lower bound* on the threat.

## 16. Defense (optional)

Perturb the client-side gaze stream (temporal/Gaussian noise, down-sampling, feature-level
differential privacy [47], the streaming-DP approach [24], the Kalεido real-time gaze-DP
system [48], or the re-identification-targeted k-anonymity/plausible-deniability approach
[49]). Show attacker EER rising while a *utility* task (reading-AOI detection or an
accessibility metric) stays acceptable. Note that partial protections can be undone when a
second uncoordinated signal is left unprotected [41] — scope the defense accordingly.
Deliverable: a **privacy–utility tradeoff curve**. Pairing an attack with a defense reviews
better.

## 17. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Webcam EER too high to be a "threat" | Use WebEyeTrack; longer windows; noise-robust distributional features; frame as lower bound. Even ~15–25% EER beats "clearable cookies." |
| Cross-task generalization weak | Report honestly; if only same-content sites link, the threat narrows to (e.g.) reading sites — still meaningful. Anchor the discussion in the known failure modes of task-independent authentication [32]. |
| N too small for deep models | Public datasets [36]–[38] for the deep/ceiling claim; fresh data for the webcam claim. |
| Low webcam framerate kills saccade features | Down-sample Gazepoint for fair comparison; report which features survive 30 Hz. |
| IRB delay | Not applicable — the study is IRB-exempt (determination on file). |

---

# Part III — Positioning and execution

## 18. Related work and the gap this plan fills

There **is** a large literature adjacent to this plan — eye-movement biometrics is a mature
field — but **no published work occupies the exact cell this plan targets: commodity
in-browser webcam gaze, on a desktop, used for *cross-site, cross-task* re-identification
framed as an unclearable web-tracking vector.** Every close analogue differs on at least one
of {hardware, setting, task-transfer, framing}. The subsections below group the literature by
the role it plays in the argument.

### 18.1 Eye-movement biometrics: the identification signal exists (foundations for RQ1, §12)

These establish that eye-movement *dynamics* re-identify people, and define the hand-crafted
feature set that route (a) uses. They are research-grade IR / cooperative-enrollment
ceilings, not the webcam threat — cite them as "the signal is real and individual," then show
the commodity gap (RQ3).

- **Holland & Komogortsev [30]** — reading-scanpath biometrics; the origin of the
  fixation/saccade + "main-sequence" feature family named in §12.
- **George & Routray [31]** — Gaussian-RBF-network score-level fusion of fixation/saccade
  features on the BioEye 2015 data, reporting an **EER of about 2.59% on the random-stimulus
  task**; a strong, interpretable baseline for route (a). *(The exact subject count and the
  higher-EER text-reading condition should be quoted from the paper's tables when written up;
  see §21.)*
- **Jäger et al., "Deep Eyedentification" [33]** and **Makowski et al.,
  "DeepEyedentificationLive" [34]** — deep identification from eye *micro-movements* (plus
  presentation-attack detection); the end-to-end ceiling for route (b), alongside Eye Know
  You Too [20].
- **Al Zaidawi et al. [35]** — cross-dataset identification and explicit **template-aging**
  analysis; directly relevant to the cross-session stability claim (RQ4) and to honest
  degradation reporting.
- **Rigas, Komogortsev & Shadmehr [52]** — adds **saccadic vigor and acceleration** (the
  main-sequence dynamics) to the CEM-B framework on 322 subjects at 1000 Hz across random-dot /
  text / video stimuli. Two uses here: it names the peak-velocity-vs-amplitude features route
  (a) leans on, and it locates the vigor signal in a **>75 Hz band** — direct evidence for the
  §9 caveat that a ~30 Hz webcam cannot resolve these cues (feeds the "which features survive"
  finding, A.5).
- **Li et al. [53]** — texture (Gabor-wavelet) features of the scanpath *trajectory* on a
  **visual-search** task (58 subjects, Tobii TX300); best EER ≈0.89% short-term but with
  **template aging inflating EER by 74–1075%** — a concrete long-interval degradation number to
  set expectations for the ≥1-week cell, and a search-task analogue for the SERP "site" (§6).
- **Galdi et al. [54]** — a **critical survey** of gaze-for-authentication that flags the
  field's lack of shared datasets/protocols and the difficulty of **uncontrolled settings**
  (remote trackers, webcams) — the exact regime this plan operates in. It also names the source
  of the withdrawn "88.6% Rank-1 / 5.8% EER / 320 subjects" figure (a Rigas multi-stimulus
  fusion scheme, *not* George & Routray — see the §21 verification note).

### 18.2 The cross-task problem — the RQ2 headline has precedent but is under-studied

This is the differentiator. Most biometric papers enroll and test on the *same* task; the
tracking threat needs task/stimulus transfer ("enroll on site A, identify on site B").

- **Kinnunen et al. [32]** — the canonical **task-independent** eye-movement authentication
  paper: no assumption that train/test share a stimulus. This is the closest prior framing to
  RQ2 and should anchor the cross-task discussion — including its honest failure modes (small
  subject pool, high error rates), which motivate the plan's longer windows and distributional
  features.
- **Eberz et al., "Looks Like Eve" [50]** — the **closest prior art overall**. It authenticates
  users **across everyday tasks** (reading, writing, browsing, video) with error comparable to a
  fixed task set, is **stable over a 2-week gap**, and **still works at 50 Hz** (downsampling a
  500 Hz Tobii; microsaccade-tied features degrade most). A reviewer *will* cite it, so the plan
  must pre-empt it with three distinctions it itself grants: (i) it decimates a **clean 500 Hz
  IR** signal, not a natively ~30 Hz noisy self-calibrating webcam (the RQ3 gap); (ii) it
  **authenticates a cooperating, enrolled** user (1:1 defense) rather than covertly
  **re-identifying** an unconsented one (1:N attack); (iii) it runs on a **workstation** — no
  browser, no same-origin boundary, no unclearable cross-site framing. It proves two ingredients
  are feasible; it does not occupy the cell (see A.1).
- **Liao et al. [51]** — implicit, **stimulus-independent** identification in **real-world
  wayfinding** (SMI ETG glasses at 60 Hz, 39 subjects): 78% / EER 6.3% overall, and 64% /
  EER 12.1% under a **leave-one-route-out** split — the real-world analogue of enroll-on-A /
  identify-on-B. Evidence that stimulus-free transfer holds outside the lab, at an already-low
  60 Hz rate; still a cooperative wearable IR tracker, not a covert webcam.

### 18.3 Longitudinal & large-N datasets (the ceiling and the gallery-size axis, §10, §13)

Back the deep-model / large-population feasibility claim on public data; reserve fresh
simultaneous capture for the webcam claim.

- **Griffith et al., GazeBase [36]** — 322 subjects, 9 rounds over 37 months; the reference
  longitudinal set for test–retest and the ceiling model.
- **Lohr et al., GazeBaseVR [37]** — binocular VR extension; useful for the gallery-size
  scaling curve and a VR contrast point.
- **Makowski et al., JuDo1000 [38]** — 150 subjects, 4 sessions with ≥1-week separation, 1000
  Hz; a direct model for the plan's cross-session, time-separated design (§10).

### 18.4 Behavioral biometrics as an unclearable, *scalable* identifier — the tracking-vector analogue (thesis, §6)

The strongest analogues for the *framing*: physically-grounded behavioral signals that (i)
scale to huge galleries and (ii) persist across sessions/devices without any client-side
state. None is desktop-webcam gaze, so each is a supporting analogy, not a scoop.

- **Nair et al., "Unique Identification of 50,000+ VR Users" [39]** — 55,541 users
  identified from head/hand motion, about 94.3% correct from 100 s of data (model trained on
  5 min per user); the definitive "biomechanics scales like a strong biometric" result and the
  best external evidence that the gallery-size axis (§13) will not collapse the threat.
- **Miller et al. [40]** — 360° VR viewing, ~95% identification, **re-identifiable across
  device types**; a near-perfect analogue for the RQ4 cross-device / unclearability claim in a
  different modality.
- **Aziz & Komogortsev [41]** — shows unprotected motion undoes eye-tracking privacy
  protections and vice-versa; reinforces that partial defenses leak, relevant to RQ5 scoping.
- **Patergianakis & Lambrinoudakis [42]** — 2026 XR study framing eye-tracking biometrics
  explicitly as **loss of anonymity** (≈96.6% identification on GazeBaseVR's 400+ users during
  video watching); the closest recent "anonymity is the stake" framing to adopt.
- **Acien et al., TypeNet [43]** — keystroke biometrics with modest degradation scaling toward
  100k users; a non-gaze precedent that a commodity behavioral channel remains a viable
  identifier at web scale.

### 18.5 Stateless web tracking & cross-device linkage — the "clearable cookie" baseline (§6 contribution 1, §14 baselines)

These define the bar the paper argues gaze *clears*: stateless-but-device-bound fingerprints
that anti-FP browsers defeat and that reset on a new device. Use them as the explicit
comparison in the metrics.

- **Acar et al., "The Web Never Forgets" [44]** — canvas fingerprinting / evercookies /
  cookie-syncing in the wild; the reference for "persistent tracking mechanisms" and the
  rhetorical anchor for the title framing.
- **Vastel et al., FP-STALKER [45]** — links *evolving* browser fingerprints over time; the
  state-of-the-art stateless linkage the gaze channel is contrasted against (fingerprints
  drift and can be reset; gaze is person-bound).
- **Zimmeck et al. [46]** — cross-device tracking analysis; the prior model for linking one
  person across contexts, which gaze does *without* the shared-network/deterministic-identifier
  assumptions.

### 18.6 Defenses for the gaze channel (RQ5, §16)

- **Steil et al. [47]** — the foundational **differential-privacy-for-gaze** paper
  (feature-level DP on eye-movement data); the natural first perturbation to evaluate.
- **Li et al., Kalεido [48]** — USENIX Security real-time gaze-DP *system* with formal
  guarantees; the deployment-shaped defense to benchmark the in-browser perturbation layer
  against.
- **David-John et al., "For Your Eyes Only" [49]** — adapts **k-anonymity / plausible
  deniability** specifically to defeat eye-movement *re-identification* on datasets; the
  defense whose threat model matches this plan most exactly.
- Streaming-DP and VR-gaze protections [13], [23], [24] complete the landscape.

### 18.7 Content-dependent gaze attacks — the contrast class this plan is *not*

Cited only to delimit scope against the content-*independent* thesis: EyeTell [27] and
GAZEploit [14] (in the delta table), plus GazeRevealer [8], gaze graphical passwords [12],
AR/VR head-motion keylogging [15], and eyeglass-reflection screen peeking [19] — all
content-*dependent* or side-channel. The "clearable cookie"-adjacent history side channel "I
Still Know What You Visited Last Summer" [5] pairs with [44]–[46]. Privacy-framing and the
SOUPS-companion consent angle draw on the eye-gaze security/privacy survey [3],
pervasive-eye-tracking privacy [6], "From Gaze to Data" [9], "What Does Your Gaze Reveal
About You?" [21], and AR privacy-concern attitudes [28].

### 18.8 The gap this plan fills

Stack the four axes and the white space is unambiguous: eye-movement biometrics is proven on
**IR hardware** ([20], [30]–[37]); **cross-task / low-rate** recognition is proven, but only on
cooperative **IR / mobile** trackers ([50] at 50 Hz downsampled, [51] at 60 Hz);
behavioral-biometric tracking at **scale/cross-device** is proven in **VR** ([39], [40], [42]);
stateless web tracking is proven for **device-bound fingerprints** ([44]–[46]). No one has shown
**commodity webcam gaze, on the open desktop web, re-identifying users cross-task and cross-site
as an unclearable tracking channel**, and quantified its gap to the IR ceiling on the *same*
subjects (RQ3). That intersection — not any single axis — is the contribution.

## 19. Target venues and timeline

- **Primary:** PETS / PoPETs — strong topical fit, rolling quarterly deadlines (good for
  iterating). *Confirm the exact cycle date from the current CFP.*
- **Reach:** USENIX Security / CCS / NDSS if the cross-site end-to-end linkage demo is strong.
- **Workshop hedge / early feedback:** WPES (co-located with CCS).
- **Companion:** SOUPS, if the consent user study is added.

**Rough critical path (calendar-bound by session separation):** pilot 2–4 wk → collection 6–10
wk (multi-session forces calendar time) → analysis 4–6 wk → writing 4 wk. ≈ 4–6 months
end-to-end (IRB is exempt, so it adds no calendar time); aim at a **PoPETs cycle in H1 2027** or
a **USENIX Security 2027** deadline. Verify exact dates against live CFPs before committing.

## 19a. Current empirical status (read before quoting any number)

**No re-identification claim in this plan is yet supported by data. The pilot is a
pipeline/feasibility check, not evidence.** State this plainly to avoid over-reading it.

- **N = 2 real participants.** The captured pilot is P01 and P02 on WebGazer (gallery size 2 →
  chance rank-1 = 0.5), plus P01 alone on WebEyeTrack (cannot be scored — a 1-person gallery). The
  plan's headline cells need N ≥ 50 (§10); the pilot fills none of them.
- **The headline pilot number is not a result.** WebGazer cross-task/cross-session rank-1 ≈ 0.75
  (chance 0.5), EER ≈ 0.32, with the shuffled-label null at rank-1 ≈ 0.50 — a thin margin over two
  identities.
- **No returning-visitor separation.** All pilot "sessions" are same-sitting (P01 S1↔S2 ≈ 14 min,
  P02 S1↔S2 ≈ 6 min). The `≥ 1-week` cross-session cells — the actual RQ1/RQ4 threat — are **empty**;
  `reid.py` now reports them as such rather than letting same-day blocks masquerade as the threat.
- **A rate confound sits on top of the signal.** WebGazer logs at ~50 Hz for P01 and ~110 Hz for
  P02 — capture rate is correlated with identity, so part of the (weak) discrimination may be
  cadence, not eyes. The rate-equalized control (`reid.py`, default) exists precisely to test this;
  it must clear before any number is quoted.
- **RQ0 is unanswered.** The confound battery (calibration-swap, cross-tracker, shuffled-null,
  rate-equalized) is the precondition (A.3); until it runs on a real cohort, "is this the person or
  the apparatus?" is genuinely open.
- **The synthetic `data_sim/` numbers** (cross-task/cross-session rank-1 ≈ 0.28 at N=12) are a
  **code sanity check on generated data**, not a claim about real eyes.
- **Modeling status.** Route (a) uses 16 hand-crafted features + a diagonal-Mahalanobis NN matcher;
  the learned metric / richer features (§12) are deferred until N supports validating them.

**Treat H1–H4 as pre-registered *predictions to be tested*, not findings — with RQ0 as the gate.**
The gating dependency for an actual verdict is a real collection (N ≥ 50, true ≥ 1-week separation,
the simultaneous Gazepoint rig, and populated condition metadata).

## 20. Immediate next steps

1. Finalize **consent + data-handling language** for the sessions (the study is IRB-exempt —
   determination on file — so no protocol filing gates the work; consent copy is still needed
   for the artifact statement and the SOUPS companion).
2. Stand up the **simultaneous Gazepoint + webcam** capture rig; verify per-frame time
   alignment between IR labels and webcam frames.
3. Use the **pluggable tracker** harness (`public/trackers/`): WebGazer, WebEyeTrack, and
   EyeGestures are vendored and on-device (WebEyeTrack/EyeGestures via
   `scripts/vendor-trackers.sh`); GazeCloud is the cloud contrast. All log the same per-frame
   gaze stream, so one feature extractor + analysis covers every arm.
4. Run a **2–3 subject pilot** across all five tasks to sanity-check feature extraction and
   the same-session re-ID sanity cell before scaling.
5. Pre-register the conditions matrix (§13) and metrics (§14) to keep the cross-task,
   cross-session claim honest.
6. Before submission, re-pull every citation flagged in §21 against its published version and
   replace preprint numbers with the peer-reviewed figures.
7. **Run the confound-control pilot first (Appendix A.3), before any headline collection.**
   The calibration-swap and shuffled-label null tests decide whether the signal is the *person*
   or the *session/calibration* — if you can't separate them, nothing downstream matters.
8. **Resolve the blocking data-hygiene issue (Appendix A.6):** the repo currently tracks
   **29 real participant gaze sessions** (`data/*.json`) in git with the `.gitignore` rule
   commented out — untrack them and scrub history *before* any public artifact release. (IRB is
   settled: the study is IRB-exempt, determination on file — no longer an open item.)

## 21. References and citation status

*Shared numbering across the GazePry documents. Peer-reviewed venues are preferred; arXiv
preprints are flagged, and their quantitative claims should be treated as indicative until the
published version is checked. The central claims of this plan rest on peer-reviewed venues
(IEEE S&P, IEEE TMC, ACM CCS, USENIX Security, CHI, ETRA, ACM TOPS, Scientific Data, IEEE
TVCG, IEEE TIFS, Pattern Recognition Letters).*

**Verification notes (for the top-tier submission):**

- **[31] George & Routray corrected.** An earlier draft attributed "EER ≈ 5.8%, 320 subjects"
  to this paper. The published paper reports an **EER of about 2.59% on the random-stimulus
  task** using the BioEye 2015 competition data; the "320 subjects" figure did not check out.
  Quote the paper's own subject count and per-task EERs directly when writing the related-work
  section. **Provenance of the withdrawn figure:** Galdi et al.'s survey [54] attributes exactly
  "Rank-1 IR 88.6%, EER 5.8%, 320 subjects" to a **Rigas et al. multi-stimulus, multi-biometric
  fusion scheme** (jumping-point-of-light + text + video) — a sibling of [52], *not* George &
  Routray. Cite that Rigas fusion paper directly if the number is used (pin its exact year/venue
  first — the survey cites it via its own numbering).
- **[27] EyeTell corrected.** The 4-digit-PIN figures are top-5 ≈65% and top-50 ≈90%; the
  ≈70% figure is the **Android lock-pattern** top-5 result, not a 6-digit PIN result. Verify
  any top-1 / 6-digit numbers against the paper's tables before quoting.
- **[20] Eye Know You Too** — EER is ≈0.58% only with 60 s of enrollment/verification on a
  reading task, rising to ≈3.66% at 5 s. Always state the window when quoting the EER.
- **Preprint flags (arXiv, not yet confirmed peer-reviewed at the numbers quoted):** [16],
  [18], [23], [25], [26], [29], [35], [41]. [20] and [35] have published versions (IEEE TIFS;
  Signal Processing: Image Communication) — cite those. [25] (WebEyeTrack), [29], and [41] are
  preprints at time of writing; re-check before submission.

[1] S. D'Mello, A. Olney, C. Williams, and P. Hays, "Gaze tutor: A gaze-reactive intelligent tutoring system," *International Journal of Human-Computer Studies*, vol. 70, no. 5, pp. 377–398, May 2012, doi: 10.1016/j.ijhcs.2012.01.004.

[2] S. D'Mello and A. Graesser, "AutoTutor and affective autotutor: Learning by talking with cognitively and emotionally intelligent computers that talk back," *ACM Trans. Interact. Intell. Syst.*, vol. 2, no. 4, pp. 1–39, Dec. 2012, doi: 10.1145/2395123.2395128.

[3] C. Katsini, Y. Abdrabou, G. E. Raptis, M. Khamis, and F. Alt, "The Role of Eye Gaze in Security and Privacy Applications: Survey and Future HCI Research Directions," in *Proc. 2020 CHI Conf. Human Factors in Computing Systems*, CHI '20, ACM, Apr. 2020, pp. 1–21, doi: 10.1145/3313831.3376840.

[4] A. Papoutsaki, J. Laskey, and J. Huang, "SearchGazer: Webcam Eye Tracking for Remote Studies of Web Search," in *Proc. 2017 Conf. Human Information Interaction and Retrieval*, CHIIR '17, ACM, Mar. 2017, pp. 17–26, doi: 10.1145/3020165.3020170.

[5] Z. Weinberg, E. Y. Chen, P. R. Jayaraman, and C. Jackson, "I Still Know What You Visited Last Summer: Leaking Browsing History via User Interaction and Side Channel Attacks," in *2011 IEEE Symp. Security and Privacy*, IEEE, May 2011, pp. 147–161, doi: 10.1109/SP.2011.23.

[6] D. J. Liebling and S. Preibusch, "Privacy considerations for a pervasive eye tracking world," in *Proc. 2014 ACM Int. Joint Conf. Pervasive and Ubiquitous Computing: Adjunct Publication*, ACM, Sep. 2014, pp. 1169–1177, doi: 10.1145/2638728.2641688.

[7] A. Papoutsaki, A. Gokaslan, J. Tompkin, Y. He, and J. Huang, "The eye of the typer: a benchmark and analysis of gaze behavior during typing," in *Proc. 2018 ACM Symp. Eye Tracking Research & Applications*, ETRA '18, ACM, Jun. 2018, pp. 1–9, doi: 10.1145/3204493.3204552.

[8] Y. Wang, W. Cai, T. Gu, and W. Shao, "Your Eyes Reveal Your Secrets: An Eye Movement Based Password Inference on Smartphone," *IEEE Trans. Mobile Computing*, vol. 19, no. 11, pp. 2714–2730, Nov. 2020, doi: 10.1109/TMC.2019.2934690.

[9] Y. Abdrabou, S. Özdel, V. Maquiling, E. Bozkir, and E. Kasneci, "From Gaze to Data: Privacy and Societal Challenges of Using Eye-tracking Data to Inform GenAI Models," in *Proc. 2025 Symp. Eye Tracking Research and Applications*, ETRA '25, ACM, May 2025, pp. 1–9, doi: 10.1145/3715669.3726788.

[10] N. Alsakar, N. Alotaibi, M. Khamis, and S. Stumpf, "Assessing and Mitigating the Privacy Implications of Eye Tracking on Handheld Mobile Devices," *ACM Trans. Priv. Secur.*, vol. 28, no. 3, p. 38:1–38:36, Aug. 2025, doi: 10.1145/3746452.

[11] Y. Yang and F. Lu, "GazeLLM: a plug-and-play zero-shot LLM reasoning framework for boosting gaze target detection," *Vis. Intell.*, vol. 3, no. 1, p. 26, Dec. 2025, doi: 10.1007/s44267-025-00101-1.

[12] A. Tiwari and R. Pal, "Gaze-Based Graphical Password Using Webcam," in *Information Systems Security*, Springer, 2018, pp. 448–461, doi: 10.1007/978-3-030-05171-6_23.

[13] E. Wilson, A. Ibragimov, M. J. Proulx, S. D. Tetali, K. Butler, and E. Jain, "Privacy-Preserving Gaze Data Streaming in Immersive Interactive Virtual Reality: Robustness and User Experience," *IEEE Trans. Visualization and Computer Graphics*, vol. 30, no. 5, pp. 2257–2268, May 2024, doi: 10.1109/TVCG.2024.3372032.

[14] H. Wang, Z. Zhan, H. Shan, S. Dai, M. Panoff, and S. Wang, "GAZEploit: Remote Keystroke Inference Attack by Gaze Estimation from Avatar Views in VR/MR Devices," in *Proc. 2024 ACM SIGSAC Conf. Computer and Communications Security*, CCS '24, ACM, Dec. 2024, pp. 1731–1745, doi: 10.1145/3658644.3690285.

[15] C. Slocum, Y. Zhang, N. Abu-Ghazaleh, and J. Chen, "Going through the motions: AR/VR keylogging from user head motions," in *USENIX Security 23*, 2023, pp. 159–174.

[16] *(arXiv preprint — flagged)* T. T. Pham, H. Nguyen, and N. Le, "GazeQwen: Lightweight Gaze-Conditioned LLM Modulation for Streaming Video Understanding," arXiv:2603.25841, Mar. 2026, doi: 10.48550/arXiv.2603.25841.

[17] S. I. Mustafa Shah Bukhari, M. Sajid, B. Ji, and B. David-John, "Rethinking Privacy Indicators in Extended Reality: Multimodal Design for Situationally Impaired Bystanders," in *2025 IEEE Int. Symp. Mixed and Augmented Reality Adjunct (ISMAR-Adjunct)*, Oct. 2025, pp. 265–272, doi: 10.1109/ISMAR-Adjunct68609.2025.00059.

[18] *(arXiv preprint — flagged)* A. M. Mathew, H. Hermassi, T. Khalid, and A. A. Khan, "GazeVLM: A Vision-Language Model for Multi-Task Gaze Understanding," arXiv:2511.06348, Mar. 2026, doi: 10.48550/arXiv.2511.06348.

[19] Y. Long, C. Yan, S. Xiao, S. Prasad, W. Xu, and K. Fu, "Private Eye: On the Limits of Textual Screen Peeking via Eyeglass Reflections in Video Conferencing," in *2023 IEEE Symp. Security and Privacy (SP)*, IEEE, May 2023, pp. 3432–3449, doi: 10.1109/SP46215.2023.10179423.

[20] D. Lohr and O. V. Komogortsev, "Eye Know You Too: Toward Viable End-to-End Eye Movement Biometrics for User Authentication," *IEEE Trans. Inf. Forensics Secur.*, vol. 17, pp. 3151–3164, 2022, doi: 10.1109/TIFS.2022.3201369. (Preprint: arXiv:2201.02110.)

[21] J. L. Kröger, O. H.-M. Lutz, and F. Müller, "What Does Your Gaze Reveal About You? On the Privacy Implications of Eye Tracking," in *Privacy and Identity Management. Data for Better Living: AI and Privacy*, Springer, 2020, pp. 226–241, doi: 10.1007/978-3-030-42504-3_15.

[22] S. Hutt, A. Wong, A. Papoutsaki, R. S. Baker, J. I. Gold, and C. Mills, "Webcam-based eye tracking to detect mind wandering and comprehension errors," *Behav. Res.*, vol. 56, no. 1, pp. 1–17, Jan. 2024, doi: 10.3758/s13428-022-02040-x.

[23] *(arXiv preprint — flagged)* L. Du, J. Jia, X. Zhang, and G. Lan, "PrivateGaze: Preserving User Privacy in Black-box Mobile Gaze Tracking Services," arXiv:2408.00950, Aug. 2024, doi: 10.48550/arXiv.2408.00950.

[24] B. David-John, D. Hosfelt, K. Butler, and E. Jain, "A privacy-preserving approach to streaming eye-tracking data," *IEEE Trans. Visual. Comput. Graphics*, vol. 27, no. 5, pp. 2555–2565, May 2021, doi: 10.1109/TVCG.2021.3067787.

[25] *(arXiv preprint — flagged)* E. Davalos et al., "WebEyeTrack: Scalable Eye-Tracking for the Browser via On-Device Few-Shot Personalization," arXiv:2508.19544, Aug. 2025, doi: 10.48550/arXiv.2508.19544.

[26] *(arXiv preprint — flagged)* V. Danry, J. Hernandez, A. Wilson, P. Maes, and J. Amores, "From Gaze to Guidance: Interpreting and Adapting to Users' Cognitive Needs with Multimodal Gaze-Aware AI Assistants," arXiv:2604.08062, Apr. 2026, doi: 10.48550/arXiv.2604.08062.

[27] Y. Chen, T. Li, R. Zhang, Y. Zhang, and T. Hedgpeth, "EyeTell: Video-Assisted Touchscreen Keystroke Inference from Eye Movements," in *2018 IEEE Symp. Security and Privacy (SP)*, IEEE, May 2018, pp. 144–160, doi: 10.1109/SP.2018.00010.

[28] E. Bozkir, B. Bühler, X. Wu, E. Kasneci, L. Bauer, and L. F. Cranor, "The impact of device type, data practices, and use case scenarios on privacy concerns about eye-tracked augmented reality in the United States and Germany," *J. Cyber Secur.*, vol. 11, no. 1, p. tyaf036, Jan. 2025, doi: 10.1093/cybsec/tyaf036.

[29] *(arXiv preprint — flagged)* H. Aziz, M. H. Raju, and O. V. Komogortsev, "Enhancing Eye Movement Biometrics for User Authentication via Continuous Gaze Offset Score Fusion," arXiv:2605.06810, 2026, doi: 10.48550/arXiv.2605.06810.

[30] C. Holland and O. V. Komogortsev, "Biometric identification via eye movement scanpaths in reading," in *2011 Int. Joint Conf. Biometrics (IJCB)*, IEEE, Oct. 2011, pp. 1–8, doi: 10.1109/IJCB.2011.6117536.

[31] A. George and A. Routray, "A score level fusion method for eye movement biometrics," *Pattern Recognition Letters*, vol. 82, pp. 207–215, Oct. 2016, doi: 10.1016/j.patrec.2015.11.020. *(Reports EER ≈ 2.59% on the random-stimulus task, BioEye 2015 data; see §21 verification note.)*

[32] T. Kinnunen, F. Sedlak, and R. Bednarik, "Towards task-independent person authentication using eye movement signals," in *Proc. 2010 Symp. Eye-Tracking Research & Applications*, ETRA '10, ACM, Mar. 2010, pp. 187–190, doi: 10.1145/1743666.1743712.

[33] L. A. Jäger, S. Makowski, P. Prasse, S. Liehr, M. Seidler, and T. Scheffer, "Deep Eyedentification: Biometric Identification Using Micro-movements of the Eye," in *Machine Learning and Knowledge Discovery in Databases (ECML PKDD 2019)*, Springer, 2020, pp. 299–314, doi: 10.1007/978-3-030-46147-8_18.

[34] S. Makowski, P. Prasse, D. R. Reich, D. Krakowczyk, L. A. Jäger, and T. Scheffer, "DeepEyedentificationLive: Oculomotoric Biometric Identification and Presentation-Attack Detection Using Deep Neural Networks," *IEEE Trans. Biometrics, Behavior, and Identity Science*, vol. 3, no. 4, pp. 506–518, Oct. 2021, doi: 10.1109/TBIOM.2021.3116875.

[35] S. M. K. Al Zaidawi, M. H. U. Prinzler, J. Lührs, and S. Maneth, "An Extensive Study of User Identification via Eye Movements across Multiple Datasets," *Signal Processing: Image Communication*, 2022, doi: 10.1016/j.image.2022.116746. (Preprint: arXiv:2111.05901.)

[36] H. Griffith, D. Lohr, E. Abdulin, and O. Komogortsev, "GazeBase, a large-scale, multi-stimulus, longitudinal eye movement dataset," *Scientific Data*, vol. 8, no. 1, p. 184, Jul. 2021, doi: 10.1038/s41597-021-00959-y.

[37] D. Lohr, S. Aziz, L. Friedman, and O. V. Komogortsev, "GazeBaseVR, a large-scale, longitudinal, binocular eye-tracking dataset collected at virtual reality," *Scientific Data*, vol. 10, no. 1, p. 177, Mar. 2023, doi: 10.1038/s41597-023-02073-7.

[38] S. Makowski, L. A. Jäger, P. Prasse, and T. Scheffer, "JuDo1000 Eye Tracking Data Set," 2020, doi: 10.17605/OSF.IO/5ZPVK. (150 subjects, 4 sessions ≥1 week apart, EyeLink Portable Duo at 1000 Hz.)

[39] V. Nair, W. Guo, J. Mattern, R. Wang, J. F. O'Brien, L. Rosenberg, and D. Song, "Unique Identification of 50,000+ Virtual Reality Users from Head & Hand Motion Data," in *Proc. 32nd USENIX Security Symp. (USENIX Security 23)*, USENIX Association, Aug. 2023, pp. 895–910.

[40] M. R. Miller, F. Herrera, H. Jun, J. A. Landay, and J. N. Bailenson, "Personal identifiability of user tracking data during observation of 360-degree VR video," *Scientific Reports*, vol. 10, no. 1, p. 17404, Oct. 2020, doi: 10.1038/s41598-020-74486-y.

[41] *(arXiv preprint — flagged)* S. Aziz and O. V. Komogortsev, "Exploring the Uncoordinated Privacy Protections of Eye Tracking and VR Motion Data for Unauthorized User Identification," arXiv:2411.12766, Nov. 2024, doi: 10.48550/arXiv.2411.12766.

[42] A. Patergianakis and C. Lambrinoudakis, "Through the looking glass: eye tracking biometrics and the loss of anonymity in extended reality," *International Journal of Information Security*, vol. 25, no. 2, art. 76, 2026, doi: 10.1007/s10207-026-01231-3. (≈96.6% identification on GazeBaseVR during video watching.)

[43] A. Acien, A. Morales, J. V. Monaco, R. Vera-Rodriguez, and J. Fierrez, "TypeNet: Deep Learning Keystroke Biometrics," *IEEE Trans. Biometrics, Behavior, and Identity Science*, vol. 4, no. 1, pp. 57–70, Jan. 2022, doi: 10.1109/TBIOM.2021.3112540.

[44] G. Acar, C. Eubank, S. Englehardt, M. Juarez, A. Narayanan, and C. Diaz, "The Web Never Forgets: Persistent Tracking Mechanisms in the Wild," in *Proc. 2014 ACM SIGSAC Conf. Computer and Communications Security*, CCS '14, ACM, Nov. 2014, pp. 674–689, doi: 10.1145/2660267.2660347.

[45] A. Vastel, P. Laperdrix, W. Rudametkin, and R. Rouvoy, "FP-STALKER: Tracking Browser Fingerprint Evolutions," in *2018 IEEE Symp. Security and Privacy (SP)*, IEEE, May 2018, pp. 728–741, doi: 10.1109/SP.2018.00008.

[46] S. Zimmeck, J. S. Li, H. Kim, S. M. Bellovin, and T. Jebara, "A Privacy Analysis of Cross-device Tracking," in *Proc. 26th USENIX Security Symp. (USENIX Security 17)*, USENIX Association, Aug. 2017, pp. 1391–1408.

[47] J. Steil, I. Hagestedt, M. X. Huang, and A. Bulling, "Privacy-aware eye tracking using differential privacy," in *Proc. 11th ACM Symp. Eye Tracking Research & Applications*, ETRA '19, ACM, Jun. 2019, pp. 1–9, doi: 10.1145/3314111.3319915.

[48] J. Li, A. Roy Chowdhury, K. Fawaz, and Y. Kim, "Kalεido: Real-Time Privacy Control for Eye-Tracking Systems," in *Proc. 30th USENIX Security Symp. (USENIX Security 21)*, USENIX Association, Aug. 2021, pp. 1793–1810.

[49] B. David-John, D. Hosfelt, K. Butler, and E. Jain, "For Your Eyes Only: Privacy-preserving eye-tracking datasets," in *Proc. 2022 Symp. Eye Tracking Research and Applications*, ETRA '22, ACM, Jun. 2022, pp. 1–6, doi: 10.1145/3517031.3529618.

[50] S. Eberz, K. B. Rasmussen, V. Lenders, and I. Martinovic, "Looks Like Eve: Exposing Insider Threats Using Eye Movement Biometrics," *ACM Trans. Priv. Secur.*, vol. 19, no. 1, art. 1, pp. 1:1–1:31, Jun. 2016, doi: 10.1145/2904018. *(Cross-task continuous authentication, 2-week-stable, reliable down to 50 Hz on a downsampled 500 Hz Tobii; 30 subjects.)*

[51] H. Liao, W. Zhao, C. Zhang, and W. Dong, "Exploring Eye Movement Biometrics in Real-World Activities: A Case Study of Wayfinding," *Sensors*, vol. 22, no. 8, art. 2949, Apr. 2022, doi: 10.3390/s22082949. *(Implicit, stimulus-independent ID in real-world wayfinding; SMI ETG glasses at 60 Hz, 39 subjects; leave-one-route-out 64% / EER 12.1%.)*

[52] I. Rigas, O. Komogortsev, and R. Shadmehr, "Biometric Recognition via Eye Movements: Saccadic Vigor and Acceleration Cues," *ACM Trans. Appl. Percept.*, vol. 13, no. 2, art. 6, pp. 6:1–6:21, Jan. 2016, doi: 10.1145/2842614. *(Saccadic vigor/acceleration added to CEM-B; EyeLink 1000 at 1000 Hz, 322 subjects; vigor signal in a >75 Hz band.)*

[53] C. Li, J. Xue, C. Quan, J. Yue, and C. Zhang, "Biometric recognition via texture features of eye movement trajectories in a visual searching task," *PLoS ONE*, vol. 13, no. 4, art. e0194475, Apr. 2018, doi: 10.1371/journal.pone.0194475. *(Gabor-wavelet scanpath-texture features; Tobii TX300, 58 subjects; EER ≈0.89% short-term, template aging inflates EER 74–1075%.)*

[54] C. Galdi, M. Nappi, D. Riccio, and H. Wechsler, "Eye movement analysis for human authentication: a critical survey," *Pattern Recognition Letters*, vol. 84, pp. 272–283, Dec. 2016, doi: 10.1016/j.patrec.2016.11.002. *(Critical survey; standards/uncontrolled-settings critique; attributes the 88.6%/5.8%/320-subject figure to a Rigas fusion scheme — see the [31] verification note.)*

---

# Appendix A — Novelty positioning, threat-model realism, and threats to validity

*Added 2026-07-11 after a full read of the ingested literature (see the wiki `sources/`). This
appendix is written to pre-empt the objections a PoPETs / USENIX Security / CCS reviewer will
raise. It does not change the thesis — it hardens it. Read it as the "what a skeptical reviewer
will say, and what in the design answers them" companion to §18.*

## A.1 Is the contribution novel? Yes — the novelty is the *intersection*, not any single axis

The empty cell is real. Stacking the four axes:

- Eye-movement biometrics is proven, but only on **research-grade IR hardware**, cooperative
  enrollment, and framed as *authentication* — Holland [30], George & Routray [31] (EER ≈2.59%,
  153 subjects), Kinnunen [32], Deep Eyedentification [33], [34], Eye Know You Too [20]
  (0.58% EER at 60 s → 3.66% at 5 s), Al Zaidawi [35], Rigas [52], Li [53]. **Cross-task and
  low-rate are already shown** — Eberz [50] (cross-task, 2-week-stable, 50 Hz), Liao [51]
  (stimulus-independent, real-world, 60 Hz) — but on cooperative IR/mobile trackers and as
  *authentication*, never as covert commodity-webcam re-ID (the three distinctions in §18.2).
- Behavioral re-ID at population **scale / cross-device** is proven, but only in **VR** — Nair
  55,541 users at 94.3% from 100 s [39], Miller 95% of 511 from <5 min [40], Patergianakis
  96.6% on GazeBaseVR video-watching [42].
- Stateless web tracking is proven, but only for **device-bound** fingerprints that anti-FP
  browsers defeat and a fresh device resets — Acar [44], FP-STALKER [45], Zimmeck [46].
- Commodity webcam gaze on the desktop is proven **usable** (Kaduk et al. 2024 report ≈1.4°,
  within ≈0.5° of an EyeLink 1000; WebEyeTrack ≈2.32 cm [25]) but has **never** been used for
  cross-task, cross-site re-identification as a tracking vector.

No published work occupies {commodity webcam × open desktop web × cross-task/cross-site × re-ID
framed as an unclearable tracking channel} and quantifies its gap to the IR ceiling on the
*same* subjects.

**Rebut the "this is just eye-movement biometrics on a worse sensor" objection head-on.** The
contribution is *not* a new biometric model. It is: (i) the first characterization of the
**commodity webcam** channel for re-ID (a sensor nobody in the EMB literature uses); (ii) the
first **cross-task / cross-site transfer** measured as a *tracking* threat rather than
same-task authentication; (iii) the first **ceiling-vs-commodity** gap on the same subjects and
sessions (RQ3); and (iv) the reframing of gaze as a **stateless, person-bound, unclearable web
identifier** contrasted against the clearable-cookie baseline. Any *one* axis alone is not
publishable; the *stack* is. Say this explicitly in the introduction.

## A.2 The three risks that actually decide acceptance (none of them is "novelty")

1. **Empirical** — does webcam *cross-task* re-ID beat chance by a margin worth a paper? (A.7)
2. **Threat-model realism** — camera-consent friction and the cross-origin mechanism. (A.4)
3. **Confounds** — is a match the *person*, or the *session / calibration / tracker*? (A.3)

If A.3 is not addressed convincingly, the paper is rejected regardless of the numbers. Treat it
as the primary methodological contribution, not an afterthought.

## A.3 Confound controls the paper *must* run (the #1 reviewer trap)

The danger: a commodity webcam tracker self-calibrates per session (WebGazer fits a ridge
regression from clicks). Two sessions of the same person may match because they share a
*calibration geometry, screen, or lighting* — not because their **eyes** are individual. If so,
the "biometric" is an apparatus artifact and the whole result is spurious. **This battery is
RQ0 (§8)** — the precondition every other RQ depends on, and the pilot to run *first* (§20 step
7). Controls to pre-register:

- **Calibration-swap / never-share-calibration.** Gallery and probe sessions of the same person
  must use **independent** calibrations (different day, re-calibrated from scratch — the harness
  already clears the model on a fresh session). Additionally run a *deliberate* control where
  the same person is enrolled and probed under **different calibration procedures** and confirm
  re-ID survives.
- **Cross-tracker generalization.** Enroll on one webcam tracker, identify on another
  (WebGazer → EyeGestures). If re-ID *only* works within a single tracker's idiosyncratic
  output, the signal is tracker-specific, not person-specific. (This is separate from RQ3,
  which reports each tracker *in isolation* for fairness.)
- **Shuffled-label null.** Recompute the entire pipeline with subject labels permuted; rank-1
  and EER must collapse to chance. Report it — it is the cheapest credibility win.
- **Appearance ablation** (*optional / contingent*, §12): dynamics-only is the primary — the
  harness captures no appearance, so "survives face removal" holds by construction. A
  dynamics+appearance arm (to show how much signal is *movement* vs *looks*) requires first
  adding an appearance-embedding channel; run it only if that channel is built.
- **Session/lighting/time negative controls.** Include at least one session under changed
  lighting/seating and, where possible, a different webcam, and show the confusion is not
  driven by capture conditions (e.g., that impostors sharing a session's lighting are not
  systematically closer).
- **Demographic-homogeneity control.** A lab-recruited gallery can be demographically narrow, so
  a "match" might exploit coarse demographic clustering (age band, glasses, gender) rather than
  fine individual identity. Recruit for spread where possible, and report whether impostor
  distances are systematically smaller *within* shared demographic strata (the per-session
  `condition` metadata already records glasses; capture the rest at enrollment). If they are,
  bound the identity claim accordingly rather than overstating it.
- **Within-session leakage bound.** Split a single session into enroll/probe halves as an
  *upper bound*, and always report the cross-session, cross-task cell separately so the easy
  case never masquerades as the threat.

## A.4 Threat-model realism — confront the camera-consent objection directly

A reviewer's first instinct: "camera permission is high-friction, per-origin, revocable, and
shows a visible indicator — this is nothing like a silent cookie." Answers to bake into §2 and
§7:

- **The correct mechanism** (now fixed in §7): a provider's script running **first-party** on
  many sites, each with its own one-time camera grant, linked **server-side**. Not a
  third-party iframe silently inheriting the camera (the platform forbids that). This is weaker
  than "silent everywhere" but still realistic — it is exactly how analytics/ad tags already
  operate, minus the camera.
- **Why the camera grant is increasingly *available*.** Do not assume it; argue it. Legitimate,
  growing contexts that already ask for the webcam and would host such a tag: **accessibility**
  gaze navigation (Razuman et al. 2025), **online proctoring**, attention/UX analytics
  (WebGazer's own pitch), "look-to-scroll"/gaze UI, **WebXR**, and the surge of
  **gaze-conditioned AI** (From Gaze to Data [9]; GazeLLM [11]; GazeQwen [16]; GazeVLM [18];
  gaze-aware assistants [26]). Gaze capture is being normalized for benign reasons — that
  normalization *is* the enabling condition. Cite Liebling & Preibusch [6]: webcam privacy loss
  is obvious to users, but **gaze extraction is opaque** — a consented camera feed does not
  signal that oculomotor *identity* is being harvested.
- **Covert calibration is the drive-by nugget — foreground it.** WebGazer/SearchGazer
  self-calibrate from ordinary clicks ([4], [7]); the attacker needs **no explicit calibration
  step**, so capture is genuinely drive-by. This is a stronger novelty point than the plan
  currently makes.
- **Scope honestly.** This is a *conditional* threat (needs a camera grant). Say so plainly and
  then argue the condition is increasingly met. Reviewers punish overclaiming far more than a
  well-scoped conditional threat.

## A.5 Defusing the "webcam gaze is too noisy for biometrics" objection

- **The trajectory is on your side:** Kaduk et al. 2024 (≈1.4°, near EyeLink), WebEyeTrack
  ≈2.32 cm [25], GazeFollower ≈0.92 cm — the accuracy objection is weakening year over year.
- **The load-bearing argument:** re-ID is **content-independent and distributional** — it needs
  *stable per-person dynamics* (fixation/saccade distributions, main-sequence slope), **not**
  pointing precision. Thilderkvist & Dobslaw 2024 show webcam gaze fails at *fine AOI-level*
  reading; that bounds the content-*dependent* vectors (D2), **not** the distributional re-ID
  signal. Make this distinction explicitly — otherwise a reviewer will cite Thilderkvist
  against you and you will have no answer on the page.
- Report *which* features survive rate-equalization to a common cadence (fixation-duration
  statistics likely robust; saccade-velocity / main-sequence features likely degraded) — turning
  the sampling-rate limitation into a finding. This has **direct precedent**: Eberz [50] finds
  authentication survives downsampling to 50 Hz but that **microsaccade-tied features degrade
  most** (statistically significant), and Rigas [52] places the saccadic-vigor signal in a
  **>75 Hz band** — so the expected casualty list is known in advance. **Note the direction of
  the risk:** the danger is not only that low true rate *weakens* saccade features, but that the
  *logged* rate varies across sessions/participants and can *manufacture* a spurious identity
  signal (see the §9 sampling-rate caveat); the rate-equalized control (`reid.py`) is what
  separates the two. (Caveat when citing Eberz: it decimates a **clean 500 Hz IR** stream,
  whereas the webcam is *natively* low-rate and noisy — "50 Hz works" is encouraging, not
  equivalent.)

## A.6 Ethics, IRB, disclosure, and artifact hygiene (table-stakes at top-tier security venues)

- **IRB: exempt (determination on file).** The study runs under a TAMU IRB-exempt
  determination, consistent with the repo README — not a gating or open item. Retain the
  determination reference for the paper's ethics statement, and keep consent + data-handling
  language documented regardless.
- **Do not ship participant gaze in git.** The repo tracks **29 real `data/*.json` session
  logs**; the `.gitignore` rule for them is commented out. Untrack and scrub history before any
  artifact release, and state the data-handling regime in the paper.
- **Responsible disclosure.** Security PCs increasingly expect it: disclose to browser vendors
  and the W3C (the camera-permission / Permissions-Policy model is the relevant surface) and
  document the timeline. Pair the attack with the RQ5 defense so the paper is not "attack only."
- **Artifact evaluation.** The harness already exists and is tracker-pluggable with a test
  suite — a strong artifact-evaluation submission, and a differentiator. Plan for it.

## A.7 Sharpened headline results and a fallback ladder

Lead with the crispest, most defensible results; do not stake the paper on the riskiest cell.

1. **Accuracy-vs-observation-window curve on the webcam channel** — "how many seconds of
   viewing links you." Quotable, and the IR ceiling already shows a steep curve (EKYT
   0.58%→3.66% [20]).
2. **Ceiling-vs-commodity gap (RQ3)** — novel and uniquely yours (both devices, same subjects).
3. **Unclearability demonstration (RQ4)** — survives cookie/cache clear, incognito, new
   profile, new device, face de-identification; the live wipe-state + cross-origin demo.
4. **Cross-task transfer (RQ2)** — the most differentiating but riskiest.

**Fallback ladder if the webcam numbers are weak:** if cross-task is weak, narrow the claim to
*same-genre* sites (e.g., reading→reading) — still a meaningful tracking threat. If webcam EER
is high in absolute terms, the contribution becomes the **gap curve** plus the framing "a
degraded-but-non-random identifier that, unlike a cookie, the user *cannot clear*" — quantified
against the canvas/UA baseline [44]–[46]. A well-scoped lower bound is publishable; an
overclaimed headline is not.

## A.8 Venue tuning

- **PoPETs / PETS (recommended first target).** Best topical fit; rolling quarterly deadlines
  suit iteration; values measurement + a defense. Submit here first, defense **included** (not
  optional), with the confound controls (A.3) front and center.
- **USENIX Security / CCS / S&P (reach).** Need the end-to-end **cross-origin linkage demo**
  working, a **crisp cross-task attack number**, and a **responsible-disclosure** section. The
  bar is a clean, quantified attack — not a feasibility study.
- **SOUPS (companion).** The camera-consent opacity (A.4) and a user study on what people
  believe they are granting is a natural companion paper — and directly reuses the IRB and
  consent materials.
- **WPES (hedge).** Early feedback co-located with CCS.

## A.9 One-paragraph "novelty statement" to reuse in the intro and rebuttals

> Eye-movement biometrics is mature on infrared hardware; behavioral re-identification at scale
> is established in virtual reality; stateless web tracking is established for device-bound
> fingerprints. We are the first to show that **commodity, in-browser webcam gaze on the open
> desktop web re-identifies users across tasks and across sites as a stateless, person-bound
> identifier that survives clearing all client-side state and removing the face from the video**,
> and to measure that channel's gap to a research-grade infrared ceiling on the same subjects.
> The novelty is the intersection of sensor (commodity webcam), setting (drive-by desktop web),
> transfer (cross-task/cross-site), and framing (unclearable tracking vector) — no prior work
> occupies it.
