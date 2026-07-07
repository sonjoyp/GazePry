# GazePry Direction 1 — Study Protocol

**Cross-Site Gaze Re-Identification as an Unclearable Web Tracking Vector**

*A study protocol for a security/privacy publication. Companion to `GazePry_Information_Leakage_Report.md`.*

---

## 1. Thesis and contribution

**Thesis.** Eye-movement dynamics captured by a commodity, in-browser webcam gaze tracker form a *stateless, person-bound* re-identification signal that browser privacy controls do not remove — clearing cookies, incognito mode, storage partitioning, and even switching devices leave it intact — and that survives removal of the face from the video, because it is carried by *movement dynamics*, not appearance.

**Why this is the right contribution.** The same-origin policy and site isolation block a script from reading gaze on *another* site (content peeking is not feasible — see the threat-model report §8). Re-identification is *content-independent*, so SOP does not touch it: two first-party sites that embed the same tracking script can link the same visitor by their gaze. This turns the report's own limitation into the paper's thesis.

**Three contributions:**
1. **A new tracking channel.** Gaze as a cookieless, cache-proof, incognito-surviving, cross-device re-identifier — a *person-bound* fingerprint, unlike canvas/font/device fingerprints which are device-bound and defeated by anti-fingerprinting browsers.
2. **Ceiling vs. commodity.** The gap between research-grade hardware (Gazepoint) and the deployed webcam channel (WebGazer / WebEyeTrack), measured on the *same* subjects. This is the direct payoff of having both devices.
3. **(Optional) A defense.** An in-browser perturbation layer that raises attacker EER at bounded utility cost, plotted as a privacy–utility curve.

---

## 2. Threat model

- **Adversary:** a tracking/analytics provider whose JS SDK is embedded across multiple first-party sites (the same structural position as an ad or analytics tag). Each embedding inherits the host page's camera permission or prompts once.
- **Goal:** link a visitor's sessions across sites and over time to a persistent pseudonymous identity **without cookies or client-side state**.
- **Capability:** client-side JS only; gaze estimation in-browser; covert calibration from ordinary mouse clicks (present in the WebGazer/GazePry lineage). Features can be computed client-side, so the adversary never needs to store the raw face.
- **Out of scope (and stated as such):** reading another origin's content (blocked by SOP), physically-present cameras, VR/MR headsets. This is a *drive-by desktop web* adversary — the gap in the literature.

**Delta from prior work (state this in Related Work):**

| Prior work | Setting | What makes ours different |
|---|---|---|
| Eye Know You Too [20], GazeBase biometrics | Research IR hardware, cooperative enrollment, same task, *authentication* | Adversarial webcam, cross-task, cross-site *tracking*, unclearable-identifier framing |
| Alsakar et al. handheld privacy [10] | Mobile front camera, *attribute* inference, single site | Desktop, cross-site *linkage*, *identity* not attributes |
| Canvas/font/device fingerprinting | Stateless but device-bound; defeated by anti-FP browsers | Physically grounded, *person*-bound, survives fresh device + face removal |
| EyeTell [27], GAZEploit [14] | Content-*dependent* keystroke inference | Content-*independent*; identity, not secrets |

---

## 3. Research questions

- **RQ1 (baseline):** How reliably can the webcam channel re-identify a returning user *same-task, cross-session*? (test–retest across days)
- **RQ2 (the tracking threat):** How much does re-ID degrade *cross-task / cross-stimulus* — enroll on site A's content, identify on site B's? This is the headline result; biometrics papers usually skip it.
- **RQ3 (ceiling vs. commodity):** What is the EER/rank-1 gap between Gazepoint, WebGazer, and WebEyeTrack on the *same* subjects and sessions?
- **RQ4 (unclearability):** Does re-ID survive cookie/cache clear, incognito, a fresh browser profile, a different day/lighting, a *different device webcam*, and *face de-identification*?
- **RQ5 (defense, optional):** What perturbation of the gaze stream defeats re-ID at acceptable utility cost?

---

## 4. Apparatus

**Recommended rig — simultaneous capture.** Record the webcam video *while* Gazepoint tracks. The Gazepoint IR gives a per-frame ground-truth gaze label for every webcam frame, so you get (a) clean labels to train/validate the webcam estimate and (b) matched per-subject data across both channels in one session. This is the cleanest way to answer RQ3.

**Three tracker arms:**
1. **Gazepoint GP3 / GP3 HD** (60/150 Hz IR) — the ceiling.
2. **WebGazer** (current brownhci build, `www/search`) — ridge regression, no head pose; the deployed reality and the GazePry lineage. *Do not use the stale GazePry/SearchGazer fork — 2016 selectors are dead.*
3. **WebEyeTrack** [25] — head-pose-aware (~2.32 cm); the near-future commodity ceiling.

**Sampling-rate caveat (methodological, state it):** webcam capture is ~30 Hz; Gazepoint is 60–150 Hz. Down-sample Gazepoint to the webcam rate for the *fair* comparison arm, and note that low webcam framerate limits saccade-velocity features — a real constraint on what the commodity channel can extract.

---

## 5. Participants and sessions

- **N:** target **40–60** for a first paper; more strengthens the verification (EER) claim. Use public datasets (below) to back the large-N *feasibility ceiling*.
- **Sessions:** **≥2–3 per participant, separated by ≥1 week.** Within-session re-ID is trivially easy and not the threat; *cross-session, time-separated* re-ID is the real "returning visitor" test and the number reviewers will look for.
- **Realistic-variation conditions:** at least one session under different lighting / seating; if you have a second laptop, one session on a *different webcam* to support the cross-device claim.
- **IRB:** camera capture of identifiable subjects = human-subjects research. **File the TAMU IRB protocol now** — it is the critical-path gate. Plan consent language carefully (it is also material for a possible SOUPS companion study).
- **Public datasets for the ceiling / large-N feasibility:** GazeBase (322 subjects, multi-round), GazeBaseVR, JuDo1000. Use these for the deep-model biometric ceiling; use *fresh* simultaneous capture for the webcam claim.

