"""
Recognition-leakage evaluation for Direction D7.

Loads probe sessions (schema ``gazepry.probe.v1``), extracts AOI-anchored
per-trial features, and asks the only question that matters: **can a page tell,
from gaze alone, which tile the visitor had seen before?**

See GazePry_D7_Recognition_Knowledge_Direction.md §5 and §7.4. What is reported:

  per-AOI AUC            comparable to the ocular-CIT literature's per-item AUCs
  probe-identification   top-1 accuracy within a trial (chance = 1/arrayN)
  item-level AUC vs k    THE HEADLINE CURVE -- "how many tiles before a page
                         knows which sites you use"
  TPR@FPR=0.1            the security-relevant operating point
  d' per feature         comparability with the psychology literature

and, before any of it is allowed to count, the **RQ0 gate**:

  shuffled-label null    permute familiarity within participant -> must be ~0.5
  saliency-only baseline item identity + slot position, familiarity withheld
                         -> must be ~0.5, or the classifier is reading the
                         pictures rather than the person

Usage:
  python recognition.py --data ../data
  python recognition.py --data ../data_probe_sim --experiment E1 --plot k.png
  python recognition.py --data ../data --experiment E2 --labels ../labels \
                        --item-class bank        # per-class contrast
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from typing import Dict, List, Optional, Tuple

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aoi_features import (  # noqa: E402
    FEATURE_NAMES, design_matrix, extract_session,
)
from labels import (  # noqa: E402
    DEFAULT_THRESHOLD, apply_labels, class_balance, load_labels,
)
import probe_protocol  # noqa: E402

CHANCE = 0.5
SELF_REPORT_EXPERIMENTS = ("E2", "E3")


def item_attribute(experiment: Optional[str], item_id: str, attr: str):
    """Look up a manifest attribute of an item (its class, its tier, ...).

    The AOI rows carry only the item id, because the session file records what
    was on screen rather than a copy of the item table. The manifest is the
    single source of the item table for both languages, so the attribute is
    resolved from there rather than duplicated into every session.
    """
    for sid, s in probe_protocol.sets().items():
        if experiment and sid != experiment:
            continue
        for it in s["items"]:
            if it["id"] == item_id:
                return it.get(attr)
    return None


def filter_by_item_attribute(rows: List[dict], attr: str, value: str) -> List[dict]:
    """Restrict to items whose manifest ``attr`` equals ``value``.

    E2 arrays are class-homogeneous, so filtering by class keeps whole trials
    intact. Filtering by tier does not: it can strip the probe out of a trial,
    which leaves the per-AOI AUC well defined but makes probe-identification
    accuracy skip those trials. That is handled by the trial scorer rather than
    papered over here.
    """
    return [r for r in rows
            if item_attribute(r.get("experiment"), r.get("itemId"), attr) == value]


# ---- loading --------------------------------------------------------------
def load_probe_sessions(data_dir: str, experiment: Optional[str] = None,
                        tracker: Optional[str] = None,
                        awareness: Optional[str] = None,
                        verbose: bool = False) -> List[dict]:
    """Load probe sessions, reporting every file it declines to use.

    Dropping is never silent: a session excluded for a missing clock anchor or
    zero scorable trials is a data-collection failure the operator needs to see,
    not a row to quietly omit.
    """
    out, dropped = [], []
    for fp in sorted(glob.glob(os.path.join(data_dir, "*.json"))):
        try:
            with open(fp, encoding="utf-8") as fh:
                s = json.load(fh)
        except (OSError, ValueError) as e:
            dropped.append((os.path.basename(fp), f"unreadable: {e}"))
            continue
        if s.get("schema") != "gazepry.probe.v1":
            continue                      # a D4 session; not an error
        if not s.get("clockAnchored", True):
            dropped.append((os.path.basename(fp), "no clock anchor (no gaze samples)"))
            continue
        if experiment and s.get("experiment") != experiment:
            continue
        if tracker and s.get("trackerFamily") != tracker:
            continue
        if awareness and s.get("awareness") != awareness:
            continue
        if not s.get("trials"):
            dropped.append((os.path.basename(fp), "no trials"))
            continue
        out.append(s)
    if verbose and dropped:
        print(f"  dropped {len(dropped)} session(s):")
        for fn, why in dropped:
            print(f"    {fn}: {why}")
    return out


# ---- metrics --------------------------------------------------------------
def auc(scores: np.ndarray, labels: np.ndarray) -> float:
    """Mann-Whitney U / ROC AUC with proper tie handling.

    Returns nan when a class is absent, rather than 0.5 -- "undefined" and
    "no better than chance" are different results and must not be conflated.
    """
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels).astype(int)
    pos, neg = labels == 1, labels == 0
    n_pos, n_neg = int(pos.sum()), int(neg.sum())
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    order = np.argsort(scores, kind="mergesort")
    ranks = np.empty(len(scores), dtype=float)
    ranks[order] = np.arange(1, len(scores) + 1, dtype=float)
    # average ranks within ties
    s_sorted = scores[order]
    i = 0
    while i < len(s_sorted):
        j = i
        while j + 1 < len(s_sorted) and s_sorted[j + 1] == s_sorted[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = (i + j + 2) / 2.0
        i = j + 1
    return float((ranks[pos].sum() - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg))


def tpr_at_fpr(scores: np.ndarray, labels: np.ndarray, target_fpr: float = 0.1) -> float:
    """Highest TPR achievable at or below ``target_fpr``."""
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels).astype(int)
    if labels.sum() == 0 or (1 - labels).sum() == 0:
        return float("nan")
    order = np.argsort(-scores, kind="mergesort")
    lab = labels[order]
    tp = np.cumsum(lab)
    fp = np.cumsum(1 - lab)
    tpr = tp / max(1, lab.sum())
    fpr = fp / max(1, (1 - lab).sum())
    ok = fpr <= target_fpr
    return float(tpr[ok].max()) if ok.any() else 0.0


def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    va, vb = a.var(ddof=1), b.var(ddof=1)
    pooled = math_sqrt(((len(a) - 1) * va + (len(b) - 1) * vb) / (len(a) + len(b) - 2))
    return float((a.mean() - b.mean()) / pooled) if pooled > 0 else 0.0


def math_sqrt(v: float) -> float:
    return float(np.sqrt(v)) if v > 0 else 0.0


# ---- model ----------------------------------------------------------------
class LogisticRegression:
    """L2-regularised logistic regression by Newton-IRLS.

    Deliberately not a deep model: at the N this direction targets (~40
    participants x 40 trials) an end-to-end model would overfit, and the
    interpretability of *which feature family survives* is the entire point of
    RQ4 and RQ5. Pure numpy so the analysis has no new dependency.
    """

    def __init__(self, l2: float = 1.0, max_iter: int = 50, tol: float = 1e-8):
        self.l2, self.max_iter, self.tol = l2, max_iter, tol
        self.w: Optional[np.ndarray] = None
        self.mu: Optional[np.ndarray] = None
        self.sd: Optional[np.ndarray] = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        self.mu = X.mean(axis=0)
        sd = X.std(axis=0)
        sd[sd == 0] = 1.0            # a constant column carries no information
        self.sd = sd
        Z = np.hstack([np.ones((len(X), 1)), (X - self.mu) / self.sd])
        d = Z.shape[1]
        w = np.zeros(d)
        # do not regularise the intercept
        pen = np.eye(d) * self.l2
        pen[0, 0] = 0.0
        for _ in range(self.max_iter):
            p = 1.0 / (1.0 + np.exp(-np.clip(Z @ w, -30, 30)))
            g = Z.T @ (p - y) + pen @ w
            s = np.clip(p * (1 - p), 1e-6, None)
            H = Z.T @ (Z * s[:, None]) + pen
            try:
                step = np.linalg.solve(H, g)
            except np.linalg.LinAlgError:
                step = np.linalg.lstsq(H, g, rcond=None)[0]
            w -= step
            if np.max(np.abs(step)) < self.tol:
                break
        self.w = w
        return self

    def decision(self, X) -> np.ndarray:
        X = np.asarray(X, dtype=float)
        Z = np.hstack([np.ones((len(X), 1)), (X - self.mu) / self.sd])
        return Z @ self.w


def lopo_scores(X, y, groups, l2: float = 1.0, seed: Optional[int] = None,
                shuffle_labels: bool = False) -> np.ndarray:
    """Leave-one-participant-out cross-validated decision scores.

    Never splits within a participant: a model that has seen the same person's
    other trials is measuring memorisation of that person, not recognition.
    When ``shuffle_labels`` is set, familiarity is permuted WITHIN participant
    (the RQ0 null) so the class balance and the participant structure are
    preserved and only the person-item link is destroyed.
    """
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=int)
    groups = np.asarray(groups)
    out = np.full(len(y), np.nan)
    rng = np.random.default_rng(seed)

    y_use = y.copy()
    if shuffle_labels:
        for g in np.unique(groups):
            m = groups == g
            y_use[m] = rng.permutation(y_use[m])

    for g in np.unique(groups):
        te = groups == g
        tr = ~te
        if tr.sum() < 10 or len(np.unique(y_use[tr])) < 2:
            continue
        model = LogisticRegression(l2=l2).fit(X[tr], y_use[tr])
        out[te] = model.decision(X[te])
    return out, y_use


def saliency_baseline_scores(rows: List[dict], y, groups, l2: float = 1.0) -> np.ndarray:
    """RQ0 control: predict familiarity from item identity and slot position ONLY.

    If this clears chance, the classifier could win without ever looking at gaze
    -- which would mean the counterbalancing failed, not that recognition leaks.

    THE TRAINING SET MUST BE GROUP-BALANCED, and this is not a detail. Holding
    one participant out leaves their own counterbalance group short by exactly
    one, so every item's marginal familiarity in the training data tilts *away*
    from the held-out participant's own assignment. The tilt is tiny (order
    1/N) but its SIGN is identical for every held-out participant, so pooled
    across the cohort it produces a wildly inverted AUC -- an artifact of
    leave-one-out, not evidence of a saliency confound. Equalising the group
    counts in each training fold removes it exactly.
    """
    items = sorted({r["itemId"] for r in rows})
    slots = sorted({r["slot"] for r in rows})
    idx_i = {v: i for i, v in enumerate(items)}
    idx_s = {v: i for i, v in enumerate(slots)}
    X = np.zeros((len(rows), len(items) + len(slots)))
    for n, r in enumerate(rows):
        X[n, idx_i[r["itemId"]]] = 1.0
        X[n, len(items) + idx_s[r["slot"]]] = 1.0

    y = np.asarray(y, dtype=int)
    groups = np.asarray(groups)
    cb = {r["participant"]: r.get("counterbalanceGroup") for r in rows}
    out = np.full(len(y), np.nan)

    for held in np.unique(groups):
        te = groups == held
        # participants available to train on, bucketed by counterbalance group
        buckets: Dict[object, List[str]] = {}
        for p in sorted(set(groups) - {held}):
            buckets.setdefault(cb.get(p), []).append(p)
        if len(buckets) > 1:
            keep_n = min(len(v) for v in buckets.values())
            keep = set()
            for v in buckets.values():
                keep.update(v[:keep_n])      # deterministic: sorted ids
        else:
            keep = set(p for v in buckets.values() for p in v)
        tr = np.array([g in keep for g in groups])
        if tr.sum() < 10 or len(np.unique(y[tr])) < 2:
            continue
        model = LogisticRegression(l2=l2).fit(X[tr], y[tr])
        out[te] = model.decision(X[te])
    return out


# ---- aggregation ----------------------------------------------------------
def probe_identification(rows: List[dict], scores: np.ndarray) -> Tuple[float, int, float]:
    """Top-1 accuracy at picking the probe AOI within each trial.

    Returns (accuracy, n_trials, chance).
    """
    trials: Dict[tuple, List[int]] = {}
    for i, r in enumerate(rows):
        trials.setdefault((r["participant"], r["sessionId"], r["trial"]), []).append(i)
    hits, total, arr_sizes = 0, 0, []
    for idx in trials.values():
        sc = scores[idx]
        if np.isnan(sc).any():
            continue
        labs = [rows[i]["familiar"] for i in idx]
        if sum(labs) != 1:
            continue                      # not a one-probe trial; skip cleanly
        arr_sizes.append(len(idx))
        total += 1
        if labs[int(np.argmax(sc))]:
            hits += 1
    if not total:
        return float("nan"), 0, float("nan")
    chance = float(np.mean([1.0 / a for a in arr_sizes]))
    return hits / total, total, chance


def feasible_ks(rows: List[dict], scores: np.ndarray,
                candidates=(1, 2, 3, 5, 10, 20, 40), min_pairs: int = 8) -> List[int]:
    """Which aggregation budgets the data can actually support.

    Reporting k=20 as `nan` because no (participant, item) pair was shown 20
    times is noise in the output; the honest report is the range the design
    reached. The caller still sees the ceiling, so a too-short session is
    visible rather than hidden.
    """
    per: Dict[tuple, int] = {}
    lab: Dict[tuple, int] = {}
    for i, r in enumerate(rows):
        if np.isnan(scores[i]):
            continue
        key = (r["participant"], r["itemId"])
        per[key] = per.get(key, 0) + 1
        lab[key] = 1 if r["familiar"] else 0
    if not per:
        return []
    # BOTH classes must survive the k threshold. Familiar items appear once per
    # trial (as the probe) while unfamiliar ones fill the other arrayN-1 slots,
    # so familiar exposure is roughly (arrayN-1)x rarer and is what actually
    # caps the curve. Counting pooled pairs would report a k that yields a
    # single-class sample and a bare `nan`.
    out = []
    for k in candidates:
        pos = sum(1 for key, c in per.items() if c >= k and lab[key] == 1)
        neg = sum(1 for key, c in per.items() if c >= k and lab[key] == 0)
        if pos >= min_pairs and neg >= min_pairs:
            out.append(k)
    return out


def item_level_auc_vs_k(rows: List[dict], scores: np.ndarray,
                        ks: List[int], seed: int = 0) -> Dict[int, float]:
    """THE HEADLINE CURVE. Aggregate a (participant, item) verdict over k trials.

    The attacker's real question is not "was this tile the probe in this trial"
    but "does this person know this thing" -- which they answer by averaging the
    score for that item over however many times they can show it.
    """
    per: Dict[tuple, List[float]] = {}
    lab: Dict[tuple, int] = {}
    for i, r in enumerate(rows):
        if np.isnan(scores[i]):
            continue
        key = (r["participant"], r["itemId"])
        per.setdefault(key, []).append(float(scores[i]))
        lab[key] = 1 if r["familiar"] else 0
    rng = np.random.default_rng(seed)
    out: Dict[int, float] = {}
    for k in ks:
        s_list, y_list = [], []
        for key, vals in per.items():
            if len(vals) < k:
                continue
            pick = rng.choice(len(vals), size=k, replace=False)
            s_list.append(float(np.mean([vals[p] for p in pick])))
            y_list.append(lab[key])
        out[k] = auc(np.array(s_list), np.array(y_list)) if len(s_list) >= 4 else float("nan")
    return out


def bootstrap_ci(rows: List[dict], scores: np.ndarray, n_boot: int = 400,
                 seed: int = 0, alpha: float = 0.05) -> Tuple[float, float]:
    """Percentile CI for per-AOI AUC, resampling PARTICIPANTS (not rows).

    Resampling rows would treat 40 trials from one person as 40 independent
    observations and produce an interval far too tight.
    """
    parts = sorted({r["participant"] for r in rows})
    by_part: Dict[str, List[int]] = {p: [] for p in parts}
    for i, r in enumerate(rows):
        by_part[r["participant"]].append(i)
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_boot):
        pick = rng.choice(len(parts), size=len(parts), replace=True)
        idx: List[int] = []
        for p in pick:
            idx.extend(by_part[parts[p]])
        idx = [i for i in idx if not np.isnan(scores[i])]
        if len(idx) < 20:
            continue
        s = scores[np.array(idx)]
        y = np.array([1 if rows[i]["familiar"] else 0 for i in idx])
        a = auc(s, y)
        if not np.isnan(a):
            vals.append(a)
    if len(vals) < 20:
        return float("nan"), float("nan")
    return (float(np.percentile(vals, 100 * alpha / 2)),
            float(np.percentile(vals, 100 * (1 - alpha / 2))))


# ---- report ---------------------------------------------------------------
def evaluate(sessions: List[dict], soft: bool = True, l2: float = 1.0,
             seed: int = 0, n_boot: int = 400,
             labels_dir: Optional[str] = None,
             label_threshold: int = DEFAULT_THRESHOLD,
             item_class: Optional[str] = None,
             item_tier: Optional[str] = None,
             verbose: bool = False) -> dict:
    rows: List[dict] = []
    for s in sessions:
        rows.extend(extract_session(s, soft=soft))
    if not rows:
        return {"error": "no scorable AOI rows"}

    subset = None
    for attr, value in (("class", item_class), ("tier", item_tier)):
        if not value:
            continue
        rows = filter_by_item_attribute(rows, attr, value)
        subset = f"{attr}={value}" if subset is None else f"{subset}, {attr}={value}"
        if not rows:
            return {"error": f"no AOI rows with {attr}={value!r}; check the manifest "
                             f"for the values this experiment actually uses"}

    # E2/E3 ground truth is the questionnaire, not the counterbalance role
    # (labels.py explains why). Refuse rather than score the wrong label.
    exps = {r.get("experiment") for r in rows}
    needs_self_report = exps & set(SELF_REPORT_EXPERIMENTS)
    label_report = None
    if needs_self_report:
        if not labels_dir:
            return {"error": (
                f"experiment(s) {sorted(needs_self_report)} need post-hoc "
                f"questionnaire labels; pass --labels <dir>. Scoring these "
                f"against the counterbalance role would measure a label the "
                f"design never controlled.")}
        labs = load_labels(labels_dir, verbose=verbose)
        if not labs:
            return {"error": f"no gazepry.labels.v1 records found in {labels_dir}"}
        rows, label_report = apply_labels(rows, labs, threshold=label_threshold,
                                          verbose=verbose)
        if not rows:
            return {"error": "no AOI rows survived self-report labelling "
                             "(no questionnaire covers the captured sessions)"}
        pos, neg = class_balance(rows)
        if pos < 10 or neg < 10:
            return {"error": f"self-report labels are too imbalanced to score "
                             f"({pos} familiar / {neg} unfamiliar)"}

    # Segmentation health. If I-DT finds no fixations (which is what a lab-grade
    # dispersion threshold does to webcam-noise data), every fixation-derived
    # feature silently collapses to a constant and quietly reports AUC 0.500 --
    # indistinguishable from "no effect". Surface it instead.
    n_trials_seen = len({(r["participant"], r["sessionId"], r["trial"]) for r in rows})
    total_fix = sum(r["features"]["fix_count"] for r in rows)
    fix_per_trial = total_fix / n_trials_seen if n_trials_seen else 0.0

    X, y, groups, items = design_matrix(rows, relative=True)
    scores, _ = lopo_scores(X, y, groups, l2=l2)
    y = np.asarray(y)

    valid = ~np.isnan(scores)
    res = {
        "n_sessions": len(sessions),
        "n_participants": len(set(groups)),
        "n_rows": len(rows),
        "n_scored": int(valid.sum()),
        "n_items": len(set(items)),
        "fixations_per_trial": fix_per_trial,
        "label_source": "self-report" if needs_self_report else "counterbalance",
        "label_report": label_report,
        "item_subset": subset,
    }
    res["auc_per_aoi"] = auc(scores[valid], y[valid])
    res["auc_ci"] = bootstrap_ci(rows, scores, n_boot=n_boot, seed=seed)
    res["tpr_at_fpr10"] = tpr_at_fpr(scores[valid], y[valid], 0.1)
    acc, n_tr, chance = probe_identification(rows, scores)
    res["probe_id_acc"], res["probe_id_n"], res["probe_id_chance"] = acc, n_tr, chance
    ks = feasible_ks(rows, scores)
    res["auc_vs_k"] = item_level_auc_vs_k(rows, scores, ks, seed=seed)
    res["k_ceiling"] = max(ks) if ks else 0

    # ---- RQ0 gate --------------------------------------------------------
    s_null, y_null = lopo_scores(X, y, groups, l2=l2, seed=seed, shuffle_labels=True)
    v = ~np.isnan(s_null)
    res["null_shuffled_auc"] = auc(s_null[v], np.asarray(y_null)[v])
    s_sal = saliency_baseline_scores(rows, y, groups, l2=l2)
    v = ~np.isnan(s_sal)
    res["null_saliency_auc"] = auc(s_sal[v], y[v]) if v.any() else float("nan")

    # ---- per-feature d' (temporal vs spatial families, RQ4) --------------
    per_feat = {}
    fam = y == 1
    for j, name in enumerate(FEATURE_NAMES):
        col = np.array([r["rel"][name] for r in rows])
        per_feat[name] = {
            "d": cohens_d(col[fam], col[~fam]),
            "auc": auc(col, y),
        }
    res["per_feature"] = per_feat
    res["rows"] = rows
    res["scores"] = scores
    return res


def rq0_verdict(res: dict) -> Tuple[bool, List[str]]:
    """Apply the section-5 RQ0 decision rule. Returns (passed, reasons)."""
    reasons = []
    ok = True
    lo, hi = res.get("auc_ci", (float("nan"), float("nan")))
    if not (isinstance(lo, float) and lo > CHANCE):
        ok = False
        reasons.append(f"per-AOI AUC CI lower bound {lo:.3f} does not exceed chance {CHANCE}")
    ns = res.get("null_shuffled_auc", float("nan"))
    if not (abs(ns - CHANCE) < 0.05):
        ok = False
        reasons.append(f"shuffled-label null AUC {ns:.3f} is not ~{CHANCE} (should collapse)")
    nsal = res.get("null_saliency_auc", float("nan"))
    if not (np.isnan(nsal) or abs(nsal - CHANCE) < 0.05):
        ok = False
        reasons.append(f"saliency-only baseline AUC {nsal:.3f} is not ~{CHANCE} "
                       f"(counterbalancing may have failed)")
    return ok, reasons


def report(res: dict, plot: Optional[str] = None) -> None:
    if "error" in res:
        print("ERROR:", res["error"])
        return
    print(f"sessions={res['n_sessions']}  participants={res['n_participants']}  "
          f"items={res['n_items']}  AOI rows={res['n_rows']} (scored {res['n_scored']})")
    if res.get("item_subset"):
        print(f"item subset: {res['item_subset']} — this is a per-class contrast, "
              f"not the pooled result")
    src = res.get("label_source", "counterbalance")
    print(f"labels: {src}"
          + (f"  (threshold >= {res['label_report']['threshold']}, "
             f"{res['label_report']['relabelled_vs_counterbalance']} rows differ "
             f"from the counterbalance role)" if res.get("label_report") else ""))
    fpt = res.get("fixations_per_trial", 0.0)
    print(f"segmentation: {fpt:.2f} I-DT fixations per trial")
    if fpt < 1.0:
        print("  WARNING: near-zero fixations detected. Every fixation-derived")
        print("  feature is now constant and will report AUC 0.500 regardless of")
        print("  the truth. Raise features.DISP_THRESHOLD or IDT_SMOOTH_WIN for")
        print("  this sensor before believing any per-feature number below.")
    print()
    lo, hi = res["auc_ci"]
    print("  headline")
    print(f"    per-AOI AUC            {res['auc_per_aoi']:.3f}   "
          f"95% CI over participants [{lo:.3f}, {hi:.3f}]")
    print(f"    TPR @ FPR=0.10         {res['tpr_at_fpr10']:.3f}")
    if not np.isnan(res["probe_id_acc"]):
        print(f"    probe identification   {res['probe_id_acc']:.3f}   "
              f"(chance {res['probe_id_chance']:.3f}, n={res['probe_id_n']} trials)")
    print()
    print("  item-level AUC vs k trials aggregated  (the headline curve)")
    if not res["auc_vs_k"]:
        print("    (no (participant, item) pair was shown often enough to aggregate)")
    for k, v in sorted(res["auc_vs_k"].items()):
        print(f"    k={k:<3d} {'nan' if np.isnan(v) else f'{v:.3f}'}")
    print(f"    design ceiling: k={res.get('k_ceiling', 0)} "
          f"(more trials per item raises this)")
    print()
    print("  RQ0 gate  (both nulls must sit at ~0.500)")
    print(f"    shuffled-label null    {res['null_shuffled_auc']:.3f}")
    nsal = res["null_saliency_auc"]
    print(f"    saliency-only baseline {'nan' if np.isnan(nsal) else f'{nsal:.3f}'}")
    ok, reasons = rq0_verdict(res)
    print(f"    verdict: {'PASS' if ok else 'FAIL'}")
    for r in reasons:
        print(f"      - {r}")
    print()
    print("  per-feature separation  (temporal families are the ones predicted")
    print("  to survive concealment -- Millen & Hancock 2019)")
    print(f"    {'feature':<22s} {'d':>7s} {'AUC':>7s}")
    for name, v in res["per_feature"].items():
        print(f"    {name:<22s} {v['d']:>7.3f} {v['auc']:>7.3f}")

    if plot:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            print(f"\n  (matplotlib not installed - skipping {plot})")
            return
        ks = sorted(res["auc_vs_k"])
        vs = [res["auc_vs_k"][k] for k in ks]
        plt.figure(figsize=(5, 3.4))
        plt.plot(ks, vs, "o-")
        plt.axhline(CHANCE, ls="--", c="gray", lw=1, label="chance")
        plt.xlabel("trials aggregated per item (k)")
        plt.ylabel("item-level AUC")
        plt.title("Recognition leakage vs observation budget")
        plt.ylim(0.4, 1.0)
        plt.legend()
        plt.tight_layout()
        plt.savefig(plot, dpi=150)
        print(f"\n  wrote {plot}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="D7 recognition-leakage evaluation")
    ap.add_argument("--data", default="../data", help="directory of session JSON files")
    ap.add_argument("--experiment", choices=["E1", "E2", "E3"], help="restrict to one experiment")
    ap.add_argument("--tracker", help="restrict to one tracker family")
    ap.add_argument("--awareness", choices=["naive", "countermeasure"])
    ap.add_argument("--labels", help="directory of questionnaire responses "
                                     "(required for E2/E3)")
    ap.add_argument("--label-threshold", type=int, default=DEFAULT_THRESHOLD,
                    help="ordinal cut for 'familiar' on the 0-3 self-report scale "
                         f"(default {DEFAULT_THRESHOLD} = has genuine prior exposure)")
    ap.add_argument("--item-class",
                    help="restrict to one manifest item class (E2: face/bank/landmark). "
                         "Arrays are class-homogeneous, so this keeps whole trials.")
    ap.add_argument("--item-tier",
                    help="restrict to one expected-penetration tier (high/medium/low) — "
                         "the 'high-salience items only' fallback analysis")
    ap.add_argument("--hard-aoi", action="store_true",
                    help="hard nearest-AOI assignment instead of soft (the §7.1 contrast)")
    ap.add_argument("--l2", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--boot", type=int, default=400)
    ap.add_argument("--plot", help="write the AUC-vs-k curve to this PNG")
    a = ap.parse_args(argv)

    sessions = load_probe_sessions(a.data, experiment=a.experiment, tracker=a.tracker,
                                   awareness=a.awareness, verbose=True)
    if not sessions:
        print(f"no probe sessions (schema gazepry.probe.v1) found in {a.data}")
        return 1
    print(f"loaded {len(sessions)} probe session(s) from {a.data}"
          f"{' [' + a.experiment + ']' if a.experiment else ''}")
    print(f"AOI assignment: {'hard' if a.hard_aoi else 'soft'}\n")
    res = evaluate(sessions, soft=not a.hard_aoi, l2=a.l2, seed=a.seed, n_boot=a.boot,
                   labels_dir=a.labels, label_threshold=a.label_threshold,
                   item_class=a.item_class, item_tier=a.item_tier, verbose=True)
    if "error" in res:
        print("ERROR:", res["error"])
        return 1
    report(res, plot=a.plot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
