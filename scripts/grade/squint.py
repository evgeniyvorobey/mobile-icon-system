"""Squint test: blur the icon and check that any signal survives."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Union

import numpy as np
from scipy import ndimage

from .binarize import composite_over_white, luminance
from .config import DEFAULTS
from .rasterize import RasterizeError, render_svg


SvgSource = Union[str, Path]


def measure_squint(
    svg_source: SvgSource,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Render at 24, blur, threshold; PASS if at least 5% of pixels remain dark."""
    cfg = (config or DEFAULTS)["squint"]
    size = int(cfg["render_size"])
    sigma = float(cfg["blur_radius"])
    lum_thresh = float(cfg["luminance_threshold"])
    min_signal = float(cfg["min_signal_ratio"])

    try:
        arr = render_svg(svg_source, size)
    except RasterizeError as exc:
        return {
            "signal_ratio": None,
            "passed": False,
            "errors": [str(exc)],
        }

    rgb = composite_over_white(arr)
    lum = luminance(rgb)
    blurred = ndimage.gaussian_filter(lum, sigma=sigma, mode="nearest")
    dark = blurred < lum_thresh
    signal_ratio = float(dark.sum()) / float(size * size)
    passed = signal_ratio >= min_signal
    return {
        "signal_ratio": signal_ratio,
        "min_signal_ratio": min_signal,
        "blur_radius": sigma,
        "luminance_threshold": lum_thresh,
        "passed": passed,
        "errors": [],
    }
