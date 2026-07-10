"""
Tests for the offline analysis (features.py, reid.py, simulate.py) plus a
cross-language parity check that the Python and JavaScript feature extractors
agree bit-for-bit. Pure stdlib unittest — no third-party test deps.

    python3 analysis/test_analysis.py            # from the repo root
    python3 -m unittest -v test_analysis         # from the analysis dir

The parity test shells out to `node test/features-cli.js`; it is skipped (not
failed) if node is unavailable.
"""
import contextlib
import io
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import warnings

# reid.load_sessions uses the repo's `json.load(open(...))` idiom; silence the
# resulting ResourceWarning so a passing run reads cleanly.
warnings.simplefilter("ignore", ResourceWarning)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import features  # noqa: E402
import reid  # noqa: E402
import simulate  # noqa: E402

SCREEN = {"innerW": 1440, "innerH": 900}
FEATURES_CLI = os.path.join(HERE, "..", "test", "features-cli.js")


def fixation(x, y, frames, t0=0):
    return [{"t": t0 + i * 33, "x": x, "y": y} for i in range(frames)]


def scan_stream(scale=1):
    spots = [(200, 200), (800, 300), (400, 600), (900, 650), (300, 400)]
    t, out = 0, []
    for x, y in spots:
        fx = fixation(x * scale, y * scale, 8, t)
        out += fx
        t = fx[-1]["t"] + 33
    return out


class TestFeatures(unittest.TestCase):
    def test_vector_length_and_finiteness(self):
        self.assertEqual(len(features.FEATURE_NAMES), 16)
        f = features.extract_features(scan_stream(), SCREEN)
        self.assertEqual(len(f), 16)
        self.assertTrue(all(math.isfinite(v) for v in f))

    def test_empty_and_all_gaps(self):
        self.assertEqual(len(features.extract_features([], SCREEN)), 16)
        gaps = [{"t": 0, "x": None, "y": None}, {"t": 33, "x": None, "y": None}]
        f = features.extract_features(gaps, SCREEN)
        self.assertTrue(all(math.isfinite(v) for v in f))

    def test_pure_fixation_has_no_saccades(self):
        f = features.extract_features(fixation(500, 500, 30), SCREEN)
        idx = features.FEATURE_NAMES.index
        self.assertEqual(f[idx("sacc_amp_mean")], 0)
        self.assertEqual(f[idx("sacc_rate")], 0)
        self.assertGreater(f[idx("fix_dur_mean")], 0)

    def test_scan_stream_has_saccades(self):
        f = features.extract_features(scan_stream(), SCREEN)
        idx = features.FEATURE_NAMES.index
        self.assertGreater(f[idx("sacc_amp_mean")], 0)
        self.assertGreater(f[idx("sacc_vel_mean")], 0)

    def test_scale_invariance(self):
        f1 = features.extract_features(scan_stream(1), {"innerW": 1440, "innerH": 900})
        f2 = features.extract_features(scan_stream(2), {"innerW": 2880, "innerH": 1800})
        for a, b, n in zip(f1, f2, features.FEATURE_NAMES):
            self.assertAlmostEqual(a, b, places=9, msg=f"{n} not scale-invariant")


class TestParity(unittest.TestCase):
    """The JS and Python extractors must stay in lockstep (README invariant)."""

    @unittest.skipUnless(shutil.which("node"), "node not available")
    def test_js_python_features_agree(self):
        for stream in (scan_stream(), fixation(500, 500, 20),
                       fixation(300, 300, 6) + [{"t": 300, "x": None, "y": None}] + fixation(900, 700, 6, 340)):
            payload = {"samples": stream, "screen": SCREEN}
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
                json.dump(payload, fh)
                tmp = fh.name
            try:
                out = subprocess.check_output(["node", FEATURES_CLI, tmp], text=True)
            finally:
                os.unlink(tmp)
            js = json.loads(out)
            py = features.extract_features(stream, SCREEN)
            self.assertEqual(len(js), len(py))
            for a, b, n in zip(js, py, features.FEATURE_NAMES):
                self.assertAlmostEqual(a, b, places=6, msg=f"JS/Py disagree on {n}")


class TestTrackerFamily(unittest.TestCase):
    def test_prefers_explicit_family(self):
        self.assertEqual(reid.tracker_family({"trackerFamily": "eyegestures", "tracker": "x-1"}), "eyegestures")

    def test_infers_from_full_id(self):
        self.assertEqual(reid.tracker_family({"tracker": "webgazer-3.5.3"}), "webgazer")

    def test_defaults_to_webgazer(self):
        self.assertEqual(reid.tracker_family({}), "webgazer")


