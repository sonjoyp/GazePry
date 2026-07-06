# GazePry — Webcam Eye-Tracking Information Leakage Assessment

**Information Leakage in Webcam-Based Eye Tracking on Laptops, Smartphones, and Tablets**

*A Threat-Model Assessment for the GazePry Project*

---

## Contents

1. [Executive Summary](#1-executive-summary)
2. [Scope and Definitions](#2-scope-and-definitions)
3. [Two Regimes of Gaze-Based Information Leakage](#3-two-regimes-of-gaze-based-information-leakage)
4. [Leakage Vectors (D1–D6)](#4-leakage-vectors-d1d6)
5. [Form-Factor Analysis](#5-form-factor-analysis)
6. [Evidence Summary](#6-evidence-summary)
7. [Enabling Conditions](#7-enabling-conditions)
8. [What Tightens and What Loosens the Threat Model](#8-what-tightens-and-what-loosens-the-threat-model)
9. [Conclusion and Recommended Next Steps](#9-conclusion-and-recommended-next-steps)
10. [References](#references)

---

## 1. Executive Summary

**Yes — a webcam-based eye tracker leaks a substantial amount of sensitive information, and it does so on laptops, smartphones, and tablets alike, although the leakage profile differs by form factor.** The leakage is not incidental. Gaze is a physically grounded signal produced by largely involuntary eye movements, so it carries information that ordinary software-level privacy defenses — anti-fingerprinting countermeasures, sandboxing, or value spoofing — do not touch. This is the central premise of GazePry: because gaze coordinates derive from physical eye behavior rather than from JavaScript-reported values, they behave as a hardware-grounded fingerprint that bypasses defenses operating at the script layer.

Across the published literature, gaze data has been shown to leak at least three broad classes of information: (i) on-screen secrets such as PINs, passwords, and the content a user reads or searches for [4], [7], [8], [12], [27]; (ii) cognitive and affective state such as attention, confusion, mind-wandering, and engagement [1], [2], [22], [26]; and (iii) stable personal attributes such as biometric identity, gender, age, and geographic origin [10], [20], [21], [29]. A 2020 survey of eye gaze in security and privacy applications [3] and a dedicated review of the privacy implications of eye tracking [21] both treat these as well-established, not hypothetical, risk categories.

Two points frame the assessment for this project. First, the most mature concrete attacks (EyeTell [27], GazeRevealer [8]) target smartphones, and the privacy-leakage literature on handheld devices is now well developed [10]. The understudied — and therefore novel — surface for GazePry is the commodity, in-browser webcam attack on a desktop or laptop screen, where mature open-source trackers (WebGazer; WebEyeTrack [25]) make covert, consent-light gaze capture practical but where the security implications have not been characterized systematically. Second, three findings tighten rather than weaken the threat model:

- On mobile, the gaze-coordinate channel is degraded by head motion and screen-size constraints [10], [25], but the camera-permission grant itself becomes the dominant leakage vector: once a page holds the video stream, it can extract biometric and demographic signal regardless of pointing accuracy.
- Cross-tab content peeking is not feasible under the browser's same-origin policy and site isolation, so the cross-site risk is re-identification through behavioral biometrics, not reading another site's content.
- The eye-movement biometric signal persists even when facial identity is stripped from the video, so consent dialogs framed around "the camera cannot see your face" understate the actual exposure.

**Bottom line:** webcam eye tracking is a genuine information-leakage channel on all three device classes. The desktop in-browser case is the least studied and the most defensible contribution; the mobile case is the best evidenced and reframes the camera grant itself as the primary risk.

## 2. Scope and Definitions

This report concerns webcam-based eye tracking: software that estimates where a person is looking using only the ordinary RGB camera built into a laptop, smartphone, or tablet, with no specialized infrared eye tracker, head-mounted display, or external hardware. The reference implementations for the project are WebGazer and its derivatives (SearchGazer [4]; GazePry's own fork of SearchGazer) and the more recent, head-pose-aware WebEyeTrack [25], all of which run entirely in the browser.

"Information leakage" here means any case in which the gaze signal allows an observer to infer something the user did not intend to disclose — a secret being typed, the content being read, a transient mental state, a stable demographic attribute, or a persistent identity. The assumed adversary is a *drive-by web adversary*: a first-party page or an embedded third-party script that obtains camera access and runs gaze estimation client-side. This is deliberately weaker than the adversaries assumed in much of the adjacent literature, which often presupposes a physically present attacker filming the victim [27], a VR/MR avatar feed [14], or eyeglass reflections in a video call [19]. The drive-by web setting is what distinguishes the GazePry threat model and is the gap the project targets.

## 3. Two Regimes of Gaze-Based Information Leakage

It is useful to separate gaze leakage into two regimes, because they have different prerequisites, different defenses, and different behavior across form factors.

### 3.1 Content-dependent leakage

In the content-dependent regime, the adversary controls or knows the on-screen layout and maps gaze coordinates onto that layout to recover what the user is interacting with. If the page renders a numeric keypad at known coordinates, a fixation sequence over those coordinates reconstructs the entered digits. EyeTell demonstrated this for touchscreen soft keyboards from a video of the user's eyes, recovering 4-digit PINs with roughly 39% top-1 and 65% top-5 accuracy and 6-digit PINs with roughly 70% top-5 accuracy [27]; GazeRevealer achieved comparable results from the smartphone front camera alone, around 77.9% per single digit and 84.4% for a full 6-digit password under ideal conditions [8]. The same principle extends to gaze-based graphical passwords entered via webcam [12], and to reading and search behavior: SearchGazer was built specifically to identify which area of interest on a search-results page a visitor is examining in real time [4], and the Eye-of-the-Typer benchmark characterizes gaze behavior during typing in fine detail [7]. Because this regime depends on a known layout, an attacker-controlled page is the natural delivery vehicle.

### 3.2 Content-independent leakage

In the content-independent regime, the adversary does not need to know what is on screen at all. The dynamics of eye movement — fixation durations, saccade velocities and amplitudes, blink patterns, and pupil response — carry information about the person independent of on-screen content. These dynamics leak cognitive and affective state: webcam-grade eye tracking has been used to detect mind-wandering and reading-comprehension errors above chance [22], and gaze has long been used to infer confusion, engagement, and cognitive load in affective tutoring systems [1], [2] and, more recently, in gaze-aware AI assistants that adapt to a user's cognitive needs [26]. The same dynamics encode stable traits. Eye-movement biometrics can re-identify individuals: research-grade systems such as Eye Know You Too reach equal error rates around 0.6% on reading tasks [20], and continuous gaze-offset fusion further improves authentication performance [29]. And gaze leaks demographics: on handheld devices, gender, age, and geographic origin are inferable from front-camera gaze data [10], [21]. This regime is the more dangerous one for privacy because it cannot be defeated by changing what the page displays.

## 4. Leakage Vectors (D1–D6)

The project organizes specific leakage vectors into six directions, mapped below to the two regimes and to representative evidence. D1–D2 are content-dependent; D3–D5 are content-independent; D6 covers defenses.

| ID | Leakage vector | Regime | What leaks | Evidence |
|---|---|---|---|---|
| **D1** | On-screen keyboard / PIN inference | Content-dependent | PINs, passwords, unlock codes | [8], [12], [27] |
| **D2** | Reading content & search intent | Content-dependent | What the user reads, queries, and attends to | [4], [7] |
| **D3** | Cognitive & affective state | Content-independent | Attention, confusion, mind-wandering, engagement, cognitive load | [1], [2], [22], [26] |
| **D4** | Behavioral-biometric re-identification & cross-site tracking | Content-independent | Persistent identity and linkage across sessions, sites, and devices | [20], [29] |
| **D5** | Attribute & demographic inference | Content-independent | Gender, age, geographic origin, and related traits | [10], [21] |
| **D6** | Defenses & drive-by detection | — | Mitigations: differential privacy, on-device processing, consent design | [13], [23], [24] |

Within the project's current codebase, D2 (reading and search-intent inference) is closest to fully implemented, inheriting SearchGazer's area-of-interest instrumentation [4]. D1 (PIN/keypad inference) is the natural content-dependent demonstrator. D3 is partially exploitable today through dwell-time and pupil features, and D4–D5 require building a matching or attribute model on top of the raw per-frame feature stream. One practical caveat from the code review: the bundled Google and Bing DOM selectors date from 2016 and no longer match current live search pages, so a self-hosted, attacker-controlled page is the realistic substrate for demonstration rather than instrumentation of a live third-party SERP.

## 5. Form-Factor Analysis

The question specifically asks about three device classes. The underlying gaze signal is the same physical phenomenon in all three, but the quality of the gaze-coordinate channel, the dominant attack, and the practical enabling conditions differ.

### 5.1 Laptop and desktop — the primary novel surface

On a laptop with a built-in webcam, the user is typically seated at a roughly fixed distance with a relatively stable head pose and a large screen. These are the most favorable conditions for the content-dependent regime: a larger display spreads interface elements across more visual angle, so the gaze-coordinate channel resolves on-screen targets more reliably than on a phone. In-browser trackers run here with no installation. WebGazer self-calibrates by watching ordinary cursor interactions and streams a per-frame gaze estimate, but its ridge-regression model lacks head-pose awareness and its accuracy degrades over a session, with point-of-gaze error rising from roughly 5 cm to 10 cm over twenty minutes [7], [25]. WebEyeTrack closes much of that gap: it is head-pose-aware, calibrates from as few as nine samples, achieves around 2.32 cm error, and is roughly twice as accurate as WebGazer [25]. The implication is that the accuracy objection to desktop in-browser attacks is weakening over time, not strengthening.

Crucially, this is the surface that the literature has not characterized as a security threat. The closest analogues all assume different conditions: physically present cameras filming the victim [27], VR/MR avatar feeds [14], head-motion side channels in headsets [15], or eyeglass reflections in video calls [19]. None of these is the commodity, consent-light, in-browser desktop case. The content-dependent PIN/keypad attack on a desktop page is, at present, a reasoned extension from the demonstrated mobile results combined with the available in-browser tooling rather than a published result — which is precisely why a minimal, consented demonstrator would be a meaningful contribution.

### 5.2 Smartphone — the best-evidenced surface

The phone is where concrete attacks already exist. EyeTell [27] and GazeRevealer [8] both reconstruct PINs and passwords on touchscreen soft keyboards from front-camera or near-field video of the eyes, at the accuracies summarized in Section 6. The privacy-leakage case is equally well established: Alsakar et al. provide the first systematic evidence of leakage from handheld gaze, collecting the SmartEyePhone dataset from 35 participants via the front camera and finding that roughly 65.5% of private attributes — gender, age, geographic origin — are inferable, with differential-privacy mechanisms reducing leakage by only about 10–28% at a utility cost [10]. PrivateGaze further studies privacy preservation specifically for black-box mobile gaze services [23].

The important nuance for mobile is that the gaze-coordinate channel is the weak link, not the leakage. WebGazer-style ridge regression degrades under the head and device motion typical of handheld use [25], so content-dependent inference that depends on precise pointing is less reliable on a phone than on a laptop. But this does not make the phone safer. As the project's own analysis notes, on mobile the **camera-permission grant itself becomes the dominant leakage vector**: the content-independent channel (identity, demographics, state) survives even when pointing accuracy is poor, because it depends on movement dynamics rather than on resolving a 1-cm keypad cell. Mobile camera permissions are also frequently granted for unrelated reasons (video calls, QR scanning, social apps), widening the opportunity.

### 5.3 Tablet — the least-studied surface

Tablets sit between the two: a front-facing camera and touchscreen keyboard like a phone, but a larger screen and often a more stationary, propped-up usage posture closer to a laptop. The consequences follow directly. The content-dependent touchscreen-keyboard threat established for phones (EyeTell-style PIN/keystroke inference [27]) applies to tablets without modification, and the larger display should, if anything, make the gaze-coordinate channel somewhat more tractable than on a phone when the device is propped on a stand. The content-independent demographic and biometric threats [10], [20] apply to any front-camera device and are not display-size dependent. The honest qualification is that there is little tablet-specific empirical work; the assessment for tablets is therefore an interpolation between the well-evidenced smartphone results [8], [10], [27] and the desktop in-browser tooling [25], and a tablet would be a reasonable second device to include in any demonstrator precisely because it is under-measured.

## 6. Evidence Summary

The table consolidates the quantitative findings cited above. Two cautions apply when reading it. First, the biometric equal-error rate is a research-grade upper bound obtained with a high-quality eye tracker, not a webcam; it is included to establish that eye movements are intrinsically distinctive enough to identify a person, while the commodity-webcam realization of that channel is substantially degraded but non-zero. Second, the keystroke-inference accuracies were obtained under controlled capture; they indicate feasibility and order of magnitude rather than guaranteed performance in the wild.

| Attack / empirical finding | Device & channel | Reported result | Source |
|---|---|---|---|
| EyeTell — PIN/keystroke inference from a video of the eyes | Touchscreen; commodity camera video of the face | 4-digit PIN: top-1 ≈39%, top-5 ≈65%, top-50 ≈90%; 6-digit PIN: top-5 ≈70% | [27] |
| GazeRevealer — password inference from the front camera | Smartphone front-facing camera | Single digit ≈77.9%; 6-digit password ≈84.4% (ideal conditions) | [8] |
| Privacy leakage from handheld gaze (SmartEyePhone study, N=35) | Smartphone front camera | ≈65.5% of private attributes (gender, age, geographic origin) inferable; differential privacy cuts leakage ≈10–28% | [10] |
| Eye-movement biometrics (Eye Know You Too) | Research-grade eye tracker, reading task (upper bound, not webcam) | Equal error rate as low as ≈0.6% — demonstrates intrinsic individual distinctiveness of gaze | [20] |
| Mind-wandering & comprehension-error detection | Browser-grade webcam | Above-chance detection of inattention and reading-comprehension failures | [22] |
| WebGazer accuracy drift (ridge regression, no head pose) | Laptop webcam, in-browser | Point-of-gaze error rises from ≈5 cm to ≈10 cm over a 20-minute session | [7], [25] |
| WebEyeTrack (head-pose-aware, on-device) | Browser; laptop and phone | ≈2.32 cm error (GazeCapture); roughly 2× more accurate than WebGazer; real-time on an iPhone | [25] |

## 7. Enabling Conditions

Three conditions make drive-by gaze leakage practical, and each is worth stating explicitly because each is also a potential intervention point (D6).

- **The camera-consent gap.** Browser camera permission is coarse and binary: a user who grants the camera for a legitimate purpose grants the raw video stream, with no separate, gaze-specific consent and no indication that eye-movement analysis is occurring. Users' privacy concerns are also sensitive to device type and stated use case [28], suggesting consent framing materially shapes exposure.
- **Covert calibration.** WebGazer-class trackers self-calibrate by correlating ordinary cursor clicks with gaze, so a page can build a usable gaze model through normal interaction without ever presenting a calibration step [4]. The project's code review confirmed this covert-calibration path (mouse-event listeners feeding the regression) is present and functional in GazePry's fork.
- **Third-party script embedding.** Because the tracker is a few lines of client-side JavaScript, it can be embedded as a third-party script inside a first-party page the user already trusts, inheriting that page's camera permission. This is the same structural problem that has long enabled browsing-history and interaction side channels [5], now applied to a physically grounded signal. The broader trend of feeding gaze into AI/LLM pipelines [9], [11] raises the stakes, since leaked gaze becomes an input to downstream inference rather than a standalone trace.

## 8. What Tightens and What Loosens the Threat Model

A credible assessment should be explicit about its limits, several of which constrain the adversary in useful ways.

**Cross-tab inference is not feasible.** The same-origin policy and browser site isolation prevent a script in one tab or origin from reading the gaze stream associated with another. The adversary sees gaze only on pages where it is running. This rules out the most alarming scenario — a background page silently reading what the user looks at on their bank's site — and means the realistic cross-site risk is re-identification through behavioral biometrics [20], [29] rather than content peeking. This is a tightening of the threat model, and it should be presented as such.

**Python-based references are upper bounds, not the threat.** High-accuracy gaze and biometric models (for example, research-grade pipelines and the biometric results in [20]) define what is achievable with good hardware and offline compute. They are not consistent with the drive-by, commodity, in-browser model that is the project's contribution, and conflating the two would overstate the in-browser attacker. They belong in the report as ceilings against which the realistic webcam channel is measured.

**Identity survives de-facing.** Conversely, one assumption that loosens the threat model: stripping facial identity from the video does not remove the eye-movement biometric, which is carried by movement dynamics rather than appearance [20], [29]. A defense or consent notice premised on "we do not store your face" therefore does not, on its own, prevent re-identification.

## 9. Conclusion and Recommended Next Steps

There is clear, citable information leakage from webcam-based eye tracking on all three device classes. On laptops, the favorable head-pose and large-screen conditions make the content-dependent channel (PIN/keypad and reading/search inference) most tractable, yet this commodity in-browser desktop case is the least characterized in the literature and is the project's strongest contribution angle. On smartphones, concrete keystroke-inference attacks and a well-developed handheld privacy-leakage literature already exist; the key reframing is that the camera-permission grant itself is the dominant risk, because content-independent leakage (identity, demographics, cognitive state) survives the degraded pointing accuracy of handheld use. Tablets inherit the smartphone touchscreen threat with a larger display and are under-measured, making them a sensible second device for evaluation.

For the strongest combined argument, the report and any demonstrator should pair one vector from each regime — for example, a content-dependent PIN-keypad inference demo together with a content-independent demonstration of biometric re-identification or cognitive-state leakage — since the two regimes together show that the leakage is robust both when the attacker controls the page and when it does not. A minimal, consented lab demonstrator on a self-hosted attacker-controlled page (given the broken 2016 SERP selectors) plus a threat-model figure built on the D1–D6 mapping above would substantiate the assessment empirically and is the recommended immediate next step.

*Note on sources:* this assessment draws on the project's working bibliography, reproduced below with original numbering preserved for consistency with the project's BibTeX and related-work table. Where an entry is an arXiv preprint, the prose treats its quantitative claims as indicative; the central claims of this report rest on peer-reviewed venues (IEEE S&P, IEEE TMC, ACM CCS, USENIX Security, CHI, ETRA, ACM TOPS, and IEEE TVCG).

## References

[1] S. D'Mello, A. Olney, C. Williams, and P. Hays, "Gaze tutor: A gaze-reactive intelligent tutoring system," *International Journal of Human-Computer Studies*, vol. 70, no. 5, pp. 377–398, May 2012, doi: 10.1016/j.ijhcs.2012.01.004.

[2] S. D'mello and A. Graesser, "AutoTutor and affective autotutor: Learning by talking with cognitively and emotionally intelligent computers that talk back," *ACM Trans. Interact. Intell. Syst.*, vol. 2, no. 4, pp. 1–39, Dec. 2012, doi: 10.1145/2395123.2395128.

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

[16] T. T. Pham, H. Nguyen, and N. Le, "GazeQwen: Lightweight Gaze-Conditioned LLM Modulation for Streaming Video Understanding," arXiv:2603.25841, Mar. 2026, doi: 10.48550/arXiv.2603.25841.

[17] S. I. Mustafa Shah Bukhari, M. Sajid, B. Ji, and B. David-John, "Rethinking Privacy Indicators in Extended Reality: Multimodal Design for Situationally Impaired Bystanders," in *2025 IEEE Int. Symp. Mixed and Augmented Reality Adjunct (ISMAR-Adjunct)*, Oct. 2025, pp. 265–272, doi: 10.1109/ISMAR-Adjunct68609.2025.00059.

[18] A. M. Mathew, H. Hermassi, T. Khalid, and A. A. Khan, "GazeVLM: A Vision-Language Model for Multi-Task Gaze Understanding," arXiv:2511.06348, Mar. 2026, doi: 10.48550/arXiv.2511.06348.

[19] Y. Long, C. Yan, S. Xiao, S. Prasad, W. Xu, and K. Fu, "Private Eye: On the Limits of Textual Screen Peeking via Eyeglass Reflections in Video Conferencing," in *2023 IEEE Symp. Security and Privacy (SP)*, IEEE, May 2023, pp. 3432–3449, doi: 10.1109/SP46215.2023.10179423.

[20] D. Lohr and O. V. Komogortsev, "Eye Know You Too: A DenseNet Architecture for End-to-end Eye Movement Biometrics," arXiv:2201.02110, Mar. 2022, doi: 10.48550/arXiv.2201.02110. (Published version: *IEEE Trans. Inf. Forensics Secur.*, vol. 17, pp. 3151–3164, 2022.)

[21] J. L. Kröger, O. H.-M. Lutz, and F. Müller, "What Does Your Gaze Reveal About You? On the Privacy Implications of Eye Tracking," in *Privacy and Identity Management. Data for Better Living: AI and Privacy*, Springer, 2020, pp. 226–241, doi: 10.1007/978-3-030-42504-3_15.

[22] S. Hutt, A. Wong, A. Papoutsaki, R. S. Baker, J. I. Gold, and C. Mills, "Webcam-based eye tracking to detect mind wandering and comprehension errors," *Behav. Res.*, vol. 56, no. 1, pp. 1–17, Jan. 2024, doi: 10.3758/s13428-022-02040-x.

[23] L. Du, J. Jia, X. Zhang, and G. Lan, "PrivateGaze: Preserving User Privacy in Black-box Mobile Gaze Tracking Services," arXiv:2408.00950, Aug. 2024, doi: 10.48550/arXiv.2408.00950.

[24] B. David-John, D. Hosfelt, K. Butler, and E. Jain, "A privacy-preserving approach to streaming eye-tracking data," *IEEE Trans. Visual. Comput. Graphics*, vol. 27, no. 5, pp. 2555–2565, May 2021, doi: 10.1109/TVCG.2021.3067787.

[25] E. Davalos et al., "WebEyeTrack: Scalable Eye-Tracking for the Browser via On-Device Few-Shot Personalization," arXiv:2508.19544, Aug. 2025, doi: 10.48550/arXiv.2508.19544.

[26] V. Danry, J. Hernandez, A. Wilson, P. Maes, and J. Amores, "From Gaze to Guidance: Interpreting and Adapting to Users' Cognitive Needs with Multimodal Gaze-Aware AI Assistants," arXiv:2604.08062, Apr. 2026, doi: 10.48550/arXiv.2604.08062.

[27] Y. Chen, T. Li, R. Zhang, Y. Zhang, and T. Hedgpeth, "EyeTell: Video-Assisted Touchscreen Keystroke Inference from Eye Movements," in *2018 IEEE Symp. Security and Privacy (SP)*, IEEE, May 2018, pp. 144–160, doi: 10.1109/SP.2018.00010.

[28] E. Bozkir, B. Bühler, X. Wu, E. Kasneci, L. Bauer, and L. F. Cranor, "The impact of device type, data practices, and use case scenarios on privacy concerns about eye-tracked augmented reality in the United States and Germany," *J. Cyber Secur.*, vol. 11, no. 1, p. tyaf036, Jan. 2025, doi: 10.1093/cybsec/tyaf036.

[29] H. Aziz, M. H. Raju, and O. V. Komogortsev, "Enhancing Eye Movement Biometrics for User Authentication via Continuous Gaze Offset Score Fusion," arXiv:2605.06810, May 2026, doi: 10.48550/arXiv.2605.06810.
