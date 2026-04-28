# 3D / Isometric

3D / Isometric is a deterministic vector style pack for mobile UI icons that need depth without becoming illustration. The pack uses an axonometric projection, explicit top / front / side faces, one light direction, and constrained shadows. It is not an image-generation style: final masters are SVG paths generated from a repeatable construction recipe.

This pack ships in v0.5 because the prior "requires camera or image-gen" objection is resolved by a fixed axonometric projection and a small-size fallback rule. Use it when a brand needs dimensionality but still needs auditable SVG masters, platform exports, and WCAG validation.

## Use when

**Strong fit:** game-adjacent products, creative tools, spatial / map / logistics apps, productivity brands with blocky geometric DNA, and brands that already use simple dimensional objects or extruded marks.

**Weak fit:** thin-line utility systems, medical / legal / banking interfaces that must read as calm and unadorned, and icon sets rendered mostly at 16pt inline size.

**Best surface:** 24pt and larger action / category icons. Tab Bar use is allowed only when the small-size fallback is defined and tested.

## Refuse if

Refuse when Brand DNA requires stroke-only icons, flat monochrome template tinting with no baked colors, or no decorative depth. Refuse when the icon must communicate its state through a single platform tint only, because face shading will be stripped or recolored inconsistently.

Refuse for sets whose primary target size is 16pt unless the user accepts the documented flat fallback for all small contexts.

## Brand DNA fit

| Brand DNA dimension | Behavior under 3D / Isometric |
|---|---|
| Geometric alphabet | inherited, then projected into axonometric faces |
| Stroke language | disabled by default; optional 1pt edge strokes only at 24pt+ |
| Terminal style | inherited only for visible silhouette edges |
| Corner treatment | inherited on the top face; front / side faces mirror the same radius where geometry permits |
| Color logic | augmented into one base hue plus lit / shaded face values |
| Optical correction | augmented by projection-centroid and shadow-weight corrections |

The style works best when the brand has simple primitives that can become solid objects: squares, rounded rectangles, cylinders, pins, folders, blocks, cards, and clear symbolic objects. Organic or thin calligraphic DNA should stay flat or use the hand-drawn pack instead.

## Construction recipe

### Projection model

Use a fixed axonometric projection for every icon in the set. Do not use perspective, camera focal length, or arbitrary per-icon angles.

```text
Given model coordinates (x, y, z), centered around (0, 0, 0):
screen_x = 12 + scale * (x - y) * 0.8660254
screen_y = 12 + scale * (x + y) * 0.5 - scale * z
```

Default `scale` is chosen so the projected object fits the 20x20 live area inside the 24x24 canvas. The projection angle is therefore 30 degrees on both receding axes. Final designer-placed straight endpoints snap to 0.25pt at 24pt; projected math-derived points may keep decimals, but they must be stable across exports.

### Layer model

Exactly 4 logical layers, in z-order:

1. `shadow` - flat projected footprint below the object, decorative only.
2. `front` - vertical face whose model edge faces the viewer.
3. `side` - vertical side face.
4. `top` - top face, always the metaphor carrier.

The `top` layer owns the icon metaphor. If the icon is unreadable with `front`, `side`, and `shadow` hidden, the icon fails.

### Face construction

Start from a simple 2D top footprint on the model plane `z = depth`. Project that footprint with the formula above. Build the `front` and `side` faces by connecting the visible lower edges from `z = depth` to `z = 0`.

- Default depth: 2.0pt projected vertical drop on a 24pt canvas.
- Allowed depth range: 1.5-3.0pt at 24pt.
- Corner radius: project the same radius used by the top footprint; do not invent extra bevels.
- Edge strokes: optional, 1pt max, same hue as the darker adjacent face, opacity 0.28-0.40.
- No hidden rear faces. If a rear face is visible, the object is over-rotated.

### Light direction and color

Use one light source for the whole set: upper-left-front, model vector `(-1, -1, +2)`.

- `top`: base brand color lightened 6-10% in perceived lightness.
- `side`: base brand color darkened 4-8%.
- `front`: base brand color darkened 10-16%.
- Optional edge stroke: front shade darkened another 8-12%, opacity 0.28-0.40.

Never use gradients to fake depth. Face value changes must come from separate flat fills so Android vector drawable export remains predictable.

### Shadow constraints

The shadow is a flattened copy of the top footprint projected at `z = 0`, offset by `(0.6pt, 1.0pt)` at 24pt.

