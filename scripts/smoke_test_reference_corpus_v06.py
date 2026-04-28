#!/usr/bin/env python3
"""Smoke test the v0.6 custom reference corpus."""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "assets" / "references" / "custom-v06"
README = ROOT / "assets" / "references" / "README.md"

PLACEHOLDER_RE = re.compile(
    r"(\bTODO\b|\bFIXME\b|\bTBD\b|\bPLACEHOLDER\b|\bCHANGEME\b|\{\{)",
    re.IGNORECASE,
)

REQUIRED_NOTE_PHRASES = [
    "Path data / structure observations",
    "What a generator should learn",
    "Licensing / provenance",
    "Original repo-authored",
]


def display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{display(path)} is not valid UTF-8: {exc}")
    except OSError as exc:
        fail(f"could not read {display(path)}: {exc}")


def check_no_placeholders(paths: list[Path]) -> None:
    for path in paths:
        text = read_text(path)
        match = PLACEHOLDER_RE.search(text)
        if match:
            fail(f"{display(path)} contains unresolved placeholder {match.group(0)!r}")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_svg(path: Path) -> ET.Element:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        fail(f"{display(path)} is not parseable SVG XML: {exc}")

    if local_name(root.tag) != "svg":
        fail(f"{display(path)} root element is not <svg>")
    if not root.get("viewBox"):
        fail(f"{display(path)} is missing viewBox")
    return root


def parse_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        fail(f"{display(path)} is not parseable JSON at line {exc.lineno}: {exc.msg}")

    if not isinstance(data, dict):
        fail(f"{display(path)} root must be a JSON object")
    return data


def note_path_for(asset_path: Path) -> Path:
    return asset_path.with_suffix(".notes.md")


def check_notes(asset_paths: list[Path]) -> None:
    for asset_path in asset_paths:
        notes = note_path_for(asset_path)
        if not notes.exists():
            fail(f"{display(asset_path)} is missing sibling {notes.name}")
        text = read_text(notes)
        for phrase in REQUIRED_NOTE_PHRASES:
            if phrase not in text:
                fail(f"{display(notes)} missing required phrase: {phrase}")
        if "Upstream URL:" not in text or "N/A" not in text:
            fail(f"{display(notes)} must declare that no upstream URL was used")


def check_required_anchors(svg_paths: list[Path], json_paths: list[Path]) -> None:
    names = {path.name for path in svg_paths + json_paths}
    required = {
        "pixel-bolt-16.svg",
        "isometric-cube-24.svg",
        "jitter-pencil-24.svg",
        "motion-pulse-static.svg",
        "motion-pulse.json",
    }
    missing = sorted(required - names)
    if missing:
        fail(f"custom-v06 is missing required anchors: {', '.join(missing)}")


def check_motion_json(path: Path, data: dict[str, Any]) -> None:
    for key in ("v", "fr", "ip", "op", "w", "h", "layers"):
        if key not in data:
            fail(f"{display(path)} missing required motion field {key!r}")
    if not isinstance(data["layers"], list) or not data["layers"]:
        fail(f"{display(path)} must contain at least one Lottie layer")
    if data.get("assets") not in (None, []):
        fail(f"{display(path)} must not reference external assets")

    meta = data.get("meta")
    if not isinstance(meta, dict):
        fail(f"{display(path)} missing meta object")
    fallback = meta.get("reduced_motion_fallback")
    if not isinstance(fallback, str) or not fallback:
        fail(f"{display(path)} missing meta.reduced_motion_fallback")
    fallback_path = path.with_name(fallback)
    if not fallback_path.exists():
        fail(f"{display(path)} fallback does not exist: {fallback}")


def check_readmes() -> None:
    if not README.exists():
        fail(f"{display(README)} does not exist")
    readme_text = read_text(README)
    if "custom-v06" not in readme_text:
        fail(f"{display(README)} must mention custom-v06")
    if "upstream-fetched" not in readme_text:
        fail(f"{display(README)} must distinguish custom-v06 from upstream-fetched material")

    local_readme = CORPUS_DIR / "README.md"
    if not local_readme.exists():
        fail(f"{display(local_readme)} does not exist")
    local_text = read_text(local_readme)
    if "additive v0.6 calibration corpus" not in local_text:
        fail(f"{display(local_readme)} must identify the v0.6 additive corpus")


def main() -> int:
    if not CORPUS_DIR.is_dir():
        fail(f"{display(CORPUS_DIR)} does not exist")

    svg_paths = sorted(CORPUS_DIR.glob("*.svg"))
    json_paths = sorted(CORPUS_DIR.glob("*.json"))
    note_paths = sorted(CORPUS_DIR.glob("*.notes.md"))
    markdown_paths = sorted(CORPUS_DIR.glob("*.md")) + [README]
    all_checked_text = svg_paths + json_paths + markdown_paths

    if not svg_paths:
        fail("custom-v06 contains no SVG assets")
    if not json_paths:
        fail("custom-v06 contains no JSON motion assets")

    check_required_anchors(svg_paths, json_paths)
    check_no_placeholders(all_checked_text)

    for svg_path in svg_paths:
        parse_svg(svg_path)

    for json_path in json_paths:
        data = parse_json(json_path)
        check_motion_json(json_path, data)

    check_notes(svg_paths + json_paths)
    check_readmes()

    unused_notes = sorted(set(note_paths) - {note_path_for(path) for path in svg_paths + json_paths})
    if unused_notes:
        fail("notes without matching asset: " + ", ".join(display(path) for path in unused_notes))

    print(
        "[OK] v0.6 custom reference corpus smoke test passed "
        f"({len(svg_paths)} SVG, {len(json_paths)} JSON)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
