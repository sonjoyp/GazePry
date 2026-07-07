/*
 * GazePry tracker SDK — Direction 1 prototype
 * ------------------------------------------------------------------
 * A single client-side script (the "third-party analytics tag") that:
 *   1. boots WebGazer v3.5.3 (commodity webcam gaze),
 *   2. runs a short click calibration,
 *   3. logs the raw per-frame gaze stream {t, x, y} for a task, and
 *   4. POSTs the session to the collection server.
 *
 * The same script is embedded in every task "site". That is the point of
 * the study: one tracking provider observing a visitor across different
 * content pages, linking them by gaze dynamics rather than by any cookie.
 *
 * Requires webgazer.js to be loaded first (window.webgazer).
 */
(function () {
  "use strict";

  var TRACKER_ID = "webgazer-3.5.3";

  var GazePry = {
    config: {
      server: "", // same-origin by default; set to a full URL for cross-origin demo
      // Persist the regression model across page loads so one calibration on the
      // hub carries to every task page in the same visit. A NEW session starts by
      // re-calibrating with {fresh:true}, which clears the prior model first.
      saveAcrossSessions: true,
    },
    identity: { participant: null, session: null },
    _engineReady: false,
    _samples: [],
    _capturing: false,
  };

  // ---- identity ---------------------------------------------------------
  function q(name) {
    return new URLSearchParams(location.search).get(name);
  }

  GazePry.loadIdentity = function () {
    var p = q("participant") || localStorage.getItem("gp_participant");
    var s = q("session") || localStorage.getItem("gp_session");
    this.identity = { participant: p, session: s };
    return this.identity;
  };

  GazePry.saveIdentity = function (participant, session) {
    localStorage.setItem("gp_participant", participant);
    localStorage.setItem("gp_session", session);
    this.identity = { participant: participant, session: session };
  };

  GazePry.requireIdentity = function () {
    this.loadIdentity();
    if (!this.identity.participant || !this.identity.session) {
      location.href = "../index.html";
      return false;
    }
    return true;
  };

  // ---- engine -----------------------------------------------------------
  GazePry.startEngine = async function () {
    if (this._engineReady) return;
    if (!window.webgazer) throw new Error("webgazer.js not loaded before gazepry-tracker.js");
    console.log("[GazePry] starting WebGazer engine…");

    var beginPromise = webgazer
      .setRegression("ridge")
      .saveDataAcrossSessions(this.config.saveAcrossSessions)
      .setGazeListener(function () {}) // real listener attached per task
      .begin();

    // begin() only resolves after WebGazer's first prediction loop completes;
    // in some environments that first getPrediction() stalls, leaving begin()
    // pending forever. The webcam and the click-to-train mouse listeners are
    // already live by the time the video appears, so don't block the UI on it:
    // race begin() against a timeout and proceed either way. Attach a catch so a
    // late rejection never becomes a silent unhandled rejection.
    var settled = Promise.resolve(beginPromise)
      .then(function () { return "ready"; })
      .catch(function (e) { console.error("[GazePry] webgazer.begin() error:", e); return "error"; });
    var timeout = new Promise(function (res) { setTimeout(function () { res("timeout"); }, 6000); });
    var outcome = await Promise.race([settled, timeout]);
    if (outcome === "timeout")
      console.warn("[GazePry] begin() slow to resolve after 6s; proceeding (webcam is live, click-training is active).");

    try {
      webgazer.showVideoPreview(true).showPredictionPoints(true).applyKalmanFilter(true);
      webgazer.params.videoViewerWidth = 160; // shrink preview so it doesn't cover content
      webgazer.params.videoViewerHeight = 120;
    } catch (e) { console.warn("[GazePry] preview config warning:", e); }

    this._engineReady = true;
    console.log("[GazePry] engine ready (outcome: " + outcome + ").");
  };

  GazePry.hidePreview = function (hide) {
    if (!window.webgazer) return;
    webgazer.showVideoPreview(!hide).showPredictionPoints(!hide).showFaceOverlay(!hide).showFaceFeedbackBox(!hide);
  };

  // ---- calibration ------------------------------------------------------
  // 9-point grid, N clicks each. Clicks feed WebGazer's regression (mouse
  // listeners are on by default); we also record explicitly to be safe.
  GazePry.calibrate = function (opts) {
    opts = opts || {};
    var clicksPerDot = opts.clicksPerDot || 5;
    var self = this;

    return new Promise(async function (resolve, reject) {
     try {
      await self.startEngine();
      if (opts.fresh && window.webgazer) {
        try { webgazer.clearData(); } catch (e) {} // reset model for a new session
      }
      self.hidePreview(false);

      var overlay = document.createElement("div");
      overlay.id = "gp-cal";
      var msg = document.createElement("div");
      msg.className = "gp-cal-msg";
      msg.innerHTML =
        "<b>Calibration.</b> Look at each yellow dot and click it " +
        clicksPerDot +
        " times until it turns green. Keep your head still and centered.";
      overlay.appendChild(msg);

      var xs = [0.08, 0.5, 0.92];
      var ys = [0.12, 0.5, 0.88];
      var dots = [];
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
            // explicit training sample at the true target location
            try { webgazer.recordScreenPosition(ev.clientX, ev.clientY, "click"); } catch (e) {}
            left--;
            dot.textContent = left > 0 ? left : "";
            if (left <= 0) {
              dot.classList.add("done");
              remaining--;
              if (remaining === 0) {
                setTimeout(function () {
                  overlay.remove();
                  resolve();
                }, 250);
              }
            }
          });
          overlay.appendChild(dot);
          dots.push(dot);
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
      self.hidePreview(true); // capture cleanly; preview off during the task
      self._samples = [];
      self._capturing = true;
      var startedAt = Date.now();
      var t0 = performance.now();
      var gaps = 0;

      webgazer.setGazeListener(function (data, clock) {
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

      var hud = buildHud(task);
      document.body.appendChild(hud.el);

      var finished = false;
      function finish() {
        if (finished) return;
        finished = true;
        self._capturing = false;
        webgazer.clearGazeListener();
        clearInterval(timer);
        hud.el.remove();
        var session = {
          schema: "gazepry.session.v1",
          participant: self.identity.participant,
          session: self.identity.session,
          task: task,
          tracker: TRACKER_ID,
          startedAt: startedAt,
          durationMs: Math.round(performance.now() - t0),
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
      self.hidePreview(true);
      var samples = [];
      var gaps = 0;
      self._capturing = true;
      var t0 = performance.now();
      webgazer.setGazeListener(function (data, clock) {
        if (!self._capturing) return;
        if (data == null) { gaps++; samples.push({ t: Math.round(clock), x: null, y: null }); }
        else samples.push({ t: Math.round(clock), x: Math.round(data.x * 10) / 10, y: Math.round(data.y * 10) / 10 });
      });
      var hud = buildHud("re-ID probe");
      document.body.appendChild(hud.el);
      var done = false;
      function finish() {
        if (done) return; done = true;
        self._capturing = false;
        webgazer.clearGazeListener();
        clearInterval(timer);
        hud.el.remove();
        resolve({
          samples: samples, nGaps: gaps,
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
      var name =
        session.participant + "_" + session.session + "_" + session.task + "_" + session.startedAt + ".json";
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
    if (window.webgazer) { try { webgazer.clearData(); } catch (e) {} }
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
