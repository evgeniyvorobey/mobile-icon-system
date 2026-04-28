# Style Pack Plugin System

The built-in style packs in this repository remain the canonical shipped specs:
[`duotone-chromatic.md`](duotone-chromatic.md), [`liquid-glass.md`](liquid-glass.md),
[`claymorphism.md`](claymorphism.md), [`3d-isometric.md`](3d-isometric.md),
[`pixel-art.md`](pixel-art.md), and [`hand-drawn.md`](hand-drawn.md). A user-defined
visual style can add the same kind of rules through a data-only `.style-pack`
manifest without editing the repo's built-in Markdown packs.

The plugin system is intentionally conservative. A manifest can describe a style,
its Brand DNA constraints, its construction recipe, and its validation gates, but it
cannot silently override Brand DNA or skip Phase 5 confirmation. Brand DNA still wins
unless the user explicitly accepts a conflict surfaced by `refuseIf`.

## Manifest File

A `.style-pack` file is JSON. Use UTF-8, no comments, and keep the file data-only:
no executable code, import hooks, shell commands, network URLs that must be fetched,
or generated scripts. Suggested file name:

```text
acme.soft-plastic.style-pack
```

The validator also accepts `*.style-pack.json` for teams whose tooling expects JSON
extensions, but `.style-pack` is the preferred portable form.

## Required Shape

Every manifest must include these top-level keys:

- `id` - stable lowercase identifier. Regex: `^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$`
- `name` - human-readable style name.
- `version` - semver-ish manifest version such as `1.0.0` or `1.0.0-beta.1`.
- `status` - one of `shipped`, `deferred`, or `experimental`.
- `category` - broad style family, for example `duotone`, `material`, `tactile`, or `illustrative`.
- `compatibility` - object describing schema, skill, and platform fit.
- `brandDnaConstraints` - object describing inherited and overridden Brand DNA dimensions.
- `brandDnaConstraints.refuseIf` - nonempty list of Brand DNA conflicts that must stop automatic application.
- `constructionRules` - object with layer model, geometry, color, SVG features, and forbidden features.
- `accessibility` - object with contrast, Forced Colors, motion, and state guidance.
- `validation` - object with review and machine-check expectations.
- `validation.checks` - nonempty list of checks the style must pass.
- `prompts` - object with selection and generation guidance.
- `prompts.examples` - nonempty list of examples showing when to accept or refuse the style.
- `artifactExpectations` - object describing the files, metadata, and review notes downstream phases should emit.

Unknown extra keys are allowed so teams can add local metadata without breaking the
base validator.

## Minimal Example

```json
{
  "id": "acme.soft-plastic",
  "name": "Soft Plastic",
  "version": "0.1.0",
  "status": "experimental",
  "category": "tactile",
  "compatibility": {
    "schemaVersion": "1.0.0",
    "mobileIconSystem": ">=0.5.0",
    "platforms": ["ios", "android"]
  },
  "brandDnaConstraints": {
    "inherits": ["geometric alphabet", "color tokens", "optical corrections"],
    "overrides": ["corner treatment"],
    "refuseIf": [
      "brand requires sharp 90 degree corners",
      "brand forbids filled icon bodies"
    ]
  },
  "constructionRules": {
    "layerModel": [
      {"id": "body", "role": "primary glyph fill"},
      {"id": "shadow", "role": "decorative depth only"}
    ],
    "numericalThresholds": {
      "cornerRadiusPercent": [24, 50],
      "bodyContrastMinimum": 3
    },
    "svgFeatures": ["path", "filter"],
    "forbiddenFeatures": ["photographic texture", "third hue"]
  },
  "accessibility": {
    "contrast": "Body fill must meet 3:1 against the target surface.",
    "forcedColors": "The metaphor must read when decorative shadows are removed.",
    "stateChanges": "Never rely on shadow strength alone."
  },
  "validation": {
    "checks": [
      {
        "id": "body-contrast",
        "description": "Primary body fill passes 3:1 non-text contrast.",
        "severity": "error"
      }
    ],
    "failureModes": ["body contrast below 3:1", "shadow carries semantic state"]
  },
  "prompts": {
    "selectionPrompt": "Use only after the user confirms a tactile filled style.",
    "examples": [
      {
        "request": "Friendly wellness app with rounded pastel Brand DNA.",
        "expectedDecision": "candidate"
      },
      {
        "request": "Sharp monochrome enterprise system.",
        "expectedDecision": "refuse"
      }
    ]
  },
  "artifactExpectations": {
    "outputs": ["style rules summary", "SVG masters with stable layer IDs"],
    "metadata": ["stylePackId", "stylePackVersion", "status"],
    "reviewNotes": ["Brand DNA conflicts and explicit overrides"]
  }
}
```

## Discovery And Loading

Style-pack manifests should be loaded only from explicit user-controlled locations,
for example a project package folder or a path supplied at runtime. A directory input
is searched recursively for `*.style-pack` and `*.style-pack.json`.

Load order should be:

1. Built-in Markdown style packs from [`README.md`](README.md), when the selected
   style is one of the shipped defaults.
2. User `.style-pack` manifests from explicitly provided paths.
3. Project-local overrides only when the user confirms the override target by ID.

ID collisions are not resolved silently. If a plugin ID matches a built-in style or
another plugin, the loader should surface the conflict and require the user to choose
which source has authority for this run.

## Workflow Integration

The manifest maps to the existing style-pack workflow without changing the shipped
Markdown files:

- Phase 5 reads `name`, `status`, `category`, `compatibility`, and
  `brandDnaConstraints.refuseIf` before presenting the visual style choice.
- Phase 7 uses `constructionRules` as the layer and SVG-generation contract.
- Phase 8 uses `validation.checks` as the style-specific Pass A / Pass B checklist.
- Phase 9 applies any optical corrections declared in `constructionRules`.
- Phase 11 uses `accessibility` and `artifactExpectations` to decide which variants,
  metadata, and review notes must be included in the package.

Experimental and deferred styles may be inspected, but should not be treated as a
production default. `status: shipped` means the author considers the style ready for
normal package work; it does not bypass Brand DNA or accessibility checks.

## Validation

Use the stdlib-only validator:

```bash
python3 scripts/validate_style_pack.py path/to/acme.soft-plastic.style-pack
python3 scripts/validate_style_pack.py path/to/style-pack-directory
```

The script exits `0` when every manifest is valid and `1` when any manifest is
missing required fields, has invalid JSON, violates the ID or version formats, uses
an unknown status, has no `refuseIf`, or has no validation checks.

The repository includes a positive fixture at
[`../../assets/style-pack-fixtures/valid/soft-plastic.style-pack`](../../assets/style-pack-fixtures/valid/soft-plastic.style-pack).
