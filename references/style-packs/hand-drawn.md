# Hand-Drawn

Hand-Drawn is a deterministic vector style pack for icons that need a human, imperfect line while remaining reproducible. It uses seeded path jitter with amplitude bounds, protected anchors, anchor budgets, and baseline alignment. The same inputs must produce the same paths every run.

This pack ships in v0.5 because the prior stochastic-drift objection is resolved by freezing the seed, jitter algorithm, and maximum deviation. The style is expressive, but it is not random.

## Use when

**Strong fit:** education, wellness, journaling, creator tools, family products, indie games, and brands with warm human-made marks.

**Weak fit:** regulated finance, medical safety, enterprise admin, system utility, or any brand whose DNA depends on mathematical precision and silent platform-native behavior.

**Best surface:** 20pt and 24pt icons where slight irregularity can be perceived. Use conservative fallback rules at 16pt.

## Refuse if

Refuse when Brand DNA requires strict geometry, perfect symmetry, crisp technical precision, or exact matching to SF Symbols / Material Symbols.

Refuse when the build or design pipeline will regenerate jitter on every export. Any per-run random drift is a hard fail.

Refuse when the icon set cannot tolerate slightly larger visual variance across icons. Hand-drawn needs a stronger cross-icon audit than flat geometric styles.

## Brand DNA fit

| Brand DNA dimension | Behavior under Hand-Drawn |
|---|---|
| Geometric alphabet | inherited as the base path before jitter |
| Stroke language | inherited, then varied within a documented wobble range |
| Terminal style | inherited but softened; round caps recommended |
| Corner treatment | inherited but imperfect; protected corners remain aligned |
| Color logic | inherited unchanged |
| Optical correction | inherited, then rechecked after jitter |

Hand-drawn should be read as "drawn by the brand," not as generic sketchiness. Start from the confirmed brand geometry, then introduce controlled imperfection.

## Construction recipe

### Deterministic seed

Each icon gets a stable seed:

```text
seed = sha256("{project_slug}:{icon_name}:{state}:handdrawn:v1")
```

Use the seed to initialize a deterministic PRNG. Store the seed in SVG metadata or package notes. Re-exporting the same icon must not change any coordinate.

### Base path first

Construct a clean base icon on the normal 24x24 / 20x20 / 16x16 grid before applying jitter. The base icon must pass metaphor, grid, and accessibility checks as if it were a flat outlined or filled icon.

Then apply jitter only to eligible anchors and handles. Do not freehand from scratch.

### Protected anchors

The following anchors are protected and get `dx = 0`, `dy = 0`:

- baseline anchors that define the bottom optical edge;
- vertical and horizontal centerline anchors;
- outer keyline extrema;
- terminal endpoints;
- anchors shared by selected / unselected state pairs;
- anchors whose movement would shrink a negative-space gap below 2pt at 24pt.

Protected anchors keep the icon aligned in rows and paired states. They may still inherit stroke-wobble styling if the stroke remains within bounds.

### Jitter bounds

Apply jitter after optical correction:

| Target size | Anchor jitter amplitude | Handle angle jitter | Handle length scale | Stroke wobble |
|---|---:|---:|---:|---:|
| 24pt | max 0.35pt | max 3deg | 0.94-1.06 | max 8% |
| 20pt | max 0.25pt | max 2deg | 0.96-1.04 | max 6% |
| 16pt | max 0.12pt, or disable | max 1deg | 0.98-1.02 | max 4% |

At 16pt, prefer disabling jitter on all structural anchors and keeping only softened terminals. Any decimal coordinate that creates blur at 16pt fails.

### Anchor budget

Hand-drawn may add anchors only when needed to create a controlled wobble. The added-anchor cap is 15% over the clean base path, with absolute maximums:

- simple icons: 14 anchors;
- medium icons: 24 anchors;
- complex icons: 46 anchors.

If the icon needs more anchors than this to look hand-drawn, the metaphor is too detailed for the style.

### Baseline alignment

Every icon in a row shares the same optical baseline after jitter. For Tab Bar / Bottom Nav sets, the bottom-most protected anchor stays on the declared baseline and the optical center may drift no more than 0.2pt from the set average at 24pt.

