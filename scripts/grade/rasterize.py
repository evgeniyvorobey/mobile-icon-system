"""SVG rasterizer wrapping resvg_py.

Public API:
    render_svg(svg_source, size) -> np.ndarray (H, W, 4) uint8 RGBA
"""
from __future__ import annotations

import io
import re
import warnings
from pathlib import Path
from typing import Tuple, Union

import numpy as np
from PIL import Image

import resvg_py


SvgSource = Union[str, Path]


class RasterizeError(RuntimeError):
    """Raised when an SVG cannot be parsed or rendered."""


_TEXT_RE = re.compile(r"<text[\s>]", re.IGNORECASE)


def _resolve_source(svg_source: SvgSource) -> Tuple[str, str]:
    """Return (svg_string, label) where label is for diagnostics."""
    if isinstance(svg_source, Path):
        path = svg_source
        if not path.exists():
            raise RasterizeError(f"SVG path does not exist: {path}")
        return path.read_text(encoding="utf-8"), str(path)
    if isinstance(svg_source, str):
        # Heuristic: if it parses as a path AND that path exists, treat as a file.
        try:
            candidate = Path(svg_source)
        except (OSError, ValueError):
            candidate = None
        if candidate is not None and len(svg_source) < 4096:
            try:
                if candidate.exists() and candidate.is_file():
                    return candidate.read_text(encoding="utf-8"), str(candidate)
            except OSError:
                pass
        return svg_source, "<inline svg>"
    raise RasterizeError(f"Unsupported svg_source type: {type(svg_source)!r}")


def _warn_on_text(svg_str: str, label: str) -> None:
    if _TEXT_RE.search(svg_str):
        warnings.warn(
            f"SVG contains <text> elements ({label}); icon text rendering "
            "depends on font availability and is discouraged.",
            stacklevel=3,
        )


def render_svg(svg_source: SvgSource, size: int) -> np.ndarray:
    """Render an SVG to an RGBA numpy array of shape (size, size, 4) uint8.

    Parameters
    ----------
    svg_source:
        Either a filesystem path (str/Path) to an SVG or the raw SVG markup.
    size:
        Output edge length in pixels (square output).

    Raises
    ------
    RasterizeError
        On parse or render failure.
    """
    if size < 1:
        raise RasterizeError(f"size must be >= 1, got {size}")

    svg_str, label = _resolve_source(svg_source)
    _warn_on_text(svg_str, label)

    try:
        png_bytes = resvg_py.svg_to_bytes(
            svg_string=svg_str,
            width=size,
            height=size,
        )
    except Exception as exc:  # noqa: BLE001 - re-wrap any backend error
        raise RasterizeError(
            f"resvg_py failed to render {label} at size={size}: {exc}"
        ) from exc

    try:
        with Image.open(io.BytesIO(bytes(png_bytes))) as img:
            rgba = img.convert("RGBA")
            arr = np.asarray(rgba, dtype=np.uint8)
    except Exception as exc:  # noqa: BLE001
        raise RasterizeError(
            f"Failed to decode rendered PNG for {label}: {exc}"
        ) from exc

    if arr.shape != (size, size, 4):
        raise RasterizeError(
            f"Unexpected raster shape {arr.shape} for {label} "
            f"(expected ({size}, {size}, 4))"
        )
    return arr
