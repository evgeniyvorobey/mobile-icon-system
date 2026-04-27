#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "mobile-icon-system"
IGNORE_PATTERNS = shutil.ignore_patterns(".git", "__pycache__", ".DS_Store")
CLAUDE_VENDOR_IGNORE_NAMES = {".git", ".claude", "__pycache__", ".DS_Store"}
_VERSION_RE = re.compile(r"^version:\s*(.+)$", re.MULTILINE)


def read_skill_version(root: Path = ROOT) -> str:
    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        return "unknown"
    text = skill_path.read_text(encoding="utf-8")
    match = _VERSION_RE.search(text)
    return match.group(1).strip() if match else "unknown"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the mobile-icon-system skill into Codex and/or a Claude project."
    )
    parser.add_argument(
        "--codex",
        action="store_true",
        help="Install the skill into the Codex skills directory.",
    )
    parser.add_argument(
        "--codex-home",
        help="Override CODEX_HOME for Codex installation. Defaults to $CODEX_HOME or ~/.codex.",
    )
    parser.add_argument(
        "--codex-mode",
        choices=("link", "copy"),
        default="link",
        help="How to install into Codex: symlink to this repo or copy it. Default: link.",
    )
    parser.add_argument(
        "--claude-project",
        help="Install the skill into the given Claude project directory.",
    )
    parser.add_argument(
        "--claude-mode",
        choices=("link", "copy"),
        default="copy",
        help="How to install into the Claude project vendor directory. Default: copy.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing install target.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        dest="show_version",
        help="Show the skill version and exit.",
    )
    args = parser.parse_args()
    if args.show_version:
        print(f"{SKILL_NAME} {read_skill_version()}")
        raise SystemExit(0)
    if not args.codex and not args.claude_project:
        parser.error("Choose at least one install target: --codex and/or --claude-project.")
    return args


