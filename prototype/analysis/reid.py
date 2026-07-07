"""
Cross-task / cross-session gaze re-identification evaluation (Direction 1).

Loads captured sessions, extracts content-independent features, and reports
re-ID accuracy under four protocols that separate the "easy" case from the
real tracking threat:

  all                       any other session may be in the gallery
  same_task_cross_session   enroll & probe on the SAME content, different visit
                            (test-retest robustness)
  cross_task                enroll on one content, probe on ANOTHER (the
                            generalisation that makes it *tracking*)
  cross_task_cross_session  different content AND different visit  <-- headline

Metrics: rank-1, rank-5 identification accuracy, and verification EER.

Usage:
  python reid.py --data ../data
  python reid.py --data ../data_sim --plot cmc.png
"""
from __future__ import annotations
import argparse
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from features import extract_features, FEATURE_NAMES  # noqa: E402


def load_sessions(data_dir):
    sessions = []
    for fp in sorted(glob.glob(os.path.join(data_dir, "*.json"))):
        try:
            s = json.load(open(fp, "r", encoding="utf-8"))
        except Exception:
            continue
        # skip anything that is not a session record (e.g. a metrics.json dump)
        if not isinstance(s, dict) or not s.get("samples") or not s.get("participant"):
            continue
        sessions.append({
            "file": os.path.basename(fp),
            "participant": s.get("participant"),
            "session": s.get("session"),
            "task": s.get("task"),
            "feat": np.array(extract_features(s["samples"], s.get("screen")), dtype=float),
        })
    return sessions


def standardize(sessions):
    X = np.array([s["feat"] for s in sessions])
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd[sd == 0] = 1.0
    for s in sessions:
        s["z"] = (s["feat"] - mu) / sd
    return mu, sd


def eligible(probe, cand, protocol):
    if cand["file"] == probe["file"]:
        return False
    same_task = cand["task"] == probe["task"]
    same_sess = cand["session"] == probe["session"]
    if protocol == "all":
        return True
    if protocol == "same_task_cross_session":
        return same_task and not same_sess
    if protocol == "cross_task":
        return not same_task
    if protocol == "cross_task_cross_session":
        return (not same_task) and (not same_sess)
    raise ValueError(protocol)


def evaluate(sessions, protocol):
    genuine, impostor = [], []
    ranks = []  # rank of the true participant, when enrolled
    n_participants_seen = set()

    for probe in sessions:
        gal = [c for c in sessions if eligible(probe, c, protocol)]
        if not gal:
            continue
        # nearest gallery session per participant (in z-space)
        best = {}
        for c in gal:
            d = float(np.linalg.norm(probe["z"] - c["z"]))
            if c["participant"] not in best or d < best[c["participant"]]:
                best[c["participant"]] = d
        ranked = sorted(best.items(), key=lambda kv: kv[1])  # (participant, dist) asc
        n_participants_seen.update(best.keys())

        # verification pairs: genuine = distance to own nearest; impostor = others
        if probe["participant"] in best:
            genuine.append(best[probe["participant"]])
        for p, d in best.items():
            if p != probe["participant"]:
                impostor.append(d)

        # identification: only scored if the true participant is enrollable here
        if probe["participant"] in best:
            order = [p for p, _ in ranked]
            ranks.append(order.index(probe["participant"]) + 1)

    n = len(ranks)
    rank1 = np.mean([r == 1 for r in ranks]) if n else float("nan")
    rank5 = np.mean([r <= 5 for r in ranks]) if n else float("nan")
    eer, thr = compute_eer(genuine, impostor)
    return {
        "protocol": protocol,
        "n_probes_scored": n,
        "n_participants": len(n_participants_seen),
        "chance_rank1": (1.0 / len(n_participants_seen)) if n_participants_seen else float("nan"),
        "rank1": rank1,
        "rank5": rank5,
        "eer": eer,
        "ranks": ranks,
    }