Do not let jitter lower one icon more than its siblings. Baseline drift reads as sloppy layout rather than human line.

### Stroke and fill rules

Outlined hand-drawn icons use `stroke-linecap="round"` and `stroke-linejoin="round"` by default. Filled hand-drawn icons may use an irregular outline, but internal counters must stay clean enough to read at target size.

No sketchy multi-stroke effect unless explicitly declared as a sub-style. The default pack is single-stroke deterministic imperfection.

## Variant axes

Generate variants by changing controlled hand-drawn parameters:

- Jitter amplitude: subtle, standard, expressive within the bounds above.
- Stroke wobble: none, light, or standard.
- Terminal softness: inherited, round-soft, or slightly tapered.
- Symmetry protection: strict, partial, or intentionally asymmetric for organic metaphors.
- Fill treatment: clean fill, slightly irregular outline, or outlined-only.
- Seed namespace: `v1a`, `v1b`, `v1c` for exploration, then freeze the winning seed as `v1`.

Do not use unseeded randomness as a variant axis.

## Accessibility implications

Hand-drawn jitter can close counters and reduce contrast at small sizes. Every icon must be rechecked after jitter for 3:1 non-text contrast, minimum negative-space gaps, and blur / squint readability.

State pairs must share protected anchors so selected and unselected states feel related, but they still need a shape or fill-density distinction. Color-only state distinction remains a hard fail.

At 16pt, jitter is heavily limited or disabled because sub-pixel drift can create fuzzy edges. Accessibility wins over the hand-drawn effect.

## Validation checklist

- [ ] A clean base path exists before jitter.
- [ ] Seed is stored and stable.
- [ ] Re-running the jitter algorithm produces identical coordinates.
- [ ] Protected anchors have no positional jitter.
- [ ] Jitter amplitude, handle jitter, and stroke wobble stay inside size-specific bounds.
- [ ] Anchor count stays under the hand-drawn budget.
- [ ] Baseline and optical center remain aligned across the set.
- [ ] Negative-space gaps remain at or above the craft-rubric minimum.
- [ ] 16pt exports either disable jitter or pass strict pixel alignment.
- [ ] State pairs differ by shape / fill density, not only color.

## Anti-patterns

1. Random jitter at render time.
2. Re-jittering on every export.
3. Moving baseline anchors and making the row bounce.
4. Adding many anchors to fake "organic" line.
5. Closing counters or gaps with wobble.
6. Double-sketch strokes that muddy 20pt and 16pt renders.
7. Applying jitter before optical correction, then never rechecking balance.

## Packaging notes

Package both the clean base SVG and the final jittered SVG when possible. The final asset is the shipped master; the base asset documents the construction.

Add metadata to every jittered SVG:

```svg
<metadata>
  {"style":"hand-drawn","seed":"project:icon:state:handdrawn:v1","amplitude":0.25}
</metadata>
```

Round final coordinates to a documented precision, usually 0.01pt for 24pt and 20pt. For 16pt, use integer or half-integer coordinates only when strokes require them.

Do not let SVGO or design-tool cleanup resample the path into a different anchor set unless the exported result is revalidated. For platform handoff, include `hand-drawn-notes.md` with seed namespace, jitter bounds, protected-anchor policy, and any icons where jitter was disabled for accessibility.

## Workflow integration

- **Phase 5** - declare seed scheme, jitter amplitude, protected-anchor policy, stroke wobble, and 16pt fallback.
- **Phase 7** - create clean base variants first; apply seeded jitter only after variant selection or as a controlled variant parameter.
- **Phase 8 Pass A** - verify seed stability, anchor budgets, baseline alignment, and protected anchors.
- **Phase 9** - re-run optical correction checks after jitter.
- **Phase 11** - render at 24pt, 20pt, and 16pt; compare repeated exports byte-for-byte or coordinate-for-coordinate.

## Sources

Use the base construction and validation thresholds from [`../icon-grid-construction.md`](../icon-grid-construction.md), [`../accessibility.md`](../accessibility.md), and [`../craft-rubric.md`](../craft-rubric.md). The seeded-jitter constraints in this pack are repo construction rules that make expressive paths reproducible.
