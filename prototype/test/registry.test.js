/*
 * Tests for the browser-side tracker orchestrator (gazepry-tracker.js) and the
 * self-registering adapters. The orchestrator is browser code, so we load it in
 * a `vm` sandbox with just enough of the DOM stubbed to exercise the pure logic:
 * the adapter registry, identity/tracker resolution, and the shipped adapters'
 * conformance to the contract. This is what guarantees a change to one adapter
 * (or to the picker) can't drop a tracker or mis-resolve the active one.
 */
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const PUBLIC = path.join(__dirname, "..", "public");
const FILES = [
  "gazepry-tracker.js",
  "trackers/webgazer.js",
  "trackers/gazecloud.js",
  "trackers/webeyetrack.js",
  "trackers/eyegestures.js",
];

// Load the orchestrator + adapters into a fresh sandbox and return window.GazePry.
// `store` seeds localStorage; `search` seeds location.search.
function loadGazePry(opts) {
  opts = opts || {};
  const store = Object.assign({}, opts.store);
  const sandbox = {
    window: {},
    console: { log() {}, warn() {}, error() {} },
    document: {
      currentScript: { src: "http://localhost/gazepry-tracker.js" },
      createElement: () => ({ style: {}, classList: { add() {}, remove() {} },
        addEventListener() {}, appendChild() {}, remove() {}, querySelector: () => ({}) }),
      head: { appendChild() {} }, body: { appendChild() {} }, addEventListener() {}, cookie: "",
    },
    performance: { now: () => 0 },
    location: { search: opts.search || "", href: "" },
    localStorage: {
      getItem: (k) => (k in store ? store[k] : null),
      setItem: (k, v) => { store[k] = String(v); },
      clear: () => { for (const k of Object.keys(store)) delete store[k]; },
    },
    sessionStorage: { clear() {} },
    screen: { width: 1440, height: 900 },
    navigator: { userAgent: "test" },
    URLSearchParams, setTimeout, setInterval, clearInterval, Promise,
    Blob: class {}, fetch: () => Promise.reject(new Error("no network in test")),
  };
  vm.createContext(sandbox);
  for (const f of FILES) {
    vm.runInContext(fs.readFileSync(path.join(PUBLIC, f), "utf8"), sandbox, { filename: f });
  }
  return { GazePry: sandbox.window.GazePry, store };
}

test("all four adapters register", () => {
  const { GazePry } = loadGazePry();
  // NB: arrays created inside the vm realm have a different Array.prototype, so
  // compare via a primitive (join) rather than deepStrictEqual.
  const fams = GazePry.listTrackers().map((t) => t.family).sort().join(",");
  assert.equal(fams, "eyegestures,gazecloud,webeyetrack,webgazer");
});

test("every adapter satisfies the minimum contract", () => {
  const { GazePry } = loadGazePry();
  for (const t of GazePry.listTrackers()) {
    assert.ok(t.family, "has family");
    assert.ok(t.label, `${t.family} has label`);
    assert.equal(typeof t.start, "function", `${t.family} has start()`);
    assert.equal(typeof t.onGaze, "function", `${t.family} has onGaze()`);
    assert.ok(["local", "cloud"].includes(t.privacy), `${t.family} declares privacy`);
    assert.equal(typeof t.available, "boolean");
    // An unavailable adapter must tell the user how to enable it.
    if (t.available === false) assert.ok(t.setup && t.setup.length > 10, `${t.family} has setup note`);
  }
});

test("shipped adapters carry the expected capability flags", () => {
  const { GazePry } = loadGazePry();
  const by = (f) => GazePry.getTracker(f);
  assert.equal(by("webgazer").available, true);
  assert.equal(by("webgazer").privacy, "local");
  assert.equal(by("webgazer").needsCalibration, true);

  assert.equal(by("gazecloud").available, true);
  assert.equal(by("gazecloud").privacy, "cloud", "GazeCloud is flagged cloud (frames leave the machine)");
  assert.equal(by("gazecloud").needsCalibration, false, "GazeCloud self-calibrates");

  // WebEyeTrack + EyeGestures are vendored (scripts/vendor-trackers.sh) and on-device.
  assert.equal(by("webeyetrack").available, true);
  assert.equal(by("webeyetrack").privacy, "local");
  assert.equal(by("webeyetrack").needsCalibration, true, "WebEyeTrack few-shot uses the click grid");

  assert.equal(by("eyegestures").available, true);
  assert.equal(by("eyegestures").privacy, "local");
  assert.equal(by("eyegestures").needsCalibration, false, "EyeGestures self-calibrates");
});

