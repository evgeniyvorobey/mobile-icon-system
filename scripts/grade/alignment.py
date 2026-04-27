"""Pixel-grid alignment audit on raw SVG geometry.

Walks ``<path d>`` and primitive shapes, scales every coordinate to each target
size, and counts how many fall off the integer grid.
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from .config import DEFAULTS


SVG_NS = "http://www.w3.org/2000/svg"
SvgSource = Union[str, Path]


_NUMBER_RE = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")
_COMMAND_RE = re.compile(r"[MmLlHhVvCcSsQqTtAaZz]")

# Argument count per absolute command. Lowercase variants share counts.
_CMD_ARGS = {
    "M": 2, "L": 2, "H": 1, "V": 1,
    "C": 6, "S": 4, "Q": 4, "T": 2,
    "A": 7, "Z": 0,
}


def _strip_ns(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def _parse_view_box(root: ET.Element, default: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    raw = root.get("viewBox")
    if not raw:
        return default
    parts = [float(x) for x in re.split(r"[\s,]+", raw.strip()) if x]
    if len(parts) != 4:
        return default
    return (parts[0], parts[1], parts[2], parts[3])


def _tokens(d_attr: str) -> List[Tuple[str, List[float]]]:
    """Yield (command, args) groups. Splits implicit-repeat commands per SVG spec."""
    out: List[Tuple[str, List[float]]] = []
    pos = 0
    while pos < len(d_attr):
        m = _COMMAND_RE.search(d_attr, pos)
        if not m:
            break
        cmd = m.group(0)
        start = m.end()
        next_cmd = _COMMAND_RE.search(d_attr, start)
        end = next_cmd.start() if next_cmd else len(d_attr)
        nums = [float(x) for x in _NUMBER_RE.findall(d_attr[start:end])]
        upper = cmd.upper()
        per = _CMD_ARGS.get(upper, 0)
        if upper == "Z" or per == 0:
            out.append((cmd, []))
        else:
            i = 0
            first = True
            while i + per <= len(nums):
                chunk = nums[i:i + per]
                if not first and upper == "M":
                    # Subsequent pairs after an M are implicit L.
                    out.append(("l" if cmd.islower() else "L", chunk))
                else:
                    out.append((cmd, chunk))
                first = False
                i += per
        pos = end
    return out


def _emit_path_points(d_attr: str) -> List[Tuple[float, float]]:
    """Walk a path's `d` attribute, returning every absolute coordinate touched."""
    points: List[Tuple[float, float]] = []
    cx = cy = 0.0
    sx = sy = 0.0  # subpath start, for Z
    started = False
    for cmd, args in _tokens(d_attr):
        upper = cmd.upper()
        rel = cmd.islower()
        if upper == "M":
            x, y = args
            cx = (cx + x) if rel and started else x
            cy = (cy + y) if rel and started else y
            sx, sy = cx, cy
            started = True
            points.append((cx, cy))
        elif upper == "L":
            x, y = args
            cx = (cx + x) if rel else x
            cy = (cy + y) if rel else y
            points.append((cx, cy))
        elif upper == "H":
            x = args[0]
            cx = (cx + x) if rel else x
            points.append((cx, cy))
        elif upper == "V":
            y = args[0]
            cy = (cy + y) if rel else y
            points.append((cx, cy))
        elif upper in ("C", "S", "Q", "T"):
            # Emit every coordinate pair (control points + endpoint).
            for i in range(0, len(args), 2):
                x = args[i]
                y = args[i + 1]
                ax = (cx + x) if rel else x
                ay = (cy + y) if rel else y
                points.append((ax, ay))
            cx = (cx + args[-2]) if rel else args[-2]
            cy = (cy + args[-1]) if rel else args[-1]
        elif upper == "A":
            # Args: rx, ry, x-axis-rot, large-arc, sweep, x, y
            x, y = args[5], args[6]
            cx = (cx + x) if rel else x
            cy = (cy + y) if rel else y
            points.append((cx, cy))
        elif upper == "Z":
            cx, cy = sx, sy
    return points


