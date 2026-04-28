# Accessibility

Mandatory accessibility checks for any icon set. Icons that convey information are subject to WCAG 2.2 — non-text contrast, target size, and screen-reader labeling — and to platform touch-target rules (iOS HIG 44pt, Material 48dp). This file is the authoritative checklist for the skill's accessibility pass and is loaded during workflow phase 5 (rules), phase 10 (evaluate), and phase 11 (validate in context).

## Why this matters

An icon that fails accessibility is shipped broken: a low-contrast Tab Bar tint hides the active state from low-vision users, a 32×32dp touch target excludes anyone with motor impairment, an unlabeled icon-only button is invisible to VoiceOver/TalkBack. None of this is optional — App Store and Play Store reviewers cite these, and many regions (EU EAA, US ADA, UK Equality Act) make WCAG 2.1/2.2 AA a legal requirement for many app categories.

## WCAG 2.2 requirements relevant to icons

### 1.4.11 Non-text Contrast (AA)

Icons and other graphical objects that convey information must have **3:1 contrast** against their background.

- Tab Bar selected/unselected glyph vs Tab Bar background → 3:1
- Action icon glyph vs button surface → 3:1
- Status icon vs the surface it sits on → 3:1
- Decorative icons (no information conveyed) — exempt, but mark as decorative for screen readers

When the icon sits on a translucent material (iOS Liquid Glass, Material 3 surfaces), test contrast against the **worst-case backdrop** the material can show, not the nominal token color.

### 2.5.5 / 2.5.8 Target Size

- **WCAG 2.5.8 (AA, minimum)**: target ≥ **24×24 CSS px**
- **WCAG 2.5.5 (AAA, enhanced)**: target ≥ **44×44 CSS px**
- **iOS HIG**: minimum **44×44pt** (matches AAA)
- **Material 3**: minimum **48×48dp** (slightly above AAA)

Touch target is the **hit area**, not the visible glyph. A 24pt visible icon inside a 48dp button is fine. A 24pt icon as a bare tappable element with no padding is not.

### 1.4.3 Contrast (Minimum) — text inside icons

If an icon contains text characters (e.g., "Aa" inside a magnifying glass), the text must hit **4.5:1** against its background. Avoid text inside icons when possible — it rarely scales below 24pt.

### 2.4.7 Focus Visible

Icons used as focusable controls must show a visible focus indicator (relevant for keyboard, switch control, hardware keyboard on iPad / Android tablets).

### 2.3.3 Animation from Interactions / `prefers-reduced-motion`

Animated icons (loading spinners, pull-to-refresh, micro-interactions) must respect the user's reduced-motion preference. Provide a static fallback frame.

## Platform touch-target specs

| Surface | iOS | Android | Web (WCAG AA) |
|---|---|---|---|
| Tab Bar / Bottom Nav | 44×44pt hit area; glyph 25pt iOS / 24dp Android | 48×48dp | 24×24 px minimum, 44×44 recommended |
| Toolbar / action icon | 44×44pt | 48×48dp | 24×24 px minimum |
| Inline icon (informational only, not tappable) | 16-20pt | 16-24dp | 16 px+ |
| Notification icon | 12-16pt iOS / 24dp source rendered at 18dp | n/a | n/a |

If an action icon is rendered at 24pt visible glyph, it still needs **at least 10pt of padding around it** on iOS (44 − 24 = 20pt total padding, 10pt per side) to make the hit area legal.

## Screen-reader labeling

Every icon used as a control must have an accessible name. The name describes the **action**, not the **glyph**.

| Surface | iOS | Android | Web |
|---|---|---|---|
| Tab Bar item | `accessibilityLabel`; selection state via `accessibilityTraits` | `contentDescription` + `android:state_selected` | `aria-label` + `aria-current="page"` |
| Icon-only button | `accessibilityLabel` describing action | `contentDescription` describing action | `aria-label` describing action |
| Decorative icon | `accessibilityElementsHidden = true` or `isAccessibilityElement = false` | `android:importantForAccessibility="no"` | `aria-hidden="true"` |
| Icon next to text label | hide icon (`isAccessibilityElement = false`); label is the name | mark icon `importantForAccessibility="no"` | `aria-hidden="true"` on icon |

**Anti-patterns** (do not ship):

- `accessibilityLabel = "icon"` or `"image"` — describes the medium, not the action
- `contentDescription = "settings_icon"` — leaks the asset name
- Localized labels missing for non-English locales
- Tab Bar item without "Selected" trait when active — VoiceOver users cannot tell which tab is current
- Icon-only buttons (e.g., a bare ☰) with no label at all — invisible to assistive tech

## Color-blind safety

Roughly 8% of men and 0.5% of women have a form of color vision deficiency. Icons must communicate without relying on color alone.

- Status icons must differ in **shape**, not only color: success = check mark, error = X or triangle, warning = triangle, info = circle. A green dot vs a red dot fails.
- Selected / unselected Tab Bar must differ in **fill density** (filled vs outlined), not only color tint.
- Heatmaps and category color-coding inside icons must pass simulation under deuteranopia, protanopia, and tritanopia.

When the brand uses red/green semantically (e.g., financial up/down arrows), pair the color with a shape change (up arrow + green vs down arrow + red — never bare green vs red squares).

## Dynamic Type and font scaling

iOS Dynamic Type and Android Font Scale can resize text up to 200%+. Inline icons that sit next to body text should scale proportionally, otherwise they shrink visually as text grows.

