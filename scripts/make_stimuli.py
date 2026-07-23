"""
Generate the D7 stimulus packs as real image files, plus their manifest.

    python scripts/make_stimuli.py                 # write public/stimuli/
    python scripts/make_stimuli.py --check         # validate an existing pack

Why generated images rather than photographs, for E1
----------------------------------------------------
E1's entire validity rests on the participant having **no prior exposure** to
the stimuli, so that familiarity is created only by the study phase and the
ground truth is exact. Photographs of real objects, places, or people fail that:
everyone has seen a beach, a dog, a keyboard, and the "novel" items would carry
uncontrolled pre-existing familiarity that no counterbalancing can remove.

So E1 uses **Julia-set fractals**: visually rich and highly distinctive (unlike
a few coloured blobs, which participants struggle to tell apart), while being
genuinely novel to every participant. Richly-detailed novel abstract images are
the standard stimulus class for recognition-memory work for exactly this reason.
They are deterministic from a seed, so the pack is reproducible from a clean
checkout and is safe to commit.

E2 and E3 are different
-----------------------
Those experiments measure *naturally acquired* familiarity, so they need the
real thing: the actual faces, logos, places, and topic cards the participant has
or has not encountered in ordinary life. This script writes **placeholders** so
the harness runs and the tests pass from a clean checkout, and
``scripts/fetch_stimuli.py`` installs the real assets over the top from
Wikimedia Commons. Placeholders are marked ``"placeholder": true`` in the
manifest and the task page refuses to run a set that still contains any --
collecting a whole cohort against stand-ins would be unrecoverable.

This script is therefore the *design* of the stimulus packs (which items exist,
what class and expected-penetration tier each one has) and the fetcher is the
*sourcing* of them. Run them in that order.

No image dependency: PNGs are written with stdlib zlib + struct.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import struct
import sys
import zlib
from typing import List, Optional

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, "public", "stimuli")

# Generated at 4:3. Tiles are ~735x400 px at 1920x1080 with a 4-tile array, so
# 800x600 gives headroom for a larger display without upscaling artefacts.
W, H = 800, 600

# Minimum usable size for a REAL (dropped-in) asset. Below this the image is
# upscaled into the tile and detail the recognition effect depends on is lost.
MIN_W, MIN_H = 600, 450

# Must match ProbeProtocol.N_GROUPS / probe_protocol.N_GROUPS. Only used to
# validate that a class-grouped set can fill an array for every group.
N_GROUPS = 4


# ---- minimal PNG writer ---------------------------------------------------
def write_png(path: str, rgb: np.ndarray) -> None:
    """Write an (H, W, 3) uint8 array as a PNG. stdlib only."""
    h, w, _ = rgb.shape
    raw = b"".join(b"\x00" + rgb[y].tobytes() for y in range(h))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)


def read_png_size(path: str):
    """(width, height) from a PNG/JPEG header, or None if unreadable.

    Used by --check so a dropped-in asset that is too small to fill a tile is
    caught before a cohort is run against it, not after.
    """
    try:
        with open(path, "rb") as fh:
            head = fh.read(32)
            if head[:8] == b"\x89PNG\r\n\x1a\n":
                w, h = struct.unpack(">II", head[16:24])
                return int(w), int(h)
            if head[:2] == b"\xff\xd8":            # JPEG: walk the segments
                fh.seek(2)
                while True:
                    b = fh.read(1)
                    while b and b != b"\xff":
                        b = fh.read(1)
                    marker = fh.read(1)
                    while marker == b"\xff":
                        marker = fh.read(1)
                    if not marker:
                        return None
                    if marker[0] in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                                     0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                        fh.read(3)
                        h, w = struct.unpack(">HH", fh.read(4))
                        return int(w), int(h)
                    size = struct.unpack(">H", fh.read(2))[0]
                    fh.seek(size - 2, 1)
    except (OSError, struct.error):
        return None
    return None


# ---- colour ---------------------------------------------------------------
def hsv_to_rgb(h: np.ndarray, s: np.ndarray, v: np.ndarray) -> np.ndarray:
    i = np.floor(h * 6.0).astype(int) % 6
    f = h * 6.0 - np.floor(h * 6.0)
    p, q, t = v * (1 - s), v * (1 - f * s), v * (1 - (1 - f) * s)
    out = np.zeros(h.shape + (3,), dtype=float)
    for k, (r, g, b) in enumerate([(v, t, p), (q, v, p), (p, v, t),
                                   (p, q, v), (t, p, v), (v, p, q)]):
        m = i == k
        out[m] = np.stack([r, g, b], axis=-1)[m]
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)


# ---- E1: Julia-set fractals ----------------------------------------------
def julia(seed: int) -> np.ndarray:
    """A distinctive, richly detailed, genuinely novel image.

    Two things make these usable as recognition stimuli rather than wallpaper:

    * **Histogram-equalised escape time.** Mapping raw escape count to
      brightness wastes nearly the whole dynamic range, because most points
      escape in the first few iterations. The result is a dark image with a thin
      bright rim: low variance, few distinct colours, and hard to tell from the
      next one. Rank-transforming the exterior spreads detail across the full
      range instead.
    * **An orbit trap for the interior.** Filling the non-escaping set with a
      flat colour discards the visually richest region. Colouring it by the
      orbit's closest approach to the origin gives the interior its own
      structure, which is what keeps two fractals with similar parameters
      looking different.
    """
    rng = np.random.default_rng(seed)
    theta = rng.uniform(0, 2 * math.pi)
    # Wider |c| than the classic "pretty" band. Near 0.75 every Julia set is a
    # symmetric multi-lobed blob; reaching out towards the boundary brings in
    # dendritic and spiral morphologies, so the set varies in SHAPE and not
    # only in colour.
    radius = rng.uniform(0.55, 1.02)
    c = complex(radius * math.cos(theta), radius * math.sin(theta))
    zoom = rng.uniform(1.15, 1.75)
    hue0 = rng.uniform(0, 1)
    hue_span = rng.uniform(0.35, 1.30)
    spin = 1.0 if rng.random() < 0.5 else -1.0
    # Contrast curve: <1 lifts the midtones (soft, airy), >1 crushes them
    # (hard-edged, high contrast). Without this every image ends up with the
    # same luminance profile because the rank transform is uniform by
    # construction.
    gamma = float(rng.uniform(0.45, 2.2))
    dark_bg = bool(rng.random() < 0.5)

    x = np.linspace(-zoom * W / H, zoom * W / H, W)
    y = np.linspace(-zoom, zoom, H)
    Z = x[None, :] + 1j * y[:, None]

    n_iter = 120
    counts = np.zeros(Z.shape, dtype=float)
    trap = np.full(Z.shape, 1e9, dtype=float)      # orbit trap: min |z| seen
    alive = np.ones(Z.shape, dtype=bool)
    for i in range(n_iter):
        Z[alive] = Z[alive] * Z[alive] + c
        az = np.abs(Z)
        np.minimum(trap, np.where(alive, az, 1e9), out=trap)
        esc = alive & (az > 2.0)
        # Smooth (continuous) escape time avoids visible banding. It can go
        # slightly negative for points that overshoot in the first iterations,
        # which would make the normalised value negative and its fractional
        # power NaN -- and a NaN cast to uint8 is a garbage pixel, not an
        # obvious error. Clamp at zero.
        counts[esc] = np.maximum(
            0.0, i + 1 - np.log2(np.maximum(np.log2(az[esc]), 1e-9)))
        alive &= ~esc
    counts[alive] = n_iter

    # exterior: rank-transform (histogram equalisation) over escaped points only
    norm = np.zeros(counts.shape, dtype=float)
    out = ~alive
    if out.any():
        vals = counts[out]
        order = np.argsort(vals, kind="mergesort")
        ranks = np.empty(len(vals), dtype=float)
        ranks[order] = np.linspace(0.0, 1.0, len(vals))
        norm[out] = ranks

    hue = np.empty(counts.shape)
    sat = np.empty(counts.shape)
    val = np.empty(counts.shape)

    shaped = np.power(norm, gamma)
    hue[out] = (hue0 + spin * hue_span * norm[out]) % 1.0
    sat[out] = np.clip(0.40 + 0.55 * (1.0 - shaped[out]), 0, 1)
    val[out] = (np.clip(0.10 + 0.90 * shaped[out], 0, 1) if dark_bg
                else np.clip(0.95 - 0.80 * shaped[out], 0, 1))

    if alive.any():
        tin = np.clip(trap[alive] / 2.0, 0.0, 1.0)
        hue[alive] = (hue0 + 0.45 + 0.35 * tin) % 1.0
        sat[alive] = np.clip(0.25 + 0.65 * tin, 0, 1)
        val[alive] = np.clip(0.08 + 0.62 * (1.0 - tin), 0, 1)
    return hsv_to_rgb(hue, sat, val)


def _thumb(img: np.ndarray) -> np.ndarray:
    """Small COLOUR signature used for the distinctiveness check.

    Greyscale would be the obvious choice and is wrong here: two fractals with
    the same luminance structure but completely different palettes score as
    identical, so the check waves through pairs a participant would find easy to
    confuse in shape while the colours differ. Keeping the channels separate
    makes both hue and structure count.
    """
    return img[::20, ::20].astype(float)


def distinct_julias(n: int, base_seed: int, min_diff: float = 22.0,
                    max_tries: int = 4000):
    """Generate ``n`` fractals that are all visually distinguishable.

    Random parameters occasionally land two images on nearly the same picture.
    In a recognition study that is not cosmetic: if a 'novel' tile looks like
    one the participant studied, the familiarity contrast is contaminated in a
    way no counterbalancing can undo. Candidates are therefore rejected until
    every pair differs by at least ``min_diff`` mean absolute RGB level, and
    the achieved minimum is reported rather than assumed. The comparison is
    made in colour on purpose: an earlier greyscale check passed pairs that
    shared structure and differed only in hue.
    """
    kept: List[np.ndarray] = []
    thumbs: List[np.ndarray] = []
    seeds: List[int] = []
    tries = 0
    seed = base_seed
    while len(kept) < n and tries < max_tries:
        tries += 1
        seed += 37
        img = julia(seed)
        th = _thumb(img)
        if any(float(np.abs(th - t).mean()) < min_diff for t in thumbs):
            continue
        kept.append(img)
        thumbs.append(th)
        seeds.append(seed)
    if len(kept) < n:
        raise RuntimeError(
            f"only found {len(kept)}/{n} sufficiently distinct fractals in "
            f"{tries} tries; lower min_diff or widen the parameter ranges")
    worst = min(float(np.abs(thumbs[i] - thumbs[j]).mean())
                for i in range(len(thumbs)) for j in range(i + 1, len(thumbs)))
    return kept, seeds, worst, tries


# ---- E2/E3: placeholder marks --------------------------------------------
def placeholder_mark(seed: int, hue: float) -> np.ndarray:
    """A distinct geometric mark standing in for a real logo / topic card.

    Deliberately does NOT look photographic: an operator glancing at the screen
    should be able to tell instantly that a real asset has not been installed.
    """
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy = W / 2.0, H / 2.0
    dx, dy = (xx - cx) / (W / 2), (yy - cy) / (H / 2)
    r = np.sqrt(dx * dx + dy * dy)
    ang = np.arctan2(dy, dx)

    petals = int(rng.integers(3, 9))
    phase = rng.uniform(0, 2 * math.pi)
    shape = np.cos(petals * ang + phase) * 0.30 + 0.62
    band = np.abs(r - shape) < rng.uniform(0.06, 0.13)
    inner = r < rng.uniform(0.16, 0.28)

    hue_a = np.full((H, W), hue % 1.0)
    sat = np.full((H, W), 0.20)
    val = np.full((H, W), 0.10)
    val[band] = 0.85
    sat[band] = 0.70
    val[inner] = 0.95
    sat[inner] = 0.35
    return hsv_to_rgb(hue_a, sat, val)


# ---- item tables ----------------------------------------------------------
E1_N = 24

# E2: three CLASSES of eight, and the ordering is load-bearing twice over.
#
#  * Arrays are built class-homogeneously (see `arrayGroupBy` below), because an
#    array mixing a face with three bank logos lets the probe be picked out by
#    category rather than by familiarity, and adds category-driven saliency
#    variance to every trial. The ocular-CIT arrays this design follows are
#    all-faces for the same reason.
#  * Each class occupies eight CONTIGUOUS indices. The Latin square makes item i
#    familiar for group g iff ((i + g) mod 4) < 2, so a block of eight splits
#    exactly 4 familiar / 4 unfamiliar for *every* group -- which is what
#    guarantees each class can always fill a 4-tile array (1 probe + 3
#    irrelevants). Reordering this table, or making a class a size that is not a
#    multiple of N_GROUPS, silently breaks that guarantee.
#
# Tiers record *expected* penetration, which drives the "high-salience items
# only" fallback analysis. They are a hypothesis about the cohort, not a label:
# the ground truth is always the post-hoc questionnaire.
#
# Faces and logos carry no on-tile caption (label ""): a caption would let the
# participant read the name instead of recognising the image, which is a
# different memory system from the one the effect rests on. `name` is for the
# questionnaire, the operator log, and the attribution file only.
E2_ITEMS = [
    # (id, name, class, tier)
    ("f_obama", "Barack Obama", "face", "high"),
    ("f_swift", "Taylor Swift", "face", "high"),
    ("f_messi", "Lionel Messi", "face", "high"),
    ("f_merkel", "Angela Merkel", "face", "medium"),
    ("f_ardern", "Jacinda Ardern", "face", "medium"),
    ("f_thunberg", "Greta Thunberg", "face", "medium"),
    ("f_miyamoto", "Shigeru Miyamoto", "face", "low"),
    ("f_strickland", "Donna Strickland", "face", "low"),

    ("b_chase", "Chase", "bank", "high"),
    ("b_bofa", "Bank of America", "bank", "high"),
    ("b_wells", "Wells Fargo", "bank", "high"),
    ("b_citi", "Citi", "bank", "high"),
    ("b_hsbc", "HSBC", "bank", "medium"),
    ("b_barclays", "Barclays", "bank", "medium"),
    ("b_santander", "Santander", "bank", "medium"),
    ("b_nordea", "Nordea", "bank", "low"),

    ("l_eiffel", "Eiffel Tower", "landmark", "high"),
    ("l_liberty", "Statue of Liberty", "landmark", "high"),
    ("l_taj", "Taj Mahal", "landmark", "high"),
    ("l_colosseum", "Colosseum", "landmark", "high"),
    ("l_sydney", "Sydney Opera House", "landmark", "medium"),
    ("l_pena", "Pena Palace", "landmark", "low"),
    ("l_sigiriya", "Sigiriya", "landmark", "low"),
    ("l_dragon", "Dragon Bridge, Ljubljana", "landmark", "low"),
]

# E3 is scoped to health / finance / legal / civic and deliberately contains NO
# protected characteristic (sexual orientation, religion, immigration status).
# The method would apply to them, the demonstration does not need them, and
# including them turns a privacy paper into an ethics problem. A JS test and a
# Python test both assert this scoping so it cannot drift back in.
#
# E3 items DO carry an on-tile caption: the card is a headline plus an image,
# which is what a topic card looks like in real web content, and the topic is
# the construct being probed.
E3_ITEMS = [
    ("t_sleep", "Sleep problems", "health"), ("t_diab", "Blood sugar", "health"),
    ("t_ment", "Therapy options", "health"), ("t_derm", "Skin conditions", "health"),
    ("t_debt", "Debt consolidation", "finance"), ("t_mort", "Mortgage rates", "finance"),
    ("t_pens", "Retirement planning", "finance"), ("t_tax", "Tax deductions", "finance"),
    ("t_tenc", "Tenant rights", "legal"), ("t_will", "Making a will", "legal"),
    ("t_emp", "Employment disputes", "legal"), ("t_claims", "Small claims court", "legal"),
    ("t_vote", "Voter registration", "civic"), ("t_coun", "Local council", "civic"),
    ("t_recy", "Recycling rules", "civic"), ("t_perm", "Building permits", "civic"),
]


def _installed_real(out_dir: str) -> dict:
    """Item ids whose REAL asset is already installed, from the current manifest.

    Regenerating used to stamp placeholders back over assets that
    ``fetch_stimuli.py`` had installed, which is a quiet way to lose a stimulus
    pack (and, if it happened between two participants, to split a cohort across
    two different stimulus sets without anything failing). An item that is
    marked ``placeholder: false`` and whose file is still on disk is left alone,
    provenance and all, unless ``--force-placeholders`` is passed.
    """
    mpath = os.path.join(out_dir, "manifest.json")
    if not os.path.exists(mpath):
        return {}
    try:
        with open(mpath, encoding="utf-8") as fh:
            m = json.load(fh)
    except (OSError, ValueError):
        return {}
    keep = {}
    for s in m.get("sets", {}).values():
        for it in s.get("items", []):
            if it.get("placeholder"):
                continue
            fp = os.path.join(out_dir, it.get("file", "").replace("/", os.sep))
            if it.get("file") and os.path.exists(fp):
                keep[it["id"]] = it
    return keep


def build(out_dir: str, force_placeholders: bool = False) -> dict:
    sets = {}
    keep = {} if force_placeholders else _installed_real(out_dir)
    n_kept = 0

    # --- E1 ---------------------------------------------------------------
    d = os.path.join(out_dir, "e1")
    os.makedirs(d, exist_ok=True)
    imgs, seeds, worst, tries = distinct_julias(E1_N, 1009)
    print(f"  E1: {E1_N} mutually distinct fractals in {tries} candidates "
          f"(worst pair differs by {worst:.1f} grey levels)")
    e1 = []
    for i, (img, sd) in enumerate(zip(imgs, seeds)):
        iid = f"abs{i:02d}"
        fn = f"{iid}.png"
        write_png(os.path.join(d, fn), img)
        e1.append({"id": iid, "label": "", "file": f"e1/{fn}",
                   "kind": "fractal", "seed": sd, "placeholder": False})
    sets["E1"] = {
        "id": "E1", "label": "Lab-installed familiarity", "studyPhase": True,
        "selfReportLabels": False,
        "minPairDistance": round(worst, 2),
        "note": "Julia-set fractals: richly detailed but genuinely novel, so "
                "familiarity is created only by the study phase. Every pair is "
                "checked to be visually distinguishable.",
        "items": e1,
    }

    # --- E2 ---------------------------------------------------------------
    d = os.path.join(out_dir, "e2")
    os.makedirs(d, exist_ok=True)
    e2 = []
    for i, (iid, name, cls, tier) in enumerate(E2_ITEMS):
        if iid in keep:
            e2.append(keep[iid])
            n_kept += 1
            continue
        fn = f"{iid}.png"
        write_png(os.path.join(d, fn), placeholder_mark(3001 + i * 53, (i * 0.13) % 1.0))
        e2.append({"id": iid, "label": "", "name": name, "file": f"e2/{fn}",
                   "kind": "brand", "class": cls, "tier": tier, "placeholder": True})
    sets["E2"] = {
        "id": "E2", "label": "Real-world familiarity (faces, banks, places)",
        "studyPhase": False, "selfReportLabels": True,
        # Arrays are drawn within a class, never across. See E2_ITEMS.
        "arrayGroupBy": "class",
        "classes": {
            "face": "Public figures",
            "bank": "Retail bank and payment brands",
            "landmark": "Widely photographed places",
        },
        "note": "Real-world familiarity the participant brought with them. Install "
                "the real assets with scripts/fetch_stimuli.py before collecting.",
        "items": e2,
    }

    # --- E3 ---------------------------------------------------------------
    d = os.path.join(out_dir, "e3")
    os.makedirs(d, exist_ok=True)
    e3 = []
    for i, (iid, label, cat) in enumerate(E3_ITEMS):
        if iid in keep:
            e3.append(keep[iid])
            n_kept += 1
            continue
        fn = f"{iid}.png"
        write_png(os.path.join(d, fn), placeholder_mark(5003 + i * 71, (0.55 + i * 0.09) % 1.0))
        e3.append({"id": iid, "label": label, "name": label, "file": f"e3/{fn}",
                   "kind": "topic", "category": cat, "placeholder": True})
    sets["E3"] = {
        "id": "E3", "label": "Sensitive-topic exposure", "studyPhase": False,
        "selfReportLabels": True,
        # No grouping: every E3 card is the same visual format (image + headline),
        # so an array mixing categories is already visually homogeneous, and
        # four items per category is too few to fill a class-homogeneous array.
        "arrayGroupBy": None,
        "note": "Topic cards. E3 probes exposure to a TOPIC rather than to a "
                "specific image, which is a weaker construct than E1/E2 -- see "
                "public/stimuli/README.md before collecting.",
        "items": e3,
    }

    manifest = {
        "schema": "gazepry.stimuli.v1",
        "generatedBy": "scripts/make_stimuli.py",
        "imageSize": {"w": W, "h": H},
        "minSize": {"w": MIN_W, "h": MIN_H},
        "sets": sets,
    }
    # Sweep files the manifest no longer references. Renaming or retiring an
    # item otherwise leaves its image on disk forever, and an orphan under
    # public/stimuli/ is one manifest edit away from being served as a stimulus
    # with no provenance behind it.
    referenced = {it["file"] for s in sets.values() for it in s["items"]}
    for sub in ("e1", "e2", "e3"):
        d = os.path.join(out_dir, sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            rel = f"{sub}/{fn}"
            if fn.startswith(".") or rel in referenced:
                continue
            os.remove(os.path.join(d, fn))
            print(f"  removed orphan {rel} (no longer in the item table)")

    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    if n_kept:
        print(f"  kept {n_kept} already-installed real asset(s) "
              f"(--force-placeholders overwrites them)")
    return manifest


# ---- validation -----------------------------------------------------------
def check(out_dir: str) -> int:
    mpath = os.path.join(out_dir, "manifest.json")
    if not os.path.exists(mpath):
        print(f"FAIL: no manifest at {mpath} -- run: python scripts/make_stimuli.py")
        return 1
    with open(mpath, encoding="utf-8") as fh:
        m = json.load(fh)

    problems: List[str] = []
    warnings: List[str] = []
    min_w = m.get("minSize", {}).get("w", MIN_W)
    min_h = m.get("minSize", {}).get("h", MIN_H)

    for sid, s in m.get("sets", {}).items():
        items = s.get("items", [])
        if len(items) < 8:
            problems.append(f"{sid}: only {len(items)} items; a 4-tile array needs at least 8")
        ids = [i["id"] for i in items]
        if len(set(ids)) != len(ids):
            problems.append(f"{sid}: duplicate item ids")
        n_placeholder = 0
        for it in items:
            fp = os.path.join(out_dir, it["file"].replace("/", os.sep))
            if not os.path.exists(fp):
                problems.append(f"{sid}/{it['id']}: missing file {it['file']}")
                continue
            size = read_png_size(fp)
            if size is None:
                warnings.append(f"{sid}/{it['id']}: could not read dimensions of {it['file']}")
            elif size[0] < min_w or size[1] < min_h:
                problems.append(f"{sid}/{it['id']}: {size[0]}x{size[1]} is below the "
                                f"{min_w}x{min_h} minimum; it would be upscaled into the tile "
                                f"and lose the detail recognition depends on")
            if it.get("placeholder"):
                n_placeholder += 1
        if n_placeholder:
            warnings.append(f"{sid}: {n_placeholder}/{len(items)} items are PLACEHOLDERS "
                            f"-- do not collect {sid} against these")

        # A grouped set draws every array from within one class, so each class
        # must be able to fill an array on its own for EVERY counterbalance
        # group. The Latin square splits a contiguous block of size 4k into
        # exactly 2k familiar / 2k unfamiliar for every group, so a class that
        # is contiguous and a multiple of N_GROUPS always yields >= 1 probe and
        # >= 3 irrelevants once it has 8 items. Anything else can leave a group
        # unable to build a trial -- at run time, mid-session.
        gb = s.get("arrayGroupBy")
        if gb:
            spans: dict = {}
            for i, it in enumerate(items):
                v = it.get(gb)
                if v is None:
                    problems.append(f"{sid}/{it['id']}: no '{gb}' value, but the set "
                                    f"groups arrays by it")
                    continue
                spans.setdefault(v, []).append(i)
            for v, idxs in spans.items():
                if len(idxs) < 8:
                    problems.append(f"{sid}: {gb}={v} has only {len(idxs)} items; a "
                                    f"class-homogeneous 4-tile array needs at least 8")
                if len(idxs) % N_GROUPS:
                    problems.append(f"{sid}: {gb}={v} has {len(idxs)} items, not a multiple "
                                    f"of {N_GROUPS}; the counterbalance square would not "
                                    f"split it evenly for every group")
                if idxs != list(range(idxs[0], idxs[0] + len(idxs))):
                    problems.append(f"{sid}: {gb}={v} items are not contiguous in the item "
                                    f"table; the counterbalance square is applied over the "
                                    f"global index, so a split block unbalances the class")

    for w in warnings:
        print("WARN: " + w)
    for p in problems:
        print("FAIL: " + p)
    if problems:
        print(f"\n{len(problems)} problem(s).")
        return 1
    total = sum(len(s.get("items", [])) for s in m.get("sets", {}).values())
    print(f"OK: {len(m.get('sets', {}))} sets, {total} items, all files present"
          + (f", {len(warnings)} warning(s)" if warnings else ""))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="generate/validate D7 stimulus packs")
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--check", action="store_true", help="validate instead of generating")
    ap.add_argument("--force-placeholders", action="store_true",
                    help="overwrite already-installed real E2/E3 assets with "
                         "placeholders (the default is to keep them)")
    a = ap.parse_args(argv)
    if a.check:
        return check(a.out)
    os.makedirs(a.out, exist_ok=True)
    m = build(a.out, force_placeholders=a.force_placeholders)
    total = sum(len(s["items"]) for s in m["sets"].values())
    print(f"wrote {total} images + manifest.json to {a.out}")
    print("  E1: real fractal stimuli, ready to use")
    print("  E2/E3: install the real assets with scripts/fetch_stimuli.py")
    return check(a.out)


if __name__ == "__main__":
    raise SystemExit(main())