def _shape_points(elem: ET.Element) -> List[Tuple[float, float]]:
    name = _strip_ns(elem.tag)
    g = elem.get
    try:
        if name == "rect":
            x = float(g("x", "0"))
            y = float(g("y", "0"))
            w = float(g("width", "0"))
            h = float(g("height", "0"))
            return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        if name == "circle":
            cx = float(g("cx", "0"))
            cy = float(g("cy", "0"))
            r = float(g("r", "0"))
            return [(cx - r, cy), (cx + r, cy), (cx, cy - r), (cx, cy + r)]
        if name == "ellipse":
            cx = float(g("cx", "0"))
            cy = float(g("cy", "0"))
            rx = float(g("rx", "0"))
            ry = float(g("ry", "0"))
            return [(cx - rx, cy), (cx + rx, cy), (cx, cy - ry), (cx, cy + ry)]
        if name == "line":
            return [
                (float(g("x1", "0")), float(g("y1", "0"))),
                (float(g("x2", "0")), float(g("y2", "0"))),
            ]
        if name in ("polygon", "polyline"):
            raw = g("points", "")
            nums = [float(n) for n in _NUMBER_RE.findall(raw)]
            return [(nums[i], nums[i + 1]) for i in range(0, len(nums) - 1, 2)]
    except (TypeError, ValueError):
        return []
    return []


def _stroke_width_int_odd(elem: ET.Element) -> bool:
    raw = elem.get("stroke-width")
    if raw is None:
        return False
    try:
        sw = float(raw)
    except ValueError:
        return False
    return abs(sw - round(sw)) < 1e-6 and int(round(sw)) % 2 == 1


def audit_alignment(
    svg_source: SvgSource,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Audit how many vertices land off the integer pixel grid at each target size."""
    cfg = (config or DEFAULTS)["alignment"]
    sizes: List[int] = list(cfg["sizes"])
    tol = float(cfg["tolerance"])
    fail_ratio_24 = float(cfg["max_off_grid_ratio_24"])
    default_vb = tuple(cfg["default_view_box"])

    text = (
        svg_source if isinstance(svg_source, str) and "<svg" in svg_source
        else Path(svg_source).read_text(encoding="utf-8")
    )
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return {
            "passed": False,
            "errors": [f"SVG parse error: {exc}"],
            "off_grid_by_size": {},
            "warnings": [],
        }

    vb = _parse_view_box(root, default_vb)
    vb_w = vb[2] if vb[2] > 0 else default_vb[2]
    vb_h = vb[3] if vb[3] > 0 else default_vb[3]

    points: List[Tuple[float, float, bool]] = []  # (x, y, half_pixel_ok)
    warnings_list: List[str] = []
    transformed_skipped = 0

    for elem in root.iter():
        name = _strip_ns(elem.tag)
        if name == "g" and elem.get("transform"):
            warnings_list.append(
                "transform present on a <g>; alignment audit may be incomplete"
            )
            transformed_skipped += 1
            continue
        if elem.get("transform") and name != "svg":
            warnings_list.append(
                f"transform present on <{name}>; alignment audit may be incomplete"
            )
            continue
        half_ok = _stroke_width_int_odd(elem)
        coords: List[Tuple[float, float]] = []
        if name == "path":
            d = elem.get("d") or ""
            coords = _emit_path_points(d)
        else:
            coords = _shape_points(elem)
        for x, y in coords:
            points.append((x, y, half_ok))

    by_size: Dict[int, Dict[str, Any]] = {}
    overall_pass = True
    for size in sizes:
        sx = float(size) / float(vb_w)
        sy = float(size) / float(vb_h)
        total = len(points)
        off = 0
        offending: List[Tuple[float, float]] = []
        for x, y, half_ok in points:
            px = (x - vb[0]) * sx
            py = (y - vb[1]) * sy
            dx = abs(px - round(px))
            dy = abs(py - round(py))
            if half_ok:
                # Allow either integer OR half-pixel offsets.
                dx = min(dx, abs(px - (round(px - 0.5) + 0.5)))
                dy = min(dy, abs(py - (round(py - 0.5) + 0.5)))
            if dx > tol or dy > tol:
                off += 1
                if len(offending) < 5:
                    offending.append((round(px, 3), round(py, 3)))
        ratio = (off / total) if total else 0.0
        size_pass = True
        if size == 24:
            size_pass = ratio <= fail_ratio_24
            if not size_pass:
                overall_pass = False
        by_size[size] = {
            "total": total,
            "off_grid": off,
            "ratio": ratio,
            "passed": size_pass,
            "examples": offending,
        }

    return {
        "view_box": list(vb),
        "off_grid_by_size": by_size,
        "passed": overall_pass,
        "warnings": warnings_list,
        "transformed_groups_skipped": transformed_skipped,
        "errors": [],
    }
