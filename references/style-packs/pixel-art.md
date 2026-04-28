# Pixel Art

Pixel Art is a native bitmap-grid style pack for mobile UI icons that intentionally uses discrete pixels as the primitive. It is not "rough SVG" and not a retro filter over a vector icon. The master logic is a target-size pixel matrix with nearest-neighbor export, binary alpha, and no anti-aliased ambiguity.

This pack ships in v0.5 because the prior SVG-first objection is resolved by treating pixel art as a bitmap-aware production path with SVG rectangle exports only as an interchange format. The source of truth is the pixel grid at each target size.

## Use when

**Strong fit:** games, retro utilities, maker tools, music trackers, coding toys, and brands whose identity uses blocky grid marks or sprite language.

**Weak fit:** finance, health, enterprise SaaS, premium lifestyle, and any app whose icons must coexist invisibly with SF Symbols or Material Symbols.

**Best surface:** 16pt, 20pt, and 24pt icons that are intentionally grid-native. Pixel art may work unusually well at 16pt because it is authored for that size instead of scaled down.

## Refuse if

Refuse when Brand DNA requires smooth curves, calligraphic strokes, translucent material, continuous gradients, or platform-template tinting that must preserve antialiased vector edges.

Refuse when the team cannot ship bitmap or bitmap-equivalent assets with nearest-neighbor scaling. If the delivery pipeline will optimize every icon into antialiased vector paths, this pack cannot hold.

## Brand DNA fit

| Brand DNA dimension | Behavior under Pixel Art |
|---|---|
| Geometric alphabet | quantized to square pixels on a target-size grid |
| Stroke language | converted to 1px or 2px pixel runs |
| Terminal style | square terminals only |
| Corner treatment | stair-step corners only; no radius |
| Color logic | limited palette of 1-4 flat colors, usually one semantic ink plus optional accent |
| Optical correction | performed by moving whole pixels, never sub-pixel anchors |

Pixel art is a strong Brand DNA match only when the brand can tolerate square terminals and visible grid logic. It should feel intentional at 1x, not like a broken export.

## Construction recipe

### Source of truth

Author each icon as a bitmap matrix at its target size. A matrix cell is either empty or filled with a named palette token. SVG may be emitted as one `<rect>` per run or per pixel, but the SVG is an export of the matrix, not the conceptual master.

Tiny example:

```text
16x16 heart, 1 = ink, . = empty
................
....11....11....
...1111..1111...
..111111111111..
..111111111111..
...1111111111...
....11111111....
.....111111.....
......1111......
.......11.......
................
```

### Grid rules by size

**16pt**

- Canvas: 16x16 pixels.
- Live area: 14x14, with at least 1px clear padding unless the metaphor needs overshoot.
- Stroke / run minimum: 1px.
- Diagonals: use a consistent 1:1 or 2:1 stair-step; do not mix patterns inside one icon.
- Detail budget: one primary metaphor plus at most one internal counter-form.
- Alpha: 0 or 255 only.

**20pt**

- Canvas: 20x20 pixels.
- Live area: 18x18.
- Stroke / run minimum: 1px; use 2px for primary outlines when the set feels too light.
- Diagonals: 1:1, 2:1, or 3:2 stair-step, documented per set.
- Detail budget: primary metaphor plus up to two internal cuts.
- Alpha: 0 or 255 only.

**24pt**

- Canvas: 24x24 pixels.
- Live area: 20x20 by default, 22x22 for dense filled glyphs after optical review.
- Stroke / run minimum: 1px; primary silhouettes should use 2px runs where possible.
- Diagonals: same family as the 16pt and 20pt versions, with added pixels only where they preserve the rhythm.
- Detail budget: primary metaphor plus secondary accent, but no texture noise.
- Alpha: 0 or 255 only, except whole-icon disabled opacity controlled by the host UI.

Never scale a 24pt matrix down to 20pt or 16pt. Redraw every target size.

### Rendering rules

- Use nearest-neighbor scaling only.
- CSS / web exports must set `image-rendering: pixelated` or the platform equivalent.
- SVG rectangle exports must use integer `x`, `y`, `width`, and `height`; add `shape-rendering="crispEdges"`.
- No strokes, round caps, filters, masks, gradients, fractional coordinates, or blur.
- No partial-alpha edge pixels. Anti-aliased ambiguity is a hard fail.

### Palette rules

Default to one ink color. A second color may mark an accent or state, but the single-color silhouette must still read. Four colors is the absolute maximum for 24pt; 16pt should use one or two.

Dithering is allowed only at 24pt and only when decorative. It must never carry the icon's meaning or state.

## Variant axes

Generate variants by changing only grid-native choices:

