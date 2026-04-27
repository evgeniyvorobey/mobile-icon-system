#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLDER = ROOT / "scripts" / "init_icon_system_package.py"
TEMPLATE_ROOT = ROOT / "assets" / "package-template"
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")
VERSION_RE = re.compile(r"^version:\s*(.+)$", re.MULTILINE)

EXPECTED_DIRS = [
    "concepts",
    "selected",
    "exports",
    "exports/svg-masters",
    "exports/ios",
    "exports/ios/pdf",
    "exports/android",
    "exports/android/vector-drawables",
    "reviews",
]


def read_skill_version() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = VERSION_RE.search(text)
    if not match:
        raise SystemExit("[FAIL] SKILL.md has no version field")
    return match.group(1).strip()


def expected_template_files() -> list[Path]:
    return sorted(
        path.relative_to(TEMPLATE_ROOT)
        for path in TEMPLATE_ROOT.rglob("*")
        if path.is_file()
    )


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
            "2026-04-27",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"[FAIL] Expected path to exist: {path}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mobile-icon-system-package-") as temp:
        output_dir = Path(temp) / "icon-system"
        result = run_scaffolder(output_dir)
        if result.returncode != 0:
            raise SystemExit(
                "[FAIL] package scaffold command failed\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )

        for dirname in EXPECTED_DIRS:
            directory = output_dir / dirname
            assert_exists(directory)
            if not directory.is_dir():
                raise SystemExit(f"[FAIL] Expected directory: {directory}")

        expected_files = expected_template_files()
        for relative_path in expected_files:
            assert_exists(output_dir / relative_path)

        created_files = sorted(path for path in output_dir.rglob("*") if path.is_file())
        if len(created_files) != len(expected_files):
            raise SystemExit(
                "[FAIL] Unexpected scaffold file count: "
                f"expected {len(expected_files)}, got {len(created_files)}"
            )

        unresolved: list[str] = []
        missing_replacements: list[str] = []
        expected_version = read_skill_version()
        for file_path in created_files:
            text = file_path.read_text(encoding="utf-8")
            matches = PLACEHOLDER_RE.findall(text)
            if matches:
                unresolved.append(
                    f"{file_path.relative_to(output_dir)} -> {', '.join(sorted(set(matches)))}"
                )
            if "Project:" in text and "Project: Smoke Project" not in text:
                missing_replacements.append(f"{file_path.relative_to(output_dir)} project")
            if "Owner:" in text and "Owner: QA Team" not in text:
                missing_replacements.append(f"{file_path.relative_to(output_dir)} owner")
            if "Date:" in text and "Date: 2026-04-27" not in text:
                missing_replacements.append(f"{file_path.relative_to(output_dir)} date")
            if "Skill version:" in text and f"Skill version: {expected_version}" not in text:
                missing_replacements.append(f"{file_path.relative_to(output_dir)} version")

        if unresolved:
            raise SystemExit(
                "[FAIL] Unresolved template placeholders found:\n"
                + "\n".join(unresolved)
            )
        if missing_replacements:
            raise SystemExit(
                "[FAIL] Expected replacements missing:\n"
                + "\n".join(missing_replacements)
            )

        if "Created icon-system package" not in result.stdout:
            raise SystemExit("[FAIL] Scaffold command did not print success summary")

    print("[OK] Package scaffold smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
