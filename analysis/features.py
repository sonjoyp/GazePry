"""
Content-independent gaze features for re-identification.

Mirrors ../reid-core.js (repo root) so the offline analysis and the live demo agree.
Input: a session dict with `samples` = [{"t": ms, "x": px|None, "y": px|None}, ...]
and `screen` = {"innerW":.., "innerH":..}. Spatial features are normalised by
the screen diagonal, so they are resolution/device independent.

These are hand-crafted eye-movement biometric features (route (a) in the study
protocol): fixation/saccade statistics, rates, blink proxy, main-sequence slope.
"""
from __future__ import annotations
import math
from typing import List, Optional

VEL_THRESHOLD = 2.0   # screen-diagonal units / second (I-VT threshold)
MIN_FIX_MS = 80       # discard sub-80 ms fixations

FEATURE_NAMES = [
    "fix_dur_mean", "fix_dur_median", "fix_dur_std", "fix_dur_p90",
    "sacc_amp_mean", "sacc_amp_median", "sacc_amp_std", "sacc_amp_p90",
    "sacc_vel_mean", "sacc_vel_median", "sacc_vel_p90",
    "fix_rate", "sacc_rate", "fix_ratio", "gap_rate", "main_seq_slope",
]


def _mean(a: List[float]) -> float:
    return sum(a) / len(a) if a else 0.0


def _std(a: List[float]) -> float:
    if len(a) < 2:
        return 0.0
    m = _mean(a)
    return math.sqrt(_mean([(v - m) ** 2 for v in a]))


def _quantile(sorted_a: List[float], q: float) -> float:
    if not sorted_a:
        return 0.0
    pos = (len(sorted_a) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    if lo == hi:
        return sorted_a[lo]
    return sorted_a[lo] + (sorted_a[hi] - sorted_a[lo]) * (pos - lo)


def extract_features(samples: List[dict], screen: Optional[dict] = None) -> List[float]:
    screen = screen or {}
    diag = math.hypot(screen.get("innerW", 1920), screen.get("innerH", 1080)) or 1.0

    pts = []          # None for a gap, else (t, nx, ny)
    gaps = 0
    for s in samples:
        x, y = s.get("x"), s.get("y")
        if x is None or y is None:
            gaps += 1
            pts.append(None)
        else:
            pts.append((s["t"], x / diag, y / diag))

    fix_durs: List[float] = []
    sacc_amps: List[float] = []
    sacc_vels: List[float] = []
    n_fix_samples = 0
    n_valid = 0
    seq_amp: List[float] = []
    seq_peak_vel: List[float] = []

    run_prev = None
    cur_fix_start = None
    in_fix = False

    def close_fix(end_t):
        nonlocal in_fix, cur_fix_start
        if in_fix and cur_fix_start is not None and end_t is not None:
            d = end_t - cur_fix_start
            if d >= MIN_FIX_MS:
                fix_durs.append(d)
        in_fix = False
        cur_fix_start = None

    for p in pts:
        if p is None:
            close_fix(run_prev[0] if run_prev else None)
            run_prev = None
            continue
        n_valid += 1
        if run_prev is None:
            run_prev = p
            cur_fix_start = p[0]
            in_fix = True
            n_fix_samples += 1
            continue
        dt = (p[0] - run_prev[0]) / 1000.0
        if dt <= 0:
            run_prev = p
            continue
        amp = math.hypot(p[1] - run_prev[1], p[2] - run_prev[2])
        vel = amp / dt
        if vel >= VEL_THRESHOLD:
            close_fix(run_prev[0])
            sacc_amps.append(amp)
            sacc_vels.append(vel)
            seq_amp.append(amp)
            seq_peak_vel.append(vel)
        else:
            n_fix_samples += 1
            if not in_fix:
                in_fix = True
                cur_fix_start = run_prev[0]
        run_prev = p
    close_fix(run_prev[0] if run_prev else None)

    dur_s = (samples[-1]["t"] - samples[0]["t"]) / 1000.0 if samples else 1.0
    if dur_s <= 0:
        dur_s = 1.0

    # main-sequence slope: peak velocity ~ amplitude (least-squares slope)
    slope = 0.0
    if len(seq_amp) >= 3:
        ma, mv = _mean(seq_amp), _mean(seq_peak_vel)
        num = sum((a - ma) * (v - mv) for a, v in zip(seq_amp, seq_peak_vel))
        den = sum((a - ma) ** 2 for a in seq_amp)
        slope = num / den if den > 0 else 0.0

    fd = sorted(fix_durs)
    sa = sorted(sacc_amps)
    sv = sorted(sacc_vels)

    feat = {
        "fix_dur_mean": _mean(fix_durs),
        "fix_dur_median": _quantile(fd, 0.5),
        "fix_dur_std": _std(fix_durs),
        "fix_dur_p90": _quantile(fd, 0.9),
        "sacc_amp_mean": _mean(sacc_amps),
        "sacc_amp_median": _quantile(sa, 0.5),
        "sacc_amp_std": _std(sacc_amps),
        "sacc_amp_p90": _quantile(sa, 0.9),
        "sacc_vel_mean": _mean(sacc_vels),
        "sacc_vel_median": _quantile(sv, 0.5),
        "sacc_vel_p90": _quantile(sv, 0.9),
        "fix_rate": len(fix_durs) / dur_s,
        "sacc_rate": len(sacc_amps) / dur_s,
        "fix_ratio": (n_fix_samples / n_valid) if n_valid else 0.0,
        "gap_rate": gaps / dur_s,
        "main_seq_slope": slope,
    }
    return [feat[n] for n in FEATURE_NAMES]
