#!/usr/bin/env python3
"""Smoke test for grade.weight set-balance."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.weight import measure_set_balance


def main() -> int:
    # Good: 5 icons all clustered near 0.25.
    good = measure_set_balance(
        [0.24, 0.25, 0.26, 0.255, 0.245],
        ["a", "b", "c", "d", "e"],
    )
    if not good["passed"]:
        print(f"[FAIL] good set balance should pass: {good}")
        return 1
    if any(abs(z) >= 1.5 for z in good["z_scores"]):
        print(f"[FAIL] good z-scores should be < 1.5: {good['z_scores']}")
        return 1

    # Bad: one outlier at 0.05 vs 4 at 0.25 -> outlier flagged with |z| > 2.5
    # AND/OR out of band (band default 35%).
    bad = measure_set_balance(
        [0.25, 0.25, 0.25, 0.25, 0.05],
        ["a", "b", "c", "d", "e"],
    )
    if bad["passed"]:
        print(f"[FAIL] bad set balance should fail: {bad}")
        return 1
    flagged_e = [o for o in bad["outliers"] if o["label"] == "e"]
    if not flagged_e:
        print(f"[FAIL] expected outlier 'e' to be flagged: {bad}")
        return 1

    print("[OK] grade.weight set balance smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
