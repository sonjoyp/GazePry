# GazePry

**Cross-site gaze re-identification as an unclearable web tracking vector.**

This repository is the research project and its experiment harness. The thesis:
eye-movement dynamics captured by a commodity in-browser webcam tracker form a
**stateless, person-bound** re-identification signal that clearing cookies /
cache / incognito does not remove, and that survives stripping the face from the
video (it is carried by *movement dynamics*, not appearance).

**Research documents (use these for the paper):**
- [`GazePry_Direction1_ReID_Study_Protocol.md`](GazePry_Direction1_ReID_Study_Protocol.md)
  — the living study protocol: thesis, threat model, research questions,
  apparatus, stimuli, features/models, conditions matrix, metrics, analysis plan,
  related work, and full bibliography. **Kept current with the direction, plan,
  and methodology** as the work evolves.
- [`GazePry_Information_Leakage_Report.md`](GazePry_Information_Leakage_Report.md)
  — the companion threat-model assessment and shared bibliography.

Everything else at the root (below) is the runnable harness that implements the
protocol.

The webcam tracker is **pluggable**: the capture harness is tracker-agnostic and
drives one of several adapters chosen per session, so the same participant can be
recorded on multiple webcam trackers and compared (protocol RQ3). Shipped
adapters: **WebGazer v3.5.3** (working, vendored — the deployed reality and the
GazePry lineage, not the deprecated 2016 SearchGazer fork, which now lives in
[`legacy-searchgazer/`](legacy-searchgazer/)),
**GazeCloud/GazeRecorder** (working via its hosted script — high-accuracy but
closed-source and **cloud**: frames leave the machine), **WebEyeTrack**
(head-pose-aware CNN + few-shot, MIT; vendored, on-device), and **EyeGestures**
(open-source Rust/WASM, vendored, on-device). The two vendored libraries are
fetched by [`scripts/vendor-trackers.sh`](scripts/vendor-trackers.sh) and are
already present under `public/lib/`. See
[`public/trackers/README-adapter.md`](public/trackers/README-adapter.md).

---

## What's here

```
GazePry/                          (repo root — the experiment lives here)
  GazePry_Direction1_ReID_Study_Protocol.md   the living study protocol (paper)
  GazePry_Information_Leakage_Report.md        companion threat-model report
  legacy-searchgazer/  archived 2016/2017 SearchGazer demo (deprecated, unused)
  server.js            zero-dependency Node server: serves the harness, ingests
                       sessions, exposes a LIVE nearest-neighbour re-ID endpoint
  reid-core.js         gaze feature extraction + matching (JS, for the live demo)
  public/              the capture harness (one shared "tracking tag", 6 tasks)
    gazepry-tracker.js   tracker-AGNOSTIC orchestrator: identity, calibration,
                         capture, watchdog, submit — drives the active adapter
    trackers/            one self-registering adapter per webcam tracker
      webgazer.js          WebGazer v3.5.3 (working, vendored)
      gazecloud.js         GazeCloud/GazeRecorder (working, hosted script; CLOUD)
      webeyetrack.js       WebEyeTrack (working, vendored; on-device)
      eyegestures.js       EyeGestures (working, vendored; on-device)
      README-adapter.md    the adapter contract + how to add a tracker
    lib/                 vendored tracker libraries (lazy-loaded per selection)
      webgazer.js          WebGazer build
      webeyetrack/         WebEyeTrack UMD bundle (+ MIT LICENSE)
      eyegestures/         EyeGestures WASM engine + shim + deps
    web/                 WebEyeTrack BlazeGaze TF.js model (served at /web/)
    task-runner.js       shared boot code for the task pages
    probe-protocol.js    D7: stimulus sets + counterbalanced trial builder
                         (runs in the browser AND in Node, so tests/simulator
                         use the same code the participant sees)
    index.html           consent + identity + TRACKER PICKER + calibration + hub
    tasks/*.html         reading · serp · images · video · form  (5 "sites")
                         + probe (D7 recognition array, trial-structured)
    reid.html            live re-ID + the "unclearable" (wipe-state) demo
  scripts/
    vendor-trackers.sh   fetch WebEyeTrack + EyeGestures into public/ (idempotent)
  analysis/            the authoritative offline evaluation (Python)
    features.py          content-independent features (mirrors reid-core.js)
                         + I-DT dispersion fixation detection (D7)
    reid.py              cross-task/cross-session re-ID: rank-1, rank-5, EER, CMC
    simulate.py          synthetic gaze generator (pipeline verification)
    probe_protocol.py    D7: Python port of probe-protocol.js (parity-tested)
    aoi_features.py      D7: soft AOI assignment + per-trial features
    recognition.py       D7: classifier, LOPO CV, AUC-vs-k, RQ0 gate
    simulate_probe.py    D7: synthetic probe sessions (incl. --effect 0 null)
    test_analysis.py     stdlib unittest: features, tracker split, JS/Py parity
    requirements.txt
  scripts/
    run-python.js        resolves python3/python/py so `npm test` works anywhere
  test/                the regression suite (node:test, zero deps)
    reid-core.test.js    feature contract + nearest-neighbour matcher
    idt.test.js          D7: dispersion-threshold fixation detection
    probe-protocol.test.js  D7: counterbalancing, trial structure, geometry
    registry.test.js     adapter registry, contract, identity/tracker resolution
    server.test.js       ingest/status/sessions/identify over a live server
    features-cli.js      helper: JS feature vector for the Python parity test
  data/                collected session logs (real participant data is tracked here)
  data_sim/            synthetic sessions for pipeline verification (regenerable)
```

