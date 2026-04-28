# Production Resources

Guidance on scaffolding handoff packages and using the production scripts. Use this when packaging (workflow phase 13).

## Scripts

### `init_icon_system_package.py`

Scaffolds a fresh package directory with templates filled in.

```bash
python3 scripts/init_icon_system_package.py /path/to/icon-system \
  --project-name "Project Name" \
  --owner "Brand Team" \
  --date "2026-04-27"
```

Creates:
- `concepts/`, `selected/`, `exports/`, `reviews/` directories
- Template files copied from `assets/package-template/` with placeholders substituted

Placeholders substituted:
- `{{PROJECT_NAME}}` — from `--project-name`
- `{{OWNER}}` — from `--owner`
- `{{DATE}}` — from `--date` (defaults to today)
- `{{SKILL_VERSION}}` — read from `SKILL.md`

### `render_icon_contact_sheet.py`

Renders an HTML contact sheet showing all icons in the set at multiple sizes and states.

```bash
python3 scripts/render_icon_contact_sheet.py /path/to/svg-masters/ \
  --output contact-sheet.html \
  --sizes 16,20,24,32 \
  --states filled,outlined
```

Output: HTML file with:
- All icons rendered at each size
- Filled and outlined variants side by side
- Light and dark mode preview
- Tab Bar / Bottom Nav frame mockups

Used in workflow phase 11 (validate in context).

### `init_multi_style_review.py`

Scaffolds a three-style review package for client A/B/C comparison before production style lock.

```bash
python3 scripts/init_multi_style_review.py /path/to/review \
  --project-name "Project Name" \
  --styles liquid-glass,3d-isometric,hand-drawn
```

Creates shared Brand DNA / inventory / constraints files, `style-a` / `style-b` / `style-c` folders, scorecard, decision log, contact-sheet placeholder, and winner lock.

### `render_multi_style_contact_sheet.py`

Renders an HTML A/B/C comparison sheet after style candidates have matching SVG
stems.

```bash
python3 scripts/render_multi_style_contact_sheet.py /path/to/review \
  --output /path/to/review/review/contact-sheet.html
```

The output embeds SVGs as data URIs and calls out missing candidate files.

### `validate_motion_spec.py`

Validates animated-icon motion specs before Lottie/dotLottie handoff.

```bash
python3 scripts/validate_motion_spec.py /path/to/motion-spec.json
```

Checks required fields, duration, easing, allowed properties, static frame, reduced-motion fallback, and validation evidence.

### `validate_lottie_assets.py`

Validates exported Lottie JSON and dotLottie ZIP files after the motion spec
passes.

```bash
python3 scripts/validate_lottie_assets.py /path/to/motion/lottie /path/to/motion/dotlottie
```

This is an asset hygiene gate, not a renderer. It still requires target-renderer
preview before shipping.

### `validate_style_pack.py`

Validates user `.style-pack` manifests before custom styles enter Phase 5.

```bash
python3 scripts/validate_style_pack.py /path/to/styles/
```

Requires Brand DNA refusal criteria, construction rules, accessibility guidance, validation checks, prompt examples, and artifact expectations.

### `build_style_pack_registry.py`

Builds a discovery registry for shipped style packs and validated plugin
manifests.

```bash
python3 scripts/build_style_pack_registry.py /path/to/style-plugins/
```

Duplicate style IDs fail by default.

### `export_platform_assets.py`

Exports conservative path-only SVG masters to Android VectorDrawable XML and
scaffolds iOS PDF-backed `.xcassets` image sets.

```bash
python3 scripts/export_platform_assets.py /path/to/package/exports/svg-masters --platform both
```

The iOS path requires same-stem vector PDFs unless
`--ios-placeholder-manifest` is passed.

### `scaffold_design_tool_handoff.py`

Creates a safe Figma/Pencil/Code Connect handoff folder without claiming that
any MCP write-back has happened.

