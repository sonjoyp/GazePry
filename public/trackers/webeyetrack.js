/*
 * WebEyeTrack adapter — the head-pose-aware, near-future commodity ceiling
 * (Davalos et al. 2025, arXiv:2508.19544; RedForestAi/WebEyeTrack, MIT). A
 * BlazeGaze CNN + MediaPipe face landmarks + few-shot personalisation, running
 * in a Web Worker so inference stays off the UI thread. Gaze inference is
 * on-device (video stays local). Study-protocol tracker arm 3.
 *
 * Vendored by scripts/vendor-trackers.sh:
 *   ../lib/webeyetrack/webeyetrack.js   UMD bundle (exports on window)
 *   ../../web/model.json + shard         BlazeGaze weights — MUST be served at the
 *                                        origin root /web/ (BlazeGaze loads
 *                                        `${location.origin}/web/model.json`).
 * At runtime it also fetches MediaPipe assets from Google/jsDelivr CDNs
 * (download-only; no camera data leaves the machine).
 *
 * Real API:
 *   const cam = new WebcamClient(videoId);
 *   const proxy = new WebEyeTrackProxy(cam);
 *   proxy.onGazeResults = (g) => { ... g.normPog=[x,y] in [-0.5,0.5]; g.gazeState }
 * The proxy also listens for window clicks and feeds them to its few-shot
 * calibrator — so the orchestrator's 9-point click grid personalises the model.
 *
 * Implements the GazePry tracker-adapter contract (see README-adapter.md).
 */
(function () {
  "use strict";

  var loaded = null;
  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src; s.onload = resolve;
      s.onerror = function () { reject(new Error("failed to load " + src)); };
      document.head.appendChild(s);
    });
  }
  function ensureVideo(id) {
    var v = document.getElementById(id);
    if (!v) {
      v = document.createElement("video");
      v.id = id; v.autoplay = true; v.playsInline = true; v.muted = true;
      v.style.display = "none";
      document.body.appendChild(v);
    }
    return v;
  }

  var adapter = {
    id: "webeyetrack-0.0.2",
    family: "webeyetrack",
    label: "WebEyeTrack",
    hint: "Head-pose-aware CNN + few-shot personalisation, in a Web Worker, in-browser (video stays local). The near-future commodity ceiling.",
    privacy: "local",
    needsCalibration: true, // few-shot: the click grid feeds its recalibrator
    available: true,
    startTimeoutMs: 20000, // model + MediaPipe assets download on first run

    load: function (base) {
      this._base = base || "";
      if (!loaded) {
        loaded = window.WebEyeTrackProxy
          ? Promise.resolve()
          : loadScript(this._base + "lib/webeyetrack/webeyetrack.js");
      }
      return loaded;
    },

    start: function () {
      if (!window.WebEyeTrackProxy || !window.WebcamClient)
        throw new Error("WebEyeTrack not loaded (run scripts/vendor-trackers.sh)");
      var self = this;
      this._cb = null;
      ensureVideo("wet-webcam");

      // Constructing the proxy kicks off: worker init -> 'ready' -> webcam start
      // -> per-frame gaze inference. It attaches its own window-click calibrator.
      this._cam = new window.WebcamClient("wet-webcam");
      this._proxy = new window.WebEyeTrackProxy(this._cam);

      return new Promise(function (resolve) {
        var settled = false;
        self._proxy.onGazeResults = function (g) {
          window.GazePry._lastBeat = performance.now();
          if (!settled) { settled = true; resolve(); } // first inference = live
          if (!self._cb) return;
          if (!g || g.gazeState === "closed" || !g.normPog) {
            self._cb(null, performance.now()); // blink / no face this frame
          } else {
            self._cb({
              x: (g.normPog[0] + 0.5) * window.innerWidth,
              y: (g.normPog[1] + 0.5) * window.innerHeight,
            }, performance.now());
          }
        };
        setTimeout(function () { if (!settled) { settled = true; resolve(); } }, adapter.startTimeoutMs);
      });
    },

    onGaze: function (cb) { this._cb = cb; },
    offGaze: function () { this._cb = null; },

    // The proxy captures window clicks itself, so each calibration-dot click is
    // already fed to the few-shot recalibrator — nothing extra to do here.
    recordCalibration: function () {},
    // No client-side identity model to clear (few-shot state lives in the worker;
    // re-running the click grid re-personalises it). Kept for the wipe demo.
    clearModel: function () {},
    showPreview: function () {},
  };

  if (window.GazePry) window.GazePry.registerTracker(adapter);
  else console.error("[webeyetrack] gazepry-tracker.js must load before this adapter");
})();
