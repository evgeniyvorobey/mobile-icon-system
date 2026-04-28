---
name: mobile-icon-system
description: Self-contained workflow for mobile app icon systems — full static icon sets, style packs/plugins, A/B/C style review, and Animated/Lottie motion specs. WCAG 2.2 accessible. Integrates with Figma / Pencil MCP when available. Use directly in Claude with /mobile-icon-system.
argument-hint: "[task / icon set / refresh / audit request]"
disable-model-invocation: true
---

# Mobile Icon System

Use the repository's canonical mobile icon system skill for this request.

When invoked:

1. Read `${CLAUDE_SKILL_DIR}/../../../SKILL.md` first. That file is the canonical skill entrypoint and contains the core workflow.
2. Read supporting files only as needed:
   - `${CLAUDE_SKILL_DIR}/../../../references/project-audit.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/brand-dna-input.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/design-tool-integrations.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/icon-grid-construction.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/icon-vocabulary.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/domain-metaphors/` (load matched domain file + `_cross-domain.md` only when phase 4 matches a domain)
   - `${CLAUDE_SKILL_DIR}/../../../references/cross-icon-consistency.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/accessibility.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/motion-system.md` (load only when animated icons, Lottie, dotLottie, or reduced-motion validation is in scope)
   - `${CLAUDE_SKILL_DIR}/../../../references/craft-rubric.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/negative-space.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/aesthetic-principles.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/platform-icon-specs.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/icon-set-evaluation.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/tab-bar-validation.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/sources.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/live-research.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/concept-quality.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/evaluation.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/creative-divergence.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/example-responses.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/package-spec.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/multi-style-review.md` (load only for A/B/C or three-style client review)
   - `${CLAUDE_SKILL_DIR}/../../../references/style-packs/plugin-system.md` (load only for user `.style-pack` manifests)
   - `${CLAUDE_SKILL_DIR}/../../../references/production-resources.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/geometric-craft.md`
   - `${CLAUDE_SKILL_DIR}/../../../references/color-system.md`
3. Detect available design-tool MCPs (Figma, Pencil, or generic) and state the source explicitly. Fall back to filesystem-only mode when no MCP is connected.
4. If the task requires real handoff files, use `${CLAUDE_SKILL_DIR}/../../../scripts/init_icon_system_package.py`.
5. Apply the canonical workflow to the current request.

Invocation payload:

$ARGUMENTS

If no arguments were passed after `/mobile-icon-system`, use the most recent user request from the conversation as the task input.

Return the result as a normal skill response, following the structure defined by the canonical skill.
