# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] — 2026-04-27

Self-contained release. The skill no longer depends on or references any sibling skill — it is a standalone tool for the full brand icon set of a mobile app.

### Added

- **Full brand icon set scope**: `references/icon-vocabulary.md` now covers 13 categories — Tab Bar / Bottom Nav, action, system, media, status, communication, commerce, content, social, editing, time, location, security — totaling ~70 metaphors with cliché map and cross-cultural notes
- **Accessibility reference** (`references/accessibility.md`): WCAG 2.2 AA / AAA requirements for icons (1.4.11 non-text contrast, 2.5.5 / 2.5.8 target size, 2.4.7 focus, 2.3.3 reduced motion), platform touch-target specs (44pt iOS / 48dp Android), screen-reader labeling per platform, color-blind safety, Dynamic Type / Font Scale, Forced Colors / Increase Contrast fallback, full ship checklist, integration map per workflow phase
- **Design-tool integrations reference** (`references/design-tool-integrations.md`): first-class guidance for Figma MCP (Brand DNA from libraries, audit from components, push back via Code Connect) and Pencil MCP (`.pen` is encrypted — Pencil MCP is the only safe access path), generic MCP contract pattern, filesystem-only fallback, audit signals for tool-backed vs screenshot-only work
- Workflow integration of accessibility into phases 4 (build context), 5 (rules gate), 7 (generate), 8 (audit), 10 (evaluate), 11 (validate), 13 (package)
- Workflow integration of design-tool MCP detection into phases 3 (audit) and 13 (package)
- New required output-contract fields: `Design tool:`, `Set scope:`, `Accessibility tier:`

### Changed

- Skill is now standalone; removed all references to `mobile-logo-system` as a prerequisite or companion. Brand DNA Mode 1 reads any well-formed `brand-dna.md` regardless of source
- `references/sources.md` authority order now lists accessibility constraints as non-negotiable, ahead of platform docs
- `references/brand-dna-input.md` Mode 1 is source-agnostic; Mode 2 documents design-tool MCP usage
- `references/project-audit.md` adds a "Design-tool sources" section with MCP guidance
- `SKILL.md` Hard Constraints expanded with accessibility and MCP-honesty rules
- `SKILL.md` Success Criteria now explicitly require WCAG 2.2 AA
- `agents/openai.yaml` and `.claude/skills/mobile-icon-system/SKILL.md` updated to reflect full-set scope, accessibility, and MCP integration

### Notes

- Reference files in this release continue to be progressively filled; `accessibility.md` and `design-tool-integrations.md` ship complete, `icon-vocabulary.md` is now full-coverage. Other reference files retain v0.1.0 scaffolds where noted.
- Existing v0.1.0 packages remain compatible — no schema changes to `assets/package-template/`. Only additive guidance.

## [0.1.0] — 2026-04-27

Initial release focused on UI icon sets (Tab Bar, Bottom Nav, action icons).

### Added

- Canonical `SKILL.md` workflow with 13 phases and two quality tiers (Standard / Hi-end)
- Mandatory user-confirmation gate after icon system rules are defined and before mass generation
- Brand DNA ingestion with three input modes (read existing `brand-dna.md`, extract from project, ask user)
- Reference library covering: project audit, brand DNA input, icon grid construction, icon vocabulary, cross-icon consistency, platform icon specs, icon set evaluation, Tab Bar validation
- Concept-quality, creative-divergence, evaluation, geometric-craft, color-system references adapted from companion skill
- Sources, live-research, workflow, package-spec, production-resources, prompt-library, example-requests, example-responses references
- Production package scaffold via `scripts/init_icon_system_package.py`
- Icon contact sheet renderer via `scripts/render_icon_contact_sheet.py`
- Repo validation, installer smoke test, contact sheet smoke tests, package scaffold smoke test
- Codex `agents/openai.yaml` metadata and Claude `.claude/skills/mobile-icon-system/SKILL.md` wrapper
- CI workflow on Python 3.9 and 3.12

### Notes

- Reference files in this initial release are scaffolded with structure and intros; full content fill is a follow-up minor release.
- No backward compatibility concerns — first version.