def resolve_codex_home(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    code_home = os.environ.get("CODEX_HOME")
    if code_home:
        return Path(code_home).expanduser().resolve()
    return Path.home() / ".codex"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def remove_path(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    shutil.rmtree(path)


def detect_installed_version(dest: Path) -> str | None:
    if dest.is_symlink():
        target = dest.resolve()
        return read_skill_version(target) if target.is_dir() else None
    if dest.is_dir():
        return read_skill_version(dest)
    return None


def print_upgrade_notice(target_label: str, old_version: str | None, new_version: str) -> None:
    old = old_version or "unknown"
    if old == new_version:
        print(f"[info] {target_label}: reinstalling v{new_version}")
    else:
        print(f"[info] {target_label}: upgrading v{old} -> v{new_version}")
        if old != "unknown" and old.split(".")[0] != new_version.split(".")[0]:
            print(f"[info] This is a major upgrade. See MIGRATION.md for breaking changes.")


def install_codex(codex_home: Path, mode: str, force: bool) -> Path:
    dest = codex_home / "skills" / SKILL_NAME
    if dest.exists() or dest.is_symlink():
        if not force:
            raise SystemExit(
                f"Codex skill target already exists: {dest}\nUse --force to overwrite it."
            )
        old_version = detect_installed_version(dest)
        print_upgrade_notice("Codex", old_version, read_skill_version())
        remove_path(dest)
    ensure_parent(dest)
    if mode == "link":
        dest.symlink_to(ROOT, target_is_directory=True)
    else:
        shutil.copytree(ROOT, dest, ignore=IGNORE_PATTERNS)
    return dest


def install_claude_vendor(vendor_dest: Path, mode: str) -> None:
    vendor_dest.mkdir(parents=True, exist_ok=True)
    for child in ROOT.iterdir():
        if child.name in CLAUDE_VENDOR_IGNORE_NAMES:
            continue
        dest_child = vendor_dest / child.name
        if mode == "link":
            dest_child.symlink_to(child, target_is_directory=child.is_dir())
            continue
        if child.is_dir():
            shutil.copytree(child, dest_child, ignore=IGNORE_PATTERNS)
        else:
            shutil.copy2(child, dest_child)


def render_claude_wrapper(repo_root_expr: str) -> str:
    return f"""---
name: {SKILL_NAME}
description: Self-contained workflow for the full brand icon set of a mobile app — Tab Bar, action, system, media, status, communication, commerce, content, social, editing, time, location, security. WCAG 2.2 accessible. Integrates with Figma / Pencil MCP when available. Use directly in Claude with /{SKILL_NAME}.
argument-hint: "[task / icon set / refresh / audit request]"
disable-model-invocation: true
---

# Mobile Icon System

Use the repository's canonical mobile icon system skill for this request.

When invoked:

1. Read `{repo_root_expr}/SKILL.md` first. That file is the canonical skill entrypoint and contains the core workflow.
2. Read supporting files only as needed:
   - `{repo_root_expr}/references/project-audit.md`
   - `{repo_root_expr}/references/brand-dna-input.md`
   - `{repo_root_expr}/references/design-tool-integrations.md`
   - `{repo_root_expr}/references/icon-grid-construction.md`
   - `{repo_root_expr}/references/icon-vocabulary.md`
   - `{repo_root_expr}/references/cross-icon-consistency.md`
   - `{repo_root_expr}/references/accessibility.md`
   - `{repo_root_expr}/references/platform-icon-specs.md`
   - `{repo_root_expr}/references/icon-set-evaluation.md`
   - `{repo_root_expr}/references/tab-bar-validation.md`
   - `{repo_root_expr}/references/sources.md`
   - `{repo_root_expr}/references/live-research.md`
   - `{repo_root_expr}/references/concept-quality.md`
   - `{repo_root_expr}/references/evaluation.md`
   - `{repo_root_expr}/references/creative-divergence.md`
   - `{repo_root_expr}/references/example-responses.md`
   - `{repo_root_expr}/references/package-spec.md`
   - `{repo_root_expr}/references/production-resources.md`
   - `{repo_root_expr}/references/geometric-craft.md`
   - `{repo_root_expr}/references/color-system.md`
3. Detect available design-tool MCPs (Figma, Pencil, or generic) and state the source explicitly. Fall back to filesystem-only mode when no MCP is connected.
4. If the task requires real handoff files, use `{repo_root_expr}/scripts/init_icon_system_package.py`.
5. Apply the canonical workflow to the current request.

Invocation payload:

$ARGUMENTS

If no arguments were passed after `/{SKILL_NAME}`, use the most recent user request from the conversation as the task input.

Return the result as a normal skill response, following the structure defined by the canonical skill.
"""


def install_claude(project_root: Path, mode: str, force: bool) -> tuple[Path, Path]:
    claude_root = project_root / ".claude"
    vendor_dest = claude_root / "vendor" / SKILL_NAME
    wrapper_dest = claude_root / "skills" / SKILL_NAME / "SKILL.md"

    if vendor_dest.exists() or vendor_dest.is_symlink():
        if not force:
            raise SystemExit(
                f"Claude vendor target already exists: {vendor_dest}\nUse --force to overwrite it."
            )
        old_version = detect_installed_version(vendor_dest)
        print_upgrade_notice("Claude", old_version, read_skill_version())
        remove_path(vendor_dest)

    if wrapper_dest.exists():
        if not force:
            raise SystemExit(
                f"Claude wrapper already exists: {wrapper_dest}\nUse --force to overwrite it."
            )
        remove_path(wrapper_dest)

    ensure_parent(vendor_dest)
    ensure_parent(wrapper_dest)

    install_claude_vendor(vendor_dest, mode=mode)

    repo_root_expr = f"${{CLAUDE_SKILL_DIR}}/../../vendor/{SKILL_NAME}"
    wrapper_dest.write_text(render_claude_wrapper(repo_root_expr), encoding="utf-8")
    return vendor_dest, wrapper_dest


def main() -> int:
    args = parse_args()
    version = read_skill_version()

    if args.codex:
        codex_home = resolve_codex_home(args.codex_home)
        codex_dest = install_codex(codex_home, mode=args.codex_mode, force=args.force)
        print(f"[OK] Installed Codex skill v{version} to {codex_dest}")

    if args.claude_project:
        project_root = Path(args.claude_project).expanduser().resolve()
        if not project_root.exists():
            print(f"Claude project directory does not exist: {project_root}", file=sys.stderr)
            return 1
        if not project_root.is_dir():
            print(
                f"Claude project path is not a directory: {project_root}",
                file=sys.stderr,
            )
            return 1
        vendor_dest, wrapper_dest = install_claude(
            project_root,
            mode=args.claude_mode,
            force=args.force,
        )
        print(f"[OK] Installed Claude vendor files v{version} to {vendor_dest}")
        print(f"[OK] Installed Claude skill wrapper to {wrapper_dest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
