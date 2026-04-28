# Migration Guide

This document captures step-by-step upgrade instructions between major and minor versions of `mobile-icon-system`.

## 0.5.0 → 0.6.0

The v0.6 release adds production-integration tooling around the v0.5 motion and style systems: Lottie/dotLottie asset validation, rendered A/B/C contact sheets, Android/iOS export scaffolding, style-pack registry discovery, design-tool write-back planning, visual regression, a demo package, and a small custom corpus expansion. Existing static, motion-spec, plugin, and multi-style prompts remain compatible.

### What you should do

1. **Re-install** to pick up the new references, templates, and scripts:
   ```bash
   python3 scripts/install_skill.py --codex --force
   python3 scripts/install_skill.py --claude-project /path/to/your/project --force
   ```
2. **Run the expanded validation suite**:
   ```bash
   python3 scripts/validate_skill_repo.py
   python3 scripts/smoke_test_lottie_assets.py
   python3 scripts/smoke_test_multi_style_contact_sheet.py
   python3 scripts/smoke_test_platform_exports.py
   python3 scripts/smoke_test_style_pack_registry.py
   python3 scripts/smoke_test_design_tool_handoff.py
   python3 scripts/smoke_test_demo_package.py
   python3 scripts/smoke_test_reference_corpus_v06.py
   ```
3. **Validate Lottie/dotLottie exports** after the motion spec passes:
   ```bash
   python3 scripts/validate_motion_spec.py motion/motion-spec.json
   python3 scripts/validate_lottie_assets.py motion/lottie motion/dotlottie
   ```
4. **Render A/B/C contact sheets** after all candidate style folders have matching SVG stems:
   ```bash
   python3 scripts/render_multi_style_contact_sheet.py ./multi-style-review \
     --output ./multi-style-review/review/contact-sheet.html
   ```
5. **Scaffold platform exports** from path-only SVG masters:
   ```bash
   python3 scripts/export_platform_assets.py ./icon-system/exports/svg-masters --platform both
   ```
6. **Create design-tool handoff plans** when a connected MCP is unavailable or write-back needs review:
   ```bash
   python3 scripts/scaffold_design_tool_handoff.py ./icon-system/design-tool-handoff \
     --project-name "Project Name" \
     --handoff-mode mixed
   ```

### What changed in outputs

- Multi-style review packages can now include a generated `review/contact-sheet.html`.
- Motion packages should include both motion-spec validation and Lottie/dotLottie asset-validation evidence.
- Production packages can include Android VectorDrawable XML, iOS `.xcassets` scaffolds, visual-regression reports, and design-tool handoff plans.
- Style-pack discovery can be tracked with `assets/style-pack-registry/registry.json`.

### Breaking changes

None. New tools are additive and opt-in. The platform exporter is intentionally strict and may fail on SVGs that render fine in a browser but are not safe to map to Android VectorDrawable without flattening.

### Known v0.6 limitations

- `validate_lottie_assets.py` validates asset structure and rejects risky mobile-icon features; it does not render pixels or prove renderer parity.
- `export_platform_assets.py` does not convert SVG to iOS PDF. It requires same-stem vector PDFs or writes placeholder manifests only when explicitly requested.
- Visual regression requires project-owned PNG baselines. The skill repo does not ship approved visual baselines for your app.

## 0.4.0 → 0.5.0

The v0.5 release adds optional subsystems for Animated/Lottie motion, user `.style-pack` plugins, three-style A/B/C client review, and three shipped style packs (3D/isometric, pixel-art, hand-drawn). Static icon workflows from v0.4 remain compatible.

### What you should do

1. **Re-install** to pick up the new references and scripts:
   ```bash
   python3 scripts/install_skill.py --codex --force
   python3 scripts/install_skill.py --claude-project /path/to/your/project --force
   ```
2. **Run the expanded validation suite**:
   ```bash
   python3 scripts/validate_skill_repo.py
   python3 scripts/smoke_test_motion_spec.py
   python3 scripts/smoke_test_style_pack_plugin.py
   python3 scripts/smoke_test_multi_style_review.py
   ```
3. **Validate motion specs** when shipping animated icons:
   ```bash
   python3 scripts/validate_motion_spec.py path/to/motion-spec.json
   ```
4. **Validate custom style plugins** before applying them:
   ```bash
   python3 scripts/validate_style_pack.py path/to/custom.style-pack
   ```
5. **Use A/B/C scaffolding** for client review:
   ```bash
   python3 scripts/init_multi_style_review.py ./multi-style-review \
     --project-name "Project Name" \
     --styles liquid-glass,3d-isometric,hand-drawn
   ```