**Two regimes on purpose.** Same-origin policy blocks a script from reading gaze
on *another* site, so this harness does **not** attempt content peeking. It
targets re-identification, which is content-independent and therefore *not*
blocked by SOP: two sites embedding the same tag link the same visitor by gaze.

---

## Quick start

### 1. Serve the harness and collect sessions

```bash
node server.js               # from the repo root -> http://localhost:8080 (npm start works too)
```

Open **http://localhost:8080** (use `localhost` — `getUserMedia` needs a secure
context; `localhost` counts, a bare LAN IP would need HTTPS).

1. Enter a participant ID (e.g. `P01`), pick a session (`S1`), pick an
   **eye-tracker**, consent, and run **calibration** (a click grid for
   click-trained trackers; self-calibrating trackers run their own).
2. Complete each of the five tasks. Different content per page stands in for a
   different "site"; **cross-task** matching is the real tracking test.
3. For a **return visit**, reload the hub, switch to `S2`, and re-calibrate
   (this clears the prior model — an honest cross-session test). Ideally do `S2`
   on a different day.
4. To compare trackers on the **same** participant (RQ3), repeat the tasks with
   the same participant/session but a different tracker selected.

Each finished task POSTs a session to `data/` as
`P01_S1_reading_webgazer_<ts>.json` — participant, session, task, **tracker
family**, timestamp (raw gaze stream `{t, x, y}`, `x=null` for a blink/lost-face
gap). If the server is down the tracker downloads the file instead — drop it into
`data/`.

### 2. Live re-identification demo

With a few participants enrolled, open **`/reid.html`**:

- **Capture 20 s probe & identify** — captures whoever is at the screen now and
  asks the server to rank enrolled participants by gaze-feature distance.
- **Wipe all browser state** — clears cookies + localStorage + sessionStorage +
  the active tracker's local model, then identify again. The match still lands,
  because *who you are* was never stored in the browser. That is the
  "unclearable" point. (The live re-ID page matches only against gallery sessions
  from the **same** tracker.)

### 3. Offline evaluation (the numbers for the paper)

```bash
cd analysis
pip install -r requirements.txt        # numpy (+ matplotlib for --plot)
python reid.py --data ../data --plot cmc.png
```

`reid.py` reports rank-1, rank-5, and EER under four protocols, **per tracker**
(it never matches across trackers), so the `cross_task_cross_session` EER of one
tracker vs. another is the RQ3 ceiling-vs-commodity gap. Restrict to one with
`--tracker webgazer`. The headline protocol is `cross_task_cross_session`
(different content **and** different visit).

---

## Tests — run them after every change

There is a regression suite so a small change can't quietly break a working
feature. **Run `npm test` after each change; keep it green before moving on.**

