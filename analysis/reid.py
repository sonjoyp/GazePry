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


def _session_quality(samples):
    """(duration_s, n_samples, valid_fraction, median_hz) for a raw sample list."""
    n = len(samples)
    if n < 2:
        return 0.0, n, (1.0 if n and samples[0].get("x") is not None else 0.0), 0.0
    dur_s = (samples[-1]["t"] - samples[0]["t"]) / 1000.0
    valid = sum(1 for s in samples if s.get("x") is not None)
    hz = (n / dur_s) if dur_s > 0 else 0.0
    return dur_s, n, (valid / n if n else 0.0), hz


def load_sessions(data_dir, min_valid_frac=0.2, min_dur_s=2.0, min_samples=20,
                  resample_hz=None, verbose=False):
    """Load session records, dropping ones too degraded to yield trustworthy
    features (all-gap captures, sub-second clips). Dropping is reported, never
    silent. `resample_hz`, when set, equalizes cadence before feature extraction
    (see features.resample) — leave None for the reproducible default feature space.
    """
    sessions, dropped = [], []
    for fp in sorted(glob.glob(os.path.join(data_dir, "*.json"))):
        name = os.path.basename(fp)
        try:
            s = json.load(open(fp, "r", encoding="utf-8"))
        except Exception:
            continue
        # skip anything that is not a session record (e.g. a metrics.json dump)
        if not isinstance(s, dict) or not s.get("samples") or not s.get("participant"):
            continue
        dur_s, n_samp, valid_frac, hz = _session_quality(s["samples"])
        if n_samp < min_samples or dur_s < min_dur_s or valid_frac < min_valid_frac:
            dropped.append((name, f"n={n_samp} dur={dur_s:.1f}s valid={valid_frac:.0%}"))
            continue
        cond = s.get("condition") or {}
        sessions.append({
            "file": name,
            "participant": s.get("participant"),
            "session": s.get("session"),
            "task": s.get("task"),
            "tracker": tracker_family(s),
            # startedAt drives the ≥1-week elapsed-time gate (eligible(), 1.2);
            # fall back to any parseable timestamp in the filename tail
            "startedAt": s.get("startedAt"),
            "median_hz": hz,
            # per-visit metadata (schema v2); older records default to baseline
            "condition": cond,
            "intervention": cond.get("intervention", "baseline"),
            # keep raw samples+screen so window/gallery/within-session analyses can
            # recompute features on a subset without re-reading the files
            "samples": s["samples"],
            "screen": s.get("screen"),
            "feat": np.array(extract_features(s["samples"], s.get("screen"),
                                              resample_hz=resample_hz), dtype=float),
        })
    if verbose and dropped:
        print(f"Data-quality guard dropped {len(dropped)} session(s) "
              f"(min valid>={min_valid_frac:.0%}, dur>={min_dur_s}s, samples>={min_samples}):")
        for name, why in dropped:
            print(f"  - {name}  [{why}]")
        print()
    return sessions


def standardize(sessions):
    X = np.array([s["feat"] for s in sessions])
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd[sd == 0] = 1.0
    for s in sessions:
        s["z"] = (s["feat"] - mu) / sd
    return mu, sd


def eligible(probe, cand, protocol, min_gap_days=None):
    if cand["file"] == probe["file"]:
        return False
    # Never match across trackers: feature distributions differ, so a cross-tracker
    # "match" is meaningless. Per-tracker EER is exactly the RQ3 comparison.
    if cand.get("tracker") != probe.get("tracker"):
        return False
    same_task = cand["task"] == probe["task"]
    same_sess = cand["session"] == probe["session"]

    def gap_ok():
        # When a minimum elapsed gap is required, a different session *id* is not
        # enough — the returning-visitor threat (RQ1/RQ4) needs a real time gap.
        # Same-day "sessions" share calibration/lighting and must not count as the
        # cross-session threat. Unknown timestamps can't be confirmed -> excluded.
        if min_gap_days is None:
            return True
        ta, tb = probe.get("startedAt"), cand.get("startedAt")
        if ta is None or tb is None:
            return False
        return abs(ta - tb) >= min_gap_days * 86400_000  # days -> ms

    if protocol == "all":
        return True
    if protocol == "same_task_cross_session":
        return same_task and (not same_sess) and gap_ok()
    if protocol == "cross_task":
        return not same_task
    if protocol == "cross_task_cross_session":
        return (not same_task) and (not same_sess) and gap_ok()
    raise ValueError(protocol)


def evaluate(sessions, protocol, min_gap_days=None):
    genuine, impostor = [], []
    ranks = []  # rank of the true participant, when enrolled
    n_participants_seen = set()

    for probe in sessions:
        gal = [c for c in sessions if eligible(probe, c, protocol, min_gap_days)]
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
        print(f"[{label}] only {len(sessions)} session(s) - need >=2; skipping.\n")
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


