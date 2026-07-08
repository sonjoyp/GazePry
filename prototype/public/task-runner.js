/*
 * Shared boot code for every task "site". A page includes this after
 * gazepry-tracker.js and provides a #gp-start button carrying:
 *   data-task="reading"  data-duration="90"
 */
(function () {
  "use strict";
  if (!GazePry.requireIdentity()) return; // redirects to the hub if no identity

  document.addEventListener("DOMContentLoaded", function () {
    var who = document.getElementById("gp-who");
    if (who) who.textContent = GazePry.identity.participant + " · " + GazePry.identity.session;

    var btn = document.getElementById("gp-start");
    if (!btn) return;
    var task = btn.dataset.task;
    var dur = parseInt(btn.dataset.duration || "60", 10);

    // Pre-boot the engine while the participant reads the page, so the click
    // starts capturing immediately instead of spending the first seconds of
    // the recording window on WebGazer boot (which would log only gaps).
    var label = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Starting camera…";
    GazePry.startEngine()
      .catch(function (e) { console.error("[GazePry] engine pre-boot failed:", e); })
      .then(function () {
        btn.disabled = false;
        btn.textContent = label;
      });

    btn.addEventListener("click", async function () {
      var bar = document.getElementById("gp-startbar");
      if (bar) bar.style.display = "none";
      btn.disabled = true;
      var res = await GazePry.runTask({ task: task, durationSec: dur });

      // local fallback record of completion (server /status is authoritative)
      try {
        var key = "gp_done_" + GazePry.identity.participant + "_" + GazePry.identity.session;
        var done = JSON.parse(localStorage.getItem(key) || "[]");
        if (done.indexOf(task) < 0) done.push(task);
        localStorage.setItem(key, JSON.stringify(done));
      } catch (e) {}

      showDone(res, task);
    });
  });

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
