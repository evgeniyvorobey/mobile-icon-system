#!/usr/bin/env python3
"""Smoke test for grade.anti_example_similarity.

Verifies:
1. user-gendered.svg flagged as hard_fail when the corpus is the tier-c dir
   (it should match itself with distance 0).
2. A clean Lucide-style user.svg passes (no near-clone of any anti-example).
3. The closest match for the gendered candidate is user-gendered.svg with
   the correct failure-mode label parsed from the .notes.md.
"""
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.anti_example_similarity import (  # noqa: E402
    ReferenceUnavailable,
    check_anti_example_similarity,
)
from grade.reference import is_available  # noqa: E402


CORPUS = ROOT / "assets" / "references" / "tier-c"
GENDERED = CORPUS / "user-gendered.svg"
CLEAN_USER = ROOT / "assets" / "references" / "tier-a" / "user.svg"


def main() -> int:
    if not is_available():
        print("[SKIP] imagehash not installed")
        return 0
    if not CORPUS.is_dir():
        print(f"[FAIL] tier-c corpus missing at {CORPUS}")
        return 1
    if not GENDERED.exists():
        print(f"[FAIL] anti-example missing: {GENDERED}")
        return 1
    if not CLEAN_USER.exists():
        print(f"[FAIL] tier-a user.svg missing: {CLEAN_USER}")
        return 1

    # Case 1: gendered candidate against the tier-c corpus → hard_fail.
    bad = check_anti_example_similarity(GENDERED, corpus_root=CORPUS)
    if bad.get("verdict") != "hard_fail":
        print(f"[FAIL] gendered should hard_fail, got {bad}")
        return 1
    if bad.get("passed"):
        print(f"[FAIL] gendered should not pass, got {bad}")
        return 1

    closest = bad.get("closest") or {}
    if closest.get("anti_example") != "user-gendered.svg":
        print(
            "[FAIL] expected closest match to be user-gendered.svg, got "
            f"{closest}"
        )
        return 1
    if closest.get("phash_distance") != 0:
        print(
            f"[FAIL] expected exact match distance 0, got {closest}"
        )
        return 1
    fmode = (closest.get("failure_mode") or "").lower()
    if "gender" not in fmode:
        print(
            f"[FAIL] expected failure mode to mention 'gender', got {closest}"
        )
        return 1

    # Top-N matches should be returned for diagnostics even on hard_fail.
    matches = bad.get("matches") or []
    if len(matches) < 1:
        print(f"[FAIL] expected at least one match in matches, got {matches}")
        return 1

    # Case 2: clean Lucide user.svg against the same corpus → ok.
    good = check_anti_example_similarity(CLEAN_USER, corpus_root=CORPUS)
    if good.get("verdict") != "ok":
        print(
            f"[FAIL] clean Lucide user.svg should pass, got {good}"
        )
        return 1
    if not good.get("passed"):
        print(f"[FAIL] clean Lucide user.svg should pass, got {good}")
        return 1
    # Ensure top-N diagnostics still surface even when the icon is clean.
    if not good.get("matches"):
        print(
            f"[FAIL] expected diagnostic matches even on pass, got {good}"
        )
        return 1

    # Case 3: graceful skip when corpus directory does not exist.
    missing = check_anti_example_similarity(
        CLEAN_USER, corpus_root=ROOT / "no-such-dir"
    )
    if missing.get("verdict") != "ok" or not missing.get("skipped"):
        print(
            f"[FAIL] missing corpus should skip with verdict=ok, got {missing}"
        )
        return 1

    print("[OK] grade.anti_example_similarity smoke test passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReferenceUnavailable as exc:
        print(f"[SKIP] {exc}")
        sys.exit(0)
