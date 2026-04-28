# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/).

## [0.4.0] — 2026-04-28

Density release. The skill now (a) **closes the grader → regen loop** so grader findings automatically feed into a regeneration brief the LLM consumes; (b) **detects two semantic failure classes programmatically** (anti-example similarity via pHash; color-only state distinction) and promotes them from warn to hard_fail; (c) **expands the calibration corpus from 27 to 118 SVGs covering 44 metaphors** with 9 explicit state pairs, 6 native-small (16/20pt) exemplars, and 5 duotone exemplars; (d) **fills color-system.md with a 1500-word workflow reference + a 3500-word deep dive** spanning OKLCH, HCT, Material You, iOS Dynamic Color, CSS Color 4, and Display P3; (e) **adds 3 visual style packs** (Liquid Glass, chromatic duotone, claymorphism) with full construction rules, anti-patterns, brand-DNA mappings, and accessibility implications; (f) **adds 10 vertical-domain catalogs** (music, finance, health, productivity, e-commerce, social, dev-tools, transportation, education, gaming) plus a cross-domain shape-collision file disambiguating 10 patterns where the same icon means different things in different verticals.

### Added

- **Render-Grade-Regenerate loop** ([`scripts/grade_with_fixes.py`](scripts/grade_with_fixes.py) + [`scripts/grade/fix_brief.py`](scripts/grade/fix_brief.py)): emits a per-icon `regeneration_brief.md` with specific actionable fix instructions, citations to craft-rubric.md sections, and tier-A reference corpus links. Workflow phase 8 now includes Pass C (grader-driven regeneration). Capped at 2 iterations per icon.
- **Semantic failure checks** ([`scripts/grade/anti_example_similarity.py`](scripts/grade/anti_example_similarity.py), [`scripts/grade/color_only_state.py`](scripts/grade/color_only_state.py)): pHash distance against tier-c corpus catches near-clones of documented anti-examples (gendered profile silhouettes, color-only state distinctions, over-detailed glyphs). Promoted from warn to hard_fail in v0.4. New `craft-rubric.md` §10 documents the algorithms.
- **Calibration corpus expansion**: 88 new SVGs + 88 `.notes.md` files across `tier-a/`, `tier-b/`, `tier-c/`, plus new tier directories `tier-a-mini/` (5 native-16pt Heroicons), `tier-a-micro/` (1 native-20pt Heroicon), and `tier-a-duotone/` (5 Phosphor duotone exemplars). 9 explicit state pairs (Lock/Unlock, Eye/Eye-off, Chevron L/R, Download/Upload, Mic/Mic-off, Star out/fill, Bookmark out/fill, Cloud/Cloud-off, Battery {full,low,charging}). 3 hand-crafted custom tier-c anti-examples. License-clean (MIT/ISC/Apache-2.0). Manifest tracks 118 SVGs total.
- **[`references/color-system.md`](references/color-system.md) + [`references/color-system-guide.md`](references/color-system-guide.md)**: filled out from v0.1 scaffold. 4-mode framework (Mode A monochrome / B duotone / C accent / D multi), contrast budgets per surface (WCAG 1.4.11), color-blind-safe status palette in OKLCH (success 140°, error 25° to avoid deuteranopia collapse with green), Material You / iOS Dynamic Color / CSS Color 4 deep dive, 8-step palette generation algorithm, 15-item audit checklist, 10 diagnostic recipes.
- **[`references/style-packs/`](references/style-packs/) — 3 visual style packs + README**: Liquid Glass (4-layer recipe with squircle radius `0.2237 × side`, specular `stdDeviation=2.4`, shadow `stdDeviation=6 dy=3`, centroid shift 1.2-1.8% downward); Chromatic Duotone (2-layer disjoint paths, secondary opacity 0.30-0.36 light / 0.38-0.44 dark, hue distance ≤60°, secondary mass +4-6% optical compensation); Claymorphism (Hype4 canonical recipe with body L 40-60% pastel clamp ≤70%, outer shadow `dy=4 stdDeviation=8` opacity 0.38-0.46, body-hue tinted shadows). Each style includes brand-DNA mapping table, "Refuse if" conditions, accessibility implications, anti-patterns, workflow integration per phase.
- **[`references/domain-metaphors/`](references/domain-metaphors/) — 12 files**: 10 vertical-domain catalogs (music, finance, health, productivity, e-commerce, social, dev-tools, transportation, education, gaming) — each with industry overview citing pioneering apps (Spotify shuffle/repeat shape disambiguation, Robinhood gain/loss chevron, Apple Health activity rings, Notion block handles, Stripe transaction lists, etc.), 18-22 metaphors per domain with structured fields (Meaning / Recommended forms / Cliché / Cross-cultural / Reference / Universal vocabulary cross-ref), per-domain cliché map, 3-5 state-pair examples. Plus [`_cross-domain.md`](references/domain-metaphors/_cross-domain.md) — 10 cross-domain shape-collision patterns disambiguating where the same icon (paper airplane, lightning, heart, refresh, cloud, group, calendar) means different things in different verticals. Plus [`README.md`](references/domain-metaphors/README.md) with load policy: skill loads only the matched domain in Phase 6, not all 10.
- **Workflow integration**: Phase 4 (Build context) now matches user-stated app domain to one of 10 domain catalogs. Phase 5 (Rules gate) adds visual-style declaration (default monochrome / duotone-mono / one of 3 style packs). Phase 6 (Define vocabulary) loads matched domain catalog + cross-domain patterns + universal vocabulary. Phase 8 adds Pass C (grader-driven regeneration loop). Phase 8 hard_fails on semantic checks (anti-example similarity, color-only state).
- New required output-contract field: `Visual style:` (default monochrome / duotone-mono / liquid-glass / duotone-chromatic / claymorphism).

