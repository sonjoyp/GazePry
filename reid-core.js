/*
 * reid-core.js — content-independent gaze features + nearest-neighbour
 * matching, used by the Node server for the LIVE re-identification demo.
 *
 * The authoritative evaluation for the paper is analysis/reid.py; this is a
 * faithful JS port of the same feature definitions so the interactive demo
 * and the offline analysis agree. Keep the two in sync if you change features.
 *
 * Input: raw sample stream [{t, x, y}] where x/y are viewport pixels and a
 * gap is encoded as x=null. Spatial features are normalised by the screen
 * diagonal so they are resolution/device independent.
 */
"use strict";

// I-VT-style velocity threshold, in screen-diagonal units per second.
// Coarse at ~30 Hz webcam rates; expose for tuning against real data.
var VEL_THRESHOLD = 2.0;
var MIN_FIX_MS = 80; // discard sub-80 ms "fixations" (noise)

function quantile(sorted, q) {
  if (!sorted.length) return 0;
  var pos = (sorted.length - 1) * q;
  var lo = Math.floor(pos), hi = Math.ceil(pos);
  if (lo === hi) return sorted[lo];
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
}
function mean(a) { return a.length ? a.reduce(function (s, v) { return s + v; }, 0) / a.length : 0; }
function std(a) {
  if (a.length < 2) return 0;
  var m = mean(a);
  return Math.sqrt(mean(a.map(function (v) { return (v - m) * (v - m); })));
}

var FEATURE_NAMES = [
  "fix_dur_mean", "fix_dur_median", "fix_dur_std", "fix_dur_p90",
  "sacc_amp_mean", "sacc_amp_median", "sacc_amp_std", "sacc_amp_p90",
  "sacc_vel_mean", "sacc_vel_median", "sacc_vel_p90",
  "fix_rate", "sacc_rate", "fix_ratio", "gap_rate", "main_seq_slope",
];

// Decimate a sample stream to an approximately uniform `hz` cadence by picking,
// for each target tick, the sample whose timestamp is nearest. Gaps (x=null) are
// preserved; returns the stream unchanged when hz is falsy or <2 samples.
//
// WebGazer logs at requestAnimationFrame cadence (~50–120 Hz), and that rate
// differs across participants/sessions — so rate-sensitive features encode
// capture cadence as much as the eye (a re-ID confound). Equalizing cadence
// before extraction removes it. Keep byte-identical to analysis/features.py
// resample() — the JS↔Py parity test covers it.
function resample(samples, hz) {
  if (!hz || samples.length < 2) return samples;
  var step = 1000 / hz;
  var t0 = samples[0].t, tEnd = samples[samples.length - 1].t;
  var out = [], j = 0, n = samples.length, t = t0;
  while (t <= tEnd + 1e-9) {
    while (j + 1 < n && Math.abs(samples[j + 1].t - t) <= Math.abs(samples[j].t - t)) j++;
    out.push(samples[j]);
    t += step;
  }
  return out;
}

// ---- I-DT dispersion-threshold fixation detection (Direction D7) --------
// The I-VT threshold above is velocity-based and coarse at webcam rates. D7's
// load-bearing feature is fixation *duration* (it is the measure that survives
// concealment — Schwedes & Wentura 2012; Millen & Hancock 2019), so it needs a
// segmentation algorithm that is stable at ~30 Hz. Thilderkvist & Dobslaw 2024
// introduced a dispersion-threshold algorithm precisely because none existed
// for low-frequency webcam data; this is that family (Salvucci & Goldberg
// I-DT). Keep byte-identical to analysis/features.py detect_fixations_idt() —
// the JS<->Py parity test covers it.
//
// Threshold is in screen-diagonal units so it is resolution independent;
// returned centroids are in VIEWPORT PIXELS because AOI assignment is in pixels.
//
// PARAMETERS ARE SET BY THE SENSOR, NOT BY TASTE. A lab-grade default (~0.045
// diag, about 1.5-2 deg) finds ZERO fixations in commodity webcam data: at a
// realistic 1.4 deg accuracy / ~50-70 px per-sample error (Kaduk et al. 2024),
// the raw point cloud of a genuine fixation already spans more than that. Two
// consequences, both deliberate:
//   1. SMOOTH FIRST. A short centred moving average over the run cuts the
//      per-sample noise by ~sqrt(smoothWin) before dispersion is measured.
//      Smoothing never crosses a gap, so a blink cannot fuse two fixations.
//   2. The default threshold is set relative to the TILE, not the fovea. D7
//      scores whole-tile AOIs (~700 px apart), so "sustained looking at one
//      tile" is the object of interest; a threshold that resolves within-tile
//      structure is both unattainable and unnecessary here.
// Both are exposed so the analysis can report sensitivity rather than hiding a
// tuned constant.
var DISP_THRESHOLD = 0.10;  // screen-diagonal units, tile-scale (see above)
var IDT_MIN_FIX_MS = 100;
var IDT_SMOOTH_WIN = 5;     // samples; 1 disables smoothing

