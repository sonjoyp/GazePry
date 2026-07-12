/*
 * WebGazer adapter — the deployed-reality commodity webcam arm and the GazePry
 * lineage (ridge regression on webcam eye patches, click-trained, no head pose).
 * Built on the current brownhci/WebGazer v3.5.3 vendored at lib/webgazer.js.
 *
 * Implements the GazePry tracker-adapter contract (see README-adapter.md).
 */
(function () {
  "use strict";

  var webgazerLoaded = null; // Promise, so load() is idempotent across pages

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = function () { reject(new Error("failed to load " + src)); };
      document.head.appendChild(s);
    });
  }

  var adapter = {
    id: "webgazer-3.5.3",
    family: "webgazer",
    label: "WebGazer 3.5.3",
    hint: "Ridge regression, click-trained, no head pose. Runs fully in the browser (no video leaves the machine).",
    privacy: "local",
    needsCalibration: true,
    available: true,
    startTimeoutMs: 9000,
    noDataHint: "usually the FaceMesh files under mediapipe/face_mesh/ failed to load.",

    load: function (base) {
      this._base = base || "";
      if (!webgazerLoaded) {
        webgazerLoaded = window.webgazer
          ? Promise.resolve()
          : loadScript(this._base + "lib/webgazer.js");
      }
      return webgazerLoaded;
    },

    start: async function () {
      if (this._started) return;
      if (!window.webgazer) throw new Error("webgazer.js not loaded");

      // WebGazer's bundled FaceMesh fetches its WASM/model files from
      // params.faceMeshSolutionPath, whose default resolves against the *page*
      // URL and 404s on task pages one level deep. Pin it to the vendored assets.
      webgazer.params.faceMeshSolutionPath = this._base + "mediapipe/face_mesh";

      // Heartbeat: wrap setGazeListener once so every callback stamps the SDK's
      // heartbeat via the listener the orchestrator installs. (The orchestrator
      // already stamps _lastBeat inside its own callbacks; this keeps the idle
      // no-op listener honest too.)
      if (!this._listenerWrapped) {
        this._listenerWrapped = true;
        var origSet = webgazer.setGazeListener.bind(webgazer);
        webgazer.setGazeListener = function (fn) {
          return origSet(function (data, clock) {
            window.GazePry._lastBeat = performance.now();
            if (fn) fn(data, clock);
          });
        };
      }

      var save = window.GazePry.config.saveAcrossSessions;
      var beginPromise = webgazer
        .setRegression("ridge")
        .saveDataAcrossSessions(save)
        .setGazeListener(function () {}) // real listener attached per task/probe
        .begin();

      // begin() resolves only after the first prediction loop completes; if that
      // first getPrediction() stalls (FaceMesh assets), it stays pending forever.
      // The webcam + click-training listeners are already live, so don't block:
      // race begin() against a short timeout and proceed either way.
      var settled = Promise.resolve(beginPromise)
        .then(function () { return "ready"; })
        .catch(function (e) { console.error("[webgazer] begin() error:", e); return "error"; });
      var timeout = new Promise(function (res) { setTimeout(function () { res("timeout"); }, 6000); });
      var outcome = await Promise.race([settled, timeout]);
      if (outcome === "timeout")
        console.warn("[webgazer] begin() slow after 6s; proceeding (webcam live, click-training active).");

      try {
        webgazer.showVideoPreview(true).showPredictionPoints(true).applyKalmanFilter(true);
        webgazer.params.videoViewerWidth = 160;
        webgazer.params.videoViewerHeight = 120;
      } catch (e) { console.warn("[webgazer] preview config warning:", e); }

      this._started = true;
    },

    onGaze: function (cb) {
      // WebGazer delivers data={x,y} in viewport pixels, or null on a lost face.
      webgazer.setGazeListener(function (data, clock) { cb(data, clock); });
    },
    offGaze: function () { try { webgazer.clearGazeListener(); } catch (e) {} },

    recordCalibration: function (x, y) {
      // Clicks already feed WebGazer's regression (mouse listeners on by default);
      // record explicitly at the true target too, to be safe.
      try { webgazer.recordScreenPosition(x, y, "click"); } catch (e) {}
    },

    clearModel: function () { try { webgazer.clearData(); } catch (e) {} },

    showPreview: function (show) {
      if (!window.webgazer) return;
      webgazer.showVideoPreview(show).showPredictionPoints(show)
        .showFaceOverlay(show).showFaceFeedbackBox(show);
    },

    pause: function () { try { webgazer.pause(); } catch (e) {} },
    resume: function () { return webgazer.resume(); },

    // Full shutdown that RELEASES THE WEBCAM. In v3.5.3 pause() only halts the
    // prediction loop and end() only removes the UI — the MediaStream (and the
    // camera light) stays live until stopVideo() stops the track. The trained
    // model is untouched (and persisted via saveDataAcrossSessions), so a later
    // start() re-begins with the same calibration.
    stop: function () {
      if (!this._started) return;
      try { // stop every track, not just getTracks()[0] like stopVideo() does
        var v = document.getElementById(webgazer.params.videoElementId);
        if (v && v.srcObject) v.srcObject.getTracks().forEach(function (t) { t.stop(); });
      } catch (e) {}
      try { webgazer.stopVideo(); } catch (e) {} // stops the stream's track, detaches video/canvas
      try { webgazer.end(); } catch (e) {}       // pauses the loop, removes container + gaze dot
      this._started = false;                     // let start() run begin() again
    },
  };

  if (window.GazePry) window.GazePry.registerTracker(adapter);
  else console.error("[webgazer] gazepry-tracker.js must load before this adapter");
})();
