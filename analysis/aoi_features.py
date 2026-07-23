"""
AOI-anchored per-trial features for Direction D7 (recognition leakage).

See GazePry_D7_Recognition_Knowledge_Direction.md §7.1-§7.2. Unlike the
content-*independent* 16-D vector in features.py (which describes a whole
session's oculomotor dynamics), these features are computed **per trial, per
AOI**, and every one of them is either coarse-spatial (which tile) or purely
temporal (how long a fixation lasted). Nothing here needs sub-degree pointing,
which is what keeps the direction inside the webcam envelope.

Two design decisions carry most of the weight:

1. **Soft AOI assignment** (§7.1). With 2-4 deg of angular error, hard
   nearest-tile assignment throws away the samples that land in the gap between
   tiles and biases the ones near an edge. Each gaze sample instead contributes
   to every AOI with a Gaussian weight, whose bandwidth is estimated per
   participant from their own calibration residual when available. Hard
   assignment is kept as a reported contrast, not deleted -- if the effect only
   survives under soft assignment, that has to be visible.

2. **Within-trial relative scaling** (§7.2). Every feature is expressed
   relative to the trial's own AOI mean. That cancels per-participant and
   per-session scale differences, including differences in logged sample cadence
   between trackers, because all AOIs in a trial were captured through the same
   sensor in the same second.
"""
from __future__ import annotations

import math
import os
import sys
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from features import detect_fixations_idt  # noqa: E402

# Pre-registered scoring windows (§6.3). The familiarity effect can REVERSE
# sign between an early orienting phase and a later one, so the windows are
# scored separately and never averaged together. These bounds come from the
# CIT literature's reported phase split (~0.7-2 s early), not from the data.
EARLY_WINDOW_MS = (700.0, 2000.0)
LATE_WINDOW_MS = (2000.0, 4000.0)

# Soft-assignment bandwidth as a fraction of the screen diagonal, used when a
# session carries no calibration residual to estimate it from. ~2.5 deg.
DEFAULT_SIGMA_FRAC = 0.05

FEATURE_NAMES = [
    "dwell_prop",            # share of trial gaze time on this AOI
    "dwell_prop_early",      # ... within the early window
    "dwell_prop_late",       # ... within the late window
    "fix_count",             # number of fixations centred on this AOI
    "fix_dur_mean",          # mean fixation duration (countermeasure-resistant)
    "fix_dur_first",         # duration of the FIRST fixation on this AOI
    "first_fix_rank",        # 0 = looked at first; -1 if never fixated
    "time_to_first_ms",      # latency to first fixation on this AOI
    "revisits",              # number of separate visits after the first
    "entropy_share",         # this AOI's contribution to scanpath entropy
]


# ---- geometry -------------------------------------------------------------
def _rect_center(rect: dict):
    return rect["x"] + rect["w"] / 2.0, rect["y"] + rect["h"] / 2.0


def _in_rect(x: float, y: float, rect: dict) -> bool:
    return (rect["x"] <= x <= rect["x"] + rect["w"] and
            rect["y"] <= y <= rect["y"] + rect["h"])


def aoi_weights(x: float, y: float, aois: List[dict], sigma: float,
                soft: bool = True) -> List[float]:
    """Weight of a gaze point against each AOI.

    Soft: Gaussian on the distance to the AOI centre, normalised to sum to 1.
    Hard: 1.0 for the containing rect, else 1.0 for the nearest centre.

    Returns all-zero weights only when ``soft`` is True and every AOI is
    astronomically far away, which cannot happen for finite sigma -- so a
    caller can treat a zero-sum result as a bug rather than a data condition.
    """
    if not aois:
        return []
    if not soft:
        w = [0.0] * len(aois)
        for i, a in enumerate(aois):
            if _in_rect(x, y, a["rect"]):
                w[i] = 1.0
                return w
        # nothing contains it: fall back to nearest centre
        best, bd = 0, float("inf")
        for i, a in enumerate(aois):
            cx, cy = _rect_center(a["rect"])
            d = (x - cx) ** 2 + (y - cy) ** 2
            if d < bd:
                best, bd = i, d
        w[best] = 1.0
        return w

    raw = []
    for a in aois:
        cx, cy = _rect_center(a["rect"])
        d2 = (x - cx) ** 2 + (y - cy) ** 2
        raw.append(math.exp(-d2 / (2.0 * sigma * sigma)))
    tot = sum(raw)
    if tot <= 0:
        # numerically underflowed: assign fully to the nearest centre
        return aoi_weights(x, y, aois, sigma, soft=False)
    return [r / tot for r in raw]


