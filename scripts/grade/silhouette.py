"""Silhouette legibility check: connected-component count must be stable across sizes."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
from scipy import ndimage

from .binarize import alpha_mask
from .config import DEFAULTS
from .rasterize import RasterizeError, render_svg


SvgSource = Union[str, Path]


def _component_count(rgba: np.ndarray, alpha_thresh: int, min_px: int) -> int:
    mask = alpha_mask(rgba, threshold=alpha_thresh)
    if not mask.any():
        return 0
    structure = np.ones((3, 3), dtype=np.uint8)  # 8-connectivity
    labels, num = ndimage.label(mask, structure=structure)
    if num == 0:
        return 0
    sizes = ndimage.sum(mask, labels, index=np.arange(1, num + 1))
    return int((sizes >= min_px).sum())


def measure_legibility(
    svg_source: SvgSource,
    config: Optional[Dict[str, Any]] = None,
    expected: Optional[int] = None,
) -> Dict[str, Any]:
    """Render the SVG at small sizes and verify the silhouette stays intact.

    Returns ``{"sizes": {16: int, 20: int, 24: int}, "expected": int,
    "stable": bool, "regressions": [...], "passed": bool, "errors": [...]}``.
    """
    cfg = (config or DEFAULTS)["silhouette"]
    sizes: List[int] = list(cfg["sizes"])
    counts: Dict[int, Optional[int]] = {}
    errors: List[str] = []

    for size in sizes:
        try:
            arr = render_svg(svg_source, size)
            counts[size] = _component_count(
                arr, cfg["alpha_threshold"], cfg["min_component_px"]
            )
        except RasterizeError as exc:
            counts[size] = None
            errors.append(f"render at size={size} failed: {exc}")

    valid_counts = [c for c in counts.values() if c is not None]
    inferred_expected = max(valid_counts) if valid_counts else 0
    expected_value = expected if expected is not None else inferred_expected

    regressions: List[Dict[str, Any]] = []
    for size, count in counts.items():
        if count is None:
            regressions.append({"size": size, "count": None, "expected": expected_value})
        elif count != expected_value:
            regressions.append(
                {"size": size, "count": int(count), "expected": int(expected_value)}
            )

    stable = len(regressions) == 0 and len(valid_counts) == len(sizes)
    return {
        "sizes": {int(k): (None if v is None else int(v)) for k, v in counts.items()},
        "expected": int(expected_value),
        "stable": stable,
        "regressions": regressions,
        "passed": stable,
        "errors": errors,
    }
