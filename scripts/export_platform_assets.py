#!/usr/bin/env python3
"""Export simple SVG icon masters to Android and iOS platform assets.

The Android exporter intentionally supports a narrow SVG subset: path-based
icons and a few simple primitives that can be expanded to VectorDrawable paths.
The iOS exporter scaffolds PDF-backed image sets; it does not attempt SVG to
PDF conversion because that requires non-stdlib rendering/conversion tooling.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional


ANDROID_NS = "http://schemas.android.com/apk/res/android"
SVG_NS = "http://www.w3.org/2000/svg"

ET.register_namespace("android", ANDROID_NS)


UNSUPPORTED_FEATURE_TAGS = {
    "filter",
    "mask",
    "linearGradient",
    "radialGradient",
    "meshGradient",
    "pattern",
    "text",
    "image",
    "foreignObject",
    "use",
    "symbol",
    "clipPath",
}

CONVERTIBLE_PRIMITIVES = {"circle", "line", "rect"}
NON_PATH_PRIMITIVES = {"ellipse", "polyline", "polygon"}

ALLOWED_CONTAINER_TAGS = {"svg", "g", "defs", "title", "desc", "metadata"}
ANDROID_COLOR_RE = re.compile(
    r"^(?:#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?|@[A-Za-z0-9_./:-]+|\?[A-Za-z0-9_./:-]+|currentColor|none)$"
)
NUMBER_RE = re.compile(r"^[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?$")
DIMENSION_RE = re.compile(
    r"^\s*([-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?)([a-zA-Z%]*)\s*$"
)
RESOURCE_NAME_RE = re.compile(r"[^a-z0-9_]+")

UNSUPPORTED_RENDERING_ATTRS = {
    "clip-rule",
    "display",
    "fill-opacity",
    "opacity",
    "paint-order",
    "stroke-dasharray",
    "stroke-dashoffset",
    "stroke-opacity",
    "vector-effect",
    "visibility",
}

SUPPORTED_PRESENTATION_ATTRS = {
    "fill",
    "stroke",
    "stroke-width",
    "stroke-linecap",
    "stroke-linejoin",
    "stroke-miterlimit",
    "fill-rule",
}


class ExportError(ValueError):
    """Raised when an asset cannot be exported safely."""


@dataclass
class ExportReport:
    android_files: list[Path] = field(default_factory=list)
    ios_imagesets: list[Path] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


@dataclass(frozen=True)
class SvgPath:
    path_data: str
    fill_color: Optional[str] = None
    stroke_color: Optional[str] = None
    stroke_width: Optional[str] = None
    stroke_linecap: Optional[str] = None
    stroke_linejoin: Optional[str] = None
    stroke_miterlimit: Optional[str] = None
    fill_type: Optional[str] = None


@dataclass(frozen=True)
class SvgMaster:
    source: Path
    resource_name: str
    viewport_width: str
    viewport_height: str
    width_dp: str
    height_dp: str
    paths: list[SvgPath]


def _local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def _attr(element: ET.Element, name: str) -> Optional[str]:
    value = element.get(name)
    if value is not None:
        return value
    return element.get(f"{{{SVG_NS}}}{name}")


def _android_attr(name: str) -> str:
    return f"{{{ANDROID_NS}}}{name}"


def _format_number(value: float) -> str:
    text = f"{value:.6f}".rstrip("0").rstrip(".")
    return text if text else "0"


def _number_attr(
    element: ET.Element,
    name: str,
    *,
    path: Path,
    default: Optional[float] = None,
    required: bool = False,
) -> float:
    raw = _attr(element, name)
    local = _local_name(element.tag)
    if raw is None or not raw.strip():
        if required or default is None:
            raise ExportError(f"{path}: <{local}> missing {name}")
        return default
    if not NUMBER_RE.match(raw.strip()):
        raise ExportError(
            f"{path}: unsupported <{local}> {name}={raw!r}; use a unitless number"
        )
    return float(raw)


def _resource_name(stem: str) -> str:
    candidate = RESOURCE_NAME_RE.sub("_", stem.lower()).strip("_")
    candidate = re.sub(r"_+", "_", candidate)
    if not candidate:
        candidate = "icon"
    if not re.match(r"^[a-z_]", candidate):
        candidate = f"ic_{candidate}"
    return candidate


def _parse_view_box(root: ET.Element, path: Path) -> tuple[str, str]:
    raw = _attr(root, "viewBox")
    if raw is None:
        raise ExportError(f"{path}: missing required svg viewBox")

    parts = re.split(r"[\s,]+", raw.strip())
    if len(parts) != 4 or not all(NUMBER_RE.match(part) for part in parts):
        raise ExportError(f"{path}: viewBox must contain four numeric values")

    min_x = float(parts[0])
    min_y = float(parts[1])
    width = float(parts[2])
    height = float(parts[3])
    if min_x != 0 or min_y != 0:
        raise ExportError(
            f"{path}: non-zero viewBox origin is unsupported; normalize to 0 0 before export"
        )
    if width <= 0 or height <= 0:
        raise ExportError(f"{path}: viewBox width and height must be positive")
    return _format_number(width), _format_number(height)


def _dimension_to_dp(
    raw: Optional[str],
    fallback: str,
    *,
    path: Path,
    attr_name: str,
    report: ExportReport,
) -> str:
    if raw is None or not raw.strip():
        return fallback

    match = DIMENSION_RE.match(raw)
    if not match:
        raise ExportError(f"{path}: unsupported {attr_name} dimension {raw!r}")

    value, unit = match.groups()
    unit = unit.lower()
    if unit not in ("", "px", "dp"):
        raise ExportError(
            f"{path}: unsupported {attr_name} unit {unit!r}; use unitless, px, or dp"
        )
    if unit in ("px", "dp"):
        report.warn(f"{path}: normalized {attr_name}={raw!r} to {value}dp")
    return _format_number(float(value))


def _parse_style(raw: Optional[str]) -> dict[str, str]:
    if not raw:
        return {}
    result: dict[str, str] = {}
    for item in raw.split(";"):
        if not item.strip():
            continue
        if ":" not in item:
            continue
        key, value = item.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def _presentation(element: ET.Element) -> dict[str, str]:
    values = _parse_style(_attr(element, "style"))
    for key in SUPPORTED_PRESENTATION_ATTRS:
        value = _attr(element, key)
        if value is not None:
            values[key] = value.strip()
    return values


def _path_from_rect(element: ET.Element, path: Path) -> str:
    x = _number_attr(element, "x", path=path, default=0)
    y = _number_attr(element, "y", path=path, default=0)
    width = _number_attr(element, "width", path=path, required=True)
    height = _number_attr(element, "height", path=path, required=True)
    if width <= 0 or height <= 0:
        raise ExportError(f"{path}: <rect> width and height must be positive")

    rx_raw = _attr(element, "rx")
    ry_raw = _attr(element, "ry")
    rx = _number_attr(element, "rx", path=path, default=0) if rx_raw is not None else 0
    ry = _number_attr(element, "ry", path=path, default=0) if ry_raw is not None else 0
    if rx_raw is not None and ry_raw is None:
        ry = rx
    if ry_raw is not None and rx_raw is None:
        rx = ry
    if rx < 0 or ry < 0:
        raise ExportError(f"{path}: <rect> rx/ry must be non-negative")

    rx = min(rx, width / 2)
    ry = min(ry, height / 2)
    right = x + width
    bottom = y + height

    if rx == 0 and ry == 0:
        return (
            f"M{_format_number(x)} {_format_number(y)} "
            f"H{_format_number(right)} V{_format_number(bottom)} "
            f"H{_format_number(x)} Z"
        )

    return (
        f"M{_format_number(x + rx)} {_format_number(y)} "
        f"H{_format_number(right - rx)} "
        f"A{_format_number(rx)} {_format_number(ry)} 0 0 1 "
        f"{_format_number(right)} {_format_number(y + ry)} "
        f"V{_format_number(bottom - ry)} "
        f"A{_format_number(rx)} {_format_number(ry)} 0 0 1 "
        f"{_format_number(right - rx)} {_format_number(bottom)} "
        f"H{_format_number(x + rx)} "
        f"A{_format_number(rx)} {_format_number(ry)} 0 0 1 "
        f"{_format_number(x)} {_format_number(bottom - ry)} "
        f"V{_format_number(y + ry)} "
        f"A{_format_number(rx)} {_format_number(ry)} 0 0 1 "
        f"{_format_number(x + rx)} {_format_number(y)} Z"
    )


def _path_from_circle(element: ET.Element, path: Path) -> str:
    cx = _number_attr(element, "cx", path=path, default=0)
    cy = _number_attr(element, "cy", path=path, default=0)
    radius = _number_attr(element, "r", path=path, required=True)
    if radius <= 0:
        raise ExportError(f"{path}: <circle> r must be positive")
    left = cx - radius
    right = cx + radius
    return (
        f"M{_format_number(left)} {_format_number(cy)} "
        f"A{_format_number(radius)} {_format_number(radius)} 0 1 0 "
        f"{_format_number(right)} {_format_number(cy)} "
        f"A{_format_number(radius)} {_format_number(radius)} 0 1 0 "
        f"{_format_number(left)} {_format_number(cy)} Z"
    )


def _path_from_line(element: ET.Element, path: Path) -> str:
    x1 = _number_attr(element, "x1", path=path, default=0)
    y1 = _number_attr(element, "y1", path=path, default=0)
    x2 = _number_attr(element, "x2", path=path, default=0)
    y2 = _number_attr(element, "y2", path=path, default=0)
    return (
        f"M{_format_number(x1)} {_format_number(y1)} "
        f"L{_format_number(x2)} {_format_number(y2)}"
    )


def _primitive_path_data(element: ET.Element, path: Path) -> str:
    local = _local_name(element.tag)
    if local == "rect":
        return _path_from_rect(element, path)
    if local == "circle":
        return _path_from_circle(element, path)
    if local == "line":
        return _path_from_line(element, path)
    raise ExportError(f"{path}: unsupported SVG element <{local}>")


def _merged_presentation(
    inherited: dict[str, str],
    element: ET.Element,
) -> dict[str, str]:
    merged = dict(inherited)
    merged.update(_presentation(element))
    return merged


def _check_color(path: Path, value: str, attr_name: str) -> None:
    if "url(" in value:
        raise ExportError(
            f"{path}: {attr_name} references paint server {value!r}; gradients/patterns are unsupported"
        )
    if not ANDROID_COLOR_RE.match(value):
        raise ExportError(
            f"{path}: unsupported {attr_name} value {value!r}; use #RGB/#RRGGBB, an Android resource/theme reference, or none"
        )


def _android_color_value(
    value: str,
    *,
    master: SvgMaster,
    report: ExportReport,
    tint: Optional[str],
    attr_name: str,
) -> str:
    if value != "currentColor":
        return value

    report.warn(
        f"{master.source}: converted {attr_name}=currentColor to #000000 "
        "for VectorDrawable export"
        + ("" if tint else "; pass --android-tint to preserve template-color behavior")
    )
    return "#000000"


def _check_stroke_width(path: Path, value: str) -> None:
    if not NUMBER_RE.match(value):
        raise ExportError(
            f"{path}: unsupported stroke-width value {value!r}; use a unitless number"
        )


def _check_stroke_linecap(path: Path, value: str) -> None:
    if value not in {"butt", "round", "square"}:
        raise ExportError(
            f"{path}: unsupported stroke-linecap value {value!r}; use butt, round, or square"
        )


def _check_stroke_linejoin(path: Path, value: str) -> None:
    if value not in {"miter", "round", "bevel"}:
        raise ExportError(
            f"{path}: unsupported stroke-linejoin value {value!r}; use miter, round, or bevel"
        )


def _check_fill_rule(path: Path, value: str) -> None:
    if value not in {"nonzero", "evenodd"}:
        raise ExportError(
            f"{path}: unsupported fill-rule value {value!r}; use nonzero or evenodd"
        )


def _android_fill_type(value: Optional[str]) -> Optional[str]:
    if value == "evenodd":
        return "evenOdd"
    if value == "nonzero":
        return "nonZero"
    return None


def _validate_attrs(path: Path, element: ET.Element) -> None:
    local = _local_name(element.tag)
    values = _parse_style(_attr(element, "style"))
    for name, value in values.items():
        if name in ("filter", "mask", "clip-path"):
            raise ExportError(f"{path}: unsupported {name} style on <{local}>")
        if name in UNSUPPORTED_RENDERING_ATTRS:
            raise ExportError(
                f"{path}: unsupported rendering style {name!r} on <{local}>"
            )
        if name in ("fill", "stroke"):
            _check_color(path, value, name)
        if name == "stroke-width":
            _check_stroke_width(path, value)
        if name == "stroke-linecap":
            _check_stroke_linecap(path, value)
        if name == "stroke-linejoin":
            _check_stroke_linejoin(path, value)
        if name == "stroke-miterlimit":
            _check_stroke_width(path, value)
        if name == "fill-rule":
            _check_fill_rule(path, value)

    for name in ("filter", "mask", "clip-path"):
        if _attr(element, name) is not None:
            raise ExportError(f"{path}: unsupported {name} attribute on <{local}>")

    for name in UNSUPPORTED_RENDERING_ATTRS:
        if _attr(element, name) is not None:
            raise ExportError(
                f"{path}: unsupported rendering attribute {name!r} on <{local}>"
            )

    for name in ("fill", "stroke"):
        value = _attr(element, name)
        if value is not None:
            _check_color(path, value.strip(), name)
    stroke_width = _attr(element, "stroke-width")
    if stroke_width is not None:
        _check_stroke_width(path, stroke_width.strip())
    stroke_linecap = _attr(element, "stroke-linecap")
    if stroke_linecap is not None:
        _check_stroke_linecap(path, stroke_linecap.strip())
    stroke_linejoin = _attr(element, "stroke-linejoin")
    if stroke_linejoin is not None:
        _check_stroke_linejoin(path, stroke_linejoin.strip())
    stroke_miterlimit = _attr(element, "stroke-miterlimit")
    if stroke_miterlimit is not None:
        _check_stroke_width(path, stroke_miterlimit.strip())
    fill_rule = _attr(element, "fill-rule")
    if fill_rule is not None:
        _check_fill_rule(path, fill_rule.strip())

    transform = _attr(element, "transform")
    if transform and (local in {"path", "g"} or local in CONVERTIBLE_PRIMITIVES):
        raise ExportError(
            f"{path}: transform on <{local}> is unsupported; flatten paths before export"
        )


def _walk_paths(
    path: Path,
    element: ET.Element,
    *,
    report: ExportReport,
    ignore_non_path: bool,
    inherited: Optional[dict[str, str]] = None,
) -> list[SvgPath]:
    inherited = inherited or {}
    local = _local_name(element.tag)

    if local in UNSUPPORTED_FEATURE_TAGS:
        raise ExportError(f"{path}: unsupported SVG feature <{local}>")
    if local in NON_PATH_PRIMITIVES:
        message = f"{path}: unsupported non-path primitive <{local}>"
        if ignore_non_path:
            report.warn(f"{message}; ignored")
            return []
        raise ExportError(message)
    if (
        local not in ALLOWED_CONTAINER_TAGS
        and local != "path"
        and local not in CONVERTIBLE_PRIMITIVES
    ):
        raise ExportError(f"{path}: unsupported SVG element <{local}>")

    _validate_attrs(path, element)
    presentation = _merged_presentation(inherited, element)

    if local == "path" or local in CONVERTIBLE_PRIMITIVES:
        if local == "path":
            path_data = _attr(element, "d")
            if path_data is None or not path_data.strip():
                raise ExportError(f"{path}: <path> missing non-empty d attribute")
            path_data = path_data.strip()
        else:
            path_data = _primitive_path_data(element, path)

        fill = presentation.get("fill")
        stroke = presentation.get("stroke")
        stroke_width = presentation.get("stroke-width")
        fill_rule = presentation.get("fill-rule")

        if fill == "none":
            fill = None
        if stroke == "none":
            stroke = None

        return [
            SvgPath(
                path_data=path_data,
                fill_color=fill,
                stroke_color=stroke,
                stroke_width=stroke_width,
                stroke_linecap=presentation.get("stroke-linecap"),
                stroke_linejoin=presentation.get("stroke-linejoin"),
                stroke_miterlimit=presentation.get("stroke-miterlimit"),
                fill_type=_android_fill_type(fill_rule),
            )
        ]

    found: list[SvgPath] = []
    for child in list(element):
        found.extend(
            _walk_paths(
                path,
                child,
                report=report,
                ignore_non_path=ignore_non_path,
                inherited=presentation,
            )
        )
    return found


def parse_svg_master(
    svg_path: Path,
    *,
    report: ExportReport,
    ignore_non_path: bool = False,
) -> SvgMaster:
    try:
        root = ET.fromstring(svg_path.read_text(encoding="utf-8"))
    except ET.ParseError as exc:
        raise ExportError(f"{svg_path}: invalid SVG XML: {exc}") from exc

    if _local_name(root.tag) != "svg":
        raise ExportError(f"{svg_path}: root element must be <svg>")

    viewport_width, viewport_height = _parse_view_box(root, svg_path)
    width_dp = _dimension_to_dp(
        _attr(root, "width"),
        viewport_width,
        path=svg_path,
        attr_name="width",
        report=report,
    )
    height_dp = _dimension_to_dp(
        _attr(root, "height"),
        viewport_height,
        path=svg_path,
        attr_name="height",
        report=report,
    )

    paths = _walk_paths(
        svg_path,
        root,
        report=report,
        ignore_non_path=ignore_non_path,
    )
    if not paths:
        raise ExportError(f"{svg_path}: no exportable <path> elements found")

    return SvgMaster(
        source=svg_path,
        resource_name=_resource_name(svg_path.stem),
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        width_dp=width_dp,
        height_dp=height_dp,
        paths=paths,
    )


def discover_svgs(svg_masters_dir: Path) -> list[Path]:
    if not svg_masters_dir.exists():
        raise ExportError(f"SVG masters directory does not exist: {svg_masters_dir}")
    if not svg_masters_dir.is_dir():
        raise ExportError(f"SVG masters path is not a directory: {svg_masters_dir}")
    return sorted(path for path in svg_masters_dir.glob("*.svg") if path.is_file())


def _ensure_unique_names(masters: Iterable[SvgMaster]) -> None:
    seen: dict[str, Path] = {}
    for master in masters:
        previous = seen.get(master.resource_name)
        if previous is not None:
            raise ExportError(
                "resource name collision after sanitizing names: "
                f"{previous.name} and {master.source.name} -> {master.resource_name}"
            )
        seen[master.resource_name] = master.source


def _write_xml(path: Path, element: ET.Element) -> None:
    tree = ET.ElementTree(element)
    ET.indent(tree, space="    ")
    path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(path, encoding="utf-8", xml_declaration=True, short_empty_elements=True)


def export_android(
    masters: list[SvgMaster],
    drawable_dir: Path,
    *,
    tint: Optional[str],
    report: ExportReport,
) -> None:
    drawable_dir.mkdir(parents=True, exist_ok=True)
    for master in masters:
        vector_attrs = {
            _android_attr("width"): f"{master.width_dp}dp",
            _android_attr("height"): f"{master.height_dp}dp",
            _android_attr("viewportWidth"): master.viewport_width,
            _android_attr("viewportHeight"): master.viewport_height,
        }
        if tint:
            vector_attrs[_android_attr("tint")] = tint

        vector = ET.Element("vector", vector_attrs)
        for index, svg_path in enumerate(master.paths, start=1):
            path_attrs = {
                _android_attr("pathData"): svg_path.path_data,
            }
            if len(master.paths) > 1:
                path_attrs[_android_attr("name")] = f"path_{index}"
            if svg_path.fill_color:
                path_attrs[_android_attr("fillColor")] = _android_color_value(
                    svg_path.fill_color,
                    master=master,
                    report=report,
                    tint=tint,
                    attr_name="fill",
                )
            if svg_path.stroke_color:
                path_attrs[_android_attr("strokeColor")] = _android_color_value(
                    svg_path.stroke_color,
                    master=master,
                    report=report,
                    tint=tint,
                    attr_name="stroke",
                )
            if svg_path.stroke_width:
                path_attrs[_android_attr("strokeWidth")] = svg_path.stroke_width
            if svg_path.stroke_linecap:
                path_attrs[_android_attr("strokeLineCap")] = svg_path.stroke_linecap
            if svg_path.stroke_linejoin:
                path_attrs[_android_attr("strokeLineJoin")] = svg_path.stroke_linejoin
            if svg_path.stroke_miterlimit:
                path_attrs[_android_attr("strokeMiterLimit")] = svg_path.stroke_miterlimit
            if svg_path.fill_type:
                path_attrs[_android_attr("fillType")] = svg_path.fill_type
            ET.SubElement(vector, "path", path_attrs)

        output_path = drawable_dir / f"{master.resource_name}.xml"
        _write_xml(output_path, vector)
        report.android_files.append(output_path)


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _ios_contents(filename: Optional[str]) -> dict[str, object]:
    image: dict[str, str] = {"idiom": "universal"}
    if filename:
        image["filename"] = filename
    return {
        "images": [image],
        "properties": {
            "preserves-vector-representation": True,
        },
        "info": {
            "author": "xcode",
            "version": 1,
        },
    }


def export_ios(
    masters: list[SvgMaster],
    xcassets_dir: Path,
    *,
    pdf_dir: Path,
    placeholder_manifest: bool,
    report: ExportReport,
) -> None:
    xcassets_dir.mkdir(parents=True, exist_ok=True)
    for master in masters:
        source_pdf = pdf_dir / f"{master.source.stem}.pdf"
        imageset_dir = xcassets_dir / f"{master.resource_name}.imageset"
        imageset_dir.mkdir(parents=True, exist_ok=True)

        if source_pdf.exists():
            target_pdf = imageset_dir / f"{master.resource_name}.pdf"
            shutil.copyfile(source_pdf, target_pdf)
            _write_json(imageset_dir / "Contents.json", _ios_contents(target_pdf.name))
        elif placeholder_manifest:
            _write_json(imageset_dir / "Contents.json", _ios_contents(None))
            todo = (
                f"# TODO: Add vector PDF for {master.resource_name}\n\n"
                f"Add a vector PDF named `{master.resource_name}.pdf` to this image set "
                "and add that filename to `Contents.json` before shipping.\n\n"
                "This exporter did not convert the SVG master to PDF; stdlib-only "
                "Python cannot perform a reliable vector SVG-to-PDF conversion.\n"
            )
            (imageset_dir / "TODO.md").write_text(todo, encoding="utf-8")
            report.warn(
                f"{master.source}: wrote placeholder iOS image set; missing {source_pdf}"
            )
        else:
            raise ExportError(
                f"{master.source}: missing iOS vector PDF with same stem at {source_pdf}; "
                "provide the PDF or pass --ios-placeholder-manifest"
            )

        report.ios_imagesets.append(imageset_dir)


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export simple SVG masters to Android VectorDrawable XML and iOS PDF-backed .xcassets image sets."
    )
    parser.add_argument(
        "svg_masters_dir",
        type=Path,
        help="Directory containing source .svg masters.",
    )
    parser.add_argument(
        "--platform",
        choices=("android", "ios", "both"),
        default="both",
        help="Platform assets to export (default: both).",
    )
    parser.add_argument(
        "--android-out",
        type=Path,
        default=None,
        help="Android drawable output directory (default: <svg-masters parent>/android/res/drawable).",
    )
    parser.add_argument(
        "--android-tint",
        default=None,
        help="Optional android:tint value to write on each VectorDrawable.",
    )
    parser.add_argument(
        "--ignore-non-path",
        action="store_true",
        help="Ignore SVG non-path primitives instead of failing. Unsupported filters, masks, gradients, text, images, and transforms still fail.",
    )
    parser.add_argument(
        "--ios-xcassets",
        type=Path,
        default=None,
        help="iOS .xcassets output directory (default: <svg-masters parent>/ios/Assets.xcassets).",
    )
    parser.add_argument(
        "--ios-pdf-dir",
        type=Path,
        default=None,
        help="Directory containing existing vector PDFs with stems matching the SVG masters (default: <svg-masters parent>/ios/pdf).",
    )
    parser.add_argument(
        "--ios-placeholder-manifest",
        action="store_true",
        help="For missing PDFs, write Contents.json plus TODO.md instead of failing. No PDF conversion is performed.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    svg_masters_dir = args.svg_masters_dir.expanduser().resolve()
    output_root = svg_masters_dir.parent
    android_out = (
        args.android_out.expanduser().resolve()
        if args.android_out
        else output_root / "android" / "res" / "drawable"
    )
    ios_xcassets = (
        args.ios_xcassets.expanduser().resolve()
        if args.ios_xcassets
        else output_root / "ios" / "Assets.xcassets"
    )
    ios_pdf_dir = (
        args.ios_pdf_dir.expanduser().resolve()
        if args.ios_pdf_dir
        else output_root / "ios" / "pdf"
    )

    report = ExportReport()
    try:
        svg_paths = discover_svgs(svg_masters_dir)
        if not svg_paths:
            raise ExportError(f"no .svg files found in {svg_masters_dir}")

        masters = [
            parse_svg_master(
                svg_path,
                report=report,
                ignore_non_path=args.ignore_non_path,
            )
            for svg_path in svg_paths
        ]
        _ensure_unique_names(masters)

        if args.platform in ("android", "both"):
            export_android(
                masters,
                android_out,
                tint=args.android_tint,
                report=report,
            )
        if args.platform in ("ios", "both"):
            export_ios(
                masters,
                ios_xcassets,
                pdf_dir=ios_pdf_dir,
                placeholder_manifest=args.ios_placeholder_manifest,
                report=report,
            )
    except ExportError as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1

    for warning in report.warnings:
        print(f"[WARN] {warning}", file=sys.stderr)

    if report.android_files:
        print(f"[OK] Android: wrote {len(report.android_files)} file(s) to {android_out}")
    if report.ios_imagesets:
        print(f"[OK] iOS: wrote {len(report.ios_imagesets)} image set(s) to {ios_xcassets}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
