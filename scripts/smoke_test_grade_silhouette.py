#!/usr/bin/env python3
"""Smoke test for grade.silhouette."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.silhouette import measure_legibility


# Three well-separated chunky dots: silhouette stays 3 across sizes.
GOOD_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<circle cx="4" cy="12" r="2" fill="#000"/>'
    '<circle cx="12" cy="12" r="2" fill="#000"/>'
    '<circle cx="20" cy="12" r="2" fill="#000"/>'
    "</svg>"
)

# Three tightly-packed hairline dots that fuse at small sizes.
BAD_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<circle cx="11" cy="12" r="0.6" fill="#000"/>'
    '<circle cx="12" cy="12" r="0.6" fill="#000"/>'
    '<circle cx="13" cy="12" r="0.6" fill="#000"/>'
    "</svg>"
)


def main() -> int:
    good = measure_legibility(GOOD_SVG, expected=3)
    if not good["stable"] or good["expected"] != 3:
        print(f"[FAIL] good silhouette failed stability: {good}")
        return 1
    if good["sizes"][16] != 3 or good["sizes"][20] != 3 or good["sizes"][24] != 3:
        print(f"[FAIL] good silhouette wrong counts: {good['sizes']}")
        return 1

    bad = measure_legibility(BAD_SVG, expected=3)
    if bad["stable"]:
        print(f"[FAIL] bad silhouette unexpectedly stable: {bad}")
        return 1
    if bad["sizes"][16] == 3:
        print(f"[FAIL] bad silhouette did not regress at 16: {bad}")
        return 1

    print("[OK] grade.silhouette smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
