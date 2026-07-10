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

---

## 15. Related work in this direction

There **is** a large literature adjacent to this proposal — eye-movement biometrics is a mature field — but **no published work occupies the exact cell this protocol targets: commodity in-browser webcam gaze, on a desktop, used for *cross-site, cross-task* re-identification framed as an unclearable web-tracking vector.** Every close analogue differs on at least one of {hardware, setting, task-transfer, framing}. The papers below are grouped by the role they play in the argument; citation numbers **continue the companion report's shared bibliography** (which ends at [29]), so [30]+ are new here. Entries already in the report — Eye Know You Too [20], continuous gaze-offset fusion [29], WebEyeTrack [25], SearchGazer [4], Eye-of-the-Typer [7], the handheld-privacy work [10], and the streaming-DP defenses [13], [23], [24] — are load-bearing for this direction too and are not repeated.

### 15.1 Eye-movement biometrics: the identification signal exists (foundations for RQ1, §7)

These establish that eye-movement *dynamics* re-identify people, and define the hand-crafted feature set the protocol's route (a) uses. They are research-grade IR / cooperative-enrollment ceilings, not the webcam threat — cite them as "the signal is real and individual," then show the commodity gap (RQ3).

- **Holland & Komogortsev [30]** — reading-scanpath biometrics; the origin of the fixation/saccade + "main-sequence" feature family named in §7.
- **George & Routray [31]** — RBFN score-level fusion of fixation/saccade features, 320 subjects, EER ≈ 5.8%; a strong, interpretable small-N baseline for route (a).
- **Jäger et al., "Deep Eyedentification" [33]** and **Makowski et al., "DeepEyedentificationLive" [34]** — deep identification from eye *micro-movements* (plus presentation-attack detection); the end-to-end ceiling for route (b), alongside Eye Know You Too [20].
- **Al Zaidawi et al. [35]** — cross-dataset identification and explicit **template-aging** analysis; directly relevant to the cross-session stability claim (RQ4) and to honest degradation reporting.

### 15.2 The cross-task problem — the RQ2 headline has precedent but is under-studied

This is the differentiator. Most biometric papers enroll and test on the *same* task; the tracking threat needs task/stimulus transfer ("enroll on site A, identify on site B").

- **Kinnunen et al. [32]** — the canonical **task-independent** eye-movement authentication paper: no assumption that train/test share a stimulus. This is the closest prior framing to RQ2 and should anchor the cross-task discussion — including its honest failure modes (high FRR on 9 subjects), which motivate the protocol's longer windows and distributional features.

### 15.3 Longitudinal & large-N datasets (the ceiling and the gallery-size axis, §5, §8)

Back the deep-model / large-population feasibility claim on public data, reserve fresh simultaneous capture for the webcam claim.

- **Griffith et al., GazeBase [36]** — 322 subjects, 9 rounds over 37 months; the reference longitudinal set for test–retest and the ceiling model.
- **Lohr et al., GazeBaseVR [37]** — binocular VR extension; useful for the gallery-size scaling curve and a VR contrast point. (JuDo1000, named in §5, sits here too.)

### 15.4 Behavioral biometrics as an unclearable, *scalable* identifier — the tracking-vector analogue (thesis, §1)

The strongest analogues for the *framing*: physically-grounded behavioral signals that (i) scale to huge galleries and (ii) persist across sessions/devices without any client-side state. None is desktop-webcam gaze, so each is a supporting analogy, not a scoop.