### Changed

- **`SKILL.md` Hard Constraints**: added "do not ship a style-pack icon without first verifying brand DNA permits it" (every style has a "Refuse if" condition).
- **`scripts/grade/report.py`**: `hard_fail_keys` now includes `silhouette`, `anti_example_similarity`, `color_only_state` (the two semantic checks added in v0.4).
- **`scripts/grade/config.py`**: added `anti_example` and `color_only_state` config blocks with thresholds.
- **`scripts/fetch_references.py`**: extended CORPUS to 88 new entries; manifest grew to 118 verified SVGs; 3 new custom tier-c files registered.
- **`assets/references/README.md`**: gap list updated for v0.5 (15 items now: pause/stop/skip media controls, volume+mute pair, cast/AirPlay/PiP, map/compass/nav arrow turn-by-turn, accessibility/help/info/theme, trending/live/record, group/community/follow/block, cart-vs-bag-vs-wallet trio, archive/file-type variants, more tier-c coverage, multi-library tier-A picks for high-traffic metaphors, Material Symbols Outlined + Carbon at tier-A, native large-size 32/40pt exemplars, animated state transitions in `tier-d-motion/`).
- **CI**: new grade smoke tests for `grade_with_fixes`, `anti_example_similarity`, `color_only_state` added to existing grade job.
- **Repo validator**: `MARKDOWN_GLOBS` now traverses `references/style-packs/` and `references/domain-metaphors/` so cross-link checks cover them.

### Notes

