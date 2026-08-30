#!/usr/bin/env python3
"""Smoke test for grade.contrast (WCAG 2.2 SC 1.4.11).

Verifies:
1. The ratio maths matches published WCAG reference values to within 0.02.
2. Luminance anchors are exact: white 1.0, black 0.0.
3. The ratio is order-independent.
4. Colours carrying alpha are rejected, not silently composited.
5. Decorative pairs are skipped and counted, not silently dropped.
6. Text pairs are held to 4.5:1 even at tier AA.
7. Tier AAA raises the non-text threshold to 4.5:1.
8. FALSIFIER: a palette that should fail does fail. A check that cannot fail
   is not a check, and a green result from one means nothing.
9. The shipped demo palette passes at its declared tier.
"""
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from grade.contrast import (  # noqa: E402
    ContrastError,
    check_palette,
    contrast_ratio,
    load_palette,
    parse_color,
    relative_luminance,
)


# Published WCAG contrast ratios, used here as an external oracle rather than
# a round-trip of our own output.
REFERENCE = [
    ("#000000", "#FFFFFF", 21.00),
    ("#FFFFFF", "#FFFFFF", 1.00),
    ("#777777", "#FFFFFF", 4.48),
    ("#767676", "#FFFFFF", 4.54),
    ("#949494", "#FFFFFF", 3.03),
    ("#0000FF", "#FFFFFF", 8.59),
    ("#FF0000", "#FFFFFF", 4.00),
    ("#008000", "#FFFFFF", 5.13),
    ("#FFFF00", "#000000", 19.56),
]

REJECT = ["#12345678", "#abcd", "rgba(0,0,0,0.5)", "rgb(300,0,0)", "nonsense", ""]


def main() -> int:
    for fg, bg, expected in REFERENCE:
        got = contrast_ratio(fg, bg)
        if abs(got - expected) > 0.02:
            print(f"[FAIL] {fg} on {bg}: got {got:.3f}, published {expected}")
            return 1

    if relative_luminance("#FFFFFF") != 1.0 or relative_luminance("#000000") != 0.0:
        print("[FAIL] luminance anchors wrong")
        return 1

    if abs(contrast_ratio("#123456", "#abcdef") - contrast_ratio("#abcdef", "#123456")) > 1e-12:
        print("[FAIL] contrast ratio is not order-independent")
        return 1

    if parse_color("#fff") != parse_color("#ffffff"):
        print("[FAIL] 3-digit shorthand does not match 6-digit")
        return 1

    for bad in REJECT:
        try:
            parse_color(bad)
        except ContrastError:
            continue
        print(f"[FAIL] {bad!r} should have been rejected")
        return 1

    decorative = check_palette(
        {
            "tier": "AA",
            "pairs": [
                {"label": "informational", "foreground": "#000", "background": "#FFF"},
                {
                    "label": "hairline",
                    "foreground": "#EEEEEE",
                    "background": "#FFFFFF",
                    "decorative": True,
                },
            ],
        }
    )
    if not decorative["passed"] or decorative["n_decorative_skipped"] != 1:
        print(f"[FAIL] decorative pair not skipped/counted: {decorative}")
        return 1
    if decorative["n_checked"] != 1:
        print(f"[FAIL] expected 1 checked pair, got {decorative['n_checked']}")
        return 1

    # #949494 on white is 3.03:1 - clears non-text AA, fails text 4.5:1.
    text_pair = check_palette(
        {
            "tier": "AA",
            "pairs": [
                {
                    "label": "Aa inside glyph",
                    "foreground": "#949494",
                    "background": "#FFFFFF",
                    "text": True,
                }
            ],
        }
    )
    if text_pair["passed"]:
        print("[FAIL] text pair at 3.03:1 should fail the 4.5:1 text threshold")
        return 1

    aaa = check_palette(
        {
            "tier": "AA",
            "pairs": [
                {"label": "borderline", "foreground": "#949494", "background": "#FFFFFF"}
            ],
        },
        tier="AAA",
    )
    if aaa["passed"] or aaa["non_text_threshold"] != 4.5:
        print(f"[FAIL] tier AAA should raise the non-text threshold and fail 3.03:1: {aaa}")
        return 1

    # FALSIFIER: the check must be able to fail on a palette built to fail.
    failing = check_palette(
        {
            "tier": "AA",
            "pairs": [
                {"label": "too light", "foreground": "#CCCCCC", "background": "#FFFFFF"}
            ],
        }
    )
    if failing["passed"] or not failing["hard_fail"] or not failing["errors"]:
        print(f"[FAIL] falsifier: a failing palette was reported as passing: {failing}")
        return 1

    demo = ROOT / "assets" / "demo-package" / "palette.json"
    if demo.is_file():
        shipped = check_palette(load_palette(demo))
        if not shipped["passed"]:
            print(f"[FAIL] shipped demo palette does not pass: {shipped['errors']}")
            return 1
    else:
        print(f"[FAIL] demo palette missing at {demo}")
        return 1

    print("[OK] grade.contrast smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
