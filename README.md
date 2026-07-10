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
  public/              the capture harness (one shared "tracking tag", 5 tasks)
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
    index.html           consent + identity + TRACKER PICKER + calibration + hub
    tasks/*.html         reading · serp · images · video · form  (5 "sites")
    reid.html            live re-ID + the "unclearable" (wipe-state) demo
  scripts/
    vendor-trackers.sh   fetch WebEyeTrack + EyeGestures into public/ (idempotent)
  analysis/            the authoritative offline evaluation (Python)
    features.py          content-independent features (mirrors reid-core.js)
    reid.py              cross-task/cross-session re-ID: rank-1, rank-5, EER, CMC
    simulate.py          synthetic gaze generator (pipeline verification)
    test_analysis.py     stdlib unittest: features, tracker split, JS/Py parity
    requirements.txt
  test/                the regression suite (node:test, zero deps)
    reid-core.test.js    feature contract + nearest-neighbour matcher
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
