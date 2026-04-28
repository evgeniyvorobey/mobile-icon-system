#!/usr/bin/env python3
"""Smoke test for grade.color_only_state.

Verifies:
1. A pair that differs ONLY in fill color (same path, different fill) is
   flagged hard_fail with verdict=hard_fail.
2. A real filled-vs-outlined pair (different paths) passes with verdict=ok.
3. An identical pair is N/A (verdict=ok, applicable=False).
"""
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.color_only_state import check_color_only_state  # noqa: E402


# Same shape, different fill colors (the failure mode).
SAME_SHAPE_RED = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<rect x="6" y="6" width="12" height="12" fill="red"/></svg>'
)
SAME_SHAPE_BLACK = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<rect x="6" y="6" width="12" height="12" fill="black"/></svg>'
)
SAME_SHAPE_BLUE = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<rect x="6" y="6" width="12" height="12" fill="blue"/></svg>'
)

# Real filled vs outlined home — different paths, different stroke/fill mode.
HOME_FILLED = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<polygon points="3,12 12,3 21,12 19,12 19,21 5,21 5,12" fill="#000"/></svg>'
)
HOME_OUTLINED = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<polygon points="3,12 12,3 21,12 19,12 19,21 5,21 5,12" '
    'fill="none" stroke="#000" stroke-width="2"/></svg>'
)


def main() -> int:
    # Case 1: pure color-only (red square vs black square) → hard_fail.
    bad = check_color_only_state(SAME_SHAPE_RED, SAME_SHAPE_BLACK)
    if bad.get("verdict") != "hard_fail" or not bad.get("hard_fail"):
        print(f"[FAIL] color-only pair should hard_fail, got {bad}")
        return 1
    if bad.get("color_diff_ratio", 0) < 0.10:
        print(f"[FAIL] expected color_diff >= 0.10, got {bad}")
        return 1
    if bad.get("shape_diff_ratio", 1) >= 0.05:
        print(
            f"[FAIL] expected shape_diff < 0.05 for same-shape pair, got {bad}"
        )
        return 1

    # Case 2: pure color-only (red vs blue) → also hard_fail.
    rb = check_color_only_state(SAME_SHAPE_RED, SAME_SHAPE_BLUE)
    if rb.get("verdict") != "hard_fail":
        print(f"[FAIL] red-vs-blue same shape should hard_fail, got {rb}")
        return 1

    # Case 3: real filled vs outlined → pass.
    good = check_color_only_state(HOME_FILLED, HOME_OUTLINED)
    if good.get("verdict") != "ok" or not good.get("passed"):
        print(f"[FAIL] real filled vs outlined should pass, got {good}")
        return 1
    if good.get("hard_fail"):
        print(f"[FAIL] real filled vs outlined should not hard_fail, got {good}")
        return 1
    if good.get("shape_diff_ratio", 0) < 0.10:
        print(
            f"[FAIL] expected shape_diff >= 0.10 for real pair, got {good}"
        )
        return 1

    # Case 4: identical pair → N/A (existing pair check handles this).
    same = check_color_only_state(SAME_SHAPE_RED, SAME_SHAPE_RED)
    if same.get("verdict") != "ok":
        print(f"[FAIL] identical pair should be ok (N/A), got {same}")
        return 1
    if same.get("applicable", True):
        print(f"[FAIL] identical pair should mark applicable=False, got {same}")
        return 1
    if same.get("hard_fail"):
        print(f"[FAIL] identical pair should not hard_fail, got {same}")
        return 1

    print("[OK] grade.color_only_state smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
