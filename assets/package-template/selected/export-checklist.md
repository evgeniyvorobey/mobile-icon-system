# Export Checklist — {{PROJECT_NAME}}

Project: {{PROJECT_NAME}}
Owner: {{OWNER}}
Date: {{DATE}}
Skill version: {{SKILL_VERSION}}

Engineering checklist for shipping the icon set. Each item is a binary check.

## SVG Masters

- [ ] All icons exported as SVG masters at the documented grid (24×24 default)
- [ ] Naming convention applied: `ic_{scope}_{name}_{state}.svg`
- [ ] State pairs (filled + outlined) present for every Tab Bar / Bottom Nav icon
- [ ] No baked color in masters
- [ ] Stroke `linecap` and `linejoin` consistent across set
- [ ] Pixel alignment verified at target export sizes
- [ ] Committed to design system repo or shared location

## iOS Exports

- [ ] PDF template images generated for all Tab Bar icons (filled + outlined)
- [ ] Asset catalog imageset created for each icon
- [ ] Render As: Template Image set on every imageset
- [ ] Tab Bar tinting verified on simulator (light + dark mode)
- [ ] Real device test on at least one iPhone model
- [ ] Liquid Glass / translucent backdrop tested (iOS 26+ if applicable)

## Android Exports

- [ ] Vector drawable XML generated for all Bottom Nav icons (filled + outlined)
- [ ] `android:tint` attribute set per state (`?attr/colorOnSecondaryContainer` active, `?attr/colorOnSurfaceVariant` inactive — or project-specific)
- [ ] Vector drawables placed in `res/drawable/`
- [ ] Light theme tinting verified on emulator
- [ ] Dark theme tinting verified on emulator
- [ ] Themed (Material You) verified under multiple dynamic palettes
- [ ] Real device test on at least one Android phone (Android 13+)

## Cross-Platform / Hybrid

- [ ] React Native / Flutter / web exports generated if applicable
- [ ] Tinting verified per platform's mechanism (currentColor for web, color prop for RN, etc.)

## Documentation

- [ ] [`reviews/icon-system-rules.md`](../reviews/icon-system-rules.md) committed to docs
- [ ] [`selected/usage-guidance.md`](usage-guidance.md) committed to docs
- [ ] [`selected/rationale.md`](rationale.md) committed to docs
- [ ] [`selected/tab-bar-icon-notes.md`](tab-bar-icon-notes.md) committed to docs
- [ ] [`selected/bottom-nav-notes.md`](bottom-nav-notes.md) committed to docs

## QA

- [ ] iOS Tab Bar with all icons + labels — light mode visual QA
- [ ] iOS Tab Bar with all icons + labels — dark mode visual QA
- [ ] Android Bottom Nav with all icons + labels — light theme visual QA
- [ ] Android Bottom Nav with all icons + labels — dark theme visual QA
- [ ] Tab Bar over photo wallpaper backdrop tested
- [ ] Touch targets verified ≥44pt iOS / ≥48dp Android
- [ ] CVD simulation passed (if duotone in use)
- [ ] WCAG 2.2 contrast verified (icon vs background, 3:1 minimum)

## Pre-Ship Sign-off

- [ ] Design lead approval
- [ ] Engineering lead approval
- [ ] QA approval
- [ ] Brand / marketing approval (if brand-significant)

## Post-Ship Monitoring

Document analytics to monitor after launch:

- [ ] Tab Bar destination discovery rates (especially for any borderline-cliché icons)
- [ ] Settings / less-common icon usage (small-size collapse risk)
- [ ] User feedback on icon recognition

## Unresolved Risks Acknowledged

List any risks documented in [`rationale.md`](rationale.md) that ship with the set:

- 
- 
