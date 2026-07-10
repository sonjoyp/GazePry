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

// Extract a fixed-length feature vector from one session's samples.
function extractFeatures(samples, screen) {
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
  extractFeatures: extractFeatures,
  identify: identify,
  standardize: standardize,
};