test("vendored tracker libraries are present on disk", () => {
  // The two adapters are only usable if scripts/vendor-trackers.sh has run.
  const need = [
    "lib/webeyetrack/webeyetrack.js",
    "web/model.json",
    "web/group1-shard1of1.bin",
    "lib/eyegestures/eyegestures.js",
    "lib/eyegestures/EyegesturesEngine.js",
    "lib/eyegestures/EyegesturesEngine_bg.wasm",
  ];
  for (const rel of need) {
    const p = path.join(PUBLIC, rel);
    assert.ok(fs.existsSync(p) && fs.statSync(p).size > 0,
      `${rel} missing or empty — run: bash scripts/vendor-trackers.sh`);
  }
});

test("registerTracker applies sensible defaults", () => {
  const { GazePry } = loadGazePry();
  GazePry.registerTracker({ family: "min", label: "Minimal", privacy: "local",
    start() {}, onGaze() {} });
  const t = GazePry.getTracker("min");
  assert.equal(t.available, true, "available defaults true");
  assert.equal(t.needsCalibration, true, "needsCalibration defaults true");
});

test("registerTracker rejects an adapter without a family", () => {
  const { GazePry } = loadGazePry();
  assert.throws(() => GazePry.registerTracker({ label: "no family" }), /family/);
});

test("loadIdentity defaults the tracker to webgazer", () => {
  const { GazePry } = loadGazePry();
  const id = GazePry.loadIdentity();
  assert.equal(id.tracker, "webgazer");
});

test("identity is read from the query string, then localStorage", () => {
  const fromQuery = loadGazePry({ search: "?participant=P09&session=S2&tracker=gazecloud" }).GazePry.loadIdentity();
  assert.deepEqual(
    { p: fromQuery.participant, s: fromQuery.session, t: fromQuery.tracker },
    { p: "P09", s: "S2", t: "gazecloud" }
  );
  const fromStore = loadGazePry({ store: { gp_participant: "P03", gp_session: "S1", gp_tracker: "eyegestures" } })
    .GazePry.loadIdentity();
  assert.equal(fromStore.participant, "P03");
  assert.equal(fromStore.tracker, "eyegestures");
});

test("saveIdentity persists participant/session/tracker", () => {
  const { GazePry, store } = loadGazePry();
  GazePry.saveIdentity("P42", "S3", "gazecloud");
  assert.equal(store.gp_participant, "P42");
  assert.equal(store.gp_session, "S3");
  assert.equal(store.gp_tracker, "gazecloud");
  assert.equal(GazePry.identity.tracker, "gazecloud");
});

test("resolveTracker follows the selected tracker and falls back safely", () => {
  const { GazePry } = loadGazePry();
  GazePry.loadIdentity();
  assert.equal(GazePry.resolveTracker().family, "webgazer", "default");
  GazePry.identity.tracker = "gazecloud";
  assert.equal(GazePry.resolveTracker().family, "gazecloud", "honours selection");
  GazePry.identity.tracker = "does-not-exist";
  assert.equal(GazePry.resolveTracker().family, "webgazer", "unknown -> default");
});

test("wipeState clears storage and the active tracker's model", () => {
  const { GazePry, store } = loadGazePry({ store: { gp_participant: "P01", keep: "x" } });
  let cleared = false;
  GazePry._active = { clearModel: () => { cleared = true; } };
  GazePry.wipeState();
  assert.equal(Object.keys(store).length, 0, "localStorage cleared");
  assert.equal(cleared, true, "active tracker model cleared");
});
