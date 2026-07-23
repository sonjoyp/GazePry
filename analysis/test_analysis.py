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

import aoi_features  # noqa: E402
import features  # noqa: E402
import labels  # noqa: E402
import probe_protocol  # noqa: E402
import recognition  # noqa: E402
import reid  # noqa: E402
import simulate  # noqa: E402
import simulate_probe  # noqa: E402

SCREEN = {"innerW": 1440, "innerH": 900}
BIG_SCREEN = {"innerW": 1920, "innerH": 1080}
FEATURES_CLI = os.path.join(HERE, "..", "test", "features-cli.js")
IDT_CLI = os.path.join(HERE, "..", "test", "idt-cli.js")
PROBE_PLAN_CLI = os.path.join(HERE, "..", "test", "probe-plan-cli.js")


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


class TestResample(unittest.TestCase):
    """Rate equalization (the pilot's identity<->cadence confound control)."""

    def _hz(self, samples):
        dur = (samples[-1]["t"] - samples[0]["t"]) / 1000.0
        return len(samples) / dur if dur > 0 else 0.0

    def test_noop_when_hz_none_or_too_short(self):
        s = fixation(100, 100, 10)
        self.assertIs(features.resample(s, None), s)          # hz falsy -> unchanged object
        one = [{"t": 0, "x": 1, "y": 1}]
        self.assertIs(features.resample(one, 30), one)        # <2 samples -> unchanged object

    def test_decimates_a_fast_stream_toward_target(self):
        # 100 Hz stream (10 ms spacing) resampled to ~30 Hz should thin out.
        fast = [{"t": i * 10, "x": 500, "y": 500} for i in range(200)]  # 2 s @ 100 Hz
        out = features.resample(fast, 30)
        self.assertLess(len(out), len(fast))
        self.assertAlmostEqual(self._hz(out), 30, delta=6)

    def test_preserves_gaps(self):
        s = fixation(200, 200, 30) + [{"t": 1000, "x": None, "y": None}] + fixation(400, 400, 30, 1040)
        out = features.resample(s, 30)
        self.assertTrue(any(p["x"] is None for p in out), "a gap survives resampling")

    @unittest.skipUnless(shutil.which("node"), "node not available")
    def test_js_python_resample_parity(self):
        fast = [{"t": i * 9, "x": 300 + (i % 7) * 20, "y": 400 + (i % 5) * 15} for i in range(160)]
        payload = {"samples": fast, "screen": SCREEN, "resampleHz": 30}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(payload, fh)
            tmp = fh.name
        try:
            out = subprocess.check_output(["node", FEATURES_CLI, tmp], text=True)
        finally:
            os.unlink(tmp)
        js = json.loads(out)
        py = features.extract_features(fast, SCREEN, resample_hz=30)
        for a, b, n in zip(js, py, features.FEATURE_NAMES):
            self.assertAlmostEqual(a, b, places=6, msg=f"JS/Py resample disagree on {n}")


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

    def test_min_gap_days_gates_cross_session(self):
        DAY = 86400_000
        probe = dict(self._s("P01", "S1", "reading", "webgazer", "a.json"), startedAt=0)
        near = dict(self._s("P01", "S2", "serp", "webgazer", "b.json"), startedAt=DAY)      # 1 day later
        far = dict(self._s("P01", "S3", "serp", "webgazer", "c.json"), startedAt=10 * DAY)  # 10 days later
        # default (no gate) still counts a different session id as cross-session
        self.assertTrue(reid.eligible(probe, near, "cross_task_cross_session"))
        # with a >=7-day gate, the same-week pair is excluded, the far pair kept
        self.assertFalse(reid.eligible(probe, near, "cross_task_cross_session", min_gap_days=7))
        self.assertTrue(reid.eligible(probe, far, "cross_task_cross_session", min_gap_days=7))

    def test_min_gap_days_excludes_unknown_timestamps(self):
        # startedAt missing -> the gap can't be confirmed -> excluded (conservative)
        probe = self._s("P01", "S1", "reading", "webgazer", "a.json")
        cand = self._s("P01", "S2", "serp", "webgazer", "b.json")
        self.assertFalse(reid.eligible(probe, cand, "cross_task_cross_session", min_gap_days=7))


class TestDataQualityGuard(unittest.TestCase):
    """load_sessions drops sessions too degraded to yield trustworthy features."""

    def _write(self, tmp, name, samples):
        rec = {"schema": "gazepry.session.v2", "participant": name.split("_")[0],
               "session": "S1", "task": "reading", "tracker": "webgazer",
               "trackerFamily": "webgazer", "startedAt": 1700000000000,
               "screen": {"innerW": 1440, "innerH": 900}, "samples": samples}
        json.dump(rec, open(os.path.join(tmp, name + ".json"), "w"))

    def test_drops_all_gap_and_too_short_keeps_good(self):
        tmp = tempfile.mkdtemp(prefix="gp-qual-")
        try:
            good = [{"t": i * 33, "x": 500 + (i % 5), "y": 400 + (i % 3)} for i in range(200)]  # ~6.6 s
            allgap = [{"t": i * 33, "x": None, "y": None} for i in range(200)]                   # 0% valid
            tooshort = [{"t": i * 33, "x": 500, "y": 400} for i in range(5)]                     # n<20
            self._write(tmp, "P01_S1_reading_1", good)
            self._write(tmp, "P02_S1_reading_2", allgap)
            self._write(tmp, "P03_S1_reading_3", tooshort)
            with contextlib.redirect_stdout(io.StringIO()):
                sessions = reid.load_sessions(tmp, verbose=True)
            kept = sorted(s["participant"] for s in sessions)
            self.assertEqual(kept, ["P01"], "only the usable session survives the guard")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


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


