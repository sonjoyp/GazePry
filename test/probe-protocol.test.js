/*
 * Unit tests for public/probe-protocol.js — the Direction D7 trial protocol.
 *
 * The counterbalancing tests are the important ones. D7's whole claim to having
 * escaped the D4 person-vs-apparatus confound rests on "every item is familiar
 * for half the participants, and slot position carries no information". If that
 * silently breaks, the direction's RQ0 gate is measuring nothing and every
 * downstream number is unfalsifiable — so it is pinned here rather than trusted.
 */
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("path");
const P = require(path.join(__dirname, "..", "public", "probe-protocol.js"));

const PIDS = Array.from({ length: 40 }, (_, i) => "P" + String(i + 1).padStart(2, "0"));

test("PRNG is deterministic and in range", () => {
  const a = P.mulberry32(12345);
  const b = P.mulberry32(12345);
  for (let i = 0; i < 200; i++) {
    const v = a();
    assert.equal(v, b());
    assert.ok(v >= 0 && v < 1, "value out of [0,1)");
  }
  assert.notEqual(P.mulberry32(1)(), P.mulberry32(2)());
});

test("hashSeed is stable and 32-bit", () => {
  assert.equal(P.hashSeed("P01"), P.hashSeed("P01"));
  assert.notEqual(P.hashSeed("P01"), P.hashSeed("P02"));
  for (const s of ["", "P01", "abcdef", "long-participant-id-0001"]) {
    const h = P.hashSeed(s);
    assert.ok(Number.isInteger(h) && h >= 0 && h <= 0xffffffff);
  }
});

test("counterbalance groups are perfectly balanced for numbered participants", () => {
  const counts = new Map();
  for (const p of PIDS) {
    const g = P.groupFor(p);
    assert.ok(g >= 0 && g < P.N_GROUPS);
    counts.set(g, (counts.get(g) || 0) + 1);
  }
  assert.equal(counts.size, P.N_GROUPS);
  const vals = [...counts.values()];
  assert.equal(Math.max(...vals) - Math.min(...vals), 0,
    "numbered IDs must spread evenly — uneven groups leak item identity into familiarity");
});

test("non-numeric participant ids still get a group (hash fallback)", () => {
  const g = P.groupFor("pilot-alpha");
  assert.ok(Number.isInteger(g) && g >= 0 && g < P.N_GROUPS);
});

test("each item is familiar for exactly half the counterbalance groups", () => {
  for (const expId of ["E1", "E2", "E3"]) {
    const items = P.SETS[expId].items;
    for (let i = 0; i < items.length; i++) {
      let n = 0;
      for (let g = 0; g < P.N_GROUPS; g++) if (P.isFamiliar(i, g)) n++;
      assert.equal(n, P.N_GROUPS / 2,
        `${expId} item ${i} familiar for ${n}/${P.N_GROUPS} groups`);
    }
  }
});

test("across a full cohort every item takes both roles about equally", () => {
  // The confound that matters: if an intrinsically eye-catching item were
  // ALWAYS the familiar one, its salience would masquerade as recognition.
  const seen = new Map(); // itemId -> [nFamiliar, nTotal]
  for (const p of PIDS) {
    const built = P.buildTrials({ participant: p, experiment: "E1", arrayN: 4, nTrials: 40 });
    for (const tr of built.trials) {
      for (const s of tr.slots) {
        const e = seen.get(s.itemId) || [0, 0];
        e[0] += s.familiar ? 1 : 0;
        e[1] += 1;
        seen.set(s.itemId, e);
      }
    }
  }
  for (const [id, [nf, nt]] of seen) {
    const frac = nf / nt;
    // A probe fills 1 of 4 slots, so the expected familiar share is ~0.25;
    // what must NOT happen is an item locked to one role.
    assert.ok(frac > 0.1 && frac < 0.45, `item ${id} familiar share ${frac.toFixed(3)} is lopsided`);
  }
});

test("slot position carries no familiarity information", () => {
  const bySlot = new Map();
  for (const p of PIDS) {
    const built = P.buildTrials({ participant: p, experiment: "E1", arrayN: 4, nTrials: 40 });
    for (const tr of built.trials) {
      for (const s of tr.slots) {
        const e = bySlot.get(s.slot) || [0, 0];
        e[0] += s.familiar ? 1 : 0;
        e[1] += 1;
        bySlot.set(s.slot, e);
      }
    }
  }
  const fracs = [...bySlot.values()].map(([nf, nt]) => nf / nt);
  assert.equal(fracs.length, 4);
  assert.ok(Math.max(...fracs) - Math.min(...fracs) < 0.05,
    `familiarity varies by slot: ${fracs.map((f) => f.toFixed(3)).join(", ")}`);
});

