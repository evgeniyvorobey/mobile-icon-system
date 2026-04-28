#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import date
from io import StringIO
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "assets" / "design-tool-handoff-template"
_VERSION_RE = re.compile(r"^version:\s*(.+)$", re.MULTILINE)
ASSET_SUFFIXES = {
    ".svg",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".xml",
    ".json",
}


def read_skill_version() -> str:
    skill_path = ROOT / "SKILL.md"
    if not skill_path.exists():
        return "unknown"
    text = skill_path.read_text(encoding="utf-8")
    match = _VERSION_RE.search(text)
    return match.group(1).strip() if match else "unknown"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a safe design-tool handoff and write-back plan."
    )
    parser.add_argument(
        "output_dir",
        help="Directory where the design-tool handoff folder should be created.",
    )
    parser.add_argument(
        "--project-name",
        default="Untitled Project",
        help="Project name to insert into handoff files.",
    )
    parser.add_argument(
        "--owner",
        default="Unassigned",
        help="Owner or team label to insert into handoff files.",
    )
    parser.add_argument(
        "--date",
        dest="handoff_date",
        default=date.today().isoformat(),
        help="Date to insert into handoff files (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--handoff-mode",
        choices=("figma", "pencil", "code-connect", "filesystem", "mixed"),
        default="mixed",
        help="Planned handoff mode. This does not verify that any tool is connected.",
    )
    parser.add_argument(
        "--figma-file-url",
        default="",
        help="Target Figma file URL for the write-back plan.",
    )
    parser.add_argument(
        "--figma-node-url",
        default="",
        help="Target Figma node or page URL for the write-back plan.",
    )
    parser.add_argument(
        "--pencil-document",
        default="",
        help="Target Pencil `.pen` document path or label for the write-back plan.",
    )
    parser.add_argument(
        "--code-root",
        default="",
        help="Repository path where mapped code components live.",
    )
    parser.add_argument(
        "--asset-dir",
        default="",
        help="Optional directory of exported assets to seed asset-manifest.csv.",
    )
    parser.add_argument(
        "--assets",
        default="",
        help="Comma-separated asset paths to seed asset-manifest.csv.",
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


def optional_value(value: str, fallback: str = "Not provided") -> str:
    stripped = value.strip()
    return stripped if stripped else fallback


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "asset"


def split_csv_values(raw_value: str) -> list[str]:
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def resolve_asset_dir(raw_path: str) -> Path | None:
    if not raw_path.strip():
        return None

    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    if not path.exists():
        raise SystemExit(f"Asset directory does not exist: {path}")
    if not path.is_dir():
        raise SystemExit(f"Asset path is not a directory: {path}")
    return path


def collect_asset_paths(raw_assets: str, asset_dir: Path | None) -> list[Path]:
    collected: list[Path] = []
    seen: set[str] = set()

    for raw_path in split_csv_values(raw_assets):
        path = Path(raw_path).expanduser()
        if not path.is_absolute():
            path = (Path.cwd() / path).resolve()
        key = str(path)
        if key not in seen:
            collected.append(path)
            seen.add(key)

    if asset_dir is not None:
        for path in sorted(asset_dir.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in ASSET_SUFFIXES:
                continue
            key = str(path.resolve())
            if key not in seen:
                collected.append(path)
                seen.add(key)

    return collected


def build_manifest_rows(raw_assets: str, asset_dir: Path | None) -> str:
    output = StringIO()
    writer = csv.writer(output, lineterminator="\n")
    asset_paths = collect_asset_paths(raw_assets, asset_dir)

    if asset_paths:
        for asset_path in asset_paths:
            suffix = asset_path.suffix.lower().lstrip(".") or "unknown"
            writer.writerow(
                [
                    slugify(asset_path.stem),
                    display_path(asset_path),
                    "shared",
                    suffix.upper(),
                    "TODO",
                    "TODO",
                    "TODO Figma component",
                    "TODO Pencil node",
                    "TODO code component",
                    "planned",
                    "Verify before write-back",
                ]
            )
    else:
        writer.writerow(
            [
                "TODO-icon",
                "TODO: exports/svg-masters/icon.svg",
                "TODO",
                "TODO",
                "TODO",
                "TODO",
                "TODO Figma component",
                "TODO Pencil node",
                "TODO code component",
                "planned",
                "Replace with exported asset before handoff",
            ]
        )

    return output.getvalue().rstrip("\n")


def render_text(text: str, values: dict[str, str]) -> str:
    rendered = text
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def template_values(
    args: argparse.Namespace, skill_version: str, asset_dir: Path | None
) -> dict[str, str]:
    asset_source = optional_value(args.asset_dir or args.assets)
    return {
        "PROJECT_NAME": args.project_name,
        "OWNER": args.owner,
        "DATE": args.handoff_date,
        "SKILL_VERSION": skill_version,
        "HANDOFF_MODE": args.handoff_mode,
        "FIGMA_FILE_URL": optional_value(args.figma_file_url),
        "FIGMA_NODE_URL": optional_value(args.figma_node_url),
        "PENCIL_DOCUMENT": optional_value(args.pencil_document),
        "CODE_ROOT": optional_value(args.code_root),
        "ASSET_SOURCE": asset_source,
        "SCAFFOLD_PROVENANCE": (
            "Generated by scaffold_design_tool_handoff.py. "
            "This script does not call Figma or Pencil MCP; all write-back steps "
            "remain planned until actual tool calls are recorded."
        ),
        "MANIFEST_ROWS": build_manifest_rows(args.assets, asset_dir),
    }


def copy_templates(output_dir: Path, values: dict[str, str]) -> list[Path]:
    created_files: list[Path] = []
    for template_path in sorted(TEMPLATE_ROOT.rglob("*")):
        if template_path.is_dir():
            continue

        relative_path = template_path.relative_to(TEMPLATE_ROOT)
        target_path = output_dir / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(
            render_text(template_path.read_text(encoding="utf-8"), values),
            encoding="utf-8",
        )
        created_files.append(target_path)
    return created_files


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()

    if not TEMPLATE_ROOT.exists():
        print(f"Template root not found: {TEMPLATE_ROOT}", file=sys.stderr)
        return 1

    skill_version = read_skill_version()
    asset_dir = resolve_asset_dir(args.asset_dir)
    values = template_values(args, skill_version, asset_dir)

    ensure_output_dir(output_dir, force=args.force)
    created_files = copy_templates(output_dir, values)

    print(f"Created design-tool handoff package (skill v{skill_version}) at {output_dir}")
    for file_path in sorted(created_files):
        print(f"- {file_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
