#!/usr/bin/env python3
"""Render an HTML A/B/C contact sheet for a multi-style review package."""
from __future__ import annotations

import argparse
import base64
import csv
from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
import sys


STYLE_KEYS = ("a", "b", "c")
STYLE_LABELS = {"a": "Style A", "b": "Style B", "c": "Style C"}
PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}")
HEADING_RE = re.compile(r"^#\s+(.+?)\s*$")
BULLET_KV_RE = re.compile(r"^-\s+(?:\*\*)?(.+?)(?:\*\*)?\s*:\s*(.*)$")
PROJECT_RE = re.compile(r"^Project:\s*(.+?)\s*$", re.IGNORECASE)


@dataclass(frozen=True)
class InventoryRow:
    row_number: int
    icon_id: str
    label: str
    locked_metaphor: str
    states: str
    target_surfaces: str


@dataclass(frozen=True)
class ConstraintItem:
    key: str
    value: str


@dataclass(frozen=True)
class StyleInfo:
    key: str
    label: str
    name: str
    brief_path: Path


def clean_display_text(raw: str | None, fallback: str = "") -> str:
    if not raw:
        return fallback
    value = PLACEHOLDER_RE.sub("", raw)
    value = " ".join(value.split())
    return value.strip(" -*") or fallback


def parse_positive_int(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Expected a positive integer: {raw}") from exc
    if value <= 0:
        raise argparse.ArgumentTypeError("Value must be a positive integer.")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render an HTML contact sheet comparing style A/B/C SVG icons."
    )
    parser.add_argument(
        "review_dir",
        help="Path to a multi-style review directory.",
    )
    parser.add_argument(
        "--output",
        help=(
            "HTML file to write. Default: <review_dir>/review/contact-sheet.html"
        ),
    )
    parser.add_argument(
        "--title",
        help="Title shown in the generated contact sheet.",
    )
    parser.add_argument(
        "--icon-size",
        type=parse_positive_int,
        default=56,
        help="Preview icon size in CSS pixels. Default: 56",
    )
    return parser.parse_args()


def validate_review_dir(review_dir: Path) -> None:
    required = [review_dir / "shared" / "icon-inventory.csv"]
    required.extend(review_dir / f"style-{key}" / "icons" for key in STYLE_KEYS)

    missing = [path for path in required if not path.exists()]
    if missing:
        lines = "\n".join(f"- {path}" for path in missing)
        raise SystemExit(f"Review package is missing required paths:\n{lines}")

    for icons_dir in required[1:]:
        if not icons_dir.is_dir():
            raise SystemExit(f"Expected icons directory: {icons_dir}")


def read_inventory(review_dir: Path) -> list[InventoryRow]:
    inventory_path = review_dir / "shared" / "icon-inventory.csv"
    rows: list[InventoryRow] = []
    seen_ids: set[str] = set()

    with inventory_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "icon_id" not in reader.fieldnames:
            raise SystemExit(
                f"Inventory must include an icon_id column: {inventory_path}"
            )

        for row_number, raw_row in enumerate(reader, start=2):
            icon_id = clean_display_text(raw_row.get("icon_id", ""))
            if not icon_id:
                raise SystemExit(
                    f"Inventory row {row_number} is missing an icon_id."
                )
            if "/" in icon_id or "\\" in icon_id:
                raise SystemExit(
                    f"Inventory row {row_number} has a non-stem icon_id: {icon_id}"
                )
            if icon_id in seen_ids:
                raise SystemExit(f"Duplicate icon_id in inventory: {icon_id}")
            seen_ids.add(icon_id)

            label = clean_display_text(raw_row.get("label", ""), fallback=icon_id)
            rows.append(
                InventoryRow(
                    row_number=row_number,
                    icon_id=icon_id,
                    label=label,
                    locked_metaphor=clean_display_text(
                        raw_row.get("locked_metaphor", "")
                    ),
                    states=clean_display_text(raw_row.get("states", "")),
                    target_surfaces=clean_display_text(
                        raw_row.get("target_surfaces", "")
                    ),
                )
            )

    if not rows:
        raise SystemExit(f"Inventory has no icon rows: {inventory_path}")
    return rows


def lines_in_section(text: str, title: str) -> list[str]:
    wanted = title.lower()
    in_section = False
    output: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            current = stripped.lstrip("#").strip().lower()
            if current == wanted:
                in_section = True
                continue
            if in_section:
                break
        if in_section:
            output.append(stripped)

    return output


