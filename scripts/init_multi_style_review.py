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
TEMPLATE_ROOT = ROOT / "assets" / "multi-style-template"
_VERSION_RE = re.compile(r"^version:\s*(.+)$", re.MULTILINE)

STYLE_KEYS = ("a", "b", "c")
STYLE_LABELS = {"a": "A", "b": "B", "c": "C"}
DEFAULT_STYLE_NAMES = {
    "a": "Calm Precision",
    "b": "Friendly Weight",
    "c": "Editorial Sharp",
}

STYLE_CANDIDATE_TEMPLATE = """# Style {{STYLE_LABEL}} - {{STYLE_NAME}}

Project: {{PROJECT_NAME}}
Owner: {{OWNER}}
Date: {{DATE}}

## Shared Inputs

- Brief: `../shared/brief.md`
- Brand DNA: `../shared/brand-dna.md`
- Inventory: `../shared/icon-inventory.csv`
- Constraints: `../shared/review-constraints.md`

## Candidate Rule Set

- Visual style:
- Stroke or fill model:
- Terminal treatment:
- Corner treatment:
- Color model:
- Detail density:
- Optical correction strength:
- Character:

## Generation Contract

- Generate every row from `../shared/icon-inventory.csv`.
- Preserve the locked metaphor for every icon.
- Use the shared grid, accessibility tier, and target surfaces.
- Use identical filename stems across style A, style B, and style C.
- Do not borrow rules or parts from another style before the winner lock.

## Output Folders

- `icons/`: SVG masters for review.
- `renders/`: rendered previews for the contact sheet.
- `exports/`: review-only platform exports if needed.
"""


def read_skill_version() -> str:
    skill_path = ROOT / "SKILL.md"
    if not skill_path.exists():
        return "unknown"
    text = skill_path.read_text(encoding="utf-8")
    match = _VERSION_RE.search(text)
    return match.group(1).strip() if match else "unknown"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a three-style mobile icon review package."
    )
    parser.add_argument(
        "output_dir",
        help="Directory where the multi-style review package should be created.",
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
        dest="review_date",
        default=date.today().isoformat(),
        help="Date to insert into template files (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--grid",
        default="24x24 base grid / 20x20 live area",
        help="Shared grid and live-area rule for all three styles.",
    )
    parser.add_argument(
        "--accessibility-tier",
        default="WCAG AA",
        help="Shared accessibility tier for all three styles.",
    )
    parser.add_argument(
        "--surfaces",
        default="iOS Tab Bar, Android Bottom Nav, action icons",
        help="Shared target surfaces for all three styles.",
    )
    parser.add_argument(
        "--icons",
        default="",
        help="Comma-separated canonical icon labels for the shared inventory.",
    )
    parser.add_argument(
        "--styles",
        default="",
        help=(
            "Comma-separated display names for style A/B/C. "
            "Overrides --style-a/--style-b/--style-c when exactly three values are provided."
        ),
    )
    parser.add_argument(
        "--style-a",
        default=DEFAULT_STYLE_NAMES["a"],
        help="Display name for style A.",
    )
    parser.add_argument(
        "--style-b",
        default=DEFAULT_STYLE_NAMES["b"],
        help="Display name for style B.",
    )
    parser.add_argument(
        "--style-c",
        default=DEFAULT_STYLE_NAMES["c"],
        help="Display name for style C.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow writing into a non-empty output directory.",
    )
    return parser.parse_args()


def resolve_style_names(args: argparse.Namespace) -> dict[str, str]:
    styles = [item.strip() for item in args.styles.split(",") if item.strip()]
    if args.styles and len(styles) != 3:
        raise SystemExit("--styles must contain exactly three comma-separated names")
    if styles:
        return {"a": styles[0], "b": styles[1], "c": styles[2]}
    return {"a": args.style_a, "b": args.style_b, "c": args.style_c}


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
    for dirname in (
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
    ):
        (path / dirname).mkdir(parents=True, exist_ok=True)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "icon"


def parse_icons(raw_icons: str) -> list[str]:
    return [item.strip() for item in raw_icons.split(",") if item.strip()]


def build_inventory_rows(icon_labels: list[str], surfaces: str) -> str:
    output = StringIO()
    writer = csv.writer(output, lineterminator="\n")

    if icon_labels:
        for label in icon_labels:
            writer.writerow(
                [
                    slugify(label),
                    label,
                    "TODO: locked metaphor",
                    "TODO: states",
                    surfaces,
                ]
            )
    else:
        writer.writerow(
            [
                "TODO",
                "TODO",
                "TODO: locked metaphor",
                "TODO: states",
                surfaces,
            ]
        )

    return output.getvalue().rstrip("\n")


def render_text(text: str, values: dict[str, str]) -> str:
    rendered = text
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def template_values(args: argparse.Namespace, skill_version: str) -> dict[str, str]:
    icon_labels = parse_icons(args.icons)
    style_names = resolve_style_names(args)
    return {
        "PROJECT_NAME": args.project_name,
        "OWNER": args.owner,
        "DATE": args.review_date,
        "SKILL_VERSION": skill_version,
        "GRID": args.grid,
        "ACCESSIBILITY_TIER": args.accessibility_tier,
        "SURFACES": args.surfaces,
        "STYLE_A_NAME": style_names["a"],
        "STYLE_B_NAME": style_names["b"],
        "STYLE_C_NAME": style_names["c"],
        "INVENTORY_ROWS": build_inventory_rows(icon_labels, args.surfaces),
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


def write_style_briefs(output_dir: Path, values: dict[str, str]) -> list[Path]:
    created_files: list[Path] = []
    for key in STYLE_KEYS:
        style_values = dict(values)
        style_values["STYLE_LABEL"] = STYLE_LABELS[key]
        style_values["STYLE_NAME"] = values[f"STYLE_{key.upper()}_NAME"]

        target_path = output_dir / f"style-{key}" / "candidate-brief.md"
        target_path.write_text(
            render_text(STYLE_CANDIDATE_TEMPLATE, style_values),
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
    values = template_values(args, skill_version)

    ensure_output_dir(output_dir, force=args.force)
    create_base_dirs(output_dir)
    created_files = copy_templates(output_dir, values)
    created_files.extend(write_style_briefs(output_dir, values))

    print(f"Created multi-style review package (skill v{skill_version}) at {output_dir}")
    for file_path in sorted(created_files):
        print(f"- {file_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
