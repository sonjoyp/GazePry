/*
 * GazePry tracker SDK — Direction 1 prototype (tracker-agnostic orchestrator)
 * ------------------------------------------------------------------
 * A single client-side script (the "third-party analytics tag") that, for a
 * chosen webcam gaze tracker:
 *   1. boots the tracker engine,
 *   2. runs a short click calibration (only for trackers that train on clicks),
 *   3. logs the raw per-frame gaze stream {t, x, y} for a task, and
 *   4. POSTs the session to the collection server.
 *
 * The same script is embedded in every task "site". That is the point of the
 * study: one tracking provider observing a visitor across different content
 * pages, linking them by gaze dynamics rather than by any cookie.
 *
 * WHICH tracker runs is pluggable. Each tracker is a small adapter file under
 * trackers/ that calls GazePry.registerTracker({...}). The active tracker is
 * chosen per session (identity.tracker) so the same participant can be captured
 * with WebGazer, WebEyeTrack, EyeGestures, GazeCloud, … and compared (RQ3).
 * See trackers/README-adapter.md for the adapter contract.
 */
(function () {
  "use strict";

  // Base URL of this script (the public/ dir). Adapters resolve their vendored
  // library + model assets against this so they load identically on the hub and
  // on task pages one level deep (a page-relative path 404s on task pages).
  var SCRIPT_BASE = (function () {
    var src = document.currentScript && document.currentScript.src;
    return src ? src.slice(0, src.lastIndexOf("/") + 1) : "";
  })();

  var GazePry = {
    config: {
      server: "", // same-origin by default; set to a full URL for cross-origin demo
      // Persist the model across page loads so one calibration on the hub carries
      // to every task page in the same visit. A NEW session re-calibrates with
      // {fresh:true}, clearing the prior model first.
      saveAcrossSessions: true,
      defaultTracker: "webgazer",
    },
    identity: { participant: null, session: null, tracker: null },
    baseUrl: SCRIPT_BASE,

    _trackers: {}, // family -> adapter
    _active: null, // the adapter currently driving the webcam
    _engineReady: false,
    _samples: [],
    _capturing: false,
  };

  // ---- tracker registry -------------------------------------------------
  // Adapters self-register (they are loaded after this file). See the adapter
  // contract in trackers/README-adapter.md.
  GazePry.registerTracker = function (adapter) {
    if (!adapter || !adapter.family) throw new Error("tracker adapter needs a 'family'");
    if (adapter.available === undefined) adapter.available = true;
    if (adapter.needsCalibration === undefined) adapter.needsCalibration = true;
    this._trackers[adapter.family] = adapter;
    return adapter;
  };
  GazePry.listTrackers = function () {
    var self = this;
    return Object.keys(this._trackers).map(function (k) { return self._trackers[k]; });
  };
  GazePry.getTracker = function (family) { return this._trackers[family]; };
  GazePry.activeTracker = function () { return this._active; };
  GazePry.resolveTracker = function () {
    var fam = this.identity.tracker || this.config.defaultTracker;
    return this._trackers[fam] || this._trackers[this.config.defaultTracker] || this.listTrackers()[0];
  };

  // ---- identity ---------------------------------------------------------
  function q(name) {
    return new URLSearchParams(location.search).get(name);
  }

  GazePry.loadIdentity = function () {
    var p = q("participant") || localStorage.getItem("gp_participant");
    var s = q("session") || localStorage.getItem("gp_session");
    var tr = q("tracker") || localStorage.getItem("gp_tracker") || this.config.defaultTracker;
    this.identity = { participant: p, session: s, tracker: tr };
    return this.identity;
  };

  GazePry.saveIdentity = function (participant, session, tracker) {
    localStorage.setItem("gp_participant", participant);
    localStorage.setItem("gp_session", session);
    if (tracker) localStorage.setItem("gp_tracker", tracker);
    this.identity = {
      participant: participant,
      session: session,
      tracker: tracker || this.identity.tracker || this.config.defaultTracker,
    };
  };

  GazePry.requireIdentity = function () {
    this.loadIdentity();
    if (!this.identity.participant || !this.identity.session) {
      location.href = "../index.html";
      return false;
    }
    return true;
  };

  // ---- session condition / environment metadata ------------------------
  // Per-VISIT metadata that CANNOT be reconstructed after collection and that
  // the analysis needs but the raw {t,x,y} stream cannot supply:
  //   intervention  — which RQ4 arm this visit is (baseline / clear-state /
  //                   incognito / new-profile / new-device / diff-lighting /
  //                   face-blur). The headline unclearability axis (§13).
  //   lighting      — free note on lighting / seating (A.3 negative control).
  //   device        — machine + webcam label, e.g. "laptopB-builtin" (RQ4
  //                   cross-device; userAgent alone can't name the camera).
  //   glasses       — corrective lenses (a per-person capture confound).
  //   calibQuality  — operator's post-calibration judgement good/fair/poor
  //                   (the calibration-artifact confound, A.3). A measured
  //                   pixel-error validation can later overwrite this.
  //   notes         — anything else worth recording for this visit.
  // Persisted per visit and merged into every stored session so the offline
  // analysis can filter and report by condition. Absent fields default; an old
  // record simply has no `condition` and is treated as baseline downstream.
  GazePry.CONDITION_FIELDS = ["intervention", "lighting", "device", "glasses", "calibQuality", "notes"];
  GazePry.DEFAULT_CONDITION = {
    intervention: "baseline", lighting: "", device: "", glasses: false, calibQuality: "", notes: "",
  };

  GazePry.loadCondition = function () {
    var c = {};
    this.CONDITION_FIELDS.forEach(function (k) {
      var v = localStorage.getItem("gp_cond_" + k);
      if (k === "glasses") c[k] = v === "true";
      else c[k] = v != null ? v : GazePry.DEFAULT_CONDITION[k];
    });
    // Query overrides let a scripted incognito / new-profile run (which starts
    // with empty localStorage) still tag its arm, e.g. ?intervention=incognito.
    var qi = q("intervention");
    if (qi) c.intervention = qi;
    var qd = q("device");
    if (qd) c.device = qd;
    return c;
  };

  GazePry.saveCondition = function (patch) {
    patch = patch || {};
    this.CONDITION_FIELDS.forEach(function (k) {
      if (k in patch) {
        var v = patch[k];
        localStorage.setItem(
          "gp_cond_" + k,
          k === "glasses" ? (v ? "true" : "false") : String(v == null ? "" : v)
        );
      }
    });
    return this.loadCondition();
  };

  // ---- engine -----------------------------------------------------------
  GazePry.startEngine = async function () {
    if (this._engineReady) return;
    var adapter = this.resolveTracker();
    if (!adapter) throw new Error("no gaze tracker registered");
    if (adapter.available === false)
      throw new Error("Tracker '" + adapter.label + "' is not installed. " + (adapter.setup || ""));
    this._active = adapter;
    console.log("[GazePry] starting tracker: " + adapter.label + " (" + adapter.family + ")…");

    if (adapter.load) await adapter.load(this.baseUrl);

    // start() should resolve once the webcam + listeners are live. Some engines
    // (e.g. WebGazer's begin()) only fully settle after the first prediction and
    // can stall if model assets fail to load; the adapter is expected to race its
    // own boot, but keep an outer safety timeout so the UI never hangs forever.
    var settled = Promise.resolve(adapter.start ? adapter.start() : null)
      .then(function () { return "ready"; })
      .catch(function (e) { console.error("[GazePry] tracker.start() error:", e); return "error"; });
    var timeout = new Promise(function (res) {
      setTimeout(function () { res("timeout"); }, adapter.startTimeoutMs || 8000);
    });
    var outcome = await Promise.race([settled, timeout]);
    if (outcome === "timeout")
      console.warn("[GazePry] " + adapter.label + " slow to start after " +
        Math.round((adapter.startTimeoutMs || 8000) / 1000) + "s; proceeding (webcam may already be live).");

    this._engineReady = true;
    this._lastBeat = performance.now();
    this._attachIdle();
    this._startWatchdog();
    console.log("[GazePry] engine ready (" + adapter.label + ", outcome: " + outcome + ").");
  };

  // Keep a heartbeat alive when nothing is capturing, so the watchdog can tell a
  // live prediction loop from a dead one. Capture/probe replace this listener and
  // re-attach it when they finish.
  GazePry._attachIdle = function () {
    if (this._active && this._active.onGaze)
      this._active.onGaze(function () { GazePry._lastBeat = performance.now(); });
  };

  // Some engines' prediction loops die on a single hung/rejected frame and every
  // counter freezes. Watch the heartbeat and, for adapters that support it,
  // restart the loop (pause + resume). If restarts never help, tell the user.
  GazePry._startWatchdog = function () {
    if (this._watchdog) return;
    var kicks = 0;
    this._watchdog = setInterval(function () {
      if (document.hidden) return; // rAF is throttled in background tabs — not a failure
      var a = GazePry._active;
      var quiet = performance.now() - GazePry._lastBeat;
      if (quiet < 4000) { kicks = 0; return; }
      if (!a || (!a.pause && !a.resume)) return; // this engine can't be kicked
      kicks++;
      console.warn("[GazePry] no gaze callbacks for " + Math.round(quiet / 1000) +
        "s — restarting " + a.label + " (attempt " + kicks + ").");
      try {
        if (a.pause) a.pause();
        setTimeout(function () { if (a.resume) Promise.resolve(a.resume()).catch(function () {}); }, 300);
      } catch (e) {}
      GazePry._lastBeat = performance.now(); // full quiet window before the next kick
      if (kicks === 3)
        GazePry._toast("Gaze engine (" + a.label + ") is producing no data. Open the console (F12) — " +
          (a.noDataHint || "check that the tracker's model/library assets loaded."));
    }, 2000);
  };

  GazePry.hidePreview = function (hide) {
    if (this._active && this._active.showPreview) this._active.showPreview(!hide);
  };

  // ---- calibration ------------------------------------------------------
  // 9-point grid, N clicks each — only for trackers that train on clicks. For
  // self-calibrating trackers (needsCalibration:false) the adapter runs its own
  // calibration inside start(), so this just boots the engine and resolves.
  GazePry.calibrate = function (opts) {
    opts = opts || {};
    var clicksPerDot = opts.clicksPerDot || 5;
    var self = this;
    self._calibClicksPerDot = clicksPerDot; // recorded into each session (calibration effort)

    return new Promise(async function (resolve, reject) {
     try {
      await self.startEngine();
      var a = self._active;
      if (opts.fresh && a.clearModel) { try { a.clearModel(); } catch (e) {} } // reset for a new session

      if (!a.needsCalibration) { resolve(); return; } // engine self-calibrated in start()
      if (a.showPreview) a.showPreview(true);

      var overlay = document.createElement("div");
      overlay.id = "gp-cal";
      var msg = document.createElement("div");
      msg.className = "gp-cal-msg";
      msg.innerHTML =
        "<b>Calibration (" + a.label + ").</b> Look at each yellow dot and click it " +
        clicksPerDot + " times until it turns green. Keep your head still and centered.";
      overlay.appendChild(msg);

      var xs = [0.08, 0.5, 0.92];
      var ys = [0.12, 0.5, 0.88];
      var remaining = xs.length * ys.length;

      ys.forEach(function (fy) {
        xs.forEach(function (fx) {
          var dot = document.createElement("div");
          dot.className = "gp-cal-dot";
          dot.style.left = fx * 100 + "%";
          dot.style.top = fy * 100 + "%";
          var left = clicksPerDot;
          dot.textContent = left;
          dot.addEventListener("click", function (ev) {
            if (left <= 0) return;
            if (a.recordCalibration) { try { a.recordCalibration(ev.clientX, ev.clientY); } catch (e) {} }
            left--;
            dot.textContent = left > 0 ? left : "";
            if (left <= 0) {
              dot.classList.add("done");
              remaining--;
              if (remaining === 0) {
                setTimeout(function () { overlay.remove(); resolve(); }, 250);
              }
            }
          });
          overlay.appendChild(dot);
        });
      });

      document.body.appendChild(overlay);
     } catch (e) {
      console.error("[GazePry] calibration failed:", e);
      GazePry._toast("Calibration/engine error: " + (e && e.message ? e.message : e) + " — see console (F12).");
      reject(e);
     }
    });
  };

  // ---- capture ----------------------------------------------------------
  GazePry.runTask = function (opts) {
    opts = opts || {};
    var task = opts.task || "unknown";
    var durationMs = (opts.durationSec || 60) * 1000;
    var self = this;

    return new Promise(async function (resolve, reject) {
     try {
      await self.startEngine();
      var a = self._active;
      if (a.showPreview) a.showPreview(false); // capture cleanly; preview off during the task
      self._samples = [];
      self._capturing = true;
      var startedAt = Date.now();
      var t0 = performance.now();
      var gaps = 0;

      a.onGaze(function (data, clock) {
        GazePry._lastBeat = performance.now();
        if (!self._capturing) return;
        if (data == null) {
          gaps++;
          self._samples.push({ t: Math.round(clock), x: null, y: null });
        } else {
          self._samples.push({
            t: Math.round(clock),
            x: Math.round(data.x * 10) / 10,
            y: Math.round(data.y * 10) / 10,
          });
        }
      });

      var hud = buildHud(task + " · " + a.label);
      document.body.appendChild(hud.el);

      var finished = false;
      function finish() {
        if (finished) return;
        finished = true;
        self._capturing = false;
        if (a.offGaze) a.offGaze();
        self._attachIdle();
        clearInterval(timer);
        hud.el.remove();
        var session = {
          schema: "gazepry.session.v2",
          participant: self.identity.participant,
          session: self.identity.session,
          task: task,
          tracker: a.id,            // full tracker id (e.g. "webgazer-3.5.3")
          trackerFamily: a.family,  // stable slug for grouping/filtering
          startedAt: startedAt,
          durationMs: Math.round(performance.now() - t0),
          // Per-visit condition/environment metadata (RQ4 + confound controls,
          // §13/A.3). Cannot be reconstructed post-hoc, so it is captured here.
          condition: self.loadCondition(),
          calibClicksPerDot: self._calibClicksPerDot || null,
          screen: {
            w: screen.width, h: screen.height, dpr: window.devicePixelRatio || 1,
            innerW: window.innerWidth, innerH: window.innerHeight,
          },
          userAgent: navigator.userAgent,
          nSamples: self._samples.length,
          nGaps: gaps,
          samples: self._samples,
        };
        self.submit(session).then(function (res) {
          resolve({ session: session, submit: res });
        });
      }

      hud.finishBtn.onclick = finish;

      var timer = setInterval(function () {
        var elapsed = performance.now() - t0;
        var left = Math.max(0, durationMs - elapsed);
        hud.update({
          left: Math.ceil(left / 1000),
          n: self._samples.length,
          gaps: gaps,
          live: self._samples.length && self._samples[self._samples.length - 1].x != null,
        });
        if (left <= 0) finish();
      }, 200);
     } catch (e) {
      console.error("[GazePry] capture failed:", e);
      GazePry._toast("Capture/engine error: " + (e && e.message ? e.message : e) + " — see console (F12).");
      reject(e);
     }
    });
  };

  // Capture a short probe WITHOUT storing it — used by the live re-ID demo.
  GazePry.captureProbe = function (durationSec) {
    var self = this;
    var durationMs = (durationSec || 20) * 1000;
    return new Promise(async function (resolve, reject) {
     try {
      await self.startEngine();
      var a = self._active;
      if (a.showPreview) a.showPreview(false);
      var samples = [];
      var gaps = 0;
      self._capturing = true;
      var t0 = performance.now();
      a.onGaze(function (data, clock) {
        GazePry._lastBeat = performance.now();
        if (!self._capturing) return;
        if (data == null) { gaps++; samples.push({ t: Math.round(clock), x: null, y: null }); }
        else samples.push({ t: Math.round(clock), x: Math.round(data.x * 10) / 10, y: Math.round(data.y * 10) / 10 });
      });
      var hud = buildHud("re-ID probe · " + a.label);
      document.body.appendChild(hud.el);
      var done = false;
      function finish() {
        if (done) return; done = true;
        self._capturing = false;
        if (a.offGaze) a.offGaze();
        self._attachIdle();
        clearInterval(timer);
        hud.el.remove();
        resolve({
          samples: samples, nGaps: gaps,
          tracker: a.id, trackerFamily: a.family,
          screen: { innerW: window.innerWidth, innerH: window.innerHeight,
            w: screen.width, h: screen.height, dpr: window.devicePixelRatio || 1 },
        });
      }
      hud.finishBtn.onclick = finish;
      var timer = setInterval(function () {
        var left = Math.max(0, durationMs - (performance.now() - t0));
        hud.update({ left: Math.ceil(left / 1000), n: samples.length, gaps: gaps,
          live: samples.length && samples[samples.length - 1].x != null });
        if (left <= 0) finish();
      }, 200);
     } catch (e) {
      console.error("[GazePry] probe capture failed:", e);
      GazePry._toast("Probe/engine error: " + (e && e.message ? e.message : e) + " — see console (F12).");
      reject(e);
     }
    });
  };

  function buildHud(task) {
    var el = document.createElement("div");
    el.id = "gp-hud";
    el.innerHTML =
      '<div class="gp-hud-title"><span class="gp-dot" id="gp-live"></span>Recording: ' + task + "</div>" +
      '<div class="gp-metric">Time left <b id="gp-left">–</b></div>' +
      '<div class="gp-metric">Samples <b id="gp-n">0</b></div>' +
      '<div class="gp-metric">Gaps (blinks/lost) <b id="gp-gaps">0</b></div>' +
      '<button class="gp-btn danger" id="gp-finish">Finish &amp; submit</button>';
    return {
      el: el,
      finishBtn: el.querySelector("#gp-finish"),
      update: function (s) {
        el.querySelector("#gp-left").textContent = s.left + "s";
        el.querySelector("#gp-n").textContent = s.n;
        el.querySelector("#gp-gaps").textContent = s.gaps;
        var dot = el.querySelector("#gp-live");
        if (s.live) dot.classList.add("live"); else dot.classList.remove("live");
      },
    };
  }

  // ---- submission -------------------------------------------------------
  GazePry.submit = async function (session) {
    var url = (this.config.server || "") + "/ingest";
    try {
      var r = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(session),
      });
      if (r.ok) {
        var j = await r.json();
        return { ok: true, via: "server", stored: j.stored };
      }
      throw new Error("HTTP " + r.status);
    } catch (e) {
      // fallback: download locally so no data is ever lost if the server is down
      var name = [session.participant, session.session, session.task,
        session.trackerFamily || "tracker", session.startedAt].join("_") + ".json";
      var blob = new Blob([JSON.stringify(session)], { type: "application/json" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = name;
      a.click();
      return { ok: false, via: "download", error: String(e), file: name };
    }
  };

  // ---- "unclearable" demo helper ---------------------------------------
  // Wipes conventional client state. Gaze re-identification is unaffected
  // because identity is re-derived from the live eye-movement stream.
  GazePry.wipeState = function () {
    try { localStorage.clear(); } catch (e) {}
    try { sessionStorage.clear(); } catch (e) {}
    document.cookie.split(";").forEach(function (c) {
      document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date(0).toUTCString() + ";path=/");
    });
    if (this._active && this._active.clearModel) { try { this._active.clearModel(); } catch (e) {} }
  };

  // Small on-screen error banner so failures aren't silent for console-less users.
  GazePry._toast = function (msg) {
    var t = document.createElement("div");
    t.textContent = msg;
    t.style.cssText =
      "position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:2147483647;" +
      "background:#f87171;color:#250606;padding:10px 16px;border-radius:8px;" +
      "font:600 14px system-ui,sans-serif;max-width:80vw;box-shadow:0 8px 24px rgba(0,0,0,.4);";
    document.body.appendChild(t);
    setTimeout(function () { t.remove(); }, 9000);
  };

  window.GazePry = GazePry;
})();