def read_constraints(review_dir: Path) -> tuple[list[ConstraintItem], dict[str, str]]:
    constraints_path = review_dir / "shared" / "review-constraints.md"
    if not constraints_path.exists():
        return [], {}

    text = constraints_path.read_text(encoding="utf-8")
    candidate_lines = lines_in_section(text, "Frozen Review Inputs")
    if not candidate_lines:
        candidate_lines = [line.strip() for line in text.splitlines()]

    items: list[ConstraintItem] = []
    style_names: dict[str, str] = {}

    for line in candidate_lines:
        match = BULLET_KV_RE.match(line)
        if not match:
            continue
        key = clean_display_text(match.group(1))
        value = clean_display_text(match.group(2))
        if not key or not value:
            continue
        items.append(ConstraintItem(key=key, value=value))

        style_match = re.fullmatch(r"Style\s+([ABCabc])", key)
        if style_match:
            style_names[style_match.group(1).lower()] = value

    return items, style_names


def read_project_name(review_dir: Path) -> str:
    for relative_path in (
        Path("shared") / "review-constraints.md",
        Path("shared") / "brief.md",
    ):
        path = review_dir / relative_path
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            match = PROJECT_RE.match(line.strip())
            if match:
                name = clean_display_text(match.group(1))
                if name:
                    return name
    return review_dir.name


def parse_candidate_name(
    brief_path: Path, label: str, fallback_name: str
) -> str:
    if brief_path.exists():
        text = brief_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            match = HEADING_RE.match(line.strip())
            if not match:
                continue

            heading = clean_display_text(match.group(1))
            if not heading:
                break

            label_prefix = re.escape(label)
            prefixed = re.match(
                rf"^{label_prefix}\s*[-:]\s*(.+)$",
                heading,
                flags=re.IGNORECASE,
            )
            if prefixed:
                name = clean_display_text(prefixed.group(1))
                if name:
                    return name

            if heading.lower() != label.lower():
                return heading
            break

    return clean_display_text(fallback_name, fallback=f"Candidate {label[-1]}")


def read_styles(review_dir: Path, constraint_style_names: dict[str, str]) -> list[StyleInfo]:
    styles: list[StyleInfo] = []
    for key in STYLE_KEYS:
        label = STYLE_LABELS[key]
        brief_path = review_dir / f"style-{key}" / "candidate-brief.md"
        styles.append(
            StyleInfo(
                key=key,
                label=label,
                name=parse_candidate_name(
                    brief_path, label, constraint_style_names.get(key, "")
                ),
                brief_path=brief_path,
            )
        )
    return styles


def expected_svg_path(review_dir: Path, style_key: str, icon_id: str) -> Path:
    filename = icon_id if icon_id.lower().endswith(".svg") else f"{icon_id}.svg"
    return review_dir / f"style-{style_key}" / "icons" / filename


def relative_to_review(review_dir: Path, path: Path) -> str:
    try:
        return path.relative_to(review_dir).as_posix()
    except ValueError:
        return path.as_posix()


