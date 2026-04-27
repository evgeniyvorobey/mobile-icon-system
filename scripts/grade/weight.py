"""Visual weight checks: per-icon ratio and set-level balance via MAD-based Z-score."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

import numpy as np

from .binarize import alpha_mask
from .config import DEFAULTS
from .rasterize import RasterizeError, render_svg


SvgSource = Union[str, Path]


def measure_weight(
    svg_source: SvgSource,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Return per-icon weight ratio and pass/fail vs. min/max bounds."""
    cfg = (config or DEFAULTS)["weight"]
    size = int(cfg["render_size"])
    try:
        arr = render_svg(svg_source, size)
    except RasterizeError as exc:
        return {
            "weight_px": None,
            "weight_ratio": None,
            "passed": False,
            "errors": [str(exc)],
        }

    mask = alpha_mask(arr, threshold=cfg["alpha_threshold"])
    weight_px = int(mask.sum())
    weight_ratio = float(weight_px) / float(size * size)
    passed = cfg["min_ratio"] <= weight_ratio <= cfg["max_ratio"]
    return {
        "weight_px": weight_px,
        "weight_ratio": weight_ratio,
        "passed": passed,
        "min_ratio": float(cfg["min_ratio"]),
        "max_ratio": float(cfg["max_ratio"]),
        "errors": [],
    }


def _median_abs_dev(values: np.ndarray) -> float:
    median = float(np.median(values))
    deviations = np.abs(values - median)
    return float(np.median(deviations))


def measure_set_balance(
    ratios: Sequence[float],
    labels: Optional[Sequence[str]] = None,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Cross-icon balance check using MAD-based Z-scores plus a relative-band guard.

    PASS: every |z| <= set_z_max AND every ratio within ±set_band of the median.
    Warns when the sample size is too small for MAD to be stable.
    """
    cfg = (config or DEFAULTS)["weight"]
    arr = np.asarray(list(ratios), dtype=np.float64)
    n = arr.size
    labels = list(labels) if labels is not None else [f"icon_{i}" for i in range(n)]

    warnings_list: List[str] = []
    if n == 0:
        return {
            "n": 0,
            "median": None,
            "mad": None,
            "z_scores": [],
            "outliers": [],
            "passed": False,
            "warnings": ["empty input"],
        }
    if n < int(cfg["min_set_size_for_mad"]):
        warnings_list.append(
            f"set size n={n} < {cfg['min_set_size_for_mad']}; MAD-based outlier "
            "detection is unstable"
        )

    median = float(np.median(arr))
    mad = _median_abs_dev(arr)
    scale = 1.4826 * mad if mad > 0 else 0.0

    z_scores: List[float] = []
    outliers: List[Dict[str, Any]] = []
    band = float(cfg["set_band"])
    z_max = float(cfg["set_z_max"])
    band_floor = median * (1.0 - band)
    band_ceil = median * (1.0 + band)

    for label, ratio in zip(labels, arr):
        z = (ratio - median) / scale if scale > 0 else 0.0
        z_scores.append(float(z))
        out_of_band = (ratio < band_floor) or (ratio > band_ceil)
        if abs(z) > z_max or out_of_band:
            outliers.append(
                {
                    "label": label,
                    "ratio": float(ratio),
                    "z": float(z),
                    "out_of_band": bool(out_of_band),
                }
            )
    passed = len(outliers) == 0
    return {
        "n": n,
        "median": median,
        "mad": float(mad),
        "scale": float(scale),
        "z_scores": z_scores,
        "labels": labels,
        "ratios": arr.tolist(),
        "outliers": outliers,
        "band": band,
        "z_max": z_max,
        "passed": passed,
        "warnings": warnings_list,
    }


def stratify_pairs(filenames: Sequence[str]) -> Dict[str, List[int]]:
    """Group indices by ``_filled`` / ``_outlined`` suffix; ``_other`` for the rest."""
    groups: Dict[str, List[int]] = {"filled": [], "outlined": [], "other": []}
    for idx, name in enumerate(filenames):
        stem = Path(name).stem.lower()
        if stem.endswith("_filled") or stem.endswith("-filled"):
            groups["filled"].append(idx)
        elif stem.endswith("_outlined") or stem.endswith("-outlined"):
            groups["outlined"].append(idx)
        else:
            groups["other"].append(idx)
    return groups
