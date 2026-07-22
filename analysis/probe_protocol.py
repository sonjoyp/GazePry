"""
Python port of ../public/probe-protocol.js (Direction D7 trial protocol).

The browser task page is the source of truth for what a participant sees; this
port exists so the simulator and the offline analysis can rebuild the same trial
plan without a browser. It must stay byte-identical to the JS -- the parity test
(test/probe-plan-cli.js + test_analysis.py::TestProbeProtocolParity) compares the
FULL plan (item ids, familiarity roles, slot order) for several participants, so
any divergence fails loudly rather than silently producing a different design.

The PRNG is reproduced exactly by keeping every intermediate masked to uint32:
JavaScript's bitwise operators work on 32-bit two's-complement values, and the
low 32 bits of add/multiply/xor are identical whether the operands are read as
signed or unsigned. So uint32 arithmetic here reproduces int32 arithmetic there.
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional

MASK = 0xFFFFFFFF


def _u32(v: int) -> int:
    return v & MASK


def _imul(a: int, b: int) -> int:
    """Math.imul: low 32 bits of the product."""
    return _u32(_u32(a) * _u32(b))


def mulberry32(seed: int):
    state = {"a": _u32(seed)}

    def rnd() -> float:
        state["a"] = _u32(state["a"] + 0x6D2B79F5)
        t = state["a"]
        t = _imul(t ^ (t >> 15), t | 1)
        t = _u32(t ^ _u32(t + _imul(t ^ (t >> 7), t | 61)))
        return _u32(t ^ (t >> 14)) / 4294967296.0

    return rnd


def hash_seed(s) -> int:
    """FNV-1a over a string -> 32-bit seed."""
    h = _u32(2166136261)
    for ch in str(s):
        h = _u32(h ^ (ord(ch) & MASK))
        h = _imul(h, 16777619)
    return _u32(h)


def shuffled(arr: List, rnd) -> List:
    a = list(arr)
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]
    return a


# ---- stimulus sets (mirror of the JS tables) ------------------------------
def _make_abstract_items(n: int) -> List[dict]:
    return [{
        "id": "abs" + ("0" if i < 10 else "") + str(i),
        "label": "", "kind": "abstract",
        "hue": round((360 / n) * i), "glyph": i % 6, "seed": 1009 + i * 37,
    } for i in range(n)]


_BRANDS = [
    ("mail", "Mailbox", "high"), ("vid", "Streamline", "high"),
    ("shop", "Marketplace", "high"), ("soc", "Circle", "high"),
    ("map", "Wayfind", "high"), ("news", "Dispatch", "medium"),
    ("bank", "Ledger", "medium"), ("fit", "Stride", "medium"),
    ("code", "Forge", "medium"), ("note", "Sheaf", "medium"),
    ("trav", "Compass", "low"), ("food", "Larder", "low"),
    ("game", "Arcade", "low"), ("learn", "Tutor", "low"),
    ("photo", "Album", "low"), ("music", "Chord", "low"),
]

_TOPICS = [
    ("t_sleep", "Sleep problems", "health"), ("t_diab", "Blood sugar", "health"),
    ("t_ment", "Therapy options", "health"), ("t_derm", "Skin conditions", "health"),
    ("t_debt", "Debt consolidation", "finance"), ("t_mort", "Mortgage rates", "finance"),
    ("t_pens", "Retirement planning", "finance"), ("t_tax", "Tax deductions", "finance"),
    ("t_tenc", "Tenant rights", "legal"), ("t_will", "Making a will", "legal"),
    ("t_emp", "Employment disputes", "legal"), ("t_imm", "Visa paperwork", "legal"),
    ("t_vote", "Voter registration", "civic"), ("t_coun", "Local council", "civic"),
    ("t_recy", "Recycling rules", "civic"), ("t_perm", "Building permits", "civic"),
]


def _make_brand_items() -> List[dict]:
    return [{"id": d[0], "label": d[1], "kind": "brand", "tier": d[2],
             "hue": (i * 47) % 360, "glyph": i % 6, "seed": 3001 + i * 53}
            for i, d in enumerate(_BRANDS)]


def _make_topic_items() -> List[dict]:
    return [{"id": d[0], "label": d[1], "kind": "topic", "category": d[2],
             "hue": (i * 31 + 200) % 360, "glyph": i % 6, "seed": 5003 + i * 71}
            for i, d in enumerate(_TOPICS)]


SETS: Dict[str, dict] = {
    "E1": {"id": "E1", "label": "Lab-installed familiarity",
           "studyPhase": True, "items": _make_abstract_items(24)},
    "E2": {"id": "E2", "label": "Real-world service familiarity",
           "studyPhase": False, "selfReportLabels": True, "items": _make_brand_items()},
    "E3": {"id": "E3", "label": "Sensitive-topic exposure",
           "studyPhase": False, "selfReportLabels": True, "items": _make_topic_items()},
}

N_GROUPS = 4
GEOM = {"minTileW": 400, "minTileH": 300, "minGap": 250, "edgeMargin": 40}
TIMING = {"fixationMs": 500, "arrayMs": 4000, "blankMs": 300}


def group_for(participant: str) -> int:
    """Prefer the participant NUMBER over a hash, so sequentially numbered IDs
    land in the four groups perfectly evenly. With a hash, group sizes drift
    apart at small N, the per-item marginal probability of "familiar" stops
    being 0.5 across the cohort, and item identity starts carrying information
    about familiarity -- which is exactly what the RQ0 saliency baseline is
    meant to find at chance."""
    m = re.search(r"(\d+)\s*$", str(participant))
    if m:
        return int(m.group(1)) % N_GROUPS
    return hash_seed("cb:" + str(participant)) % N_GROUPS


def is_familiar(item_index: int, group: int) -> bool:
    return ((item_index + group) % N_GROUPS) < N_GROUPS / 2


def build_trials(participant: str, experiment: str = "E1", array_n: int = 4,
                 n_trials: int = 40, group: Optional[int] = None) -> dict:
    """Rebuild one participant's counterbalanced trial plan. See the JS for the
    design rationale (§6.4): one familiar-role probe per trial among
    ``array_n - 1`` unfamiliar-role irrelevants, slot order randomised."""
    s = SETS.get(experiment)
    if not s:
        raise ValueError("unknown experiment: " + str(experiment))
    array_n = 2 if array_n == 2 else 4
    if group is None:
        group = group_for(participant)
    rnd = mulberry32(hash_seed(f"{participant}|{experiment}|{array_n}"))

    items = [{"item": it, "index": i, "familiar": is_familiar(i, group)}
             for i, it in enumerate(s["items"])]
    fam = [r for r in items if r["familiar"]]
    unf = [r for r in items if not r["familiar"]]
    if not fam or len(unf) < array_n - 1:
        raise ValueError(f"stimulus set too small for arrayN={array_n}")

    trials = []
    probe_queue: List[dict] = []
    for t in range(n_trials):
        if not probe_queue:
            probe_queue = shuffled(fam, rnd)
        probe = probe_queue.pop()
        pool = [r for r in shuffled(unf, rnd) if r["item"]["id"] != probe["item"]["id"]]
        slots = shuffled([probe] + pool[:array_n - 1], rnd)
        trials.append({
            "index": t,
            "probeItemId": probe["item"]["id"],
            "slots": [{"slot": i, "itemId": r["item"]["id"],
                       "familiar": r["familiar"], "item": r["item"]}
                      for i, r in enumerate(slots)],
        })
    return {"participant": participant, "experiment": experiment, "arrayN": array_n,
            "counterbalanceGroup": group, "nTrials": n_trials, "trials": trials}


def layout(array_n: int, vw: int, vh: int) -> dict:
    cols = 2
    rows = 1 if array_n == 2 else 2
    gap = GEOM["minGap"]
    avail_w = vw - 2 * GEOM["edgeMargin"] - (cols - 1) * gap
    avail_h = vh - 2 * GEOM["edgeMargin"] - (rows - 1) * gap
    tw, th = int(avail_w // cols), int(avail_h // rows)
    ok = tw >= GEOM["minTileW"] and th >= GEOM["minTileH"]
    total_w = cols * tw + (cols - 1) * gap
    total_h = rows * th + (rows - 1) * gap
    x0 = round((vw - total_w) / 2)
    y0 = round((vh - total_h) / 2)
    rects = []
    for i in range(array_n):
        c, r = i % cols, i // cols
        rects.append({"x": x0 + c * (tw + gap), "y": y0 + r * (th + gap), "w": tw, "h": th})
    return {"ok": ok, "cols": cols, "rows": rows, "gap": gap,
            "tileW": tw, "tileH": th, "rects": rects}