- Use SF Symbols' `Image(systemName:).imageScale(.medium)` cadence on iOS, or scale icons with `UIFontMetrics`
- On Android, size inline icons via `sp` units, not `dp`, when they pair with text
- Test the icon set at the largest accessibility text size — does the silhouette still read?

Tab Bar and Bottom Nav icons typically do **not** scale with Dynamic Type (the bar's own height scales label, not glyph). Verify on the target platform version.

## Forced Colors / High Contrast Mode

Windows High Contrast and macOS Increase Contrast can replace icon colors with system tokens. Multi-color icons can collapse into a flat silhouette.

- Test icons under Increase Contrast (macOS) and System Color Filters (iOS / Android)
- Multi-color icons should degrade gracefully to a single-color silhouette
- Never encode meaning in the second color alone — primary silhouette must convey meaning by itself

## Reduced motion

Animated icons must check the user's reduced-motion preference and provide a static fallback. For Lottie/dotLottie icon motion, define and validate the motion contract with [`motion-system.md`](motion-system.md) before exporting runtime assets.

- iOS: `UIAccessibility.isReduceMotionEnabled`
- Android: `Settings.Global.TRANSITION_ANIMATION_SCALE` and `Settings.Global.ANIMATOR_DURATION_SCALE`
- Web: `@media (prefers-reduced-motion: reduce)`

The static fallback must convey the same state — a frozen "loading" icon should still read as "loading" (e.g., a static spinner or a "..." indicator), not as a generic placeholder.

## Skill checklist (run during phase 11)

For every icon set the skill ships, verify:

- [ ] All informational icons hit **3:1 contrast** vs their background, including selected/unselected states and themed (Material You) variants
- [ ] Touch targets meet platform minima: **44×44pt** iOS / **48×48dp** Android — verify in mockup, not just glyph size
- [ ] Each icon-control has an accessible name describing the **action**, not the glyph; localized strings exist for all supported languages
- [ ] Tab Bar / Bottom Nav state communicates via shape (fill vs outline), not only color
- [ ] Status icons differ by shape, not only color
- [ ] If any icon contains text, text contrast hits **4.5:1**
- [ ] If any icon animates, a `prefers-reduced-motion` static fallback exists
- [ ] If any icon ships as Lottie/dotLottie, `python3 scripts/validate_motion_spec.py <motion-spec.json>` passes
- [ ] Icons survive a deuteranopia simulation pass
- [ ] Icons survive Increase Contrast / Forced Colors fallback (single-color silhouette reads)
- [ ] Inline icons paired with text scale with Dynamic Type / Font Scale
- [ ] Decorative icons are explicitly hidden from assistive tech

Failure on any item blocks ship. Document the failure in the package's `cross-icon-audit.md` and propose the fix in the punch list.

## How this integrates with the workflow

| Workflow phase | Accessibility responsibility |
|---|---|
| 4. Build context | Capture target locales, target accessibility tier (AA / AAA), known assistive-tech constraints |
| 5. Icon system rules (gate) | State the contrast budget (target 3:1 minimum, 4.5:1 for any text); state the touch-target rule (44pt iOS / 48dp Android) |
| 7. Generate the set | Construct silhouettes that survive single-color collapse — color is never the only carrier of meaning |
| 8. Cross-icon consistency audit | Confirm state-pair distinction is shape-based, not color-only |
| 10. Evaluate | Score under "platform fit" and "state distinction" with explicit accessibility sub-checks |
| 11. Validate in context | Run the full checklist above; render one set at 200% Dynamic Type + one set under deuteranopia simulation |
| 13. Package | Include `accessibility-notes.md` in the handoff package — labels, traits, contrast measurements, known caveats |

## Sources

- [WCAG 2.2 — Web Content Accessibility Guidelines](https://www.w3.org/TR/WCAG22/) — 1.4.3, 1.4.11, 2.4.7, 2.5.5, 2.5.8, 2.3.3
- [Apple HIG — Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) — 44pt minimum, Dynamic Type, VoiceOver labeling
- [Material 3 — Accessibility](https://m3.material.io/foundations/accessible-design/overview) — 48dp minimum, TalkBack labeling, color contrast tokens
- [Apple — Supporting Voice Control and VoiceOver](https://developer.apple.com/documentation/uikit/accessibility_for_uikit) — `accessibilityLabel`, traits, `isAccessibilityElement`
- [Android — Accessibility developer guide](https://developer.android.com/guide/topics/ui/accessibility) — `contentDescription`, `importantForAccessibility`

When any of these specs feel out of date, run [`live-research.md`](live-research.md) before treating values here as current.

## Failure modes

- **Treating accessibility as a final pass instead of a constraint** — by phase 11 it is too late to change the silhouette to survive single-color collapse
- **Confusing visible glyph size with hit area** — a 24pt glyph in a 32pt button still fails 44pt iOS minimum
- **Color-only state distinction** — a tinted-vs-untinted glyph fails for color-blind users; always pair with fill-vs-outline
- **`accessibilityLabel = "icon"`** — describes the medium, leaks the asset, fails screen reader test
- **Animated icons without reduced-motion fallback** — vestibular-disorder users get sick; legally non-compliant in many regions
- **Skipping localization of accessibility labels** — non-English VoiceOver/TalkBack reads the English string with the wrong language inflection