```bash
npm test          # from the repo root: JS suite (node:test) + Python suite (unittest)
npm run test:js   # just the JavaScript tests
npm run test:py   # just the Python tests
```

Zero test dependencies: JavaScript uses the built-in `node:test` runner, Python
uses stdlib `unittest`. What's covered:

- **`reid-core.js`** — the 16-feature contract, fixation/saccade segmentation,
  screen-scale invariance, gap counting, `standardize` (incl. zero-variance
  guard), and `identify` ranking + `exclude` + empty-gallery behaviour.
- **Tracker registry / adapters** — all four adapters register; each meets the
  contract; capability flags are correct (GazeCloud is `cloud` + self-calibrating;
  WebEyeTrack + EyeGestures are `local` and vendored); the vendored libraries are
  present on disk; identity + tracker resolution (query → localStorage → default)
  and `wipeState`.
- **`server.js`** — ingest (incl. filename carries the tracker family, 400 on bad
  input, legacy-record family inference), status/sessions scoped by tracker,
  `identify` never mixing trackers, static serving + path-traversal guard.
- **Analysis** — features, `tracker_family`, protocol eligibility (never matches
  across trackers), `evaluate`, `simulate`, per-tracker reporting, and a
  **JS↔Python parity** test proving `reid-core.js` and `features.py` agree.
- **Direction D7** — the counterbalancing invariants (every item familiar for
  half the cohort; slot position carries no familiarity information; exactly one
  probe per trial), I-DT segmentation in both languages plus a **second JS↔Python
  parity** test, a **third parity** test proving the browser trial protocol and
  its Python port build the *same design*, AOI soft/hard assignment, and an
  end-to-end check that the pipeline recovers a planted effect **and reports
  chance on a null dataset**. Two regression tests pin the failure modes found
  while building it (zero-fixation collapse at a lab-grade threshold; the
  leave-one-out bias in the saliency control).

When you change a feature, add or update a test in the same commit so the
guarantee keeps up with the code. If you change the feature set, the parity test
(`test/features-cli.js` + `analysis/test_analysis.py::TestParity`) forces
`reid-core.js` and `features.py` to stay in sync.

---

## Webcam trackers (the pluggable arms)

Pick the tracker on the hub; it drives calibration, capture, and the live re-ID
demo for that session. Adapters live in `public/trackers/`.

| Tracker | Status | Privacy | Calibration | Role |
|---|---|---|---|---|
| **WebGazer 3.5.3** (`webgazer`) | working, vendored | local (video stays in browser) | 9-point click grid | the deployed reality; GazePry lineage |
| **GazeCloud / GazeRecorder** (`gazecloud`) | working (hosted script, needs internet) | **cloud** — frames sent to GazeRecorder | built-in (self) | high-accuracy commodity contrast |
| **WebEyeTrack** (`webeyetrack`) | working, vendored | local (video on-device; model/wasm from CDN) | few-shot (click grid) | head-pose-aware near-future ceiling (protocol arm 3) |
| **EyeGestures** (`eyegestures`) | working, vendored | local (video on-device; MediaPipe from CDN) | self (built-in) | actively-maintained open-source arm |

- **On-device vs. cloud.** WebGazer, WebEyeTrack, and EyeGestures run gaze
  inference **in the browser** — no camera data leaves the machine. (WebEyeTrack
  and EyeGestures *download* model/WASM assets from CDNs at load; that is
  download-only.) GazeCloud is different: it uploads webcam frames to
  GazeRecorder's servers. For a paper about webcam gaze as a *tracking vector*,
  "the most accurate drop-in option also exfiltrates your face" is itself worth
  stating — keep GazeCloud separate from the on-device arms.
- **Vendored assets.** WebEyeTrack and EyeGestures are fetched by
  [`scripts/vendor-trackers.sh`](scripts/vendor-trackers.sh) into `public/lib/`
  (and the BlazeGaze model into `public/web/`) and are already present. Re-run the
  script to refresh them. WebEyeTrack's model is served at the origin root
  `/web/` because its loader hardcodes `${origin}/web/model.json`.
- **To add a different tracker:** copy the closest adapter, implement the
  contract (`start` + `onGaze` emitting `{x,y}` viewport pixels is the minimum),
  add one `<script>` line to each page's tracker block, and it appears in the
  picker automatically.

