"""Grade pipeline package: render SVG icons and grade them on visual quality.

Public API is via the module entry points (rasterize, silhouette, weight,
alignment, stroke, squint, pair, reference, contrast, report, config). The CLI
orchestrator lives in scripts/render_and_grade.py.
"""
from __future__ import annotations

__all__ = [
    "rasterize",
    "binarize",
    "silhouette",
    "weight",
    "alignment",
    "stroke",
    "squint",
    "pair",
    "reference",
    "anti_example_similarity",
    "color_only_state",
    "contrast",
    "report",
    "config",
]
