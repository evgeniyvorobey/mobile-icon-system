"""Filled-vs-outlined pair distinction check."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Union

import numpy as np

from .binarize import alpha_mask
from .config import DEFAULTS
from .rasterize import RasterizeError, render_svg


SvgSource = Union[str, Path]


def measure_pair_distinction(
    svg_a: SvgSource,
    svg_b: SvgSource,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Compare two icons (e.g. ``home_filled`` vs ``home_outlined``).

    Returns absolute and relative diff ratios with pass/fail.
    """
    cfg = (config or DEFAULTS)["pair"]
    size = int(cfg["render_size"])
    chan_thresh = int(cfg["channel_diff_threshold"])
    min_diff = float(cfg["min_diff_ratio"])
    min_rel_diff = float(cfg["min_relative_diff"])
    alpha_thresh = int(cfg["alpha_threshold"])

    errors = []
    try:
        a = render_svg(svg_a, size)
    except RasterizeError as exc:
        errors.append(f"render A failed: {exc}")
        a = None
    try:
        b = render_svg(svg_b, size)
    except RasterizeError as exc:
        errors.append(f"render B failed: {exc}")
        b = None
    if a is None or b is None:
        return {
            "diff_ratio": None,
            "relative_diff": None,
            "passed": False,
            "errors": errors,
        }

    diff_per_channel = np.abs(a.astype(np.int32) - b.astype(np.int32)).sum(axis=-1)
    diff = (diff_per_channel > chan_thresh).astype(np.uint8)
    diff_count = int(diff.sum())
    diff_ratio = float(diff_count) / float(size * size)

    union_mask = alpha_mask(a, threshold=alpha_thresh) | alpha_mask(b, threshold=alpha_thresh)
    union_count = int(union_mask.sum())
    relative_diff = float(diff_count) / float(max(union_count, 1))

    passed = (diff_ratio >= min_diff) and (relative_diff >= min_rel_diff)
    return {
        "diff_ratio": diff_ratio,
        "relative_diff": relative_diff,
        "min_diff_ratio": min_diff,
        "min_relative_diff": min_rel_diff,
        "diff_pixels": diff_count,
        "union_pixels": union_count,
        "passed": passed,
        "errors": errors,
    }