def svg_data_uri(path: Path) -> str:
    svg_text = path.read_text(encoding="utf-8")
    encoded = base64.b64encode(svg_text.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def count_present_svgs(review_dir: Path, rows: list[InventoryRow], style_key: str) -> int:
    return sum(
        1
        for row in rows
        if expected_svg_path(review_dir, style_key, row.icon_id).is_file()
    )


def render_constraints(items: list[ConstraintItem]) -> str:
    if not items:
        return (
            "<p class=\"empty-note\">No shared review constraints file was found.</p>"
        )

    details = "\n".join(
        f"<div><dt>{escape(item.key)}</dt><dd>{escape(item.value)}</dd></div>"
        for item in items
    )
    return f"<dl class=\"constraints-list\">{details}</dl>"


def render_inventory_meta(row: InventoryRow) -> str:
    meta: list[str] = []
    if row.locked_metaphor:
        meta.append(f"<span>Metaphor: {escape(row.locked_metaphor)}</span>")
    if row.states:
        meta.append(f"<span>States: {escape(row.states)}</span>")
    if row.target_surfaces:
        meta.append(f"<span>Surfaces: {escape(row.target_surfaces)}</span>")
    if not meta:
        return ""
    return f"<div class=\"icon-meta\">{''.join(meta)}</div>"


def render_style_header(
    review_dir: Path, rows: list[InventoryRow], style: StyleInfo
) -> str:
    present = count_present_svgs(review_dir, rows, style.key)
    total = len(rows)
    missing = total - present
    status = f"{present}/{total} SVGs"
    if missing:
        status = f"{status}, {missing} missing"
    status_class = "status-warn" if missing else "status-ok"
    brief_rel = relative_to_review(review_dir, style.brief_path)

    return f"""
      <th scope="col" class="style-heading" data-style-key="{escape(style.key)}">
        <span class="style-code">{escape(style.label)}</span>
        <span class="style-name">{escape(style.name)}</span>
        <span class="style-brief">{escape(brief_rel)}</span>
        <span class="{status_class}">{escape(status)}</span>
      </th>
    """


def render_style_cell(
    review_dir: Path, row: InventoryRow, style: StyleInfo, icon_size: int
) -> str:
    svg_path = expected_svg_path(review_dir, style.key, row.icon_id)
    svg_rel = relative_to_review(review_dir, svg_path)
    if not svg_path.is_file():
        return f"""
        <td class="style-cell missing-cell"
            data-style-key="{escape(style.key)}"
            data-svg-state="missing"
            data-missing-svg="{escape(svg_rel)}">
          <div class="missing-indicator">
            <strong>Missing SVG</strong>
            <span>{escape(svg_rel)}</span>
          </div>
        </td>
        """

    uri = svg_data_uri(svg_path)
    alt = f"{row.label} in {style.label} - {style.name}"
    return f"""
      <td class="style-cell"
          data-style-key="{escape(style.key)}"
          data-svg-state="present"
          data-svg-path="{escape(svg_rel)}">
        <figure>
          <div class="preview-frame">
            <img data-review-img
                 alt="{escape(alt)}"
                 src="{uri}"
                 width="{icon_size}"
                 height="{icon_size}"
                 style="width:{icon_size}px;height:{icon_size}px"/>
          </div>
          <figcaption>{escape(svg_rel)}</figcaption>
        </figure>
      </td>
    """


def render_icon_row(
    review_dir: Path, row: InventoryRow, styles: list[StyleInfo], icon_size: int, index: int
) -> str:
    cells = "".join(render_style_cell(review_dir, row, style, icon_size) for style in styles)
    meta = render_inventory_meta(row)
    return f"""
    <tr class="icon-row" data-row-index="{index}" data-icon-id="{escape(row.icon_id)}">
      <th scope="row" class="icon-heading">
        <span class="icon-label">{escape(row.label)}</span>
        <span class="icon-id">{escape(row.icon_id)}</span>
        {meta}
      </th>
      {cells}
    </tr>
    """


STYLE = """
:root {
  color-scheme: light;
  --ink: #202124;
  --muted: #5f6368;
  --line: #dadce0;
  --panel: #f8f9fa;
  --paper: #ffffff;
  --ok: #137333;
  --warn: #a14200;
  --warn-bg: #fff4e5;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  padding: 28px;
  color: var(--ink);
  background: var(--paper);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
h1 {
  margin: 0 0 8px;
  font-size: 30px;
  line-height: 1.15;
  letter-spacing: 0;
}
h2 {
  margin: 0 0 12px;
  font-size: 18px;
  letter-spacing: 0;
}
.lede {
  margin: 0;
  color: var(--muted);
}
section {
  margin-top: 28px;
}
.constraints-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 10px;
  margin: 0;
}
.constraints-list div {
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 10px 12px;
  background: var(--panel);
}
dt {
  margin: 0 0 4px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}
dd {
  margin: 0;
}
.empty-note {
  margin: 0;
  color: var(--warn);
}
.table-wrap {
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 8px;
}
table {
  width: 100%;
  min-width: 820px;
  border-collapse: collapse;
}
th, td {
  border-bottom: 1px solid var(--line);
  padding: 12px;
  vertical-align: top;
}
thead th {
  position: sticky;
  top: 0;
  z-index: 1;
  background: var(--paper);
  border-bottom: 2px solid var(--ink);
}
tbody tr:last-child th,
tbody tr:last-child td {
  border-bottom: 0;
}
.icon-heading {
  width: 260px;
  text-align: left;
  background: #fcfcfc;
}
.icon-label,
.icon-id,
.style-code,
.style-name,
.style-brief,
.status-ok,
.status-warn,
.icon-meta span {
  display: block;
}
.icon-label,
.style-code {
  font-weight: 700;
}
.icon-id,
.style-brief,
.icon-meta {
  margin-top: 4px;
  color: var(--muted);
  font-size: 12px;
}
.style-heading {
  min-width: 180px;
  text-align: left;
}
.style-name {
  margin-top: 2px;
  font-weight: 500;
}
.status-ok,
.status-warn {
  margin-top: 6px;
  font-size: 12px;
  font-weight: 700;
}
.status-ok { color: var(--ok); }
.status-warn { color: var(--warn); }
.style-cell {
  min-width: 180px;
  text-align: center;
}
figure {
  margin: 0;
}
.preview-frame {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 96px;
  height: 96px;
  margin: 0 auto;
  border: 1px solid var(--line);
  border-radius: 6px;
  background:
    linear-gradient(45deg, #f1f3f4 25%, transparent 25%),
    linear-gradient(-45deg, #f1f3f4 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #f1f3f4 75%),
    linear-gradient(-45deg, transparent 75%, #f1f3f4 75%);
  background-color: #fff;
  background-position: 0 0, 0 8px, 8px -8px, -8px 0;
  background-size: 16px 16px;
}
.preview-frame img {
  display: block;
}
figcaption {
  margin-top: 8px;
  color: var(--muted);
  font-size: 11px;
  overflow-wrap: anywhere;
}
.missing-cell {
  background: var(--warn-bg);
}
.missing-indicator {
  display: flex;
  min-height: 96px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border: 1px dashed var(--warn);
  border-radius: 6px;
  color: var(--warn);
}
.missing-indicator span {
  max-width: 160px;
  font-size: 11px;
  overflow-wrap: anywhere;
}
@media print {
  body { padding: 16px; }
  thead th { position: static; }
  .table-wrap { overflow: visible; }
}
"""


def render_html(
    title: str,
    review_dir: Path,
    rows: list[InventoryRow],
    styles: list[StyleInfo],
    constraints: list[ConstraintItem],
    icon_size: int,
) -> str:
    headers = "".join(render_style_header(review_dir, rows, style) for style in styles)
    body_rows = "".join(
        render_icon_row(review_dir, row, styles, icon_size, index)
        for index, row in enumerate(rows, start=1)
    )
    constraints_html = render_constraints(constraints)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{escape(title)}</title>
  <style>{STYLE}</style>
</head>
<body data-review-type="multi-style-contact-sheet">
  <header>
    <h1>{escape(title)}</h1>
    <p class="lede">{len(rows)} inventory rows compared across style A, style B, and style C.</p>
  </header>

  <section aria-labelledby="constraints-title">
    <h2 id="constraints-title">Shared Constraints</h2>
    {constraints_html}
  </section>

  <section aria-labelledby="contact-sheet-title">
    <h2 id="contact-sheet-title">A/B/C Contact Sheet</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th scope="col" class="icon-heading">Icon</th>
            {headers}
          </tr>
        </thead>
        <tbody>
          {body_rows}
        </tbody>
      </table>
    </div>
  </section>
</body>
</html>
"""


def resolve_output_path(review_dir: Path, raw_output: str | None) -> Path:
    if raw_output:
        return Path(raw_output).expanduser().resolve()
    return review_dir / "review" / "contact-sheet.html"


def main() -> int:
    args = parse_args()
    review_dir = Path(args.review_dir).expanduser().resolve()
    if not review_dir.is_dir():
        print(f"Review directory not found: {review_dir}", file=sys.stderr)
        return 1

    validate_review_dir(review_dir)
    rows = read_inventory(review_dir)
    constraints, constraint_style_names = read_constraints(review_dir)
    styles = read_styles(review_dir, constraint_style_names)

    title = clean_display_text(args.title)
    if not title:
        title = f"A/B/C Icon Review - {read_project_name(review_dir)}"

    html = render_html(
        title=title,
        review_dir=review_dir,
        rows=rows,
        styles=styles,
        constraints=constraints,
        icon_size=args.icon_size,
    )

    output_path = resolve_output_path(review_dir, args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    missing_count = sum(
        1
        for row in rows
        for style in styles
        if not expected_svg_path(review_dir, style.key, row.icon_id).is_file()
    )
    print(f"Wrote multi-style contact sheet: {output_path}")
    print(f"Inventory rows: {len(rows)}")
    print(f"Missing SVGs: {missing_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
