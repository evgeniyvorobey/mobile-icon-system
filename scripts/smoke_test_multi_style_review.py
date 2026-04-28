#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLDER = ROOT / "scripts" / "init_multi_style_review.py"
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")

EXPECTED_DIRS = [
    "shared",
    "review",
    "style-a",
    "style-a/icons",
    "style-a/renders",
    "style-a/exports",
    "style-b",
    "style-b/icons",
    "style-b/renders",
    "style-b/exports",
    "style-c",
    "style-c/icons",
    "style-c/renders",
    "style-c/exports",
]

EXPECTED_FILES = [
    "shared/brief.md",
    "shared/brand-dna.md",
    "shared/icon-inventory.csv",
    "shared/review-constraints.md",
    "style-a/candidate-brief.md",
    "style-b/candidate-brief.md",
    "style-c/candidate-brief.md",
    "review/contact-sheet.md",
    "review/decision-log.md",
    "review/scorecard.md",
    "review/winner-lock.md",
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
            "--grid",
            "24x24 base / 20x20 live area",
            "--accessibility-tier",
            "WCAG AA",
            "--surfaces",
            "iOS Tab Bar, Android Bottom Nav",
            "--icons",
            "home, search, profile",
            "--style-a",
            "Calm Precision",
            "--style-b",
            "Friendly Weight",
            "--style-c",
            "Editorial Sharp",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def run_scaffolder_with_styles_alias(output_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCAFFOLDER),
            str(output_dir),
            "--project-name",
            "Alias Project",
            "--styles",
            "Liquid Glass,3D Isometric,Hand Drawn",
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
    (output_dir / "existing.txt").write_text("keep me", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCAFFOLDER), str(output_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        raise SystemExit("[FAIL] Scaffolder wrote into a non-empty dir without --force")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="multi-style-review-") as temp:
        temp_dir = Path(temp)
        output_dir = temp_dir / "review"
        result = run_scaffolder(output_dir)
        if result.returncode != 0:
            raise SystemExit(
                "[FAIL] multi-style scaffold command failed\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )

        for dirname in EXPECTED_DIRS:
            directory = output_dir / dirname
            assert_exists(directory)
            if not directory.is_dir():
                raise SystemExit(f"[FAIL] Expected directory: {directory}")

        for filename in EXPECTED_FILES:
            file_path = output_dir / filename
            assert_exists(file_path)
            if not file_path.is_file():
                raise SystemExit(f"[FAIL] Expected file: {file_path}")

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
                "[FAIL] Unresolved template placeholders found:\n"
                + "\n".join(unresolved)
            )

        inventory = (output_dir / "shared" / "icon-inventory.csv").read_text(
            encoding="utf-8"
        )
        for expected in ("home,home", "search,search", "profile,profile"):
            if expected not in inventory:
                raise SystemExit(f"[FAIL] Missing inventory row fragment: {expected}")

        constraints = (output_dir / "shared" / "review-constraints.md").read_text(
            encoding="utf-8"
        )
        for expected in (
            "Same icon inventory",
            "Same locked metaphor",
            "Same base grid",
            "WCAG AA",
            "iOS Tab Bar, Android Bottom Nav",
        ):
            if expected not in constraints:
                raise SystemExit(f"[FAIL] Missing shared constraint: {expected}")

        winner_lock = (output_dir / "review" / "winner-lock.md").read_text(
            encoding="utf-8"
        )
        if "No silent mixing" not in winner_lock:
            raise SystemExit("[FAIL] Winner lock does not block silent style mixing")

        for key, name in (
            ("a", "Calm Precision"),
            ("b", "Friendly Weight"),
            ("c", "Editorial Sharp"),
        ):
            brief = (output_dir / f"style-{key}" / "candidate-brief.md").read_text(
                encoding="utf-8"
            )
            if name not in brief:
                raise SystemExit(f"[FAIL] Missing style name in style-{key} brief")
            if "../shared/icon-inventory.csv" not in brief:
                raise SystemExit(f"[FAIL] style-{key} brief does not reference inventory")

        assert_command_failed_on_non_empty_dir(temp_dir / "blocked")

        alias_dir = temp_dir / "alias-review"
        alias_result = run_scaffolder_with_styles_alias(alias_dir)
        if alias_result.returncode != 0:
            raise SystemExit(
                "[FAIL] --styles alias scaffold command failed\n"
                f"stdout:\n{alias_result.stdout}\n"
                f"stderr:\n{alias_result.stderr}"
            )
        for key, name in (
            ("a", "Liquid Glass"),
            ("b", "3D Isometric"),
            ("c", "Hand Drawn"),
        ):
            brief = (alias_dir / f"style-{key}" / "candidate-brief.md").read_text(
                encoding="utf-8"
            )
            if name not in brief:
                raise SystemExit(f"[FAIL] --styles alias missing {name} in style-{key}")

        if "Created multi-style review package" not in result.stdout:
            raise SystemExit("[FAIL] Scaffold command did not print success summary")

    print("[OK] Multi-style review scaffold smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
