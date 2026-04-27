#!/usr/bin/env python3
"""Smoke test for grade.squint."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.squint import measure_squint


# Chunky filled square: plenty of dark pixels survive a 2px blur.
GOOD_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<rect x="4" y="4" width="16" height="16" fill="#000"/></svg>'
)

# 0.5px hairline that will essentially disappear under a 2px Gaussian.
BAD_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<line x1="2" y1="12" x2="22" y2="12" stroke="#000" stroke-width="0.5"/></svg>'
)


def main() -> int:
    good = measure_squint(GOOD_SVG)
    if not good["passed"]:
        print(f"[FAIL] good squint should pass: {good}")
        return 1
    if good["signal_ratio"] < 0.20:
        print(f"[FAIL] good squint signal too weak: {good}")
        return 1

    bad = measure_squint(BAD_SVG)
    if bad["passed"]:
        print(f"[FAIL] bad squint should fail: {bad}")
        return 1
    if bad["signal_ratio"] >= 0.05:
        print(f"[FAIL] bad squint signal too strong: {bad}")
        return 1

    print("[OK] grade.squint smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
