#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "assets" / "package-template"
_VERSION_RE = re.compile(r"^version:\s*(.+)$", re.MULTILINE)


def read_skill_version() -> str:
    skill_path = ROOT / "SKILL.md"
    if not skill_path.exists():
        return "unknown"
    text = skill_path.read_text(encoding="utf-8")
    match = _VERSION_RE.search(text)
    return match.group(1).strip() if match else "unknown"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a mobile icon system handoff package."
    )
    parser.add_argument(
        "output_dir",
        help="Directory where the icon-system package should be created.",
    )
    parser.add_argument(
        "--project-name",
        default="Untitled Project",
        help="Project name to insert into template files.",
    )
    parser.add_argument(
        "--owner",
        default="Unassigned",
        help="Owner or team label to insert into template files.",
    )
    parser.add_argument(
        "--date",
        dest="package_date",
        default=date.today().isoformat(),
        help="Date to insert into template files (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow writing into a non-empty output directory.",
    )
    return parser.parse_args()


def ensure_output_dir(path: Path, force: bool) -> None:
    if path.exists():
        if any(path.iterdir()) and not force:
            raise SystemExit(
                f"Output directory is not empty: {path}\n"
                "Use --force to scaffold into a non-empty directory."
            )
        return
    path.mkdir(parents=True, exist_ok=True)


def create_base_dirs(path: Path) -> None:
    for name in (
        "concepts",
        "selected",
        "exports",
        "exports/svg-masters",
        "exports/ios",
        "exports/ios/pdf",
        "exports/android",
        "exports/android/vector-drawables",
        "reviews",
    ):
        (path / name).mkdir(parents=True, exist_ok=True)


def render_template(text: str, project_name: str, owner: str, package_date: str, skill_version: str) -> str:
    return (
        text.replace("{{PROJECT_NAME}}", project_name)
        .replace("{{OWNER}}", owner)
        .replace("{{DATE}}", package_date)
        .replace("{{SKILL_VERSION}}", skill_version)
    )


def copy_templates(output_dir: Path, project_name: str, owner: str, package_date: str, skill_version: str) -> list[Path]:
    created_files: list[Path] = []
    for template_path in sorted(TEMPLATE_ROOT.rglob("*")):
        if template_path.is_dir():
            continue
        relative_path = template_path.relative_to(TEMPLATE_ROOT)
        target_path = output_dir / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)

        rendered = render_template(
            template_path.read_text(encoding="utf-8"),
            project_name=project_name,
            owner=owner,
            package_date=package_date,
            skill_version=skill_version,
        )
        target_path.write_text(rendered, encoding="utf-8")
        created_files.append(target_path)
    return created_files


def main() -> int:
    args = parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    if not TEMPLATE_ROOT.exists():
        print(f"Template root not found: {TEMPLATE_ROOT}", file=sys.stderr)
        return 1

    skill_version = read_skill_version()

    ensure_output_dir(output_dir, force=args.force)
    create_base_dirs(output_dir)
    created_files = copy_templates(
        output_dir,
        project_name=args.project_name,
        owner=args.owner,
        package_date=args.package_date,
        skill_version=skill_version,
    )

    print(f"Created icon-system package (skill v{skill_version}) at {output_dir}")
    for file_path in created_files:
        print(f"- {file_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
