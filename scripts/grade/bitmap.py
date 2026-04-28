#!/usr/bin/env python3
"""Pixel-art bitmap checks for SVG icons.

The checker rasterizes SVG input through ``grade.rasterize`` and then applies
small, deterministic sanity checks that matter for pixel-art style icons:
crisp alpha edges, limited color palette, sensible fill coverage, and simple
connected-component structure.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import numpy as np

try:  # Package import when used as ``grade.bitmap``.
    from .rasterize import RasterizeError, render_svg
except ImportError:  # Direct script execution: ``python scripts/grade/bitmap.py``.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from grade.rasterize import RasterizeError, render_svg


SvgSource = Union[str, Path]


DEFAULT_BITMAP_CONFIG: Dict[str, Any] = {
    "sizes": [16, 20, 24],
    "alpha_threshold": 128,
    "alpha_visible_threshold": 0,
    "palette_alpha_threshold": 128,
    "max_ambiguous_alpha_ratio": 0.01,
    "max_ambiguous_alpha_px": None,
    "max_palette_colors": 8,
    "min_filled_ratio": 0.03,
    "max_filled_ratio": 0.70,
    "min_components": 1,
    "max_components": 8,
    "min_component_px": 1,
}


def _merged_config(config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    merged = dict(DEFAULT_BITMAP_CONFIG)
    if config:
        merged.update(config)
    merged["sizes"] = [int(size) for size in merged["sizes"]]
    return merged


def _component_sizes(mask: np.ndarray) -> List[int]:
    """Return connected-component sizes using 8-connectivity."""
    if mask.ndim != 2:
        raise ValueError(f"Expected 2D mask, got shape {mask.shape}")

    height, width = mask.shape
    seen = np.zeros(mask.shape, dtype=bool)
    sizes: List[int] = []
    neighbors: Tuple[Tuple[int, int], ...] = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )

    for start_y, start_x in np.argwhere(mask):
        y0 = int(start_y)
        x0 = int(start_x)
        if seen[y0, x0]:
            continue

        stack = [(y0, x0)]
        seen[y0, x0] = True
        size = 0
        while stack:
            y, x = stack.pop()
            size += 1
            for dy, dx in neighbors:
                ny = y + dy
                nx = x + dx
                if (
                    0 <= ny < height
                    and 0 <= nx < width
                    and mask[ny, nx]
                    and not seen[ny, nx]
                ):
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        sizes.append(size)

    return sizes


def _palette_color_count(
    rgba: np.ndarray,
    *,
    alpha_threshold: int,
) -> int:
    alpha = rgba[..., 3]
    visible = alpha >= alpha_threshold
    if not bool(visible.any()):
        return 0
    rgb = rgba[..., :3][visible]
    return int(np.unique(rgb.reshape(-1, 3), axis=0).shape[0])


def _analyze_raster(rgba: np.ndarray, config: Dict[str, Any]) -> Dict[str, Any]:
    if rgba.ndim != 3 or rgba.shape[-1] != 4:
        raise ValueError(f"Expected RGBA array, got shape {rgba.shape}")

    alpha = rgba[..., 3]
    total_px = int(alpha.size)
    visible_alpha = int(config["alpha_visible_threshold"])
    alpha_threshold = int(config["alpha_threshold"])
    min_component_px = int(config["min_component_px"])

    visible_mask = alpha > visible_alpha
    ambiguous_mask = (alpha > visible_alpha) & (alpha < 255)
    filled_mask = alpha >= alpha_threshold

    visible_px = int(visible_mask.sum())
    ambiguous_px = int(ambiguous_mask.sum())
    filled_px = int(filled_mask.sum())
    denominator = max(visible_px, 1)

    component_sizes = [
        int(size) for size in _component_sizes(filled_mask) if int(size) >= min_component_px
    ]
    return {
        "render_size": int(rgba.shape[0]),
        "visible_px": visible_px,
        "filled_px": filled_px,
        "filled_ratio": float(filled_px) / float(total_px),
        "ambiguous_alpha_px": ambiguous_px,
        "ambiguous_alpha_ratio": float(ambiguous_px) / float(denominator),
        "palette_color_count": _palette_color_count(
            rgba,
            alpha_threshold=int(config["palette_alpha_threshold"]),
        ),
        "component_count": len(component_sizes),
        "component_sizes": sorted(component_sizes, reverse=True),
    }


def _size_failures(metrics: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    max_ambiguous_ratio = float(config["max_ambiguous_alpha_ratio"])
    if metrics["ambiguous_alpha_ratio"] > max_ambiguous_ratio:
        failures.append(
            "ambiguous alpha ratio "
            f"{metrics['ambiguous_alpha_ratio']:.4f} > {max_ambiguous_ratio:.4f}"
        )

    max_ambiguous_px = config.get("max_ambiguous_alpha_px")
    if max_ambiguous_px is not None and metrics["ambiguous_alpha_px"] > int(max_ambiguous_px):
        failures.append(
            f"ambiguous alpha pixels {metrics['ambiguous_alpha_px']} > {int(max_ambiguous_px)}"
        )

    max_palette_colors = int(config["max_palette_colors"])
    if metrics["palette_color_count"] > max_palette_colors:
        failures.append(
            f"palette colors {metrics['palette_color_count']} > {max_palette_colors}"
        )

    min_filled_ratio = float(config["min_filled_ratio"])
    max_filled_ratio = float(config["max_filled_ratio"])
    if metrics["filled_ratio"] < min_filled_ratio:
        failures.append(
            f"filled ratio {metrics['filled_ratio']:.4f} < {min_filled_ratio:.4f}"
        )
    if metrics["filled_ratio"] > max_filled_ratio:
        failures.append(
            f"filled ratio {metrics['filled_ratio']:.4f} > {max_filled_ratio:.4f}"
        )

    min_components = int(config["min_components"])
    max_components = int(config["max_components"])
    if metrics["component_count"] < min_components:
        failures.append(f"components {metrics['component_count']} < {min_components}")
    if metrics["component_count"] > max_components:
        failures.append(f"components {metrics['component_count']} > {max_components}")

    return failures


def audit_bitmap(
    svg_source: SvgSource,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Audit SVG raster output for pixel-art suitability.

    Parameters
    ----------
    svg_source:
        SVG path or raw SVG markup accepted by ``grade.rasterize.render_svg``.
    config:
        Optional threshold overrides. See ``DEFAULT_BITMAP_CONFIG`` for keys.

    Returns
    -------
    dict
        JSON-serializable report with per-size metrics, failures, and ``passed``.
    """
    cfg = _merged_config(config)
    per_size: Dict[int, Dict[str, Any]] = {}
    errors: List[str] = []

    for size in cfg["sizes"]:
        try:
            rgba = render_svg(svg_source, size)
            metrics = _analyze_raster(rgba, cfg)
            failures = _size_failures(metrics, cfg)
            per_size[int(size)] = {
                **metrics,
                "failures": failures,
                "passed": len(failures) == 0,
            }
        except (RasterizeError, ValueError) as exc:
            message = f"render/analyze at size={size} failed: {exc}"
            errors.append(message)
            per_size[int(size)] = {
                "render_size": int(size),
                "failures": [message],
                "passed": False,
            }

    failed_sizes = [
        int(size) for size, result in per_size.items() if not bool(result.get("passed"))
    ]
    return {
        "passed": not errors and not failed_sizes,
        "sizes": cfg["sizes"],
        "results": per_size,
        "failed_sizes": failed_sizes,
        "errors": errors,
        "criteria": {
            "max_ambiguous_alpha_ratio": float(cfg["max_ambiguous_alpha_ratio"]),
            "max_ambiguous_alpha_px": cfg.get("max_ambiguous_alpha_px"),
            "max_palette_colors": int(cfg["max_palette_colors"]),
            "min_filled_ratio": float(cfg["min_filled_ratio"]),
            "max_filled_ratio": float(cfg["max_filled_ratio"]),
            "min_components": int(cfg["min_components"]),
            "max_components": int(cfg["max_components"]),
            "alpha_threshold": int(cfg["alpha_threshold"]),
            "palette_alpha_threshold": int(cfg["palette_alpha_threshold"]),
        },
    }


