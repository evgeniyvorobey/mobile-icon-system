#!/usr/bin/env python3
"""Check a declared icon palette against WCAG 2.2 non-text contrast (SC 1.4.11).

Usage
-----
    python3 scripts/check_contrast.py assets/demo-package/palette.json
    python3 scripts/check_contrast.py palette.json --tier AAA
    python3 scripts/check_contrast.py --pair "#1B4DE4" "#FFFFFF"

Exit codes match the grade pipeline: 0 pass, 1 warnings only, 2 hard fail.

Scope, stated plainly: this checks declared colour pairs. It does not render
an icon, and it says nothing about whether an icon is legible, well drawn, or
correctly labelled. Icons here use currentColor, so the shipped ink colour
lives in the consuming app's palette, not in the SVG - the palette file is
therefore the honest unit of validation.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from grade.contrast import (  # noqa: E402
    ContrastError,
    check_pair,
    check_palette,
    load_palette,
)


def _render(result: dict) -> str:
    lines = [
        "# WCAG 2.2 non-text contrast (SC 1.4.11)",
        "",
        f"Tier: **{result['tier']}** - informational graphics need "
        f"{result['non_text_threshold']:.1f}:1; text inside an icon needs 4.5:1.",
        "",
        f"Pairs declared: {result['n_pairs']} | checked: {result['n_checked']} | "
        f"decorative, exempt: {result['n_decorative_skipped']}",
        "",
        "| Pair | Foreground | Background | Ratio | Required | Verdict |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for p in result["pairs"]:
        if p.get("skipped"):
            lines.append(
                f"| {p['label']} | - | - | - | - | skipped ({p['skipped']}) |"
            )
            continue
        ratio = "n/a" if p["ratio"] is None else f"{p['ratio']:.2f}:1"
        verdict = "pass" if p["passed"] else "**FAIL**"
        if p["passed"] and p["warnings"]:
            verdict = "pass (narrow)"
        lines.append(
            f"| {p['label']} | `{p['foreground']}` | `{p['background']}` | "
            f"{ratio} | {p['threshold']:.1f}:1 | {verdict} |"
        )
    if result["errors"]:
        lines += ["", "## Failures"] + [f"- {e}" for e in result["errors"]]
    if result["warnings"]:
        lines += ["", "## Warnings"] + [f"- {w}" for w in result["warnings"]]
    if not result["errors"] and not result["warnings"]:
        lines += ["", "All declared pairs clear the threshold."]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("palette", nargs="?", help="Path to a palette JSON file")
    ap.add_argument("--tier", choices=["AA", "AAA"], help="Override the palette's tier")
    ap.add_argument(
        "--pair",
        nargs=2,
        metavar=("FOREGROUND", "BACKGROUND"),
        help="Check a single ad-hoc colour pair instead of a file",
    )
    args = ap.parse_args()

    if args.pair:
        threshold = 4.5 if args.tier == "AAA" else 3.0
        entry = check_pair(args.pair[0], args.pair[1], threshold, "ad-hoc pair")
        if entry["ratio"] is None:
            print("\n".join(f"error: {e}" for e in entry["errors"]))
            return 2
        print(
            f"{entry['ratio']:.2f}:1 "
            f"({'pass' if entry['passed'] else 'FAIL'} against {threshold:.1f}:1)"
        )
        return 0 if entry["passed"] else 2

    if not args.palette:
        ap.error("provide a palette file, or use --pair FOREGROUND BACKGROUND")

    try:
        palette = load_palette(args.palette)
        result = check_palette(palette, args.tier)
    except (ContrastError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(_render(result))
    if result["hard_fail"]:
        return 2
    if result["warnings"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
