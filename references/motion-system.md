# Motion System

Animated icons are a separate subsystem from static icon style. Treat motion as interaction behavior: it must preserve the icon system's semantic meaning, accessibility guarantees, and export contract without changing the visual rules for static glyphs.

## Scope

Use this subsystem for Lottie or dotLottie icon motion such as confirmation, loading, state change, refresh, upload, download, attention, or small transition feedback. Do not use it to define a visual style pack. Style remains governed by the base icon system; this file governs trigger, timing, export, fallback, and evidence.

Motion is optional. A static icon must remain the source of truth for recognition, accessibility labels, contrast, touch targets, and selected/unselected state meaning.

## Motion Spec Format

Store one JSON object per animated icon, or a JSON file with a top-level `motionSpecs` array.

```json
{
  "iconId": "ic_action_refresh",
  "trigger": "pullToRefreshReleased",
  "semanticPurpose": "Confirms that refresh has started and the list is updating.",
  "durationMs": 420,
  "easing": "standard",
  "allowedProperties": ["rotation", "opacity"],
  "timeline": [
    {
      "atMs": 0,
      "state": "idle",
      "properties": { "rotation": 0, "opacity": 1 }
    },
    {
      "atMs": 220,
      "state": "active",
      "properties": { "rotation": 180, "opacity": 1 }
    },
    {
      "atMs": 420,
      "state": "settled",
      "properties": { "rotation": 360, "opacity": 1 }
    }
  ],
  "motionTriggers": [],
  "deliverables": {
    "lottie": "exports/lottie/ic_action_refresh.json",
    "dotLottie": "exports/dotlottie/ic_action_refresh.lottie"
  },
  "staticFrame": {
    "path": "exports/static/ic_action_refresh_static.svg",
    "timeMs": 420,
    "purpose": "Final settled refresh glyph used when motion is disabled."
  },
  "reducedMotion": {
    "mode": "staticFrame",
    "fallback": "Use the static frame and update surrounding status text.",
    "motionTriggers": [],
    "durationMs": 0
  },
  "validationEvidence": {
    "lottiePreview": "exports/reviews/ic_action_refresh_lottie_preview.png",
    "dotLottiePreview": "exports/reviews/ic_action_refresh_dotlottie_preview.png",
    "staticFrameReviewed": true,
    "reducedMotionTested": true,
    "platforms": ["ios", "android"]
  }
}
```

Required fields:

| Field | Requirement |
|---|---|
| `iconId` | Existing icon ID, preferably `ic_{scope}_{name}`. |
| `trigger` | Product event that starts playback; avoid vague values like `onLoad` unless the icon is truly a loader. |
| `semanticPurpose` | What the motion communicates, not how it looks. |
| `durationMs` | Per-play or per-loop duration in milliseconds. |
| `easing` | Named easing or explicit cubic bezier. |
| `allowedProperties` | Properties the animator may change. |
| `timeline` | Ordered key moments with `atMs`, state, and changed properties. |
| `deliverables.lottie` | Lottie JSON export path. |
| `deliverables.dotLottie` | dotLottie package path. |
| `staticFrame` | Static frame that preserves meaning when motion is unavailable. |
| `reducedMotion` | Fallback behavior for users who request reduced motion. |
| `validationEvidence` | Proof that exports, static frame, and reduced-motion behavior were checked. |

## Timing

Icon motion should be fast enough to feel attached to the user action and slow enough to be legible:

- Micro feedback: 120-240 ms.
- State confirmation: 200-500 ms.
- Transfer, refresh, or progress handoff: 400-900 ms.
- Looping loaders: 600-1200 ms per loop.
- Hard validation cap: 50-1500 ms.

Autoplay is allowed only when the semantic state is currently active, such as a loading indicator. Decorative autoplay is out of scope for this subsystem.

## Easing

Use named easing for consistency, or an explicit `cubic-bezier(x1, y1, x2, y2)` when a named curve cannot express the interaction.

Recommended names:

