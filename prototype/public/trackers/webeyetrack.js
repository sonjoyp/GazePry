/*
 * WebEyeTrack adapter — the head-pose-aware, near-future commodity ceiling
 * (Davalos et al. 2025, arXiv:2508.19544). CNN gaze estimation + MediaPipe face
 * mesh + few-shot on-device personalisation, all in the browser (video stays
 * local). This is tracker arm 3 in the study protocol (§4).
 *
 * STATUS: available:false until you vendor the WebEyeTrack browser build. The
 * adapter is written against its documented shape; wire the two TODOs below to
 * the actual library API, drop the assets under lib/webeyetrack/, and flip
 * available:true. Implements the GazePry tracker-adapter contract.
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

  var adapter = {
    id: "webeyetrack-0.1",
    family: "webeyetrack",
    label: "WebEyeTrack",
    hint: "Head-pose-aware CNN + few-shot personalisation, in-browser (video stays local). The near-future commodity ceiling.",
    privacy: "local",
    needsCalibration: true, // few-shot: the click grid supplies the support points
    available: false,
    setup:
      "Vendor the WebEyeTrack browser build under prototype/public/lib/webeyetrack/ " +
      "(see https://arxiv.org/abs/2508.19544 and the project repo), wire the two TODOs " +
      "in trackers/webeyetrack.js to its API, then set available:true.",

    load: function (base) {
      this._base = base || "";
      if (!loaded) {
        // TODO(vendor): point at the actual WebEyeTrack entry script(s).
        loaded = window.WebEyeTrack
          ? Promise.resolve()
          : loadScript(this._base + "lib/webeyetrack/webeyetrack.js");
      }
      return loaded;
    },

    start: async function () {
      if (!window.WebEyeTrack) throw new Error("WebEyeTrack not loaded (vendor the library first)");
      // TODO(vendor): initialise the engine and begin the camera loop. Expected shape:
      //   this._engine = new WebEyeTrack({ faceMeshAssets: this._base + "mediapipe/face_mesh" });
      //   await this._engine.start();
      //   this._engine.onGaze(g => this._emit(g));   // g in viewport px, or null on lost face
      this._started = true;
    },

    // Bridge the engine's gaze events to the orchestrator's callback in the
    // WebGazer-compatible {x,y} viewport-pixel contract.
    _emit: function (g, clock) {
      window.GazePry._lastBeat = performance.now();
      if (this._cb) this._cb(g && g.x != null ? { x: g.x, y: g.y } : null, clock == null ? performance.now() : clock);
    },
    onGaze: function (cb) { this._cb = cb; },
    offGaze: function () { this._cb = null; },

    // Few-shot personalisation: feed each calibration click as a support sample.
    recordCalibration: function (x, y) {
      // TODO(vendor): this._engine.addCalibrationPoint(x, y);
    },
    clearModel: function () {
      // TODO(vendor): this._engine && this._engine.resetPersonalization();
    },
    showPreview: function () {},
    pause: function () { /* TODO(vendor): this._engine && this._engine.pause(); */ },
    resume: function () { /* TODO(vendor): return this._engine && this._engine.resume(); */ },
  };

  if (window.GazePry) window.GazePry.registerTracker(adapter);
  else console.error("[webeyetrack] gazepry-tracker.js must load before this adapter");
})();
