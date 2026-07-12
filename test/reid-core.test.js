/*
 * Unit tests for reid-core.js — the content-independent gaze features and the
 * nearest-neighbour matcher that back the live re-ID demo. These pin the feature
 * contract (16 named features, screen-normalised, fixation/saccade segmentation)
 * and the ranking behaviour so a refactor can't silently change either.
 */
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("path");
const reid = require(path.join(__dirname, "..", "reid-core"));

const SCREEN = { innerW: 1440, innerH: 900 };

// Build a stream of `frames` steady points at (x,y), ~30 Hz, starting at t0.
function fixation(x, y, frames, t0) {
  const s = [];
  for (let i = 0; i < frames; i++) s.push({ t: t0 + i * 33, x, y });
  return s;
}
// A reading-like stream: alternating fixations joined by single-frame saccades.
function scanStream(scale) {
  scale = scale || 1;
  const spots = [[200, 200], [800, 300], [400, 600], [900, 650], [300, 400]];
  let t = 0;
  let out = [];
  for (const [x, y] of spots) {
    const fx = fixation(x * scale, y * scale, 8, t); // ~264 ms fixation
    out = out.concat(fx);
    t = fx[fx.length - 1].t + 33; // next point one frame later = the saccade step
  }
  return out;
}

test("FEATURE_NAMES has 16 entries and extractFeatures matches its length", () => {
  assert.equal(reid.FEATURE_NAMES.length, 16);
  const f = reid.extractFeatures(scanStream(), SCREEN);
  assert.equal(f.length, 16);
  assert.ok(f.every((v) => typeof v === "number" && Number.isFinite(v)), "all features finite");
});

test("empty / all-gap streams do not throw and return a full vector", () => {
  assert.equal(reid.extractFeatures([], SCREEN).length, 16);
  const gaps = [{ t: 0, x: null, y: null }, { t: 33, x: null, y: null }];
  const f = reid.extractFeatures(gaps, SCREEN);
  assert.equal(f.length, 16);
  assert.ok(f.every(Number.isFinite));
});

test("a pure fixation has saccade features = 0 but a positive fixation rate", () => {
  const f = reid.extractFeatures(fixation(500, 500, 30, 0), SCREEN);
  const idx = (n) => reid.FEATURE_NAMES.indexOf(n);
  assert.equal(f[idx("sacc_amp_mean")], 0, "no saccades");
  assert.equal(f[idx("sacc_rate")], 0);
  assert.ok(f[idx("fix_dur_mean")] > 0, "fixation duration measured");
  assert.ok(f[idx("fix_ratio")] > 0.9, "almost all samples are fixation");
});

test("a scan stream produces real saccades", () => {
  const f = reid.extractFeatures(scanStream(), SCREEN);
  const idx = (n) => reid.FEATURE_NAMES.indexOf(n);
  assert.ok(f[idx("sacc_amp_mean")] > 0, "saccade amplitude detected");
  assert.ok(f[idx("sacc_vel_mean")] > 0, "saccade velocity detected");
  assert.ok(f[idx("sacc_rate")] > 0);
});

test("gaps are counted into gap_rate", () => {
  const withGaps = fixation(400, 400, 10, 0)
    .concat([{ t: 350, x: null, y: null }, { t: 383, x: null, y: null }])
    .concat(fixation(400, 400, 10, 420));
  const f = reid.extractFeatures(withGaps, SCREEN);
  assert.ok(f[reid.FEATURE_NAMES.indexOf("gap_rate")] > 0, "gap rate positive when blinks present");
});

test("spatial features are screen-normalised (scale-invariant)", () => {
  // Same motion at 2x pixels on a 2x screen -> identical normalised features.
  const f1 = reid.extractFeatures(scanStream(1), { innerW: 1440, innerH: 900 });
  const f2 = reid.extractFeatures(scanStream(2), { innerW: 2880, innerH: 1800 });
  for (let i = 0; i < f1.length; i++) {
    assert.ok(Math.abs(f1[i] - f2[i]) < 1e-9, `feature ${reid.FEATURE_NAMES[i]} invariant to resolution`);
  }
});

test("resample decimates a fast stream toward the target cadence, preserving gaps", () => {
  const fast = [];
  for (let i = 0; i < 200; i++) fast.push({ t: i * 10, x: 500, y: 500 }); // 2 s @ 100 Hz
  const out = reid.resample(fast, 30);
  assert.ok(out.length < fast.length, "stream is thinned");
  const hz = (out.length) / ((out[out.length - 1].t - out[0].t) / 1000);
  assert.ok(Math.abs(hz - 30) < 6, "resampled cadence is near 30 Hz");
  // a gap survives
  const withGap = fixation(200, 200, 30, 0)
    .concat([{ t: 1000, x: null, y: null }])
    .concat(fixation(400, 400, 30, 1040));
  assert.ok(reid.resample(withGap, 30).some((p) => p.x === null), "a gap survives resampling");
});

test("resample is a no-op when hz is falsy or the stream is too short", () => {
  const s = fixation(100, 100, 10, 0);
  assert.equal(reid.resample(s, 0), s, "hz falsy returns the same stream");
  const one = [{ t: 0, x: 1, y: 1 }];
  assert.equal(reid.resample(one, 30), one, "<2 samples returns the same stream");
});

test("standardize z-scores columns and guards zero-variance columns", () => {
  const std = reid.standardize([[0, 5], [2, 5], [4, 5]]);
  assert.deepEqual(std.mu, [2, 5]);
  assert.equal(std.sd[1], 1, "zero-variance column sd forced to 1 (no divide-by-zero)");
  // column 0 is centred: mean of z ~ 0
  const zcol0 = std.z.map((r) => r[0]);
  assert.ok(Math.abs(zcol0.reduce((a, b) => a + b, 0)) < 1e-9);
  // constant column -> all z = 0
  assert.ok(std.z.every((r) => r[1] === 0));
});

test("identify ranks the matching participant first", () => {
  const mk = (participant, session, vec) => ({ participant, session, task: "reading", features: vec });
  const base = new Array(16).fill(0);
  const p1 = base.map((_, i) => i);          // 0..15
  const p2 = base.map((_, i) => i + 100);    // 100..115  (clearly separated)
  const gallery = [mk("P01", "S1", p1), mk("P02", "S1", p2)];
  const probe = p2.slice();                  // identical to P02
  const res = reid.identify(probe, gallery, {});
  assert.equal(res.rank1, "P02");
  assert.equal(res.ranked[0].participant, "P02");
  assert.ok(res.ranked[0].score <= res.ranked[1].score, "ranked ascending by distance");
});

test("identify honours excludeParticipant+excludeSession", () => {
  const mk = (participant, session, vec) => ({ participant, session, task: "reading", features: vec });
  const p1 = new Array(16).fill(0);
  const p2 = new Array(16).fill(100);
  const gallery = [mk("P01", "S1", p1), mk("P02", "S1", p2)];
  const probe = p2.slice();
  // Excluding the only P02 session must make the match fall to P01.
  const res = reid.identify(probe, gallery, { excludeParticipant: "P02", excludeSession: "S1" });
  assert.equal(res.rank1, "P01");
});

test("identify on an empty gallery returns rank1 null", () => {
  const res = reid.identify(new Array(16).fill(0), [], {});
  assert.equal(res.rank1, null);
  assert.deepEqual(res.ranked, []);
});
