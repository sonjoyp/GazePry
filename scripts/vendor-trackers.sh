#!/usr/bin/env bash
#
# vendor-trackers.sh — download the third-party webcam eye-tracker libraries the
# harness depends on into public/, so the WebEyeTrack and EyeGestures arms can
# run without a build step. Idempotent: safe to re-run.
#
# Vendored (all open-source / freely distributed):
#   WebEyeTrack (MIT, RedForestAi/WebEyeTrack) -> public/lib/webeyetrack/ + public/web/
#   EyeGestures Lite (NativeSensors) hosted build + deps -> public/lib/eyegestures/
#
# Both do gaze inference ON-DEVICE (no video leaves the machine). They do fetch
# model/wasm assets from CDNs at load time (Google/jsdelivr for MediaPipe; the
# EyeGestures WASM engine is vendored locally here). That is download-only and
# does not upload any camera data.
#
# Usage:  bash scripts/vendor-trackers.sh   (from the repo root)
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"      # repo root
PUB="$HERE/public"
LIB="$PUB/lib"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

say() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
get() { # url dest
  curl -fsSL --retry 3 -m 120 "$1" -o "$2"
  printf '   %8d  %s\n' "$(wc -c < "$2")" "${2#$PUB/}"
}

# ---------------------------------------------------------------------------
say "WebEyeTrack (npm: webeyetrack@0.0.2, MIT)"
mkdir -p "$LIB/webeyetrack" "$PUB/web"
( cd "$TMP" && npm pack webeyetrack@0.0.2 >/dev/null 2>&1 )
TGZ="$(ls "$TMP"/webeyetrack-*.tgz | head -1)"
tar xzf "$TGZ" -C "$TMP"
cp "$TMP/package/dist/index.js"             "$LIB/webeyetrack/webeyetrack.js"
cp "$TMP/package/dist/index.js.LICENSE.txt" "$LIB/webeyetrack/webeyetrack.js.LICENSE.txt" 2>/dev/null || true
printf '   %8d  %s\n' "$(wc -c < "$LIB/webeyetrack/webeyetrack.js")" "lib/webeyetrack/webeyetrack.js (UMD, exports on window)"

# BlazeGaze TF.js model — BlazeGaze.ts loads it from `${origin}/web/model.json`,
# so it must sit at the SERVER ROOT path /web/ (i.e. public/web/).
WET_RAW="https://raw.githubusercontent.com/RedForestAi/WebEyeTrack/main/js/examples/minimal-example/public/web"
get "$WET_RAW/model.json"            "$PUB/web/model.json"
get "$WET_RAW/group1-shard1of1.bin"  "$PUB/web/group1-shard1of1.bin"
get "https://raw.githubusercontent.com/RedForestAi/WebEyeTrack/main/LICENSE" "$LIB/webeyetrack/LICENSE"

# ---------------------------------------------------------------------------
say "EyeGestures Lite (hosted build + WASM engine + deps)"
mkdir -p "$LIB/eyegestures"
EG="https://eyegestures.com"
get "$EG/eyegestures.js"               "$LIB/eyegestures/eyegestures.js"
get "$EG/EyegesturesEngine.js"         "$LIB/eyegestures/EyegesturesEngine.js"
get "$EG/EyegesturesEngine_bg.wasm"    "$LIB/eyegestures/EyegesturesEngine_bg.wasm"
get "$EG/eyegestures.css"              "$LIB/eyegestures/eyegestures.css"
# External runtime deps the EyeGestures docs require (vendored so nothing but
# MediaPipe face-mesh is fetched off-site at runtime).
get "https://www.lactame.com/lib/ml/6.0.0/ml.min.js"                 "$LIB/eyegestures/ml.min.js"
get "https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.8.0/math.min.js" "$LIB/eyegestures/math.min.js"
get "https://raw.githubusercontent.com/NativeSensors/EyeGesturesLite/main/License" "$LIB/eyegestures/License" || true

say "Done. Vendored trackers are under public/lib/ and public/web/."
echo "Enable them by confirming available:true in trackers/webeyetrack.js and trackers/eyegestures.js (already set)."
