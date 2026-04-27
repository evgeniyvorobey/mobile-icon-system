#!/usr/bin/env python3
"""Smoke test for grade.stroke."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.stroke import measure_stroke


# Outline rect with uniform stroke (1.75px) - cv should be very low.
GOOD_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<rect x="4" y="4" width="16" height="16" fill="none" stroke="#000" '
    'stroke-width="1.75"/></svg>'
)

# Tapered triangle: width changes a lot from base to tip.
BAD_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<polygon points="2,22 22,22 12,2" fill="#000"/></svg>'
)


def main() -> int:
    good = measure_stroke(GOOD_SVG)
    if good.get("skipped"):
        print(f"[FAIL] good stroke unexpectedly skipped: {good}")
        return 1
    if not good["passed"]:
        print(f"[FAIL] good stroke should pass: {good}")
        return 1
    if good["cv"] is None or good["cv"] > 0.15:
        print(f"[FAIL] good stroke cv too high: {good}")
        return 1

    bad = measure_stroke(BAD_SVG)
    # Triangle is 'filled' visually, but it's also a tapered shape; either skipped
    # because filled OR fails because cv is high. Both are acceptable signals.
    if not bad.get("skipped") and (bad["cv"] is None or bad["cv"] <= 0.15):
        print(f"[FAIL] bad stroke should fail or be detected as filled: {bad}")
        return 1

    # Build a more precise tapered hairline shape that survives the filled-skip:
    TAPER_SVG = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        '<polygon points="2,40 98,49 98,51 2,60" fill="#000"/></svg>'
    )
    tapered = measure_stroke(TAPER_SVG)
    if tapered.get("skipped"):
        # Extra defensive: the test still passes if previous bad signal already fired.
        print("[OK] grade.stroke smoke test passed (tapered case skipped as filled).")
        return 0
    if tapered["cv"] is None or tapered["cv"] <= 0.15:
        print(f"[FAIL] tapered stroke should have high cv: {tapered}")
        return 1

    print("[OK] grade.stroke smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
