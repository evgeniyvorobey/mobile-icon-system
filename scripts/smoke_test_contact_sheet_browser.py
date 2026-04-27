#!/usr/bin/env python3
"""Browser smoke test for the icon contact sheet.

Renders a dummy icon set, generates the HTML contact sheet, then opens it in
headless Chromium via Playwright (installed temporarily via npm) and
verifies that the expected markers are visible in the rendered DOM.

Requires: Node.js / npm available on PATH.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.request import url2pathname


ROOT = Path(__file__).resolve().parents[1]
RENDER_SCRIPT = ROOT / "scripts" / "render_icon_contact_sheet.py"


DUMMY_FILLED = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" fill="#000"/></svg>"""
DUMMY_OUTLINED = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" fill="none" stroke="#000" stroke-width="1.75"/></svg>"""


PLAYWRIGHT_SCRIPT_TEMPLATE = """
const {{ chromium }} = require('playwright');
(async () => {{
  const browser = await chromium.launch({{ headless: true }});
  const page = await browser.newPage();
  await page.goto({url_literal});
  const visibleImageCount = await page.locator('[data-review-img]').count();
  const sizeGridPresent = await page.locator('[data-grid="size-grid"]').count();
  const iosSurfacePresent = await page.locator('[data-surface="ios"]').count();
  const androidSurfacePresent = await page.locator('[data-surface="android"]').count();
  const result = {{
    visibleImageCount,
    sizeGridPresent,
    iosSurfacePresent,
    androidSurfacePresent,
  }};
  console.log(JSON.stringify(result));
  await browser.close();
}})();
"""


def write_dummy_set(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "ic_tab_home_filled.svg").write_text(DUMMY_FILLED, encoding="utf-8")
    (directory / "ic_tab_home_outlined.svg").write_text(DUMMY_OUTLINED, encoding="utf-8")
    (directory / "ic_tab_search_filled.svg").write_text(DUMMY_FILLED, encoding="utf-8")
    (directory / "ic_tab_search_outlined.svg").write_text(DUMMY_OUTLINED, encoding="utf-8")


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True)
    if result.returncode != 0:
        raise SystemExit(
            f"[FAIL] command failed: {' '.join(cmd)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def main() -> int:
    if shutil.which("npm") is None or shutil.which("npx") is None:
        print("[SKIP] npm/npx not available; browser smoke test requires Node.js.")
        return 0

    with tempfile.TemporaryDirectory(prefix="mobile-icon-system-browser-") as temp:
        temp_path = Path(temp)
        svg_dir = temp_path / "icons"
        write_dummy_set(svg_dir)

        output = temp_path / "contact-sheet.html"
        run(
            [
                sys.executable,
                str(RENDER_SCRIPT),
                str(svg_dir),
                "--output",
                str(output),
                "--title",
                "Browser Smoke Icon Contact Sheet",
            ],
            cwd=ROOT,
        )

        # Set up a temp Node project and install Playwright
        node_dir = temp_path / "node-runner"
        node_dir.mkdir(parents=True, exist_ok=True)
        (node_dir / "package.json").write_text(
            json.dumps({"name": "icon-system-browser-smoke", "version": "0.0.1", "private": True}),
            encoding="utf-8",
        )

        run(["npm", "install", "--no-audit", "--no-fund", "playwright@1"], cwd=node_dir)
        run(["npx", "playwright", "install", "--with-deps", "chromium"], cwd=node_dir)

        url_literal = json.dumps(output.as_uri())
        script_text = PLAYWRIGHT_SCRIPT_TEMPLATE.format(url_literal=url_literal)
        (node_dir / "smoke.js").write_text(script_text, encoding="utf-8")

        result = run(["node", "smoke.js"], cwd=node_dir)
        try:
            payload = json.loads(result.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError) as exc:
            raise SystemExit(
                f"[FAIL] Could not parse playwright output: {result.stdout!r}"
            ) from exc

        visible = payload.get("visibleImageCount", 0)
        if visible < 4:
            raise SystemExit(
                f"[FAIL] Expected at least 4 visible icon images, got {visible}"
            )
        if not payload.get("sizeGridPresent"):
            raise SystemExit("[FAIL] size-grid not present in rendered DOM")
        if not payload.get("iosSurfacePresent"):
            raise SystemExit("[FAIL] iOS surface mockup not present in rendered DOM")
        if not payload.get("androidSurfacePresent"):
            raise SystemExit("[FAIL] Android surface mockup not present in rendered DOM")

    print("[OK] Browser contact sheet smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