def sigma_for(session: dict) -> float:
    """Soft-assignment bandwidth in pixels for one session.

    Prefers a per-participant estimate from the calibration residual the harness
    records; falls back to DEFAULT_SIGMA_FRAC of the screen diagonal. The
    fallback is reported by callers rather than applied silently, because a
    bandwidth that does not reflect the participant's actual tracker error is a
    modelling assumption, not a measurement.
    """
    screen = session.get("screen") or {}
    diag = math.hypot(screen.get("innerW", 1920), screen.get("innerH", 1080)) or 1.0
    resid = (session.get("condition") or {}).get("calibResidualPx")
    if resid:
        try:
            r = float(resid)
            if r > 0:
                return r
        except (TypeError, ValueError):
            pass
    return DEFAULT_SIGMA_FRAC * diag


# ---- per-trial extraction -------------------------------------------------
def trial_samples(samples: List[dict], onset_t, offset_t) -> List[dict]:
    """Samples falling inside one trial's array-presentation window."""
    if onset_t is None or offset_t is None:
        return []
    return [s for s in samples if onset_t <= s["t"] <= offset_t]


def extract_trial(session: dict, trial: dict, soft: bool = True,
                  sigma: Optional[float] = None) -> Optional[List[dict]]:
    """Per-AOI feature rows for one trial.

    Returns None when the trial cannot be scored (no clock anchor, empty
    window, no valid gaze) rather than emitting zero-filled rows -- a
    zero-filled row is indistinguishable from "looked nowhere", which is a
    real and different observation.
    """
    aois = trial.get("aois") or []
    if len(aois) < 2:
        return None
    onset, offset = trial.get("onsetT"), trial.get("offsetT")
    win = trial_samples(session.get("samples") or [], onset, offset)
    if len(win) < 5:
        return None
    if sigma is None:
        sigma = sigma_for(session)

    screen = session.get("screen") or {}
    n = len(aois)

    # --- dwell, from raw samples weighted across AOIs -----------------------
    dwell = [0.0] * n
    dwell_early = [0.0] * n
    dwell_late = [0.0] * n
    n_valid = 0
    for i in range(len(win) - 1):
        s, nxt = win[i], win[i + 1]
        if s.get("x") is None or s.get("y") is None:
            continue
        dt = nxt["t"] - s["t"]
        if dt <= 0 or dt > 250:      # a >250 ms step means a dropout, not dwell
            continue
        n_valid += 1
        rel = s["t"] - onset
        w = aoi_weights(s["x"], s["y"], aois, sigma, soft)
        for j in range(n):
            dwell[j] += w[j] * dt
            if EARLY_WINDOW_MS[0] <= rel < EARLY_WINDOW_MS[1]:
                dwell_early[j] += w[j] * dt
            elif LATE_WINDOW_MS[0] <= rel < LATE_WINDOW_MS[1]:
                dwell_late[j] += w[j] * dt
    if n_valid < 5:
        return None

    def _props(vals):
        tot = sum(vals)
        return [v / tot for v in vals] if tot > 0 else [0.0] * n

    p_all, p_early, p_late = _props(dwell), _props(dwell_early), _props(dwell_late)

    # --- fixation-derived features -----------------------------------------
    fixations = detect_fixations_idt(win, screen)
    fix_owner = []       # index of the AOI each fixation is attributed to
    for f in fixations:
        w = aoi_weights(f["x"], f["y"], aois, sigma, soft)
        fix_owner.append(max(range(n), key=lambda j: w[j]))

    counts = [0] * n
    durs: List[List[float]] = [[] for _ in range(n)]
    first_rank = [-1] * n
    first_lat = [None] * n
    visits = [0] * n
    prev_owner = None
    for rank, (f, owner) in enumerate(zip(fixations, fix_owner)):
        counts[owner] += 1
        durs[owner].append(f["durMs"])
        if first_rank[owner] < 0:
            first_rank[owner] = rank
            first_lat[owner] = f["tStart"] - onset
        if owner != prev_owner:
            visits[owner] += 1
        prev_owner = owner

    # scanpath entropy contribution: -p*log2(p) over fixation-count shares
    tot_fix = sum(counts)
    ent_share = []
    for c in counts:
        p = (c / tot_fix) if tot_fix else 0.0
        ent_share.append(-p * math.log(p, 2) if p > 0 else 0.0)

    # trial duration used to normalise the "never fixated" latency sentinel
    trial_ms = (offset - onset) if (offset is not None and onset is not None) else 4000.0

    rows = []
    for j, a in enumerate(aois):
        rows.append({
            "participant": session.get("participant"),
            "sessionId": session.get("session"),
            "experiment": session.get("experiment"),
            "tracker": session.get("trackerFamily"),
            "arrayN": session.get("arrayN"),
            "coverTask": session.get("coverTask"),
            "awareness": session.get("awareness"),
            "counterbalanceGroup": session.get("counterbalanceGroup"),
            "delayCondition": session.get("delayCondition"),
            "trial": trial.get("index"),
            "slot": a.get("slot", j),
            "itemId": a.get("itemId"),
            "familiar": bool(a.get("familiar")),
            "features": {
                "dwell_prop": p_all[j],
                "dwell_prop_early": p_early[j],
                "dwell_prop_late": p_late[j],
                "fix_count": float(counts[j]),
                "fix_dur_mean": (sum(durs[j]) / len(durs[j])) if durs[j] else 0.0,
                "fix_dur_first": durs[j][0] if durs[j] else 0.0,
                "first_fix_rank": float(first_rank[j]),
                # never fixated -> the full trial elapsed without a look, which
                # is the honest encoding of "later than any observed latency"
                "time_to_first_ms": float(first_lat[j]) if first_lat[j] is not None else float(trial_ms),
                "revisits": float(max(0, visits[j] - 1)),
                "entropy_share": ent_share[j],
            },
        })
    return rows


