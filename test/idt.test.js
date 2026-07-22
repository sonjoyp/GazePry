/*
 * Unit tests for the I-DT dispersion-threshold fixation detector in reid-core.js
 * (Direction D7). Fixation DURATION is the measure the CIT literature reports as
 * surviving deliberate concealment, so it is the one D7 leans on hardest —
 * which makes the segmentation that produces it worth pinning precisely.
 */
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("path");
const reid = require(path.join(__dirname, "..", "reid-core"));

const SCREEN = { innerW: 1920, innerH: 1080 };
const DIAG = Math.hypot(1920, 1080);

// steady point, ~60 Hz
function steady(x, y, ms, t0) {
  const s = [];
  for (let t = 0; t < ms; t += 16) s.push({ t: t0 + t, x, y });
  return s;
}
// deterministic pseudo-noise so the test never flakes
function noisy(x, y, ms, t0, sigma, seed) {
  const rnd = (function (a) {
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  })(seed);
  const s = [];
  for (let t = 0; t < ms; t += 16) {
    // Box-Muller-ish: sum of uniforms is close enough to normal for a test
    const gx = (rnd() + rnd() + rnd() - 1.5) * 2 * sigma;
    const gy = (rnd() + rnd() + rnd() - 1.5) * 2 * sigma;
    s.push({ t: t0 + t, x: x + gx, y: y + gy });
  }
  return s;
}

test("a clean steady dwell is one fixation with the right duration", () => {
  const f = reid.detectFixationsIDT(steady(500, 400, 600, 0), SCREEN);
  assert.equal(f.length, 1);
  assert.ok(Math.abs(f[0].durMs - 592) <= 20, "duration " + f[0].durMs);
  assert.ok(Math.abs(f[0].x - 500) < 1 && Math.abs(f[0].y - 400) < 1);
  assert.ok(f[0].n > 10);
});

test("two separated dwells give two fixations", () => {
  const s = steady(300, 300, 500, 0).concat(steady(1400, 800, 500, 600));
  const f = reid.detectFixationsIDT(s, SCREEN);
  assert.equal(f.length, 2);
  assert.ok(f[0].x < 500 && f[1].x > 1200);
});

test("a dwell shorter than the minimum is not a fixation", () => {
  const f = reid.detectFixationsIDT(steady(500, 400, 60, 0), SCREEN);
  assert.equal(f.length, 0);
});

test("a gap splits a dwell instead of fusing it", () => {
  const s = steady(500, 400, 400, 0)
    .concat([{ t: 420, x: null, y: null }, { t: 440, x: null, y: null }])
    .concat(steady(500, 400, 400, 460));
  const f = reid.detectFixationsIDT(s, SCREEN);
  assert.equal(f.length, 2, "a blink must not merge two fixations into one long one");
});

test("continuous drift across the screen is not reported as a fixation", () => {
  const s = [];
  for (let i = 0; i < 120; i++) s.push({ t: i * 16, x: 100 + i * 14, y: 100 + i * 8 });
  const f = reid.detectFixationsIDT(s, SCREEN, { smoothWin: 1 });
  for (const fx of f) {
    assert.ok(fx.durMs < 400, "a long sweep was classified as a fixation: " + fx.durMs);
  }
});

test("the threshold is in screen-diagonal units (resolution independent)", () => {
  // Same relative geometry on two screen sizes must segment the same way.
  const big = reid.detectFixationsIDT(steady(960, 540, 500, 0), { innerW: 1920, innerH: 1080 });
  const small = reid.detectFixationsIDT(steady(480, 270, 500, 0), { innerW: 960, innerH: 540 });
  assert.equal(big.length, small.length);
});

test("REGRESSION: a lab-grade threshold finds nothing in webcam-noise data", () => {
  // This is the bug that silently zeroed every fixation feature during the
  // build: at ~1.4 deg webcam error the raw cloud of a real fixation already
  // exceeds a 0.045-diag threshold, so I-DT returns nothing and the downstream
  // features all become constants that report AUC 0.500 — indistinguishable
  // from "no effect". Pinned so the defaults can't drift back.
  const sigma = 0.03 * DIAG; // ~66 px, a realistic webcam per-sample error
  const s = noisy(900, 500, 800, 0, sigma, 99);
  const lab = reid.detectFixationsIDT(s, SCREEN, { dispersion: 0.045, smoothWin: 1 });
  assert.equal(lab.length, 0, "lab threshold unexpectedly found fixations — update the note in reid-core.js");
  const tuned = reid.detectFixationsIDT(s, SCREEN);
  assert.ok(tuned.length >= 1, "the shipped defaults must recover the dwell, got " + tuned.length);
});

test("smoothing reduces fragmentation of a noisy dwell", () => {
  const sigma = 0.02 * DIAG;
  const s = noisy(900, 500, 900, 0, sigma, 4242);
  const raw = reid.detectFixationsIDT(s, SCREEN, { smoothWin: 1 });
  const sm = reid.detectFixationsIDT(s, SCREEN, { smoothWin: 5 });
  const dur = (a) => a.reduce((t, f) => t + f.durMs, 0);
  assert.ok(dur(sm) >= dur(raw), "smoothing should recover at least as much dwell time");
});

test("empty and all-gap input yield no fixations rather than throwing", () => {
  assert.deepEqual(reid.detectFixationsIDT([], SCREEN), []);
  assert.deepEqual(
    reid.detectFixationsIDT([{ t: 0, x: null, y: null }, { t: 16, x: null, y: null }], SCREEN),
    []
  );
});

test("fixations are ordered and non-overlapping", () => {
  const s = steady(200, 200, 400, 0)
    .concat(steady(1500, 300, 400, 500))
    .concat(steady(800, 900, 400, 1000));
  const f = reid.detectFixationsIDT(s, SCREEN);
  for (let i = 1; i < f.length; i++) {
    assert.ok(f[i].tStart >= f[i - 1].tEnd, "fixations overlap or are out of order");
  }
});

test("the detector is exported with its tunables", () => {
  assert.equal(typeof reid.detectFixationsIDT, "function");
  assert.equal(typeof reid.DISP_THRESHOLD, "number");
  assert.equal(typeof reid.IDT_MIN_FIX_MS, "number");
  assert.equal(typeof reid.IDT_SMOOTH_WIN, "number");
});
