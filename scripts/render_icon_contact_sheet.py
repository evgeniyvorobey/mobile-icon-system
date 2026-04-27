#!/usr/bin/env python3
"""
Render an HTML contact sheet for an icon set.

Shows every icon in the input directory at multiple target sizes (default 16,
20, 24, 32 pt) so the cross-icon consistency audit and Tab Bar / Bottom Nav
context validation can be done visually.

Usage:

    python3 scripts/render_icon_contact_sheet.py /path/to/svg-masters \\
        --output contact-sheet.html \\
        --sizes 16,20,24,32

If a file pair like ic_tab_home_filled.svg / ic_tab_home_outlined.svg is
detected, the icons are grouped into a state pair row so filled / outlined
sit side by side.
"""
from __future__ import annotations

import argparse
import base64
from collections import defaultdict
from html import escape
from pathlib import Path
import re
import sys


DEFAULT_SIZES = [16, 20, 24, 32]
PAIR_RE = re.compile(r"^(.*)_(filled|outlined)$", re.IGNORECASE)


def parse_sizes(raw: str) -> list[int]:
    sizes: list[int] = []
    for part in raw.split(","):
        value = part.strip()
        if not value:
            continue
        try:
            size = int(value)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                f"Invalid size {value!r}; use comma-separated integers."
            ) from exc
        if size <= 0:
            raise argparse.ArgumentTypeError("Sizes must be positive integers.")
        sizes.append(size)
    if not sizes:
        raise argparse.ArgumentTypeError("At least one size is required.")
    return sizes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render an HTML contact sheet for an icon set."
    )
    parser.add_argument(
        "svg_source",
        help=(
            "Path to a directory containing SVG masters or a list of SVG files."
        ),
    )
    parser.add_argument(
        "--output",
        default="icon-contact-sheet.html",
        help="HTML file to write. Default: icon-contact-sheet.html",
    )
    parser.add_argument(
        "--title",
        default="Icon Set Contact Sheet",
        help="Title shown in the generated review sheet.",
    )
    parser.add_argument(
        "--sizes",
        type=parse_sizes,
        default=DEFAULT_SIZES,
        help="Comma-separated target sizes in pt. Default: 16,20,24,32",
    )
    return parser.parse_args()


def collect_svg_files(source: str) -> list[Path]:
    path = Path(source).expanduser().resolve()
    if path.is_dir():
        files = sorted(path.glob("*.svg"))
        if not files:
            raise SystemExit(f"No SVG files found in directory: {path}")
        return files
    if path.is_file():
        if path.suffix.lower() != ".svg":
            raise SystemExit(f"Expected an .svg file: {path}")
        return [path]
    raise SystemExit(f"SVG source not found: {path}")


