# Style-Pack Registry

The style-pack registry is a discovery index for shipped Markdown packs and
validated `.style-pack` plugin manifests. It helps tools list available style
choices without changing the Phase 5 gate.

The generated registry lives at
[`../../assets/style-pack-registry/registry.json`](../../assets/style-pack-registry/registry.json).
Build it with:

```bash
python3 scripts/build_style_pack_registry.py
```

Add user plugin manifests from explicit paths:

```bash
python3 scripts/build_style_pack_registry.py path/to/style-plugins/
```

Use `--output -` to inspect JSON without writing the tracked asset.

## Indexed Fields

Every entry includes:

- `id` - stable style-pack identifier.
- `name` - display name from the Markdown title or plugin manifest.
- `status` - `shipped`, `deferred`, or `experimental`.
- `sourceType` - `builtin` for repo Markdown packs, `plugin` for `.style-pack`
  manifests.
- `path` - source file path.
- `version` - plugin manifest version when available.
- `categories` - broad discovery buckets such as `duotone`, `material`,
  `tactile`, `dimensional`, `bitmap`, or `organic`.
- `tags` - additional searchable style traits.
- `refuseIf.summary` - compact Brand DNA conflict summary that Phase 5 must
  surface before any non-default style is applied.

## Validation And Duplicates

Plugin entries are validated with the existing
[`../../scripts/validate_style_pack.py`](../../scripts/validate_style_pack.py)
logic before indexing. Invalid manifests fail the build.

Duplicate IDs fail the build by default, including collisions between a plugin
and a built-in pack. `--allow-duplicates` is for inspection only; it writes the
collisions to `duplicateIds` so an integrator can see the conflict.

## Phase 5 Boundary

The registry is not a runtime style loader. A listed entry means only that the
pack is discoverable and, for plugins, structurally valid. Brand DNA conflicts,
accessibility implications, and explicit user confirmation still happen in
Phase 5 before construction rules enter generation.