// Centred moving average over one gap-free run. Returns a new array; the
// timestamps are untouched.
function _smoothRun(run, win) {
  if (!win || win < 2 || run.length < 2) return run;
  var h = Math.floor(win / 2), n = run.length, out = new Array(n);
  for (var i = 0; i < n; i++) {
    var a = Math.max(0, i - h), b = Math.min(n - 1, i + h);
    var sx = 0, sy = 0;
    for (var k = a; k <= b; k++) { sx += run[k].x; sy += run[k].y; }
    var c = b - a + 1;
    out[i] = { t: run[i].t, x: sx / c, y: sy / c };
  }
  return out;
}

function _dispersion(run, i, j) {
  var minX = run[i].x, maxX = run[i].x, minY = run[i].y, maxY = run[i].y;
  for (var k = i + 1; k <= j; k++) {
    if (run[k].x < minX) minX = run[k].x;
    if (run[k].x > maxX) maxX = run[k].x;
    if (run[k].y < minY) minY = run[k].y;
    if (run[k].y > maxY) maxY = run[k].y;
  }
  return (maxX - minX) + (maxY - minY);
}

function detectFixationsIDT(samples, screen, opts) {
  opts = opts || {};
  screen = screen || {};
  var diag = Math.sqrt(
    Math.pow(screen.innerW || 1920, 2) + Math.pow(screen.innerH || 1080, 2)
  ) || 1;
  var thresh = (opts.dispersion == null ? DISP_THRESHOLD : opts.dispersion) * diag;
  var minDur = opts.minDurMs == null ? IDT_MIN_FIX_MS : opts.minDurMs;
  var smoothWin = opts.smoothWin == null ? IDT_SMOOTH_WIN : opts.smoothWin;

  // split into runs of consecutive valid samples (a gap ends a candidate)
  var runs = [], cur = [];
  for (var i = 0; i < samples.length; i++) {
    var s = samples[i];
    if (s.x == null || s.y == null) { if (cur.length) { runs.push(cur); cur = []; } continue; }
    cur.push({ t: s.t, x: s.x, y: s.y });
  }
  if (cur.length) runs.push(cur);

  var fixations = [];
  for (var r = 0; r < runs.length; r++) {
    var run = _smoothRun(runs[r], smoothWin);
    var a = 0, n = run.length;
    while (a < n) {
      // grow to the minimum duration
      var b = a;
      while (b + 1 < n && run[b].t - run[a].t < minDur) b++;
      if (run[b].t - run[a].t < minDur) break; // not enough samples left
      if (_dispersion(run, a, b) > thresh) { a++; continue; }
      // extend while it stays a fixation
      while (b + 1 < n && _dispersion(run, a, b + 1) <= thresh) b++;
      var sx = 0, sy = 0;
      for (var k = a; k <= b; k++) { sx += run[k].x; sy += run[k].y; }
      var cnt = b - a + 1;
      fixations.push({
        tStart: run[a].t, tEnd: run[b].t, durMs: run[b].t - run[a].t,
        x: sx / cnt, y: sy / cnt, n: cnt,
      });
      a = b + 1;
    }
  }
  return fixations;
}

