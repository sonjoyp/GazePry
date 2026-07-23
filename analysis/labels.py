"""
Post-hoc questionnaire labels for Direction D7 experiments E2 and E3.

E1 installs familiarity in the lab, so its ground truth is the counterbalance
assignment recorded in the session itself. **E2 and E3 do not work that way.**
There, familiarity is whatever the participant actually brought with them, and
the only source of truth is the questionnaire they fill in afterwards
(D7 §6.6). Scoring E2/E3 against the counterbalance flag would be scoring a
label the design never controlled -- the trial builder's `familiar` role is,
for those experiments, only a slot-assignment device.

This module loads `labels/*.json` (schema ``gazepry.labels.v1``) and re-labels
extracted AOI rows against self-report.

The binary cut is applied HERE and not at collection time, on purpose: the
questionnaire stores raw ordinals, so the familiar/unfamiliar threshold stays a
reportable analysis choice rather than an irreversible property of the data.
"""
from __future__ import annotations

import glob
import json
import os
from typing import Dict, List, Optional, Tuple

# Default cut on the 0-3 ordinal scales:
#   E2  0 never heard of it | 1 heard, never used | 2 used occasionally | 3 use regularly
#   E3  0 never | 1 once or twice | 2 several times | 3 regularly
# >=2 means "has genuine prior exposure", which is the construct the attack
# claims to detect. 1 ("heard of it") is deliberately NOT familiar: brand
# recognition without use is a much weaker memory trace and lumping it in would
# inflate the positive class with cases the mechanism does not predict.
DEFAULT_THRESHOLD = 2


def load_labels(labels_dir: str, verbose: bool = False) -> Dict[Tuple[str, str, str], dict]:
    """Load questionnaire records, keyed by (participant, session, experiment).

    When a cell has been answered more than once, the LATEST record wins and the
    duplication is reported -- silently averaging two questionnaires would hide
    a re-run that the operator needs to know about.
    """
    out: Dict[Tuple[str, str, str], dict] = {}
    dupes: List[str] = []
    if not os.path.isdir(labels_dir):
        return out
    for fp in sorted(glob.glob(os.path.join(labels_dir, "*.json"))):
        try:
            with open(fp, encoding="utf-8") as fh:
                rec = json.load(fh)
        except (OSError, ValueError):
            continue
        if rec.get("schema") != "gazepry.labels.v1":
            continue
        key = (rec.get("participant"), rec.get("session"), rec.get("experiment"))
        if key in out:
            dupes.append("/".join(str(k) for k in key))
        if key not in out or rec.get("collectedAt", 0) >= out[key].get("collectedAt", 0):
            out[key] = rec
    if verbose and dupes:
        print(f"  note: {len(dupes)} cell(s) have multiple questionnaires; "
              f"using the most recent for: {', '.join(sorted(set(dupes)))}")
    return out


def response_map(rec: dict) -> Dict[str, Optional[int]]:
    return {i.get("itemId"): i.get("response")
            for i in (rec.get("items") or []) if i.get("itemId")}


def apply_labels(rows: List[dict], labels: Dict[Tuple[str, str, str], dict],
                 threshold: int = DEFAULT_THRESHOLD,
                 verbose: bool = False) -> Tuple[List[dict], dict]:
    """Re-label AOI rows from self-report. Returns (kept_rows, report).

    Rows are DROPPED when no questionnaire covers them or the item was left
    blank. That is deliberate: a missing answer is not evidence of
    unfamiliarity, and defaulting it to False would quietly manufacture
    negatives out of participant fatigue.
    """
    kept: List[dict] = []
    missing_cell, missing_item, flipped = set(), 0, 0
    for r in rows:
        key = (r.get("participant"), r.get("sessionId"), r.get("experiment"))
        rec = labels.get(key)
        if rec is None:
            missing_cell.add("/".join(str(k) for k in key))
            continue
        resp = response_map(rec).get(r.get("itemId"))
        if resp is None:
            missing_item += 1
            continue
        c = dict(r)
        new_familiar = int(resp) >= threshold
        if new_familiar != bool(r.get("familiar")):
            flipped += 1
        c["familiar"] = new_familiar
        c["selfReport"] = int(resp)
        c["labelSource"] = "self-report"
        kept.append(c)

    report = {
        "n_in": len(rows), "n_kept": len(kept),
        "missing_questionnaire_cells": sorted(missing_cell),
        "unanswered_items": missing_item,
        "relabelled_vs_counterbalance": flipped,
        "threshold": threshold,
    }
    if verbose:
        print(f"  self-report labels: kept {len(kept)}/{len(rows)} AOI rows "
              f"(threshold >= {threshold})")
        if missing_cell:
            print(f"    NO QUESTIONNAIRE for {len(missing_cell)} cell(s): "
                  f"{', '.join(sorted(missing_cell))}")
        if missing_item:
            print(f"    {missing_item} row(s) dropped for unanswered items")
        print(f"    {flipped} row(s) differ from the counterbalance role "
              f"(expected for E2/E3 - the design does not control real familiarity)")
    return kept, report


def class_balance(rows: List[dict]) -> Tuple[int, int]:
    pos = sum(1 for r in rows if r.get("familiar"))
    return pos, len(rows) - pos
