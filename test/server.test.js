/*
 * Integration tests for server.js — the zero-dependency collection + live re-ID
 * server. Spawns the real server against a throwaway data dir and drives every
 * endpoint over HTTP: ingest, status, sessions, identify, static serving, and
 * the tracker-threading / backward-compat rules (filenames carry the tracker
 * family; galleries never mix trackers; legacy records infer their family).
 */
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { spawn } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const SERVER = path.join(__dirname, "..", "server.js");
const SCREEN = { innerW: 1440, innerH: 900 };
const PORT = 8100 + Math.floor(Math.random() * 800);
const BASE = `http://localhost:${PORT}`;

let child;
let dataDir;
let labelsDir;

function fixations(spots) {
  let t = 0;
  const out = [];
  for (const [x, y, frames] of spots) {
    for (let i = 0; i < frames; i++) { out.push({ t, x, y }); t += 33; }
    t += 33; // saccade gap to the next fixation
  }
  return out;
}
const streamA = fixations([[200, 200, 8], [340, 250, 8], [250, 340, 8]]);
const streamB = fixations([[1000, 700, 12], [1120, 640, 12], [900, 760, 12]]);

function session(participant, sess, task, family, samples) {
  return {
    schema: "gazepry.session.v1", participant, session: sess, task,
    tracker: family + "-x", trackerFamily: family,
    startedAt: Date.now(), screen: SCREEN, nSamples: samples.length, samples,
  };
}
async function post(pathname, body) {
  const r = await fetch(BASE + pathname, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  });
  return { status: r.status, json: await r.json().catch(() => null) };
}
async function getJson(pathname) {
  const r = await fetch(BASE + pathname);
  return { status: r.status, json: await r.json().catch(() => null) };
}

test.before(async () => {
  dataDir = fs.mkdtempSync(path.join(os.tmpdir(), "gp-server-"));
  labelsDir = fs.mkdtempSync(path.join(os.tmpdir(), "gp-labels-"));
  child = spawn("node", [SERVER, "--port", String(PORT), "--data", dataDir,
    "--labels", labelsDir], { stdio: "ignore" });
  // wait for readiness
  const deadline = Date.now() + 8000;
  for (;;) {
    try { const r = await fetch(BASE + "/sessions"); if (r.ok) break; } catch (e) {}
    if (Date.now() > deadline) throw new Error("server did not start in time");
    await new Promise((res) => setTimeout(res, 100));
  }
});

test.after(() => {
  if (child) child.kill();
  if (dataDir) fs.rmSync(dataDir, { recursive: true, force: true });
  if (labelsDir) fs.rmSync(labelsDir, { recursive: true, force: true });
});

test("POST /ingest stores a file whose name carries the tracker family", async () => {
  const r = await post("/ingest", session("P01", "S1", "reading", "webgazer", streamA));
  assert.equal(r.status, 200);
  assert.match(r.json.stored, /^P01_S1_reading_webgazer_\d+\.json$/);
  assert.ok(fs.existsSync(path.join(dataDir, r.json.stored)));
});

test("POST /ingest rejects a record missing required fields", async () => {
  const r = await post("/ingest", { participant: "P01", session: "S1" }); // no task/samples
  assert.equal(r.status, 400);
  assert.ok(r.json.error);
});

test("POST /ingest infers the family for a legacy record (tracker id only)", async () => {
  const legacy = session("P07", "S1", "reading", "webgazer", streamA);
  delete legacy.trackerFamily;       // old record: only the full id survives
  legacy.tracker = "webgazer-3.5.3";
  const r = await post("/ingest", legacy);
  assert.equal(r.status, 200);
  assert.match(r.json.stored, /_webgazer_\d+\.json$/, "family inferred from 'webgazer-3.5.3'");
});

test("gallery is seeded across two trackers", async () => {
  // P01/P02 on webgazer; a distinct P09 on gazecloud (must not leak into webgazer).
  await post("/ingest", session("P02", "S1", "reading", "webgazer", streamB));
  await post("/ingest", session("P09", "S1", "reading", "gazecloud", streamA));
  const r = await getJson("/sessions");
  assert.ok(r.json.count >= 4);
  assert.deepEqual(r.json.trackers.sort(), ["gazecloud", "webgazer"]);
});

