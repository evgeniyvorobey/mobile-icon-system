#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "SKILL.md",
    "CHANGELOG.md",
    "MIGRATION.md",
    "LICENSE",
    ".github/workflows/ci.yml",
    ".claude/skills/mobile-icon-system/SKILL.md",
    "agents/openai.yaml",
    "references/sources.md",
    "references/live-research.md",
    "references/project-audit.md",
    "references/brand-dna-input.md",
    "references/design-tool-integrations.md",
    "references/icon-grid-construction.md",
    "references/icon-vocabulary.md",
    "references/cross-icon-consistency.md",
    "references/accessibility.md",
    "references/motion-system.md",
    "references/craft-rubric.md",
    "references/negative-space.md",
    "references/aesthetic-principles.md",
    "references/platform-icon-specs.md",
    "references/icon-set-evaluation.md",
    "references/tab-bar-validation.md",
    "references/creative-divergence.md",
    "references/concept-quality.md",
    "references/evaluation.md",
    "references/package-spec.md",
    "references/multi-style-review.md",
    "references/example-requests.md",
    "references/example-responses.md",
    "references/production-resources.md",
    "references/prompt-library.md",
    "references/geometric-craft.md",
    "references/geometric-craft-guide.md",
    "references/color-system.md",
    "references/color-system-guide.md",
    "references/workflow.md",
    "references/style-packs/README.md",
    "references/style-packs/plugin-system.md",
    "references/style-packs/liquid-glass.md",
    "references/style-packs/duotone-chromatic.md",
    "references/style-packs/claymorphism.md",
    "references/style-packs/3d-isometric.md",
    "references/style-packs/pixel-art.md",
    "references/style-packs/hand-drawn.md",
    "references/style-packs/deferred-styles.md",
    "references/domain-metaphors/README.md",
    "references/domain-metaphors/_cross-domain.md",
    "references/domain-metaphors/music.md",
    "references/domain-metaphors/finance.md",
    "references/domain-metaphors/health.md",
    "references/domain-metaphors/productivity.md",
    "references/domain-metaphors/e-commerce.md",
    "references/domain-metaphors/social.md",
    "references/domain-metaphors/dev-tools.md",
    "references/domain-metaphors/transportation.md",
    "references/domain-metaphors/education.md",
    "references/domain-metaphors/gaming.md",
    "scripts/install_skill.py",
    "scripts/init_icon_system_package.py",
    "scripts/init_multi_style_review.py",
    "scripts/render_icon_contact_sheet.py",
    "scripts/validate_motion_spec.py",
    "scripts/validate_style_pack.py",
    "scripts/apply_path_jitter.py",
    "scripts/smoke_test_contact_sheet_browser.py",
    "scripts/smoke_test_contact_sheet.py",
    "scripts/smoke_test_installer.py",
    "scripts/smoke_test_package_scaffold.py",
    "scripts/smoke_test_motion_spec.py",
    "scripts/smoke_test_style_pack_plugin.py",
    "scripts/smoke_test_multi_style_review.py",
    "scripts/smoke_test_path_jitter.py",
    "scripts/grade/bitmap.py",
    "scripts/smoke_test_grade_bitmap.py",
    "assets/style-pack-fixtures/valid/soft-plastic.style-pack",
    "assets/multi-style-template/shared/brief.md",
    "assets/multi-style-template/shared/brand-dna.md",
    "assets/multi-style-template/shared/icon-inventory.csv",
    "assets/multi-style-template/shared/review-constraints.md",
    "assets/multi-style-template/review/contact-sheet.md",
    "assets/multi-style-template/review/decision-log.md",
    "assets/multi-style-template/review/scorecard.md",
    "assets/multi-style-template/review/winner-lock.md",
    "assets/package-template/reviews/project-ui-snapshot.md",
    "assets/package-template/reviews/icon-system-rules.md",
    "assets/package-template/reviews/concept-scorecard.md",
    "assets/package-template/reviews/cross-icon-audit.md",
    "assets/package-template/selected/rationale.md",
    "assets/package-template/selected/usage-guidance.md",
    "assets/package-template/selected/tab-bar-icon-notes.md",
    "assets/package-template/selected/bottom-nav-notes.md",
    "assets/package-template/selected/export-checklist.md",
]

