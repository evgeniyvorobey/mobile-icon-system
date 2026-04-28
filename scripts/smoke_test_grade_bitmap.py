#!/usr/bin/env python3
"""Smoke test for grade.bitmap."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.bitmap import audit_bitmap


CRISP_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<path d="M 6 6 H 18 V 18 H 6 Z" fill="#000"/></svg>'
)

BLURRY_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<circle cx="12" cy="12" r="7.5" fill="#000"/></svg>'
)

MANY_COLOR_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<rect x="6" y="6" width="2" height="12" fill="#101010"/>'
    '<rect x="8" y="6" width="2" height="12" fill="#303030"/>'
    '<rect x="10" y="6" width="2" height="12" fill="#505050"/>'
    '<rect x="12" y="6" width="2" height="12" fill="#707070"/>'
    '<rect x="14" y="6" width="2" height="12" fill="#909090"/>'
    '<rect x="16" y="6" width="2" height="12" fill="#b0b0b0"/>'
    "</svg>"
)


SMOKE_CONFIG = {
    "sizes": [24],
    "max_ambiguous_alpha_ratio": 0.0,
    "max_ambiguous_alpha_px": 0,
    "max_palette_colors": 4,
    "min_filled_ratio": 0.05,
    "max_filled_ratio": 0.70,
    "min_components": 1,
    "max_components": 4,
    "min_component_px": 1,
}


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        crisp = _write(tmp_path / "crisp.svg", CRISP_SVG)
        blurry = _write(tmp_path / "blurry.svg", BLURRY_SVG)
        many_color = _write(tmp_path / "many-color.svg", MANY_COLOR_SVG)

        crisp_report = audit_bitmap(crisp, SMOKE_CONFIG)
        if not crisp_report["passed"]:
            print(f"[FAIL] crisp pixel-art fixture should pass: {crisp_report}")
            return 1

        blurry_report = audit_bitmap(blurry, SMOKE_CONFIG)
        if blurry_report["passed"]:
            print(f"[FAIL] blurry fixture should fail alpha ambiguity: {blurry_report}")
            return 1
        blurry_24 = blurry_report["results"][24]
        if blurry_24["ambiguous_alpha_px"] <= 0:
            print(f"[FAIL] expected ambiguous alpha pixels for blurry fixture: {blurry_24}")
            return 1

        many_color_report = audit_bitmap(many_color, SMOKE_CONFIG)
        if many_color_report["passed"]:
            print(f"[FAIL] many-color fixture should fail palette limit: {many_color_report}")
            return 1
        many_color_24 = many_color_report["results"][24]
        if many_color_24["palette_color_count"] <= SMOKE_CONFIG["max_palette_colors"]:
            print(f"[FAIL] expected palette overflow for many-color fixture: {many_color_24}")
            return 1

    print("[OK] grade.bitmap smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
