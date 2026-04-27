# Tab Bar / Bottom Nav Validation

In-context testing protocol for icon sets that ship in Tab Bar (iOS) or Bottom Nav (Android). This is workflow step 11. Quantitative evaluation passes nothing if the set falls apart on a real screen — this file defines the contexts every set must survive.

## Mandatory Contexts

For any Tab Bar / Bottom Nav icon set, validate in these contexts before declaring ship-ready:

### 1. iOS Tab Bar — light mode

- Render Tab Bar with all icons + labels at full 25pt
- Light system background, default tint color
- Both selected and unselected states shown (one selected, others unselected)
- Verify: each icon distinct, labels coherent, selected state obvious

### 2. iOS Tab Bar — dark mode

- Same as above, dark system background, dark mode tint
- Verify: contrast holds, no icon disappears

### 3. iOS Tab Bar — at 25pt with realistic labels

- Real label lengths (not "Tab 1, Tab 2"); use actual destination names
- Verify: label truncation doesn't hide meaning
- Verify: icon + label combination doesn't feel cramped

### 4. iOS Tab Bar — with photo wallpaper showing through

- Translucent Tab Bar over a photo wallpaper
- Verify: icons readable against varied backdrops
- Verify: tint color contrasts adequately

### 5. Android Bottom Nav — light theme

- Material 3 Bottom Nav with all destinations + labels
- Active destination uses pill background (default Material 3) or no background per project preference
- Verify: active vs inactive obvious, labels readable

### 6. Android Bottom Nav — dark theme

- Same as above, dark Material theme
- Verify: contrast holds

### 7. Android Bottom Nav — themed (Material You)

- Bottom Nav with user-customized accent color (Material You dynamic color)
- Test against 3 dynamic palettes: warm, cool, neutral
- Verify: icons read clearly under all tints

### 8. Adjacent to system icons

- iOS: place app's Tab Bar adjacent to a system Tab Bar (e.g., screenshot from Messages or Settings) at the same scale
- Android: place app's Bottom Nav adjacent to a Material 3 default
- Verify: app icons feel native (not cheap or off-brand) but distinguishable from system

### 9. Competitor row

- Mock up: a row of 8 icons combining your set with 4 competitor app icons at the same scale
- Verify: your set doesn't disappear (recognition), doesn't shout (cohesion)
- Verify: still reads as a family while competitors look different

### 10. Small-size fallback (if any icon needs it)

- For sets that include 16pt notification or inline contexts, render at 16pt
- Verify: icons designed for 24pt either work at 16pt or have a documented small-size variant

## Validation Output Format

```markdown
## Context Validation

### iOS Tab Bar — Light Mode
[mockup or rendered SVG]
✓ All icons distinct
✓ Selected state clear (Home, filled)
✗ Settings icon appears slightly heavy in row

### iOS Tab Bar — Dark Mode
[mockup or rendered SVG]
✓ Contrast holds with darkmode tint
✓ No icon disappears

### Android Bottom Nav — Light Theme
[mockup or rendered SVG]
✓ Active pill works with all icons
✓ Labels coherent with icon meaning

### ... (etc for each mandatory context)

## Issues Found
1. Settings icon heavy in row — reduce gear teeth count
2. Library icon hard to distinguish from Activity at 20pt — test alternative metaphor
3. Profile icon needs slight up-shift for optical centering in Tab Bar bounds

## Ship Verdict
- Ship with follow-ups: 3 issues identified, none blocking
```

## Mockup Rendering

The skill can render context mockups via:

1. **Inline SVG composition** — wrap icons in Tab Bar / Bottom Nav frames defined as SVG
2. **HTML preview** — use [`render_icon_contact_sheet.py`](../scripts/render_icon_contact_sheet.py) to generate an HTML page with Tab Bar / Bottom Nav frames
3. **Pencil/.pen frame** — open a .pen with reference Tab Bar / Bottom Nav layouts and place icons

For all three, use the documented frame dimensions:

- iOS Tab Bar: 393×83pt frame (iPhone 15 standard), icons at 25pt within
- Android Bottom Nav: 360×80dp frame (Material 3 default), icons at 24dp within

## What Validates and What Doesn't

### Validation does NOT replace user testing

- A skilled designer + this protocol catches most issues
- Real users may misunderstand metaphors that pass cliché audit
- Instrument the launch with analytics on tab discovery; iterate based on data

### Validation IS the difference between shipping and not

- Skipping these contexts is the most common cause of "icons looked great in Figma, terrible in production"
- Mandatory before declaring ship-ready

## Failure Modes

- **Validating at master size only** — 24×24 master can pass while 20pt Tab Bar version fails
- **Skipping dark mode** — contrast issues are common in dark mode Tab Bar
- **Skipping themed (Material You)** — colored backgrounds expose contrast holes
- **Using fake labels** — real label lengths interact with icon perception
- **Skipping the competitor row** — context-free icons can read fine and still disappear in real Tab Bar adjacent to competitor apps
- **Treating "looks good in mockup" as ship-ready** — mockup is necessary but not sufficient