class TestEligibility(unittest.TestCase):
    def _s(self, participant, session, task, tracker, file):
        return {"participant": participant, "session": session, "task": task,
                "tracker": tracker, "file": file}

    def test_never_matches_across_trackers(self):
        probe = self._s("P01", "S1", "reading", "webgazer", "a.json")
        cand = self._s("P02", "S2", "serp", "gazecloud", "b.json")
        self.assertFalse(reid.eligible(probe, cand, "all"))

    def test_same_file_excluded(self):
        probe = self._s("P01", "S1", "reading", "webgazer", "a.json")
        self.assertFalse(reid.eligible(probe, probe, "all"))

    def test_protocol_semantics(self):
        probe = self._s("P01", "S1", "reading", "webgazer", "a.json")
        cross_task_same_sess = self._s("P02", "S1", "serp", "webgazer", "b.json")
        same_task_cross_sess = self._s("P02", "S2", "reading", "webgazer", "c.json")
        cross_both = self._s("P02", "S2", "serp", "webgazer", "d.json")
        self.assertTrue(reid.eligible(probe, cross_task_same_sess, "cross_task"))
        self.assertFalse(reid.eligible(probe, same_task_cross_sess, "cross_task"))
        self.assertTrue(reid.eligible(probe, same_task_cross_sess, "same_task_cross_session"))
        self.assertTrue(reid.eligible(probe, cross_both, "cross_task_cross_session"))
        self.assertFalse(reid.eligible(probe, cross_task_same_sess, "cross_task_cross_session"))


class TestEvaluate(unittest.TestCase):
    def test_ranks_and_eer_on_a_tiny_separable_set(self):
        import numpy as np
        # two participants, two sessions, one task, clearly separable features
        def mk(p, s, feat):
            return {"file": f"{p}_{s}.json", "participant": p, "session": s,
                    "task": "reading", "tracker": "webgazer", "feat": np.array(feat, float)}
        base = [0.0] * 16
        sessions = [
            mk("P01", "S1", [i for i in range(16)]),
            mk("P01", "S2", [i + 0.1 for i in range(16)]),
            mk("P02", "S1", [i + 50 for i in range(16)]),
            mk("P02", "S2", [i + 50.1 for i in range(16)]),
        ]
        reid.standardize(sessions)
        res = reid.evaluate(sessions, "same_task_cross_session")
        self.assertEqual(res["rank1"], 1.0, "each session's nearest cross-session neighbour is its own identity")
        self.assertLess(res["eer"], 0.5)


class TestSimulate(unittest.TestCase):
    def test_gen_session_tags_tracker(self):
        traits = simulate.subject_traits(1)
        sess = simulate.gen_session("P01", "S1", "reading", traits, 123, tracker="webeyetrack")
        self.assertEqual(sess["tracker"], "webeyetrack")
        self.assertEqual(sess["trackerFamily"], "webeyetrack")
        self.assertTrue(sess["samples"])
        self.assertEqual(len(features.extract_features(sess["samples"], sess["screen"])), 16)


class TestLoadAndReportPerTracker(unittest.TestCase):
    def test_load_and_multitracker_split(self):
        tmp = tempfile.mkdtemp(prefix="gp-analysis-")
        try:
            for tr, seed in (("webgazer", 7), ("gazecloud", 9)):
                for si in range(4):
                    pid = f"P{si + 1:02d}"
                    traits = simulate.subject_traits(seed * 1000 + si)
                    for se in range(2):
                        for ti, task in enumerate(simulate.TASKS):
                            s = simulate.gen_session(pid, f"S{se+1}", task, traits,
                                                     seed * 100000 + si * 1000 + se * 100 + ti, tracker=tr)
                            fn = f"{pid}_S{se+1}_{task}_{tr}_{s['startedAt']}.json"
                            json.dump(s, open(os.path.join(tmp, fn), "w"))
            sessions = reid.load_sessions(tmp)
            self.assertEqual(len(sessions), 2 * 4 * 2 * len(simulate.TASKS))
            trackers = sorted(set(s["tracker"] for s in sessions))
            self.assertEqual(trackers, ["gazecloud", "webgazer"])
            # report_tracker on one family should score and never touch the other
            # (it prints a metrics table; capture that so test output stays clean)
            with contextlib.redirect_stdout(io.StringIO()):
                rows = reid.report_tracker([s for s in sessions if s["tracker"] == "webgazer"], "webgazer")
            self.assertTrue(rows)
            self.assertTrue(all(r["tracker"] == "webgazer" for r in rows))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
