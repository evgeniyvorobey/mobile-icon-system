#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_platform_assets.py"
ANDROID_NS = "http://schemas.android.com/apk/res/android"


SIMPLE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
  <path fill="#123456" fill-rule="evenodd" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M4 4 H20 V20 H4 Z"/>
</svg>
"""

UNSUPPORTED_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <text x="2" y="12">Nope</text>
</svg>
"""

NON_PATH_WITH_PATH_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <ellipse cx="12" cy="12" rx="10" ry="8" fill="#ffffff"/>
  <path fill="#123456" d="M4 4 H20 V20 H4 Z"/>
</svg>
"""

PRIMITIVE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <rect x="4.5" y="4.75" width="15" height="14.5" rx="2.75" stroke="currentColor" stroke-width="1.75"/>
  <circle cx="8.25" cy="10" r="1" fill="currentColor"/>
  <line x1="11.25" y1="10" x2="16" y2="10" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"/>
</svg>
"""

CURRENT_COLOR_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path fill="currentColor" stroke="currentColor" stroke-width="2" d="M4 4 H20 V20 H4 Z"/>
</svg>
"""

DUMMY_PDF = b"%PDF-1.4\n% mobile-icon-system smoke fixture\n1 0 obj\n<<>>\nendobj\n%%EOF\n"


def run_exporter(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(EXPORTER), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def android_attr(name: str) -> str:
    return f"{{{ANDROID_NS}}}{name}"


def assert_success(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode != 0:
        raise SystemExit(
            f"[FAIL] {label} failed\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def assert_failure(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode == 0:
        raise SystemExit(
            f"[FAIL] {label} unexpectedly succeeded\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def test_android_export(temp_root: Path) -> None:
    svg_dir = temp_root / "android-case" / "svg-masters"
    drawable_dir = temp_root / "android-case" / "res" / "drawable"
    svg_dir.mkdir(parents=True)
    (svg_dir / "Check Mark.svg").write_text(SIMPLE_SVG, encoding="utf-8")

    result = run_exporter(
        str(svg_dir),
        "--platform",
        "android",
        "--android-out",
        str(drawable_dir),
        "--android-tint",
        "?attr/colorControlNormal",
    )
    assert_success(result, "Android export")

    output = drawable_dir / "check_mark.xml"
    if not output.exists():
        raise SystemExit(f"[FAIL] missing Android vector drawable: {output}")

    root = ET.parse(output).getroot()
    if root.tag != "vector":
        raise SystemExit(f"[FAIL] expected <vector>, got {root.tag}")

    expected_vector_attrs = {
        "width": "24dp",
        "height": "24dp",
        "viewportWidth": "24",
        "viewportHeight": "24",
        "tint": "?attr/colorControlNormal",
    }
    for key, expected in expected_vector_attrs.items():
        actual = root.get(android_attr(key))
        if actual != expected:
            raise SystemExit(f"[FAIL] vector {key}: expected {expected!r}, got {actual!r}")

    path = root.find("path")
    if path is None:
        raise SystemExit("[FAIL] Android vector missing <path>")

    expected_path_attrs = {
        "pathData": "M4 4 H20 V20 H4 Z",
        "fillColor": "#123456",
        "fillType": "evenOdd",
        "strokeColor": "#000000",
        "strokeWidth": "1.5",
        "strokeLineCap": "round",
        "strokeLineJoin": "round",
    }
    for key, expected in expected_path_attrs.items():
        actual = path.get(android_attr(key))
        if actual != expected:
            raise SystemExit(f"[FAIL] path {key}: expected {expected!r}, got {actual!r}")


def test_ios_export(temp_root: Path) -> None:
    case_dir = temp_root / "ios-case"
    svg_dir = case_dir / "svg-masters"
    pdf_dir = case_dir / "ios" / "pdf"
    xcassets_dir = case_dir / "ios" / "Assets.xcassets"
    svg_dir.mkdir(parents=True)
    pdf_dir.mkdir(parents=True)
    (svg_dir / "check.svg").write_text(SIMPLE_SVG, encoding="utf-8")
    (pdf_dir / "check.pdf").write_bytes(DUMMY_PDF)

    result = run_exporter(
        str(svg_dir),
        "--platform",
        "ios",
        "--ios-pdf-dir",
        str(pdf_dir),
        "--ios-xcassets",
        str(xcassets_dir),
    )
    assert_success(result, "iOS export")

    imageset = xcassets_dir / "check.imageset"
    copied_pdf = imageset / "check.pdf"
    contents_path = imageset / "Contents.json"
    if not copied_pdf.exists():
        raise SystemExit(f"[FAIL] missing copied PDF: {copied_pdf}")
    if not contents_path.exists():
        raise SystemExit(f"[FAIL] missing Contents.json: {contents_path}")

    contents = json.loads(contents_path.read_text(encoding="utf-8"))
    if contents["properties"]["preserves-vector-representation"] is not True:
        raise SystemExit("[FAIL] iOS Contents.json does not preserve vector representation")
    if contents["images"] != [{"idiom": "universal", "filename": "check.pdf"}]:
        raise SystemExit(f"[FAIL] unexpected iOS images payload: {contents['images']!r}")


def test_ios_placeholder_manifest(temp_root: Path) -> None:
    case_dir = temp_root / "ios-placeholder-case"
    svg_dir = case_dir / "svg-masters"
    xcassets_dir = case_dir / "ios" / "Assets.xcassets"
    svg_dir.mkdir(parents=True)
    (svg_dir / "later.svg").write_text(SIMPLE_SVG, encoding="utf-8")

    result = run_exporter(
        str(svg_dir),
        "--platform",
        "ios",
        "--ios-xcassets",
        str(xcassets_dir),
        "--ios-placeholder-manifest",
    )
    assert_success(result, "iOS placeholder export")

    imageset = xcassets_dir / "later.imageset"
    contents_path = imageset / "Contents.json"
    todo_path = imageset / "TODO.md"
    if not contents_path.exists():
        raise SystemExit(f"[FAIL] missing placeholder Contents.json: {contents_path}")
    if not todo_path.exists():
        raise SystemExit(f"[FAIL] missing placeholder TODO.md: {todo_path}")

    contents = json.loads(contents_path.read_text(encoding="utf-8"))
    if contents["properties"]["preserves-vector-representation"] is not True:
        raise SystemExit("[FAIL] placeholder does not preserve vector representation")
    if contents["images"] != [{"idiom": "universal"}]:
        raise SystemExit(
            f"[FAIL] placeholder should not pretend a PDF exists: {contents['images']!r}"
        )
    if "did not convert" not in todo_path.read_text(encoding="utf-8"):
        raise SystemExit("[FAIL] placeholder TODO does not state that conversion did not happen")


def test_unsupported_feature_fails(temp_root: Path) -> None:
    svg_dir = temp_root / "unsupported-case" / "svg-masters"
    drawable_dir = temp_root / "unsupported-case" / "res" / "drawable"
    svg_dir.mkdir(parents=True)
    (svg_dir / "bad.svg").write_text(UNSUPPORTED_SVG, encoding="utf-8")

    result = run_exporter(
        str(svg_dir),
        "--platform",
        "android",
        "--android-out",
        str(drawable_dir),
    )
    assert_failure(result, "unsupported SVG export")
    if "unsupported SVG feature <text>" not in (result.stdout + result.stderr):
        raise SystemExit(
            "[FAIL] unsupported SVG error did not mention <text>\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def test_ignore_non_path_flag(temp_root: Path) -> None:
    svg_dir = temp_root / "ignore-non-path-case" / "svg-masters"
    drawable_dir = temp_root / "ignore-non-path-case" / "res" / "drawable"
    svg_dir.mkdir(parents=True)
    (svg_dir / "with-rect.svg").write_text(NON_PATH_WITH_PATH_SVG, encoding="utf-8")

    result = run_exporter(
        str(svg_dir),
        "--platform",
        "android",
        "--android-out",
        str(drawable_dir),
        "--ignore-non-path",
    )
    assert_success(result, "ignore non-path export")
    if "unsupported non-path primitive <ellipse>; ignored" not in result.stderr:
        raise SystemExit(
            "[FAIL] ignore non-path export did not warn about ignored ellipse\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    output = drawable_dir / "with_rect.xml"
    root = ET.parse(output).getroot()
    paths = root.findall("path")
    if len(paths) != 1:
        raise SystemExit(f"[FAIL] expected one exported path after ignoring ellipse, got {len(paths)}")


def test_simple_primitive_export(temp_root: Path) -> None:
    svg_dir = temp_root / "primitive-case" / "svg-masters"
    drawable_dir = temp_root / "primitive-case" / "res" / "drawable"
    svg_dir.mkdir(parents=True)
    (svg_dir / "plan.svg").write_text(PRIMITIVE_SVG, encoding="utf-8")

    result = run_exporter(
        str(svg_dir),
        "--platform",
        "android",
        "--android-out",
        str(drawable_dir),
        "--android-tint",
        "?attr/colorControlNormal",
    )
    assert_success(result, "simple primitive Android export")

    root = ET.parse(drawable_dir / "plan.xml").getroot()
    paths = root.findall("path")
    if len(paths) != 3:
        raise SystemExit(f"[FAIL] expected 3 primitive-derived paths, got {len(paths)}")
    if not paths[0].get(android_attr("pathData"), "").startswith("M7.25 4.75 H16.75"):
        raise SystemExit("[FAIL] rounded rect was not converted to expected path data")
    if "A1 1" not in paths[1].get(android_attr("pathData"), ""):
        raise SystemExit("[FAIL] circle was not converted to arc path data")
    if paths[2].get(android_attr("strokeLineCap")) != "round":
        raise SystemExit("[FAIL] line stroke-linecap was not preserved")


def test_current_color_export(temp_root: Path) -> None:
    svg_dir = temp_root / "current-color-case" / "svg-masters"
    drawable_dir = temp_root / "current-color-case" / "res" / "drawable"
    svg_dir.mkdir(parents=True)
    (svg_dir / "template.svg").write_text(CURRENT_COLOR_SVG, encoding="utf-8")

    result = run_exporter(
        str(svg_dir),
        "--platform",
        "android",
        "--android-out",
        str(drawable_dir),
        "--android-tint",
        "?attr/colorControlNormal",
    )
    assert_success(result, "currentColor Android export")
    if "converted fill=currentColor to #000000" not in result.stderr:
        raise SystemExit("[FAIL] currentColor conversion warning missing")

    root = ET.parse(drawable_dir / "template.xml").getroot()
    path = root.find("path")
    if path is None:
        raise SystemExit("[FAIL] currentColor export missing path")
    if path.get(android_attr("fillColor")) != "#000000":
        raise SystemExit("[FAIL] currentColor fill was not converted to #000000")
    if path.get(android_attr("strokeColor")) != "#000000":
        raise SystemExit("[FAIL] currentColor stroke was not converted to #000000")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mobile-icon-platform-export-") as temp:
        temp_root = Path(temp)
        test_android_export(temp_root)
        test_ios_export(temp_root)
        test_ios_placeholder_manifest(temp_root)
        test_unsupported_feature_fails(temp_root)
        test_ignore_non_path_flag(temp_root)
        test_simple_primitive_export(temp_root)
        test_current_color_export(temp_root)

    print("[OK] Platform export smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
