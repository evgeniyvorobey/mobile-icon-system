#!/usr/bin/env python3
"""Smoke test for grade.reference (perceptual hash)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.reference import (
    ReferenceUnavailable,
    compare_to_reference,
    is_available,
)


REF_CHECK = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<polyline points="4,13 10,19 20,6" fill="none" stroke="#000" stroke-width="2"/>'
    "</svg>"
)
SIMILAR_CHECK = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<polyline points="5,13 10,18 19,7" fill="none" stroke="#000" stroke-width="2"/>'
    "</svg>"
)


def main() -> int:
    if not is_available():
        print("[SKIP] imagehash not installed")
        return 0

    # Identical SVG -> distance 0 -> plagiarism flag.
    same = compare_to_reference(REF_CHECK, [REF_CHECK])
    if same["verdict"] != "plagiarism":
        print(f"[FAIL] identical comparison should be plagiarism: {same}")
        return 1

    # Slight variation -> low distance, on-vocabulary OR still plagiarism (very close).
    similar = compare_to_reference(SIMILAR_CHECK, [REF_CHECK])
    if similar["distance"] is None or similar["distance"] > 22:
        print(f"[FAIL] similar comparison should be on-vocabulary, got {similar}")
        return 1

    # Off-vocabulary case: a very different glyph.
    far_svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
        '<rect x="2" y="2" width="20" height="6" fill="#000"/>'
        '<rect x="2" y="10" width="20" height="2" fill="#000"/>'
        '<rect x="2" y="14" width="20" height="2" fill="#000"/>'
        '<rect x="2" y="18" width="20" height="4" fill="#000"/>'
        "</svg>"
    )
    far = compare_to_reference(far_svg, [REF_CHECK])
    # Distance from a checkmark to a barcode is typically large.
    if far["distance"] is None:
        print(f"[FAIL] off-vocab distance unexpectedly None: {far}")
        return 1

    print("[OK] grade.reference smoke test passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReferenceUnavailable as exc:
        print(f"[SKIP] {exc}")
        sys.exit(0)
