---
name: mobile-icon-system
version: 0.7.0
description: Use when designing, refreshing, auditing, motion-enabling, exporting, or client-reviewing a brand-coherent UI icon set for a mobile app — covers the full app icon system (Tab Bar / Bottom Nav, action, system, media, status, communication, commerce, content, social, editing, time, location, security) plus 10 vertical-domain catalogs (music, finance, health, productivity, e-commerce, social, dev-tools, transportation, education, gaming), 6 shipped visual-style packs (Liquid Glass, chromatic duotone, claymorphism, 3D/isometric, pixel-art, hand-drawn), user `.style-pack` plugins with registry discovery, 3-style parallel A/B/C review with rendered contact sheets, and an Animated/Lottie motion subsystem with asset validation. Best for icon-set work that must inherit visual DNA from an existing logo or design system, stay consistent across the whole set, follow WCAG 2.2 accessibility guidance with declared colour pairs checked mechanically against SC 1.4.11, render at tier-A craft level (calibrated against a hand-curated 122-SVG reference corpus (75 tier-A, 21 tier-B, 11 tier-C anti-examples, 15 duotone/mini/micro and custom anchors) plus custom style/motion anchors, generate-N-pick-1 variant search, mandatory second-eye critique loop, grader-driven regeneration loop, semantic-failure detection, bitmap-aware pixel-art checks), and ship as platform-ready iOS/Android assets with optional Figma / Pencil write-back planning where available.
---

# Mobile Icon System

A self-contained icon-set designer + production workflow. Generates the full brand icon set for a mobile app — Tab Bar, Bottom Nav, action, system, media, status, communication, commerce, content, social, editing, time, location, security — inheriting one Brand DNA across the whole set, with WCAG 2.2 non-text contrast checked mechanically on the declared palette (`scripts/check_contrast.py`), and shipped as platform-ready iOS/Android assets. It can also create motion specs and Lottie/dotLottie handoff plans for animated icons as a separate subsystem, and can generate one icon set in three visual styles for client A/B/C review before locking a winner. Integrates with Figma and Pencil where MCP access is available; works from filesystem alone otherwise.

## When To Use

Use when the user wants: a complete brand icon set for an app, a refresh of an existing icon set, brand-coherent navigation / action / system icons that match an existing logo, single icon additions that must fit an existing system, accessibility-aware icon work (WCAG 2.2 AA / AAA), animated/Lottie icon motion specs, multi-style client review, custom `.style-pack` plugin validation, or evaluation of an existing set for consistency.

