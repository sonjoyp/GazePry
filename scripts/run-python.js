/*
 * run-python.js — resolve a Python interpreter, then run a script with it.
 *
 *   node scripts/run-python.js analysis/test_analysis.py [args...]
 *
 * Exists because `python3` is not a valid command on a default Windows install
 * (where the launcher is `py` and the interpreter is `python`), while `python`
 * on some Linux distros is either absent or still Python 2. Hardcoding either
 * one breaks `npm test` for half the people who clone this repo.
 *
 * It probes candidates in order and picks the first that reports Python >= 3.
 * The chosen interpreter's exit code is propagated unchanged, so a genuine test
 * failure is never masked by the fallback logic — the only thing being retried
 * is "does this interpreter exist", never "did the script pass".
 */
"use strict";
const { spawnSync } = require("child_process");

const CANDIDATES = ["python3", "python", "py"];

function version(cmd) {
  // `py` needs -3 to select a Python 3 launcher target.
  const args = cmd === "py" ? ["-3", "--version"] : ["--version"];
  const r = spawnSync(cmd, args, { encoding: "utf8" });
  if (r.error || r.status !== 0) return null;
  const m = String(r.stdout || r.stderr).match(/Python (\d+)\.(\d+)/);
  if (!m || parseInt(m[1], 10) < 3) return null;
  return { cmd, prefix: cmd === "py" ? ["-3"] : [], label: m[0] };
}

const script = process.argv[2];
if (!script) {
  console.error("usage: node scripts/run-python.js <script.py> [args...]");
  process.exit(2);
}

let chosen = null;
for (const c of CANDIDATES) {
  chosen = version(c);
  if (chosen) break;
}
if (!chosen) {
  console.error(
    "No Python 3 interpreter found (tried: " + CANDIDATES.join(", ") + ").\n" +
    "Install Python 3 and make sure it is on PATH, then re-run."
  );
  process.exit(127);
}

const rest = process.argv.slice(3);
const run = spawnSync(chosen.cmd, [...chosen.prefix, script, ...rest], { stdio: "inherit" });
if (run.error) {
  console.error("failed to run " + chosen.cmd + ": " + run.error.message);
  process.exit(1);
}
process.exit(run.status === null ? 1 : run.status);