```bash
python3 scripts/scaffold_design_tool_handoff.py /path/to/package/design-tool-handoff \
  --project-name "Project Name" \
  --handoff-mode mixed
```

### `visual_regression_contact_sheet.py`

Compares approved PNG baselines against current contact-sheet or platform
preview snapshots.

```bash
python3 scripts/visual_regression_contact_sheet.py baseline current \
  --report-json report.json
```

## Template Structure

Templates live in `assets/package-template/`:

```
assets/package-template/
├── reviews/
│   ├── project-ui-snapshot.md
│   ├── icon-system-rules.md
│   ├── concept-scorecard.md
│   └── cross-icon-audit.md
└── selected/
    ├── rationale.md
    ├── usage-guidance.md
    ├── tab-bar-icon-notes.md
    ├── bottom-nav-notes.md
    └── export-checklist.md
```

## Workflow With Scripts

Typical packaging workflow:

```bash
# 1. Scaffold the package
python3 scripts/init_icon_system_package.py ~/projects/myapp/icon-system \
  --project-name "MyApp" \
  --owner "Design Team"

# 2. Drop your generated SVG masters into exports/svg-masters/
cp /tmp/generated-icons/*.svg ~/projects/myapp/icon-system/exports/svg-masters/

# 3. Render contact sheet for review
python3 scripts/render_icon_contact_sheet.py \
  ~/projects/myapp/icon-system/exports/svg-masters/ \
  --output ~/projects/myapp/icon-system/reviews/contact-sheet.html

# 4. Open in browser to verify
open ~/projects/myapp/icon-system/reviews/contact-sheet.html

# 5. Fill in selected/rationale.md, system-rules.md, etc.
```

For multi-style review, run `init_multi_style_review.py` before Phase 7 production and `render_multi_style_contact_sheet.py` after candidate SVGs exist. For motion, validate `motion-spec.json` before exporting Lottie/dotLottie assets, then run `validate_lottie_assets.py` on the exports. For custom styles, validate all `.style-pack` manifests before Phase 5 confirmation and build a registry only for discovery. For platform delivery, use `export_platform_assets.py` after SVG masters are final.

## Manual Steps

The skill assists but does not fully automate:

- Filling in `selected/rationale.md` (skill drafts; user reviews and edits)
- Filling in `usage-guidance.md` per surface (skill drafts based on platform specs)
- Producing iOS vector PDFs; the exporter can package them but not create them from SVG
- Previewing Lottie/dotLottie binaries in the target renderer after validation
- Final QA on real devices

## Brand DNA Source

The skill reads any well-formed `brand-dna.md` it finds in the project regardless of who or what wrote it (hand-written, exported from another tool, carried over from a sibling project). The package's handoff documentation cites the source:

- Drop a hand-written `brand-dna.md` at project root, `brand/`, `.claude/`, `design-system/`, or `docs/`, **or**
- Let the skill extract Brand DNA from existing logo / brand assets in the project (filesystem or via a connected design-tool MCP — see [`design-tool-integrations.md`](design-tool-integrations.md)), **or**
- Provide Brand DNA inputs interactively when prompted

See [`brand-dna-input.md`](brand-dna-input.md) for the canonical structure and the three input modes.

## Failure Modes

- **Skipping the scaffold** — files end up scattered, no single source of truth
- **Editing scaffolded templates without reviewing first** — placeholders remain (`{{PROJECT_NAME}}` in production docs)
- **Not running the contact sheet** — context validation skipped
- **Manually exporting without checklist** — Render As: Template Image misconfigured silently
- **Skipping motion spec validation** — animated icons ship without static reduced-motion fallback
- **Skipping Lottie asset validation** — exported JSON/ZIP files contain image, font, expression, or manifest issues
- **Applying unvalidated style plugins** — custom styles bypass Brand DNA and accessibility gates
- **Claiming design-tool write-back from a scaffold** — a plan is not evidence that Figma or Pencil was changed
- **Updating visual baselines without review** — hides regressions instead of documenting approved changes