def relativise(rows: List[dict]) -> List[dict]:
    """Express each AOI's features relative to its own trial's AOI mean (section 7.2).

    Additive for features that are already proportions or counts; the point is
    that a constant offset shared by every AOI in a trial (sensor drift, a
    sleepy participant, a slow logging cadence) cancels.
    """
    if not rows:
        return rows
    n = len(rows)
    out = []
    for r in rows:
        rel = {}
        for k in FEATURE_NAMES:
            m = sum(x["features"][k] for x in rows) / n
            rel[k] = r["features"][k] - m
        c = dict(r)
        c["rel"] = rel
        out.append(c)
    return out


def extract_session(session: dict, soft: bool = True) -> List[dict]:
    """All scorable per-AOI rows for one probe session, relativised per trial."""
    if session.get("schema") != "gazepry.probe.v1":
        return []
    if not session.get("clockAnchored", True):
        return []          # trial marks were never mapped onto the sample clock
    sigma = sigma_for(session)
    out: List[dict] = []
    for trial in session.get("trials") or []:
        rows = extract_trial(session, trial, soft=soft, sigma=sigma)
        if rows:
            out.extend(relativise(rows))
    return out


def design_matrix(rows: List[dict], relative: bool = True):
    """(X, y, groups, items) as plain lists -- numpy is applied by the caller."""
    key = "rel" if relative else "features"
    X = [[r[key][k] for k in FEATURE_NAMES] for r in rows]
    y = [1 if r["familiar"] else 0 for r in rows]
    groups = [r["participant"] for r in rows]
    items = [r["itemId"] for r in rows]
    return X, y, groups, items