class TestConditionAndControls(unittest.TestCase):
    def _write_sim(self, tmp, subjects=6, sessions=2, tracker="webgazer", seed=7):
        for si in range(subjects):
            pid = f"P{si + 1:02d}"
            traits = simulate.subject_traits(seed * 1000 + si)
            for se in range(sessions):
                for ti, task in enumerate(simulate.TASKS):
                    s = simulate.gen_session(pid, f"S{se+1}", task, traits,
                                             seed * 100000 + si * 1000 + se * 100 + ti, tracker=tracker)
                    fn = f"{pid}_S{se+1}_{task}_{tracker}_{s['startedAt']}.json"
                    json.dump(s, open(os.path.join(tmp, fn), "w"))

    def test_load_carries_condition_and_samples(self):
        tmp = tempfile.mkdtemp(prefix="gp-cond-")
        try:
            self._write_sim(tmp, subjects=3, sessions=2)
            sessions = reid.load_sessions(tmp)
            self.assertTrue(sessions)
            s = sessions[0]
            self.assertEqual(s["intervention"], "baseline")          # v2 condition carried
            self.assertIn("condition", s)
            self.assertTrue(s["samples"])                            # raw samples retained
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_window_sweep_runs_and_full_matches_default(self):
        tmp = tempfile.mkdtemp(prefix="gp-win-")
        try:
            self._write_sim(tmp, subjects=6, sessions=2)
            sessions = reid.load_sessions(tmp)
            with contextlib.redirect_stdout(io.StringIO()):
                rows = reid.window_sweep(sessions, "webgazer", windows=(5, None))
            self.assertEqual(len(rows), 2)
            # the "full" window should score at least as many probes as a 5s cut
            full = [r for r in rows if r["window_s"] == "full"][0]
            self.assertGreaterEqual(full["n_probes_scored"], 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_shuffle_null_collapses_to_chance(self):
        tmp = tempfile.mkdtemp(prefix="gp-null-")
        try:
            self._write_sim(tmp, subjects=8, sessions=2)
            sessions = reid.load_sessions(tmp)
            with contextlib.redirect_stdout(io.StringIO()):
                res = reid.shuffle_null(sessions, "webgazer", n_perm=10)
            # real signal beats chance; shuffled labels sit near chance
            self.assertGreater(res["real"]["rank1"], res["real"]["chance_rank1"])
            self.assertLessEqual(res["shuffled_rank1_mean"], res["real"]["chance_rank1"] * 2 + 1e-9)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_gallery_sweep_and_within_session_run(self):
        tmp = tempfile.mkdtemp(prefix="gp-gal-")
        try:
            self._write_sim(tmp, subjects=6, sessions=2)
            sessions = reid.load_sessions(tmp)
            with contextlib.redirect_stdout(io.StringIO()):
                grows = reid.gallery_sweep(sessions, "webgazer", sizes=(3, None))
                wr = reid.within_session_bound(sessions, "webgazer")
            self.assertEqual(len(grows), 2)
            self.assertIsNotNone(wr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


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


# =========================================================================
# Direction D7 — recognition & concealed-knowledge leakage
# =========================================================================

def steady(x, y, ms, t0=0, step=16):
    return [{"t": t0 + t, "x": x, "y": y} for t in range(0, ms, step)]


class TestIDT(unittest.TestCase):
    """The dispersion-threshold detector that produces D7's fixation durations."""

    def test_clean_dwell_is_one_fixation(self):
        f = features.detect_fixations_idt(steady(500, 400, 600), BIG_SCREEN)
        self.assertEqual(len(f), 1)
        self.assertAlmostEqual(f[0]["durMs"], 592, delta=20)
        self.assertAlmostEqual(f[0]["x"], 500, delta=1)

    def test_gap_splits_a_dwell(self):
        s = (steady(500, 400, 400)
             + [{"t": 420, "x": None, "y": None}, {"t": 440, "x": None, "y": None}]
             + steady(500, 400, 400, 460))
        self.assertEqual(len(features.detect_fixations_idt(s, BIG_SCREEN)), 2)

    def test_short_dwell_rejected(self):
        self.assertEqual(features.detect_fixations_idt(steady(500, 400, 60), BIG_SCREEN), [])

    def test_empty_and_all_gap_inputs(self):
        self.assertEqual(features.detect_fixations_idt([], BIG_SCREEN), [])
        self.assertEqual(
            features.detect_fixations_idt([{"t": 0, "x": None, "y": None}], BIG_SCREEN), [])

    def test_zero_fixations_at_lab_threshold(self):
        """REGRESSION. A lab-grade threshold finds NOTHING in webcam-noise data.

        This silently zeroed every fixation-derived feature during the build:
        with no fixations the columns become constants and report AUC 0.500,
        which is indistinguishable from "no effect". Pinned so the shipped
        defaults cannot drift back to a value that cannot see a webcam.
        """
        rng = __import__("random").Random(99)
        diag = math.hypot(1920, 1080)
        sigma = 0.03 * diag                     # ~66 px, realistic webcam error
        s = [{"t": t, "x": 900 + rng.gauss(0, sigma), "y": 500 + rng.gauss(0, sigma)}
             for t in range(0, 800, 16)]
        lab = features.detect_fixations_idt(s, BIG_SCREEN, dispersion=0.045, smooth_win=1)
        self.assertEqual(len(lab), 0, "lab threshold saw fixations — update the note in features.py")
        tuned = features.detect_fixations_idt(s, BIG_SCREEN)
        self.assertGreaterEqual(len(tuned), 1, "shipped defaults must recover the dwell")

    def test_ordered_and_non_overlapping(self):
        s = steady(200, 200, 400) + steady(1500, 300, 400, 500) + steady(800, 900, 400, 1000)
        f = features.detect_fixations_idt(s, BIG_SCREEN)
        for a, b in zip(f, f[1:]):
            self.assertGreaterEqual(b["tStart"], a["tEnd"])


class TestIDTParity(unittest.TestCase):
    @unittest.skipUnless(shutil.which("node"), "node not available")
    def test_js_python_idt_agree(self):
        rng = __import__("random").Random(5)
        noisy = [{"t": t, "x": 900 + rng.gauss(0, 40), "y": 500 + rng.gauss(0, 40)}
                 for t in range(0, 900, 16)]
        streams = [
            steady(500, 400, 600),
            steady(300, 300, 400) + [{"t": 420, "x": None, "y": None}] + steady(1200, 800, 400, 460),
            noisy,
        ]
        for stream in streams:
            for opts in ({}, {"dispersion": 0.2, "smoothWin": 1}, {"smoothWin": 7, "minDurMs": 150}):
                payload = {"samples": stream, "screen": BIG_SCREEN}
                payload.update(opts)
                with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
                    json.dump(payload, fh)
                    tmp = fh.name
                try:
                    out = subprocess.check_output(["node", IDT_CLI, tmp], text=True)
                finally:
                    os.unlink(tmp)
                js = json.loads(out)
                py = features.detect_fixations_idt(
                    stream, BIG_SCREEN,
                    dispersion=opts.get("dispersion"),
                    min_dur_ms=opts.get("minDurMs"),
                    smooth_win=opts.get("smoothWin"))
                self.assertEqual(len(js), len(py), f"fixation count differs for opts={opts}")
                for a, b in zip(js, py):
                    self.assertEqual(a["tStart"], b["tStart"])
                    self.assertEqual(a["tEnd"], b["tEnd"])
                    self.assertAlmostEqual(a["x"], b["x"], places=6)
                    self.assertAlmostEqual(a["y"], b["y"], places=6)
                    self.assertEqual(a["n"], b["n"])


class TestProbeProtocol(unittest.TestCase):
    def test_groups_balanced_for_numbered_ids(self):
        pids = [f"P{i:02d}" for i in range(1, 41)]
        counts = {}
        for p in pids:
            g = probe_protocol.group_for(p)
            counts[g] = counts.get(g, 0) + 1
        self.assertEqual(len(counts), probe_protocol.N_GROUPS)
        self.assertEqual(max(counts.values()) - min(counts.values()), 0)

    def test_each_item_familiar_for_half_the_groups(self):
        for exp in ("E1", "E2", "E3"):
            items = probe_protocol.sets()[exp]["items"]
            for i in range(len(items)):
                n = sum(1 for g in range(probe_protocol.N_GROUPS)
                        if probe_protocol.is_familiar(i, g))
                self.assertEqual(n, probe_protocol.N_GROUPS // 2)

    def test_one_probe_per_trial(self):
        for array_n in (2, 4):
            b = probe_protocol.build_trials("P07", "E1", array_n, 20)
            self.assertEqual(len(b["trials"]), 20)
            for t in b["trials"]:
                self.assertEqual(len(t["slots"]), array_n)
                fam = [s for s in t["slots"] if s["familiar"]]
                self.assertEqual(len(fam), 1)
                self.assertEqual(fam[0]["itemId"], t["probeItemId"])
                self.assertEqual(len({s["itemId"] for s in t["slots"]}), array_n)

    def test_layout_refuses_small_viewport(self):
        self.assertTrue(probe_protocol.layout(4, 1920, 1080)["ok"])
        self.assertFalse(probe_protocol.layout(4, 1024, 640)["ok"])


class TestProbeProtocolParity(unittest.TestCase):
    """The browser protocol and the Python port must build the SAME design.

    Divergence here would mean the analysis is scoring a different experiment
    from the one the participant actually saw — silent and unrecoverable.
    """

    @unittest.skipUnless(shutil.which("node"), "node not available")
    def test_js_python_plans_agree(self):
        for pid, exp, arr, n in (("P01", "E1", 4, 12), ("P02", "E2", 2, 10),
                                 ("P17", "E3", 4, 15), ("pilot-alpha", "E1", 4, 8)):
            out = subprocess.check_output(
                ["node", PROBE_PLAN_CLI, pid, exp, str(arr), str(n)], text=True)
            js = json.loads(out)
            py = probe_protocol.build_trials(pid, exp, arr, n)
            self.assertEqual(js["counterbalanceGroup"], py["counterbalanceGroup"],
                             f"group differs for {pid}")
            self.assertEqual(js["arrayN"], py["arrayN"])
            self.assertEqual(len(js["trials"]), len(py["trials"]))
            for jt, pt in zip(js["trials"], py["trials"]):
                self.assertEqual(jt["probeItemId"], pt["probeItemId"])
                self.assertEqual(jt["slots"],
                                 [[s["itemId"], s["familiar"]] for s in pt["slots"]])


class TestAOIFeatures(unittest.TestCase):
    def _aois(self):
        L = probe_protocol.layout(4, 1920, 1080)
        return [{"slot": i, "itemId": f"i{i}", "familiar": i == 1, "rect": L["rects"][i]}
                for i in range(4)]

    def test_soft_weights_sum_to_one(self):
        aois = self._aois()
        for (x, y) in [(100, 100), (960, 540), (1800, 1000)]:
            w = aoi_features.aoi_weights(x, y, aois, 100.0, soft=True)
            self.assertAlmostEqual(sum(w), 1.0, places=9)

    def test_hard_assignment_picks_containing_rect(self):
        aois = self._aois()
        r = aois[2]["rect"]
        cx, cy = r["x"] + r["w"] / 2, r["y"] + r["h"] / 2
        w = aoi_features.aoi_weights(cx, cy, aois, 100.0, soft=False)
        self.assertEqual(w.index(1.0), 2)
        self.assertEqual(sum(w), 1.0)

    def test_soft_favours_the_nearest_tile(self):
        aois = self._aois()
        r = aois[0]["rect"]
        w = aoi_features.aoi_weights(r["x"] + r["w"] / 2, r["y"] + r["h"] / 2,
                                     aois, 120.0, soft=True)
        self.assertEqual(max(range(4), key=lambda i: w[i]), 0)

    def test_degenerate_trials_return_none_not_zeros(self):
        """A zero-filled row is indistinguishable from 'looked nowhere', which
        is a real and different observation — so unscorable trials are dropped."""
        sess = {"schema": "gazepry.probe.v1", "screen": BIG_SCREEN, "samples": []}
        self.assertIsNone(aoi_features.extract_trial(
            sess, {"index": 0, "onsetT": 0, "offsetT": 4000, "aois": self._aois()}))
        # missing clock anchor
        self.assertIsNone(aoi_features.extract_trial(
            sess, {"index": 0, "onsetT": None, "offsetT": None, "aois": self._aois()}))

    def test_relativise_zero_sums_within_trial(self):
        rows = [{"features": {k: float(i + 1) for k in aoi_features.FEATURE_NAMES}}
                for i in range(4)]
        out = aoi_features.relativise(rows)
        for k in aoi_features.FEATURE_NAMES:
            self.assertAlmostEqual(sum(r["rel"][k] for r in out), 0.0, places=9)

    def test_extract_session_ignores_non_probe_schema(self):
        self.assertEqual(aoi_features.extract_session({"schema": "gazepry.session.v2"}), [])

    def test_extract_session_drops_unanchored(self):
        s = simulate_probe.make_session("P01", "E1", 4, 3, 0.8, 1, "webgazer",
                                        "naive", "memory-adjacent", "immediate")
        s["clockAnchored"] = False
        self.assertEqual(aoi_features.extract_session(s), [])


class TestRecognitionMetrics(unittest.TestCase):
    def test_auc_basics(self):
        import numpy as np
        self.assertAlmostEqual(recognition.auc(np.array([1., 2, 3, 4]), np.array([0, 0, 1, 1])), 1.0)
        self.assertAlmostEqual(recognition.auc(np.array([4., 3, 2, 1]), np.array([0, 0, 1, 1])), 0.0)
        # all ties -> exactly chance
        self.assertAlmostEqual(recognition.auc(np.array([1., 1, 1, 1]), np.array([0, 0, 1, 1])), 0.5)

    def test_auc_is_nan_when_a_class_is_missing(self):
        """'Undefined' and 'no better than chance' are different results."""
        import numpy as np
        self.assertTrue(math.isnan(recognition.auc(np.array([1., 2]), np.array([1, 1]))))

    def test_tpr_at_fpr(self):
        import numpy as np
        s = np.array([0.9, 0.8, 0.7, 0.1, 0.05])
        y = np.array([1, 1, 1, 0, 0])
        self.assertAlmostEqual(recognition.tpr_at_fpr(s, y, 0.1), 1.0)

    def test_logistic_regression_separates(self):
        import numpy as np
        rng = np.random.default_rng(0)
        X = np.vstack([rng.normal(0, 1, (80, 3)), rng.normal(2.5, 1, (80, 3))])
        y = np.array([0] * 80 + [1] * 80)
        m = recognition.LogisticRegression().fit(X, y)
        self.assertGreater(recognition.auc(m.decision(X), y), 0.95)

    def test_logistic_regression_survives_a_constant_column(self):
        import numpy as np
        rng = np.random.default_rng(1)
        X = np.hstack([rng.normal(0, 1, (60, 2)), np.ones((60, 1))])
        y = np.array([0, 1] * 30)
        m = recognition.LogisticRegression().fit(X, y)
        self.assertTrue(np.all(np.isfinite(m.decision(X))))


class TestRecognitionEndToEnd(unittest.TestCase):
    """The pipeline must find the effect when it is there, and NOT when it isn't.

    The null half is the one that matters: a pipeline that reports a signal on
    effect=0 data is broken in a way no amount of real collection would reveal.
    """

    @staticmethod
    def _sessions(effect, n=12, trials=24, seed=3):
        return [simulate_probe.make_session(f"P{i + 1:02d}", "E1", 4, trials, effect,
                                            seed * 1000 + i, "webgazer", "naive",
                                            "memory-adjacent", "immediate")
                for i in range(n)]

    def test_recovers_a_planted_effect(self):
        res = recognition.evaluate(self._sessions(0.9), n_boot=120)
        self.assertNotIn("error", res)
        self.assertGreater(res["auc_per_aoi"], 0.7)
        self.assertGreater(res["auc_ci"][0], 0.5)
        self.assertGreater(res["probe_id_acc"], res["probe_id_chance"])

    def test_reports_chance_on_a_null_dataset(self):
        res = recognition.evaluate(self._sessions(0.0), n_boot=120)
        self.assertLess(abs(res["auc_per_aoi"] - 0.5), 0.08,
                        f"found signal in a null dataset: AUC={res['auc_per_aoi']:.3f}")
        ok, _ = recognition.rq0_verdict(res)
        self.assertFalse(ok, "RQ0 must NOT certify a signal on null data")

    def test_rq0_nulls_collapse_on_real_effect_data(self):
        res = recognition.evaluate(self._sessions(0.9), n_boot=120)
        self.assertLess(abs(res["null_shuffled_auc"] - 0.5), 0.08,
                        "shuffled-label null did not collapse")
        self.assertLess(abs(res["null_saliency_auc"] - 0.5), 0.08,
                        "saliency-only baseline is not at chance — counterbalancing or "
                        "the group-balanced training fold is broken")
        ok, reasons = recognition.rq0_verdict(res)
        self.assertTrue(ok, "RQ0 gate should pass on clean effect data: " + "; ".join(reasons))

    def test_segmentation_produces_fixations(self):
        """Guards the failure mode where I-DT finds nothing and every
        fixation feature quietly becomes a constant reporting AUC 0.500."""
        res = recognition.evaluate(self._sessions(0.9), n_boot=60)
        self.assertGreater(res["fixations_per_trial"], 1.0)

    def test_feasible_ks_require_both_classes(self):
        import numpy as np
        rows = []
        for cls, cnt in ((1, 3), (0, 12)):
            for it in range(10):
                for _ in range(cnt):
                    rows.append({"participant": "P01", "itemId": f"{cls}-{it}",
                                 "familiar": bool(cls)})
        scores = np.zeros(len(rows))
        ks = recognition.feasible_ks(rows, scores, candidates=(1, 5, 10), min_pairs=8)
        self.assertIn(1, ks)
        self.assertNotIn(5, ks, "k=5 has no familiar pairs and would yield a bare nan")

    def test_loader_skips_d4_sessions_and_reports_drops(self):
        tmp = tempfile.mkdtemp(prefix="gp-probe-")
        try:
            good = simulate_probe.make_session("P01", "E1", 4, 5, 0.8, 1, "webgazer",
                                               "naive", "memory-adjacent", "immediate")
            bad = dict(good)
            bad["clockAnchored"] = False
            for name, obj in (("a.json", good), ("b.json", bad),
                              ("c.json", {"schema": "gazepry.session.v2", "samples": []})):
                with open(os.path.join(tmp, name), "w", encoding="utf-8") as fh:
                    json.dump(obj, fh)
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                got = recognition.load_probe_sessions(tmp, verbose=True)
            self.assertEqual(len(got), 1)
            self.assertIn("no clock anchor", buf.getvalue())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestStimulusPack(unittest.TestCase):
    """The stimulus manifest is now the single source of the item tables, and
    the images are real files rather than shapes drawn at runtime."""

    def test_manifest_loads_and_is_shared_by_both_languages(self):
        m = probe_protocol.load_manifest()
        self.assertEqual(m["schema"], "gazepry.stimuli.v1")
        self.assertEqual(set(m["sets"]), {"E1", "E2", "E3"})

    def test_every_item_points_at_a_file_that_exists(self):
        root = os.path.dirname(probe_protocol.MANIFEST_PATH)
        for sid, s in probe_protocol.sets().items():
            self.assertGreaterEqual(len(s["items"]), 8, f"{sid} too small for a 4-tile array")
            ids = [i["id"] for i in s["items"]]
            self.assertEqual(len(set(ids)), len(ids), f"{sid} has duplicate ids")
            for it in s["items"]:
                fp = os.path.join(root, it["file"].replace("/", os.sep))
                self.assertTrue(os.path.exists(fp), f"missing stimulus {it['file']}")
                self.assertGreater(os.path.getsize(fp), 1000, f"{it['file']} is suspiciously tiny")

    def test_e1_images_meet_the_minimum_size(self):
        sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
        import make_stimuli
        root = os.path.dirname(probe_protocol.MANIFEST_PATH)
        m = probe_protocol.load_manifest()
        min_w, min_h = m["minSize"]["w"], m["minSize"]["h"]
        for it in probe_protocol.sets()["E1"]["items"]:
            size = make_stimuli.read_png_size(
                os.path.join(root, it["file"].replace("/", os.sep)))
            self.assertIsNotNone(size, f"unreadable {it['file']}")
            self.assertGreaterEqual(size[0], min_w)
            self.assertGreaterEqual(size[1], min_h)

    def test_placeholder_state_is_reported_honestly(self):
        """E2/E3 measure naturally acquired familiarity, so shipping stand-ins
        must be visible to the tooling, not just documented.

        Whether the real assets are installed depends on whether
        ``fetch_stimuli.py`` has run, so the assertion is that the flag matches
        the manifest -- pinning it either way would fail on one of two
        legitimate states.
        """
        self.assertFalse(probe_protocol.uses_placeholders("E1"))
        for exp in ("E2", "E3"):
            any_ph = any(i.get("placeholder") for i in probe_protocol.sets()[exp]["items"])
            self.assertEqual(probe_protocol.uses_placeholders(exp), any_ph)

    def test_real_items_carry_provenance(self):
        """Attribution is a licence obligation for the CC BY / CC BY-SA assets,
        and a stimulus figure with no source is unreproducible."""
        for exp in ("E2", "E3"):
            for it in probe_protocol.sets()[exp]["items"]:
                if it.get("placeholder"):
                    continue
                for field in ("source", "licence", "retrieved"):
                    self.assertTrue(it.get(field),
                                    f"{exp}/{it['id']} is marked real but has no {field}")

    def test_grouped_arrays_never_mix_classes(self):
        """An array of one face among three bank logos would let the probe be
        picked out by category rather than by familiarity."""
        for exp, s in probe_protocol.sets().items():
            group_by = s.get("arrayGroupBy")
            if not group_by:
                continue
            by_id = {i["id"]: i for i in s["items"]}
            for array_n in (2, 4):
                for pid in (f"P{i:02d}" for i in range(1, 13)):
                    b = probe_protocol.build_trials(pid, exp, array_n, 20)
                    for t in b["trials"]:
                        classes = {by_id[sl["itemId"]][group_by] for sl in t["slots"]}
                        self.assertEqual(len(classes), 1,
                                         f"{exp} {pid} trial {t['index']} mixes {group_by}")

    def test_every_class_can_fill_an_array_for_every_group(self):
        """The Latin square runs over the GLOBAL item index, so a class that is
        not a contiguous multiple of N_GROUPS can leave some counterbalance
        group unable to build a trial -- mid-session, not at startup."""
        for exp, s in probe_protocol.sets().items():
            group_by = s.get("arrayGroupBy")
            if not group_by:
                continue
            for g in range(probe_protocol.N_GROUPS):
                tally: dict = {}
                for i, it in enumerate(s["items"]):
                    fam, unf = tally.setdefault(it.get(group_by), [0, 0])
                    if probe_protocol.is_familiar(i, g):
                        tally[it.get(group_by)] = [fam + 1, unf]
                    else:
                        tally[it.get(group_by)] = [fam, unf + 1]
                for cls, (nf, nu) in tally.items():
                    self.assertGreaterEqual(nf, 1, f"{exp} group {g} class {cls}: no probe")
                    self.assertGreaterEqual(nu, 3, f"{exp} group {g} class {cls}: {nu} irrelevants")

    def test_e1_stimuli_are_mutually_distinguishable(self):
        """A 'novel' tile that looks like a studied one contaminates the
        familiarity contrast in a way counterbalancing cannot undo."""
        s = probe_protocol.sets()["E1"]
        self.assertIn("minPairDistance", s)
        self.assertGreater(s["minPairDistance"], 15.0,
                           "E1 fractals are too similar to each other")

    def test_e3_has_no_protected_characteristics(self):
        allowed = {"health", "finance", "legal", "civic"}
        for it in probe_protocol.sets()["E3"]["items"]:
            self.assertIn(it.get("category"), allowed,
                          f"unexpected E3 category: {it.get('category')}")

    def test_generator_is_deterministic(self):
        sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
        import make_stimuli
        a = make_stimuli.julia(4242)
        b = make_stimuli.julia(4242)
        self.assertTrue((a == b).all(), "same seed must give the same image")
        c = make_stimuli.julia(4243)
        self.assertFalse((a == c).all(), "different seeds must differ")

    def test_generated_images_contain_no_garbage_pixels(self):
        """REGRESSION: the smooth escape-time formula can go negative, and a
        NaN cast to uint8 is a garbage pixel rather than an obvious error."""
        sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
        import make_stimuli
        import numpy as np
        for seed in (11, 1009, 77777):
            img = make_stimuli.julia(seed)
            self.assertEqual(img.dtype, np.uint8)
            self.assertGreater(float(img.std()), 25.0,
                               "image is nearly uniform — little to recognise")

    def test_checker_flags_a_missing_file(self):
        tmp = tempfile.mkdtemp(prefix="gp-stim-")
        try:
            sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
            import make_stimuli
            m = {"schema": "gazepry.stimuli.v1", "minSize": {"w": 10, "h": 10},
                 "sets": {"E1": {"items": [{"id": f"i{n}", "file": "e1/nope.png"}
                                           for n in range(8)]}}}
            with open(os.path.join(tmp, "manifest.json"), "w", encoding="utf-8") as fh:
                json.dump(m, fh)
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                rc = make_stimuli.check(tmp)
            self.assertEqual(rc, 1)
            self.assertIn("missing file", buf.getvalue())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestItemSubsets(unittest.TestCase):
    """`--item-class` / `--item-tier`: the per-class contrast and the
    high-salience-only fallback analysis."""

    def test_attribute_lookup_reads_the_manifest(self):
        item = probe_protocol.sets()["E2"]["items"][0]
        self.assertEqual(
            recognition.item_attribute("E2", item["id"], "class"), item["class"])
        self.assertIsNone(recognition.item_attribute("E2", "no-such-item", "class"))

    def test_filter_keeps_only_the_named_class(self):
        e2 = probe_protocol.sets()["E2"]["items"]
        rows = [{"experiment": "E2", "itemId": i["id"]} for i in e2]
        for cls in {i["class"] for i in e2}:
            kept = recognition.filter_by_item_attribute(rows, "class", cls)
            self.assertTrue(kept)
            self.assertEqual(len(kept), sum(1 for i in e2 if i["class"] == cls))
            for r in kept:
                self.assertEqual(
                    recognition.item_attribute("E2", r["itemId"], "class"), cls)

    def test_unknown_subset_is_an_error_not_an_empty_result(self):
        """An empty subset scored silently would report nan and read as a
        negative result rather than as a typo."""
        sessions = [simulate_probe.make_session("P01", "E1", 4, 8, 0.9, 1, "webgazer",
                                                "naive", "memory-adjacent", "immediate")]
        res = recognition.evaluate(sessions, item_class="not-a-class", n_boot=20)
        self.assertIn("error", res)
        self.assertIn("not-a-class", res["error"])


class TestStimulusSourcing(unittest.TestCase):
    """The fetcher that installs the real E2/E3 assets. All offline: nothing
    here touches the network, so the suite stays runnable without one."""

    def _mod(self):
        sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
        import fetch_stimuli
        return fetch_stimuli

    def _sources(self):
        with open(os.path.join(os.path.dirname(probe_protocol.MANIFEST_PATH),
                               "sources.json"), encoding="utf-8") as fh:
            return json.load(fh)

    def test_sources_describe_items_that_actually_exist(self):
        src = self._sources()
        self.assertEqual(src["schema"], "gazepry.stimuli.sources.v1")
        for sid, sset in src["sets"].items():
            known = {i["id"] for i in probe_protocol.sets()[sid]["items"]}
            seen = set()
            for spec in sset["items"]:
                self.assertIn(spec["id"], known,
                              f"sources.json names {sid}/{spec['id']}, which is not "
                              f"in the item table -- the asset would be orphaned")
                self.assertNotIn(spec["id"], seen, f"duplicate source for {spec['id']}")
                seen.add(spec["id"])
                self.assertIn(spec.get("fit", "cover"), ("cover", "contain"))
                res = spec.get("resolve") or {}
                self.assertTrue(res.get("commonsFile") or res.get("wikipediaLead"),
                                f"{spec['id']}: no way to resolve a file")

    def test_non_free_licences_are_refused(self):
        """The whole point of the licence gate: a fair-use logo must never be
        downloaded into a GPLv3 repo intended for public release."""
        m = self._mod()
        for good in ("Public domain", "CC0", "CC BY 4.0", "CC BY-SA 3.0",
                     "PD-textlogo", "FAL"):
            self.assertTrue(m.licence_is_free(good), good)
        for bad in ("Fair use", "Non-free logo", "All rights reserved",
                    "Copyrighted, dedicated to the public", "", None):
            self.assertFalse(m.licence_is_free(bad), str(bad))

    def test_png_decoder_round_trips_the_writer(self):
        """The decoder exists only because a logo has to be composited onto a
        uniform canvas; a mis-decoded logo is a corrupted stimulus."""
        import numpy as np
        m = self._mod()
        sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
        import make_stimuli
        rng = np.random.default_rng(3)
        img = rng.integers(0, 256, size=(37, 53, 3), dtype=np.uint8)
        tmp = tempfile.mkdtemp(prefix="gp-png-")
        try:
            fp = os.path.join(tmp, "x.png")
            make_stimuli.write_png(fp, img)
            back = m.read_png(fp)
            self.assertEqual(back.shape, (37, 53, 4))
            self.assertTrue((back[:, :, :3] == img).all(), "PNG round-trip corrupted pixels")
            self.assertTrue((back[:, :, 3] == 255).all())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_letterbox_centres_without_overflowing(self):
        import numpy as np
        m = self._mod()
        wide = np.zeros((60, 900, 4), dtype=np.uint8)
        wide[:, :, :3] = 10
        wide[:, :, 3] = 255
        out = m.letterbox(wide, 400, 300)
        self.assertEqual(out.shape, (300, 400, 3))
        # corners stay canvas background; the mark lands in the middle
        self.assertTrue((out[0, 0] == np.array(m.CANVAS_BG, dtype=np.uint8)).all())
        self.assertTrue((out[150, 200] < 60).all())

    def test_verify_reports_a_tampered_asset(self):
        m = self._mod()
        tmp = tempfile.mkdtemp(prefix="gp-lock-")
        try:
            os.makedirs(os.path.join(tmp, "e2"))
            fp = os.path.join(tmp, "e2", "x.png")
            with open(fp, "wb") as fh:
                fh.write(b"original")
            lock = {"schema": "gazepry.stimuli.lock.v1", "items": {
                "x": {"file": "e2/x.png", "sha256": m.sha256_file(fp)}}}
            with open(os.path.join(tmp, "stimuli.lock.json"), "w", encoding="utf-8") as fh:
                json.dump(lock, fh)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(m.verify(tmp), 0)
            with open(fp, "wb") as fh:
                fh.write(b"tampered")
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                self.assertEqual(m.verify(tmp), 1)
            self.assertIn("changed since it was locked", buf.getvalue())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_installed_assets_match_the_lock(self):
        """If a lock exists, what is on disk must be what was locked."""
        m = self._mod()
        root = os.path.dirname(probe_protocol.MANIFEST_PATH)
        if not os.path.exists(os.path.join(root, "stimuli.lock.json")):
            self.skipTest("no assets fetched yet (python scripts/fetch_stimuli.py)")
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            rc = m.verify(root)
        self.assertEqual(rc, 0, buf.getvalue())


class TestSelfReportLabels(unittest.TestCase):
    """E2/E3 ground truth is the questionnaire, not the counterbalance role."""

    @staticmethod
    def _write_labels(tmp, participant, experiment, responses, when=1):
        rec = {"schema": "gazepry.labels.v1", "participant": participant,
               "session": "S1", "experiment": experiment, "collectedAt": when,
               "items": [{"itemId": k, "response": v} for k, v in responses.items()]}
        fn = f"{participant}_S1_{experiment}_labels_{when}.json"
        with open(os.path.join(tmp, fn), "w", encoding="utf-8") as fh:
            json.dump(rec, fh)
        return rec

    def test_loads_and_keys_by_cell(self):
        tmp = tempfile.mkdtemp(prefix="gp-lab-")
        try:
            self._write_labels(tmp, "P01", "E2", {"mail": 3, "vid": 0})
            labs = labels.load_labels(tmp)
            self.assertIn(("P01", "S1", "E2"), labs)
            self.assertEqual(labels.response_map(labs[("P01", "S1", "E2")])["mail"], 3)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_latest_questionnaire_wins(self):
        tmp = tempfile.mkdtemp(prefix="gp-lab-")
        try:
            self._write_labels(tmp, "P01", "E2", {"mail": 0}, when=1)
            self._write_labels(tmp, "P01", "E2", {"mail": 3}, when=2)
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                labs = labels.load_labels(tmp, verbose=True)
            self.assertEqual(labels.response_map(labs[("P01", "S1", "E2")])["mail"], 3)
            self.assertIn("multiple questionnaires", buf.getvalue())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_ignores_foreign_schemas(self):
        tmp = tempfile.mkdtemp(prefix="gp-lab-")
        try:
            with open(os.path.join(tmp, "x.json"), "w", encoding="utf-8") as fh:
                json.dump({"schema": "gazepry.probe.v1"}, fh)
            self.assertEqual(labels.load_labels(tmp), {})
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_threshold_applies_and_is_adjustable(self):
        rows = [{"participant": "P01", "sessionId": "S1", "experiment": "E2",
                 "itemId": f"i{v}", "familiar": False} for v in range(4)]
        labs = {("P01", "S1", "E2"): {"items": [
            {"itemId": f"i{v}", "response": v} for v in range(4)]}}
        kept, _ = labels.apply_labels(rows, labs, threshold=2)
        self.assertEqual([r["familiar"] for r in kept], [False, False, True, True])
        kept1, _ = labels.apply_labels(rows, labs, threshold=1)
        self.assertEqual([r["familiar"] for r in kept1], [False, True, True, True])

    def test_unanswered_items_are_dropped_not_defaulted(self):
        """A blank answer is participant fatigue, not evidence of unfamiliarity;
        defaulting it to False would manufacture negatives."""
        rows = [{"participant": "P01", "sessionId": "S1", "experiment": "E2",
                 "itemId": "a", "familiar": False},
                {"participant": "P01", "sessionId": "S1", "experiment": "E2",
                 "itemId": "b", "familiar": False}]
        labs = {("P01", "S1", "E2"): {"items": [
            {"itemId": "a", "response": 3}, {"itemId": "b", "response": None}]}}
        kept, rep = labels.apply_labels(rows, labs)
        self.assertEqual(len(kept), 1)
        self.assertEqual(rep["unanswered_items"], 1)

    def test_rows_without_a_questionnaire_are_dropped_and_reported(self):
        rows = [{"participant": "P09", "sessionId": "S1", "experiment": "E2",
                 "itemId": "a", "familiar": True}]
        kept, rep = labels.apply_labels(rows, {})
        self.assertEqual(kept, [])
        self.assertEqual(rep["missing_questionnaire_cells"], ["P09/S1/E2"])

    def test_evaluate_refuses_e2_without_labels(self):
        """Scoring E2 on the counterbalance role would measure a label the
        design never controlled — so it must be an error, not a silent default."""
        ss = [simulate_probe.make_session(f"P{i + 1:02d}", "E2", 4, 10, 0.9, 700 + i,
                                          "webgazer", "naive", "memory-adjacent", None)
              for i in range(6)]
        res = recognition.evaluate(ss, n_boot=20)
        self.assertIn("error", res)
        self.assertIn("questionnaire", res["error"])

    def test_evaluate_uses_self_report_when_provided(self):
        tmp = tempfile.mkdtemp(prefix="gp-lab-")
        try:
            ss = [simulate_probe.make_session(f"P{i + 1:02d}", "E2", 4, 12, 0.9, 800 + i,
                                              "webgazer", "naive", "memory-adjacent", None)
                  for i in range(8)]
            # Self-report that AGREES with the planted effect for each participant.
            items = [it["id"] for it in probe_protocol.sets()["E2"]["items"]]
            for i, s in enumerate(ss):
                fam = {a["itemId"] for t in s["trials"] for a in t["aois"] if a["familiar"]}
                self._write_labels(tmp, s["participant"], "E2",
                                   {it: (3 if it in fam else 0) for it in items})
            res = recognition.evaluate(ss, n_boot=60, labels_dir=tmp)
            self.assertNotIn("error", res)
            self.assertEqual(res["label_source"], "self-report")
            self.assertGreater(res["auc_per_aoi"], 0.7)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_self_report_that_contradicts_gaze_collapses_to_chance(self):
        """The label really is driving the score: keep the same gaze, randomise
        the questionnaire, and the result must fall apart."""
        tmp = tempfile.mkdtemp(prefix="gp-lab-")
        try:
            import random
            rng = random.Random(5)
            ss = [simulate_probe.make_session(f"P{i + 1:02d}", "E2", 4, 12, 0.9, 900 + i,
                                              "webgazer", "naive", "memory-adjacent", None)
                  for i in range(8)]
            items = [it["id"] for it in probe_protocol.sets()["E2"]["items"]]
            for s in ss:
                self._write_labels(tmp, s["participant"], "E2",
                                   {it: rng.choice([0, 3]) for it in items})
            res = recognition.evaluate(ss, n_boot=60, labels_dir=tmp)
            self.assertLess(abs(res["auc_per_aoi"] - 0.5), 0.12,
                            f"random labels still scored {res['auc_per_aoi']:.3f}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_e1_does_not_need_labels(self):
        ss = [simulate_probe.make_session(f"P{i + 1:02d}", "E1", 4, 12, 0.9, 600 + i,
                                          "webgazer", "naive", "memory-adjacent", "immediate")
              for i in range(8)]
        res = recognition.evaluate(ss, n_boot=40)
        self.assertNotIn("error", res)
        self.assertEqual(res["label_source"], "counterbalance")


class TestServerExcludesProbeSessions(unittest.TestCase):
    """D7 probe sessions share the data dir with D4 sessions but must never
    enter the re-ID gallery: their stream is chopped into adversary-driven 4 s
    trials, so a whole-session dynamics vector measures the trial structure."""

    def test_probe_schema_is_marked_for_exclusion(self):
        s = simulate_probe.make_session("P01", "E1", 4, 3, 0.8, 1, "webgazer",
                                        "naive", "memory-adjacent", "immediate")
        self.assertTrue(str(s["schema"]).startswith("gazepry.probe"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