test("GET /sessions?tracker= filters to one tracker family", async () => {
  const wg = await getJson("/sessions?tracker=webgazer");
  assert.ok(wg.json.sessions.every((s) => s.tracker === "webgazer"));
  assert.ok(!wg.json.participants.includes("P09"), "gazecloud-only participant absent from webgazer view");
  const gc = await getJson("/sessions?tracker=gazecloud");
  assert.deepEqual(gc.json.participants, ["P09"]);
});

test("GET /status is scoped by participant/session/tracker", async () => {
  const r = await getJson("/status?participant=P01&session=S1&tracker=webgazer");
  assert.ok(r.json.tasks.includes("reading"));
  const other = await getJson("/status?participant=P01&session=S1&tracker=gazecloud");
  assert.deepEqual(other.json.tasks, [], "no P01 sessions under gazecloud");
});

test("POST /identify ranks within the same tracker only", async () => {
  const r = await post("/identify", {
    samples: streamB, screen: SCREEN, tracker: "webgazer",
    excludeParticipant: "P02", excludeSession: "S1", // exclude the enrolment we copied
  });
  assert.equal(r.status, 200);
  assert.equal(r.json.tracker, "webgazer");
  assert.ok(!r.json.galleryParticipants.includes("P09"), "cross-tracker entry not in the gallery");
  // With P02/S1 excluded, the remaining webgazer people are P01/P07 — a real ranking still returns.
  assert.ok(r.json.ranked.length >= 1);
});

test("POST /identify against a self-copy returns the right person (no exclude)", async () => {
  const r = await post("/identify", { samples: streamB, screen: SCREEN, tracker: "webgazer" });
  assert.equal(r.json.rank1, "P02", "probe copied from P02's stream matches P02");
});

test("D7 probe sessions are ingested but kept OUT of the re-ID gallery", async () => {
  // Probe sessions share the data dir with D4 sessions. Their gaze stream is
  // chopped into 4 s trials driven by an adversary-chosen stimulus, so a
  // whole-session dynamics vector over one would describe the trial structure
  // rather than the person — it must never become gallery material.
  const probe = {
    schema: "gazepry.probe.v1",
    participant: "PX9", session: "S1", task: "probe",
    tracker: "webgazer-3.5.3", trackerFamily: "webgazer",
    experiment: "E1", arrayN: 4, coverTask: "memory-adjacent", awareness: "naive",
    counterbalanceGroup: 1, startedAt: Date.now(), screen: SCREEN,
    clockAnchored: true, nTrials: 1,
    trials: [{ index: 0, probeItemId: "abs00", onsetT: 0, offsetT: 400, aois: [] }],
    nSamples: streamA.length, samples: streamA,
  };
  const ing = await post("/ingest", probe);
  assert.equal(ing.status, 200, "a probe session must still be accepted and stored");
  assert.ok(fs.existsSync(path.join(dataDir, ing.json.stored)));

  const s = await getJson("/sessions");
  assert.ok(!s.json.participants.includes("PX9"), "probe participant leaked into /sessions");
  assert.ok(!s.json.sessions.some((e) => e.task === "probe"), "probe task leaked into the gallery");

  const st = await getJson("/status?participant=PX9&session=S1&tracker=webgazer");
  assert.deepEqual(st.json.tasks, [], "probe completion is not tracked via the re-ID gallery");

  const id = await post("/identify", { samples: streamA, screen: SCREEN, tracker: "webgazer" });
  assert.ok(!id.json.galleryParticipants.includes("PX9"), "probe entry became identifiable");
});

test("POST /labels stores questionnaire responses OUTSIDE the gaze data dir", async () => {
  // Service usage and topic exposure are exactly what the D7 attack extracts,
  // so they are the most sensitive artefact the study holds. They must not land
  // in data/, where a bulk copy or `git add data/` would sweep them along.
  const rec = {
    schema: "gazepry.labels.v1", participant: "P42", session: "S1", experiment: "E2",
    collectedAt: Date.now(),
    items: [{ itemId: "mail", response: 3 }, { itemId: "vid", response: 0 }],
  };
  const r = await post("/labels", rec);
  assert.equal(r.status, 200);
  assert.equal(r.json.answered, 2);
  assert.ok(!fs.existsSync(path.join(dataDir, r.json.stored)), "labels leaked into the gaze dir");
  assert.ok(fs.existsSync(path.join(labelsDir, r.json.stored)));
});

