# Geometric Craft Guide (Long-form)

Long-form rationale and worked examples behind the geometric craft checklist in [`geometric-craft.md`](geometric-craft.md). Use this when learning the principles or explaining a decision; use the checklist for runtime craft passes.

## Why Geometric Craft Matters at Icon Scale

A 1024×1024 logo can survive sloppy construction because the eye has resolution to forgive. A 24×24 icon cannot. Every pixel is visible; every off-grid coordinate produces visible blur or anti-aliasing inconsistency.

Three forces compound at icon scale:

1. **Pixel constraint** — anti-aliasing makes off-pixel strokes blurry
2. **Optical perception** — small shapes are read holistically; tiny imperfections aggregate
3. **Set comparison** — icons sit next to each other and reveal each other's weaknesses

Geometric craft is the discipline of designing for these compounding forces.

## Construction Grids

A construction grid is a coordinate system for icon design. Every shape, every anchor, every stroke endpoint references the grid.

### Grid choice

- 24×24: Material standard, cross-platform default
- 20×20: iOS Tab Bar visual mass
- 16×16: small contexts (notification, inline)

The grid determines:
- Available anchor positions (snap points)
- Stroke alignment options
- Corner radius options

### Why grid alignment matters

Off-grid alignment produces:
- Anti-aliased blur at export
- Inconsistency across the set (one icon at 0.7pt offset, another at 0.3)
- Difficult diff in version control

On-grid alignment produces:
- Crisp pixel rendering
- Predictable anti-aliasing
- Easy review and version diff

## Optical Corrections in Detail

Geometry and perception are not the same. Optical corrections close the gap.

### Diagonal stroke compensation

A 1pt orthogonal stroke and a 1pt diagonal stroke have the same numeric width. Visually, the diagonal looks thinner because:
- Less ink along the same length
- Anti-aliasing distributes more pixels for the same physical stroke

Compensation: thicken diagonals by 3-7%. At 1.75pt orthogonal, diagonal is 1.85pt.

This is consistent across the set. Document the rule and apply.

### Circle overshoot

A circle of diameter D and a square of side D have different perceived sizes — the square looks bigger because of its 4 corners pushing outward.

Compensation: circles overshoot the square frame by 1-2% (e.g., 24×24 grid, circle is ⌀24.5).

### Visual centering

A play triangle pointing right has its mass to the left. Geometric centering puts the triangle's centroid at the bounding-box center, which makes the icon look biased left.

Visual centering shifts the triangle right by 0.5-1pt so its perceived center sits at the bounding-box center.

Apply visual centering to:
- Directional icons (play, magnifying glass with handle, arrow)
- Asymmetric icons (filled bell, settings gear with off-axis detail)
- Icons whose silhouette has uneven mass distribution

### Negative-space density compensation

A wifi icon has gaps. A solid square doesn't. The wifi reads as visually smaller because gaps reduce perceived ink mass.

Compensation: scale density-heavy icons up 2-3% within their bounding box.

## Anchor Reduction

Why fewer anchors is better:

1. **Smoother curves** — fewer anchors mean fewer chances for tangent breaks
2. **Cleaner SVG** — smaller files, easier to review
3. **Predictable rendering** — fewer subdivision points for the rasterizer
4. **Easier consistency** — fewer anchors mean the same anchor patterns recur across the set

### Where to place anchors

For curves, place anchors at extrema:
- 0° (rightmost point)
- 90° (topmost point)
- 180° (leftmost point)
- 270° (bottommost point)

A circle drawn with 4 anchors at extrema is rounder than a circle with 8 random anchors.

For straight segments, place anchors only at endpoints. Intermediate anchors on a straight segment are redundant.

### Anchor reduction procedure

1. Start with the icon as drawn
2. Inspect each anchor: is it doing something? If not, delete it
3. Re-evaluate the curve: does it still feel right?
4. If yes, keep the reduction; if no, reposition rather than re-add anchor

## Tangent Continuity

When two curve segments meet, their tangent vectors describe how they connect:

- **G0 (positional)**: segments touch but tangents may differ → visible kink
- **G1 (tangent)**: tangents align → smooth visual transition
- **G2 (curvature)**: tangents and curvature align → premium-feeling smoothness

For UI icons:
- G1 minimum at every corner where curves meet
- G2 for hi-end where curves are prominent

### How to verify

Most vector editors highlight tangent breaks. Pencil and Figma show curvature combs that visualize G2.

If your tool doesn't show this, manually check by zooming 800% — visible kinks indicate G0 (broken).

## Path Cleanliness

A clean SVG `d` attribute has:

- Coordinates with consistent precision (e.g., always 2 decimal places)
- Minimal command repetition
- No floating-point detritus from rounding errors
- Consistent command style (relative `m`/`l` or absolute `M`/`L`, but pick one)

Clean paths review faster, diff cleaner in git, and produce predictable rendering.

### Common detritus

```
M 12.000001 8.999999 L 12.0 9.0
```

Should be:

```
M 12 9 L 12 9 (and the stroke-only second L is redundant)
```

Use vector tools' "round coordinates" feature, or hand-edit.

## Pixel Alignment

At target export size, every shape edge must land on the pixel grid. For 1pt strokes:

- Stroke center on integer pixel: `<line x1="12" y1="0" x2="12" y2="24"/>`
- Stroke fills full pixel column

For 1.5pt strokes:

- Stroke center on half pixel: `<line x1="12.25" y1="0" x2="12.25" y2="24"/>` won't work; needs centerpiece on .5
- Or: thicker stroke (2pt) with sub-pixel center

For 2pt strokes:
- Stroke center on integer pixel works cleanly

The rule: center of the stroke must align with the pixel grid such that the stroke fills full pixel rows/columns at export size.

## Validation by Eye

After mathematical correctness, the eye is the final judge:

- Render at target size
- Zoom 800-1200% to see anti-aliasing
- Compare to other icons in the set (squint test)
- Look at the icon next to a system icon (Material / SF) at the same size — does it feel native?

## Failure Modes

- **Geometry-only craft, no perceptual checks** — produces icons that are technically correct but feel off
- **Optical corrections without consistency** — different compensations on different icons creates set drift
- **Path cleanliness sacrificed for "preserve original"** — a few bad anchors propagate through edits
- **Pixel alignment at master size, not target size** — masters can be on grid while exports are not
- **Skipping G1 verification** — tangent breaks read as cheap, especially at hi-end
