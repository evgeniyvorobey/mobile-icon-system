# Workflow

Full workflow for the icon system skill, expanded from `SKILL.md`. 13 phases, two quality tiers (Standard / Hi-end). Use this as the canonical reference when running a complete icon-system project.

## Quality Tiers

### Standard (default)

- 8-dimension evaluation matrix
- Small-size legibility checks (16/20/24pt as applicable)
- Basic platform validation (iOS Tab Bar OR Android Bottom Nav, both states)
- Cross-icon consistency audit
- Single state per icon if Tab Bar / Bottom Nav not in scope

### Hi-end

- All Standard checks plus:
- Per-icon optical correction (diagonal compensation, circle overshoot, negative-space density)
- Cross-icon stroke optical balancing (visual weight match across set)
- Path cleanliness audit
- Full Tab Bar AND Bottom Nav validation including themed (Material You) state
- Anchor reduction
- Tangent continuity verification

### Triggers for Hi-end

- User requests premium / craft-level quality
- App has large user base (1M+ users)
- Custom brand identity (not generic Material/SF)
- Reference to small-size precision (16pt requirement)
- Multi-language launch
- Theming required (Material You, custom theme system)

## Phase Map

| Phase | Standard | Hi-end | Notes |
|---|---|---|---|
| 1. Classify request | ✓ | ✓ | |
| 2. Establish Brand DNA | ✓ | ✓ | |
| 3. Audit current UI | ✓ | ✓ | |
| 4. Build context | ✓ | ✓ | |
| 5. Define icon system rules (gate) | ✓ | ✓ | mandatory user-confirmation gate |
| 6. Define vocabulary | ✓ | ✓ | |
| 7. Generate the set (variants then pick) | ✓ (2 variants) | ✓ (3+ variants) | per-icon variant generation, justified pick |
| 8. Audit (consistency + second-eye) | ✓ | ✓ | mandatory; loops back to phase 7 on regression |
| 9. Craft pass | skip | ✓ | hi-end only; uses calibration corpus |
| 10. Evaluate | ✓ | ✓ | |
| 11. Validate in context | ✓ | ✓ | hi-end adds themed + competitor row |
| 12. Improve or question | ✓ | ✓ | |
| 13. Package | ✓ | ✓ | |

## Phase 1 — Classify the Request

Determine which mode applies:

- **Icon system creation** — new set from scratch
- **Single icon addition** — adding one icon to an existing set (must inherit existing system rules)
- **Icon set audit / refinement** — evaluate or improve an existing set
- **Packaging** — handoff prep for an already-validated set
- **Export-readiness audit** — check ship-readiness without redesign

Choose tier (Standard / Hi-end) and state in first response.

## Phase 2 — Establish Brand DNA

Read [`brand-dna-input.md`](brand-dna-input.md). Three self-contained input modes — the skill does not depend on any other tool or generator to acquire Brand DNA:

1. Read an existing `brand-dna.md` from the project (regardless of who or what created it)
2. Extract from project brand assets (logo SVG, design-system files, or via a connected design-tool MCP — see [`design-tool-integrations.md`](design-tool-integrations.md))
3. Ask the user directly via a guided conversation

State Brand DNA source explicitly (`Brand DNA source: ...`).

If extracting in Mode 2, ask the user to confirm extracted DNA before proceeding. Optionally write the confirmed Brand DNA to `./brand/brand-dna.md` so future runs can use Mode 1.

## Phase 3 — Audit Current UI

Read [`project-audit.md`](project-audit.md). Inspect:

- Current icon set (if any) in the project
- App screenshots showing current UI
- Color tokens and design system files
- Typography choices

Build a UI snapshot: stroke weight, optical sizing, metaphor abstraction level, current cliché load.

If existing set is present, decide redesign tolerance:
- **Evolutionary** — refine existing set, preserve recognition
- **Adjacent** — same metaphors, new construction
- **Reset** — fresh start, new metaphors and construction

## Phase 4 — Build Context