- **Nair et al., "Unique Identification of 50,000+ VR Users" [39]** — 55,541 users identified from head/hand motion, 94% from 100 s; the definitive "biomechanics scales like a strong biometric" result. The best external evidence that the gallery-size axis (§8) will not collapse the threat, and a direct template for the "person-bound, not device-bound" thesis.
- **Miller et al. [40]** — 360° VR viewing, ~95% identification, **re-identifiable across device types**; near-perfect analogue for the RQ4 cross-device / unclearability claim in a different modality.
- **Aziz & Komogortsev [41]** — shows unprotected motion undoes eye-tracking privacy protections and vice-versa; reinforces that partial defenses leak, relevant to RQ5 scoping.
- **Patergianakis & Lambrinoudakis [42]** — 2026 XR study framing eye-tracking biometrics explicitly as **loss of anonymity** (96.6% on GazeBaseVR's 400+ users); the closest recent "anonymity is the stake" framing to adopt.
- **Acien et al., TypeNet [43]** — keystroke biometrics with <5% degradation scaling to 100k users; a non-gaze precedent that a commodity behavioral channel remains a viable identifier at web scale.

### 15.5 Stateless web tracking & cross-device linkage — the "clearable cookie" baseline (§1 contribution 1, §9 baselines)

These define the bar the paper argues gaze *clears*: stateless-but-device-bound fingerprints that anti-FP browsers defeat and that reset on a new device. Use them as the explicit comparison in the metrics.

- **Acar et al., "The Web Never Forgets" [44]** — canvas fingerprinting / evercookies / cookie-syncing in the wild; the reference for "persistent tracking mechanisms" and the rhetorical anchor for the title framing.
- **Vastel et al., FP-STALKER [45]** — links *evolving* browser fingerprints over time; the state-of-the-art stateless linkage the gaze channel is contrasted against (fingerprints drift and can be reset; gaze is person-bound).
- **Zimmeck et al. [46]** — cross-device tracking analysis; the prior model for linking one person across contexts, which gaze does *without* the shared-network/deterministic-identifier assumptions.

### 15.6 Defenses for the gaze channel (RQ5, §11)

Beyond the streaming-DP work already cited ([13], [23], [24]), these complete the defense landscape for the privacy–utility curve.

- **Steil et al. [47]** — the foundational **differential-privacy-for-gaze** paper (feature-level DP on eye-movement data); the natural first perturbation to evaluate.
- **Li et al., Kalεido [48]** — USENIX Security real-time gaze-DP *system* with formal guarantees; the deployment-shaped defense to benchmark the in-browser perturbation layer against.
- **David-John et al., "For Your Eyes Only" [49]** — adapts **k-anonymity / plausible deniability** specifically to defeat eye-movement *re-identification* on datasets; the defense whose threat model matches this protocol most exactly.

### 15.7 The gap this protocol fills

Stack the four axes and the white space is unambiguous: eye-movement biometrics is proven on **IR hardware** ([20], [30]–[37]); behavioral-biometric tracking at **scale/cross-device** is proven in **VR** ([39], [40]); stateless web tracking is proven for **device-bound fingerprints** ([44]–[46]). No one has shown **commodity webcam gaze, on the open desktop web, re-identifying users cross-task and cross-site as an unclearable tracking channel**, and quantified its gap to the IR ceiling on the *same* subjects (RQ3). That intersection — not any single axis — is the contribution.

---

## 16. Additional references (continuing the shared bibliography)

*Numbering continues from the companion report's [29]. Peer-reviewed venues are preferred; arXiv entries are flagged and their quantitative claims treated as indicative.*

[30] C. Holland and O. V. Komogortsev, "Biometric identification via eye movement scanpaths in reading," in *2011 Int. Joint Conf. Biometrics (IJCB)*, IEEE, Oct. 2011, pp. 1–8, doi: 10.1109/IJCB.2011.6117536.

[31] A. George and A. Routray, "A score level fusion method for eye movement biometrics," *Pattern Recognition Letters*, vol. 82, pp. 207–215, Oct. 2016, doi: 10.1016/j.patrec.2015.11.020.

[32] T. Kinnunen, F. Sedlak, and R. Bednarik, "Towards task-independent person authentication using eye movement signals," in *Proc. 2010 Symp. Eye-Tracking Research & Applications*, ETRA '10, ACM, Mar. 2010, pp. 187–190, doi: 10.1145/1743666.1743712.

[33] L. A. Jäger, S. Makowski, P. Prasse, S. Liehr, M. Seidler, and T. Scheffer, "Deep Eyedentification: Biometric Identification Using Micro-movements of the Eye," in *Machine Learning and Knowledge Discovery in Databases (ECML PKDD 2019)*, Springer, 2020, pp. 299–314, doi: 10.1007/978-3-030-46147-8_18.

[34] S. Makowski, P. Prasse, D. R. Reich, D. Krakowczyk, L. A. Jäger, and T. Scheffer, "DeepEyedentificationLive: Oculomotoric Biometric Identification and Presentation-Attack Detection Using Deep Neural Networks," *IEEE Trans. Biometrics, Behavior, and Identity Science*, vol. 3, no. 4, pp. 506–518, Oct. 2021, doi: 10.1109/TBIOM.2021.3116875.

[35] S. M. K. Al Zaidawi, M. H. U. Prinzler, J. Lührs, and S. Maneth, "An Extensive Study of User Identification via Eye Movements across Multiple Datasets," arXiv:2111.05901, Nov. 2021, doi: 10.48550/arXiv.2111.05901. (Journal version: *Signal Processing: Image Communication*, 2022.)

[36] H. Griffith, D. Lohr, E. Abdulin, and O. Komogortsev, "GazeBase, a large-scale, multi-stimulus, longitudinal eye movement dataset," *Scientific Data*, vol. 8, no. 1, p. 184, Jul. 2021, doi: 10.1038/s41597-021-00959-y.

[37] D. Lohr, S. Aziz, L. Friedman, and O. V. Komogortsev, "GazeBaseVR, a large-scale, longitudinal, binocular eye-tracking dataset collected at virtual reality," *Scientific Data*, vol. 10, no. 1, p. 177, Mar. 2023, doi: 10.1038/s41597-023-02073-7.

[38] *(reserved — JuDo1000 dataset, referenced in §5; add exact citation when fixed.)*

[39] V. Nair, W. Guo, J. Mattern, R. Wang, J. F. O'Brien, L. Rosenberg, and D. Song, "Unique Identification of 50,000+ Virtual Reality Users from Head & Hand Motion Data," in *Proc. 32nd USENIX Security Symp. (USENIX Security 23)*, USENIX Association, Aug. 2023, pp. 895–910.

[40] M. R. Miller, F. Herrera, H. Jun, J. A. Landay, and J. N. Bailenson, "Personal identifiability of user tracking data during observation of 360-degree VR video," *Scientific Reports*, vol. 10, no. 1, p. 17404, Oct. 2020, doi: 10.1038/s41598-020-74486-y.

[41] S. Aziz and O. V. Komogortsev, "Exploring the Uncoordinated Privacy Protections of Eye Tracking and VR Motion Data for Unauthorized User Identification," arXiv:2411.12766, Nov. 2024, doi: 10.48550/arXiv.2411.12766.

[42] A. Patergianakis and C. Lambrinoudakis, "Through the looking glass: eye tracking biometrics and the loss of anonymity in extended reality," *International Journal of Information Security*, vol. 25, no. 2, art. 76, 2026, doi: 10.1007/s10207-026-01231-3.

[43] A. Acien, A. Morales, J. V. Monaco, R. Vera-Rodriguez, and J. Fierrez, "TypeNet: Deep Learning Keystroke Biometrics," *IEEE Trans. Biometrics, Behavior, and Identity Science*, vol. 4, no. 1, pp. 57–70, Jan. 2022, doi: 10.1109/TBIOM.2021.3112540.

[44] G. Acar, C. Eubank, S. Englehardt, M. Juarez, A. Narayanan, and C. Diaz, "The Web Never Forgets: Persistent Tracking Mechanisms in the Wild," in *Proc. 2014 ACM SIGSAC Conf. Computer and Communications Security*, CCS '14, ACM, Nov. 2014, pp. 674–689, doi: 10.1145/2660267.2660347.

[45] A. Vastel, P. Laperdrix, W. Rudametkin, and R. Rouvoy, "FP-STALKER: Tracking Browser Fingerprint Evolutions," in *2018 IEEE Symp. Security and Privacy (SP)*, IEEE, May 2018, pp. 728–741, doi: 10.1109/SP.2018.00008.

[46] S. Zimmeck, J. S. Li, H. Kim, S. M. Bellovin, and T. Jebara, "A Privacy Analysis of Cross-device Tracking," in *Proc. 26th USENIX Security Symp. (USENIX Security 17)*, USENIX Association, Aug. 2017, pp. 1391–1408.

[47] J. Steil, I. Hagestedt, M. X. Huang, and A. Bulling, "Privacy-aware eye tracking using differential privacy," in *Proc. 11th ACM Symp. Eye Tracking Research & Applications*, ETRA '19, ACM, Jun. 2019, pp. 1–9, doi: 10.1145/3314111.3319915.

[48] J. Li, A. Roy Chowdhury, K. Fawaz, and Y. Kim, "Kalεido: Real-Time Privacy Control for Eye-Tracking Systems," in *Proc. 30th USENIX Security Symp. (USENIX Security 21)*, USENIX Association, Aug. 2021, pp. 1793–1810.

[49] B. David-John, D. Hosfelt, K. Butler, and E. Jain, "For Your Eyes Only: Privacy-preserving eye-tracking datasets," in *Proc. 2022 Symp. Eye Tracking Research and Applications*, ETRA '22, ACM, Jun. 2022, pp. 1–6, doi: 10.1145/3517031.3529618.
