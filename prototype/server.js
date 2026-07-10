/*
 * GazePry Direction 1 — collection + live re-ID server (zero dependencies).
 *
 *   node server.js [--port 8080] [--data ./data]
 *
 * Serves the capture harness from public/, ingests session logs to data/,
 * and exposes a live nearest-neighbour re-identification endpoint that links
 * a probe to an enrolled participant by gaze dynamics alone (no cookie).
 */
"use strict";
const http = require("http");
const fs = require("fs");
const path = require("path");
const reid = require("./reid-core");

function arg(name, def) {
  const i = process.argv.indexOf("--" + name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : def;
}
const PORT = parseInt(arg("port", process.env.PORT || "8080"), 10);
const PUBLIC = path.join(__dirname, "public");
const DATA = path.resolve(arg("data", path.join(__dirname, "data")));
fs.mkdirSync(DATA, { recursive: true });

const MIME = {
  ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
  ".map": "application/json", ".svg": "image/svg+xml", ".png": "image/png",
  ".jpg": "image/jpeg", ".ico": "image/x-icon",
  // MediaPipe FaceMesh runtime assets (public/mediapipe/face_mesh/)
  ".wasm": "application/wasm", ".data": "application/octet-stream",
  ".binarypb": "application/octet-stream",
};

function send(res, code, body, headers) {
  headers = headers || {};
  // permissive CORS so a cross-origin task page can POST to this collector
  headers["Access-Control-Allow-Origin"] = "*";
  headers["Access-Control-Allow-Headers"] = "Content-Type";
  headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS";
  res.writeHead(code, headers);
  res.end(body);
}
function sendJson(res, code, obj) {
  send(res, code, JSON.stringify(obj), { "Content-Type": "application/json" });
}
function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (c) => {
      data += c;
      if (data.length > 60 * 1024 * 1024) reject(new Error("body too large"));
    });
    req.on("end", () => resolve(data));
    req.on("error", reject);
  });
}
function safeName(s) { return String(s || "").replace(/[^a-zA-Z0-9._-]/g, "_"); }
// Tracker family (slug) for a session, tolerant of older records that only had
// the full tracker id (e.g. "webgazer-3.5.3" -> "webgazer").
function familyOf(sess) {
  return sess.trackerFamily || (sess.tracker ? String(sess.tracker).split("-")[0] : "webgazer");
}

// ---- gallery (features cached by filename+mtime) ------------------------
const featCache = new Map();
function loadGallery() {
  const gallery = [];
  for (const fn of fs.readdirSync(DATA)) {
    if (!fn.endsWith(".json")) continue;
    const fp = path.join(DATA, fn);
    let stat;
    try { stat = fs.statSync(fp); } catch (e) { continue; }
    const key = fn + ":" + stat.mtimeMs;
    let entry = featCache.get(fn);
    if (!entry || entry.key !== key) {
      let sess;
      try { sess = JSON.parse(fs.readFileSync(fp, "utf8")); } catch (e) { continue; }
      if (!sess.samples) continue;
      entry = {
        key,
        participant: sess.participant, session: sess.session, task: sess.task,
        tracker: sess.tracker, trackerFamily: familyOf(sess),
        features: reid.extractFeatures(sess.samples, sess.screen),
      };
      featCache.set(fn, entry);
    }
    gallery.push(entry);
  }
  return gallery;
}

// ---- static -------------------------------------------------------------
function serveStatic(req, res, pathname) {
  let rel = decodeURIComponent(pathname);
  if (rel === "/") rel = "/index.html";
  const fp = path.normalize(path.join(PUBLIC, rel));
  if (!fp.startsWith(PUBLIC)) return send(res, 403, "Forbidden");
  fs.readFile(fp, (err, buf) => {
    if (err) return send(res, 404, "Not found: " + rel);
    send(res, 200, buf, { "Content-Type": MIME[path.extname(fp)] || "application/octet-stream" });
  });
}

// ---- server -------------------------------------------------------------
const server = http.createServer(async (req, res) => {
  const u = new URL(req.url, "http://" + (req.headers.host || "localhost"));
  const pathname = u.pathname;
  const query = u.searchParams;

  if (req.method === "OPTIONS") return send(res, 204, "");

  // POST /ingest — store a captured session
  if (req.method === "POST" && pathname === "/ingest") {
    try {
      const sess = JSON.parse(await readBody(req));
      if (!sess.participant || !sess.session || !sess.task || !Array.isArray(sess.samples))
        return sendJson(res, 400, { error: "missing participant/session/task/samples" });
      const fn = [safeName(sess.participant), safeName(sess.session), safeName(sess.task),
        safeName(familyOf(sess)), Date.now()].join("_") + ".json";
      fs.writeFileSync(path.join(DATA, fn), JSON.stringify(sess));
      console.log(`ingest: ${fn} (${sess.samples.length} samples, ${sess.nGaps || 0} gaps)`);
      return sendJson(res, 200, { stored: fn });
    } catch (e) {
      return sendJson(res, 400, { error: String(e) });
    }
  }

  // GET /status — which tasks this participant/session/tracker has completed.
  // tracker is optional; when given, completion is scoped to that tracker so the
  // same session on a different tracker is tracked independently.
  if (req.method === "GET" && pathname === "/status") {
    const p = query.get("participant"), s = query.get("session"), tr = query.get("tracker");
    const tasks = loadGallery()
      .filter((g) => g.participant === p && g.session === s && (!tr || g.trackerFamily === tr))
      .map((g) => g.task);
    return sendJson(res, 200, { tasks: Array.from(new Set(tasks)) });
  }

  // GET /sessions — gallery metadata (for the re-ID demo UI). Optional ?tracker=
  // filters to one tracker family so the picker matches like-with-like.
  if (req.method === "GET" && pathname === "/sessions") {
    const tr = query.get("tracker");
    const g = loadGallery()
      .filter((e) => !tr || e.trackerFamily === tr)
      .map((e) => ({ participant: e.participant, session: e.session, task: e.task, tracker: e.trackerFamily }));
    const participants = Array.from(new Set(g.map((x) => x.participant)));
    const trackers = Array.from(new Set(loadGallery().map((e) => e.trackerFamily)));
    return sendJson(res, 200, { count: g.length, participants, trackers, sessions: g });
  }

  // POST /identify — live re-ID: link a probe to an enrolled participant
  if (req.method === "POST" && pathname === "/identify") {
    try {
      const body = JSON.parse(await readBody(req));
      if (!Array.isArray(body.samples)) return sendJson(res, 400, { error: "missing samples" });
      const probe = reid.extractFeatures(body.samples, body.screen);
      // Only rank against the same tracker: feature distributions differ across
      // trackers, so mixing them would be an unfair (and meaningless) comparison.
      const gallery = loadGallery().filter((g) => !body.tracker || g.trackerFamily === body.tracker);
      const result = reid.identify(probe, gallery, {
        excludeParticipant: body.excludeParticipant,
        excludeSession: body.excludeSession,
      });
      return sendJson(res, 200, {
        tracker: body.tracker || null,
        galleryParticipants: Array.from(new Set(gallery.map((g) => g.participant))),
        rank1: result.rank1,
        ranked: result.ranked.slice(0, 5),
      });
    } catch (e) {
      return sendJson(res, 400, { error: String(e) });
    }
  }

  return serveStatic(req, res, pathname);
});

server.listen(PORT, () => {
  console.log(`GazePry server → http://localhost:${PORT}`);
  console.log(`  web root: ${PUBLIC}`);
  console.log(`  data dir: ${DATA}`);
});
