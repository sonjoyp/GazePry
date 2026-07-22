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
real thing: actual service logos or homepage screenshots (E2), and real article
or topic-page cards (E3). This script writes **placeholders** so the harness
runs out of the box, and `public/stimuli/README.md` documents how to drop in the
real assets. Placeholders are marked ``"placeholder": true`` in the manifest,
and the task page refuses to run E2/E3 on them without an explicit override --
collecting a whole cohort against placeholder stimuli would be unrecoverable.

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

E2_ITEMS = [
    ("mail", "Mailbox", "high"), ("vid", "Streamline", "high"),
    ("shop", "Marketplace", "high"), ("soc", "Circle", "high"),
    ("map", "Wayfind", "high"), ("news", "Dispatch", "medium"),
    ("bank", "Ledger", "medium"), ("fit", "Stride", "medium"),
    ("code", "Forge", "medium"), ("note", "Sheaf", "medium"),
    ("trav", "Compass", "low"), ("food", "Larder", "low"),
    ("game", "Arcade", "low"), ("learn", "Tutor", "low"),
    ("photo", "Album", "low"), ("music", "Chord", "low"),
]

E3_ITEMS = [
    ("t_sleep", "Sleep problems", "health"), ("t_diab", "Blood sugar", "health"),
    ("t_ment", "Therapy options", "health"), ("t_derm", "Skin conditions", "health"),
    ("t_debt", "Debt consolidation", "finance"), ("t_mort", "Mortgage rates", "finance"),
    ("t_pens", "Retirement planning", "finance"), ("t_tax", "Tax deductions", "finance"),
    ("t_tenc", "Tenant rights", "legal"), ("t_will", "Making a will", "legal"),
    ("t_emp", "Employment disputes", "legal"), ("t_imm", "Visa paperwork", "legal"),
    ("t_vote", "Voter registration", "civic"), ("t_coun", "Local council", "civic"),
    ("t_recy", "Recycling rules", "civic"), ("t_perm", "Building permits", "civic"),
]


def build(out_dir: str) -> dict:
    sets = {}

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
    for i, (iid, label, tier) in enumerate(E2_ITEMS):
        fn = f"{iid}.png"
        write_png(os.path.join(d, fn), placeholder_mark(3001 + i * 53, (i * 0.13) % 1.0))
        e2.append({"id": iid, "label": label, "file": f"e2/{fn}",
                   "kind": "brand", "tier": tier, "placeholder": True})
    sets["E2"] = {
        "id": "E2", "label": "Real-world service familiarity", "studyPhase": False,
        "selfReportLabels": True,
        "note": "PLACEHOLDERS. Replace with real logos or homepage screenshots "
                "before collecting E2 -- see public/stimuli/README.md.",
        "items": e2,
    }

    # --- E3 ---------------------------------------------------------------
    d = os.path.join(out_dir, "e3")
    os.makedirs(d, exist_ok=True)
    e3 = []
    for i, (iid, label, cat) in enumerate(E3_ITEMS):
        fn = f"{iid}.png"
        write_png(os.path.join(d, fn), placeholder_mark(5003 + i * 71, (0.55 + i * 0.09) % 1.0))
        e3.append({"id": iid, "label": label, "file": f"e3/{fn}",
                   "kind": "topic", "category": cat, "placeholder": True})
    sets["E3"] = {
        "id": "E3", "label": "Sensitive-topic exposure", "studyPhase": False,
        "selfReportLabels": True,
        "note": "PLACEHOLDERS. Replace with real topic/article cards before "
                "collecting E3 -- see public/stimuli/README.md.",
        "items": e3,
    }

    manifest = {
        "schema": "gazepry.stimuli.v1",
        "generatedBy": "scripts/make_stimuli.py",
        "imageSize": {"w": W, "h": H},
        "minSize": {"w": MIN_W, "h": MIN_H},
        "sets": sets,
    }
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
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
    a = ap.parse_args(argv)
    if a.check:
        return check(a.out)
    os.makedirs(a.out, exist_ok=True)
    m = build(a.out)
    total = sum(len(s["items"]) for s in m["sets"].values())
    print(f"wrote {total} images + manifest.json to {a.out}")
    print("  E1: real fractal stimuli, ready to use")
    print("  E2/E3: PLACEHOLDERS -- see public/stimuli/README.md before collecting")
    return check(a.out)


if __name__ == "__main__":
    raise SystemExit(main())
