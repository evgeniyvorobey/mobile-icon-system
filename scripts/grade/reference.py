"""Perceptual-hash comparison against a reference corpus.

If ``imagehash`` is missing, every public function raises
``ReferenceUnavailable`` so callers can degrade gracefully.
"""
from __future__ import annotations

import io
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

from PIL import Image

from .config import DEFAULTS
from .rasterize import RasterizeError, render_svg


SvgSource = Union[str, Path]


class ReferenceUnavailable(RuntimeError):
    """Raised when imagehash is not installed."""


try:
    import imagehash  # type: ignore[import-not-found]
    _IMAGEHASH_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised when dep absent
    imagehash = None  # type: ignore[assignment]
    _IMAGEHASH_AVAILABLE = False


def is_available() -> bool:
    return _IMAGEHASH_AVAILABLE


def _hash_svg(svg_source: SvgSource, size: int, hash_size: int):
    if not _IMAGEHASH_AVAILABLE:
        raise ReferenceUnavailable("install imagehash to use reference comparison")
    arr = render_svg(svg_source, size)
    # Pillow deprecates the `mode` kwarg on fromarray; let it infer from shape.
    img = Image.fromarray(arr).convert("RGB")
    return imagehash.phash(img, hash_size=hash_size)


def hash_icon(svg_source: SvgSource, config: Optional[Dict[str, Any]] = None):
    """Return a phash of the rendered icon (raises if imagehash missing)."""
    cfg = (config or DEFAULTS)["reference"]
    return _hash_svg(svg_source, int(cfg["render_size"]), int(cfg["hash_size"]))


def compare_to_reference(
    candidate: SvgSource,
    references: Sequence[SvgSource],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Compute the minimum phash distance between ``candidate`` and ``references``.

    Returns dict with distance, verdict, and best-match index.
    """
    if not _IMAGEHASH_AVAILABLE:
        raise ReferenceUnavailable("install imagehash to use reference comparison")
    cfg = (config or DEFAULTS)["reference"]
    plagiarism_max = int(cfg["plagiarism_max"])
    off_vocab_min = int(cfg["off_vocab_min"])

    cand_hash = _hash_svg(candidate, int(cfg["render_size"]), int(cfg["hash_size"]))
    distances: List[int] = []
    errors: List[str] = []
    for ref in references:
        try:
            ref_hash = _hash_svg(ref, int(cfg["render_size"]), int(cfg["hash_size"]))
        except RasterizeError as exc:
            errors.append(f"ref render failed for {ref}: {exc}")
            distances.append(10**9)
            continue
        distances.append(int(cand_hash - ref_hash))
    if not distances:
        return {
            "distance": None,
            "verdict": "no_references",
            "best_index": None,
            "passed": True,
            "warnings": ["no references provided"],
            "errors": errors,
        }
    best = min(distances)
    best_idx = distances.index(best)
    if best < plagiarism_max:
        verdict = "plagiarism"
        passed = False
    elif best > off_vocab_min:
        verdict = "off-vocabulary"
        passed = False
    else:
        verdict = "on-vocabulary"
        passed = True
    return {
        "distance": int(best),
        "verdict": verdict,
        "best_index": best_idx,
        "all_distances": distances,
        "passed": passed,
        "warnings": [],
        "errors": errors,
    }
