#!/usr/bin/env python3
"""Smoke test for grade.alignment."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.alignment import audit_alignment


GOOD_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<path d="M 4 4 L 20 4 L 20 20 L 4 20 Z" fill="#000"/></svg>'
)

BAD_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<path d="M 4.3 4.3 L 19.7 4.3 L 19.7 19.7 L 4.3 19.7 Z" fill="#000"/></svg>'
)


def main() -> int:
    good = audit_alignment(GOOD_SVG)
    g24 = good["off_grid_by_size"][24]
    if g24["off_grid"] != 0:
        print(f"[FAIL] good alignment has off-grid points at 24: {g24}")
        return 1
    if not good["passed"]:
        print(f"[FAIL] good alignment should pass overall: {good}")
        return 1

    bad = audit_alignment(BAD_SVG)
    b24 = bad["off_grid_by_size"][24]
    if b24["off_grid"] < 4:
        print(f"[FAIL] bad alignment expected >=4 off-grid at 24, got {b24}")
        return 1
    if bad["passed"]:
        print(f"[FAIL] bad alignment should fail: {bad}")
        return 1

    print("[OK] grade.alignment smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
