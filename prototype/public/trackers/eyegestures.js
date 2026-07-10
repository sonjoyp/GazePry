/*
 * EyeGestures adapter — an actively-maintained open-source webcam tracker
 * (NativeSensors/EyeGestures). V4+ ships a shared Rust/WASM engine with a
 * JavaScript web build, so it runs straight in the browser (video stays local).
 * A good open-source second commodity arm alongside WebGazer.
 *
 * STATUS: available:false until you vendor the EyeGestures web build. The adapter
 * is written against its documented shape; wire the TODOs to the actual API, drop
 * the assets under lib/eyegestures/, and flip available:true. Implements the
 * GazePry tracker-adapter contract.
 *
 * Docs: https://eyegestures.com/  ·  https://github.com/NativeSensors/EyeGestures
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
    id: "eyegestures-v4",
    family: "eyegestures",
    label: "EyeGestures",
    hint: "Open-source Rust/WASM webcam engine, in-browser (video stays local). Uses a moving-dot calibration.",
    privacy: "local",
    needsCalibration: true, // its calibration takes on-screen target points; the click grid supplies them
    available: false,
    setup:
      "Vendor the EyeGestures web/WASM build under prototype/public/lib/eyegestures/ " +
      "(see https://github.com/NativeSensors/EyeGestures), wire the TODOs in " +
      "trackers/eyegestures.js to its API, then set available:true.",

    load: function (base) {
      this._base = base || "";
      if (!loaded) {
        // TODO(vendor): point at the actual EyeGestures web entry script(s).
        loaded = window.EyeGestures
          ? Promise.resolve()
          : loadScript(this._base + "lib/eyegestures/eyegestures.js");
      }
      return loaded;
    },

    start: async function () {
      if (!window.EyeGestures) throw new Error("EyeGestures not loaded (vendor the library first)");
      // TODO(vendor): construct + start the engine and route gaze events. Expected shape:
      //   this._engine = new EyeGestures.WebEngine();
      //   await this._engine.start();
      //   this._engine.on("gaze", g => this._emit(g)); // g.point = [x,y] viewport px; g.blink -> null
      this._started = true;
    },

    _emit: function (g, clock) {
      window.GazePry._lastBeat = performance.now();
      var pt = g && !g.blink && g.point ? { x: g.point[0], y: g.point[1] } : null;
      if (this._cb) this._cb(pt, clock == null ? performance.now() : clock);
    },
    onGaze: function (cb) { this._cb = cb; },
    offGaze: function () { this._cb = null; },

    recordCalibration: function (x, y) {
      // TODO(vendor): this._engine.calibratePoint(x, y);
    },
    clearModel: function () {
      // TODO(vendor): this._engine && this._engine.resetCalibration();
    },
    showPreview: function () {},
    pause: function () { /* TODO(vendor): this._engine && this._engine.pause(); */ },
    resume: function () { /* TODO(vendor): return this._engine && this._engine.resume(); */ },
  };

  if (window.GazePry) window.GazePry.registerTracker(adapter);
  else console.error("[eyegestures] gazepry-tracker.js must load before this adapter");
})();
