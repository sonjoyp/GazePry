# GazePry

**A security/privacy research project on information leakage from webcam-based eye tracking.**

GazePry studies what a *drive-by web adversary* — a first- or third-party script
that obtains camera access and runs gaze estimation client-side — can infer about
a user, on commodity laptops/desktops with no special hardware. It builds on the
WebGazer / SearchGazer lineage but reframes it as a threat model.

> The root of this repo still contains the original **SearchGazer (2016/2017)**
> demo files (`searchgazer.js`, `index.html`, `examples/`, `css/`, `media/`) for
> historical reference. That library is out of date. **New work uses the current
> [brownhci/WebGazer](https://github.com/brownhci/WebGazer) v3.5.3**, bundled in
> the prototype below.

## Contents

- **[`GazePry_Information_Leakage_Report.md`](GazePry_Information_Leakage_Report.md)**
  — threat-model assessment: two regimes of gaze leakage (content-dependent vs
  content-independent), leakage vectors D1–D6, form-factor analysis, evidence
  table, and a full bibliography.
- **[`GazePry_Direction1_ReID_Study_Protocol.md`](GazePry_Direction1_ReID_Study_Protocol.md)**
  — the study protocol for the lead research direction: *cross-site gaze
  re-identification as an unclearable web tracking vector*. Threat model, research
  questions, apparatus (incl. the Gazepoint ground-truth rig), conditions matrix,
  metrics, and target venues.
- **[`prototype/`](prototype/)** — a working prototype for Direction 1:
  a WebGazer v3.5.3 capture harness (five task "sites" sharing one tracking tag),
  a zero-dependency Node ingestion + live re-ID server, and a Python evaluation
  pipeline (content-independent features, cross-task/cross-session rank-1 / EER /
  CMC) that is verifiable end-to-end on synthetic data. See
  [`prototype/README.md`](prototype/README.md).

## Quick start

```bash
cd prototype
node server.js            # http://localhost:8080 — capture harness + re-ID demo
```

```bash
cd prototype/analysis     # verify the analysis pipeline without a webcam
pip install -r requirements.txt
python simulate.py --out ../data_sim
python reid.py --data ../data_sim --plot ../data_sim/cmc.png
```

## Credit & license

The eye-tracking engine is [WebGazer](https://webgazer.cs.brown.edu) by the
Brown HCI Group; the search instrumentation derives from SearchGazer
(Papoutsaki, Laskey, Huang, CHIIR 2017). This project is licensed under GPLv3
(see [`LICENSE.md`](LICENSE.md) / [`gplv3.md`](gplv3.md)).

```
@inproceedings{papoutsaki2017searchgazer,
  author = {Alexandra Papoutsaki and James Laskey and Jeff Huang},
  title  = {SearchGazer: Webcam Eye Tracking for Remote Studies of Web Search},
  booktitle = {Proc. ACM SIGIR Conf. Human Information Interaction \& Retrieval (CHIIR)},
  year   = {2017}, organization = {ACM}
}
```
