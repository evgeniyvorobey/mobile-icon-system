#!/usr/bin/env python3
"""Smoke test for ``scripts/grade_with_fixes.py``.

Runs the orchestrator over a tiny fixture dir (one clean circle + one
decimal-anchor square pair) and asserts:

* exit code is 1 (warn) or 2 (hard_fail) — the dirty fixture must trip
  *something*,
* the generated regeneration brief mentions the failing icon by name,
* the brief cites the failing check name (alignment),
* the brief cites a craft-rubric.md section,
* the brief includes the original SVG markup verbatim.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "grade_with_fixes.py"
FIXTURES = ROOT / "assets" / "references" / "fixtures" / "grade_with_fixes"
DIRTY_NAME = "circle_dirty.svg"


def main() -> int:
    if not FIXTURES.exists():
        print(f"[FAIL] fixtures missing at {FIXTURES}")
        return 1
    dirty = FIXTURES / DIRTY_NAME
    clean = FIXTURES / "circle_clean.svg"
    if not dirty.exists() or not clean.exists():
        print(f"[FAIL] expected both fixtures (clean+dirty) under {FIXTURES}")
        return 1

    with tempfile.TemporaryDirectory(prefix="grade-with-fixes-smoke-") as tmp:
        brief_path = Path(tmp) / "regeneration_brief.md"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(FIXTURES),
                "--brief-out",
                str(brief_path),
                "--reference-corpus",
                str(ROOT / "assets" / "references" / "tier-a"),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        if result.returncode not in (1, 2):
            print(
                "[FAIL] expected exit 1 (warn) or 2 (hard_fail) for the dirty "
                f"fixture; got {result.returncode}\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )
            return 1
        if not brief_path.exists():
            print(f"[FAIL] brief not written to {brief_path}")
            return 1
        brief = brief_path.read_text(encoding="utf-8")
        if DIRTY_NAME not in brief:
            print(f"[FAIL] brief does not mention dirty icon name {DIRTY_NAME!r}\n"
                  f"---\n{brief}\n---")
            return 1
        if "alignment" not in brief.lower():
            print(f"[FAIL] brief does not cite the alignment check\n"
                  f"---\n{brief}\n---")
            return 1
        if "craft-rubric.md" not in brief:
            print(f"[FAIL] brief does not cite craft-rubric.md\n"
                  f"---\n{brief}\n---")
            return 1
        # Original SVG markup must be embedded — look for the dirty icon's
        # signature path-data fragment.
        if "M 4.27 4.27" not in brief:
            print(f"[FAIL] brief does not include original SVG markup\n"
                  f"---\n{brief}\n---")
            return 1

    print("[OK] grade_with_fixes smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