All adapters emit the **same** `{t, x, y}` stream, so one feature extractor
(`reid-core.js` / `analysis/features.py`) and one analysis serve every tracker.

---

## Verify without a webcam

The analysis pipeline is verifiable end-to-end on synthetic subjects that have
stable oculomotor traits across tasks/sessions:

```bash
cd analysis
python simulate.py --out ../data_sim --subjects 12 --sessions 2
python reid.py --data ../data_sim --plot ../data_sim/cmc.png
```

To exercise the **multi-tracker** (RQ3) analysis without a webcam, tag two
synthetic runs with different tracker labels into one directory — `reid.py` then
prints a separate table per tracker and never matches across them:

```bash
python simulate.py --out ../data_sim_mt --subjects 12 --sessions 2 --tracker webgazer --seed 7
python simulate.py --out ../data_sim_mt --subjects 12 --sessions 2 --tracker gazecloud --seed 9
python reid.py --data ../data_sim_mt
```

Expected (12 synthetic subjects, chance rank-1 = 0.083):

| protocol | rank-1 | rank-5 | EER |
|---|---|---|---|
| all | 0.31 | 0.95 | 0.22 |
| same_task_cross_session | 0.55 | 0.97 | 0.16 |
| cross_task | 0.18 | 0.84 | 0.27 |
| **cross_task_cross_session** (headline) | **0.28** | 0.86 | 0.25 |

rank-1 sits far above chance and EER well below 0.5 under every protocol,
with same-task easiest and cross-task hardest — the ordering the study predicts.
These are a **code sanity check on synthetic data, not a claim about real eyes.**
Real numbers come from the browser harness.

---

## Direction D7 — recognition & concealed-knowledge probe

A second, independent experiment lives in the same harness. Where D4 asks *who
is this visitor*, **D7 asks what they have seen before**: a page renders a
coarse tile array and infers, from dwell asymmetry and fixation timing alone,
which tile the visitor recognises. See
[`GazePry_D7_Recognition_Knowledge_Direction.md`](GazePry_D7_Recognition_Knowledge_Direction.md).

### Collect

Open the hub and pick **Recognition probe**. The setup card sets the design
cell (experiment E1/E2/E3, array size, cover task, awareness condition, delay,
trial count); the participant then just does the task.

```
fixation cross (500 ms) → tile array (4000 ms) → cover-task prompt
```

Sessions are written as `gazepry.probe.v1` records carrying a `trials[]` array
(per-trial AOI rectangles, onset/offset, familiarity role) alongside the raw
`{t,x,y}` stream. They are ingested by the same server but are **excluded from
the D4 re-ID gallery**, because a whole-session dynamics vector over
adversary-driven 4 s trials describes the trial structure, not the person.

### Stimuli

The task shows **real image files** from `public/stimuli/`, described by a
manifest that both the browser and the Python analysis read, so the item table
cannot drift between them.

```bash
npm run d7:stimuli          # design the packs; generate E1 and any placeholders
npm run d7:stimuli:fetch    # install the real E2 assets from Wikimedia Commons
npm run d7:stimuli:check    # validate: files present, big enough, ids unique
npm run d7:stimuli:verify   # offline: assets still match their lock hashes
```

**E1** ships 24 Julia-set fractals. It is abstract on purpose: E1's validity
depends on the participant having **no prior exposure**, so photographs of real
things would smuggle in uncontrolled familiarity that counterbalancing cannot
remove. The generator histogram-equalises escape time and colours the interior
by an orbit trap (the naive mapping gives a dark image with a thin bright rim
and little to recognise), and resamples candidates until **every pair differs by
at least 22 mean absolute RGB levels** — a "novel" tile that resembles a studied
one contaminates the contrast irreparably.

**E2** measures familiarity the participant already had, so it uses the real
thing: 24 items in three classes of eight — **public figures**, **retail-bank
wordmarks**, and **widely photographed places** — each class spanning universal
to niche recognition. Arrays are drawn *within* a class, never across, so a trial
is four faces or four bank marks; a mixed array would let the probe be picked out
by category rather than by familiarity.

