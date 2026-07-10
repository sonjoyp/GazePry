/*
 * EyeGestures adapter — an actively-maintained open-source webcam tracker
 * (NativeSensors / EyeGestures Lite). A Rust/WASM engine + JS shim that runs in
 * the browser; gaze inference is on-device (video stays local). A good
 * open-source second commodity arm alongside WebGazer.
 *
 * Vendored by scripts/vendor-trackers.sh into ../lib/eyegestures/. At runtime it
 * additionally fetches MediaPipe face-mesh from jsDelivr (download-only; no
 * camera data leaves the machine).
 *
 * Real API (EyeGestures Lite v4): a global `EyeGestures` class —
 *   const g = new EyeGestures(videoElementId, onPoint);
 *   g.invisible(); g.start();
 *   // onPoint([x, y], calibrated): x/y are VIEWPORT pixels; calibrated=false
 *   //   while its built-in calibration is still converging, true once ready.
 * It self-calibrates (no click grid), so needsCalibration:false.
 *
 * Implements the GazePry tracker-adapter contract (see README-adapter.md).
 */
(function () {
  "use strict";

  var loaded = null;
  function loadScript(src, module) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      if (module) s.type = "module";
      s.onload = resolve;
      s.onerror = function () { reject(new Error("failed to load " + src)); };
      document.head.appendChild(s);
    });
  }
  function loadCss(href) {
    if (document.querySelector('link[href="' + href + '"]')) return;
    var l = document.createElement("link");
    l.rel = "stylesheet"; l.href = href;
    document.head.appendChild(l);
  }
  // EyeGestures uses getElementById("video"/"status"/"error"); create hidden ones.
  function ensureEl(tag, id) {
    var el = document.getElementById(id);
    if (!el) {
      el = document.createElement(tag);
      el.id = id;
      el.style.display = "none";
      document.body.appendChild(el);
    }
    return el;
  }

  var adapter = {
    id: "eyegestures-lite-4",
    family: "eyegestures",
    label: "EyeGestures",
    hint: "Open-source Rust/WASM webcam engine, in-browser (video stays local; MediaPipe assets load from CDN). Self-calibrating.",
    privacy: "local",
    needsCalibration: false, // runs its own calibration inside start()
    available: true,
    startTimeoutMs: 60000, // its calibration is user-paced

    load: function (base) {
      this._base = base || "";
      var dir = this._base + "lib/eyegestures/";
      if (!loaded) {
        loadCss(dir + "eyegestures.css");
        // Point the engine loader at the vendored WASM module (else it resolves
        // EyegesturesEngine.js relative to the script and re-fetches from origin).
        window.EyeGesturesEngineModuleUrl = dir + "EyegesturesEngine.js";
        // Documented external deps, vendored locally; then the tracker itself.
        loaded = loadScript(dir + "ml.min.js")
          .then(function () { return loadScript(dir + "math.min.js"); })
          .then(function () { return window.EyeGestures ? null : loadScript(dir + "eyegestures.js"); });
      }
      return loaded;
    },

    start: function () {
      if (!window.EyeGestures) throw new Error("EyeGestures not loaded (run scripts/vendor-trackers.sh)");
      var self = this;
      this._cb = null;
      this._video = ensureEl("video", "video");
      this._video.setAttribute("autoplay", "");
      this._video.setAttribute("playsinline", "");
      ensureEl("div", "status");
      ensureEl("div", "error");

      return new Promise(function (resolve) {
        var settled = false;
        function onPoint(point, calibrated) {
          window.GazePry._lastBeat = performance.now();
          if (!settled && calibrated) { settled = true; resolve(); } // ready once calibrated
          if (self._cb && point) self._cb({ x: point[0], y: point[1] }, performance.now());
          else if (self._cb) self._cb(null, performance.now());
        }
        self._engine = new window.EyeGestures("video", onPoint);
        self._engine.invisible();       // hide the blue gaze cursor during tasks
        self._engine.start();           // shows its calibration, then streams gaze
        // Safety net: proceed even if the "calibrated" flag never flips.
        setTimeout(function () { if (!settled) { settled = true; resolve(); } }, adapter.startTimeoutMs);
      });
    },

    onGaze: function (cb) { this._cb = cb; },
    offGaze: function () { this._cb = null; },

    // Self-calibrating: the click grid is skipped (needsCalibration:false) and
    // there is no client-side identity model to clear.
    recordCalibration: function () {},
    clearModel: function () { try { this._engine && this._engine.recalibrate(); } catch (e) {} },
    showPreview: function (show) { try { show ? this._engine.visible() : this._engine.invisible(); } catch (e) {} },
    stop: function () { try { this._engine && this._engine.stop(); } catch (e) {} },
  };

  if (window.GazePry) window.GazePry.registerTracker(adapter);
  else console.error("[eyegestures] gazepry-tracker.js must load before this adapter");
})();
