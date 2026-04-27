# Icon Grid Construction

Defines the construction grids icons are built on, keyline shapes for visual balance, optical sizing, and stroke contrast rules. This is the geometric foundation; cross-icon consistency rules build on top of it.

## Why Grids

Icons in a set must feel like a family. A shared grid is the cheapest way to achieve that — every shape lands on the same lattice, every stroke falls on the same baseline, every corner uses the same radius increment. Without a grid, even icons drawn by the same hand will drift visually.

## Standard Grids

### 24×24 (Default — Cross-platform)

Most common UI icon size. Used by Material Design, Lucide, Phosphor, Tabler. Recommended default for new sets.

- **Live area**: 20×20 (2pt keyline padding on all sides)
- **Stroke weight**: 1.75pt (default), 1.5pt (light), 2pt (bold)
- **Pixel grid**: align all strokes to 0.5pt increments
- **Corner radius**: 1pt minor / 2pt major

### 20×20 (iOS Tab Bar)

iOS Tab Bar template images are typically 25pt with the visual mass at ~20×20pt. Use this for Tab Bar-only sets.

- **Live area**: 18×18 (1pt keyline padding)
- **Stroke weight**: 1.5pt outlined, full silhouette filled
- **Pixel grid**: 0.5pt increments
- **Corner radius**: 1pt default

### 16×16 (Small contexts)

Inline icons, list affordances, system tray. Hardest to get right — every pixel matters.

- **Live area**: 14×14 (1pt keyline padding)
- **Stroke weight**: 1.25pt or solid silhouette only
- **Pixel grid**: 1pt increments mandatory
- **Corner radius**: 1pt or square

## Keyline Shapes

Keyline shapes are reference primitives that ensure icons of different topology feel the same optical size. Material Design uses four:

- **Square keyline**: 18×18 (centered) — anchors square-feeling icons
- **Circle keyline**: ⌀20 — anchors round icons (slightly larger to compensate for smaller perceived area)
- **Vertical rectangle keyline**: 16×20 — anchors tall icons
- **Horizontal rectangle keyline**: 20×16 — anchors wide icons

For 24×24 grid, keyline values above. Scale proportionally for 20×20 and 16×16.

Apply keylines as **construction guides**, not hard bounds. Some icons (e.g., a magnifying glass with diagonal handle) need to extend slightly past the keyline to feel right at the same optical weight.

## Optical Sizing

Geometric pixel equality ≠ optical equality. Three corrections to apply consistently:

### Diagonal stroke compensation

Diagonals appear thinner than orthogonal strokes at the same numeric weight. Compensate by **3-7%** thicker on diagonals.

Example: 1.75pt orthogonal → 1.85pt diagonal.

### Circle overshoot

A circle drawn at the exact same height as a square will look smaller. Overshoot circles by **1-2%** of the bounding box.

Example: 24×24 grid, circle should be ⌀24.5 not ⌀24.

### Negative-space density compensation

Icons with dense negative space (e.g., a wifi icon's gaps) read as visually smaller. Slight overall scale-up (**2-3%**) helps balance them against simpler shapes.

## Stroke Contrast

Most icon sets use **uniform stroke weight** for simplicity. Some brands use a contrast pair (e.g., 1pt thin / 2pt thick). Rules:

- **Uniform** — every stroke in the set is the same weight. Easiest to maintain. Default choice.
- **Contrast pair** — two weights only, used consistently (e.g., outline=2pt, internal detail=1pt). Document which goes where.
- **Modulated** — variable stroke within one icon. Almost never used in UI icon sets; reserved for illustrative marks.

If Brand DNA specifies a contrast pair, document the application rule (where each weight is used) and apply it across every icon.

## Stroke Joins and Caps

Must be consistent across the set:

- **Caps**: `butt` / `round` / `square`. Round is most common. Match the brand's terminal style.
- **Joins**: `miter` / `round` / `bevel`. Round is forgiving and most common.
- **Miter limit**: if using miter joins, set explicitly (e.g., `stroke-miterlimit: 4`) to avoid artifacts at sharp corners.

## Pixel Alignment

All strokes and shape edges must align to the pixel grid at the target export size. For SVG masters at 24×24:

- 1pt strokes: integer-pixel positions
- 1.5pt and 2pt strokes: half-pixel positions allowed (centered on pixel boundaries)
- Avoid: sub-half-pixel positions, fractional pixel coordinates

Validate by exporting at target size and zooming 800-1200% to inspect.

## Construction Templates

A reusable construction template per grid:

```
24×24 grid (SVG):
- Bounding box: 24×24
- Keyline guides: square 18×18, circle ⌀20, vertical 16×20, horizontal 20×16
- Pixel grid: 1pt and 0.5pt rulers
- Stroke baseline: 0pt and 1pt offset rules
```

Save these as reusable Pencil/.pen frames or Figma components for the project.

## Failure Modes

- **No grid** — icons drawn freehand drift in size and weight
- **Grid present but ignored** — icons technically on grid but optical balance never checked
- **Inconsistent stroke weight** — rounding 1.75pt to 1.7pt or 1.8pt across icons
- **Missing diagonal compensation** — diagonal strokes appear thin even with grid alignment
- **No keyline shapes used** — square icons end up looking bigger than circular ones
