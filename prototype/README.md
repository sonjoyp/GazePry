# GazePry — Direction 1 Prototype

**Cross-site gaze re-identification as an unclearable web tracking vector.**

A working prototype for the thesis in
[`../GazePry_Direction1_ReID_Study_Protocol.md`](../GazePry_Direction1_ReID_Study_Protocol.md):
eye-movement dynamics captured by a commodity in-browser webcam tracker form a
**stateless, person-bound** re-identification signal that clearing cookies /
cache / incognito does not remove, and that survives stripping the face from the
video (it is carried by *movement dynamics*, not appearance).

Built on the **current** [brownhci/WebGazer](https://github.com/brownhci/WebGazer)
(v3.5.3), not the deprecated 2016 SearchGazer fork in the repo root.

---

## What's here

```
prototype/
  server.js            zero-dependency Node server: serves the harness, ingests
                       sessions, exposes a LIVE nearest-neighbour re-ID endpoint
  reid-core.js         gaze feature extraction + matching (JS, for the live demo)
  public/              the capture harness (one shared "tracking tag", 5 tasks)
    lib/webgazer.js      WebGazer v3.5.3 build (the commodity webcam tracker)
    gazepry-tracker.js   the "third-party analytics SDK": calibrate + log + submit
    task-runner.js       shared boot code for the task pages
    index.html           consent + identity + calibration + task hub
    tasks/*.html         reading · serp · images · video · form  (5 "sites")
    reid.html            live re-ID + the "unclearable" (wipe-state) demo
  analysis/            the authoritative offline evaluation (Python)
    features.py          content-independent features (mirrors reid-core.js)
    reid.py              cross-task/cross-session re-ID: rank-1, rank-5, EER, CMC
    simulate.py          synthetic gaze generator (pipeline verification)
    requirements.txt
  data/                collected sessions land here (git-ignored)
```

**Two regimes on purpose.** Same-origin policy blocks a script from reading gaze
on *another* site, so this prototype does **not** attempt content peeking. It
targets re-identification, which is content-independent and therefore *not*
blocked by SOP: two sites embedding the same tag link the same visitor by gaze.

---

## Quick start

### 1. Serve the harness and collect sessions

```bash
cd prototype
node server.js               # -> http://localhost:8080   (npm start also works)
```

Open **http://localhost:8080** (use `localhost` — `getUserMedia` needs a secure
context; `localhost` counts, a bare LAN IP would need HTTPS).

1. Enter a participant ID (e.g. `P01`), pick a session (`S1`), consent, and run
   the click **calibration**.
2. Complete each of the five tasks. Different content per page stands in for a
   different "site"; **cross-task** matching is the real tracking test.
3. For a **return visit**, reload the hub, switch to `S2`, and re-calibrate
   (this clears the prior model — an honest cross-session test). Ideally do `S2`
   on a different day.

Each finished task POSTs a session to `data/` as
`P01_S1_reading_<ts>.json` (raw gaze stream `{t, x, y}`, `x=null` for a
blink/lost-face gap). If the server is down the tracker downloads the file
instead — drop it into `data/`.

### 2. Live re-identification demo

With a few participants enrolled, open **`/reid.html`**:

- **Capture 20 s probe & identify** — captures whoever is at the screen now and
  asks the server to rank enrolled participants by gaze-feature distance.
- **Wipe all browser state** — clears cookies + localStorage + sessionStorage +
  the WebGazer model, then identify again. The match still lands, because
  *who you are* was never stored in the browser. That is the "unclearable" point.

### 3. Offline evaluation (the numbers for the paper)

```bash
cd analysis
pip install -r requirements.txt        # numpy (+ matplotlib for --plot)
python reid.py --data ../data --plot cmc.png
```

`reid.py` reports rank-1, rank-5, and EER under four protocols; the headline is
`cross_task_cross_session` (different content **and** different visit).

---

## Verify without a webcam

The analysis pipeline is verifiable end-to-end on synthetic subjects that have
stable oculomotor traits across tasks/sessions:

```bash
cd analysis
python simulate.py --out ../data_sim --subjects 12 --sessions 2
python reid.py --data ../data_sim --plot ../data_sim/cmc.png
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
| RQ3 ceiling vs commodity | Gazepoint rig above + `tracker` field |
| RQ4 unclearability | `reid.html` wipe-state demo; cross-origin collector |
| RQ5 defense (future) | perturb the stream in `gazepry-tracker.js` before submit |

## Caveats

- **Webcam accuracy is the honest risk.** WebGazer drifts over a session; the
  I-VT velocity threshold (`VEL_THRESHOLD` in `reid-core.js` / `features.py`) is
  coarse at ~30 Hz and will need tuning against real data. Treat webcam re-ID
  numbers as a **lower bound** on the threat.
- The hand-crafted feature set is route (a) from the protocol. A deep model
  (Eye Know You Too-style) is the ceiling and a natural extension.
- `features.py` and `reid-core.js` must stay in sync if you change features.
- IRB: this project is IRB-exempt; still, never commit raw participant gaze
  (`data/` is git-ignored).
