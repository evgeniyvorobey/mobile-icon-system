# Claymorphism

Claymorphism was coined by Michał Malewicz at Hype4 ([hype4.academy/articles/coding/how-to-create-claymorphism-using-css](https://hype4.academy/articles/coding/how-to-create-claymorphism-using-css)). It delivers warmth and tactility on static SVG using only `box-shadow` (or SVG-filter equivalent) plus generous corner radius — cheap to render, trivial to author from rules. Critically, claymorphism **survives the accessibility filter that kills neumorphism**: the primary glyph stays a high-contrast solid silhouette, so WCAG 2.2 §1.4.11 is satisfied by the body alone — Axess Lab's neumorphism critique ([axesslab.com/neumorphism/](https://axesslab.com/neumorphism/)) does not apply.

This pack ships in v0.4 because it fills a real product gap: brands wanting personality and warmth without the contrast trap of neumorphism or the platform-foreign look of skeuomorphism. Natural fit for fintech-with-personality, kid-friendly products, wellness, "approachable not childish" brands.

## When to use this style

**Strong fit:** brand archetypes "warm / friendly / approachable / playful-but-not-childish", pastel-leaning palettes, kids' apps, wellness apps, fintech that wants less serious than category default.

**Weak fit:** enterprise / B2B "serious / minimal" brands, sharp-corner Brand DNA (without heavy radius reads as colored card with drop shadow), stroke-only DNA (stroked plastic looks wrong).

**Decision flowchart hint:** if Brand DNA mandates sharp corners or stroke-only, refuse and surface in phase 5. The user can override explicitly; the skill must not override silently.

## Construction rules

### Layer model

**3 logical layers**, achievable in pure SVG with a simple filter chain:

1. `body` — primary glyph as solid fill with large border-radius (squircle preferred). Filled at brand color, alpha 1.0.
2. `outer-shadow` — drop shadow under body. `<filter>` with `<feGaussianBlur stdDeviation="8"/>` plus offset, tinted in body hue.
3. `inner-highlight` — inner shadow at bottom edge for soft "pressed-in" feel. `<filter>` with `<feGaussianBlur>` plus inset composite, tinted lighter than body.

### Hype4 canonical recipe

Verified at [hype4.academy/articles/coding/how-to-create-claymorphism-using-css](https://hype4.academy/articles/coding/how-to-create-claymorphism-using-css):

```css
box-shadow:
  0 35px 68px 0 rgba(170, 63, 254, 0.42),
  inset 0 -8px 16px 0 #D6A2FF;
```

Translated to SVG-equivalent at 24pt master canvas: outer shadow `dy=4`, `stdDeviation=8`, fill at body-hue at alpha 0.42; inner highlight `dy=-1`, `stdDeviation=2`, fill at body-hue +20% L at alpha 1.0 inside the shape.

### Numerical thresholds

- Body border-radius: **24-50% of side** (24% icon-shaped, 50% circular)
- Outer shadow `dy`: **4** at 24pt master
- Outer shadow `stdDeviation`: **8** at 24pt master
- Outer shadow opacity: **0.38-0.46**
- Outer shadow tint: body-hue darkened **25-32% L**
- Inner highlight `dy`: **-1** at 24pt master
- Inner highlight `stdDeviation`: **2** at 24pt master
- Inner highlight opacity: **0.85-1.0**
- Inner highlight tint: body-hue lightened **15-22% L**
- Body color L (HSL): **40-60%** (pastel); **clamp ≤70% on light backgrounds** for WCAG 3:1
- Centroid shift: **0.5-1.0% upward** (the shadow biases the icon downward)
- Live area shrink: **12%** (shadow extends apparent bounding box ~12% downward)

### SVG features required

`<filter>` with `<feGaussianBlur>`, `<feOffset>`, `<feFlood>`, `<feComposite operator="in"/>` to tint shadow to body hue. Inner highlight: `<feComponentTransfer>` + `<feComposite operator="arithmetic"/>` to invert alpha. Alternative: pre-compose the inner highlight as a fixed `<path>` inside body with `clip-path` referencing body.

### Stroke / fill rules

Body is **always fill**. **Strokes forbidden** — clay reads as plastic mass; stroked plastic looks wrong. Refuse in phase 5 if brand is stroke-only.

### Color rules specific to this style

Pastel palette canonical. Brand-primary at 40-55% L in HSL; if darker, lighten body to that range and use original brand color as outer shadow tint. **Two values per icon**: body color + body-hue-darkened-30%-for-shadow. Inner highlight is **body-hue-lightened-20%, NOT white** — white inner highlights bleach the body.

### Optical correction adjustments specific to this style

Apply **0.5-1.0% upward centroid shift** (outer shadow biases perceived weight downward) and **12% live-area shrink** on body geometry (shadow extends apparent bounding box ~12% downward).

## Brand DNA mapping

| Brand DNA dimension | Behavior under Claymorphism |
|---|---|
| Geometric alphabet | inherited unchanged |
| Stroke language | **disabled** (style is fill-based) |
| Terminal style | **disabled** (no exposed terminals) |
| Corner treatment | **overridden** — forced to 24-50% radius |
| Color logic | **overridden** — body is brand-primary lightened to pastel L if needed; shadow is body-hue darkened; inner highlight is body-hue lightened |
| Optical correction | **augmented** — adds 0.5-1.0% upward centroid shift and 12% live-area shrink |

**Refuse if:** brand demands sharp corners or stroked icons. The user can override their Brand DNA explicitly in phase 5, but the skill must not make that call silently.

## Accessibility implications

WCAG 2.2 §1.4.11 applies to the body — the **body fill alone must hit 3:1 against surface**. Shadow stack is decorative and contributes nothing to perceived contrast (Axess Lab neumorphism critique applies to any shadow-based claim). State changes must use body fill, shape, or structural delta — **never shadow strength alone**. **Forced-Colors mode collapses shadows entirely**; design for a "shadowless" fallback. Pastel risks failing 3:1 if body L > 80%; clamp body L ≤70% on light backgrounds. See [`accessibility.md`](../accessibility.md).

## Anti-patterns

1. **Grey shadows on colored body** — kills clay illusion. Shadows must be tinted with body hue, not desaturated.
2. **Sharp corners** — without heavy radius reads as colored card with drop shadow. Not the same style.
3. **Multiple bodies per icon** — stacked candy look; doesn't survive small sizes and reads as illustration.
4. **Inner highlight in white** — body looks bleached. Use body-hue-lightened-20%, never `#FFFFFF`.
5. **Importing into a flat-design brand without consultation** — surface the conflict in phase 5; don't override silently.

## Reference library

- [codeadrian.github.io/clay.css](https://codeadrian.github.io/clay.css/) — MIT, canonical CSS implementation referenced by Hype4
- [hype4.academy/tools/claymorphism-generator](https://hype4.academy/tools/claymorphism-generator) — Hype4's CSS generator
- [hype4.academy/articles/coding/how-to-create-claymorphism-using-css](https://hype4.academy/articles/coding/how-to-create-claymorphism-using-css) — definition source by Michał Malewicz
- [blog.logrocket.com/implementing-claymorphism-css/](https://blog.logrocket.com/implementing-claymorphism-css/) — secondary engineering reference
- [blog.openreplay.com/implementing-claymorphism-css/](https://blog.openreplay.com/implementing-claymorphism-css/) — third-party verification of the canonical recipe
- [axesslab.com/neumorphism/](https://axesslab.com/neumorphism/) — accessibility critique that justifies WHY claymorphism beats neumorphism

## Workflow integration

- **Phase 5** — claymorphism sub-block (body radius, shadow `dy`/`stdDeviation`/opacity, inner highlight `dy`/`stdDeviation`/tint, body L clamp, centroid shift). Refuse if Brand DNA forbids fills or rounded corners.
- **Phase 7** — each variant produces an SVG with body `<path>` plus filter definitions. Filters in single `<defs>` block referenced by `filter="url(#clay)"`.
- **Phase 8 Pass A** — body-radius compliance check (24-50% of side). Pass B asks: "Does body color survive 3:1 alone?" and "Is shadow tinted in body hue?"
- **Phase 9** — apply centroid shift and live-area reduction. Compare against `assets/references/tier-a-claymorphism/` when corpus is populated.
- **Phase 11** — render against light, dark, pastel-on-pastel surfaces. 3:1 check on body alone (ignore shadows). Forced-Colors mode test with shadows stripped.

## Failure modes

- Grey / desaturated shadows on colored body — kills the clay illusion.
- Sharp corners (radius < 24% of side) — reads as flat card with shadow.
- White inner highlight — body reads as bleached.
- Body L > 70% on light background — fails 3:1 per the clamp rule.
- State distinction by shadow strength alone — fails Forced-Colors and accessibility.
- Multiple body masses per icon (stacked clay) — reads as illustration; doesn't survive 16-24pt.
- Applied to stroke-only Brand DNA without explicit user override.
- Outer shadow `dy` or `stdDeviation` outside documented bands — icon floats too high or presses too deep.

## Sources

See Reference library above. Plus W3C WCAG 2.2 §1.4.11 — [w3.org/WAI/WCAG22/Understanding/non-text-contrast.html](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).
