#!/usr/bin/env python3
"""Smoke test for grade.rasterize."""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.rasterize import RasterizeError, render_svg


GOOD_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<circle cx="12" cy="12" r="8" fill="#000"/></svg>'
)

BAD_SVG = "<svg this is not valid svg"

TEXT_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<text x="12" y="12">A</text></svg>'
)


def main() -> int:
    arr = render_svg(GOOD_SVG, 24)
    if arr.shape != (24, 24, 4):
        print(f"[FAIL] expected shape (24,24,4), got {arr.shape}")
        return 1
    if arr.dtype.name != "uint8":
        print(f"[FAIL] expected dtype uint8, got {arr.dtype}")
        return 1
    center = int(arr[12, 12, 3])
    if center < 200:
        print(f"[FAIL] expected center alpha ~255, got {center}")
        return 1
    corner = int(arr[0, 0, 3])
    if corner != 0:
        print(f"[FAIL] expected corner alpha 0, got {corner}")
        return 1

    try:
        render_svg(BAD_SVG, 24)
    except RasterizeError:
        pass
    else:
        print("[FAIL] bad SVG should have raised RasterizeError")
        return 1

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        render_svg(TEXT_SVG, 24)
    text_warnings = [w for w in caught if "text" in str(w.message).lower()]
    if not text_warnings:
        print("[FAIL] expected text warning when rendering SVG with <text>")
        return 1

    print("[OK] grade.rasterize smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
