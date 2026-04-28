#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLDER = ROOT / "scripts" / "scaffold_design_tool_handoff.py"
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")

EXPECTED_FILES = [
    "asset-manifest.csv",
    "code-connect-map.md",
    "figma-writeback-plan.md",
    "pencil-writeback-plan.md",
    "verification-checklist.md",
]


def run_scaffolder(output_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCAFFOLDER),
            str(output_dir),
            "--project-name",
            "Smoke Project",
            "--owner",
            "QA Team",
            "--date",
            "2026-04-28",
            "--handoff-mode",
            "mixed",
            "--figma-file-url",
            "https://www.figma.com/design/ABC123/Smoke",
            "--figma-node-url",
            "https://www.figma.com/design/ABC123/Smoke?node-id=1-2",
            "--pencil-document",
            "design/source.pen",
            "--code-root",
            "src/components/icons",
            "--assets",
            "exports/svg-masters/home.svg,exports/svg-masters/search.svg",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"[FAIL] Expected path to exist: {path}")


def assert_command_failed_on_non_empty_dir(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    existing_file = output_dir / "existing.txt"
    existing_file.write_text("keep me", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCAFFOLDER), str(output_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        raise SystemExit("[FAIL] Scaffolder wrote into a non-empty dir without --force")
    if existing_file.read_text(encoding="utf-8") != "keep me":
        raise SystemExit("[FAIL] Non-empty dir protection changed an existing file")
    if "Output directory is not empty" not in result.stderr:
        raise SystemExit("[FAIL] Non-empty dir error did not explain the protection")


def assert_no_unresolved_placeholders(output_dir: Path) -> None:
    unresolved: list[str] = []
    for file_path in sorted(output_dir.rglob("*")):
        if not file_path.is_file():
            continue
        text = file_path.read_text(encoding="utf-8")
        matches = PLACEHOLDER_RE.findall(text)
        if matches:
            unresolved.append(
                f"{file_path.relative_to(output_dir)} -> {', '.join(sorted(set(matches)))}"
            )

    if unresolved:
        raise SystemExit(
            "[FAIL] Unresolved template placeholders found:\n" + "\n".join(unresolved)
        )


def assert_replacements(output_dir: Path) -> None:
    expected_fragments = (
        "Project: Smoke Project",
        "Owner: QA Team",
        "Date: 2026-04-28",
        "Planned handoff mode: mixed",
        "This script does not call Figma or Pencil MCP",
    )
    for file_name in (
        "code-connect-map.md",
        "figma-writeback-plan.md",
        "pencil-writeback-plan.md",
        "verification-checklist.md",
    ):
        text = (output_dir / file_name).read_text(encoding="utf-8")
        for fragment in expected_fragments:
            if fragment not in text:
                raise SystemExit(f"[FAIL] Missing replacement in {file_name}: {fragment}")


def assert_manifest(output_dir: Path) -> None:
    manifest_path = output_dir / "asset-manifest.csv"
    rows = list(csv.DictReader(manifest_path.open(encoding="utf-8")))
    if len(rows) != 2:
        raise SystemExit(f"[FAIL] Expected 2 manifest rows, got {len(rows)}")

    asset_ids = {row["asset_id"] for row in rows}
    if asset_ids != {"home", "search"}:
        raise SystemExit(f"[FAIL] Unexpected manifest asset IDs: {sorted(asset_ids)}")

    for row in rows:
        if row["status"] != "planned":
            raise SystemExit(f"[FAIL] Manifest row is not marked planned: {row}")
        if row["format"] != "SVG":
            raise SystemExit(f"[FAIL] Manifest row did not infer SVG format: {row}")


def assert_no_fake_mcp_claims(output_dir: Path) -> None:
    figma_plan = (output_dir / "figma-writeback-plan.md").read_text(encoding="utf-8")
    pencil_plan = (output_dir / "pencil-writeback-plan.md").read_text(encoding="utf-8")
    checklist = (output_dir / "verification-checklist.md").read_text(encoding="utf-8")

    if "Actual Figma MCP call performed: No" not in figma_plan:
        raise SystemExit("[FAIL] Figma plan does not mark MCP calls as not performed")
    if "Actual Pencil MCP call performed: No" not in pencil_plan:
        raise SystemExit("[FAIL] Pencil plan does not mark MCP calls as not performed")
    if "No Figma write-back claim is made unless an actual Figma MCP call is logged" not in checklist:
        raise SystemExit("[FAIL] Checklist does not enforce Figma provenance honesty")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="design-tool-handoff-") as temp:
        temp_dir = Path(temp)
        output_dir = temp_dir / "handoff"
        result = run_scaffolder(output_dir)
        if result.returncode != 0:
            raise SystemExit(
                "[FAIL] design-tool handoff scaffold command failed\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )

        for file_name in EXPECTED_FILES:
            file_path = output_dir / file_name
            assert_exists(file_path)
            if not file_path.is_file():
                raise SystemExit(f"[FAIL] Expected file: {file_path}")

        created_files = sorted(
            str(path.relative_to(output_dir))
            for path in output_dir.rglob("*")
            if path.is_file()
        )
        if created_files != EXPECTED_FILES:
            raise SystemExit(
                "[FAIL] Unexpected scaffold files:\n" + "\n".join(created_files)
            )

        assert_no_unresolved_placeholders(output_dir)
        assert_replacements(output_dir)
        assert_manifest(output_dir)
        assert_no_fake_mcp_claims(output_dir)
        assert_command_failed_on_non_empty_dir(temp_dir / "blocked")

        if "Created design-tool handoff package" not in result.stdout:
            raise SystemExit("[FAIL] Scaffold command did not print success summary")

    print("[OK] Design-tool handoff scaffold smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