def read_svg(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def svg_data_uri(svg_text: str) -> str:
    encoded = base64.b64encode(svg_text.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def group_state_pairs(files: list[Path]) -> list[dict]:
    """Group filled / outlined pairs into one row entry; singletons become their own row."""
    by_stem: dict[str, dict[str, Path]] = defaultdict(dict)
    singletons: list[Path] = []

    for path in files:
        match = PAIR_RE.match(path.stem)
        if match:
            base, state = match.group(1), match.group(2).lower()
            by_stem[base][state] = path
        else:
            singletons.append(path)

    rows: list[dict] = []
    for base, states in sorted(by_stem.items()):
        rows.append(
            {
                "name": base,
                "filled": states.get("filled"),
                "outlined": states.get("outlined"),
            }
        )
    for path in singletons:
        rows.append({"name": path.stem, "filled": None, "outlined": None, "single": path})

    return rows


def render_icon_cell(size: int, svg_text: str | None, label: str) -> str:
    if not svg_text:
        return f"""<td class="icon-cell empty"><span class="missing">missing</span></td>"""
    uri = svg_data_uri(svg_text)
    return (
        f"""<td class="icon-cell">"""
        f"""<img data-review-img alt="{escape(label)} at {size}pt" src="{uri}" """
        f"""width="{size}" height="{size}" style="width:{size}px;height:{size}px"/>"""
        f"""</td>"""
    )


def render_row(row: dict, sizes: list[int]) -> str:
    name = row["name"]
    filled = row.get("filled")
    outlined = row.get("outlined")
    single = row.get("single")

    filled_svg = read_svg(filled) if filled else None
    outlined_svg = read_svg(outlined) if outlined else None
    single_svg = read_svg(single) if single else None

    cells_filled = "".join(
        render_icon_cell(size, filled_svg, f"{name} filled") for size in sizes
    )
    cells_outlined = "".join(
        render_icon_cell(size, outlined_svg, f"{name} outlined") for size in sizes
    )
    cells_single = "".join(
        render_icon_cell(size, single_svg, name) for size in sizes
    )

    if single_svg is not None:
        return f"""
        <tr class="icon-row" data-icon-name="{escape(name)}">
          <th class="icon-name">{escape(name)}</th>
          <th class="state-label">single</th>
          {cells_single}
        </tr>
        """

    return f"""
    <tr class="icon-row" data-icon-name="{escape(name)}">
      <th class="icon-name" rowspan="2">{escape(name)}</th>
      <th class="state-label">filled</th>
      {cells_filled}
    </tr>
    <tr class="icon-row icon-row-outlined" data-icon-name="{escape(name)}">
      <th class="state-label">outlined</th>
      {cells_outlined}
    </tr>
    """


def render_size_header(sizes: list[int]) -> str:
    headers = "".join(f"<th class='size-header'>{s}pt</th>" for s in sizes)
    return f"""
    <tr>
      <th class="icon-name">Icon</th>
      <th class="state-label">State</th>
      {headers}
    </tr>
    """


def render_tab_bar_mockup(rows: list[dict], surface: str = "ios") -> str:
    """Render a Tab Bar (iOS) or Bottom Nav (Android) mockup with the icons."""
    label_map = {
        "ios": "iOS Tab Bar (light)",
        "android": "Android Bottom Nav (light)",
    }
    icon_size = 25 if surface == "ios" else 24
    cells: list[str] = []
    for row in rows[:5]:
        name = row["name"]
        filled = row.get("filled")
        outlined = row.get("outlined") or row.get("single")
        svg_text = read_svg(filled or outlined) if (filled or outlined) else None
        if not svg_text:
            cells.append(f"<div class='nav-cell empty'>{escape(name)}</div>")
            continue
        uri = svg_data_uri(svg_text)
        cells.append(
            f"<div class='nav-cell'>"
            f"<img data-review-img alt='{escape(name)} {surface}' src='{uri}' width='{icon_size}' height='{icon_size}'/>"
            f"<span class='nav-label'>{escape(name.replace('ic_tab_', '').replace('ic_', ''))}</span>"
            f"</div>"
        )
    return f"""
    <section class="surface-mockup surface-{surface}" data-surface="{surface}">
      <h3>{label_map[surface]}</h3>
      <div class="nav-frame">{''.join(cells)}</div>
    </section>
    """


def render_html(title: str, rows: list[dict], sizes: list[int]) -> str:
    size_header = render_size_header(sizes)
    icon_rows = "".join(render_row(row, sizes) for row in rows)
    ios_mockup = render_tab_bar_mockup(rows, surface="ios")
    android_mockup = render_tab_bar_mockup(rows, surface="android")

    style = """
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 24px; color: #222; }
    h1 { margin-top: 0; }
    section { margin-bottom: 32px; }
    table { border-collapse: collapse; }
    th, td { padding: 8px; text-align: center; }
    th.icon-name { text-align: left; padding-right: 12px; min-width: 140px; }
    th.state-label { text-align: left; font-weight: normal; color: #666; min-width: 80px; }
    th.size-header { font-weight: 600; color: #333; min-width: 56px; }
    .icon-cell { background: #f7f7f9; border: 1px solid #eee; }
    .icon-cell.empty { color: #c00; font-style: italic; }
    .icon-cell img { display: block; margin: 0 auto; }
    .icon-row-outlined .icon-cell { background: #fff; }
    .nav-frame { display: flex; gap: 16px; padding: 12px 24px; border-radius: 16px; background: #fafafa; box-shadow: 0 0 0 1px #eee; }
    .nav-cell { display: flex; flex-direction: column; align-items: center; gap: 4px; min-width: 60px; }
    .nav-cell img { display: block; }
    .nav-label { font-size: 10px; color: #555; }
    .surface-mockup h3 { margin-bottom: 8px; }
    """

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{escape(title)}</title>
  <style>{style}</style>
</head>
<body>
  <h1>{escape(title)}</h1>

  <section class="size-grid">
    <h2>Icon Size Grid</h2>
    <table data-grid="size-grid">
      <thead>{size_header}</thead>
      <tbody>{icon_rows}</tbody>
    </table>
  </section>

  <section class="surface-mockups">
    <h2>Surface Mockups</h2>
    {ios_mockup}
    {android_mockup}
  </section>
</body>
</html>"""


def main() -> int:
    args = parse_args()

    files = collect_svg_files(args.svg_source)
    rows = group_state_pairs(files)

    html = render_html(title=args.title, rows=rows, sizes=args.sizes)

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    print(f"Wrote contact sheet: {output_path}")
    print(f"Icons rendered: {len(rows)} rows across {len(args.sizes)} sizes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
