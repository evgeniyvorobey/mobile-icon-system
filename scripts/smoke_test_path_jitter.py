#!/usr/bin/env python3
"""Smoke test for deterministic SVG path jitter."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_path_jitter import jitter_svg_paths


SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<path id="icon" fill="none" stroke="#000" '
    'd="M 4 4 L 20 4 C 21 8 21 16 20 20 L 4 20 Q 2 12 4 4 Z"/>'
    "</svg>"
)

_NUMBER_RE = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")


def _path_numbers(svg_text: str) -> list[float]:
    match = re.search(r"\bd=[\"']([^\"']+)[\"']", svg_text)
    if not match:
        raise AssertionError("missing d attribute")
    return [float(value) for value in _NUMBER_RE.findall(match.group(1))]


def main() -> int:
    first = jitter_svg_paths(SVG, seed=42, amplitude=0.25)
    second = jitter_svg_paths(SVG, seed=42, amplitude=0.25)
    if first != second:
        print("[FAIL] same seed should produce identical jittered SVG")
        return 1

    different = jitter_svg_paths(SVG, seed=43, amplitude=0.25)
    if different == first:
        print("[FAIL] different seed should change jittered SVG")
        return 1

    unchanged = jitter_svg_paths(SVG, seed=99, amplitude=0.0, snap=0.5)
    if unchanged != SVG:
        print("[FAIL] amplitude 0 should leave SVG unchanged")
        return 1

    original_numbers = _path_numbers(SVG)
    jittered_numbers = _path_numbers(first)
    for original, jittered in zip(original_numbers, jittered_numbers):
        if abs(jittered - original) > 0.250001:
            print(f"[FAIL] jitter exceeded amplitude: {original} -> {jittered}")
            return 1

    snapped = jitter_svg_paths(SVG, seed=7, amplitude=0.75, snap=0.5)
    for value in _path_numbers(snapped):
        doubled = value / 0.5
        if abs(doubled - round(doubled)) > 1e-9:
            print(f"[FAIL] snapped coordinate is not on 0.5 increment: {value}")
            return 1

    print("[OK] path jitter smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
