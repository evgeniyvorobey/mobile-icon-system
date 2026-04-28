# Mobile Icon System Skill

**Current version: 0.5.0** | [Changelog](CHANGELOG.md) | [Migration guide](MIGRATION.md)

A self-contained AI skill for Codex and Claude that designs, refines, audits, motion-enables, client-reviews, and packages the **full brand icon set** for a mobile app — Tab Bar / Bottom Nav, action, system, media, status, communication, commerce, content, social, editing, time, location, and security icons — all inheriting one Brand DNA, validated for WCAG 2.2 accessibility and grade-checked against a hand-curated craft rubric, and shipped as platform-ready iOS/Android assets.

It is built for real product UI work, not generic icon-pack generation. The skill is fully standalone — it does not depend on any other skill or external generator — integrates with Figma and Pencil MCP servers when available, ships a calibration corpus of tier-A/B/C reference icons so generators can compare instead of guess, includes render-and-grade pipelines that rasterize SVG output and measure it against numerical thresholds, supports custom `.style-pack` plugins, adds a separate Animated/Lottie motion subsystem, and falls back to filesystem-only mode when no design-tool MCP is connected.

## Contents

- [What It Does](#what-it-does)
- [What It Is Not](#what-it-is-not)
- [Key Capabilities](#key-capabilities)
- [Quality Tiers](#quality-tiers)
- [Installation](#installation)
- [Production Package](#production-package)
- [Repository Structure](#repository-structure)
- [Versioning](#versioning)
- [Validation](#validation)
- [Ready-To-Use Prompts](#ready-to-use-prompts)
- [Suggested Usage Pattern](#suggested-usage-pattern)
- [Compatibility](#compatibility)
- [Canonical Files](#canonical-files)

## What It Does

1. ingest Brand DNA self-contained — read an existing `brand-dna.md` (regardless of who or what wrote it), extract from project brand assets, or guide the user through a brief intake
2. inspect the current app's UI patterns and icon set first — via Figma MCP, Pencil MCP, or filesystem (whichever is available)
3. verify current platform guidance for Tab Bar / Bottom Nav and WCAG 2.2 amendments when freshness matters
4. define icon system rules (grid, stroke, terminals, states, accessibility budget) — wait for user confirmation
5. generate the full brand icon set in one batch, balanced across the row, covering every category in scope — or generate the same set in three visual styles for A/B/C client review
6. run a cross-icon consistency audit and a WCAG 2.2 accessibility audit
7. evaluate the set on icon-specific dimensions and validate in real Tab Bar / Bottom Nav / action / status surfaces
8. create and validate animated-icon motion specs with static reduced-motion fallbacks when motion is in scope
9. scaffold a real handoff package with platform-ready exports, accessibility notes, motion notes, and design-tool handoff (Figma Code Connect / Pencil exports) when an MCP is connected

## What It Is Not

- Not a full-coverage utility icon library — for hundreds of generic glyphs, start with [SF Symbols](https://developer.apple.com/sf-symbols/), [Material Symbols](https://fonts.google.com/icons), [Lucide](https://lucide.dev), [Tabler](https://tabler.io/icons), or [Phosphor](https://phosphoricons.com)
- Not an illustration tool
- Not a single-decorative-graphic generator
- Not a long-form character animation tool — Lottie support is scoped to product UI icon motion
- Not for app launcher / home screen marks — those need different construction rules; pair with a dedicated logo workflow

## Key Capabilities

- **Self-contained** — no dependency on any other skill, generator, or external service. All inputs come from the project, the user, or a connected design-tool MCP
- **Full brand icon set scope** — covers Tab Bar / Bottom Nav, action, system, media, status, communication, commerce, content, social, editing, time, location, security categories (~50–80 icons in a typical app set), all inheriting one Brand DNA
- **Accessibility-first** — WCAG 2.2 AA by default (3:1 non-text contrast, 44pt iOS / 48dp Android touch targets, screen-reader labeling, color-blind-safe state distinction, Dynamic Type, reduced motion, Forced Colors fallback), AAA where requested. Dedicated [`references/accessibility.md`](references/accessibility.md)
- **Design-tool integration** — first-class Figma MCP and Pencil MCP support; pulls Brand DNA from Figma libraries, reads `.pen` files via Pencil MCP (required — `.pen` is encrypted), pushes back via Code Connect. Falls back to filesystem-only mode when no MCP is available. Dedicated [`references/design-tool-integrations.md`](references/design-tool-integrations.md)
- Brand DNA ingestion with three self-contained input modes (read existing `brand-dna.md`, extract from project, guided intake)
- Project-first UI audit using local screenshots, design boards, color tokens, current icon set, or design-tool MCP
- Icon system rules definition with mandatory user-confirmation gate before mass generation
- Set-level generation with cross-icon consistency built in
- **Multi-style parallel generation** — one set in three visual styles for A/B/C client review, with shared vocabulary and decision logging via [`references/multi-style-review.md`](references/multi-style-review.md) and [`scripts/init_multi_style_review.py`](scripts/init_multi_style_review.py)
- **Style-pack plugins** — user `.style-pack` manifests validated with [`scripts/validate_style_pack.py`](scripts/validate_style_pack.py) before custom construction rules enter the Phase 5 gate
- **Animated/Lottie subsystem** — separate motion specs, easing, static frames, and reduced-motion fallback validation via [`references/motion-system.md`](references/motion-system.md) and [`scripts/validate_motion_spec.py`](scripts/validate_motion_spec.py)
- Live research workflow for Apple HIG Tab Bar, Material 3 Bottom Nav, and WCAG amendments
- 8-dimension icon-set evaluation matrix
- Tab Bar / Bottom Nav context validation with selected and unselected states
- Hi-end craft pass: per-icon optical correction, cross-icon stroke balancing, path cleanliness
- **Expanded shipped style packs** — Liquid Glass, chromatic duotone, claymorphism, 3D/isometric, pixel-art, and hand-drawn; pixel-art adds bitmap-aware checks and hand-drawn uses deterministic path jitter
- Production package scaffolding via [`scripts/init_icon_system_package.py`](scripts/init_icon_system_package.py)
- Repository validation via [`scripts/validate_skill_repo.py`](scripts/validate_skill_repo.py)

## Quality Tiers

The skill supports two quality tiers:

- **Standard** — base evaluation matrix, small-size legibility checks at target sizes (16/20/24pt), basic platform validation. Default for most requests.
- **Hi-end** — full craft pipeline. Adds per-icon optical correction, cross-icon stroke balancing, comprehensive context testing across iOS Tab Bar and Android Bottom Nav with selected/unselected states. Activated when the work demands it.

See the tier selection triggers in [`SKILL.md`](SKILL.md) step 1.

## Installation

### Codex

Quick install (symlink, recommended):

```bash
python3 scripts/install_skill.py --codex
```

Copy instead of symlink:

```bash
python3 scripts/install_skill.py --codex --codex-mode copy
```

Default install path: `${CODEX_HOME:-$HOME/.codex}/skills/mobile-icon-system`

**Invocation:**

```text
Use $mobile-icon-system.

Generate the full brand icon set for this app — Tab Bar, action,
system, status, and content icons. Read the brand-dna.md if it exists,
otherwise extract Brand DNA from our logo. Define the icon system rules
including the accessibility budget (3:1 contrast, 44pt touch targets)
and ask me to confirm before generating the set.
```

### Claude

Quick install into a Claude project:

```bash
python3 scripts/install_skill.py --claude-project /path/to/your/project
```

Symlink instead of copy:

```bash
python3 scripts/install_skill.py --claude-project /path/to/your/project --claude-mode link
```

This creates:
- a Claude wrapper at `.claude/skills/mobile-icon-system/SKILL.md`
- a vendor copy of the repo at `.claude/vendor/mobile-icon-system`

**Invocation:**

```text
/mobile-icon-system generate the full brand icon set for this app
```

### Both at once

```bash
python3 scripts/install_skill.py --codex --claude-project /path/to/your/project
```

### Upgrading

Rerun with `--force` to overwrite an existing install:

```bash
python3 scripts/install_skill.py --codex --force
```

The installer shows the version transition and warns about major upgrades.

### Using this repo directly

If you opened this repository as a Claude project, the skill is already available via `/mobile-icon-system`. No installation needed.

For Codex, load `SKILL.md` as the main skill entrypoint and `agents/openai.yaml` as metadata.

## Production Package

Scaffold a handoff package:

```bash
python3 scripts/init_icon_system_package.py /path/to/icon-system --project-name "Project Name"
```

Options:

```bash
python3 scripts/init_icon_system_package.py /path/to/icon-system \
  --project-name "Project Name" \
  --owner "Brand Team" \
  --date "2026-04-27"
```

This creates review files, rationale files, Tab Bar / Bottom Nav usage notes, and an export checklist.

## Repository Structure

```text
mobile-icon-system/
├── SKILL.md                            # canonical skill entrypoint
├── README.md
├── CHANGELOG.md
├── MIGRATION.md
├── LICENSE
├── .github/
│   └── workflows/
│       └── ci.yml                      # repo validation + smoke tests
├── .claude/
│   └── skills/
│       └── mobile-icon-system/
│           └── SKILL.md                # Claude wrapper
├── agents/
│   └── openai.yaml                     # Codex UI metadata
├── references/
│   ├── accessibility.md                # WCAG 2.2 AA/AAA, touch targets, screen readers, color-blind safety
│   ├── brand-dna-input.md              # Brand DNA ingestion (3 self-contained input modes)
│   ├── color-system.md                 # color application across the set
│   ├── color-system-guide.md           # color craft long-form
│   ├── concept-quality.md              # icon-set quality gates
│   ├── creative-divergence.md          # broader rule-set range when category feels generic
│   ├── cross-icon-consistency.md       # set-level balancing rules
│   ├── design-tool-integrations.md     # Figma MCP, Pencil MCP, generic MCP guidance
│   ├── evaluation.md                   # generic evaluation framework
│   ├── example-requests.md             # realistic request patterns
│   ├── example-responses.md            # gold-standard answer shape
│   ├── geometric-craft.md              # construction grids, optical corrections
│   ├── geometric-craft-guide.md        # geometric craft long-form
│   ├── icon-grid-construction.md       # 24/20/16 grids, keylines, stroke contrast
│   ├── icon-set-evaluation.md          # 8-dimension set scoring matrix
│   ├── icon-vocabulary.md              # full-set metaphor library, 13 categories
│   ├── live-research.md                # platform watchlists
│   ├── motion-system.md                # Animated/Lottie subsystem, easing, reduced-motion validation
│   ├── multi-style-review.md           # A/B/C client review workflow
│   ├── package-spec.md                 # final deliverables spec
│   ├── platform-icon-specs.md          # iOS Tab Bar + Android Bottom Nav specs
│   ├── production-resources.md         # scaffolding and handoff file guidance
│   ├── project-audit.md                # current UI snapshot
│   ├── prompt-library.md               # ready-to-use prompts
│   ├── sources.md                      # source map and authority order
│   ├── tab-bar-validation.md           # in-context Tab Bar / Bottom Nav testing
│   ├── workflow.md                     # full workflow phases
│   └── style-packs/                    # built-in and plugin visual style specs
├── assets/
│   └── package-template/
│       ├── reviews/                    # project-ui-snapshot, icon-system-rules, concept-scorecard, cross-icon-audit
│       └── selected/                   # rationale, usage-guidance, tab-bar-icon-notes, bottom-nav-notes, export-checklist
└── scripts/
    ├── install_skill.py                # install into Codex and/or Claude projects
    ├── init_icon_system_package.py     # scaffold handoff package from templates
    ├── init_multi_style_review.py      # scaffold A/B/C style review packages
    ├── validate_motion_spec.py         # validate animated-icon motion specs
    ├── validate_style_pack.py          # validate user .style-pack manifests
    ├── apply_path_jitter.py            # deterministic hand-drawn path jitter
    ├── render_icon_contact_sheet.py    # render icon set contact sheet (HTML + SVG)
    ├── validate_skill_repo.py          # validate repo structure and relative links
    ├── smoke_test_contact_sheet_browser.py # browser visual smoke test
    ├── smoke_test_contact_sheet.py     # contact sheet smoke test
    ├── smoke_test_installer.py         # installer smoke tests
    └── smoke_test_package_scaffold.py  # package scaffold smoke test
```

## Versioning

This skill uses [semantic versioning](https://semver.org/):
- **major** — breaking changes to templates, evaluation matrix, or workflow phases
- **minor** — new reference files or capabilities without breaking existing packages
- **patch** — typos, wording, link fixes

Show the current version:

```bash
python3 scripts/install_skill.py --version
```

See [`CHANGELOG.md`](CHANGELOG.md) for what changed in each version.
See [`MIGRATION.md`](MIGRATION.md) for step-by-step upgrade instructions.

## Validation

```bash
python3 scripts/validate_skill_repo.py        # structure, links, version consistency
python3 scripts/smoke_test_installer.py        # installer smoke tests
python3 scripts/smoke_test_contact_sheet.py    # SVG contact sheet smoke test
python3 scripts/smoke_test_contact_sheet_browser.py  # browser visual smoke test
python3 scripts/smoke_test_package_scaffold.py # package scaffold smoke test
python3 scripts/smoke_test_multi_style_review.py # A/B/C review scaffold smoke test
python3 scripts/smoke_test_motion_spec.py      # motion spec validator smoke test
python3 scripts/smoke_test_style_pack_plugin.py # .style-pack plugin validator smoke test
python3 scripts/smoke_test_path_jitter.py      # deterministic path-jitter smoke test
python3 scripts/smoke_test_grade_bitmap.py     # pixel-art bitmap grader smoke test
python3 scripts/install_skill.py --help        # installer options
```

The browser visual smoke test requires Node.js/npm (`npx`) and installs a temporary Playwright package. It opens the generated HTML contact sheet in headless Chromium and verifies visible icon SVGs plus key review sections.

## Ready-To-Use Prompts

Detailed prompts covering common scenarios: Tab Bar refresh aligned with existing logo, full icon set from scratch with brand DNA input, single icon addition to an existing system, icon-set audit without redesign, brand-coherent monochrome icon set.

Each prompt activates the appropriate workflow depth. Prompts work in both platforms and can be written in any language.

See the full prompt library: [`references/prompt-library.md`](references/prompt-library.md)

## Suggested Usage Pattern

1. ensure Brand DNA is available — write or paste an existing `brand-dna.md`, point to your logo SVG, or be ready to answer the guided intake
2. ask the skill to audit the current app UI — the skill will detect Figma MCP / Pencil MCP / filesystem and state the source
3. let it verify live platform guidance when freshness matters
4. ask for icon system rules including the accessibility budget — review and confirm before generation
5. ask for the full icon set, generated as one balanced batch across every category in scope (Tab Bar, action, system, media, status, communication, commerce, content, social, editing, time, location, security), or ask for a 3-style A/B/C review before production
6. let it run cross-icon consistency audit and the WCAG 2.2 accessibility audit; surface corrections
7. if hi-end: run the craft pass (geometric construction, optical corrections, color craft, themed-palette pass)
8. validate in Tab Bar / Bottom Nav and adjacent surface contexts with both states, plus the accessibility checklist (contrast, touch targets, color-blind simulation, Dynamic Type, reduced motion)
9. when icons animate, validate the motion spec before Lottie/dotLottie handoff
10. once a direction is validated, scaffold or fill the handoff package — including accessibility notes, motion notes, style-plugin manifests, and design-tool handoff (Figma Code Connect / Pencil exports) when MCP is connected

## Compatibility

- **Python**: 3.9+
- **Platforms**: Codex (OpenAI), Claude (Anthropic)
- **OS**: macOS, Linux. Windows works but the default symlink install mode (`--codex-mode link`) may require Developer Mode or elevated permissions — use `--codex-mode copy` on Windows to avoid this.
- **CI**: tested on Ubuntu with Python 3.9 and 3.12
- **Design-tool MCPs**: Figma MCP, Pencil MCP, or any generic design-tool MCP — auto-detected; filesystem-only fallback fully supported
- **License**: [MIT](LICENSE)

## Canonical Files

- Main skill: [`SKILL.md`](SKILL.md)
- Codex metadata: [`agents/openai.yaml`](agents/openai.yaml)
- Claude wrapper: [`.claude/skills/mobile-icon-system/SKILL.md`](.claude/skills/mobile-icon-system/SKILL.md)
- Research and workflow references: [`references/`](references)
- Package templates: [`assets/package-template/`](assets/package-template)
- Utility scripts: [`scripts/`](scripts)
- Changelog: [`CHANGELOG.md`](CHANGELOG.md)
- Migration guide: [`MIGRATION.md`](MIGRATION.md)
- License: [`LICENSE`](LICENSE)