| Name | Use |
|---|---|
| `linear` | Progress indicators and mechanical trim changes. |
| `standard` | Default icon response and most state changes. |
| `decelerate` | Elements arriving or settling into place. |
| `accelerate` | Elements leaving or dismissing. |
| `ease-in-out` | Symmetric toggles or reversible motion. |
| `emphasized` | Rare, higher-salience confirmation where the icon still stays stable. |

Lottie keyframes support in and out easing handles. The authoring spec may name curves in product language, but exported Lottie must preserve the equivalent handle intent.

Avoid bounce, elastic, spring overshoot, or large y-axis overshoot for small UI icons unless product testing proves it is necessary and reduced-motion fallback has been verified.

## Allowed Properties

Allowed by default:

- `opacity`
- `scale`
- `scaleX`
- `scaleY`
- `translateX`
- `translateY`
- `rotation`
- `strokeDashOffset`
- `pathTrimStart`
- `pathTrimEnd`
- `pathTrimOffset`
- `fillColor`
- `strokeColor`

Disallowed by default:

- Blur, glow, shadow animation, depth-of-field, parallax, perspective, camera, 3D transforms.
- Path morphs that change the icon metaphor rather than revealing an existing construction.
- Color-only meaning changes without a static shape/state equivalent.
- Multi-axis or multi-speed effects used as decoration.

## Lottie Deliverables

Ship both:

- Lottie JSON: `exports/lottie/{iconId}.json`
- dotLottie package: `exports/dotlottie/{iconId}.lottie`

Keep the static SVG master as the recognition source. Lottie and dotLottie are runtime delivery formats, not the source of icon identity.

Lottie JSON is a JSON-encoded vector animation format with registered media type `video/lottie+json`. dotLottie v2 packages one or more Lottie animations in a ZIP-based `.lottie` file and uses root `manifest.json` metadata for `animations`, optional `themes`, and optional `stateMachines`.

## Reduced Motion

Every animated icon must provide a `staticFrame` and `reducedMotion` fallback.

Reduced-motion fallbacks may use:

- `staticFrame`
- `dissolve`
- `highlightFade`
- `colorShift`

Reduced-motion fallbacks must not include:

- Depth simulation, parallax, animated blur, or depth-of-field.
- Multi-axis motion, multi-speed motion, scaling/zooming, spinning, or vortex effects.
- Ongoing/autoplay motion without a stop control.
- Meaningful motion removed without replacing the meaning through static state, dissolve, highlight, color shift, text, or surrounding UI state.

When the default animation contains a potentially sensitive motion trigger, the fallback must disable or change that trigger. Do not make reduced motion a slower copy of the same problematic movement.

## Validation

Run the validator against each motion spec:

```bash
python3 scripts/validate_motion_spec.py path/to/motion-spec.json
```

The validator checks required fields, duration sanity, easing format, allowed properties, Lottie and dotLottie deliverables, static frame, reduced-motion fallback, and banned reduced-motion triggers.

## Evidence Checklist

Before shipping, record validation evidence:

- [ ] Lottie JSON opens in the target renderer.
- [ ] dotLottie package opens in the target renderer.
- [ ] Static frame reads as the same icon state at 16/20/24 pt.
- [ ] Reduced-motion setting was tested on every platform in scope.
- [ ] Screen-reader label and state remain correct during and after motion.
- [ ] Motion does not become the only carrier of meaning.
- [ ] Timeline and easing match the JSON spec.

## Sources

- [Lottie Format Specification](https://lottie.github.io/lottie-spec/dev/specs/format/) — JSON top-level format, `video/lottie+json`, scalable vector-animation usage.
- [Lottie Properties Specification](https://lottie.github.io/lottie-spec/1.0/specs/properties/) — keyframe `i` and `o` easing handles and cubic-bezier interpolation.
- [dotLottie v2.0 Specification](https://dotlottie.io/spec/2.0/) — `.lottie` package structure and `manifest.json` fields for animations, themes, and state machines.
- [Apple Reduced Motion Evaluation Criteria](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria) — reduced-motion triggers and replacement patterns.