### What changed in inputs

- Phase 4 now captures motion requirements separately from visual style.
- Phase 5 visual style options now include `3d-isometric`, `pixel-art`, `hand-drawn`, and custom `.style-pack` plugins.
- A new Phase 7.5 supports one set generated in three styles for client review. The client must lock one winner before production generation continues.
- Motion/Lottie work reads `references/motion-system.md` and requires a JSON motion spec before Lottie/dotLottie handoff.

### What changed in outputs

- New required output-contract field: `Motion scope:` (`none`, `motion-spec`, `Lottie`, or `dotLottie`).
- Production packages may include optional `motion/`, `style-review/`, and `style-plugins/` sections.
- Pixel-art packages must document bitmap-aware QA.
- Hand-drawn packages must document deterministic jitter seed, amplitude, and protected-anchor policy.

### Breaking changes

None for existing static icon prompts. New flows are opt-in. If a prompt asks for animated icons, the skill now blocks production until a static frame and reduced-motion fallback are specified.

### Known v0.5 limitations

- `validate_motion_spec.py` validates the motion contract, not the rendered Lottie file. Renderer-specific compatibility still needs product QA.
- `.style-pack` manifests are data-only; they do not execute custom generators.
- Multi-style review scaffolding creates review structure and decision logs, but it does not render contact sheets automatically.

## 0.3.0 → 0.4.0

The v0.4 release closes the grader→regen loop, adds semantic failure detection as hard_fail, expands the corpus from 27 to 118 SVGs / 14 to 44 metaphors, fills color-system.md, ships 3 visual style packs (Liquid Glass, chromatic duotone, claymorphism), and adds 10 vertical-domain metaphor catalogs. No file format in `assets/package-template/` changed; existing v0.3 packages remain valid.

### What you should do

1. **Re-install** to pick up new reference files and corpus:
   ```bash
   python3 scripts/install_skill.py --codex --force
   python3 scripts/install_skill.py --claude-project /path/to/your/project --force
   ```
2. **Refresh the calibration corpus** to download all 88 new SVGs:
   ```bash
   python3 scripts/fetch_references.py --update
   ```
3. **(Optional) Try the regeneration loop**: after the LLM ships a set, run:
   ```bash
   pip install -r requirements-grade.txt    # if not already
   python3 scripts/grade_with_fixes.py path/to/your/icons --brief-out regen_brief.md
   ```
   Hand the brief to the LLM and ask it to regenerate the flagged icons. Re-run the script to verify improvement. Cap at 2 iterations per icon.

### What changed in inputs

- Phase 4 (Build context) now matches your stated app category to one of 10 domain-metaphor catalogs. If you say "music streaming app", the skill loads `references/domain-metaphors/music.md` plus the cross-domain disambiguation file in Phase 6.
- Phase 5 (Rules gate) now asks you to declare visual style (default monochrome / duotone-mono / liquid-glass / duotone-chromatic / claymorphism). Each style pack has a "Refuse if" condition checked against your brand DNA.
- Phase 6 (Vocabulary) loads matched domain catalog + cross-domain patterns + universal vocabulary. Domain wins where it conflicts with universal (e.g., heart in health = anatomical, not romantic).
- Phase 8 (Audit) adds Pass C (grader-driven regeneration loop) — runs the programmatic grader, emits `regen_brief.md`, regenerates flagged icons, re-runs grader. Cap at 2 iterations per icon.

### What changed in outputs

- New required output-contract field: `Visual style:` declaration in every response.
- Phase 8 audit now hard_fails on two semantic checks: anti-example similarity (output too close to a tier-c documented failure) and color-only state distinction (state pair differs only in color, not shape — fails accessibility).

### Breaking changes

None. All v0.3 prompts continue to work. Style-pack selection is opt-in (default = monochrome). Domain catalog matching is automatic but additive.

### Known v0.4 limitations

- 3 new tier-A icons (`banknote.svg`, `fingerprint.svg`, `scissors.svg`) hard_fail the silhouette stability check at 16pt due to fine details collapsing — documented in their respective `.notes.md` files. They remain tier-A at 24pt+ (their design size) but should not be naively downscaled to 16pt.
- The grader's `reference.py` (legacy v0.3 pHash check, distinct from new `anti_example_similarity.py`) has a known alpha-drop bug that produces all-zero distances for transparent SVGs. The new `anti_example_similarity.py` works around this with white-compositing. Fix scheduled for v0.4.1.

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
