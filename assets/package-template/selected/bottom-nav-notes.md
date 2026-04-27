# Bottom Navigation Notes — {{PROJECT_NAME}}

Project: {{PROJECT_NAME}}
Owner: {{OWNER}}
Date: {{DATE}}
Skill version: {{SKILL_VERSION}}

Android Bottom Navigation specifics for this icon set, aligned with Material Design 3.

## Canonical Specifications

- **Size**: 24×24dp
- **Format**: vector drawable XML
- **Touch target**: 48×48dp minimum (icon + padding)
- **Active indicator**: pill-shaped background (Material 3 default; can be disabled per project preference)

## Resource Setup

For each Bottom Nav icon:

1. Convert SVG master → vector drawable XML (Android Studio: Drag-drop SVG into `res/drawable/`)
2. Verify generated XML — should look like:

```xml
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24"
    android:tint="?attr/colorOnSurface">
    <path
        android:fillColor="@android:color/black"
        android:pathData="M12,4 ..."/>
</vector>
```

3. Set `android:tint` per state (see Tinting section)

## States

| State | Variant | Resource |
|---|---|---|
| Active | filled | `ic_tab_{name}_filled.xml` |
| Inactive | outlined | `ic_tab_{name}_outlined.xml` |

## Tinting

Material 3 Bottom Nav tints automatically based on theme attributes:

- Active: `?attr/colorOnSecondaryContainer`
- Inactive: `?attr/colorOnSurfaceVariant`

For custom theming, override the relevant theme attributes in `themes.xml`.

```xml
<style name="Theme.YourApp" parent="Theme.Material3.DayNight">
    <item name="colorOnSecondaryContainer">@color/brandPrimary</item>
    <item name="colorOnSurfaceVariant">@color/brandSecondary</item>
</style>
```

## Light + Dark Theme

Material's day/night theme system handles light/dark automatically. Verify:

- Light theme (default `Theme.Material3.Light`)
- Dark theme (default `Theme.Material3.Dark`)
- Both themes show icons with adequate contrast

## Themed Icons (Material You) — Android 13+

For dynamic color support:

- Bottom Nav inherits dynamic color when using `Theme.Material3.DynamicColors.*`
- No additional work needed if using Material 3 defaults
- For brand-locked colors that should NOT inherit dynamic color, hardcode the color tokens

Verify under multiple Material You palettes:

- Warm red wallpaper
- Cool blue wallpaper
- Neutral gray wallpaper
- Earth green wallpaper
- Vibrant purple wallpaper

## Active Indicator (Pill Background)

Material 3 default Bottom Nav shows a pill behind the active icon. For projects that prefer no pill:

```xml
<style name="Widget.YourApp.NavigationBar" parent="Widget.Material3.NavigationBarView">
    <item name="itemActiveIndicatorStyle">@style/NoActiveIndicator</item>
</style>

<style name="NoActiveIndicator" parent="Widget.Material3.NavigationBarView.ActiveIndicator">
    <item name="android:width">0dp</item>
    <item name="android:height">0dp</item>
</style>
```

## Common Mistakes

- **PNG instead of vector drawable** — loses crispness across densities, can't be tinted
- **Hardcoded color in `android:fillColor`** — overrides theme tinting
- **Wrong viewport size** — should match grid (24)
- **Forgetting the active indicator** — Material 3 default is pill background

## Per-Icon Notes

| Icon | Note |
|---|---|
| | |
| | |

## Verification Checklist

- [ ] All icons exported as vector drawable XML
- [ ] `android:tint` set correctly per state
- [ ] Light theme tinting verified
- [ ] Dark theme tinting verified
- [ ] Themed (Material You) verified under 3+ dynamic palettes
- [ ] Active indicator behavior matches design intent
- [ ] Real device test on at least one Android phone (Android 13+)
