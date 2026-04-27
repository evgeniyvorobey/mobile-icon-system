# Migration Guide

This document captures step-by-step upgrade instructions between major and minor versions of `mobile-icon-system`.

## 0.2.0 → 0.3.0

The 0.3.0 release adds the calibration corpus, generate-N-pick-1, second-eye critique loop, numerical craft rubric, negative-space and aesthetic-principles references, and the render-and-grade pipeline. No file format in `assets/package-template/` changed; existing v0.2.0 packages remain valid.

### What you should do

1. **Re-install** to pick up the new reference files and corpus:
   ```bash
   python3 scripts/install_skill.py --codex --force
   python3 scripts/install_skill.py --claude-project /path/to/your/project --force
   ```
2. **(Optional) Install the grade pipeline** if you want to actually rasterize and check icon SVG output:
   ```bash
   pip install -r requirements-grade.txt
   python3 scripts/render_and_grade.py path/to/your/icons/
   ```
   None of the v0.2.0 prompts require this — the pipeline is purely additive.
3. **(Optional) Refresh the calibration corpus** if you want to re-fetch from upstream sources:
   ```bash
   python3 scripts/fetch_references.py --update
   ```

### What changed in inputs

- Phase 7 (Generate the set) now requires N variants per icon. Standard tier defaults to 2; hi-end to 3+. The skill picks a winner with explicit per-axis reasoning. If you previously asked for "generate the set" you'll get more variant exploration and a justified pick — the winning set is still the primary deliverable.
- Phase 8 (Audit) expanded to two passes: cross-icon consistency (existing) plus second-eye critique (new). The second-eye pass can loop back to phase 7 for any icon scoring below B on any rubric axis. Loop capped at 2 iterations per icon.
- Phase 9 (hi-end craft) now references the calibration corpus directly when a tier-A example exists for the metaphor in scope.

### What changed in outputs

- The skill cites which calibration-corpus files it consulted in the response.
- When the grade pipeline runs, the response includes a per-icon scorecard with verdict (ok / warn / hard_fail) and a Markdown report.

### Breaking changes

None. All v0.2.0 prompts continue to work. The variant-pick discipline and critique loop are workflow additions, not signature changes.

## 0.1.0 → 0.2.0

The 0.2.0 release expands scope to the **full brand icon set** (13 categories), adds first-class **WCAG 2.2 accessibility** support, adds **Figma / Pencil MCP integration**, and removes all sibling-skill dependencies — the skill is now fully self-contained.

No file format in `assets/package-template/` changed. Existing v0.1.0 packages remain compatible. The migration is additive on the input side; output stays backwards-compatible.

### What you should do

1. **Re-install** to pick up the new reference files (`accessibility.md`, `design-tool-integrations.md`) and the expanded `icon-vocabulary.md`:
   ```bash
   python3 scripts/install_skill.py --codex --force
   python3 scripts/install_skill.py --claude-project /path/to/your/project --force
   ```
2. **Update your invocation prompts** to take advantage of the new scope — instead of "Refresh the Tab Bar icons", consider "Generate the full brand icon set across Tab Bar, action, system, status, and content categories". The skill now works equally well at full-set scale.
3. **Add an accessibility tier to your prompts** when relevant — default is WCAG 2.2 AA; specify AAA when shipping into a regulated context (EU EAA, US ADA, UK Equality Act categories).
4. **Connect a design-tool MCP** when available — the skill now natively integrates with Figma MCP and Pencil MCP, and will state the source explicitly. No code changes required; the MCP just needs to be running.

### What changed in inputs

- Brand DNA Mode 1 no longer requires a specific generator. Any well-formed `brand-dna.md` works — hand-written, exported from another tool, or carried over from a sibling project. See [`references/brand-dna-input.md`](references/brand-dna-input.md).
- Phase 5 (icon system rules) now requires you to confirm an **accessibility budget** along with grid / stroke / style. The skill will propose defaults (3:1 contrast, 44pt iOS / 48dp Android touch targets) — confirm or override.

### What changed in outputs

- New required output-contract fields: `Design tool:`, `Set scope:`, `Accessibility tier:`. These join the existing `Mode:`, `Platform scope:`, `Brand DNA source:`, `Assumptions:`, etc.
- Phase 13 packages now include an `accessibility-notes.md` — labels per locale, traits, contrast measurements, reduced-motion fallbacks.
- When a design-tool MCP is connected, Phase 13 also writes design-tool handoff (Figma Code Connect mappings or Pencil exports).

### Breaking changes

None. All v0.1.0 prompts continue to work. The expanded scope and new fields are additive.

## 0.1.0 (initial release)

No prior version. No migration required.
