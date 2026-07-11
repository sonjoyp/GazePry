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


def tracker_family(s):
    """Tracker slug for a session, tolerant of older records that stored only the
    full tracker id (e.g. "webgazer-3.5.3" -> "webgazer")."""
    fam = s.get("trackerFamily")
    if fam:
        return fam
    tid = s.get("tracker")
    return tid.split("-")[0] if tid else "webgazer"


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
        cond = s.get("condition") or {}
        sessions.append({
            "file": os.path.basename(fp),
            "participant": s.get("participant"),
            "session": s.get("session"),
            "task": s.get("task"),
            "tracker": tracker_family(s),
            # per-visit metadata (schema v2); older records default to baseline
            "condition": cond,
            "intervention": cond.get("intervention", "baseline"),
            # keep raw samples+screen so window/gallery/within-session analyses can
            # recompute features on a subset without re-reading the files
            "samples": s["samples"],
            "screen": s.get("screen"),
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
    # Never match across trackers: feature distributions differ, so a cross-tracker
    # "match" is meaningless. Per-tracker EER is exactly the RQ3 comparison.
    if cand.get("tracker") != probe.get("tracker"):
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


PROTOCOLS = ["all", "same_task_cross_session", "cross_task", "cross_task_cross_session"]


def report_tracker(sessions, label):
    """Standardize WITHIN this tracker's sessions and print the 4-protocol table.
    Returns the metric rows (for optional json dump)."""
    if len(sessions) < 2:
        print(f"[{label}] only {len(sessions)} session(s) — need >=2; skipping.\n")
        return []
    standardize(sessions)  # per-tracker stats: a fair, self-contained feature space
    participants = sorted(set(s["participant"] for s in sessions))
    tasks = sorted(set(s["task"] for s in sessions))
    print(f"=== tracker: {label} ===")
    print(f"{len(sessions)} sessions | {len(participants)} participants {participants} | tasks {tasks}")
    header = f"{'protocol':<26}{'probes':>7}{'IDs':>5}{'chance':>8}{'rank-1':>8}{'rank-5':>8}{'EER':>8}"
    print(header)
    print("-" * len(header))
    rows = []
    for p in PROTOCOLS:
        r = evaluate(sessions, p)
        r["tracker"] = label
        rows.append(r)
        def fmt(v):
            return "  n/a " if v != v else f"{v:7.3f}"
        print(f"{r['protocol']:<26}{r['n_probes_scored']:>7}{r['n_participants']:>5}"
              f"{fmt(r['chance_rank1'])}{fmt(r['rank1'])}{fmt(r['rank5'])}{fmt(r['eer'])}")
    print()
    return rows


# ---------------------------------------------------------------------------
# Additive controls & sweeps (§14 headline curves + Appendix A.3 confounds).
# Each rebuilds features on shallow copies and re-standardizes within the subset,
# so the default per-protocol run above is never disturbed.
# ---------------------------------------------------------------------------

def _window_feat(sess, window_s):
    """Feature vector from only the first `window_s` seconds of a session
    (None = full session). Answers 'how many seconds of viewing links you'."""
    if window_s is None:
        return sess["feat"]
    samples = sess.get("samples") or []
    if not samples:
        return sess["feat"]
    t0 = samples[0]["t"]
    cut = [s for s in samples if (s["t"] - t0) <= window_s * 1000.0]
    return np.array(extract_features(cut, sess.get("screen")), dtype=float)


def _eval_with(sessions, protocol, feat_fn):
    """Evaluate on shallow copies whose features come from feat_fn(sess),
    re-standardizing within this subset."""
    subset = [dict(s) for s in sessions]
    for s in subset:
        s["feat"] = feat_fn(s)
    standardize(subset)
    return evaluate(subset, protocol)


def window_sweep(sessions, label, protocol="cross_task_cross_session",
                 windows=(5, 15, 30, 60, None)):
    """Accuracy vs. observation window — §14 key curve / A.7 headline result #1."""
    print(f"=== [{label}] observation-window sweep ({protocol}) ===")
    print(f"{'window':>8}{'probes':>8}{'rank-1':>8}{'rank-5':>8}{'EER':>8}")
    rows = []
    for w in windows:
        r = _eval_with(sessions, protocol, lambda s, w=w: _window_feat(s, w))
        r["window_s"] = w if w is not None else "full"
        r["tracker"] = label
        rows.append(r)
        f = lambda v: "  n/a " if v != v else f"{v:7.3f}"
        print(f"{str(r['window_s']):>8}{r['n_probes_scored']:>8}{f(r['rank1'])}{f(r['rank5'])}{f(r['eer'])}")
    print()
    return rows


def gallery_sweep(sessions, label, protocol="cross_task_cross_session",
                  sizes=(10, 25, 50, None), seed=0):
    """Accuracy vs. gallery size — how the threat scales to a tracked population."""
    parts = sorted(set(s["participant"] for s in sessions))
    rng = np.random.RandomState(seed)
    print(f"=== [{label}] gallery-size sweep ({protocol}) ===")
    print(f"{'gallery':>8}{'probes':>8}{'chance':>8}{'rank-1':>8}{'EER':>8}")
    rows = []
    seen = set()
    for g in sizes:
        gsize = len(parts) if (g is None or g >= len(parts)) else g
        if gsize in seen:  # sizes larger than the pool clamp to full — print it once
            continue
        seen.add(gsize)
        keep = set(parts) if gsize >= len(parts) else set(rng.choice(parts, size=gsize, replace=False))
        sub = [s for s in sessions if s["participant"] in keep]
        r = _eval_with(sub, protocol, lambda s: s["feat"])
        r["gallery"] = gsize
        r["tracker"] = label
        rows.append(r)
        f = lambda v: "  n/a " if v != v else f"{v:7.3f}"
        print(f"{gsize:>8}{r['n_probes_scored']:>8}{f(r['chance_rank1'])}{f(r['rank1'])}{f(r['eer'])}")
    print()
    return rows


def shuffle_null(sessions, label, protocol="cross_task_cross_session", n_perm=20, seed=0):
    """Shuffled-label null (A.3): permute participant labels and re-run. rank-1
    must collapse toward chance and EER toward 0.5, or the 'biometric' is an
    artifact. The cheapest credibility win — always report it."""
    rng = np.random.RandomState(seed)
    real = _eval_with(sessions, protocol, lambda s: s["feat"])
    # Scramble labels ACROSS SESSIONS (not a consistent per-person bijection, which
    # would merely rename clusters and preserve grouping). Reassigning the multiset
    # of labels to sessions at random destroys the person<->session association, so
    # a genuine biometric collapses to chance while an apparatus artifact would not.
    labels = [s["participant"] for s in sessions]
    r1s, eers = [], []
    for _ in range(n_perm):
        perm = labels[:]
        rng.shuffle(perm)
        subset = [dict(s) for s in sessions]
        for s, lab in zip(subset, perm):
            s["participant"] = lab
        standardize(subset)
        r = evaluate(subset, protocol)
        if r["rank1"] == r["rank1"]:
            r1s.append(r["rank1"])
        if r["eer"] == r["eer"]:
            eers.append(r["eer"])
    chance = real["chance_rank1"]
    print(f"=== [{label}] shuffled-label null ({protocol}, {n_perm} permutations) ===")
    print(f"  real:    rank-1 ={real['rank1']:.3f}  EER={real['eer']:.3f}  (chance rank-1 ~= {chance:.3f})")
    if r1s:
        print(f"  shuffled: rank-1 = {np.mean(r1s):.3f} +/- {np.std(r1s):.3f}  "
              f"EER = {np.mean(eers):.3f} +/- {np.std(eers):.3f}")
        print(f"  -> {'PASS' if np.mean(r1s) <= chance * 2 else 'CHECK'}: shuffled rank-1 should sit near chance.\n")
    else:
        print("  (no scorable probes under this protocol)\n")
    return {"real": real, "shuffled_rank1_mean": float(np.mean(r1s)) if r1s else float("nan"),
            "shuffled_eer_mean": float(np.mean(eers)) if eers else float("nan")}


def within_session_bound(sessions, label):
    """Within-session leakage UPPER BOUND (A.3): split each session's samples into
    enroll/probe halves and re-ID same-task cross-'session'. Always reported next
    to the real cross-session cell so the easy case never masquerades as the threat."""
    halves = []
    for s in sessions:
        samples = s.get("samples") or []
        if len(samples) < 8:
            continue
        mid = len(samples) // 2
        for tag, part in (("H1", samples[:mid]), ("H2", samples[mid:])):
            halves.append({
                "file": f"{s['file']}#{tag}", "participant": s["participant"],
                "session": f"{s['session']}-{tag}", "task": s["task"],
                "tracker": s["tracker"], "screen": s.get("screen"), "samples": part,
                "feat": np.array(extract_features(part, s.get("screen")), dtype=float),
            })
    if len(halves) < 2:
        print(f"=== [{label}] within-session bound === (too few samples)\n")
        return None
    r = _eval_with(halves, "same_task_cross_session", lambda s: s["feat"])
    print(f"=== [{label}] within-session leakage bound (upper bound, not the threat) ===")
    fmt = lambda v: "n/a" if v != v else f"{v:.3f}"
    print(f"  rank-1 = {fmt(r['rank1'])}  rank-5 = {fmt(r['rank5'])}  EER = {fmt(r['eer'])}\n")
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.path.join(os.path.dirname(__file__), "..", "data"))
    ap.add_argument("--tracker", default=None, help="evaluate only this tracker family (e.g. webgazer)")
    ap.add_argument("--plot", default=None, help="optional path to save a CMC plot (needs matplotlib)")
    ap.add_argument("--out", default=None, help="optional path to write metrics json")
    ap.add_argument("--windows", action="store_true",
                    help="also print the accuracy-vs-observation-window sweep (§14 headline curve)")
    ap.add_argument("--gallery", action="store_true",
                    help="also print the accuracy-vs-gallery-size sweep (§14)")
    ap.add_argument("--shuffle", action="store_true",
                    help="also run the shuffled-label null control (A.3)")
    ap.add_argument("--within-session", action="store_true",
                    help="also print the within-session leakage upper bound (A.3)")
    ap.add_argument("--controls", action="store_true",
                    help="shorthand for --windows --gallery --shuffle --within-session")
    args = ap.parse_args()
    if args.controls:
        args.windows = args.gallery = args.shuffle = args.within_session = True

    sessions = load_sessions(args.data)
    if args.tracker:
        sessions = [s for s in sessions if s["tracker"] == args.tracker]
    if len(sessions) < 2:
        print(f"Need >=2 sessions in {args.data}"
              + (f" for tracker '{args.tracker}'" if args.tracker else "")
              + f"; found {len(sessions)}.")
        print("Collect real data with the harness, or generate synthetic data:")
        print("  python simulate.py --out ../data_sim")
        return

    trackers = sorted(set(s["tracker"] for s in sessions))
    print(f"Loaded {len(sessions)} sessions across {len(trackers)} tracker(s): {trackers}\n")

    # RQ3: report each tracker separately (ceiling vs commodity is a per-tracker
    # comparison), standardizing within each so the feature spaces stay fair.
    rows = []
    for tr in trackers:
        rows += report_tracker([s for s in sessions if s["tracker"] == tr], tr)

    print("Headline per tracker (real tracking threat) = cross_task_cross_session.")
    print("rank-1 >> chance and EER well below 0.5 => gaze links users across content and visits.")
    if len(trackers) > 1:
        print("Compare cross_task_cross_session EER across trackers for the RQ3 ceiling-vs-commodity gap.")
    print()

    # Additive controls / headline curves (opt-in), per tracker.
    if args.windows or args.gallery or args.shuffle or args.within_session:
        for tr in trackers:
            sub = [s for s in sessions if s["tracker"] == tr]
            if len(sub) < 2:
                continue
            if args.windows:
                window_sweep(sub, tr)
            if args.gallery:
                gallery_sweep(sub, tr)
            if args.shuffle:
                shuffle_null(sub, tr)
            if args.within_session:
                within_session_bound(sub, tr)

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
            # Plot the headline protocol's CMC, one curve per tracker.
            for tr in trackers:
                sub = [s for s in sessions if s["tracker"] == tr]
                if len(sub) < 2:
                    continue
                standardize(sub)
                xs, ys = cmc_curve(sub, "cross_task_cross_session")
                plt.plot(xs, ys, marker="o", label=tr)
            plt.xlabel("rank k"); plt.ylabel("identification rate (CMC)")
            plt.ylim(0, 1.02); plt.grid(alpha=.3); plt.legend(fontsize=8)
            plt.title("Cross-site gaze re-ID (cross-task, cross-session) — CMC by tracker")
            plt.tight_layout(); plt.savefig(args.plot, dpi=130)
            print(f"Wrote CMC plot -> {args.plot}")
        except ImportError:
            print("matplotlib not installed; skipping plot (pip install matplotlib).")


if __name__ == "__main__":
    main()