test("POST /labels rejects an empty or malformed response set", async () => {
  const base = { schema: "gazepry.labels.v1", participant: "P43", session: "S1", experiment: "E2" };
  assert.equal((await post("/labels", base)).status, 400, "missing items");
  assert.equal((await post("/labels", { ...base, items: [] })).status, 400, "no items");
  assert.equal((await post("/labels", { ...base, items: [{ itemId: "mail" }] })).status, 400,
    "an all-unanswered questionnaire must not be accepted as data");
});

test("GET /probe-status reports trials, quality flags and questionnaire state", async () => {
  const mkProbe = (participant, experiment, over) => ({
    schema: "gazepry.probe.v1", participant, session: "S1", task: "probe",
    tracker: "webgazer-3.5.3", trackerFamily: "webgazer",
    experiment, arrayN: 4, coverTask: "memory-adjacent", awareness: "naive",
    counterbalanceGroup: 1, startedAt: Date.now(), screen: SCREEN,
    clockAnchored: true, nTrials: 2, nSamples: 400, nGaps: 10,
    trials: [{ index: 0, onsetT: 0, offsetT: 4000, aois: [] },
             { index: 1, onsetT: 5000, offsetT: 9000, aois: [] }],
    samples: streamA,
    ...over,
  });

  await post("/ingest", mkProbe("PQ1", "E1"));                              // clean
  await post("/ingest", mkProbe("PQ2", "E1", { clockAnchored: false }));    // unscorable
  await post("/ingest", mkProbe("PQ3", "E1", { nSamples: 60 }));            // starved
  await post("/ingest", mkProbe("PQ4", "E1", { nSamples: 400, nGaps: 300 })); // face lost
  await post("/ingest", mkProbe("PQ5", "E2"));                             // needs labels

  const s = await getJson("/probe-status");
  assert.equal(s.status, 200);
  const by = Object.fromEntries(s.json.sessions.map((x) => [x.participant, x]));

  assert.equal(by.PQ1.usable, true);
  assert.deepEqual(by.PQ1.problems, []);
  assert.equal(by.PQ1.nTrials, 2);

  assert.equal(by.PQ2.usable, false);
  assert.match(by.PQ2.problems.join(" "), /clock anchor/);
  assert.equal(by.PQ3.usable, false, "60 samples over 2 trials is starved");
  assert.equal(by.PQ4.usable, false, "75% gaps must be flagged");

  // E2 needs a questionnaire; E1 does not.
  assert.equal(by.PQ5.needsLabels, true);
  assert.equal(by.PQ5.hasLabels, false);
  assert.equal(by.PQ1.needsLabels, false);

  await post("/labels", {
    schema: "gazepry.labels.v1", participant: "PQ5", session: "S1", experiment: "E2",
    collectedAt: Date.now(), items: [{ itemId: "mail", response: 2 }],
  });
  const s2 = await getJson("/probe-status?participant=PQ5");
  assert.equal(s2.json.sessions.length, 1, "participant filter applies");
  assert.equal(s2.json.sessions[0].hasLabels, true, "questionnaire not picked up");
});

test("/probe-status never exposes raw gaze samples", async () => {
  const s = await getJson("/probe-status");
  const body = JSON.stringify(s.json);
  assert.ok(!body.includes("\"samples\""), "the console payload must stay metadata-only");
});

test("GET / serves the hub and path traversal is blocked", async () => {
  const home = await fetch(BASE + "/");
  assert.equal(home.status, 200);
  assert.match(await home.text(), /GazePry/);
  // Encoded so the client can't normalise the "../" away before it reaches the
  // server's own path-traversal guard.
  const bad = await fetch(BASE + "/%2e%2e/server.js");
  assert.ok([403, 404].includes(bad.status), "traversal outside public/ refused");
  assert.doesNotMatch(await bad.text().catch(() => ""), /createServer/, "server.js source not leaked");
});
