---
type: note
tags: [note, d7, recognition, instrumentation, methodology, gotchas, stimuli]
date: 2026-07-22
sources: [d7-recognition-knowledge-direction]
reviewed: false
updated: 2026-07-22
---

# 2026-07-22 — Building the D7 probe: four things the design document did not anticipate

Follow-on to [[2026-07-22-d7-recognition-direction]], which decided the
direction. This note records what changed once
[[recognition-knowledge-leakage]] was actually implemented as a running
collection and analysis pipeline. Four of the findings are load-bearing: each
one, left alone, would have produced a number that looked publishable and meant
nothing. **No human data has been collected** — everything below is from
synthetic sessions, unit tests, and deliberate sabotage runs.

The code itself is not documented here (see `README.md`,
`D7_COLLECTION_RUNSHEET.md`, and the repo); only the findings and the reasoning
behind the choices.

## 1. The lab-grade I-DT threshold finds zero fixations on webcam noise

[[thilderkvist-2024-limitations]] establishes that a dispersion-threshold
(I-DT) detector is required at webcam sample rates. It does not follow that the
lab-standard *threshold* transfers.

At the ~67 px positional noise a WebGazer stream carries, a dispersion window of
0.045 screen-diagonals — the usual lab figure — segmented **zero** fixations
across an entire synthetic cohort. The failure was silent in the worst way:
every fixation-derived feature became a constant, and constants score exactly
AUC 0.500, so the pipeline reported "no recognition effect" rather than "the
segmenter did not run".

Resolution, applied identically in `reid-core.js` and `analysis/features.py`:

- a 5-sample centred moving average that never spans a gap in the stream,
- `DISP_THRESHOLD = 0.10` screen-diagonals — roughly **twice** the lab value,
  chosen at tile scale rather than at the scale of within-image features,
- a `fixations per trial` diagnostic printed on every run, with a warning below
  1.0.

The diagnostic matters more than the constant. The right threshold is a
property of the sensor and the geometry, so a different camera or seating
distance can re-open the collapse; the run sheet therefore treats the line as a
gate to read, not decoration. This is a concrete instance of
[[webcam-tracking-validation]]'s general caution: an algorithm that ports does
not mean its parameters port.

## 2. Leave-one-participant-out quietly breaks the saliency control

The RQ0 gate requires a saliency-only baseline — item identity with no gaze —
to sit at chance, since [[recognition-knowledge-leakage]] rests on item-level
counterbalancing making saliency orthogonal to familiarity.

It came out at **AUC 0.101**, which reads as catastrophically broken
counterbalancing. It was not. With four counterbalance groups and LOPO folds,
holding out one participant leaves their own group under-represented by exactly
one relative to the other three. That is enough to invert each item's marginal
familiarity rate in the training fold, and because the under-representation is
always the held-out participant's group, the inversion has a *consistent sign*
across folds. A control that is systematically wrong scores far below chance
rather than at it.

Fixed by group-balancing the training folds: baseline moved 0.101 → **0.488**.

The general lesson for [[reid-protocols]]: a below-chance control is evidence of
structure in the fold construction, not evidence of a broken design. Diagnose
before rebuilding.

## 3. The RQ0 gate was verified to bite, by sabotage

A gate that has never fired is an assumption. Counterbalancing was deliberately
broken (`group_for = lambda p: 0`, i.e. every participant in one group) to check
that the gate refuses the result:

| Run | headline AUC | saliency baseline | RQ0 |
|---|---|---|---|
| Sabotaged counterbalancing | 0.935 | 1.000 | **FAIL** |
| Null data (`--effect 0`) | 0.525 [0.498, 0.544] | 0.488 | **FAIL** |
| Effect data (`--effect 0.8`) | 0.918 [0.901, 0.933] | 0.488 | **PASS** |

The first row is the one worth keeping. Without the saliency control, sabotaged
counterbalancing yields **AUC 0.935** — a headline number better than the honest
one, produced entirely by item identity. That is what the control exists to
catch, and it does.

Two further nulls behave correctly: randomising the questionnaire responses
collapses E2/E3 to chance (so self-report genuinely drives those results), and
`--effect 0` reports chance end to end.

Reproduce with `npm run d7:verify`. All three rows above were re-run on
2026-07-22; the effect and null rows are current output, the sabotage row was
recorded during the session and the sabotage is not committed.

## 4. Near-duplicate stimuli, and a distinctiveness check that could not see them

E1 installs familiarity in the lab, so its stimuli must be **novel** —
photographs of real things would smuggle in uncontrolled prior exposure that no
counterbalancing removes. E1 therefore ships 24 generated Julia-set fractals as
real PNG files (`public/stimuli/`, manifest schema `gazepry.stimuli.v1`, shared
by the JS task page and the Python analysis so the item table cannot drift
between them).

Two problems, in order of severity:

- **Minimum pairwise difference was 1.3 mean absolute levels** — some "novel"
  tiles were near-copies of studied ones, which contaminates the familiarity
  contrast irrecoverably. The generator now rejects candidates until every pair
  differs by ≥ 22; achieved minimum **34.14**, recorded in the manifest as
  `minPairDistance` rather than assumed.
- **The first distinctiveness check compared greyscale thumbnails**, so pairs
  sharing structure and differing only in hue passed it. Switching to colour
  thumbnails was what exposed the real duplicates. Noted in the code comment,
  because the greyscale version looks perfectly reasonable on review.

Also fixed: the smooth escape-time formula can go negative, and the resulting
NaN cast to uint8 as arbitrary pixel values rather than an error — a silent
corruption, now clamped and pinned by a regression test. Image contrast was
separately raised (per-image pixel std 19.3 → 65.7) by histogram-equalising
escape time and orbit-trapping the interior.

**E2 and E3 measure familiarity the participant brought with them**, so they
need real logos, screenshots, and topic cards. They currently ship visible
stand-ins, and the task page **disables Begin** while a set contains
placeholders — a block rather than a warning, because by the time anyone reads a
warning the cohort has already been collected and cannot be salvaged.

## Verification state

- `npm test` — **147 pass, 0 fail** (71 JS + 76 Python), 2026-07-22.
- `npm run d7:verify` — effect PASSes RQ0, null correctly refuses (table above).
- `npm run d7:stimuli:check` — 3 sets, 56 items, all files present.
- JS↔Python parity is asserted by three tests (features, I-DT segmentation,
  trial plan), so the browser and the analysis cannot silently disagree.

## Open items this note does not resolve

- **Data hygiene, still blocking collection.** 44 real gaze sessions from prior
  work remain tracked in git (`.gitignore` was commented out; it is re-enabled,
  but that only governs untracked paths). Untracking is a git-index operation
  left to a human; a history scrub before any public artifact release is a
  separate destructive decision. See `D7_COLLECTION_RUNSHEET.md` §1.1.
- Real E2/E3 assets are not installed, so only E1 can currently be run.
- The four unverified citations from [[2026-07-22-d7-recognition-direction]]
  are still unverified.
- Every number above is synthetic. The E1 pilot (N ≈ 12) asks one question
  only: *does RQ0 clear on real eyes?*

## Related

- [[2026-07-22-d7-recognition-direction]] — the direction decision this
  implements; supersedes nothing in it.
- [[thilderkvist-2024-limitations]] — the I-DT requirement whose *threshold*
  turned out not to transfer (§1).
- [[eye-movement-memory-effect]] — the effect the temporal features target;
  §1's collapse disabled exactly the fixation-duration channel predicted to be
  the countermeasure-resistant one.
- [[reid-confound-controls]] — D4's confound battery, the model for the RQ0
  gate that §3 stress-tested.