`scripts/fetch_stimuli.py` installs them from Wikimedia Commons and enforces
three things the honour system would not: only **freely-licensed** files (a
machine-checked allow-list; anything else is refused, not downloaded), a **lock
file** pinning the resolved file and the SHA-256 of every byte written so two
cohorts provably saw the same stimuli, and **generated attribution** that cannot
drift from what is on disk. The images themselves are gitignored; the manifest,
sources, lock, and attribution are committed, so a clean checkout reproduces the
pack with two commands.

**E3** now ships 8 real everyday documents (a vaccination card, a census form, a
jury summons, a payslip…) and is collectable once fetched, but its construct is
kept separate on purpose: its cards probe exposure to a *topic* rather than to a
specific image, a weaker construct than E1/E2 rather than just a weaker
manipulation, so E3 is reported separately with an episodic-versus-semantic
caveat and never used to support the mechanism claim. Free Commons coverage also
makes finance and legal thin (one item each), so they are illustrative, not a
category comparison. See [`public/stimuli/README.md`](public/stimuli/README.md).

The task page **disables Begin** while a set contains placeholders rather than
warning, since a cohort collected against stand-ins cannot be salvaged.

Four things the page enforces rather than assumes:

- **It refuses to run E2/E3 on placeholder stimuli**, and flags any image that
  fails to load on the completion card so a blank-tile trial is never scored as
  real data.

- **It refuses to run in a small window.** Tiles must be ≥400×300 px with ≥250 px
  gaps — the geometry Van der Cruyssen et al. 2024 actually validated on
  WebGazer. A smaller layout is outside the published envelope, so the Begin
  button disables instead of quietly collecting unusable data.
- **Counterbalancing is derived from the participant ID**, so every item is the
  familiar one for half the cohort. Without this the classifier could separate
  the classes on which *pictures* they are; with it, item salience and slot
  position are orthogonal to familiarity by construction.
- **Trial marks are mapped onto the sample clock**, anchored on the first gaze
  sample. Adapters emit their own clock base, so a `performance.now()` onset
  would not be on the same axis as the samples. If the anchor never lands the
  session records `clockAnchored: false` and the analysis drops it.

### Evaluate

```bash
npm run d7:verify        # simulate effect + null datasets, evaluate both
```

or directly:

```bash
cd analysis
python simulate_probe.py --out ../data_probe_sim  --subjects 20 --trials 40 --effect 0.8
python simulate_probe.py --out ../data_probe_null --subjects 20 --trials 40 --effect 0
python recognition.py --data ../data_probe_sim --experiment E1 --plot k.png
```

`recognition.py` reports per-AOI AUC with a CI bootstrapped **over
participants**, TPR@FPR=0.10, probe-identification accuracy, the item-level
**AUC-vs-k curve** (*"how many tiles before a page knows which sites you use"*),
and per-feature d′ split by feature family. Cross-validation is
leave-one-participant-out; it never splits within a person.

**The RQ0 gate runs on every invocation** and must clear before any number
counts: a shuffled-label null (familiarity permuted within participant) and a
saliency-only baseline (item identity + slot position, familiarity withheld)
both have to sit at ≈0.500. On the synthetic effect data they land at 0.510 and
0.488 while the real signal reaches 0.918; on the null dataset the headline
collapses to 0.525 with a CI including chance and the gate correctly refuses to
certify it.

| dataset | per-AOI AUC | 95% CI | probe id (chance .25) | RQ0 |
|---|---|---|---|---|
| `--effect 0.8` | 0.918 | [0.901, 0.933] | 0.751 | PASS |
| `--effect 0` (null) | 0.525 | [0.498, 0.544] | 0.261 | correctly refuses |

**These are a code sanity check on generated data, not a claim about real eyes.**
The generator writes the effect in by construction. Real numbers require the E1
pilot.

### Two findings from building it

- **A lab-grade I-DT threshold finds zero fixations in webcam-noise data.** At a
  realistic ~1.4° error the raw point cloud of a genuine fixation already exceeds
  a 0.045-diagonal dispersion threshold, so every fixation-derived feature
  silently becomes a constant reporting AUC 0.500 — indistinguishable from "no
  effect". The detector therefore smooths first and uses a tile-scale threshold,
  `recognition.py` prints fixations-per-trial and warns when it collapses, and
  the failure is pinned by a regression test in both languages.
