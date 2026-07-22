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


def resample(samples: List[dict], hz: Optional[float]) -> List[dict]:
    """Decimate a sample stream to an approximately uniform ``hz`` cadence by
    picking, for each target tick, the sample whose timestamp is nearest. Gaps
    (``x`` is None) are preserved. Returns the list unchanged when ``hz`` is
    falsy or there are <2 samples.

    Rationale: WebGazer logs at requestAnimationFrame cadence (~50–120 Hz here),
    and that rate differs across participants/sessions. Rate-sensitive features
    (saccade velocity, the various rates, the main-sequence slope) then encode
    *capture cadence* as much as the eye, which is a re-ID confound perfectly
    correlated with identity in the pilot. Equalizing the cadence before feature
    extraction removes that confound. This must stay byte-identical to
    ``reid-core.js`` ``resample()`` — the JS↔Py parity test covers it.
    """
    if not hz or len(samples) < 2:
        return samples
    step = 1000.0 / hz
    t0 = samples[0]["t"]
    t_end = samples[-1]["t"]
    out: List[dict] = []
    j = 0
    n = len(samples)
    t = float(t0)
    while t <= t_end + 1e-9:
        while j + 1 < n and abs(samples[j + 1]["t"] - t) <= abs(samples[j]["t"] - t):
            j += 1
        out.append(samples[j])
        t += step
    return out


# ---- I-DT dispersion-threshold fixation detection (Direction D7) ----------
# The I-VT threshold above is velocity-based and coarse at webcam rates. D7's
# load-bearing feature is fixation *duration* (the measure that survives
# concealment -- Schwedes & Wentura 2012; Millen & Hancock 2019), so it needs a
# segmentation algorithm that is stable at ~30 Hz. Thilderkvist & Dobslaw 2024
# introduced a dispersion-threshold algorithm precisely because none existed for
# low-frequency webcam data; this is that family (Salvucci & Goldberg I-DT).
# Must stay byte-identical to reid-core.js detectFixationsIDT() -- the JS<->Py
# parity test covers it.
#
# The threshold is in screen-diagonal units (resolution independent); returned
# centroids are in VIEWPORT PIXELS, because AOI assignment is done in pixels.
#
# PARAMETERS ARE SET BY THE SENSOR, NOT BY TASTE. A lab-grade default (~0.045
# diag, about 1.5-2 deg) finds ZERO fixations in commodity webcam data: at a
# realistic 1.4 deg accuracy / ~50-70 px per-sample error (Kaduk et al. 2024),
# the raw point cloud of a genuine fixation already spans more than that. Two
# consequences, both deliberate:
#   1. SMOOTH FIRST. A short centred moving average over the run cuts per-sample
#      noise by ~sqrt(smooth_win) before dispersion is measured. Smoothing never
#      crosses a gap, so a blink cannot fuse two fixations into one.
#   2. The default threshold is set relative to the TILE, not the fovea. D7
#      scores whole-tile AOIs (~700 px apart), so "sustained looking at one
#      tile" is the object of interest; a threshold that resolves within-tile
#      structure is both unattainable and unnecessary here.
# Both are exposed so the analysis can report sensitivity rather than hiding a
# tuned constant. See test_analysis.py::TestIDT::test_zero_fixations_at_lab_threshold.
DISP_THRESHOLD = 0.10    # screen-diagonal units, tile-scale (see above)
IDT_MIN_FIX_MS = 100
IDT_SMOOTH_WIN = 5       # samples; 1 disables smoothing


def _smooth_run(run, win):
    """Centred moving average over one gap-free run; timestamps untouched."""
    if not win or win < 2 or len(run) < 2:
        return run
    h, n = win // 2, len(run)
    out = []
    for i in range(n):
        a, b = max(0, i - h), min(n - 1, i + h)
        c = b - a + 1
        sx = sum(run[k][1] for k in range(a, b + 1))
        sy = sum(run[k][2] for k in range(a, b + 1))
        out.append((run[i][0], sx / c, sy / c))
    return out


def _dispersion(run, i: int, j: int) -> float:
    min_x = max_x = run[i][1]
    min_y = max_y = run[i][2]
    for k in range(i + 1, j + 1):
        x, y = run[k][1], run[k][2]
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
    return (max_x - min_x) + (max_y - min_y)


def detect_fixations_idt(samples: List[dict], screen: Optional[dict] = None,
                         dispersion: Optional[float] = None,
                         min_dur_ms: Optional[float] = None,
                         smooth_win: Optional[int] = None) -> List[dict]:
    """Segment a gaze stream into fixations by dispersion threshold.

    Returns ``[{"tStart","tEnd","durMs","x","y","n"}, ...]`` with ``x``/``y`` the
    centroid in viewport pixels. A gap (``x`` is None) ends a candidate window,
    so a blink never merges two fixations into one long one.
    """
    screen = screen or {}
    diag = math.hypot(screen.get("innerW", 1920), screen.get("innerH", 1080)) or 1.0
    thresh = (DISP_THRESHOLD if dispersion is None else dispersion) * diag
    min_dur = IDT_MIN_FIX_MS if min_dur_ms is None else min_dur_ms
    sm = IDT_SMOOTH_WIN if smooth_win is None else smooth_win

    runs: List[list] = []
    cur: list = []
    for s in samples:
        x, y = s.get("x"), s.get("y")
        if x is None or y is None:
            if cur:
                runs.append(cur)
                cur = []
            continue
        cur.append((s["t"], x, y))
    if cur:
        runs.append(cur)

    fixations: List[dict] = []
    for raw_run in runs:
        run = _smooth_run(raw_run, sm)
        a, n = 0, len(run)
        while a < n:
            b = a
            while b + 1 < n and run[b][0] - run[a][0] < min_dur:
                b += 1
            if run[b][0] - run[a][0] < min_dur:
                break
            if _dispersion(run, a, b) > thresh:
                a += 1
                continue
            while b + 1 < n and _dispersion(run, a, b + 1) <= thresh:
                b += 1
            cnt = b - a + 1
            sx = sum(run[k][1] for k in range(a, b + 1))
            sy = sum(run[k][2] for k in range(a, b + 1))
            fixations.append({
                "tStart": run[a][0], "tEnd": run[b][0],
                "durMs": run[b][0] - run[a][0],
                "x": sx / cnt, "y": sy / cnt, "n": cnt,
            })
            a = b + 1
    return fixations


def extract_features(samples: List[dict], screen: Optional[dict] = None,
                     resample_hz: Optional[float] = None) -> List[float]:
    if resample_hz:
        samples = resample(samples, resample_hz)
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
