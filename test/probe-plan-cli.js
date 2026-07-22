/*
 * probe-plan-cli.js — CLI wrapper around ProbeProtocol.buildTrials, used by the
 * Python parity test (analysis/test_analysis.py::TestProbeProtocolParity) to
 * prove the browser protocol and the Python port build the SAME design.
 *
 *   node test/probe-plan-cli.js <participant> <experiment> <arrayN> <nTrials>
 *
 * Prints a compact plan as JSON on stdout: the counterbalance group plus, per
 * trial, the slot order as [itemId, familiar] pairs. Item content is not
 * printed — only what the design determines.
 */
"use strict";
const path = require("path");
const P = require(path.join(__dirname, "..", "public", "probe-protocol.js"));

const [participant, experiment, arrayN, nTrials] = process.argv.slice(2);
if (!participant) {
  console.error("usage: node probe-plan-cli.js <participant> <experiment> <arrayN> <nTrials>");
  process.exit(2);
}
const built = P.buildTrials({
  participant,
  experiment: experiment || "E1",
  arrayN: parseInt(arrayN || "4", 10),
  nTrials: parseInt(nTrials || "40", 10),
});
process.stdout.write(JSON.stringify({
  participant: built.participant,
  experiment: built.experiment,
  arrayN: built.arrayN,
  counterbalanceGroup: built.counterbalanceGroup,
  nTrials: built.nTrials,
  trials: built.trials.map((t) => ({
    index: t.index,
    probeItemId: t.probeItemId,
    slots: t.slots.map((s) => [s.itemId, s.familiar]),
  })),
}));
