# mobile-icon-system

A standalone skill for Codex and Claude that designs, audits and packages the full brand icon set of a mobile app, with render-and-grade pipelines, WCAG 2.2 contrast checks on declared palettes, style packs, Lottie motion validation and platform exports.

## Layout

- `SKILL.md`: canonical entrypoint and 13-phase workflow; its Progressive Disclosure section lists when each reference loads.
- `.claude/skills/mobile-icon-system/SKILL.md` (Claude) and `.agents/skills/mobile-icon-system/SKILL.md` (Codex): twin wrappers that reach the canonical files through `${CLAUDE_SKILL_DIR}/../../../`. They differ only in the host name in `description`; change both together. `agents/openai.yaml` is Codex metadata.
- `references/`: workflow references, domain metaphors, style packs.
- `assets/`: package templates, the calibration corpus, and `demo-package/` (SVG masters plus `palette.json`), which CI grades.
- `scripts/`: installer, validators, the `grade/` package with `render_and_grade.py` and `grade_with_fixes.py`, exporters, and one `smoke_test_*.py` per tool.

## Changing the skill

1. Edit, then run every step of `.github/workflows/ci.yml` locally. Done is all of them green.
   - The grade steps need `pip install -r requirements-grade.txt`.
   - `smoke_test_contact_sheet_browser.py` needs Node.js (`npx`).
   - `render_and_grade.py assets/demo-package/exports/svg-masters` exits 2 or more on a hard failure, which fails CI.
2. A new tool ships with its own `smoke_test_*.py` and a step in `ci.yml`.
3. A claim in `README.md` or `SKILL.md` is backed by a check that runs in CI. v0.7.0 found a grader that never ran and a contrast claim with no maths behind it.
4. Release: one version in `SKILL.md` frontmatter, the `**Current version: X.Y.Z**` line in `README.md`, and a `## [X.Y.Z]` header in `CHANGELOG.md` (`validate_skill_repo.py` checks all three), plus upgrade steps in `MIGRATION.md` when a package breaks. Semver rules are in `README.md`.

## Source of truth and copies

This repo is the source of truth. After a change, report which copies need a sync and leave the sync to the owner.

- `~/Documents/thera_tales/.claude/skills/mobile-icon-system/SKILL.md` and `~/Documents/thera_tales/.claude/vendor/mobile-icon-system/`: a wrapper plus a vendor copy, made by `python3 scripts/install_skill.py --claude-project <path> --force`. That command overwrites the wrapper, and this wrapper differs from what it writes, so merge it by hand.