Extract:
- App category
- Navigation structure (which tabs / nav items exist)
- Full icon inventory required (Tab Bar, action, system, media, status, communication, commerce, content, social, editing, time, location, security — see [`icon-vocabulary.md`](icon-vocabulary.md) coverage map)
- Platform priority (iOS / Android / cross-platform)
- State requirements (selected/unselected for Tab Bar; pressed / disabled for action icons)
- System icon coexistence
- Target locales and languages (informs cross-cultural metaphor choices)
- Accessibility tier (WCAG AA default, AAA if user requests) — see [`accessibility.md`](accessibility.md)

Preserve user's existing direction unless they ask for a reset.

## Phase 5 — Define Icon System Rules (MANDATORY GATE)

Read [`icon-grid-construction.md`](icon-grid-construction.md), [`cross-icon-consistency.md`](cross-icon-consistency.md), and [`accessibility.md`](accessibility.md).

Output:
- Base grid (24/20/16) + live area
- Stroke weight + diagonal compensation rule
- Style (filled / outlined / both)
- Selected/unselected state pairing logic (must distinguish via shape, not color alone — accessibility constraint)
- Optical sizing protocol
- Terminal style + corner radius logic
- Color application rules
- Accessibility budget: contrast target (3:1 minimum, 4.5:1 if any text inside icons), touch-target rule (44pt iOS / 48dp Android), reduced-motion fallback policy

**Stop. Ask user to confirm rules. Do not proceed to vocabulary or generation.**

This gate exists because changing rules mid-set requires regenerating everything. Catch disagreement before mass work.

## Phase 6 — Define Vocabulary

Read [`icon-vocabulary.md`](icon-vocabulary.md). For each icon needed:
- Confirm metaphor (avoid clichés)
- Note recognition risks
- Note cross-cultural readability
- Note state requirements (filled + outlined for Tab Bar)

Output a vocabulary table for user review.

## Phase 7 — Generate the Set (variants then pick)

**One batch, all icons.** Never generate one at a time — set-level consistency requires set-level thinking.

For every icon in scope, generate **3 distinct variants** (2 minimum for Standard tier; hi-end always 3+). Variants must differ on at least two of:
- Primitive choice (which geometric primitives are recruited for this metaphor)
- Anchor distribution and density
- Optical correction strength (conservative / standard / pronounced)
- Terminal angle interpretation
- Negative-space allocation (counter-form size, trapped space distribution)

Each variant:
- Built on agreed grid
- Inherits Brand DNA
- Outputs both states if Tab Bar
- Schematic SVG inline, no production polish yet

After all variants are produced, read [`concept-quality.md`](concept-quality.md), [`craft-rubric.md`](craft-rubric.md), [`negative-space.md`](negative-space.md), and [`aesthetic-principles.md`](aesthetic-principles.md). For each icon, score every variant against the rubric and **pick a winner with explicit per-axis reasoning**. Present:
- The winning set as the primary deliverable
- A collapsed appendix containing the runner-ups per icon, so the user can request a swap

Per-icon verification on the winners: meaning, silhouette, recognition at intended size, negative-space coherence, anchor economy.

**Why this exists.** Generate-once-pick-once produces "first idea" icons. Designers iterate. Forcing N variants forces the search space to widen, and forcing a justified pick exposes the construction reasoning. This is the difference between "an icon" and "the icon".

## Phase 8 — Audit (consistency + second-eye critique)

Two mandatory passes. Both apply to the winning set chosen in phase 7. Standard tier runs both; hi-end runs both before the craft pass.

### Pass A — Cross-icon consistency

Read [`cross-icon-consistency.md`](cross-icon-consistency.md). Run the full 6-step audit:

1. Stroke audit
2. Terminal + join audit
3. Corner radius audit
4. Visual weight audit (squint test)
5. Optical centering audit
6. State-pair audit (if Tab Bar)

### Pass B — Second-eye critique

This is the "sleep on it" pass that separates craft from competence. The model must step out of the brand context and read the set as if seeing it fresh.