- Shadow opacity: 0.10-0.18 on light surfaces, 0.18-0.26 on dark surfaces.
- Blur: none by default. If SVG filters are allowed, `stdDeviation <= 0.5` at 24pt.
- Shadow extent: must stay inside the 24x24 canvas and may not define the semantic silhouette.
- No long cast shadows, ambient occlusion stacks, or perspective ground planes.

### Small-size fallback

At 20pt, keep `top`, `front`, and `side`, but reduce depth to 1.0-1.5pt and remove edge strokes.

At 16pt, ship a separate flat fallback: hide `front`, `side`, and `shadow`; use the `top` silhouette redrawn on the 16x16 grid with one color. Do not scale the 24pt isometric master down to 16pt.

## Variant axes

Generate variants by changing only controlled axes:

- Depth: shallow 1.5pt, standard 2.0pt, deep 3.0pt.
- Footprint abstraction: block, slab, cylinder, or folded-plane interpretation of the same metaphor.
- Face contrast: low 6% spread, standard 12% spread, high 16% spread, while preserving 3:1 contrast for semantic faces.
- Corner strategy: inherited radius, reduced radius for tiny faces, or squared extrusion for pixel-snapped brands.
- Shadow presence: none, flat shadow, or minimal blurred shadow within the constraints above.

Do not vary the projection formula per icon. A set with mixed camera angles is not a style; it is inconsistent illustration.

## Accessibility implications

The top silhouette must pass WCAG 2.2 non-text contrast at 3:1 against the surface by itself. Face contrast is decorative; it cannot be the only carrier of meaning.

State changes must alter shape or fill density, not only face shading. In Forced Colors / Increase Contrast, all faces may collapse to one system color, so the icon must still read as a single-color silhouette. Shadows are ignored for contrast and meaning.

The 16pt fallback is an accessibility requirement, not an optional export. Users with larger text, dense toolbars, or notification surfaces will encounter the fallback size.

## Validation checklist

- [ ] Every icon uses the same axonometric projection formula.
- [ ] Layer IDs are exactly `shadow`, `front`, `side`, and `top` when those layers exist.
- [ ] The `top` layer alone communicates the metaphor.
- [ ] Light direction is upper-left-front across the full set.
- [ ] Face values follow top lightest, side medium, front darkest.
- [ ] Shadow opacity, offset, blur, and extent stay inside the documented bands.
- [ ] 20pt and 16pt fallbacks are separate tested assets, not scaled exports.
- [ ] Single-color collapse still reads under Forced Colors / Increase Contrast.
- [ ] Visual weight variance across the set stays within the craft-rubric set-level threshold.

## Anti-patterns

1. Perspective camera per icon - breaks set consistency and makes SVG reproduction ambiguous.
2. Image-generated depth baked into raster shadows - not auditable and not Android-vector friendly.
3. Gradients on every face - turns simple depth into illustration and complicates contrast.
4. Over-deep extrusion - at 24pt anything above 3pt depth steals space from the metaphor.
5. State by lighting only - fails color-blind and Forced Colors checks.
6. Scaling the 24pt isometric icon to 16pt - produces unreadable face slivers.

## Packaging notes

Ship SVG masters with stable layer groups:

```svg
<g id="shadow">...</g>
<g id="front">...</g>
<g id="side">...</g>
<g id="top">...</g>
```

Package 24pt and 20pt dimensional masters separately from 16pt flat fallbacks. Name the fallback explicitly, for example `ic_action_box_16_flat.svg`, and document in `system-rules.md` that product surfaces at 16pt must use the flat asset.

For Android vector drawables, prefer flat fills and no filters. If the SVG master uses a minimal blurred shadow, provide a no-filter Android export with the shadow removed or flattened. For iOS template-image workflows, do not mark dimensional SVGs as template images unless the product intentionally collapses face colors to one tint.

## Workflow integration

- **Phase 5** - declare projection formula, depth range, face color tokens, shadow policy, and small-size fallback policy.
- **Phase 7** - generate variants by depth, footprint abstraction, and face contrast only; projection is invariant.
- **Phase 8 Pass A** - check layer IDs, face order, light direction, and projection consistency.
- **Phase 9** - apply optical balancing after projection, then verify the top layer's silhouette against the flat fallback.
- **Phase 11** - render 24pt, 20pt, and 16pt assets in context; test single-color collapse.

## Sources

Use the base grid, accessibility, and craft thresholds from [`../icon-grid-construction.md`](../icon-grid-construction.md), [`../accessibility.md`](../accessibility.md), and [`../craft-rubric.md`](../craft-rubric.md). The projection is the standard isometric axonometric formula with 30-degree receding axes; the pack fixes that formula as the repo's deterministic construction rule.