- **Leave-one-participant-out biases the saliency control.** Holding a
  participant out leaves their own counterbalance group short by one, tilting
  every item's training marginal *away* from their labels with a perfectly
  consistent sign — which showed up as an alarming AUC of 0.10 from a design
  that was actually fine. The control now balances group counts within each
  training fold.

## Gazepoint ground-truth rig (RQ3: ceiling vs commodity)

To measure the gap between research hardware and the webcam channel on the *same*
subjects, record the webcam **while** Gazepoint tracks, so every webcam frame has
an IR ground-truth label:

1. Run the Gazepoint (GP3/GP3 HD) with its own capture, logging gaze at 60/150 Hz
   with system timestamps.
2. Run this harness in the browser at the same time; the WebGazer stream already
   carries `t` (ms). Align the two clocks with a shared event (e.g. a keypress or
   an on-screen flash at task start).
3. Down-sample Gazepoint to the webcam rate (~30 Hz) for the fair-comparison arm.
   Note that 30 Hz limits saccade-velocity features — report which features
   survive the commodity rate.
4. Feed each channel's stream through the same `features.py` and compare re-ID
   metrics (`tracker` field distinguishes them). This yields the ceiling
   (Gazepoint) vs realistic (WebGazer) contribution directly.

---

## Cross-origin / third-party-tag demonstration

The tracker is one script embedded in every task page — already the "one provider
across many pages" model. To make the cross-*origin* linkage literal, run the
collector separately and point the tag at it from a page served on a different
origin:

```bash
node server.js --port 8080                     # site A (task pages)
node server.js --port 9090 --data ./data       # the tracking collector
```

In a task page set `GazePry.config.server = "http://localhost:9090"` before
capture. The collector (CORS-enabled) receives sessions from any origin and
re-identifies across them — no cookie, no shared storage.

---

## Mapping to the study protocol

| Protocol RQ | Where it lives |
|---|---|
| RQ1 same-task cross-session baseline | `reid.py` protocol `same_task_cross_session` |
| RQ2 cross-task ("tracking") generalisation | `reid.py` protocols `cross_task*` |
| RQ3 ceiling vs commodity | Gazepoint rig above + the pluggable webcam trackers; `reid.py` reports per-tracker and never matches across them |
| RQ4 unclearability | `reid.html` wipe-state demo; cross-origin collector |
| RQ5 defense (future) | perturb the stream in `gazepry-tracker.js` before submit (applies to every tracker) |

## Caveats

- **Webcam accuracy is the honest risk.** The on-device webcam trackers drift
  over a session (WebGazer most, WebEyeTrack least); the I-VT velocity threshold
  (`VEL_THRESHOLD` in `reid-core.js` / `features.py`) is coarse at ~30 Hz and
  will need tuning against real data. Treat webcam re-ID numbers as a **lower
  bound** on the threat.
- **GazeCloud sends video off-device.** It is closed-source and cloud-based;
  only use it with participant consent covering third-party processing, and keep
  it clearly separated from the on-device arms in any comparison.
- The hand-crafted feature set is route (a) from the protocol. A deep model
  (Eye Know You Too-style) is the ceiling and a natural extension.
- `features.py` and `reid-core.js` must stay in sync if you change features.
- IRB: this project is IRB-exempt. Note that `data/` currently holds **real
  participant session logs tracked in this repo** — these are gaze coordinate
  streams only (no raw video), but treat them as sensitive and confirm consent
  covers sharing before publishing the repo.

---

## Credit & license

Gaze estimation engines are third-party: **WebGazer** (Brown HCI Group),
**WebEyeTrack** (RedForestAI, MIT), **EyeGestures** (NativeSensors), and the
optional cloud **GazeCloud/GazeRecorder**. Vendored library licenses live beside
their code under `public/lib/`. The archived SearchGazer demo (Papoutsaki,
Laskey, Huang, CHIIR 2017) is in `legacy-searchgazer/`. This project is licensed
under GPLv3 (see [`LICENSE.md`](LICENSE.md) / [`gplv3.md`](gplv3.md)).