- **Three new tier-A icons (`banknote.svg`, `fingerprint.svg`, `scissors.svg`) hard_fail the silhouette stability check at 16pt** — small details (Lucide banknote's `.01`-length serial dots; Phosphor fingerprint's intentionally offset loops; Lucide scissors' finger-loop+blade gap) collapse below 20pt. These are inherent traits of the upstream construction, not regressions. Each `.notes.md` documents the limitation explicitly: tier-A at 24pt+, paired with a tier-a-mini variant for sub-20pt contexts. The grader's hard_fail on these icons is informative — it teaches "tier-A craft can be size-bound."
- The v0.3 calibration finding (alignment threshold 0.50 default + math-derivation exemption documented in `craft-rubric.md` §2) carries forward unchanged — most new tier-A icons trip alignment as warn (math-derived endpoints), no regression.
- Reference files now substantially complete. Remaining v0.1 scaffold-only file: `geometric-craft-guide.md` long-form (the short `geometric-craft.md` is filled).
- The corpus has reached the **size-of-corpus diminishing-returns boundary at ~120 SVGs**. v0.5 expansion should be additive in *kind* (filling v0.5 gap categories) rather than additive in *count*.
- Backward compatibility: no schema changes to `assets/package-template/`. Existing v0.3 packages and prompts remain valid; visual-style + domain catalog selections are workflow additions, not signature changes.

## [0.3.0] — 2026-04-27

Craft release. The skill now (a) ships a calibration corpus of tier-A/B/C reference SVGs so generators can compare instead of guess, (b) requires generate-N-pick-1 variant search per icon, (c) runs a mandatory second-eye critique loop that can iterate back to generation, (d) loads numerical craft thresholds with cited sources, (e) treats negative space as a primary design element, (f) loads ten aesthetic principles from the design canon, and (g) ships a Python render-and-grade pipeline that actually rasterizes SVG output and measures it against the rubric.

### Added

- **Calibration corpus** ([`assets/references/`](assets/references/)): 27 hand-curated SVGs across three tiers — 16 tier-A craft exemplars (Lucide, Phosphor, Tabler), 6 tier-B competent examples (Heroicons mostly), 5 tier-C anti-examples (3 hand-crafted custom failure cases plus 2 from upstream libraries that drifted). Every SVG ships with a `.notes.md` file containing path-data craft observations sourced verbatim from the research phase. License-clean (MIT/ISC/Apache-2.0); SHA256 manifest in [`assets/references/manifest.json`](assets/references/manifest.json) with refresh script [`scripts/fetch_references.py`](scripts/fetch_references.py). Loaded by phase 7 (variant pick) and phase 9 (hi-end craft pass) so the LLM compares its output against tier-A construction principles.
- **Numerical craft rubric** ([`references/craft-rubric.md`](references/craft-rubric.md)): 8 sections of cited thresholds (optical correction, pixel-grid alignment, anchor economy, stroke uniformity, curve quality, negative space, set-level balance, squint/blur tests). Sources: Apple HIG, Material Design 3, W3C SVG, WCAG 2.2, Cheng *Designing Type*, Müller-Brockmann, Pomax bezierinfo, Phosphor/Lucide design notes. Open TODOs explicitly flagged for thresholds where literature is silent.
- **Negative space reference** ([`references/negative-space.md`](references/negative-space.md)): counter-form, trapped space, named negatives, density rhythm, hierarchy through emptiness, gestalt closure. Cited Lupton (*Thinking with Type*), Cheng (*Designing Type*), Müller-Brockmann, Tschichold, Wertheimer (gestalt), Arnheim. 5-step audit checklist + numerical thresholds.
- **Aesthetic principles reference** ([`references/aesthetic-principles.md`](references/aesthetic-principles.md)): 10 principles with rationale, application, anti-example, citation. Sources: Vignelli (*Canon*), Rams ("Ten Principles"), Müller-Brockmann (*Grid Systems*), Tschichold (*The New Typography*), Bringhurst (*Elements of Typographic Style*), Lupton, Cheng, Wathan & Schoger (*Refactoring UI*), Arnheim, Chimero (*The Shape of Design*).
- **Critique loop in workflow** (phase 8 expanded): two-pass audit — Pass A consistency, Pass B second-eye critique applying the rubric with explicit "step out of the brand context" instruction. Loops back to phase 7 for any icon scoring below B on any axis. Capped at 2 loop iterations per icon.
- **Generate-N-pick-1 in workflow** (phase 7): each icon generated as 3 distinct variants (2 minimum for Standard tier; hi-end 3+) varying primitive choice / anchor distribution / optical correction strength / terminal angle / negative-space allocation. Winner picked with explicit per-axis reasoning; runner-ups in collapsed appendix.
- **Render-and-grade pipeline** ([`scripts/grade/`](scripts/grade/) package + [`scripts/render_and_grade.py`](scripts/render_and_grade.py) CLI): rasterizes SVG via `resvg_py` (Rust, sub-100ms/icon, no system deps), runs 8 algorithmic checks (silhouette legibility, weight, alignment, stroke uniformity, squint/blur, pair distinction, set-level balance, optional perceptual-hash reference comparison). 10 smoke tests, all pass. Calibrated against the tier-A corpus — alignment + single-icon weight are warn-by-default to avoid false positives on math-derived endpoints (e.g., Lucide bell's clapper at `12 ± √3`); `--strict` flag re-promotes to hard-fail. New CI job on Python 3.9 + 3.12, no `apt-get` required.
- **Per-metaphor reference blocks in [`references/icon-vocabulary.md`](references/icon-vocabulary.md)**: 14 of the most common metaphors now cite specific tier-A/B/C corpus files with one-line craft observations.
- New required output-contract fields: skill responses now declare design-tool source, set scope, and accessibility tier explicitly (carried from v0.2 plus the variant-pick reasoning per icon).

### Changed

- **`SKILL.md` workflow phase 7**: replaces single-batch generation with mandatory variant-search-then-pick.
- **`SKILL.md` workflow phase 8**: expands single consistency audit into two passes (consistency + second-eye critique) with loop-back capability.
- **`SKILL.md` workflow phase 9**: hi-end craft pass now references the calibration corpus for direct comparison.
- **`SKILL.md` Hard Constraints**: added "do not generate single variant per icon", "do not skip second-eye critique pass".
- **`SKILL.md` Success Criteria**: hi-end now requires comparison with corpus where a tier-A reference exists.
- **`references/craft-rubric.md` §2**: added math-derivation exemption note so the integer-anchor rule doesn't false-positive on tier-A icons.
- **Repo validator** ([`scripts/validate_skill_repo.py`](scripts/validate_skill_repo.py)) now requires the 3 new reference files.
- **Claude wrapper** + **install_skill.py wrapper template** + **`.claude/skills/mobile-icon-system/SKILL.md`** updated to load the new references.

### Notes

- Reference files in this release are now substantially filled — `craft-rubric.md`, `negative-space.md`, `aesthetic-principles.md` ship complete with cited sources. Only a handful of v0.1.0 scaffolds remain (`geometric-craft-guide.md`, `color-system-guide.md` long-form versions), to be filled when needed.
- The render-and-grade pipeline adds new pip dependencies (`resvg_py`, `numpy`, `Pillow`, `scipy`, `imagehash`). Existing usage that doesn't invoke the grader is unaffected — none of the existing scripts pulled these in.
- Calibration corpus initial release covers 14 high-leverage metaphors. Gap analysis in [`assets/references/README.md`](assets/references/README.md) identifies expansion areas (filter, lock, eye, chevrons, duotone exemplars, 16/20pt-native variants, RTL-mirrored sub-corpus). Future minor releases will fill.
- Backward compatibility: no schema changes to `assets/package-template/`. Existing v0.2.0 packages and prompts remain valid; the new variant-pick discipline is opt-in by default and on for hi-end.

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