test("every trial has exactly one probe among arrayN slots", () => {
  for (const arrayN of [2, 4]) {
    for (const expId of ["E1", "E2", "E3"]) {
      const built = P.buildTrials({ participant: "P07", experiment: expId, arrayN, nTrials: 25 });
      assert.equal(built.trials.length, 25);
      for (const tr of built.trials) {
        assert.equal(tr.slots.length, arrayN);
        const fam = tr.slots.filter((s) => s.familiar);
        assert.equal(fam.length, 1, "exactly one familiar item per trial");
        assert.equal(fam[0].itemId, tr.probeItemId);
        const ids = new Set(tr.slots.map((s) => s.itemId));
        assert.equal(ids.size, arrayN, "no repeated item within a trial");
      }
    }
  }
});

test("trial plans are reproducible from the participant id alone", () => {
  const a = P.buildTrials({ participant: "P12", experiment: "E2", arrayN: 4, nTrials: 20 });
  const b = P.buildTrials({ participant: "P12", experiment: "E2", arrayN: 4, nTrials: 20 });
  assert.deepEqual(
    a.trials.map((t) => t.slots.map((s) => [s.itemId, s.familiar])),
    b.trials.map((t) => t.slots.map((s) => [s.itemId, s.familiar]))
  );
  const c = P.buildTrials({ participant: "P13", experiment: "E2", arrayN: 4, nTrials: 20 });
  assert.notDeepEqual(a.trials[0].slots.map((s) => s.itemId), c.trials[0].slots.map((s) => s.itemId));
});

test("probe items are cycled, not sampled with replacement", () => {
  const built = P.buildTrials({ participant: "P03", experiment: "E1", arrayN: 4, nTrials: 36 });
  const counts = new Map();
  for (const tr of built.trials) counts.set(tr.probeItemId, (counts.get(tr.probeItemId) || 0) + 1);
  const vals = [...counts.values()];
  assert.ok(Math.max(...vals) - Math.min(...vals) <= 1,
    "probe usage should be near-uniform, got " + vals.join(","));
});

test("studySet returns exactly the familiar-role items", () => {
  const plan = { participant: "P05", experiment: "E1", arrayN: 4, nTrials: 40 };
  const study = P.studySet(plan);
  const built = P.buildTrials(plan);
  const famIds = new Set();
  built.trials.forEach((t) => t.slots.forEach((s) => { if (s.familiar) famIds.add(s.itemId); }));
  assert.deepEqual(new Set(study.map((i) => i.id)), famIds);
  assert.ok(study.length > 0);
});

test("layout honours the validated geometry and flags undersized viewports", () => {
  const big = P.layout(4, 1920, 1080);
  assert.equal(big.rects.length, 4);
  assert.ok(big.ok, "1920x1080 should satisfy the envelope");
  assert.ok(big.tileW >= P.GEOM.minTileW && big.tileH >= P.GEOM.minTileH);
  // tiles must not overlap, and the gap must be preserved
  assert.ok(big.rects[1].x - (big.rects[0].x + big.rects[0].w) >= P.GEOM.minGap - 1);
  assert.ok(big.rects[2].y - (big.rects[0].y + big.rects[0].h) >= P.GEOM.minGap - 1);

  const small = P.layout(4, 1024, 640);
  assert.equal(small.ok, false, "a small viewport must be refused, not silently shrunk");
});

test("stimulus sets are big enough for a 4-tile array and have unique ids", () => {
  for (const expId of ["E1", "E2", "E3"]) {
    const items = P.SETS[expId].items;
    assert.ok(items.length >= 8, expId + " too small");
    assert.equal(new Set(items.map((i) => i.id)).size, items.length, expId + " has duplicate ids");
  }
});

test("E3 contains no protected-characteristic topics", () => {
  // The direction deliberately scopes E3 to health/finance/legal/civic
  // (D7 §6.5). This asserts that scoping so it cannot drift in later.
  const allowed = new Set(["health", "finance", "legal", "civic"]);
  for (const it of P.SETS.E3.items) {
    assert.ok(allowed.has(it.category), "unexpected E3 category: " + it.category);
  }
});
