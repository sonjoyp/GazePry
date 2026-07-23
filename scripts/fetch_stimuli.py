"""
Install the REAL E2/E3 stimulus assets from Wikimedia Commons.

    python scripts/fetch_stimuli.py                  # fetch everything in sources.json
    python scripts/fetch_stimuli.py --set E2         # one set
    python scripts/fetch_stimuli.py --relock         # re-resolve, then fetch
    python scripts/fetch_stimuli.py --verify         # offline: hash-check what is on disk

Why this exists
---------------
``make_stimuli.py`` designs the stimulus packs and writes obvious placeholders
for E2/E3. This script sources them. The split matters because E2 and E3 measure
familiarity the participant **brought with them**, so the images have to be the
actual faces, brands, and places they may or may not have encountered -- a
generated stand-in measures nothing, and the task page refuses to run a set that
still contains one.

Three properties this is built around, in order of how much trouble their
absence causes:

**Only free licences.** Every asset is checked against an allow-list of free
licences (public domain, CC0, CC BY, CC BY-SA, FAL) using the licence Commons
itself reports. Anything else is refused, loudly, and not downloaded. Most
retail-bank marks qualify because a plain wordmark is below the threshold of
originality for copyright; a mark that is *not* free simply cannot be used here,
and the fix is to choose a different item rather than to relax the check. Note
this is a copyright test only -- the trademark question (showing a mark to
identify the thing it denotes) is a judgement for you and your institution.

**Reproducibility.** ``sources.json`` says *which person or brand* an item
denotes; a Wikipedia lead image can change under you, so the file that was
actually resolved, its licence, and the SHA-256 of the bytes written are pinned
in ``stimuli.lock.json``. A later run reuses the pinned file unless ``--relock``
is passed, and ``--verify`` re-checks the hashes offline. Two cohorts collected
months apart therefore saw provably the same stimuli, or you find out.

**Attribution.** CC BY and CC BY-SA require credit. ``ATTRIBUTION.md`` is
regenerated from the lock on every fetch, so the credit list cannot drift from
what is on disk, and it is what a paper's stimulus figure cites.

No new dependency: urllib + zlib + struct, numpy only for the letterbox
compositing that ``make_stimuli.py`` already needs numpy for.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from typing import Dict, List, Optional, Tuple

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from make_stimuli import MIN_H, MIN_W, read_png_size, write_png  # noqa: E402

STIM_DIR = os.path.join(ROOT, "public", "stimuli")
SOURCES = os.path.join(STIM_DIR, "sources.json")
LOCK = os.path.join(STIM_DIR, "stimuli.lock.json")
MANIFEST = os.path.join(STIM_DIR, "manifest.json")
ATTRIB = os.path.join(STIM_DIR, "ATTRIBUTION.md")

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

# Wikimedia blocks requests without a descriptive User-Agent carrying a contact.
# Set GAZEPRY_CONTACT to your own address before running against their servers.
DEFAULT_CONTACT = "https://github.com/gazepry (set GAZEPRY_CONTACT)"
USER_AGENT = "GazePry-stimulus-fetcher/1.0 ({contact})"

# Licences whose terms permit redistribution and derivative presentation. The
# match is a normalised prefix test against the LicenseShortName Commons
# reports. NOT on this list, deliberately: every "fair use" / "non-free" tag.
FREE_LICENCE_PREFIXES = (
    "public domain", "pd-", "cc0", "cc by", "cc-by",
    "fal", "free art license", "gfdl", "no restrictions",
)

# Canvas for a letterboxed logo. 4:3 at the fetch width, matching the generated
# packs, so a logo tile and a fractal tile fill the AOI rectangle identically.
CANVAS_BG = (255, 255, 255)
INNER = 0.80          # fraction of the canvas a logo may occupy

MIME_EXT = {
    "image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif",
    "image/webp": ".webp",
}


# ---- HTTP -----------------------------------------------------------------
def _ua() -> str:
    return USER_AGENT.format(contact=os.environ.get("GAZEPRY_CONTACT", DEFAULT_CONTACT))


def _get(url: str, tries: int = 3) -> bytes:
    """GET with a descriptive UA and a short backoff.

    Errors are raised, never swallowed into an empty result: a half-fetched
    stimulus pack that reports success is exactly the failure this whole file
    exists to prevent.
    """
    last: Optional[Exception] = None
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": _ua()})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET failed after {tries} tries: {url} ({last})")


def _api(base: str, params: dict) -> dict:
    params = dict(params, format="json")
    return json.loads(_get(base + "?" + urllib.parse.urlencode(params)).decode("utf-8"))


def _strip_html(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]*>", "", s or "")).strip()


# ---- Commons resolution ---------------------------------------------------
def resolve_lead_image(article: str) -> str:
    """en.wikipedia article -> the file name of its lead image.

    Used for people and places, where the lead image is reliably a free photo
    and hunting for a specific Commons file name by hand is guesswork. The
    result is pinned into the lock precisely because it is not stable.
    """
    j = _api(WIKIPEDIA_API, {"action": "query", "prop": "pageimages",
                             "piprop": "name", "redirects": 1, "titles": article})
    pages = (j.get("query") or {}).get("pages") or {}
    for p in pages.values():
        if p.get("pageimage"):
            return p["pageimage"].replace("_", " ")
        if "missing" in p:
            raise RuntimeError(f"no en.wikipedia article '{article}'")
    raise RuntimeError(f"'{article}' has no lead image; name a commonsFile instead")


def commons_info(file_title: str, width: int) -> dict:
    """Licence, author, and a rendered thumbnail URL at ``width`` px."""
    j = _api(COMMONS_API, {"action": "query", "prop": "imageinfo",
                           "iiprop": "url|size|mime|extmetadata",
                           "iiurlwidth": width, "titles": "File:" + file_title})
    pages = (j.get("query") or {}).get("pages") or {}
    for p in pages.values():
        if "missing" in p:
            raise RuntimeError(f"File:{file_title} is not on Commons "
                               f"(a local fair-use upload cannot be used here)")
        ii = (p.get("imageinfo") or [None])[0]
        if not ii:
            raise RuntimeError(f"File:{file_title} returned no imageinfo")
        em = ii.get("extmetadata") or {}
        return {
            "file": p["title"].replace("File:", ""),
            "thumbUrl": ii.get("thumburl"),
            "thumbWidth": ii.get("thumbwidth"),
            "thumbHeight": ii.get("thumbheight"),
            "mime": ii.get("mime"),
            "descriptionUrl": ii.get("descriptionurl"),
            "licence": _strip_html((em.get("LicenseShortName") or {}).get("value", "")),
            "licenceUrl": _strip_html((em.get("LicenseUrl") or {}).get("value", "")),
            "artist": _strip_html((em.get("Artist") or {}).get("value", "")),
            "credit": _strip_html((em.get("Credit") or {}).get("value", "")),
        }
    raise RuntimeError(f"File:{file_title}: empty API response")


def licence_is_free(licence: str) -> bool:
    lic = (licence or "").strip().lower()
    return bool(lic) and any(lic.startswith(p) for p in FREE_LICENCE_PREFIXES)


# ---- PNG decode + letterbox ----------------------------------------------
def read_png(path: str) -> np.ndarray:
    """Decode an 8-bit non-interlaced PNG to (H, W, 4) uint8 RGBA.

    Only what MediaWiki's SVG renderer and PNG thumbnailer actually emit is
    supported. Anything else raises rather than returning an approximation --
    a silently mis-decoded logo is a corrupted stimulus, not a cosmetic bug.
    """
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG")
    pos, idat, pal, trns = 8, bytearray(), None, None
    w = h = depth = ctype = interlace = None
    while pos < len(data):
        (ln,) = struct.unpack(">I", data[pos:pos + 4])
        tag = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + ln]
        pos += 12 + ln
        if tag == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
        elif tag == b"PLTE":
            pal = np.frombuffer(body, dtype=np.uint8).reshape(-1, 3)
        elif tag == b"tRNS":
            trns = np.frombuffer(body, dtype=np.uint8)
        elif tag == b"IDAT":
            idat += body
        elif tag == b"IEND":
            break
    if depth != 8 or interlace != 0:
        raise ValueError(f"{path}: only 8-bit non-interlaced PNG is supported "
                         f"(got depth={depth}, interlace={interlace})")
    nch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ctype)
    if nch is None:
        raise ValueError(f"{path}: unsupported PNG colour type {ctype}")

    raw = zlib.decompress(bytes(idat))
    stride = w * nch
    out = np.zeros((h, stride), dtype=np.uint8)
    prev = np.zeros(stride, dtype=np.uint8)
    p = 0
    for y in range(h):
        ft = raw[p]
        line = np.frombuffer(raw[p + 1:p + 1 + stride], dtype=np.uint8).astype(np.int32)
        p += 1 + stride
        cur = np.zeros(stride, dtype=np.int32)
        if ft == 0:
            cur = line
        else:
            # Per-pixel recurrence: filters 1/3/4 reference the pixel `nch`
            # bytes to the left of the one being reconstructed, so this cannot
            # be vectorised across the row.
            pr = prev.astype(np.int32)
            for i in range(stride):
                a = cur[i - nch] if i >= nch else 0
                b = pr[i]
                c = pr[i - nch] if i >= nch else 0
                if ft == 1:
                    v = line[i] + a
                elif ft == 2:
                    v = line[i] + b
                elif ft == 3:
                    v = line[i] + ((a + b) >> 1)
                elif ft == 4:
                    pp = a + b - c
                    pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c)
                    v = line[i] + (a if (pa <= pb and pa <= pc) else (b if pb <= pc else c))
                else:
                    raise ValueError(f"{path}: bad PNG filter type {ft}")
                cur[i] = v & 0xFF
        out[y] = cur.astype(np.uint8)
        prev = out[y]

    px = out.reshape(h, w, nch)
    if ctype == 0:
        rgba = np.dstack([px[:, :, 0]] * 3 + [np.full((h, w), 255, np.uint8)])
    elif ctype == 4:
        rgba = np.dstack([px[:, :, 0]] * 3 + [px[:, :, 1]])
    elif ctype == 2:
        rgba = np.dstack([px, np.full((h, w), 255, np.uint8)])
    elif ctype == 6:
        rgba = px
    else:                                        # palette
        if pal is None:
            raise ValueError(f"{path}: palette PNG with no PLTE chunk")
        idx = px[:, :, 0]
        rgb = pal[idx]
        alpha = (trns[idx] if trns is not None and len(trns) > int(idx.max())
                 else np.full((h, w), 255, np.uint8))
        rgba = np.dstack([rgb, alpha])
    return rgba.astype(np.uint8)


def resize_rgba(rgba: np.ndarray, w: int, h: int) -> np.ndarray:
    """Bilinear resample to exactly (h, w).

    Only ever used to shrink a rendered logo into the letterbox inner box.
    MediaWiki rounds a requested thumbnail width up to one of its standard
    sizes, so "ask for the width you want" does not actually give you that
    width and the fit has to be done here.
    """
    sh, sw = rgba.shape[:2]
    if (sw, sh) == (w, h):
        return rgba
    ys = np.linspace(0, sh - 1, h)
    xs = np.linspace(0, sw - 1, w)
    y0 = np.floor(ys).astype(int); y1 = np.minimum(y0 + 1, sh - 1)
    x0 = np.floor(xs).astype(int); x1 = np.minimum(x0 + 1, sw - 1)
    wy = (ys - y0)[:, None, None]
    wx = (xs - x0)[None, :, None]
    src = rgba.astype(float)
    top = src[y0][:, x0] * (1 - wx) + src[y0][:, x1] * wx
    bot = src[y1][:, x0] * (1 - wx) + src[y1][:, x1] * wx
    return np.clip(top * (1 - wy) + bot * wy, 0, 255).astype(np.uint8)


def letterbox(rgba: np.ndarray, cw: int, ch: int, inner: float = INNER) -> np.ndarray:
    """Centre an RGBA image on a cw x ch opaque canvas, flattening alpha.

    Logos are wide wordmarks of wildly different aspect ratios; dropped straight
    into a 4:3 tile the browser would scale each one to a different apparent
    size, which is an item saliency difference dressed up as a stimulus.
    Compositing every mark at the same margin on the same canvas removes that,
    so the only thing varying across a bank array is which bank it is.
    """
    h, w = rgba.shape[:2]
    box_w, box_h = int(cw * inner), int(ch * inner)
    scale = min(box_w / w, box_h / h)
    if scale < 1.0:
        w, h = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
        rgba = resize_rgba(rgba, w, h)
    canvas = np.zeros((ch, cw, 3), dtype=np.uint8)
    canvas[:, :] = CANVAS_BG
    x0, y0 = (cw - w) // 2, (ch - h) // 2
    a = rgba[:, :, 3:4].astype(float) / 255.0
    fg = rgba[:, :, :3].astype(float)
    bg = canvas[y0:y0 + h, x0:x0 + w].astype(float)
    canvas[y0:y0 + h, x0:x0 + w] = np.clip(fg * a + bg * (1 - a), 0, 255).astype(np.uint8)
    return canvas


# ---- fetching -------------------------------------------------------------
def sha256_file(path: str) -> str:
    hh = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            hh.update(block)
    return hh.hexdigest()


def fetch_item(set_id: str, spec: dict, width: int, out_dir: str,
               pinned: Optional[dict], relock: bool) -> dict:
    """Resolve, licence-check, download, and install one item. Returns a lock entry."""
    iid = spec["id"]
    fit = spec.get("fit", "cover")

    file_title = None
    if pinned and not relock:
        file_title = pinned.get("commonsFile")
    if not file_title:
        res = spec.get("resolve") or {}
        if res.get("commonsFile"):
            file_title = res["commonsFile"]
        elif res.get("wikipediaLead"):
            file_title = resolve_lead_image(res["wikipediaLead"])
        else:
            raise RuntimeError(f"{iid}: resolve needs commonsFile or wikipediaLead")

    canvas_w, canvas_h = width, int(round(width * 3 / 4))
    req_w = int(canvas_w * INNER) if fit == "contain" else width
    info = commons_info(file_title, req_w)

    if not licence_is_free(info["licence"]):
        raise RuntimeError(
            f"{iid}: File:{info['file']} is licensed '{info['licence'] or 'unknown'}', "
            f"which is not on the free allow-list. Pick a different source rather "
            f"than relaxing the check -- this repo must not redistribute it. "
            f"({info['descriptionUrl']})")

    blob = _get(info["thumbUrl"])
    ext = MIME_EXT.get(info["mime"], "")
    # A thumbnail of an SVG or a PDF is rendered to PNG/JPEG; trust the URL.
    url_ext = os.path.splitext(urllib.parse.urlparse(info["thumbUrl"]).path)[1].lower()
    if url_ext in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
        ext = ".jpg" if url_ext == ".jpeg" else url_ext
    if not ext:
        raise RuntimeError(f"{iid}: cannot tell the image format of {info['thumbUrl']}")

    sub = set_id.lower()
    os.makedirs(os.path.join(out_dir, sub), exist_ok=True)
    # A real asset can arrive with a different extension from the placeholder it
    # replaces (f_obama.png -> f_obama.jpg). Leaving both on disk leaves a
    # placeholder one manifest edit away from being served as a stimulus.
    for stale in os.listdir(os.path.join(out_dir, sub)):
        if os.path.splitext(stale)[0] == iid:
            os.remove(os.path.join(out_dir, sub, stale))
    tmp = os.path.join(out_dir, sub, iid + ".download" + ext)
    with open(tmp, "wb") as fh:
        fh.write(blob)

    if fit == "contain":
        if ext != ".png":
            os.remove(tmp)
            raise RuntimeError(f"{iid}: fit=contain needs a PNG render, got {ext}. "
                               f"Use an SVG or PNG source for logos.")
        mark = read_png(tmp)
        os.remove(tmp)
        # The output canvas always clears the minimum size, so the size check
        # below cannot catch a mark that is simply too small to fill it. A mark
        # rendered at half the scale of its neighbours is an item-saliency
        # difference across a bank array, which is exactly what compositing onto
        # a shared canvas is supposed to remove.
        mh, mw = mark.shape[:2]
        box_w, box_h = canvas_w * INNER, canvas_h * INNER
        if mw < 0.9 * box_w and mh < 0.9 * box_h:
            raise RuntimeError(
                f"{iid}: the mark renders at {mw}x{mh}, too small to fill the "
                f"{int(box_w)}x{int(box_h)} inner box, so it would appear smaller "
                f"than the other marks in its array. Use a vector (SVG) source or "
                f"a larger PNG.")
        img = letterbox(mark, canvas_w, canvas_h)
        rel = f"{sub}/{iid}.png"
        write_png(os.path.join(out_dir, rel.replace("/", os.sep)), img)
    else:
        rel = f"{sub}/{iid}{ext}"
        dst = os.path.join(out_dir, rel.replace("/", os.sep))
        if os.path.exists(dst):
            os.remove(dst)
        os.replace(tmp, dst)

    full = os.path.join(out_dir, rel.replace("/", os.sep))
    size = read_png_size(full)
    if size is None:
        raise RuntimeError(f"{iid}: cannot read the dimensions of {rel}")
    if size[0] < MIN_W or size[1] < MIN_H:
        raise RuntimeError(
            f"{iid}: {size[0]}x{size[1]} is below the {MIN_W}x{MIN_H} minimum -- it "
            f"would be upscaled into the tile and lose the detail recognition "
            f"depends on. Pick a higher-resolution source.")

    return {
        "set": set_id, "file": rel, "fit": fit,
        "commonsFile": info["file"], "descriptionUrl": info["descriptionUrl"],
        "licence": info["licence"], "licenceUrl": info["licenceUrl"],
        "artist": info["artist"], "credit": info["credit"],
        "thumbUrl": info["thumbUrl"],
        "width": size[0], "height": size[1],
        "sha256": sha256_file(full),
        "retrieved": datetime.date.today().isoformat(),
    }


# ---- manifest / attribution -----------------------------------------------
def apply_to_manifest(lock: dict, manifest_path: str) -> int:
    """Mark fetched items as real in the manifest and record their provenance."""
    with open(manifest_path, encoding="utf-8") as fh:
        m = json.load(fh)
    n = 0
    for s in m.get("sets", {}).values():
        for it in s.get("items", []):
            e = lock["items"].get(it["id"])
            if not e or e["set"] != s["id"]:
                continue
            it["file"] = e["file"]
            it["placeholder"] = False
            it["source"] = e["descriptionUrl"]
            it["licence"] = e["licence"]
            it["attribution"] = e["artist"] or e["credit"] or "see source"
            it["retrieved"] = e["retrieved"]
            n += 1
    for s in m.get("sets", {}).values():
        if s["id"] in ("E2", "E3") and not any(i.get("placeholder") for i in s["items"]):
            s["note"] = (f"Real assets installed from Wikimedia Commons by "
                         f"scripts/fetch_stimuli.py; provenance per item, credits in "
                         f"ATTRIBUTION.md.")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=2)
    return n


def write_attribution(lock: dict, path: str) -> None:
    lines = [
        "# Stimulus attribution",
        "",
        "Generated by `scripts/fetch_stimuli.py` from `stimuli.lock.json` — do not",
        "edit by hand; re-run the fetcher instead. CC BY and CC BY-SA require this",
        "credit wherever the stimuli are shown, including a paper's stimulus figure.",
        "",
        "All assets are from Wikimedia Commons under a free licence. Marks shown to",
        "identify the service they denote are used nominatively; the copyright status",
        "recorded here is not a trademark clearance.",
        "",
        "| Item | Commons file | Licence | Credit | Source |",
        "|---|---|---|---|---|",
    ]
    for iid in sorted(lock["items"]):
        e = lock["items"][iid]
        cred = (e["artist"] or e["credit"] or "—").replace("|", "/")[:80]
        lines.append(f"| `{iid}` | {e['commonsFile'].replace('|', '/')} | {e['licence']} "
                     f"| {cred} | <{e['descriptionUrl']}> |")
    lines.append("")
    lines.append(f"_{len(lock['items'])} assets, locked {lock.get('fetchedAt', '?')}._")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# ---- commands -------------------------------------------------------------
def load_json(path: str) -> Optional[dict]:
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def verify(stim_dir: str) -> int:
    """Offline: every locked asset present, unmodified, and big enough."""
    lock = load_json(os.path.join(stim_dir, "stimuli.lock.json"))
    if not lock:
        print("no stimuli.lock.json — nothing has been fetched yet "
              "(run: python scripts/fetch_stimuli.py)")
        return 1
    bad: List[str] = []
    for iid, e in sorted(lock["items"].items()):
        fp = os.path.join(stim_dir, e["file"].replace("/", os.sep))
        if not os.path.exists(fp):
            bad.append(f"{iid}: missing {e['file']}")
            continue
        got = sha256_file(fp)
        if got != e["sha256"]:
            bad.append(f"{iid}: {e['file']} changed since it was locked "
                       f"(sha256 {got[:12]} != {e['sha256'][:12]})")
    for b in bad:
        print("FAIL: " + b)
    if bad:
        print(f"\n{len(bad)} problem(s). Re-fetch with: python scripts/fetch_stimuli.py")
        return 1
    print(f"OK: {len(lock['items'])} locked asset(s) present and unmodified")
    return 0


def fetch(stim_dir: str, only_set: Optional[str], relock: bool) -> int:
    src = load_json(os.path.join(stim_dir, "sources.json"))
    if not src or src.get("schema") != "gazepry.stimuli.sources.v1":
        print(f"FAIL: no gazepry.stimuli.sources.v1 at {stim_dir}/sources.json")
        return 1
    if os.environ.get("GAZEPRY_CONTACT") is None:
        print("NOTE: set GAZEPRY_CONTACT to your email or project URL — Wikimedia's")
        print("      policy requires a contactable User-Agent for automated access.")

    old = load_json(os.path.join(stim_dir, "stimuli.lock.json")) or {"items": {}}
    width = int(src.get("targetWidth", 900))
    items: Dict[str, dict] = {}
    failures: List[str] = []
    planned: List[Tuple[str, dict]] = []
    for sid, sset in src.get("sets", {}).items():
        if only_set and sid != only_set:
            continue
        for spec in sset.get("items", []):
            planned.append((sid, spec))
    if not planned:
        print(f"nothing to fetch{' for ' + only_set if only_set else ''} "
              f"— sources.json declares no items")
        return 1

    for n, (sid, spec) in enumerate(planned, 1):
        iid = spec["id"]
        print(f"  [{n:2d}/{len(planned)}] {sid}/{iid} … ", end="", flush=True)
        try:
            entry = fetch_item(sid, spec, width, stim_dir,
                               old["items"].get(iid), relock)
            items[iid] = entry
            print(f"{entry['width']}x{entry['height']}  {entry['licence']}")
        except (RuntimeError, ValueError, OSError) as e:
            print("FAILED")
            failures.append(f"{sid}/{iid}: {e}")

    # Carry forward anything already locked that this run did not touch, so
    # `--set E2` does not silently unlock E3.
    merged = dict(old.get("items", {}))
    merged.update(items)
    lock = {
        "schema": "gazepry.stimuli.lock.v1",
        "fetchedBy": "scripts/fetch_stimuli.py",
        "fetchedAt": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "targetWidth": width,
        "items": merged,
    }
    if items:
        with open(os.path.join(stim_dir, "stimuli.lock.json"), "w", encoding="utf-8") as fh:
            json.dump(lock, fh, indent=2)
        n = apply_to_manifest(lock, os.path.join(stim_dir, "manifest.json"))
        write_attribution(lock, os.path.join(stim_dir, "ATTRIBUTION.md"))
        print(f"\nlocked {len(items)} asset(s); {n} manifest item(s) marked real")
        print("wrote stimuli.lock.json and ATTRIBUTION.md")

    if failures:
        print(f"\n{len(failures)} item(s) failed:")
        for f in failures:
            print("  FAIL: " + f)
        print("\nThe set stays marked as placeholders while any item is missing, so "
              "the task page will keep refusing to collect it. That is the intended "
              "behaviour — fix the sources rather than working around it.")
        return 1
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="install real E2/E3 stimuli from Wikimedia Commons")
    ap.add_argument("--stimuli", default=STIM_DIR, help="stimulus directory")
    ap.add_argument("--set", dest="only_set", choices=["E2", "E3"],
                    help="fetch only one set")
    ap.add_argument("--relock", action="store_true",
                    help="re-resolve lead images instead of reusing the locked file")
    ap.add_argument("--verify", action="store_true",
                    help="offline: hash-check installed assets against the lock")
    a = ap.parse_args(argv)
    if a.verify:
        return verify(a.stimuli)
    return fetch(a.stimuli, a.only_set, a.relock)


if __name__ == "__main__":
    raise SystemExit(main())
