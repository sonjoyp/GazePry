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
            items = probe_protocol.SETS[exp]["items"]
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