MARKDOWN_GLOBS = [
    "README.md",
    "SKILL.md",
    ".claude/skills/*/SKILL.md",
    "references/*.md",
    "references/style-packs/*.md",
    "references/domain-metaphors/*.md",
    "assets/multi-style-template/**/*.md",
    "assets/package-template/**/*.md",
]

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---\n", re.DOTALL)
VERSION_RE = re.compile(r"^version:\s*(.+)$", re.MULTILINE)
README_VERSION_RE = re.compile(r"\*\*Current version:\s*(.+?)\*\*")
CHANGELOG_VERSION_RE = re.compile(r"^## \[(.+?)\]", re.MULTILINE)


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def validate_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))


def validate_skill_frontmatter() -> None:
    skill_path = ROOT / "SKILL.md"
    content = skill_path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        fail("SKILL.md must begin with YAML frontmatter")

    frontmatter = match.group("body")
    if "name:" not in frontmatter or "description:" not in frontmatter:
        fail("SKILL.md frontmatter must contain both name and description")
    if "version:" not in frontmatter:
        fail("SKILL.md frontmatter must contain a version field")


def validate_relative_links() -> None:
    markdown_files: list[Path] = []
    for pattern in MARKDOWN_GLOBS:
        markdown_files.extend(ROOT.glob(pattern))

    broken_links: list[str] = []
    for file_path in sorted(set(markdown_files)):
        text = file_path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for match in LINK_RE.finditer(line):
                target = match.group(1).strip()
                if not target or "://" in target or target.startswith("#") or target.startswith("mailto:"):
                    continue
                # Strip any in-anchor fragment like "../foo.md#section"
                target_no_frag = target.split("#", 1)[0]
                if not target_no_frag:
                    continue
                candidate = (file_path.parent / target_no_frag).resolve()
                fallback = (ROOT / target_no_frag).resolve()
                if not candidate.exists() and not fallback.exists():
                    broken_links.append(
                        f"{file_path.relative_to(ROOT)}:{lineno} -> {target}"
                    )

    if broken_links:
        fail("Broken relative links found:\n" + "\n".join(broken_links))


def validate_version_consistency() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = VERSION_RE.search(skill_text)
    if not match:
        fail("SKILL.md frontmatter does not contain a version field")
    canonical = match.group(1).strip()

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    rm = README_VERSION_RE.search(readme_text)
    if not rm:
        fail("README.md does not contain a **Current version: X.Y.Z** badge")
    if rm.group(1).strip() != canonical:
        fail(
            f"Version mismatch: SKILL.md says {canonical}, "
            f"README.md says {rm.group(1).strip()}"
        )

    changelog_text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    cm = CHANGELOG_VERSION_RE.search(changelog_text)
    if not cm:
        fail("CHANGELOG.md does not contain a ## [X.Y.Z] version header")
    if cm.group(1).strip() != canonical:
        fail(
            f"Version mismatch: SKILL.md says {canonical}, "
            f"CHANGELOG.md latest entry says {cm.group(1).strip()}"
        )


def validate_installer_script() -> None:
    text = (ROOT / "scripts" / "install_skill.py").read_text(encoding="utf-8")
    required = ["mobile-icon-system", "--codex", "--claude-project"]
    missing = [m for m in required if m not in text]
    if missing:
        fail("install_skill.py is missing expected markers: " + ", ".join(missing))


def validate_prompt_library_user_gate() -> None:
    prompt_path = ROOT / "references" / "prompt-library.md"
    text = prompt_path.read_text(encoding="utf-8")
    forbidden_markers = [
        "Recommend one winner",
        "Select the winner",
        "select winner",
        "Run the craft pass on the winner without confirming",
        "Score and select the rule set yourself",
    ]
    found = [marker for marker in forbidden_markers if marker in text]
    if found:
        fail(
            "Prompt library bypasses the mandatory user-selection gate:\n"
            + "\n".join(found)
        )
    if "mandatory user-selection gate" not in text:
        fail("Prompt library must mention the mandatory user-selection gate")


def validate_creative_divergence_examples() -> None:
    text = (ROOT / "references" / "creative-divergence.md").read_text(
        encoding="utf-8"
    )
    required_markers = [
        "Worked Examples",
        "Bad Set: Decorative Pseudo-Difference",
        "Good Set: True Divergence",
        "Pseudo-Difference Filter",
    ]
    missing = [marker for marker in required_markers if marker not in text]
    if missing:
        fail(
            "Creative divergence examples are incomplete:\n"
            + "\n".join(missing)
        )


def main() -> int:
    validate_required_files()
    validate_skill_frontmatter()
    validate_relative_links()
    validate_version_consistency()
    validate_installer_script()
    validate_prompt_library_user_gate()
    validate_creative_divergence_examples()
    print("[OK] Skill repository structure and relative links are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
