"""Color-only state distinction check.

Detects when a state pair (e.g. selected vs unselected, filled vs outlined)
differs ONLY in color/tint and not in shape. Such pairs fail accessibility:
they collapse under Forced Colors mode (Windows High Contrast) and under
deuteranopia simulation, leaving assistive-technology users with no way to
tell the states apart.

Algorithm
---------
1. Render both icons at the configured size (default 24×24 RGBA).
2. Compute a color-aware diff ratio: per-pixel sum of |ΔR|+|ΔG|+|ΔB|+|ΔA|;
   pixels above ``channel_diff_threshold`` count as different.
3. Compute a color-blind shape diff ratio: composite each render over white,
   convert to greyscale via ``PIL.Image.convert("L")`` (proper Rec. 601
   luminance), threshold at 50%, XOR the binary masks.
4. Hard-fail when ``color_diff_ratio >= min_color_diff`` AND
   ``shape_diff_ratio < max_shape_diff_for_color_only``.
5. Pass when ``shape_diff_ratio >= min_shape_diff``.
6. Otherwise N/A — fall through to existing pair-distinction check.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
from PIL import Image

from .binarize import composite_over_white
from .config import DEFAULTS
from .rasterize import RasterizeError, render_svg


SvgSource = Union[str, Path]


def _color_diff_ratio(a: np.ndarray, b: np.ndarray, chan_thresh: int) -> float:
    diff_per_channel = np.abs(a.astype(np.int32) - b.astype(np.int32)).sum(axis=-1)
    diff = (diff_per_channel > chan_thresh).astype(np.uint8)
    return float(diff.sum()) / float(a.shape[0] * a.shape[1])


def _shape_diff_ratio(a: np.ndarray, b: np.ndarray, lum_threshold: int) -> float:
    """Color-blind shape diff via PIL ``convert('L')`` luminance + 50% binarization."""
    img_a = Image.fromarray(composite_over_white(a)).convert("L")
    img_b = Image.fromarray(composite_over_white(b)).convert("L")
    bin_a = (np.asarray(img_a, dtype=np.uint8) < lum_threshold).astype(np.uint8)
    bin_b = (np.asarray(img_b, dtype=np.uint8) < lum_threshold).astype(np.uint8)
    diff = (bin_a != bin_b).astype(np.uint8)
    return float(diff.sum()) / float(bin_a.shape[0] * bin_a.shape[1])


def check_color_only_state(
    svg_a: SvgSource,
    svg_b: SvgSource,
    *,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Check whether two state-pair SVGs differ ONLY in color (not in shape).

    Parameters
    ----------
    svg_a, svg_b:
        The two state SVGs (e.g. ``home_filled`` and ``home_outlined``, or
        ``notification_unread`` and ``notification_read``).
    config:
        Optional config dict. Reads ``config["color_only_state"]`` for thresholds:
            - ``render_size`` (default 24)
            - ``channel_diff_threshold`` (default 16)
            - ``min_color_diff`` (default 0.10) — below this, the pair is
              effectively identical and this check is N/A
            - ``max_shape_diff_for_color_only`` (default 0.05) — below this,
              the shapes are the same and ``color_only`` is the diagnosis
            - ``min_shape_diff`` (default 0.10) — at or above this, the
              shapes meaningfully differ and the pair passes
            - ``luminance_threshold`` (default 128) — 50% binarization level

    Returns
    -------
    dict with ``passed``, ``verdict``, ``color_diff_ratio``, ``shape_diff_ratio``,
    plus diagnostic fields. ``hard_fail`` flag included for the report
    aggregator.
    """
    cfg_all = config or DEFAULTS
    cfg = cfg_all.get("color_only_state") or DEFAULTS["color_only_state"]
    size = int(cfg.get("render_size", 24))
    chan_thresh = int(cfg.get("channel_diff_threshold", 16))
    min_color = float(cfg.get("min_color_diff", 0.10))
    max_shape_for_color_only = float(cfg.get("max_shape_diff_for_color_only", 0.05))
    min_shape = float(cfg.get("min_shape_diff", 0.10))
    lum_thresh = int(cfg.get("luminance_threshold", 128))

    errors: List[str] = []
    warnings: List[str] = []

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
            "passed": False,
            "verdict": "hard_fail",
            "color_diff_ratio": None,
            "shape_diff_ratio": None,
            "hard_fail": True,
            "errors": errors,
            "warnings": warnings,
        }

    color_diff = _color_diff_ratio(a, b, chan_thresh)
    shape_diff = _shape_diff_ratio(a, b, lum_thresh)

    diagnostics: Dict[str, Any] = {
        "color_diff_ratio": color_diff,
        "shape_diff_ratio": shape_diff,
        "min_color_diff": min_color,
        "max_shape_diff_for_color_only": max_shape_for_color_only,
        "min_shape_diff": min_shape,
        "luminance_threshold": lum_thresh,
        "render_size": size,
        "errors": errors,
    }

    if color_diff < min_color:
        # Pair is effectively identical; existing pair-distinction check
        # handles this — color-only-state is not applicable.
        return {
            **diagnostics,
            "verdict": "ok",
            "passed": True,
            "hard_fail": False,
            "applicable": False,
            "reason": (
                f"color_diff_ratio {color_diff:.3f} < {min_color:.2f}; "
                "pair is effectively identical, color-only check N/A"
            ),
            "warnings": warnings,
        }

    if shape_diff < max_shape_for_color_only:
        # Strong color difference but the shapes are essentially the same →
        # the difference IS color-only. Hard-fail.
        warnings.append(
            f"color_only_state: pair differs by color only "
            f"(color_diff={color_diff:.3f}, shape_diff={shape_diff:.3f}); "
            "fails Forced Colors mode and deuteranopia"
        )
        return {
            **diagnostics,
            "verdict": "hard_fail",
            "passed": False,
            "hard_fail": True,
            "applicable": True,
            "reason": (
                f"shape_diff_ratio {shape_diff:.3f} < "
                f"{max_shape_for_color_only:.2f} while color_diff_ratio "
                f"{color_diff:.3f} >= {min_color:.2f}: difference is color only"
            ),
            "warnings": warnings,
        }

    if shape_diff >= min_shape:
        # Genuine shape difference present.
        return {
            **diagnostics,
            "verdict": "ok",
            "passed": True,
            "hard_fail": False,
            "applicable": True,
            "reason": (
                f"shape_diff_ratio {shape_diff:.3f} >= {min_shape:.2f}: "
                "real shape difference present"
            ),
            "warnings": warnings,
        }

    # Borderline: there's some shape change but not enough to clearly pass.
    # We do NOT hard-fail on borderline — that would create false positives
    # on real outlined pairs near the threshold. Surface as a warning and
    # let the existing pair distinction check make the call.
    warnings.append(
        f"color_only_state: borderline shape difference "
        f"(shape_diff={shape_diff:.3f} between {max_shape_for_color_only:.2f} "
        f"and {min_shape:.2f}); review manually"
    )
    return {
        **diagnostics,
        "verdict": "warn",
        "passed": True,
        "hard_fail": False,
        "applicable": True,
        "reason": (
            f"shape_diff_ratio {shape_diff:.3f} between "
            f"{max_shape_for_color_only:.2f} and {min_shape:.2f}: borderline"
        ),
        "warnings": warnings,
    }