- Target matrix: 16x16, 20x20, or 24x24 redrawn from scratch.
- Silhouette density: sparse, standard, or chunky.
- Diagonal rhythm: 1:1, 2:1, or 3:2 stair-step.
- Palette: monochrome, monochrome plus accent, or two-state palette.
- Counter-form size: conservative, standard, or expanded.
- Outline strategy: no outline, 1px outline, or filled silhouette.

Do not generate variants by adding antialiasing, sub-pixel curves, or vector stroke effects.

## Accessibility implications

Pixel art must pass the same WCAG 2.2 non-text contrast checks as every other icon. The filled pixels that communicate the metaphor must hit 3:1 against the surface.

Color cannot be the only distinction between states. Selected / unselected pairs need a pixel-shape delta, such as filled body versus hollow body, added notch, or changed internal counter-form.

At 16pt, decorative details disappear quickly. If an icon needs a label to be understood at 16pt, simplify the matrix rather than relying on surrounding text.

Screen-reader labels and touch targets follow [`../accessibility.md`](../accessibility.md): the visible 16pt or 20pt sprite still needs a 44pt iOS / 48dp Android hit area when it is interactive.

## Bitmap-aware grader needs

Existing SVG geometry graders are not enough for this pack. The validation path must inspect the rendered bitmap at the target size and check:

- all occupied pixels are on integer grid cells;
- alpha is binary, with no antialiased edge pixels;
- nearest-neighbor export is preserved at 1x, 2x, and 3x;
- color count stays within the declared palette;
- connected components and filled-pixel ratios are measured on the matrix, not on vector path bounds;
- 16pt, 20pt, and 24pt masters are compared as sibling redraws, not scaled versions.

Use [`../../scripts/grade/bitmap.py`](../../scripts/grade/bitmap.py) for these checks during Phase 9 / Phase 11. The grader is intentionally heuristic and does not replace semantic review, but it catches the failures the SVG geometry grader cannot see: partial-alpha edges, palette overflow, and target-size fill/component drift.

## Validation checklist

- [ ] Each target size has its own source matrix.
- [ ] No matrix was created by scaling another size.
- [ ] All filled cells sit on integer coordinates.
- [ ] Alpha is binary: no partial-alpha edge pixels.
- [ ] Palette count is within the declared limit.
- [ ] Diagonal stair-step rhythm is consistent across the set.
- [ ] Single-color collapse remains readable.
- [ ] State pairs differ by shape, not only color.
- [ ] Nearest-neighbor rendering is verified at 1x, 2x, and 3x.
- [ ] Bitmap-aware QA is documented in the package.

## Anti-patterns

1. Exporting an antialiased SVG and calling it pixel art.
2. Scaling a 24pt sprite down to 16pt.
3. Mixed diagonal rhythms inside one set.
4. One-pixel decorative noise that changes the metaphor at small size.
5. Partial-alpha pixels on edges.
6. Rounded caps or curves hidden inside SVG strokes.
7. Color-only selected states.

## Packaging notes

Package the matrix source alongside exports. A Markdown matrix, JSON grid, or design-tool pixel frame is acceptable as long as it preserves exact cells and palette tokens.

Recommended deliverables:

- `svg-masters/` rectangle-based SVG exports for cross-platform review.
- `png/1x`, `png/2x`, and `png/3x` nearest-neighbor PNG exports for bitmap-native use.
- Android vector drawable exports only if they preserve integer rectangles.
- iOS image sets with interpolation disabled by the consuming UI where possible.
- `pixel-art-notes.md` documenting grid size, palette, diagonal rhythm, and bitmap-aware QA status.

Do not run path optimizers that merge rectangles into antialiased curves. If optimization is required, optimize by horizontal pixel runs with integer rectangle bounds.

## Workflow integration

- **Phase 5** - declare pixel sizes, palette limit, diagonal rhythm, nearest-neighbor export requirement, and bitmap-aware QA command.
- **Phase 7** - generate variants as matrices, then emit rectangle SVG only after picking.
- **Phase 8 Pass A** - check integer cells, binary alpha, palette count, and per-size redraws; use `python3 scripts/grade/bitmap.py <svg> --sizes 16,20,24` on exported SVGs.
- **Phase 9** - perform optical corrections by moving whole pixels only.
- **Phase 11** - inspect 16pt, 20pt, and 24pt in context at 1x, 2x, and 3x.

## Sources

Use the base size, contrast, and touch-target constraints from [`../icon-grid-construction.md`](../icon-grid-construction.md), [`../accessibility.md`](../accessibility.md), and [`../craft-rubric.md`](../craft-rubric.md). Pixel-specific constraints in this pack are repo construction rules: integer matrices, binary alpha, and nearest-neighbor rendering are mandatory for deterministic output.
