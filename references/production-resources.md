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

## Manual Steps

The skill assists but does not fully automate:

- Filling in `selected/rationale.md` (skill drafts; user reviews and edits)
- Filling in `usage-guidance.md` per surface (skill drafts based on platform specs)
- Producing platform-specific exports (PDF for iOS, vector drawable XML for Android)
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
