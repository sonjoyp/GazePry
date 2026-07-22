"""
Synthetic recognition-probe sessions (Direction D7 pipeline verification).

The D4 counterpart is simulate.py. This generates ``gazepry.probe.v1`` sessions
so the whole D7 chain -- trial plan, AOI assignment, I-DT segmentation, feature
extraction, classifier, RQ0 nulls -- is runnable and testable end to end without
a webcam or a participant.

**These are not results.** They are a code sanity check on generated data. The
generator writes the effect in by construction, so recovering it proves the
pipeline is wired up, and nothing whatsoever about real eyes.

The most important switch is ``--effect 0``, which produces a dataset with NO
familiarity effect. The pipeline must report chance on it. A pipeline that finds
a signal in the null is broken in a way that no amount of real data would reveal.

Usage:
  python simulate_probe.py --out ../data_probe_sim --subjects 20 --trials 40
  python simulate_probe.py --out ../data_probe_null --subjects 20 --effect 0
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
from typing import List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe_protocol import TIMING, build_trials, layout  # noqa: E402

VIEW_W, VIEW_H = 1920, 1080


def _lognormal(rng: random.Random, mean_ms: float, sigma: float = 0.35) -> float:
    mu = math.log(max(1.0, mean_ms)) - sigma * sigma / 2
    return math.exp(rng.gauss(mu, sigma))


def simulate_trial(rng: random.Random, rects: List[dict], familiar_idx: int,
                   effect: float, hz: float, noise_px: float,
                   bias: tuple, gap_rate: float) -> List[dict]:
    """One trial's gaze samples over the array-presentation window.

    The effect is written in two places, mirroring what the literature reports:
      - a DWELL bias (more/less looking at the familiar tile), and
      - a FIXATION-DURATION bias (longer fixations on the familiar tile), which
        is the channel Millen & Hancock 2019 found survives concealment.
    Setting ``effect=0`` removes both and yields a pure null.
    """
    dur = TIMING["arrayMs"]
    n = len(rects)
    # selection weights: the familiar tile is visited more often
    w = [1.0] * n
    w[familiar_idx] = 1.0 + effect
    tot = sum(w)
    w = [v / tot for v in w]

    samples: List[dict] = []
    t = 0.0
    step = 1000.0 / hz
    while t < dur:
        # pick a tile, then dwell there for one fixation
        r = rng.random()
        acc, target = 0.0, n - 1
        for i, p in enumerate(w):
            acc += p
            if r <= acc:
                target = i
                break
        base = 260.0 * (1.0 + 0.45 * effect if target == familiar_idx else 1.0)
        fix_ms = _lognormal(rng, base)
        cx = rects[target]["x"] + rects[target]["w"] / 2.0
        cy = rects[target]["y"] + rects[target]["h"] / 2.0
        end = min(dur, t + fix_ms)
        while t < end:
            if rng.random() < gap_rate:
                samples.append({"t": round(t), "x": None, "y": None})
            else:
                samples.append({
                    "t": round(t),
                    "x": round(cx + bias[0] + rng.gauss(0, noise_px), 1),
                    "y": round(cy + bias[1] + rng.gauss(0, noise_px), 1),
                })
            t += step
        # saccade: a couple of in-flight samples between tiles
        for _ in range(2):
            if t >= dur:
                break
            samples.append({"t": round(t),
                            "x": round(rng.uniform(0, VIEW_W), 1),
                            "y": round(rng.uniform(0, VIEW_H), 1)})
            t += step
    return samples


def make_session(pid: str, experiment: str, array_n: int, n_trials: int,
                 effect: float, seed: int, tracker: str, awareness: str,
                 cover: str, delay: str) -> dict:
    rng = random.Random(seed)
    plan = build_trials(pid, experiment, array_n, n_trials)
    L = layout(array_n, VIEW_W, VIEW_H)

    # Per-participant capture properties. The cadence spread is deliberate: it
    # reproduces the D4 logged-rate confound (~50-120 Hz varying by person) so
    # the within-trial relativisation in aoi_features.py is actually exercised.
    hz = rng.uniform(45, 115)
    noise_px = rng.uniform(45, 110)              # webcam spatial error
    bias = (rng.gauss(0, 40), rng.gauss(0, 40))  # per-person calibration offset
    gap_rate = rng.uniform(0.02, 0.10)

    samples: List[dict] = []
    trials: List[dict] = []
    clock = 1000.0
    for tr in plan["trials"]:
        clock += TIMING["fixationMs"]
        onset = round(clock)
        fam_idx = next(i for i, s in enumerate(tr["slots"]) if s["familiar"])
        ts = simulate_trial(rng, L["rects"], fam_idx, effect, hz, noise_px, bias, gap_rate)
        for s in ts:
            samples.append({"t": round(onset + s["t"]), "x": s["x"], "y": s["y"]})
        clock += TIMING["arrayMs"]
        offset = round(clock)
        clock += TIMING["blankMs"] + rng.uniform(600, 2200)   # cover-task response
        trials.append({
            "index": tr["index"],
            "probeItemId": tr["probeItemId"],
            "onsetT": onset, "offsetT": offset,
            "coverResponseSlot": rng.randrange(array_n),
            "coverResponseItemId": None,
            "coverResponseFamiliar": None,
            "aois": [{"slot": i, "itemId": s["itemId"], "familiar": s["familiar"],
                      "rect": L["rects"][i]} for i, s in enumerate(tr["slots"])],
        })

    n_gaps = sum(1 for s in samples if s["x"] is None)
    return {
        "schema": "gazepry.probe.v1",
        "participant": pid, "session": "S1", "task": "probe",
        "tracker": tracker + "-sim", "trackerFamily": tracker,
        "experiment": experiment, "arrayN": array_n,
        "coverTask": cover, "awareness": awareness,
        "counterbalanceGroup": plan["counterbalanceGroup"],
        "delayCondition": delay,
        "startedAt": 1700000000000 + seed * 1000,
        "durationMs": round(clock),
        "condition": {"synthetic": True, "calibResidualPx": round(noise_px, 1)},
        "screen": {"w": VIEW_W, "h": VIEW_H, "dpr": 1,
                   "innerW": VIEW_W, "innerH": VIEW_H},
        "userAgent": "simulate_probe.py",
        "nSamples": len(samples), "nGaps": n_gaps, "nTrials": len(trials),
        "clockAnchored": True,
        "trials": trials, "samples": samples,
        "meta": {"synthetic": True, "effect": effect, "hz": round(hz, 1),
                 "noisePx": round(noise_px, 1), "protocolVersion": "d7.v1"},
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="synthetic D7 recognition-probe sessions")
    ap.add_argument("--out", required=True)
    ap.add_argument("--subjects", type=int, default=20)
    ap.add_argument("--trials", type=int, default=40)
    ap.add_argument("--array", type=int, default=4, choices=[2, 4])
    ap.add_argument("--experiment", default="E1", choices=["E1", "E2", "E3"])
    ap.add_argument("--effect", type=float, default=0.8,
                    help="familiarity effect size; 0 produces a NULL dataset")
    ap.add_argument("--awareness", default="naive", choices=["naive", "countermeasure"])
    ap.add_argument("--cover", default="memory-adjacent")
    ap.add_argument("--delay", default="immediate")
    ap.add_argument("--tracker", default="webgazer")
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args(argv)

    os.makedirs(a.out, exist_ok=True)
    written = 0
    for i in range(a.subjects):
        pid = f"S{i + 1:02d}"
        sess = make_session(pid, a.experiment, a.array, a.trials, a.effect,
                            a.seed * 1000 + i, a.tracker, a.awareness,
                            a.cover, a.delay)
        fn = f"{pid}_S1_probe_{a.tracker}_{sess['startedAt']}.json"
        with open(os.path.join(a.out, fn), "w", encoding="utf-8") as fh:
            json.dump(sess, fh)
        written += 1
    print(f"wrote {written} synthetic probe session(s) to {a.out} "
          f"(experiment={a.experiment}, effect={a.effect}, array={a.array})")
    if a.effect == 0:
        print("  NULL dataset: the pipeline must report chance on this.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