def compute_eer(genuine, impostor):
    """EER from genuine/impostor DISTANCES (smaller distance = more similar).
    Similarity s = -distance; accept if s >= thr. Sweep candidate thresholds
    and take the point where FAR and FRR are closest."""
    if not genuine or not impostor:
        return float("nan"), float("nan")
    g = -np.array(genuine, dtype=float)
    im = -np.array(impostor, dtype=float)
    thrs = np.unique(np.concatenate([g, im]))
    best_eer, best_thr, best_gap = 1.0, 0.0, float("inf")
    for t in thrs:
        far = float(np.mean(im >= t))   # impostors accepted
        frr = float(np.mean(g < t))     # genuines rejected
        gap = abs(far - frr)
        if gap < best_gap:
            best_gap = gap
            best_eer = (far + frr) / 2.0
            best_thr = float(t)
    return best_eer, best_thr


def cmc_curve(sessions, protocol, max_rank=10):
    res = evaluate(sessions, protocol)
    ranks = res["ranks"]
    if not ranks:
        return list(range(1, max_rank + 1)), [float("nan")] * max_rank
    xs = list(range(1, max_rank + 1))
    ys = [float(np.mean([r <= k for r in ranks])) for k in xs]
    return xs, ys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.path.join(os.path.dirname(__file__), "..", "data"))
    ap.add_argument("--plot", default=None, help="optional path to save a CMC plot (needs matplotlib)")
    ap.add_argument("--out", default=None, help="optional path to write metrics json")
    args = ap.parse_args()

    sessions = load_sessions(args.data)
    if len(sessions) < 2:
        print(f"Need >=2 sessions in {args.data}; found {len(sessions)}.")
        print("Collect real data with the harness, or generate synthetic data:")
        print("  python simulate.py --out ../data_sim")
        return

    standardize(sessions)
    participants = sorted(set(s["participant"] for s in sessions))
    tasks = sorted(set(s["task"] for s in sessions))
    print(f"Loaded {len(sessions)} sessions | {len(participants)} participants "
          f"{participants} | tasks {tasks}\n")

    protocols = ["all", "same_task_cross_session", "cross_task", "cross_task_cross_session"]
    rows = []
    header = f"{'protocol':<26}{'probes':>7}{'IDs':>5}{'chance':>8}{'rank-1':>8}{'rank-5':>8}{'EER':>8}"
    print(header)
    print("-" * len(header))
    for p in protocols:
        r = evaluate(sessions, p)
        rows.append(r)
        def fmt(v):
            return "  n/a " if v != v else f"{v:7.3f}"
        print(f"{r['protocol']:<26}{r['n_probes_scored']:>7}{r['n_participants']:>5}"
              f"{fmt(r['chance_rank1'])}{fmt(r['rank1'])}{fmt(r['rank5'])}{fmt(r['eer'])}")

    print("\nHeadline (real tracking threat) = cross_task_cross_session.")
    print("rank-1 >> chance and EER well below 0.5 => gaze links users across content and visits.")

    if args.out:
        json.dump([{k: v for k, v in r.items() if k != "ranks"} for r in rows],
                  open(args.out, "w"), indent=2)
        print(f"\nWrote metrics -> {args.out}")

    if args.plot:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            plt.figure(figsize=(6, 4))
            for p in protocols:
                xs, ys = cmc_curve(sessions, p)
                plt.plot(xs, ys, marker="o", label=p)
            plt.xlabel("rank k"); plt.ylabel("identification rate (CMC)")
            plt.ylim(0, 1.02); plt.grid(alpha=.3); plt.legend(fontsize=8)
            plt.title("Cross-site gaze re-identification — CMC")
            plt.tight_layout(); plt.savefig(args.plot, dpi=130)
            print(f"Wrote CMC plot -> {args.plot}")
        except ImportError:
            print("matplotlib not installed; skipping plot (pip install matplotlib).")


if __name__ == "__main__":
    main()
