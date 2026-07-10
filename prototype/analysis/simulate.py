"""
Synthetic gaze generator — verifies the re-ID pipeline end-to-end without a
webcam. Each simulated subject has STABLE latent oculomotor traits (fixation
durations, saccade amplitudes, blink rate) that persist across sessions and
tasks; tasks modulate those traits. If the pipeline is correct, cross-task /
cross-session re-ID on this data should score far above chance.

This is a sanity harness for the code, NOT a claim about real eyes. Real data
comes from the browser harness; see the prototype README.

Usage:
  python simulate.py --out ../data_sim --subjects 12 --sessions 2
  python reid.py --data ../data_sim
"""
from __future__ import annotations
import argparse
import json
import math
import os
import random

TASKS = ["reading", "serp", "images", "video", "form"]

# task modulation of (fixation-duration factor, saccade-amplitude factor, is_pursuit).
# Kept mild so that stable per-subject traits remain recoverable ACROSS tasks —
# this is a code-verification harness, not a model of real cross-task difficulty.
TASK_MOD = {
    "reading": (0.88, 0.70, False),
    "serp":    (1.00, 1.00, False),
    "images":  (1.18, 1.18, False),
    "video":   (1.00, 0.55, True),   # smooth pursuit dominates
    "form":    (1.05, 0.90, False),
}


def subject_traits(subject_seed):
    r = random.Random(subject_seed)
    # wide inter-subject spread so identity dominates task modulation
    return {
        "fix_mean_ms": r.uniform(160, 360),      # base fixation duration
        "fix_cv": r.uniform(0.20, 0.55),         # variability
        "sacc_amp": r.uniform(0.08, 0.24),       # fraction of screen diagonal
        "sacc_prob": r.uniform(0.65, 0.97),      # chance of a real saccade vs micro
        "blink_hz": r.uniform(0.10, 0.55),       # blinks / second (task-stable cue)
    }


def gen_session(pid, sid, task, traits, session_seed, dur_s=60, fps=30, tracker="synthetic"):
    r = random.Random(session_seed)
    innerW, innerH = 1440, 900
    diag = math.hypot(innerW, innerH)
    fdac, saac, pursuit = TASK_MOD[task]

    # small day-to-day (session) drift on top of stable traits
    fix_mean = traits["fix_mean_ms"] * fdac * r.uniform(0.95, 1.05)
    amp = traits["sacc_amp"] * saac * r.uniform(0.95, 1.05)
    blink_hz = traits["blink_hz"] * r.uniform(0.90, 1.10)

    samples = []
    t = 0.0
    x = r.uniform(0.3, 0.7) * innerW
    y = r.uniform(0.3, 0.7) * innerH
    # pursuit target params
    px_amp, py_amp = 0.4 * innerW, 0.35 * innerH
    total_ms = dur_s * 1000
    gaps = 0

    def step_time():
        return 1000.0 / fps * r.uniform(0.85, 1.15)  # webcam-like jitter

    if pursuit:
        # smooth pursuit: gaze tracks a slowly moving target with small noise
        start = t
        while t < total_ms:
            phase = (t - start) / 1000.0
            tx = innerW / 2 + px_amp * math.sin(0.55 * phase)
            ty = innerH / 2 + py_amp * math.sin(0.83 * phase + 1.1)
            x += (tx - x) * 0.35 + r.gauss(0, 3)
            y += (ty - y) * 0.35 + r.gauss(0, 3)
            if r.random() < blink_hz / fps:
                for _ in range(r.randint(1, 3)):
                    samples.append({"t": round(t), "x": None, "y": None}); gaps += 1; t += step_time()
                continue
            samples.append({"t": round(t), "x": round(x, 1), "y": round(y, 1)})
            t += step_time()
    else:
        # alternate fixations and saccades
        while t < total_ms:
            fd = max(60.0, r.gauss(fix_mean, fix_mean * traits["fix_cv"]))
            fend = t + fd
            while t < fend and t < total_ms:
                if r.random() < blink_hz / fps:
                    for _ in range(r.randint(1, 3)):
                        samples.append({"t": round(t), "x": None, "y": None}); gaps += 1; t += step_time()
                    continue
                jx = x + r.gauss(0, 2.5)  # fixational jitter (px)
                jy = y + r.gauss(0, 2.5)
                samples.append({"t": round(t), "x": round(jx, 1), "y": round(jy, 1)})
                t += step_time()
            if t >= total_ms:
                break
            # saccade: single-frame jump (high velocity) to a new target
            if r.random() < traits["sacc_prob"]:
                a = abs(r.gauss(amp, amp * 0.3)) * diag
                ang = r.uniform(0, 2 * math.pi)
                x = min(max(x + a * math.cos(ang), 5), innerW - 5)
                y = min(max(y + a * math.sin(ang), 5), innerH - 5)
                samples.append({"t": round(t), "x": round(x, 1), "y": round(y, 1)})
                t += step_time()

    return {
        "schema": "gazepry.session.v1",
        "participant": pid, "session": sid, "task": task,
        "tracker": tracker, "trackerFamily": tracker,
        "startedAt": 1700000000000 + session_seed,
        "durationMs": int(samples[-1]["t"]) if samples else 0,
        "screen": {"innerW": innerW, "innerH": innerH, "w": innerW, "h": innerH, "dpr": 1},
        "userAgent": "synthetic",
        "nSamples": len(samples), "nGaps": gaps,
        "samples": samples,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "data_sim"))
    ap.add_argument("--subjects", type=int, default=12)
    ap.add_argument("--sessions", type=int, default=2)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--tracker", default="synthetic",
                    help="tracker label to tag these sessions with; run twice with different "
                         "labels into the same --out to exercise the per-tracker (RQ3) analysis")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    n = 0
    for si in range(args.subjects):
        pid = f"P{si + 1:02d}"
        traits = subject_traits(args.seed * 1000 + si)  # stable per subject
        for se in range(args.sessions):
            sid = f"S{se + 1}"
            for ti, task in enumerate(TASKS):
                session_seed = args.seed * 100000 + si * 1000 + se * 100 + ti
                sess = gen_session(pid, sid, task, traits, session_seed, tracker=args.tracker)
                fn = f"{pid}_{sid}_{task}_{args.tracker}_{sess['startedAt']}.json"
                json.dump(sess, open(os.path.join(args.out, fn), "w"))
                n += 1
    print(f"Wrote {n} synthetic '{args.tracker}' sessions for {args.subjects} subjects "
          f"x {args.sessions} sessions x {len(TASKS)} tasks -> {args.out}")


if __name__ == "__main__":
    main()
