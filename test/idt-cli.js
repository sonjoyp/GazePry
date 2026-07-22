/*
 * idt-cli.js — CLI wrapper around reid-core.detectFixationsIDT, used by the
 * Python parity test (analysis/test_analysis.py::TestIDTParity) to prove the JS
 * and Python fixation detectors segment identically.
 *
 *   node test/idt-cli.js <input.json>
 *
 * where <input.json> is { "samples": [...], "screen": {...},
 *                         "dispersion"?: n, "minDurMs"?: n, "smoothWin"?: n }.
 * Prints the fixation list as JSON on stdout.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const reid = require(path.join(__dirname, "..", "reid-core"));

const fp = process.argv[2];
if (!fp) {
  console.error("usage: node idt-cli.js <input.json>");
  process.exit(2);
}
const input = JSON.parse(fs.readFileSync(fp, "utf8"));
const opts = {};
if (input.dispersion != null) opts.dispersion = input.dispersion;
if (input.minDurMs != null) opts.minDurMs = input.minDurMs;
if (input.smoothWin != null) opts.smoothWin = input.smoothWin;
process.stdout.write(JSON.stringify(reid.detectFixationsIDT(input.samples, input.screen, opts)));
