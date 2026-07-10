/*
 * GazeCloudAPI (GazeRecorder) adapter — a high-accuracy, self-calibrating webcam
 * tracker that is trivial to drop in. NOTE: it is CLOSED-SOURCE and CLOUD-BASED —
 * webcam frames are processed on GazeRecorder's servers. For a privacy paper that
 * is itself a finding: include it as the "high-accuracy commodity" contrast point,
 * but flag in the writeup that, unlike WebGazer/WebEyeTrack/EyeGestures, video
 * leaves the machine (privacy = "cloud").
 *
 * Docs: https://gazerecorder.com/gazecloudapi/
 * Implements the GazePry tracker-adapter contract (see README-adapter.md).
 */
(function () {
  "use strict";

  var SCRIPT_URL = "https://api.gazerecorder.com/GazeCloudAPI.js";
  var loaded = null;

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = function () { reject(new Error("failed to load " + src + " (needs internet)")); };
      document.head.appendChild(s);
    });
  }

  var adapter = {
    id: "gazecloud-api",
    family: "gazecloud",
    label: "GazeCloud (GazeRecorder)",
    hint: "High-accuracy, self-calibrating. CLOSED-SOURCE + CLOUD: webcam frames are sent to GazeRecorder servers.",
    privacy: "cloud",
    needsCalibration: false, // runs its own calibration overlay inside start()
    available: true,
    startTimeoutMs: 90000, // its calibration is user-paced; don't time it out early

    load: function () {
      if (!loaded) loaded = window.GazeCloudAPI ? Promise.resolve() : loadScript(SCRIPT_URL);
      return loaded;
    },

    start: function () {
      if (!window.GazeCloudAPI) throw new Error("GazeCloudAPI not loaded");
      var self = this;
      this._cb = null;
      // GazeCloud gives GazeX/GazeY (screen) and docX/docY (document); state 0 = valid.
      // Convert document coords to viewport pixels to match the WebGazer contract.
      window.GazeCloudAPI.OnResult = function (g) {
        window.GazePry._lastBeat = performance.now();
        if (!self._cb) return;
        var clock = performance.now();
        if (g && g.state === 0) {
          self._cb({ x: g.docX - (window.scrollX || 0), y: g.docY - (window.scrollY || 0) }, clock);
        } else {
          self._cb(null, clock); // no valid gaze this frame (blink / lost / off-screen)
        }
      };
      return new Promise(function (resolve) {
        var done = false;
        window.GazeCloudAPI.OnCalibrationComplete = function () { if (!done) { done = true; resolve(); } };
        // If the host wants click-refinement during use, uncomment:
        // window.GazeCloudAPI.UseClickRecalibration = true;
        try { window.GazeCloudAPI.StartEyeTracking(); } catch (e) { console.error("[gazecloud] start error:", e); resolve(); }
        // Safety net if OnCalibrationComplete never fires.
        setTimeout(function () { if (!done) { done = true; resolve(); } }, adapter.startTimeoutMs);
      });
    },

    onGaze: function (cb) { this._cb = cb; },
    offGaze: function () { this._cb = null; },

    // Self-calibrating: no click training, and there is no client-side model to
    // clear (identity was never stored in the browser — the "unclearable" point).
    recordCalibration: function () {},
    clearModel: function () {},

    showPreview: function () {}, // GazeCloud manages its own on-screen UI
  };

  if (window.GazePry) window.GazePry.registerTracker(adapter);
  else console.error("[gazecloud] gazepry-tracker.js must load before this adapter");
})();