Do not use for: full-coverage utility icon libraries with hundreds of glyphs ([SF Symbols](https://developer.apple.com/sf-symbols/), [Material Symbols](https://fonts.google.com/icons), [Tabler](https://tabler.io/icons), [Lucide](https://lucide.dev) are better starting points), illustration, single decorative graphics, or long-form character animation. App launcher / home screen marks need different construction rules than UI icons; use a dedicated logo workflow for that.

## Output Contract

Every response must include: `Mode:`, `Platform scope:`, `Brand DNA source:`, `Design tool:` (Figma MCP / Pencil MCP / filesystem-only), `Set scope:` (which icon categories are in this run), `Visual style:`, `Motion scope:` (none / motion-spec / Lottie / dotLottie), `Accessibility tier:` (WCAG AA / AAA), `Assumptions:`, `Known facts:` vs `Recommendations:`, `Next actions:`.

When the task is icon production, create or update SVG artifacts. When the task includes animated icons, create a motion spec first and validate it with `python3 scripts/validate_motion_spec.py <motion-spec.json>` before producing Lottie/dotLottie handoff artifacts; validate exported Lottie/dotLottie files with `python3 scripts/validate_lottie_assets.py <exports>`. When a handoff package is needed, read [references/production-resources.md](references/production-resources.md) and scaffold with `python3 scripts/init_icon_system_package.py`.

## Workflow

Full workflow details: [references/workflow.md](references/workflow.md)

### 1. Classify the request

Choose one mode: icon-system creation, single icon addition, icon-set audit/refinement, multi-style client review, motion-system add-on, style-pack plugin validation, packaging, export-readiness audit.

#### Quality tier

**Standard** (default) — base evaluation matrix, small-size legibility checks at target sizes (16/20/24pt), basic platform validation, single state per icon if Tab Bar not in scope.

**Hi-end** — full craft pipeline: geometric construction, optical correction per icon, cross-icon consistency audit, color craft, stroke optical balancing, full Tab Bar / Bottom Nav validation including selected/unselected states.

Hi-end triggers: user requests premium/craft-level quality, large user base, store-prominent app, custom brand identity (not generic Material/SF), explicit references to small-size precision or theming.

State the chosen tier in the first response. Can upgrade mid-workflow.

### 2. Establish Brand DNA

Read [references/brand-dna-input.md](references/brand-dna-input.md).

Brand DNA defines the visual language icons must inherit:
- Geometric alphabet (circle / square / arc / cut)
- Stroke weight + contrast
- Corner radius / treatment
- Terminal style (square / round / cut)
- Color logic
- Optical correction principles

Three self-contained input modes — the skill does not depend on any other tool to obtain Brand DNA:
1. **Read** an existing `brand-dna.md` from the project, regardless of who or what created it
2. **Extract** from logo / brand assets in the project, via filesystem or a connected design-tool MCP (see [references/design-tool-integrations.md](references/design-tool-integrations.md))
3. **Ask** the user directly via guided intake, with labeled assumptions

### 3. Audit current UI

Read [references/project-audit.md](references/project-audit.md) and, when a design-tool MCP is connected, [references/design-tool-integrations.md](references/design-tool-integrations.md). Inspect the app's current icon set (if any), UI patterns, color tokens, typography. Build a consistency snapshot: stroke weight, optical sizing, metaphor abstraction level, current cliché load. Determine: are we refreshing an existing set, designing fresh, or adding to a partial system?

### 4. Build context

Extract: app category, **domain catalog selection** — match user's stated app category to one of [references/domain-metaphors/](references/domain-metaphors/) (music, finance, health, productivity, e-commerce, social, dev-tools, transportation, education, gaming); load matched domain file plus `_cross-domain.md` in Phase 6 alongside universal vocabulary; if no match, fall back to universal only. Then: navigation structure (which tabs / nav items exist), full icon inventory required across categories ([references/icon-vocabulary.md](references/icon-vocabulary.md) coverage map), platform priority (iOS / Android / cross-platform), state requirements (selected/unselected for Tab Bar; pressed / disabled for action icons), motion requirements (none / trigger-based micro-interactions / loading / status transition / ongoing animation), system icon coexistence (does the app also use SF Symbols / Material in places?), target locales, accessibility tier (WCAG AA default, AAA if user requests). Preserve user's existing direction unless they ask for a reset.

### 5. Define icon system rules

**Mandatory gate. Do not generate icons before user confirms the rules.**

Read [references/icon-grid-construction.md](references/icon-grid-construction.md), [references/cross-icon-consistency.md](references/cross-icon-consistency.md), and [references/accessibility.md](references/accessibility.md).

Output:
- Base grid (24×24 / 20×20 / 16×16) with live area + keyline padding
- Stroke weight (e.g., 1.75pt) + exception rules
- Style: filled / outlined / duotone (one primary, one optional secondary)
- Visual style: monochrome / outlined / filled / duotone-mono / duotone-chromatic / liquid-glass / claymorphism / 3d-isometric / pixel-art / hand-drawn / custom `.style-pack` plugin (default = monochrome; if user chooses a style-pack option, load the corresponding reference at [references/style-packs/](references/style-packs/); if user supplies a plugin, validate it with `python3 scripts/validate_style_pack.py <file-or-dir>`)
- Selected/unselected state pairing (Tab Bar) — must distinguish via shape, not color alone
- Optical sizing balance protocol
- Terminal style + corner radius logic
- Color application rules (when icons are tinted vs duotone)
- Accessibility budget: contrast target (3:1 minimum non-text, 4.5:1 if any text inside icons), touch-target rule (44pt iOS / 48dp Android), reduced-motion fallback policy; if motion is in scope, read [references/motion-system.md](references/motion-system.md) and require a static frame plus reduced-motion substitute before generation

State strongest direction in one sentence. **Ask user to choose / confirm.** Do not proceed until they respond.

### 6. Define vocabulary

Read [references/icon-vocabulary.md](references/icon-vocabulary.md) PLUS — when phase 4 matched a domain — the corresponding [references/domain-metaphors/{domain}.md](references/domain-metaphors/) file plus [references/domain-metaphors/_cross-domain.md](references/domain-metaphors/_cross-domain.md). When the domain catalog conflicts with universal (e.g., heart in health = anatomical, in universal = romantic), the domain wins for this app — explicitly note the override in the icon-system rules.

For each icon needed across the full set (Tab Bar, action, system, media, status, communication, commerce, content, social, editing, time, location, security):
- Confirm metaphor (avoid category clichés)
- Note cross-cultural readability risk
- Note recognition risk at target size
- Note collision risk with system icons
- Note accessibility risk (color-only state distinction, text inside glyph)

Output a vocabulary table the user can review before generation. For a full app icon set this typically covers 40–80 icons grouped by category.

### 7. Generate the set — variants then pick

Generate icons in **one batch** — never one at a time. Each icon must be produced as **3 distinct variants**, with the variations spanning at least two of these axes:
- Primitive choice (e.g., Home as house silhouette vs geometric anchor; Search with circular vs elliptical lens)
- Anchor distribution (denser/sparser path, different cusp placement)
- Optical correction strength (conservative / standard / pronounced)
- Terminal angle interpretation (exact perpendicular vs slight tangent)
- Negative-space allocation (counter-form area shifts)

For each variant:
- Built on the agreed grid
- Inherits Brand DNA
- Filled + outlined per-state where Tab Bar is in scope
- Inline schematic SVG, no production polish yet

After generating the 3 variants per icon, read [references/concept-quality.md](references/concept-quality.md), [references/craft-rubric.md](references/craft-rubric.md), [references/negative-space.md](references/negative-space.md), and [references/aesthetic-principles.md](references/aesthetic-principles.md). Apply the rubric to each variant. **Pick the winner per icon** with explicit per-axis reasoning ("variant 2 wins: 6 anchors vs 9, optical center 0.4pt above geometric, no trapped space below 4pt"). Present the winning set first; collapse the 2 runner-ups per icon into an appendix that the user can expand.

This is not optional. Standard tier may use 2 variants instead of 3 to control token cost; hi-end always generates 3+.

### 7.5. Multi-style parallel review (when requested)

When the user asks for client review, A/B testing, or "one set in 3 styles", read [references/multi-style-review.md](references/multi-style-review.md). Generate the same vocabulary, grid, Brand DNA, metaphors, state requirements, and accessibility tier across exactly three style candidates. Scaffold review artifacts with:

```
python3 scripts/init_multi_style_review.py <review_dir> --project-name "<Project>" --styles style-a,style-b,style-c
```

After candidate SVGs exist, render a reviewer-friendly HTML comparison:

```
python3 scripts/render_multi_style_contact_sheet.py <review_dir> --output <review_dir>/review/contact-sheet.html
```

Do not blend styles after review. The client chooses one winner; lock that style in Phase 5 and continue production for the chosen style only. Runner-up styles remain review artifacts, not production assets.

### 8. Audit — consistency + second-eye critique

Two mandatory passes before craft / evaluation. Both apply to the winning set chosen in step 7.

**Pass A — Cross-icon consistency.** Read [references/cross-icon-consistency.md](references/cross-icon-consistency.md). Verify across the set:
- Same stroke weight (with optical exceptions documented)
- Same corner radius logic
- Same terminal style
- Visual weight balanced (no icon dominates the row)
- Filled/outlined pairs share construction
- Optical centering consistent

**Pass B — Second-eye critique.** Step out of the brand context. Read the set as if you have never seen the Brand DNA, the icon-system rules, the user's brief. Read [references/craft-rubric.md](references/craft-rubric.md), [references/negative-space.md](references/negative-space.md), [references/aesthetic-principles.md](references/aesthetic-principles.md). Score every icon A/B/C on each rubric axis. For any axis scoring below B: **loop back to step 7** for that icon (regenerate variants, re-pick), not the whole set. Document the loop iterations in the audit output.

**Pass C — Grader-driven regeneration loop.** After Pass A and Pass B, run the programmatic grader with brief generation:

```
python3 scripts/grade_with_fixes.py <icons_dir> --brief-out regen_brief.md
```

If `regen_brief.md` is non-empty, **read it and regenerate every icon flagged**, applying the brief's specific fix instructions (which check failed by how much, the craft-rubric.md citation, the tier-A reference's "What a generator should learn" block, the original SVG markup). Re-run the grader. Cap at **2 grader iterations per icon** — if any icon still fails after 2 iterations, surface it as an unresolved item in phase 12 (Improve or question). This pass is mandatory for hi-end tier; optional but recommended for Standard tier.

Output: per-icon scorecard, corrections made, loop iterations, grader iterations, remaining risks.

### 9. Craft pass (hi-end only)

> Standard tier skips to step 10. **Load craft files only at this step.**

Read and run checklists: [geometric-craft.md](references/geometric-craft.md), [color-system.md](references/color-system.md), [craft-rubric.md](references/craft-rubric.md).

Per-icon optical corrections, path cleanliness, anchor reduction, tangent continuity, pixel alignment at target sizes (16/20/24pt). Cross-icon: stroke optical balancing (visual weight match across set, not just numeric stroke equality). For any icon that has a tier-A reference in [`assets/references/tier-A-craft/`](assets/references/), compare construction patterns and document where the output diverges and why.

### 10. Evaluate

Read [references/icon-set-evaluation.md](references/icon-set-evaluation.md). Score the set on 8 dimensions: small-size legibility, brand fit, platform fit, set consistency, metaphor clarity, cliché avoidance, cross-cultural readability, state distinction (if Tab Bar). Reject if: any icon needs a label at intended size, stroke weight drifts unintentionally, set has dominant outlier.

### 11. Validate in context

Read [references/tab-bar-validation.md](references/tab-bar-validation.md) and [references/accessibility.md](references/accessibility.md). Test:
- iOS Tab Bar mockup with all icons + labels (light + dark) — when Tab Bar in scope
- Android Bottom Nav mockup with selected/unselected states — when Bottom Nav in scope
- Action / system / status icons rendered on their target surfaces (toolbar, button, alert, banner, list row)
- Real screen contexts adjacent to system icons (do they fight?)
- 16pt size if any icon needs to appear at small contexts (notification, inline)
- Run the [references/accessibility.md](references/accessibility.md) checklist: 3:1 non-text contrast in every theme, 44pt iOS / 48dp Android touch target verification, deuteranopia simulation, single-color collapse fallback (Forced Colors / Increase Contrast), Dynamic Type / Font Scale pass for inline icons, reduced-motion static fallback for any animated icon, screen-reader labels per locale
- If pixel-art is selected, run `python3 scripts/smoke_test_grade_bitmap.py` during repo validation and use `scripts/grade/bitmap.py` on candidate SVGs to verify crisp native-pixel behavior.
- If hand-drawn is selected, any jitter must be deterministic via `python3 scripts/apply_path_jitter.py --seed <seed>` and the seed must be documented in the package.
- If motion is in scope, validate every motion spec with `python3 scripts/validate_motion_spec.py <motion-spec.json>`, validate exported Lottie/dotLottie assets with `python3 scripts/validate_lottie_assets.py <exports>`, and verify the reduced-motion path is not color-only, not animation-only, and has a static frame.
- If approved PNG baselines exist, run `python3 scripts/visual_regression_contact_sheet.py <baseline_dir> <current_dir> --report-json <report.json>` after rendering contact-sheet or platform snapshots.

### 12. Improve or question

Identify weakest icon, weakest dimension, 2-3 concrete improvement moves. Ask only high-leverage questions. Proceed with labeled assumptions where possible.

### 13. Package

Read [references/package-spec.md](references/package-spec.md). When a design-tool MCP is connected, also read [references/design-tool-integrations.md](references/design-tool-integrations.md). Output:
- SVG masters per icon (filled + outlined where applicable)
- Platform exports (iOS template images / PDF, Android vector drawables), optionally scaffolded with `python3 scripts/export_platform_assets.py <exports/svg-masters>`
- Usage guidance per surface (Tab Bar tint, Bottom Nav active/inactive, action button states, status surfaces)
- Naming convention (e.g., `ic_tab_home_filled.svg`)
- Accessibility notes — labels per locale, traits, contrast measurements per theme, reduced-motion fallbacks (see [references/accessibility.md](references/accessibility.md))
- Motion specs, Lottie/dotLottie asset-validation logs, and renderer assumptions when motion is in scope (see [references/motion-system.md](references/motion-system.md) and [references/lottie-asset-validation.md](references/lottie-asset-validation.md))
- Style plugin manifests or multi-style decision logs when used (see [references/style-packs/plugin-system.md](references/style-packs/plugin-system.md), [references/multi-style-review.md](references/multi-style-review.md))
- Design-tool handoff or write-back plan (Figma MCP / Code Connect mappings / Pencil MCP / filesystem fallback) when needed
- Export checklist
- Unresolved risks

## Tooling

- **SVG masters**: source of truth for every icon
- **Figma MCP**: preferred when a Figma file or design system is connected — read variables, components, screenshots; push back via MCP or Code Connect only when the tool call actually happens. See [references/design-tool-integrations.md](references/design-tool-integrations.md) and [references/design-tool-writeback.md](references/design-tool-writeback.md).
- **Pencil MCP**: required for any `.pen` file — `.pen` files are encrypted and cannot be opened with `Read`/`Grep`. Use `pencil.batch_get` to read and `pencil.batch_design` to write.
- **Other design-tool MCPs**: any server providing design-context tools — same contract pattern (read before write, transactions where supported, screenshot for visual confirmation)
- **Image generation**: mood/exploration only, never final masters
- **Motion validation**: validate motion spec JSON with `scripts/validate_motion_spec.py`; validate exported Lottie/dotLottie files with `scripts/validate_lottie_assets.py`. Lottie/dotLottie are delivery formats, not style packs.
- **Style plugin validation**: validate `.style-pack` manifests with `scripts/validate_style_pack.py`; build discovery indexes with `scripts/build_style_pack_registry.py`. Custom styles must pass Brand DNA and accessibility gates before Phase 7.
- **Multi-style contact sheets**: render A/B/C HTML comparison sheets with `scripts/render_multi_style_contact_sheet.py`.
- **Platform export automation**: export path-only SVG masters to Android VectorDrawable XML and scaffold iOS PDF-backed `.xcassets` with `scripts/export_platform_assets.py`.
- **Visual regression**: compare approved PNG baselines with `scripts/visual_regression_contact_sheet.py` when project snapshots exist.
- **Pixel-art checks**: use `scripts/grade/bitmap.py` for bitmap-aware crispness and palette checks when pixel-art is selected.
- **Hand-drawn jitter**: use `scripts/apply_path_jitter.py` only with a documented deterministic seed and bounded amplitude.
- **Web research**: when platform guidance may have changed (HIG Tab Bar specs, Material 3 navigation, WCAG 2.2 amendments)
- **Local files (fallback)**: always search project for existing icons, brand assets, design tokens, `brand-dna.md`, color tokens, typography — fully supported when no design-tool MCP is available

## Bilingual Policy

Reply in user's language. Keep source titles in original language. Prefer English labels with localized explanatory copy for reusable artifacts (file names, tokens, layer names should stay English).

## Progressive Disclosure

Load only when needed:
- [references/sources.md](references/sources.md) — source map and authority order
- [references/live-research.md](references/live-research.md) — research watchlists
- [references/project-audit.md](references/project-audit.md) — UI audit
- [references/brand-dna-input.md](references/brand-dna-input.md) — Brand DNA ingestion
- [references/design-tool-integrations.md](references/design-tool-integrations.md) — Figma / Pencil / generic MCP integration
- [references/design-tool-writeback.md](references/design-tool-writeback.md) — Figma/Pencil write-back provenance, Code Connect mapping, filesystem-only handoff scaffold
- [references/icon-grid-construction.md](references/icon-grid-construction.md) — grid + stroke rules
- [references/icon-vocabulary.md](references/icon-vocabulary.md) — full-set metaphor library (13 categories) with calibration-corpus references per metaphor
- [references/domain-metaphors/](references/domain-metaphors/) — 10 domain catalogs (music, finance, health, productivity, e-commerce, social, dev-tools, transportation, education, gaming) + cross-domain patterns + README; loaded only when user states a matching app domain in Phase 4
- [references/cross-icon-consistency.md](references/cross-icon-consistency.md) — set balancing
- [references/craft-rubric.md](references/craft-rubric.md) — numerical thresholds for craft grading (cited; loaded by phase 7 variant pick + phase 8 critique)
- [references/negative-space.md](references/negative-space.md) — counter-form, trapped space, density rhythm (loaded by phase 5 + 7 + 8 + 9)
- [references/aesthetic-principles.md](references/aesthetic-principles.md) — 10 principles (Vignelli, Rams, Müller-Brockmann; loaded by phase 5 + 9)
- [references/accessibility.md](references/accessibility.md) — WCAG 2.2, touch targets, screen-reader labeling, color-blind safety
- [references/motion-system.md](references/motion-system.md) — Animated/Lottie subsystem, motion spec schema, easing, reduced-motion validation; loaded only when motion is in scope
- [references/lottie-asset-validation.md](references/lottie-asset-validation.md) — Lottie JSON and dotLottie asset hygiene; loaded only when Lottie/dotLottie files are produced or audited
- [references/style-packs/](references/style-packs/) — Liquid Glass, chromatic duotone, claymorphism, 3D/isometric, pixel-art, hand-drawn construction rules plus deferred-style register and registry; loaded only when user picks one of these styles in Phase 5
- [references/style-packs/plugin-system.md](references/style-packs/plugin-system.md) — custom `.style-pack` manifest format and validation; loaded only when the user supplies or asks for a custom style plugin
- [references/multi-style-review.md](references/multi-style-review.md) — A/B/C client review workflow for one set generated in three styles, including generated contact sheets; loaded only for multi-style review requests
- [references/platform-export-automation.md](references/platform-export-automation.md) — Android VectorDrawable and iOS PDF-backed `.xcassets` export automation
- [references/demo-package.md](references/demo-package.md) — compact generated demo package and smoke-test expectations
- [references/visual-regression.md](references/visual-regression.md) — PNG baseline comparison for rendered review snapshots
- [assets/references/](assets/references/) — calibration corpus (tier-A / tier-B / tier-C SVGs with `.notes.md` craft observations; loaded by phase 7 variant pick and phase 9 craft pass)
- [references/platform-icon-specs.md](references/platform-icon-specs.md) — iOS/Android specs
- [references/icon-set-evaluation.md](references/icon-set-evaluation.md) — scoring
- [references/tab-bar-validation.md](references/tab-bar-validation.md) — context testing
- [references/workflow.md](references/workflow.md) — full workflow
- [references/package-spec.md](references/package-spec.md) — deliverables
- [references/production-resources.md](references/production-resources.md) — handoff
- [references/concept-quality.md](references/concept-quality.md) — quality gates
- [references/evaluation.md](references/evaluation.md) — generic evaluation
- [references/creative-divergence.md](references/creative-divergence.md) — divergence
- [references/example-requests.md](references/example-requests.md) — request shapes
- [references/example-responses.md](references/example-responses.md) — response shapes
- [references/prompt-library.md](references/prompt-library.md) — ready prompts
- [references/geometric-craft.md](references/geometric-craft.md) — step 9 only
- [references/geometric-craft-guide.md](references/geometric-craft-guide.md) — step 9 only
- [references/color-system.md](references/color-system.md) — step 9 only
- [references/color-system-guide.md](references/color-system-guide.md) — step 9 only

## Hard Constraints

Do not:
- design icons one at a time when a set is requested — always think and balance across the whole set
- generate only one variant per icon — produce 2-3 distinct variants and pick a winner per icon (step 7)
- skip the second-eye critique pass (step 8 / Pass B) — the consistency audit alone does not catch craft regressions
- skip the grader-driven regeneration loop (step 8 / Pass C) on hi-end — the algorithmic grader catches measurement failures Pass B's LLM judgment misses
- skip the Brand DNA step — icons must inherit, not invent
- skip the icon system rules gate — user must confirm grid / stroke / style / accessibility budget before generation
- mix incompatible stroke weights or terminal styles in one set
- treat geometric pixel equality as optical equality at 20pt
- claim Tab Bar readiness without selected and unselected states
- claim Bottom Nav readiness without active / inactive states
- substitute system icons (SF Symbols / Material) silently when brand-coherence is required
- generate full production package before user confirms direction
- self-select between alternative icon-system rule sets — present and wait for user choice
- ignore the existing app icon set without saying so explicitly
- ask broad questions when a labeled assumption suffices
- present geometry without a construction grid
- use color to rescue a weak silhouette
- ship a state-pair that distinguishes only by color — fails for color-blind users; pair with shape (filled vs outlined)
- ship without a 3:1 non-text contrast check on every theme the icon will render in
- ship a style-pack icon without first verifying brand DNA permits it (every style pack has a "Refuse if" condition — honor it)
- treat Animated/Lottie as a visual style pack — motion is a separate subsystem with its own spec, fallback, and validation
- ship animated icons without a static frame and reduced-motion substitute
- ship a custom `.style-pack` without validating its manifest
- blend multiple style-pack winners after A/B/C review without explicitly locking one dominant style
- run stochastic hand-drawn jitter without documenting the seed and amplitude
- ship pixel-art icons without bitmap-aware native-size validation
- claim a `.pen` file was inspected without using Pencil MCP — `.pen` files are encrypted; `Read`/`Grep` returns garbage
- claim Figma context was used without actually invoking the Figma MCP
- assume a design-tool MCP is connected — detect first, then state the source explicitly

## Success Criteria

### Both tiers
Brand-coherent, platform-correct, set-consistent across every category in scope, legible at 20pt, project-aligned, WCAG 2.2 AA accessible (3:1 non-text contrast, 44pt iOS / 48dp Android touch targets, screen-reader labels, color-blind-safe state distinction), documented, package-ready.

### Hi-end (additional)
Optically corrected per icon, geometrically constructed, cross-icon weight balanced, context-validated in real Tab Bar / Bottom Nav, validated under Material You themed palettes, WCAG 2.2 AAA where requested.

### Failure signals
Single icon dominates the row → set not balanced. Stroke weights drift across set unintentionally → consistency failed. Icons require labels at intended size → legibility failed. Brand DNA invented vs inherited → not on brief. Selected/unselected states ambiguous → state distinction failed. State distinction relies on color alone → accessibility failed. Touch target below 44pt iOS / 48dp Android → accessibility failed. `.pen` file claimed inspected without Pencil MCP → false provenance.
