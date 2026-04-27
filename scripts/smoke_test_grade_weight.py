#!/usr/bin/env python3
"""Smoke test for grade.weight (single-icon ratio)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.weight import measure_weight


# Center-aligned 12x12 square inside 24x24 viewBox => ~25% area.
GOOD_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<rect x="6" y="6" width="12" height="12" fill="#000"/></svg>'
)

# A 1x1 square => 1 / 576 ratio ~= 0.0017.
BAD_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<rect x="12" y="12" width="1" height="1" fill="#000"/></svg>'
)


def main() -> int:
    good = measure_weight(GOOD_SVG)
    if not good["passed"]:
        print(f"[FAIL] good weight should pass: {good}")
        return 1
    if not (0.20 <= good["weight_ratio"] <= 0.30):
        print(f"[FAIL] good weight ratio out of expected band: {good['weight_ratio']}")
        return 1

    bad = measure_weight(BAD_SVG)
    if bad["passed"]:
        print(f"[FAIL] bad weight should fail: {bad}")
        return 1
    if bad["weight_ratio"] >= 0.10:
        print(f"[FAIL] bad weight ratio too high: {bad['weight_ratio']}")
        return 1

    print("[OK] grade.weight smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
