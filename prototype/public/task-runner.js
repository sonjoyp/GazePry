/*
 * Shared boot code for every task "site". A page includes this after
 * gazepry-tracker.js and provides a #gp-start element carrying:
 *   data-task="reading"  data-duration="90"
 *
 * The flow is hands-free: the camera pre-boots while the participant reads the
 * page, then a short countdown runs, then recording starts automatically. The
 * #gp-start element is kept only as the source of the data-task / data-duration
 * config — it is hidden, never clicked.
 */
(function () {
  "use strict";
  if (!GazePry.requireIdentity()) return; // redirects to the hub if no identity

  document.addEventListener("DOMContentLoaded", function () {
    var who = document.getElementById("gp-who");
    if (who) {
      var t = GazePry.getTracker(GazePry.identity.tracker);
      who.textContent = GazePry.identity.participant + " · " + GazePry.identity.session +
        " · " + (t ? t.label : GazePry.identity.tracker);
    }

    var cfg = document.getElementById("gp-start");
    if (!cfg) return;
    var task = cfg.dataset.task;
    var dur = parseInt(cfg.dataset.duration || "60", 10);

    // Hide the (now vestigial) start button and replace it with a status line.
    cfg.style.display = "none";
    var status = document.createElement("span");
    status.className = "gp-note";
    status.id = "gp-status";
    status.textContent = "Starting camera…";
    cfg.parentNode.insertBefore(status, cfg);

    run(task, dur, status);
  });

  async function run(task, dur, status) {
    // Pre-boot the engine BEFORE the countdown so WebGazer warm-up (which logs
    // only gaps) and the participant's page-orientation gaze never enter the
    // recording window. Only once the camera is producing predictions do we
    // count down and start capturing.
    try {
      await GazePry.startEngine();
    } catch (e) {
      console.error("[GazePry] engine boot failed:", e);
      status.textContent = "Camera failed to start — see console (F12).";
      return;
    }
    status.textContent = "Camera ready.";
    await countdown(3, "Get ready — recording starts in");

    var bar = document.getElementById("gp-startbar");
    if (bar) bar.style.display = "none";

    var res = await GazePry.runTask({ task: task, durationSec: dur });

    // local fallback record of completion (server /status is authoritative)
    try {
      var key = "gp_done_" + GazePry.identity.participant + "_" + GazePry.identity.session +
        "_" + (GazePry.identity.tracker || "");
      var done = JSON.parse(localStorage.getItem(key) || "[]");
      if (done.indexOf(task) < 0) done.push(task);
      localStorage.setItem(key, JSON.stringify(done));
    } catch (e) {}

    showDone(res, task);
  }

  // Full-screen "Get ready… 3-2-1" overlay that auto-dismisses, then resolves.
  function countdown(seconds, msg) {
    return new Promise(function (resolve) {
      var ov = document.createElement("div");
      ov.id = "gp-countdown";
      var m = document.createElement("div");
      m.className = "gp-cd-msg";
      m.textContent = msg;
      var n = document.createElement("div");
      n.className = "gp-cd-num";
      n.textContent = seconds;
      ov.appendChild(m);
      ov.appendChild(n);
      document.body.appendChild(ov);

      var left = seconds;
      var iv = setInterval(function () {
        left--;
        if (left <= 0) {
          clearInterval(iv);
          ov.remove();
          resolve();
        } else {
          n.textContent = left;
        }
      }, 1000);
    });
  }

  function showDone(res, task) {
    var via =
      res.submit.via === "server"
        ? "Saved to server: <code>" + (res.submit.stored || "") + "</code>"
        : "Server unavailable — downloaded <code>" + (res.submit.file || "") +
          "</code> (move it into <code>prototype/data/</code>)";
    var d = document.createElement("div");
    d.className = "gp-card gp-done";
    d.innerHTML =
      "<h2>Task complete: " + task + "</h2>" +
      '<p class="gp-note">' + res.session.nSamples + " gaze samples, " +
      res.session.nGaps + " gaps, in " + Math.round(res.session.durationMs / 1000) + " s.</p>" +
      '<p class="gp-note">' + via + "</p>" +
      '<div class="gp-row"><a class="gp-btn" href="../index.html">&larr; Back to tasks</a></div>';
    document.body.appendChild(d);
  }
})();
