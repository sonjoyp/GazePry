/*
 * probe-protocol.js — stimulus sets and the counterbalanced trial builder for
 * Direction D7 (recognition & concealed-knowledge leakage).
 *
 * See GazePry_D7_Recognition_Knowledge_Direction.md §6.2–§6.5. This module is
 * the single source of truth for *what is shown and in what role*, so the task
 * page, the simulator, and the tests all agree.
 *
 * THE CORE CONTROL (§6.4, RQ0). Every item appears as `familiar` for half the
 * participants and `unfamiliar` for the other half, assigned by a Latin square
 * over `counterbalanceGroup`. Item saliency, colour, and semantic category are
 * therefore held constant across the familiarity contrast, and screen position
 * is randomised per trial. Without this the whole direction is unfalsifiable:
 * a classifier could separate "familiar" from "unfamiliar" purely on which
 * pictures they are.
 *
 * Runs unmodified in the browser (window.ProbeProtocol) and in Node
 * (module.exports) so the tests and the simulator use the same code as the
 * task page.
 */
(function (root, factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.ProbeProtocol = api;
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // ---- deterministic PRNG ------------------------------------------------
  // mulberry32: small, fast, and identical in JS and the Python port, so a
  // participant's trial order is reproducible from their ID alone. Never use
  // Math.random() here — an unreproducible trial order cannot be re-analysed.
  function mulberry32(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // FNV-1a over a string -> 32-bit seed. Same participant id => same sequence.
  function hashSeed(str) {
    var h = 2166136261 >>> 0;
    str = String(str);
    for (var i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = Math.imul(h, 16777619) >>> 0;
    }
    return h >>> 0;
  }

  function shuffled(arr, rnd) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(rnd() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  // ---- stimulus sets -----------------------------------------------------
  // Items are rendered as procedural SVG (no external assets, CSP-safe, and no
  // third-party logos vendored into the repo). `label` is what the participant
  // sees; `hue`/`glyph` drive the drawing. For a real E2 run the brand set is
  // swapped for actual screenshots — see STIMULUS_NOTES below.
  var SETS = {
    // E1 — lab-installed familiarity. Abstract, meaningless shapes: the
    // participant can have NO pre-existing exposure, so familiarity is created
    // entirely by the study phase and ground truth is perfect (§6.5 E1).
    E1: {
      id: "E1",
      label: "Lab-installed familiarity",
      studyPhase: true,
      items: makeAbstractItems(24),
    },
    // E2 — naturally acquired familiarity. Placeholder brand-like marks; the
    // familiarity label comes from the POST-HOC questionnaire, never from this
    // table (§6.5 E2). `familiar` here is only the counterbalance *assignment*
    // used for E1-style analysis; for E2 the analysis uses `selfReport`.
    E2: {
      id: "E2",
      label: "Real-world service familiarity",
      studyPhase: false,
      selfReportLabels: true,
      items: makeBrandItems(),
    },
    // E3 — topic exposure. Content cards; consented self-report labels only.
    // NO protected characteristics (§6.5 E3) — health/finance/legal/civic only.
    E3: {
      id: "E3",
      label: "Sensitive-topic exposure",
      studyPhase: false,
      selfReportLabels: true,
      items: makeTopicItems(),
    },
  };

  function makeAbstractItems(n) {
    var out = [];
    for (var i = 0; i < n; i++) {
      out.push({
        id: "abs" + (i < 10 ? "0" : "") + i,
        label: "",
        kind: "abstract",
        hue: Math.round((360 / n) * i),
        glyph: i % 6,
        seed: 1009 + i * 37,
      });
    }
    return out;
  }

  function makeBrandItems() {
    // Neutral placeholder marks standing in for real services. The point of the
    // set is that penetration VARIES across it, so `tier` records the expected
    // prevalence band used for the A.7-style fallback ("high-salience only").
    var defs = [
      ["mail", "Mailbox", "high"], ["vid", "Streamline", "high"],
      ["shop", "Marketplace", "high"], ["soc", "Circle", "high"],
      ["map", "Wayfind", "high"], ["news", "Dispatch", "medium"],
      ["bank", "Ledger", "medium"], ["fit", "Stride", "medium"],
      ["code", "Forge", "medium"], ["note", "Sheaf", "medium"],
      ["trav", "Compass", "low"], ["food", "Larder", "low"],
      ["game", "Arcade", "low"], ["learn", "Tutor", "low"],
      ["photo", "Album", "low"], ["music", "Chord", "low"],
    ];
    return defs.map(function (d, i) {
      return { id: d[0], label: d[1], kind: "brand", tier: d[2],
        hue: (i * 47) % 360, glyph: i % 6, seed: 3001 + i * 53 };
    });
  }

  function makeTopicItems() {
    var defs = [
      ["t_sleep", "Sleep problems", "health"], ["t_diab", "Blood sugar", "health"],
      ["t_ment", "Therapy options", "health"], ["t_derm", "Skin conditions", "health"],
      ["t_debt", "Debt consolidation", "finance"], ["t_mort", "Mortgage rates", "finance"],
      ["t_pens", "Retirement planning", "finance"], ["t_tax", "Tax deductions", "finance"],
      ["t_tenc", "Tenant rights", "legal"], ["t_will", "Making a will", "legal"],
      ["t_emp", "Employment disputes", "legal"], ["t_imm", "Visa paperwork", "legal"],
      ["t_vote", "Voter registration", "civic"], ["t_coun", "Local council", "civic"],
      ["t_recy", "Recycling rules", "civic"], ["t_perm", "Building permits", "civic"],
    ];
    return defs.map(function (d, i) {
      return { id: d[0], label: d[1], kind: "topic", category: d[2],
        hue: (i * 31 + 200) % 360, glyph: i % 6, seed: 5003 + i * 71 };
    });
  }

  // ---- counterbalancing --------------------------------------------------
  // N_GROUPS Latin-square groups. Item i is `familiar` for group g iff
  // ((i + g) mod N_GROUPS) < N_GROUPS/2 — so across a full set of groups each
  // item is familiar exactly half the time, and each participant sees a
  // balanced mix. Group is derived from the participant id (stable), not from
  // recruitment order (which would correlate with time of day, cohort, etc.).
  var N_GROUPS = 4;

  // Prefer the participant NUMBER over a hash. Sequentially numbered IDs
  // (P01, P02, ...) then land in the four groups perfectly evenly, which
  // matters more than it looks: with a hash, group sizes drift apart at small
  // N, the per-item marginal probability of "familiar" stops being 0.5 across
  // the cohort, and item identity starts carrying information about
  // familiarity — which is exactly what the RQ0 saliency baseline is supposed
  // to find at chance. Hash is the fallback for non-numeric IDs.
  function groupFor(participant) {
    var m = String(participant).match(/(\d+)\s*$/);
    if (m) return parseInt(m[1], 10) % N_GROUPS;
    return hashSeed("cb:" + participant) % N_GROUPS;
  }

  function isFamiliar(itemIndex, group) {
    return ((itemIndex + group) % N_GROUPS) < N_GROUPS / 2;
  }

  /*
   * Build the full trial list for one participant.
   *
   *   opts = { participant, experiment:"E1"|"E2"|"E3", arrayN:2|4,
   *            nTrials, group? }
   *
   * Each trial pairs exactly ONE familiar-role item (the probe) with
   * (arrayN-1) unfamiliar-role items (the irrelevants), which is the
   * array-CIT structure of Nahari 2019 [C2] and Schwedes & Wentura 2012 [C1].
   * Slot order is randomised per trial so screen position carries no
   * information about familiarity.
   */
  function buildTrials(opts) {
    opts = opts || {};
    var participant = opts.participant || "P00";
    var expId = opts.experiment || "E1";
    var set = SETS[expId];
    if (!set) throw new Error("unknown experiment: " + expId);
    var arrayN = opts.arrayN === 2 ? 2 : 4;
    var group = opts.group == null ? groupFor(participant) : opts.group;
    var rnd = mulberry32(hashSeed(participant + "|" + expId + "|" + arrayN));

    var items = set.items.map(function (it, i) {
      return { item: it, index: i, familiar: isFamiliar(i, group) };
    });
    var fam = items.filter(function (r) { return r.familiar; });
    var unf = items.filter(function (r) { return !r.familiar; });
    if (!fam.length || unf.length < arrayN - 1) {
      throw new Error("stimulus set too small for arrayN=" + arrayN);
    }

    var nTrials = opts.nTrials || 40;
    var trials = [];
    // Cycle the probe list (shuffled per pass) so every familiar item is used a
    // near-equal number of times rather than sampled with replacement.
    var probeQueue = [];
    for (var t = 0; t < nTrials; t++) {
      if (!probeQueue.length) probeQueue = shuffled(fam, rnd);
      var probe = probeQueue.pop();
      var pool = shuffled(unf, rnd).filter(function (r) { return r.item.id !== probe.item.id; });
      var slots = [probe].concat(pool.slice(0, arrayN - 1));
      slots = shuffled(slots, rnd);
      trials.push({
        index: t,
        probeItemId: probe.item.id,
        slots: slots.map(function (r, s) {
          return { slot: s, itemId: r.item.id, familiar: r.familiar, item: r.item };
        }),
      });
    }
    return {
      participant: participant, experiment: expId, arrayN: arrayN,
      counterbalanceGroup: group, nTrials: nTrials, trials: trials,
    };
  }

  // Which items this participant is meant to be exposed to in an E1 study
  // phase (i.e. the familiar-role set for their counterbalance group).
  function studySet(opts) {
    var built = buildTrials(opts);
    var set = SETS[built.experiment];
    var seen = {};
    built.trials.forEach(function (tr) {
      tr.slots.forEach(function (s) { if (s.familiar) seen[s.itemId] = true; });
    });
    return set.items.filter(function (it) { return seen[it.id]; });
  }

  // ---- geometry (§6.2) ---------------------------------------------------
  // Pinned by Van der Cruyssen et al. 2024 [W1], whose novelty-preference
  // replication worked on WebGazer with 472x331 px images 295 px apart, and by
  // the <=4-AOI webcam bound. Tiles shrink to fit a small viewport but never
  // below MIN_TILE — a smaller tile is outside the validated envelope, so the
  // page refuses to run rather than silently collecting unusable data.
  var GEOM = { minTileW: 400, minTileH: 300, minGap: 250, edgeMargin: 40 };

  function layout(arrayN, vw, vh) {
    var cols = arrayN === 2 ? 2 : 2;
    var rows = arrayN === 2 ? 1 : 2;
    var gap = GEOM.minGap;
    var availW = vw - 2 * GEOM.edgeMargin - (cols - 1) * gap;
    var availH = vh - 2 * GEOM.edgeMargin - (rows - 1) * gap;
    var tw = Math.floor(availW / cols);
    var th = Math.floor(availH / rows);
    var ok = tw >= GEOM.minTileW && th >= GEOM.minTileH;
    var totalW = cols * tw + (cols - 1) * gap;
    var totalH = rows * th + (rows - 1) * gap;
    var x0 = Math.round((vw - totalW) / 2);
    var y0 = Math.round((vh - totalH) / 2);
    var rects = [];
    for (var i = 0; i < arrayN; i++) {
      var c = i % cols, r = Math.floor(i / cols);
      rects.push({ x: x0 + c * (tw + gap), y: y0 + r * (th + gap), w: tw, h: th });
    }
    return { ok: ok, cols: cols, rows: rows, gap: gap, tileW: tw, tileH: th, rects: rects };
  }

  // ---- trial timing (§6.3) ----------------------------------------------
  // The 4000 ms window spans BOTH phases of the effect: the early orienting
  // window (~0.7-2 s) and the later window, which can reverse in sign. Scoring
  // windows are pre-registered in analysis/aoi_features.py, not chosen here.
  var TIMING = { fixationMs: 500, arrayMs: 4000, blankMs: 300 };

  var COVER_TASKS = {
    // Weaker per Nahari 2019 [C2], but maximally plausible as ordinary content.
    "low-demand": {
      id: "low-demand",
      prompt: "Which image best fits the section you just read?",
      demandsMemory: false,
    },
    // Imposes the memory demand [C2] found countermeasure-resistant, while
    // still reading as an ordinary onboarding/preference prompt.
    "memory-adjacent": {
      id: "memory-adjacent",
      prompt: "Which of these have you seen on this site before?",
      demandsMemory: true,
    },
  };

  var STIMULUS_NOTES =
    "Procedural SVG placeholders. For a real E2 run, replace makeBrandItems() " +
    "with actual service logos/screenshots and record their provenance; do not " +
    "commit third-party marks to this repo without checking their licence.";

  return {
    SETS: SETS, GEOM: GEOM, TIMING: TIMING, COVER_TASKS: COVER_TASKS,
    N_GROUPS: N_GROUPS, STIMULUS_NOTES: STIMULUS_NOTES,
    mulberry32: mulberry32, hashSeed: hashSeed, shuffled: shuffled,
    groupFor: groupFor, isFamiliar: isFamiliar,
    buildTrials: buildTrials, studySet: studySet, layout: layout,
  };
});