---

## 6. Stimuli — the multi-"site" design

Different tasks elicit different gaze dynamics, so distinct tasks stand in for distinct "sites." Enroll on one, identify on another to test cross-site generalization.

1. **Reading** — a text passage (reading biometrics heritage, [7], [22]).
2. **SERP scanning** — a search-results layout (the SearchGazer core, [4]).
3. **Free image viewing.**
4. **Video watching.**
5. **Form / typing task.**

Report **same-task** (upper bound) and **cross-task** (the tracking threat) separately.

---

## 7. Features and models

- **Content-independent features (primary):** fixation durations, saccade amplitudes and velocities (the "main sequence" relationship is highly individual), blink rate, pupil dynamics, microsaccades if resolvable. These are the classic eye-movement biometric features.
- **Two modeling routes:**
  - **(a) Hand-crafted features + classifier** — interpretable, robust at small N. Start here.
  - **(b) End-to-end deep model** (DenseNet-style, à la Eye Know You Too [20]) — the ceiling; train/validate on public data, fine-tune on yours.
- **Critical control:** the primary condition **excludes the raw face image / appearance features**, so the "survives de-identification" claim is clean. Run an appearance-*including* arm only as an upper bound, to quantify how much signal is dynamics vs. appearance.

---

## 8. Conditions matrix

The experimental cells (each × 3 tracker arms):

| Axis | Levels |
|---|---|
| Task pairing | same-task / cross-task |
| Session | same-session / cross-session (≥1 wk) |
| Observation window | 5 s / 15 s / 30 s / 60 s / full |
| Gallery size | 10 / 25 / 50 / full (scaling to a tracked population) |
| Intervention | none / cookie-cache clear / incognito / new profile / new device / face-blur |
| Features | dynamics-only / dynamics+appearance |

Headline cell: **cross-task, cross-session, dynamics-only, webcam** — that is the real-world tracking threat.

---

## 9. Metrics

- **Identification:** rank-1 / rank-5 accuracy; CMC curve.
- **Verification:** EER; ROC / AUC.
- **Two key curves:**
  - Accuracy vs. **observation window** — "how many seconds of viewing links you" (a practical, quotable result).
  - Accuracy vs. **gallery size** — how the threat scales to a large tracked population.
- **Baselines:** chance; conventional fingerprint (canvas/UA) as the *clearable* comparison — the point is gaze persists where those reset after a clear.

---

## 10. Analysis plan

- Report degradation from ceiling (Gazepoint) → WebEyeTrack → WebGazer for each cell.
- Statistical treatment of cross-session stability (test–retest); report confidence intervals over subject splits, not a single split.
- Honest headline: even a **degraded-but-non-random** webcam EER is a publishable tracking threat when the comparison is "a cookie the user *can* clear." Frame webcam numbers as a *lower bound* on the threat.

---

## 11. Defense (optional, RQ5)

Perturb the client-side gaze stream (temporal/Gaussian noise, down-sampling, spatial DP à la David-John et al. [24], or the streaming-DP approach [13]). Show attacker EER rising while a *utility* task (reading-AOI detection or an accessibility metric) stays acceptable. Deliverable: a **privacy–utility tradeoff curve**. Pairing an attack with a defense reviews better.

---

## 12. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Webcam EER too high to be a "threat" | Use WebEyeTrack; longer windows; noise-robust distributional features; frame as lower bound. Even ~15–25% EER beats "clearable cookies." |
| Cross-task generalization weak | Report honestly; if only same-content sites link, the threat narrows to (e.g.) reading sites — still meaningful. |
| N too small for deep models | Public datasets for the deep/ceiling claim; fresh data for the webcam claim. |
| Low webcam framerate kills saccade features | Down-sample Gazepoint for fair comparison; report which features survive 30 Hz. |
| IRB delay | File now — it is the critical path. |

---

## 13. Target venues and timeline

- **Primary:** PETS / PoPETs — strong topical fit, rolling quarterly deadlines (good for iterating). *Confirm the exact cycle date from the current CFP.*
- **Reach:** USENIX Security / CCS / NDSS if the cross-site end-to-end linkage demo is strong.
- **Workshop hedge / early feedback:** WPES (co-located with CCS).
- **Companion:** SOUPS, if you add the consent user study.

**Rough critical path (calendar-bound by IRB + session separation):** IRB 4–8 wk → pilot 2–4 wk → collection 6–10 wk (multi-session forces calendar time) → analysis 4–6 wk → writing 4 wk. ≈ 6–8 months end-to-end; aim at a **PoPETs cycle in H1 2027** or a **USENIX Security 2027** deadline. Verify exact dates against live CFPs before committing.

---

## 14. Immediate next steps

1. Draft and file the **TAMU IRB** protocol (consent + camera capture) — start today; it gates everything.
2. Stand up the **simultaneous Gazepoint + webcam** capture rig; verify per-frame time alignment between IR labels and webcam frames.
3. Pull **current brownhci/WebGazer** (`www/search`) and **WebEyeTrack**; wire both to log per-frame gaze + raw features.
4. Run a **2–3 subject pilot** across all five tasks to sanity-check feature extraction and the same-session re-ID sanity cell before scaling.
5. Pre-register the conditions matrix (§8) and metrics (§9) to keep the cross-task, cross-session claim honest.
