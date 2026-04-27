"""Stroke-width uniformity via distance-transform medial axis approximation."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Union

import numpy as np
from scipy import ndimage

from .binarize import alpha_mask
from .config import DEFAULTS
from .rasterize import RasterizeError, render_svg


SvgSource = Union[str, Path]


def _local_maxima(dist: np.ndarray) -> np.ndarray:
    """Boolean mask of pixels that equal the local 3x3 maximum of `dist` and are > 0."""
    # Use grey_dilation as a 3x3 max filter; ties (plateaus) are kept.
    dilated = ndimage.grey_dilation(dist, size=(3, 3))
    return (dist > 0) & (dist == dilated)


def measure_stroke(
    svg_source: SvgSource,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Estimate stroke-width coefficient of variation; skip cleanly when not applicable."""
    cfg = (config or DEFAULTS)["stroke"]
    size = int(cfg["render_size"])
    cv_max = float(cfg["cv_max"])
    filled_skip = float(cfg["filled_skip_ratio"])
    min_samples = int(cfg["min_samples"])

    try:
        arr = render_svg(svg_source, size)
    except RasterizeError as exc:
        return {
            "cv": None,
            "passed": False,
            "skipped": False,
            "reason": str(exc),
            "errors": [str(exc)],
        }

    mask = alpha_mask(arr, threshold=128)
    fill_ratio = float(mask.sum()) / float(size * size)
    if fill_ratio > filled_skip:
        return {
            "cv": None,
            "passed": True,
            "skipped": True,
            "reason": f"icon appears filled (mask ratio {fill_ratio:.2f} > {filled_skip})",
            "fill_ratio": fill_ratio,
            "n_samples": 0,
            "errors": [],
        }

    dist = ndimage.distance_transform_edt(mask).astype(np.float32)
    medial = _local_maxima(dist)
    widths = (2.0 * dist[medial]).astype(np.float64)
    n = int(widths.size)
    if n < min_samples:
        return {
            "cv": None,
            "passed": True,
            "skipped": True,
            "reason": f"insufficient samples (n={n} < {min_samples})",
            "fill_ratio": fill_ratio,
            "n_samples": n,
            "errors": [],
        }

    mean = float(widths.mean())
    std = float(widths.std())
    cv = (std / mean) if mean > 0 else float("inf")
    passed = cv <= cv_max
    return {
        "cv": float(cv),
        "mean_px": mean,
        "std_px": std,
        "n_samples": n,
        "fill_ratio": fill_ratio,
        "cv_max": cv_max,
        "skipped": False,
        "passed": passed,
        "errors": [],
    }