def rate_control(sessions, label, protocol="cross_task_cross_session", hz=30):
    """Rate-equalized negative control (A.3, the decisive 'is it real?' test).
    Re-extract every session at a common cadence and re-run the headline protocol.
    Capture rate differs by participant in the pilot (P01≈50 Hz, P02≈110 Hz) and
    drives rate-sensitive features, so a match could be tracking *cadence*, not
    eyes. If re-ID holds after equalizing rate, the signal is (more likely) the
    person; if it collapses toward the null, it was the apparatus."""
    base = _eval_with(sessions, protocol, lambda s: s["feat"])

    def rfeat(s):
        return np.array(extract_features(s.get("samples") or [], s.get("screen"),
                                         resample_hz=hz), dtype=float)
    eq = _eval_with(sessions, protocol, rfeat)
    f = lambda v: "  n/a " if v != v else f"{v:7.3f}"
    print(f"=== [{label}] rate-equalized control ({protocol}) ===")
    print(f"  as-captured    : rank-1 ={f(base['rank1'])}  EER ={f(base['eer'])}  "
          f"(chance rank-1 ~= {f(base['chance_rank1'])})")
    print(f"  resampled {hz:>3} Hz: rank-1 ={f(eq['rank1'])}  EER ={f(eq['eer'])}")
    print(f"  -> if rank-1 drops toward chance after equalizing rate, the 'biometric' "
          f"was capture cadence.\n")
    return {"as_captured": base, "rate_equalized": eq, "hz": hz}


def cross_session_gap_report(sessions, label, min_gap_days=7):
    """Report the cross-session protocols restricted to gallery/probe pairs that
    are truly >= min_gap_days apart. A different session *id* alone is not the
    returning-visitor threat; same-day blocks share calibration/lighting. On a
    same-sitting pilot this correctly reports *no eligible pairs* — the honest state."""
    print(f"=== [{label}] true cross-session (>= {min_gap_days} day gap) ===")
    any_pairs = False
    for protocol in ("same_task_cross_session", "cross_task_cross_session"):
        r = evaluate(sessions, protocol, min_gap_days=min_gap_days)
        f = lambda v: "  n/a " if v != v else f"{v:7.3f}"
        if r["n_probes_scored"] == 0:
            print(f"  {protocol:<26} no eligible pairs >= {min_gap_days} days apart")
        else:
            any_pairs = True
            print(f"  {protocol:<26} probes={r['n_probes_scored']:>3}  "
                  f"rank-1 ={f(r['rank1'])}  EER ={f(r['eer'])}")
    if not any_pairs:
        print("  (pilot sessions are same-sitting; the returning-visitor threat is untested here)")
    print()


def capture_rate_summary(sessions, label):
    """Print median capture rate per participant — makes the rate confound visible.
    Wide spread across participants means rate is a candidate identity shortcut."""
    by_p = {}
    for s in sessions:
        by_p.setdefault(s["participant"], []).append(s.get("median_hz") or 0.0)
    print(f"=== [{label}] capture rate by participant (Hz, median across sessions) ===")
    for p in sorted(by_p):
        vals = sorted(by_p[p])
        med = vals[len(vals) // 2]
        print(f"  {p}: {med:5.1f} Hz  (n={len(vals)} sessions)")
    print()


def confound_battery(sessions, label):
    """The controls that decide whether a match is the person or the apparatus.
    Printed by default beside every headline number (plan A.3 / 1.3)."""
    capture_rate_summary(sessions, label)
    shuffle_null(sessions, label)
    rate_control(sessions, label)
    cross_session_gap_report(sessions, label)
    within_session_bound(sessions, label)


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
    ap.add_argument("--no-battery", action="store_true",
                    help="suppress the default confound battery (rate control, shuffle-null, "
                         "true cross-session, within-session) — normally always printed (A.3)")
    ap.add_argument("--controls", action="store_true",
                    help="shorthand for --windows --gallery (the heavier sweeps)")
    args = ap.parse_args()
    if args.controls:
        args.windows = args.gallery = True

    sessions = load_sessions(args.data, verbose=True)
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
    print("A headline number is only trustworthy once the confound battery below clears:")
    print("  the match must survive rate-equalization, sit well above the shuffled-label null,")
    print("  and (for the returning-visitor threat) hold on truly >=1-week-apart sessions.")
    if len(trackers) > 1:
        print("Compare cross_task_cross_session EER across trackers for the RQ3 ceiling-vs-commodity gap.")
    print()

    # Confound battery (A.3 / 1.3) — printed by default beside every headline; the
    # controls that decide whether a match is the person or the apparatus.
    if not args.no_battery:
        for tr in trackers:
            sub = [s for s in sessions if s["tracker"] == tr]
            if len(sub) < 2:
                continue
            confound_battery(sub, tr)

    # Heavier additive sweeps (opt-in), per tracker.
    if args.windows or args.gallery:
        for tr in trackers:
            sub = [s for s in sessions if s["tracker"] == tr]
            if len(sub) < 2:
                continue
            if args.windows:
                window_sweep(sub, tr)
            if args.gallery:
                gallery_sweep(sub, tr)

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
