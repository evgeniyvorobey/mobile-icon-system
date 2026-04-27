#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install_skill.py"
SKILL_NAME = "mobile-icon-system"


def run(*args: str, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(INSTALLER), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if expect_success and result.returncode != 0:
        raise SystemExit(
            f"[FAIL] command failed: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    if not expect_success and result.returncode == 0:
        raise SystemExit(
            f"[FAIL] command unexpectedly succeeded: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"[FAIL] Expected path to exist: {path}")


def assert_not_exists(path: Path) -> None:
    if path.exists():
        raise SystemExit(f"[FAIL] Expected path to be absent: {path}")


def main() -> int:
    temp_root = Path(tempfile.mkdtemp(prefix="mobile-icon-system-smoke-"))
    try:
        codex_home = temp_root / "codex-home"
        claude_project = temp_root / "claude-project"
        claude_project.mkdir(parents=True, exist_ok=True)

        run("--codex", "--codex-home", str(codex_home), "--codex-mode", "copy")
        codex_skill = codex_home / "skills" / SKILL_NAME
        assert_exists(codex_skill / "SKILL.md")
        assert_exists(codex_skill / "agents" / "openai.yaml")

        run("--claude-project", str(claude_project), "--claude-mode", "copy")
        vendor_root = claude_project / ".claude" / "vendor" / SKILL_NAME
        wrapper = claude_project / ".claude" / "skills" / SKILL_NAME / "SKILL.md"
        assert_exists(vendor_root / "SKILL.md")
        assert_exists(wrapper)
        assert_not_exists(vendor_root / ".claude")

        claude_project_link = temp_root / "claude-project-link"
        claude_project_link.mkdir(parents=True, exist_ok=True)
        run("--claude-project", str(claude_project_link), "--claude-mode", "link")
        vendor_root_link = claude_project_link / ".claude" / "vendor" / SKILL_NAME
        assert_exists(vendor_root_link / "SKILL.md")
        assert_not_exists(vendor_root_link / ".claude")

        not_a_dir = temp_root / "not-a-dir.txt"
        not_a_dir.write_text("x", encoding="utf-8")
        result = run("--claude-project", str(not_a_dir), expect_success=False)
        if "not a directory" not in result.stderr:
            raise SystemExit(
                "[FAIL] Expected a clear 'not a directory' error for invalid "
                "--claude-project input."
            )

        print("[OK] Installer smoke tests passed.")
        return 0
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
