"""WCAG 2.2 non-text contrast check (SC 1.4.11) for declared icon palettes.

Why this module exists
----------------------
README.md and SKILL.md claimed icons were "validated for WCAG 2.2
accessibility" and that the skill delivers "3:1 non-text contrast by default".
`references/accessibility.md` states the rule correctly, but nothing in the
repository ever computed a contrast ratio - the claim rested on prose. This
module makes the claim true, or the claim has to come out.

What it checks, and what it cannot
----------------------------------
Icon SVGs here use ``currentColor``: the ink colour is supplied by the
consuming app, not by the file. Rasterising an SVG and measuring its own
pixels would therefore measure the renderer's default, not the shipped
colour, and would be theatre.

So the unit of validation is the **declared palette**: the foreground/background
pairs the icon system says it ships with, per surface and per state. That is
the artifact a designer actually controls and the one an auditor would ask for.

This checks colour pairs. It does NOT check:
- translucent materials (iOS Liquid Glass, Material 3 surfaces) - the rule for
  those is worst-case backdrop, and the worst case has to be declared as its
  own pair (see `references/accessibility.md`)
- whether the icon is informational or decorative - decorative icons are exempt
  from SC 1.4.11 and must be declared ``"decorative": true`` to be skipped
- anything about touch targets, labels, or screen-reader behaviour

Thresholds
----------
SC 1.4.11 Non-text Contrast (AA): 3:1 for graphical objects conveying
information. SC 1.4.3 Contrast (Minimum): 4.5:1 for text inside an icon.
AAA raises non-text to 4.5:1 in this implementation, matching the tier
language in `references/accessibility.md`.

Maths per WCAG 2.x: channel values are divided by 255, linearised with the
sRGB transfer function, combined as 0.2126R + 0.7152G + 0.0722B, and the
ratio taken as (L_lighter + 0.05) / (L_darker + 0.05).
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union


__all__ = [
    "parse_color",
    "relative_luminance",
    "contrast_ratio",
    "check_pair",
    "check_palette",
    "load_palette",
    "NON_TEXT_AA",
    "NON_TEXT_AAA",
    "TEXT_AA",
]


# SC 1.4.11 Non-text Contrast (AA). Graphical objects conveying information.
NON_TEXT_AA = 3.0
# AAA tier as used by references/accessibility.md.
NON_TEXT_AAA = 4.5
# SC 1.4.3 Contrast (Minimum), for text characters drawn inside an icon.
TEXT_AA = 4.5


_HEX_RE = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
_RGB_RE = re.compile(
    r"^rgba?\(\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*(?:[,/]\s*([\d.]+%?)\s*)?\)$",
    re.IGNORECASE,
)

_NAMED = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "lime": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "aqua": (0, 255, 255),
    "magenta": (255, 0, 255),
    "fuchsia": (255, 0, 255),
    "silver": (192, 192, 192),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),
    "maroon": (128, 0, 0),
    "olive": (128, 128, 0),
    "green": (0, 128, 0),
    "purple": (128, 0, 128),
    "teal": (0, 128, 128),
    "navy": (0, 0, 128),
    "orange": (255, 165, 0),
}


class ContrastError(ValueError):
    """Raised when a colour cannot be parsed."""


def parse_color(value: Union[str, Sequence[int]]) -> Tuple[int, int, int]:
    """Parse ``#rgb``, ``#rrggbb``, 4/8-digit hex, ``rgb()``, or a CSS name.

    Alpha is rejected rather than silently ignored: a semi-transparent ink
    colour has no single contrast ratio - it depends on what is behind it,
    which is exactly the worst-case-backdrop case the caller must declare
    explicitly as its own opaque pair.
    """
    if isinstance(value, (list, tuple)):
        if len(value) != 3:
            raise ContrastError(f"expected 3 channels, got {len(value)}: {value!r}")
        rgb = tuple(int(c) for c in value)
        for c in rgb:
            if not 0 <= c <= 255:
                raise ContrastError(f"channel out of range 0-255: {value!r}")
        return rgb  # type: ignore[return-value]

    if not isinstance(value, str):
        raise ContrastError(f"unsupported colour type {type(value).__name__}: {value!r}")

    text = value.strip()
    lowered = text.lower()
    if lowered in _NAMED:
        return _NAMED[lowered]

    m = _HEX_RE.match(text)
    if m:
        digits = m.group(1)
        if len(digits) in (3, 4):
            if len(digits) == 4:
                raise ContrastError(
                    f"{value!r} carries alpha; declare the composited opaque "
                    f"colour instead (see the worst-case-backdrop rule)"
                )
            r, g, b = (int(d * 2, 16) for d in digits[:3])
            return (r, g, b)
        if len(digits) == 8:
            raise ContrastError(
                f"{value!r} carries alpha; declare the composited opaque "
                f"colour instead (see the worst-case-backdrop rule)"
            )
        return (int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16))

    m = _RGB_RE.match(text)
    if m:
        if m.group(4) is not None:
            raise ContrastError(
                f"{value!r} carries alpha; declare the composited opaque colour instead"
            )
        rgb = tuple(int(m.group(i)) for i in (1, 2, 3))
        for c in rgb:
            if not 0 <= c <= 255:
                raise ContrastError(f"channel out of range 0-255: {value!r}")
        return rgb  # type: ignore[return-value]

    raise ContrastError(f"unrecognised colour: {value!r}")


def _linearise(channel_255: int) -> float:
    c = channel_255 / 255.0
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(color: Union[str, Sequence[int]]) -> float:
    """WCAG relative luminance: 0.2126R + 0.7152G + 0.0722B on linear sRGB."""
    r, g, b = parse_color(color)
    return (
        0.2126 * _linearise(r)
        + 0.7152 * _linearise(g)
        + 0.0722 * _linearise(b)
    )


def contrast_ratio(
    foreground: Union[str, Sequence[int]],
    background: Union[str, Sequence[int]],
) -> float:
    """WCAG contrast ratio, 1.0 to 21.0. Order-independent."""
    l1 = relative_luminance(foreground)
    l2 = relative_luminance(background)
    lighter, darker = (l1, l2) if l1 >= l2 else (l2, l1)
    return (lighter + 0.05) / (darker + 0.05)


def check_pair(
    foreground: Union[str, Sequence[int]],
    background: Union[str, Sequence[int]],
    threshold: float = NON_TEXT_AA,
    label: str = "",
) -> Dict[str, Any]:
    """Check one foreground/background pair against a ratio threshold."""
    try:
        ratio = contrast_ratio(foreground, background)
    except ContrastError as exc:
        return {
            "label": label,
            "foreground": foreground,
            "background": background,
            "threshold": threshold,
            "ratio": None,
            "passed": False,
            "hard_fail": True,
            "errors": [str(exc)],
            "warnings": [],
        }

    passed = ratio >= threshold
    entry: Dict[str, Any] = {
        "label": label,
        "foreground": foreground,
        "background": background,
        "threshold": threshold,
        "ratio": round(ratio, 3),
        "passed": passed,
        "hard_fail": not passed,
        "errors": [],
        "warnings": [],
    }
    if not passed:
        entry["errors"].append(
            f"{label or 'pair'}: {ratio:.2f}:1 against a required {threshold:.1f}:1 "
            f"({foreground} on {background})"
        )
    elif ratio < threshold * 1.1:
        entry["warnings"].append(
            f"{label or 'pair'}: {ratio:.2f}:1 clears {threshold:.1f}:1 by under 10% - "
            f"a small token change will break it"
        )
    return entry


def load_palette(path: Union[str, Path]) -> Dict[str, Any]:
    """Load a palette JSON declaring the pairs the icon set ships with.

    Expected shape::

        {
          "tier": "AA",
          "pairs": [
            {"label": "Tab Bar selected glyph on bar surface",
             "foreground": "#1B4DE4", "background": "#FFFFFF"},
            {"label": "Decorative divider", "foreground": "#EEE",
             "background": "#FFF", "decorative": true},
            {"label": "Aa inside search glyph", "foreground": "#333",
             "background": "#FFF", "text": true}
          ]
        }
    """
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("pairs"), list):
        raise ContrastError(f"{p}: expected an object with a 'pairs' array")
    return data


def check_palette(
    palette: Dict[str, Any],
    tier: Optional[str] = None,
) -> Dict[str, Any]:
    """Check every declared pair. Returns the standard grade-check dict.

    Decorative pairs are skipped (SC 1.4.11 exempts them) but are reported so
    that "skipped" is visible rather than silent. Pairs marked ``text`` are
    held to SC 1.4.3 at 4.5:1 regardless of tier.
    """
    resolved_tier = (tier or palette.get("tier") or "AA").upper()
    if resolved_tier not in ("AA", "AAA"):
        raise ContrastError(f"unknown tier {resolved_tier!r}; expected AA or AAA")
    non_text_threshold = NON_TEXT_AA if resolved_tier == "AA" else NON_TEXT_AAA

    results: List[Dict[str, Any]] = []
    errors: List[str] = []
    warnings: List[str] = []
    skipped = 0

    for raw in palette["pairs"]:
        label = str(raw.get("label", "")).strip()
        if raw.get("decorative"):
            skipped += 1
            results.append(
                {
                    "label": label,
                    "skipped": "decorative - exempt from SC 1.4.11",
                    "passed": True,
                    "hard_fail": False,
                    "ratio": None,
                }
            )
            continue
        threshold = TEXT_AA if raw.get("text") else non_text_threshold
        entry = check_pair(
            raw.get("foreground"), raw.get("background"), threshold, label
        )
        results.append(entry)
        errors.extend(entry["errors"])
        warnings.extend(entry["warnings"])

    checked = len(results) - skipped
    return {
        "tier": resolved_tier,
        "non_text_threshold": non_text_threshold,
        "n_pairs": len(results),
        "n_checked": checked,
        "n_decorative_skipped": skipped,
        "pairs": results,
        "passed": not errors,
        "hard_fail": bool(errors),
        "errors": errors,
        "warnings": warnings,
    }
