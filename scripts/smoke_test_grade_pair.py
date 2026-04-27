#!/usr/bin/env python3
"""Smoke test for grade.pair filled/outlined distinction."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.pair import measure_pair_distinction


HOME_FILLED = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<polygon points="3,12 12,3 21,12 19,12 19,21 5,21 5,12" fill="#000"/></svg>'
)
HOME_OUTLINED = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<polygon points="3,12 12,3 21,12 19,12 19,21 5,21 5,12" '
    'fill="none" stroke="#000" stroke-width="1.75"/></svg>'
)


def main() -> int:
    good = measure_pair_distinction(HOME_FILLED, HOME_OUTLINED)
    if not good["passed"]:
        print(f"[FAIL] good pair should pass: {good}")
        return 1
    if good["relative_diff"] < 0.30:
        print(f"[FAIL] good pair relative_diff too low: {good}")
        return 1

    bad = measure_pair_distinction(HOME_FILLED, HOME_FILLED)
    if bad["passed"]:
        print(f"[FAIL] identical pair should fail: {bad}")
        return 1
    if bad["diff_ratio"] >= 0.05:
        print(f"[FAIL] identical pair diff_ratio too high: {bad}")
        return 1

    print("[OK] grade.pair smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
