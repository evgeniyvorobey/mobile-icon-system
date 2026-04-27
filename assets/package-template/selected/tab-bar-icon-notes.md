# Tab Bar Icon Notes — {{PROJECT_NAME}}

Project: {{PROJECT_NAME}}
Owner: {{OWNER}}
Date: {{DATE}}
Skill version: {{SKILL_VERSION}}

iOS Tab Bar specifics for this icon set.

## Canonical Specifications

- **Size**: 25pt template image
- **Visible mass target**: ~20×20pt within the 25pt frame
- **Format**: PDF template image (preferred) or PNG @1x/2x/3x
- **Render As**: Template Image (asset catalog setting)

## Asset Catalog Setup

For each Tab Bar icon, in `Assets.xcassets`:

1. Add icon as image set
2. Drop in PDF (single asset, scales automatically) or PNG @1x/2x/3x
3. In the right panel, set **Render As**: Template Image
4. Confirm: image preview should appear black-on-white in the asset catalog

If image appears with original color when selected, Render As is misconfigured — Tab Bar tint won't work.

## States

| State | Variant | iOS API |
|---|---|---|
| Selected | filled | `tabBarItem.selectedImage` |
| Unselected | outlined | `tabBarItem.image` |

## Tinting

```swift
tabBar.tintColor = .systemBlue  // selected
tabBar.unselectedItemTintColor = .systemGray  // unselected
```

For custom theming:

```swift
tabBar.tintColor = .brandPrimary  // from your color tokens
tabBar.unselectedItemTintColor = .brandSecondary
```

## Light + Dark Mode

Tab Bar tint adapts automatically when using semantic colors (`UIColor.label`, `UIColor.systemBlue`, etc.).

For custom brand colors, define light + dark variants in the asset catalog color set:

- Light appearance: tint A
- Dark appearance: tint B

Verify on a real device or simulator in both modes.

## Liquid Glass / iOS 26+ (if applicable)

For iOS 26+ where Tab Bar uses Liquid Glass material:

- Icons sit behind translucent glass distortion
- Stroke clarity matters more — verify legibility against varied wallpapers
- Test against high-contrast and busy backgrounds

## Common Mistakes

- **Forgetting Render As: Template Image** — silent tinting failure
- **Baking color into PDF** — overrides system tinting
- **Using regular images instead of template** — colors don't adapt to tint
- **Wrong size** — exporting at 24pt instead of 25pt produces slightly cropped icons

## Per-Icon Notes

Document any icon-specific behavior:

| Icon | Note |
|---|---|
| | |
| | |

## Verification Checklist

- [ ] All icons exported as PDF template images
- [ ] Render As: Template Image set on each
- [ ] Light mode tinting verified on simulator
- [ ] Dark mode tinting verified on simulator
- [ ] Real device test on at least one iPhone model
- [ ] Tab Bar with photo wallpaper backdrop verified
