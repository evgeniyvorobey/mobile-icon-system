#!/usr/bin/env python3
"""End-to-end smoke test: run render_and_grade.py against a small icon set."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_and_grade.py"


HOME_FILLED = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<polygon points="3,12 12,3 21,12 19,12 19,21 5,21 5,12" fill="#000"/></svg>'
)
HOME_OUTLINED = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<polygon points="3,12 12,3 21,12 19,12 19,21 5,21 5,12" '
    'fill="none" stroke="#000" stroke-width="2"/></svg>'
)
SEARCH = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<circle cx="11" cy="11" r="6" fill="none" stroke="#000" stroke-width="2"/>'
    '<line x1="16" y1="16" x2="21" y2="21" stroke="#000" stroke-width="2" '
    'stroke-linecap="round"/></svg>'
)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mobile-icon-system-grade-") as temp:
        svg_dir = Path(temp) / "icons"
        svg_dir.mkdir(parents=True)
        (svg_dir / "ic_tab_home_filled.svg").write_text(HOME_FILLED, encoding="utf-8")
        (svg_dir / "ic_tab_home_outlined.svg").write_text(HOME_OUTLINED, encoding="utf-8")
        (svg_dir / "ic_action_search.svg").write_text(SEARCH, encoding="utf-8")

        report_md = Path(temp) / "report.md"
        report_json = Path(temp) / "report.json"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(svg_dir),
                "--report-md",
                str(report_md),
                "--report-json",
                str(report_json),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode == 2:
            print(
                "[FAIL] render_and_grade.py returned hard fail\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )
            return 1
        if not report_md.exists() or not report_json.exists():
            print(f"[FAIL] reports missing (md={report_md.exists()}, json={report_json.exists()})")
            return 1

        report = json.loads(report_json.read_text(encoding="utf-8"))
        names = {icon["name"] for icon in report["icons"]}
        expected = {"ic_tab_home_filled.svg", "ic_tab_home_outlined.svg", "ic_action_search.svg"}
        if names != expected:
            print(f"[FAIL] icons in report mismatch: {names}")
            return 1
        non_ok = [i for i in report["icons"] if i["verdict"] != "ok"]
        if non_ok:
            print(
                "[FAIL] expected all end-to-end fixture icons to verdict=ok, "
                f"non-ok: {[(i['name'], i['verdict'], i['warnings'], i['errors']) for i in non_ok]}"
            )
            return 1

    print("[OK] grade end-to-end smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
