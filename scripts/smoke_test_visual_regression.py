#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "visual_regression_contact_sheet.py"


def write_png(path: Path, color: tuple[int, int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGBA", (8, 8), color)
    image.save(path)


def run_compare(base: Path, current: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(base),
            str(current),
            "--max-diff-ratio",
            "0.01",
            "--max-channel-delta",
            "8",
            *extra,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="visual-regression-") as tmp:
        root = Path(tmp)
        baseline = root / "baseline"
        current = root / "current"
        changed = root / "changed"

        write_png(baseline / "contact-sheet.png", (10, 20, 30, 255))
        write_png(current / "contact-sheet.png", (10, 20, 30, 255))
        ok = run_compare(baseline, current, "--report-json", str(root / "report.json"))
        if ok.returncode != 0:
            raise SystemExit(
                "[FAIL] identical snapshots failed\n"
                f"stdout:\n{ok.stdout}\nstderr:\n{ok.stderr}"
            )
        if not (root / "report.json").exists():
            raise SystemExit("[FAIL] report JSON was not written")

        write_png(changed / "contact-sheet.png", (250, 20, 30, 255))
        bad = run_compare(baseline, changed)
        if bad.returncode == 0:
            raise SystemExit("[FAIL] changed snapshot unexpectedly passed")
        if "diff_ratio" not in bad.stdout:
            raise SystemExit("[FAIL] changed snapshot report missing diff_ratio")

        missing = root / "missing"
        missing.mkdir()
        missing_result = run_compare(baseline, missing)
        if missing_result.returncode == 0:
            raise SystemExit("[FAIL] missing current snapshot unexpectedly passed")
        if "missing-current" not in missing_result.stdout:
            raise SystemExit("[FAIL] missing current report did not explain failure")

    print("[OK] visual regression smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
