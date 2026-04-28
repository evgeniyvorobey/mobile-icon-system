#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DEMO_ROOT = ROOT / "assets" / "demo-package"
SVG_DIR = DEMO_ROOT / "exports" / "svg-masters"
CONTACT_SHEET = ROOT / "scripts" / "render_icon_contact_sheet.py"

PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
SVG_NS = "{http://www.w3.org/2000/svg}"

EXPECTED_FILES = [
    "README.md",
    "brand-dna.md",
    "system-rules.md",
    "vocabulary.md",
    "package-notes.md",
    "selected/rationale.md",
    "reviews/scorecard.md",
    "exports/svg-masters/ic_action_capture.svg",
    "exports/svg-masters/ic_tab_plan_filled.svg",
    "exports/svg-masters/ic_tab_plan_outlined.svg",
    "exports/svg-masters/ic_tab_today_filled.svg",
    "exports/svg-masters/ic_tab_today_outlined.svg",
]

EXPECTED_SVGS = [
    "ic_action_capture.svg",
    "ic_tab_plan_filled.svg",
    "ic_tab_plan_outlined.svg",
    "ic_tab_today_filled.svg",
    "ic_tab_today_outlined.svg",
]


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def assert_expected_files() -> None:
    for relative in EXPECTED_FILES:
        path = DEMO_ROOT / relative
        if not path.exists():
            fail(f"Expected demo package file to exist: {path}")
        if not path.is_file():
            fail(f"Expected demo package path to be a file: {path}")

    actual_svgs = sorted(path.name for path in SVG_DIR.glob("*.svg"))
    if actual_svgs != sorted(EXPECTED_SVGS):
        fail(
            "Unexpected SVG master set:\n"
            f"expected: {', '.join(sorted(EXPECTED_SVGS))}\n"
            f"actual: {', '.join(actual_svgs)}"
        )


def assert_no_placeholders() -> None:
    unresolved: list[str] = []
    for path in sorted(DEMO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        matches = sorted(set(PLACEHOLDER_RE.findall(text)))
        if matches:
            unresolved.append(
                f"{path.relative_to(DEMO_ROOT)} -> {', '.join(matches)}"
            )

    if unresolved:
        fail("Unresolved placeholders found:\n" + "\n".join(unresolved))


def local_name(tag: str) -> str:
    if tag.startswith("{"):
        return tag.rsplit("}", 1)[1]
    return tag


def parse_svg(path: Path) -> ET.Element:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        fail(f"SVG failed XML parse: {path}: {exc}")

    if root.tag not in {f"{SVG_NS}svg", "svg"}:
        fail(f"Expected SVG root element in {path}, got {root.tag!r}")
    if root.get("viewBox") != "0 0 24 24":
        fail(f"Expected 24 by 24 viewBox in {path}")
    return root


def assert_svg_hygiene() -> None:
    for path in sorted(SVG_DIR.glob("*.svg")):
        root = parse_svg(path)
        serialized = path.read_text(encoding="utf-8")
        if "currentColor" not in serialized:
            fail(f"Expected tintable currentColor usage in {path}")

        for element in root.iter():
            if local_name(element.tag) == "image":
                fail(f"External raster/image element is not allowed in {path}")
            for attr_name, attr_value in element.attrib.items():
                if local_name(attr_name) == "href" and attr_value.startswith(
                    ("http://", "https://", "file:")
                ):
                    fail(f"External href is not allowed in {path}: {attr_value}")


def run_contact_sheet() -> None:
    with tempfile.TemporaryDirectory(prefix="mobile-icon-demo-package-") as temp:
        output = Path(temp) / "demo-contact-sheet.html"
        result = subprocess.run(
            [
                sys.executable,
                str(CONTACT_SHEET),
                str(SVG_DIR),
                "--output",
                str(output),
                "--title",
                "Tidepool Tasks Demo Contact Sheet",
                "--sizes",
                "16,20,24,32",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            fail(
                "contact sheet command failed\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )
        if not output.exists():
            fail(f"Expected contact sheet to exist: {output}")

        html = output.read_text(encoding="utf-8")
        required_markers = [
            "Tidepool Tasks Demo Contact Sheet",
            "ic_action_capture",
            "ic_tab_plan",
            "ic_tab_today",
            "Icon Size Grid",
            "Surface Mockups",
            "data-grid=\"size-grid\"",
            "data-surface=\"ios\"",
            "data-surface=\"android\"",
            "data:image/svg+xml;base64,",
        ]
        missing = [marker for marker in required_markers if marker not in html]
        if missing:
            fail(
                "Contact sheet missing expected markers:\n"
                + "\n".join(missing)
            )


def main() -> int:
    assert_expected_files()
    assert_no_placeholders()
    assert_svg_hygiene()
    run_contact_sheet()
    print("[OK] Demo package smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
