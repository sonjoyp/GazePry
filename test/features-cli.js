/*
 * features-cli.js — tiny CLI wrapper around reid-core.extractFeatures, used by
 * the Python parity test (analysis/test_analysis.py) to prove the JS and Python
 * feature extractors agree bit-for-bit on the same input.
 *
 *   node test/features-cli.js <session.json>
 *
 * where <session.json> is { "samples": [...], "screen": {...} }. Prints the
 * feature vector as a JSON array on stdout.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const reid = require(path.join(__dirname, "..", "reid-core"));

const fp = process.argv[2];
if (!fp) {
  console.error("usage: node features-cli.js <session.json>");
  process.exit(2);
}
const input = JSON.parse(fs.readFileSync(fp, "utf8"));
process.stdout.write(JSON.stringify(reid.extractFeatures(input.samples, input.screen)));
