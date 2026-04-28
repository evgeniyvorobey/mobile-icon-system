#!/usr/bin/env python3
"""Smoke test for the multi-style contact sheet renderer."""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_multi_style_contact_sheet.py"
PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}")


SVG_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><{shape}/></svg>"""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def svg(shape: str) -> str:
    return SVG_TEMPLATE.format(shape=shape)


def build_review_package(review_dir: Path) -> None:
    for relative_dir in (
        "shared",
        "review",
        "style-a/icons",
        "style-b/icons",
        "style-c/icons",
    ):
        (review_dir / relative_dir).mkdir(parents=True, exist_ok=True)

    write_text(
        review_dir / "shared" / "icon-inventory.csv",
        "\n".join(
            [
                "icon_id,label,locked_metaphor,states,target_surfaces",
                "home,Home,house,default,iOS Tab Bar",
                "search,Search,magnifying glass,default,iOS Tab Bar",
                "profile,Profile,user silhouette,default,Android Bottom Nav",
            ]
        )
        + "\n",
    )
    write_text(
        review_dir / "shared" / "review-constraints.md",
        "\n".join(
            [
                "# Review Constraints - Smoke Project",
                "",
                "Project: Smoke Project",
                "",
                "## Frozen Review Inputs",
                "",
                "- Grid: 24x24 base / 20x20 live area",
                "- Accessibility tier: WCAG AA",
                "- Target surfaces: iOS Tab Bar, Android Bottom Nav",
                "- Style A: Calm Precision",
                "- Style B: Friendly Weight",
                "- Style C: Editorial Sharp",
            ]
        )
        + "\n",
    )

    for key, name in (
        ("a", "Calm Precision"),
        ("b", "Friendly Weight"),
        ("c", "Editorial Sharp"),
    ):
        write_text(
            review_dir / f"style-{key}" / "candidate-brief.md",
            f"# Style {key.upper()} - {name}\n\n## Candidate Rule Set\n\n",
        )

    shapes = {
        "home": "rect x=\"5\" y=\"8\" width=\"14\" height=\"11\" fill=\"#111\"",
        "search": "circle cx=\"10\" cy=\"10\" r=\"6\" fill=\"none\" stroke=\"#111\" stroke-width=\"2\"",
        "profile": "circle cx=\"12\" cy=\"8\" r=\"4\" fill=\"#111\"",
    }

    for key in ("a", "b", "c"):
        for icon_id, shape in shapes.items():
            if key == "b" and icon_id == "profile":
                continue
            write_text(
                review_dir / f"style-{key}" / "icons" / f"{icon_id}.svg",
                svg(shape),
            )


def assert_contains(html: str, markers: list[str]) -> None:
    missing = [marker for marker in markers if marker not in html]
    if missing:
        raise SystemExit(
            "[FAIL] Multi-style contact sheet missing expected markers:\n"
            + "\n".join(missing)
        )


def assert_row_order(html: str, icon_ids: list[str]) -> None:
    positions = []
    for icon_id in icon_ids:
        marker = f'data-icon-id="{icon_id}"'
        position = html.find(marker)
        if position == -1:
            raise SystemExit(f"[FAIL] Missing row marker: {marker}")
        positions.append(position)
    if positions != sorted(positions):
        raise SystemExit("[FAIL] Contact sheet rows do not follow inventory order")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="multi-style-contact-sheet-") as temp:
        review_dir = Path(temp) / "review-package"
        build_review_package(review_dir)

        output = review_dir / "review" / "contact-sheet.html"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(review_dir),
                "--output",
                str(output),
                "--title",
                "Smoke A/B/C Contact Sheet",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            raise SystemExit(
                "[FAIL] multi-style contact sheet command failed\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )
        if not output.exists():
            raise SystemExit(f"[FAIL] Expected contact sheet to exist: {output}")

        html = output.read_text(encoding="utf-8")
        assert_contains(
            html,
            [
                "Smoke A/B/C Contact Sheet",
                "Shared Constraints",
                "24x24 base / 20x20 live area",
                "A/B/C Contact Sheet",
                "Calm Precision",
                "Friendly Weight",
                "Editorial Sharp",
                "data-style-key=\"a\"",
                "data-style-key=\"b\"",
                "data-style-key=\"c\"",
                "data:image/svg+xml;base64,",
                "data-review-img",
                "data-missing-svg=\"style-b/icons/profile.svg\"",
                "Missing SVG",
                "Home",
                "Search",
                "Profile",
            ],
        )
        if "Missing SVGs: 1" not in result.stdout:
            raise SystemExit("[FAIL] Command summary did not report one missing SVG")
        assert_row_order(html, ["home", "search", "profile"])

        placeholders = PLACEHOLDER_RE.findall(html)
        if placeholders:
            raise SystemExit(
                "[FAIL] Unresolved placeholders found in contact sheet:\n"
                + "\n".join(sorted(set(placeholders)))
            )
        if "http://" in html or "https://" in html:
            raise SystemExit("[FAIL] Contact sheet should not reference external assets")

    print("[OK] Multi-style contact sheet smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