1. Re-read [`craft-rubric.md`](craft-rubric.md), [`negative-space.md`](negative-space.md), [`aesthetic-principles.md`](aesthetic-principles.md). Do NOT re-read the brief, Brand DNA, or rules — read the icons as a stranger would.
2. Score every icon A/B/C across each rubric axis (anchor economy, optical correction, terminal precision, negative-space rhythm, silhouette quality, family resemblance, intentionality, restraint).
3. For any axis scoring below B on any icon: **loop back to phase 7** for that icon only. Regenerate 3 fresh variants, apply rubric, re-pick. Do not regenerate the whole set.
4. Cap loop iterations at 2 per icon. If still below B after 2 loops, document the unresolved gap in the audit output and surface it as a punch-list item in phase 12.
5. Loops are token-expensive but cheap relative to shipping mediocre icons. Do not skip loops to save tokens unless the user explicitly requests minimal mode.

### Output

- Per-icon scorecard (A/B/C per axis, both passes)
- Corrections made
- Loop iterations per icon
- Remaining risks

This phase is the single biggest quality lever in the workflow. Do not collapse it into phase 10 (Evaluate) — evaluation scores; this phase fixes.

## Phase 9 — Craft Pass (Hi-end Only)

> Standard tier skips to phase 10. **Load craft files only at this step.**

Read [`geometric-craft.md`](geometric-craft.md), [`color-system.md`](color-system.md).

Per-icon:
- Optical corrections applied
- Path cleanliness verified
- Anchor reduction
- Tangent continuity G1+
- Pixel alignment at all target sizes

Cross-icon:
- Stroke optical balancing (visual weight, not numeric)
- Color application consistent across set

Output: corrections made, remaining risks, updated SVG masters.

## Phase 10 — Evaluate

Read [`icon-set-evaluation.md`](icon-set-evaluation.md). Score the set on the 8-dimension matrix.

Composite score, per-dimension notes, ship verdict (ship / ship with follow-ups / re-work needed).

## Phase 11 — Validate in Context

Read [`tab-bar-validation.md`](tab-bar-validation.md) and [`accessibility.md`](accessibility.md). Mandatory contexts:

- iOS Tab Bar (light + dark) — required when Tab Bar is in scope
- Android Bottom Nav (light + dark) — required when Bottom Nav is in scope
- Action icons rendered on their target surfaces (toolbar, button, list row)
- System / status icons in their use context (alert, banner, list affordance)
- Themed (hi-end) — Material You dynamic palettes
- Competitor row (hi-end)
- Small-size fallback if applicable
- Accessibility validation (run the [`accessibility.md`](accessibility.md) checklist): 3:1 non-text contrast in every theme, 44pt iOS / 48dp Android touch-target verification, deuteranopia simulation pass, single-color collapse fallback, Dynamic Type pass for inline icons

Render mockups and verify each context.

## Phase 12 — Improve or Question

Identify:
- Weakest icon
- Weakest dimension
- 2-3 concrete improvement moves in priority order

Ask only high-leverage questions. Proceed with labeled assumptions where possible.

## Phase 13 — Package

Read [`package-spec.md`](package-spec.md) and [`design-tool-integrations.md`](design-tool-integrations.md) when a design-tool MCP is connected. Output:
- SVG masters per icon
- Platform exports (iOS PDF, Android vector drawable)
- Usage guidance per surface
- Naming convention
- Accessibility notes (labels per locale, traits, contrast measurements, reduced-motion fallbacks) — see [`accessibility.md`](accessibility.md)
- Design-tool handoff (Figma Code Connect mappings, Pencil exports) when an MCP is connected
- Export checklist
- Unresolved risks

Scaffold via `scripts/init_icon_system_package.py` if a real handoff folder is needed.

## Stopping Conditions

The workflow halts at:

- Phase 5 gate — until user confirms rules
- Phase 8 Pass B — loops back to Phase 7 on craft regression (not a halt, an iteration); cap at 2 loops per icon
- Phase 12 — when 2+ unresolved questions block progress

Do not self-resolve gate decisions. Do not proceed without explicit user confirmation.

## Iteration Loops

The workflow has two intentional loops:

1. **Variant search (within Phase 7)** — N variants per icon, then pick. The "loop" is internal to phase 7; it doesn't iterate over phases.
2. **Craft regression (Phase 8 Pass B → Phase 7)** — when second-eye critique scores any icon below B on any axis, regenerate that icon only. Cap at 2 iterations per icon to bound cost.

Both loops are mandatory. They are the difference between "first idea" output and craft-level output.
