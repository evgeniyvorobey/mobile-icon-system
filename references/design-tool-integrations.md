# Design-Tool Integrations

How the skill connects to the design tools where icon work actually lives — Figma, Pencil (`.pen`), and any MCP server the host environment exposes. This file defines the input/output contract with each tool, the fallback path when a tool is unavailable, and the audit signals that distinguish tool-backed work from screenshot-only guesses.

This file is loaded during workflow phase 3 (project audit) and phase 13 (packaging) when the host environment provides design-tool MCP access.

## Detection: what is available?

Before phase 3, check which design tools the host exposes:

1. **Pencil MCP** — tools prefixed `pencil` (e.g., `pencil.get_editor_state`, `pencil.batch_get`, `pencil.batch_design`). Indicates a `.pen` file workflow.
2. **Figma MCP** — tools providing `get_design_context`, `get_screenshot`, `get_metadata`, `get_variable_defs`, `get_code_connect_map`, `add_code_connect_map`. Indicates a Figma file is connected.
3. **Other design-tool MCPs** — any server providing design-context tools (Sketch, Penpot, Framer, etc.). Treat with the same contract pattern.
4. **None** — fall back to filesystem-only mode: read SVGs from the project, accept user-pasted screenshots, ask for exports.

State the detected tool in the response (`Design tool: Figma MCP detected` / `Design tool: Pencil MCP detected` / `Design tool: filesystem-only mode`). Never silently assume a tool is available.

## Figma integration

### When to use it

The skill prefers Figma MCP over filesystem inspection when:

- The user provides a Figma file URL or node URL
- The project's design system lives in Figma and is the source of truth
- Brand DNA needs to come from a published Figma library (variables, components, styles)
- Icons need to be pushed back to Figma as Code Connect mappings

### Brand DNA extraction from Figma

Use the design-context capability to read the Figma library's foundations:

1. Pull color and effect variables → confirm color logic dimension of Brand DNA
2. Pull number variables (radii, stroke widths, grid) → confirm corner treatment, stroke language
3. Read primary symbol / logo component → confirm geometric alphabet, terminal style
4. Inspect the first existing icon component → reveal current grid, padding, stroke

State `Brand DNA source: Figma library variables + primary-symbol component (file: <key>)` in the response.

### Existing icon audit from Figma

Use design-context + screenshot capabilities to inventory the current icon set:

1. List icon components in the icons page or library
2. For each icon, capture: component name, variant properties (state, size, weight), declared stroke, declared corner radius
3. Render screenshots of the icon row at intended size
4. Flag inconsistencies (mixed strokes, missing variants, unbound color)

### Pushing back to Figma

When the icon set is validated and ready for handoff:

- Use `add_code_connect_map` to register the source-of-truth SVG file path against each Figma icon component, so designers see the canonical asset alongside the design
- Document the mapping in the package's `usage-guidance.md`
- Prefer Code Connect over re-uploading SVGs — designers usually want their components, not parallel files

### Authentication

Some Figma MCPs require an auth flow (`authenticate` → `complete_authentication`). Run authentication only when needed; never trigger it speculatively. If the user has not connected Figma, state that and continue in filesystem-only mode.

## Pencil integration

### When to use it

Pencil MCP is the **only** way to read or write `.pen` files — they are encrypted and `Read`/`Grep` will fail on them. If the project contains `.pen` files, use Pencil MCP exclusively for them.

### Reading a `.pen` icon set

1. Call `get_editor_state` to find the active document and selection
2. Call `open_document` if the user named a specific `.pen` path
3. Call `batch_get` with patterns to find icon frames (e.g., `name:ic_tab_*`, `type:Frame, size:24×24`)
4. Call `get_variables` to read declared color and number variables
5. Call `get_screenshot` to render an icon for visual review
6. Call `get_guidelines` to load any Pencil-supplied design guidelines that constrain the file

### Designing in `.pen`

Use `batch_design` with insert/copy/update/replace/move/delete/image operations:

- One `batch_design` call per coherent change set, max ~25 operations per call
- Always read `get_guidelines` first — Pencil enforces project-level rules
- For a full set generation, draft all icons in one batch so set-level consistency is in the same edit
- For per-icon optical correction (hi-end craft pass), separate batches per icon are fine

### Exporting from `.pen`

Use `export_nodes` to produce SVG / PNG / PDF for the production package. Mirror the same naming convention defined in [`package-spec.md`](package-spec.md).

## Generic MCP guidance

For any design-tool MCP not listed above:

1. **Discover the tool surface first** — list tools, read tool descriptions, understand the read/write contract before acting
2. **Read before write** — never call a write/mutate tool without first reading current state
3. **Respect transactions** — if the MCP exposes start/commit/cancel-editing semantics, wrap each batch in a transaction
4. **Pull screenshots over text** — visual icon work needs visual confirmation; rely on screenshot capabilities rather than only metadata
5. **Treat the MCP as authoritative for the file it owns** — do not bypass an MCP by reading the underlying binary directly

## Fallback: filesystem-only mode

When no design-tool MCP is available, the skill works from project files:

- SVG masters → read from `assets/icons/`, `src/icons/`, `Assets.xcassets/`, `res/drawable*/`
- Brand assets → read from `brand/`, `assets/brand/`, `design-system/`
- Screenshots → ask the user to paste or save under `assets/screenshots/`
- Color tokens → read from `colors.json`, `tokens.json`, `theme.ts`, `colors.xml`, asset catalogs

Filesystem mode is fully supported. The skill does not need a design-tool MCP to ship — but when one is available, the result is more accurate, faster, and reusable inside the design system.

## Audit signals: tool-backed vs screenshot-only

When the skill ships an output, declare the source so reviewers can trust the depth:

| Source | Trust level | Use when |
|---|---|---|
| Figma library + components (MCP) | High | Variables and components are the source of truth |
| Pencil `.pen` document (MCP) | High | The icon set lives in a `.pen` workflow |
| SVG files in repo (filesystem) | Medium-High | Repo holds the canonical SVG masters |
| Screenshots only | Medium | No SVG access — visual inspection only |
| User description, no visual | Low | Ask for at least one screenshot or SVG before generating |

Do not claim Brand DNA was extracted from a Figma library if the file was not actually opened. Do not claim a `.pen` file was inspected if Pencil MCP was not invoked. Honesty about the source affects every downstream decision.

## Failure modes

- **Reading a `.pen` file with Read/Grep** — files are encrypted; output is garbage. Always use Pencil MCP.
- **Triggering an auth flow without need** — annoys the user, may expose credentials. Only authenticate when about to call a tool that requires it.
- **Bypassing an MCP for the file it owns** — reading raw bytes from a tool-managed file diverges from the tool's view; ship-time mismatch is guaranteed.
- **Silent fallback** — if Figma MCP is unavailable, say so and continue in filesystem mode. Do not pretend the file was inspected.
- **One-icon-at-a-time `batch_design` calls** — defeats the set-level consistency that the workflow guarantees. Batch the full set in one call.
- **Skipping `get_guidelines` in Pencil** — project-level rules will reject your batch; read first.
