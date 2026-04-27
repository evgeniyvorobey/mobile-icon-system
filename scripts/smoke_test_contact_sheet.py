#!/usr/bin/env python3
"""Smoke test for the icon contact sheet renderer.

Generates a small set of dummy icon SVGs (filled + outlined pairs and a
singleton) into a temp directory, then runs render_icon_contact_sheet.py
against the directory and verifies key markers in the output HTML.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_icon_contact_sheet.py"


DUMMY_FILLED = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" fill="#000"/></svg>"""
DUMMY_OUTLINED = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" fill="none" stroke="#000" stroke-width="1.75"/></svg>"""
DUMMY_SINGLETON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="#000"/></svg>"""


def write_dummy_set(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "ic_tab_home_filled.svg").write_text(DUMMY_FILLED, encoding="utf-8")
    (directory / "ic_tab_home_outlined.svg").write_text(DUMMY_OUTLINED, encoding="utf-8")
    (directory / "ic_tab_search_filled.svg").write_text(DUMMY_FILLED, encoding="utf-8")
    (directory / "ic_tab_search_outlined.svg").write_text(DUMMY_OUTLINED, encoding="utf-8")
    (directory / "ic_action_share.svg").write_text(DUMMY_SINGLETON, encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mobile-icon-system-contact-") as temp:
        svg_dir = Path(temp) / "icons"
        write_dummy_set(svg_dir)

        output = Path(temp) / "icon-contact-sheet.html"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(svg_dir),
                "--output",
                str(output),
                "--title",
                "Smoke Icon Contact Sheet",
                "--sizes",
                "16,20,24,32",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            raise SystemExit(
                "[FAIL] contact sheet command failed\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )
        if not output.exists():
            raise SystemExit(f"[FAIL] Expected contact sheet to exist: {output}")

        html = output.read_text(encoding="utf-8")
        required = [
            "Smoke Icon Contact Sheet",
            "ic_tab_home",
            "ic_tab_search",
            "ic_action_share",
            "Icon Size Grid",
            "Surface Mockups",
            "iOS Tab Bar (light)",
            "Android Bottom Nav (light)",
            "data:image/svg+xml;base64,",
            "data-review-img",
            "data-grid=\"size-grid\"",
            "data-surface=\"ios\"",
            "data-surface=\"android\"",
            "20pt",
            "filled",
            "outlined",
        ]
        missing = [marker for marker in required if marker not in html]
        if missing:
            raise SystemExit(
                "[FAIL] Contact sheet missing expected markers:\n"
                + "\n".join(missing)
            )

    print("[OK] Icon contact sheet smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