// Extract a fixed-length feature vector from one session's samples.
function extractFeatures(samples, screen, resampleHz) {
  if (resampleHz) samples = resample(samples, resampleHz);
  screen = screen || {};
  var diag = Math.sqrt(
    Math.pow(screen.innerW || 1920, 2) + Math.pow(screen.innerH || 1080, 2)
  ) || 1;

  // segment on gaps: build runs of consecutive valid points with times
  var pts = [];
  var gaps = 0;
  for (var i = 0; i < samples.length; i++) {
    var s = samples[i];
    if (s.x == null || s.y == null) { gaps++; pts.push(null); continue; }
    pts.push({ t: s.t, x: s.x / diag, y: s.y / diag });
  }

  // point-to-point velocities within valid consecutive pairs
  // classify each interior point as fixation (slow) or saccade (fast)
  var fixDurs = [];
  var saccAmps = [];
  var saccVels = [];
  var nFixSamples = 0, nValid = 0;

  var runStartT = null, runPrev = null, curFixStartT = null, inFix = false;
  var seqAmp = [], seqPeakVel = []; // for main-sequence slope

  function closeFix(endT) {
    if (inFix && curFixStartT != null && endT != null) {
      var d = endT - curFixStartT;
      if (d >= MIN_FIX_MS) fixDurs.push(d);
    }
    inFix = false; curFixStartT = null;
  }

  for (var j = 0; j < pts.length; j++) {
    var p = pts[j];
    if (p == null) { closeFix(runPrev ? runPrev.t : null); runPrev = null; continue; }
    nValid++;
    if (runPrev == null) { runPrev = p; curFixStartT = p.t; inFix = true; nFixSamples++; continue; }
    var dt = (p.t - runPrev.t) / 1000;
    if (dt <= 0) { runPrev = p; continue; }
    var amp = Math.hypot(p.x - runPrev.x, p.y - runPrev.y);
    var vel = amp / dt;
    if (vel >= VEL_THRESHOLD) {
      // saccade step
      closeFix(runPrev.t);
      saccAmps.push(amp);
      saccVels.push(vel);
      seqAmp.push(amp); seqPeakVel.push(vel);
    } else {
      nFixSamples++;
      if (!inFix) { inFix = true; curFixStartT = runPrev.t; }
    }
    runPrev = p;
  }
  closeFix(runPrev ? runPrev.t : null);

  var durS = samples.length ? (samples[samples.length - 1].t - samples[0].t) / 1000 : 1;
  if (durS <= 0) durS = 1;

  // main-sequence slope: peak velocity ~ amplitude (least squares slope)
  var slope = 0;
  if (seqAmp.length >= 3) {
    var ma = mean(seqAmp), mv = mean(seqPeakVel), num = 0, den = 0;
    for (var k = 0; k < seqAmp.length; k++) {
      num += (seqAmp[k] - ma) * (seqPeakVel[k] - mv);
      den += (seqAmp[k] - ma) * (seqAmp[k] - ma);
    }
    slope = den > 0 ? num / den : 0;
  }

  var fdSorted = fixDurs.slice().sort(function (a, b) { return a - b; });
  var saSorted = saccAmps.slice().sort(function (a, b) { return a - b; });
  var svSorted = saccVels.slice().sort(function (a, b) { return a - b; });

  var f = {
    fix_dur_mean: mean(fixDurs),
    fix_dur_median: quantile(fdSorted, 0.5),
    fix_dur_std: std(fixDurs),
    fix_dur_p90: quantile(fdSorted, 0.9),
    sacc_amp_mean: mean(saccAmps),
    sacc_amp_median: quantile(saSorted, 0.5),
    sacc_amp_std: std(saccAmps),
    sacc_amp_p90: quantile(saSorted, 0.9),
    sacc_vel_mean: mean(saccVels),
    sacc_vel_median: quantile(svSorted, 0.5),
    sacc_vel_p90: quantile(svSorted, 0.9),
    fix_rate: fixDurs.length / durS,
    sacc_rate: saccAmps.length / durS,
    fix_ratio: nValid ? nFixSamples / nValid : 0,
    gap_rate: gaps / durS,
    main_seq_slope: slope,
  };
  return FEATURE_NAMES.map(function (n) { return f[n]; });
}

// Standardise a matrix of vectors column-wise; returns {mu, sd, z}.
function standardize(vectors) {
  var d = vectors[0] ? vectors[0].length : 0;
  var mu = new Array(d).fill(0), sd = new Array(d).fill(0);
  for (var c = 0; c < d; c++) {
    var col = vectors.map(function (v) { return v[c]; });
    mu[c] = mean(col);
    sd[c] = std(col) || 1;
  }
  var z = vectors.map(function (v) { return v.map(function (x, c) { return (x - mu[c]) / sd[c]; }); });
  return { mu: mu, sd: sd, z: z };
}
function applyStd(v, mu, sd) { return v.map(function (x, c) { return (x - mu[c]) / sd[c]; }); }
function euclid(a, b) {
  var s = 0;
  for (var i = 0; i < a.length; i++) s += (a[i] - b[i]) * (a[i] - b[i]);
  return Math.sqrt(s);
}

/*
 * Rank gallery participants for a probe.
 *   gallery: [{participant, session, task, features:[...]}]
 *   probeFeatures: [...]
 * Returns [{participant, score, task, session}] ascending by distance
 * (nearest gallery session per participant), plus rank-1 participant.
 */
function identify(probeFeatures, gallery, opts) {
  opts = opts || {};
  var pool = gallery.filter(function (g) {
    if (opts.excludeParticipant && g.participant === opts.excludeParticipant &&
        opts.excludeSession && g.session === opts.excludeSession) return false;
    return true;
  });
  if (!pool.length) return { ranked: [], rank1: null };

  var std = standardize(pool.map(function (g) { return g.features; }));
  var zProbe = applyStd(probeFeatures, std.mu, std.sd);

  var best = {}; // participant -> {score, task, session}
  pool.forEach(function (g, i) {
    var dist = euclid(zProbe, std.z[i]);
    if (!(g.participant in best) || dist < best[g.participant].score) {
      best[g.participant] = { participant: g.participant, score: dist, task: g.task, session: g.session };
    }
  });
  var ranked = Object.keys(best).map(function (p) { return best[p]; })
    .sort(function (a, b) { return a.score - b.score; });
  return { ranked: ranked, rank1: ranked.length ? ranked[0].participant : null };
}

module.exports = {
  FEATURE_NAMES: FEATURE_NAMES,
  VEL_THRESHOLD: VEL_THRESHOLD,
  DISP_THRESHOLD: DISP_THRESHOLD,
  IDT_MIN_FIX_MS: IDT_MIN_FIX_MS,
  IDT_SMOOTH_WIN: IDT_SMOOTH_WIN,
  extractFeatures: extractFeatures,
  detectFixationsIDT: detectFixationsIDT,
  resample: resample,
  identify: identify,
  standardize: standardize,
};