def _parse_sizes(value: str) -> List[int]:
    sizes = [int(part.strip()) for part in value.split(",") if part.strip()]
    if not sizes:
        raise argparse.ArgumentTypeError("at least one size is required")
    if any(size < 1 for size in sizes):
        raise argparse.ArgumentTypeError("sizes must be positive integers")
    return sizes


def _json_default(obj: Any) -> Any:
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    raise TypeError(f"not JSON serializable: {type(obj).__name__}")


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit an SVG for deterministic pixel-art bitmap criteria."
    )
    parser.add_argument("svg", type=Path, help="SVG file to rasterize and audit")
    parser.add_argument(
        "--sizes",
        type=_parse_sizes,
        default=DEFAULT_BITMAP_CONFIG["sizes"],
        help="comma-separated render sizes, default: 16,20,24",
    )
    parser.add_argument("--alpha-threshold", type=int, default=128)
    parser.add_argument("--palette-alpha-threshold", type=int, default=128)
    parser.add_argument("--max-ambiguous-alpha-ratio", type=float, default=0.01)
    parser.add_argument("--max-ambiguous-alpha-px", type=int, default=None)
    parser.add_argument("--max-palette-colors", type=int, default=8)
    parser.add_argument("--min-filled-ratio", type=float, default=0.03)
    parser.add_argument("--max-filled-ratio", type=float, default=0.70)
    parser.add_argument("--min-components", type=int, default=1)
    parser.add_argument("--max-components", type=int, default=8)
    parser.add_argument("--min-component-px", type=int, default=1)
    return parser


def _config_from_args(args: argparse.Namespace) -> Dict[str, Any]:
    return {
        "sizes": args.sizes,
        "alpha_threshold": args.alpha_threshold,
        "palette_alpha_threshold": args.palette_alpha_threshold,
        "max_ambiguous_alpha_ratio": args.max_ambiguous_alpha_ratio,
        "max_ambiguous_alpha_px": args.max_ambiguous_alpha_px,
        "max_palette_colors": args.max_palette_colors,
        "min_filled_ratio": args.min_filled_ratio,
        "max_filled_ratio": args.max_filled_ratio,
        "min_components": args.min_components,
        "max_components": args.max_components,
        "min_component_px": args.min_component_px,
    }


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    report = audit_bitmap(args.svg, _config_from_args(args))
    print(json.dumps(report, indent=2, sort_keys=True, default=_json_default))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
