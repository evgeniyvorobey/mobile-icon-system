# Prompt Library

Ready-to-use prompts for the mobile icon system skill. Concept prompts stop at the mandatory user-selection gate; after the user confirms icon system rules, the same brief continues into generation, consistency audit, evaluation, and packaging.

All prompts work in both platforms:
- Codex: prefix with `Use $mobile-icon-system.`
- Claude: prefix with `/mobile-icon-system`

Prompts are written in English, but the skill is bilingual — you can translate or rewrite any prompt in your language and the skill will reply accordingly.

## 1. Tab Bar Refresh — Brand-Coherent

Refresh existing Tab Bar to inherit brand DNA from the project's logo.

```text
Refresh our Tab Bar icons (5 destinations: Home, Search, Library, Profile,
Settings) to match the brand DNA in our logo. Currently we use a mix of
Material outlined icons and three custom icons — inconsistent stroke
weight and metaphor coherence is poor.

Do the following:
1. Audit the current Tab Bar set and document what's wrong (stroke
   inconsistency, mixed metaphors, state pair gaps).
2. Extract Brand DNA from brand/primary-symbol.svg. Confirm extraction
   with me before proceeding.
3. Propose icon system rules: grid, stroke weight + diagonal compensation,
   terminals, corners, state pairing. Halt at the mandatory user-selection
   gate and ask me to confirm.
4. After I confirm, generate the full set in one batch (filled + outlined
   variants for all 5).
5. Run cross-icon consistency audit and surface any drift.
6. Score the set on the 8-dimension matrix.
7. Validate in iOS Tab Bar (light + dark) and Android Bottom Nav (light +
   dark) contexts.
8. Identify the 3 highest-priority improvement moves.
```

## 2. Full Icon Set From Scratch

Greenfield project, no existing icon set. Brand has color and type but no icons yet.

```text
We are building a new health app. The brand identity has colors and
typography defined but no icon system. We need:
- 5 Tab Bar icons (Home, Search, Library, Profile, Activity)
- 4 action icons (Add, Share, Edit, Delete)
- 3 navigation icons (Back, Menu, Close)

Brand feels precise and warm — medical credibility without clinical
coldness.

Do the following:
1. Ask me for Brand DNA inputs since no logo exists in the project.
2. Run a creative divergence pass — propose 3 distinct icon system rule
   sets (e.g., "calm precision", "friendly weight", "editorial sharp").
3. Each rule set must be applicable to the full vocabulary; show one icon
   (Home) under each set so I can choose.
4. Halt at the mandatory user-selection gate and ask me to choose a rule
   set. Do not proceed to vocabulary or generation.
5. After I choose, define the vocabulary table for all 12 icons.
6. Generate the set in one batch (Tab Bar gets filled + outlined; action
   and nav can be single state).
7. Run consistency audit, evaluation, and Tab Bar validation.
8. Output the production package via init_icon_system_package.py.
```

## 3. Single Icon Addition To Existing System

```text
Our existing icon system is documented in icon-system/system-rules.md.
We need to add one icon: Notifications. It will live in the Tab Bar as
a 6th destination.

Do the following:
1. Read the existing icon-system rules. Confirm: 24×24 grid, 1.75pt
   stroke, round terminals, R=2 corners, filled+outlined states.
2. Propose a metaphor and form for Notifications. Reference icon-vocabulary.md
   for cliché map (avoid bell with ringing lines).
3. Generate filled + outlined variants matching the existing system.
4. Run cross-icon consistency check against the existing 5 icons (do not
   audit the existing 5 — only verify the new icon fits).
5. Validate in iOS Tab Bar with all 6 icons + labels.
6. Output the new SVG masters and naming.
```

## 4. Icon Set Audit (No Redesign)

```text
Audit our current Tab Bar icon set and tell me if it is ship-ready.
Do not redesign — just evaluate.

Check:
1. Inspect the existing 5 SVGs in src/assets/icons/tabs/
2. Check stroke weight consistency, terminal style, corner radius logic,
   state pair coherence.
3. Test legibility at 20pt and 16pt.
4. Compare metaphors against icon-vocabulary.md cliché map.
5. Place against our logo at brand/primary-symbol.svg — does the set feel
   like the same family?
6. Validate in iOS Tab Bar and Android Bottom Nav.
7. Output a prioritized punch list ordered by ship-risk.
8. Recommend which issues are blocking and which can be follow-ups.

Do not propose redesigns unless something is fundamentally broken.
```

## 5. Brand-Coherent Monochrome With Material You

```text
Android-first utility app. We need 5 Bottom Nav icons that work great
under Material You themed icon support. Brand identity must show through
under aggressive system tinting.

Priority order:
1. Establish Brand DNA from our logo (brand/primary-symbol.svg).
2. Propose icon system rules optimized for monochrome silhouette
   identity. Halt at the mandatory user-selection gate.
3. After I confirm, generate the set as monochrome silhouettes
   (filled active + outlined inactive).
4. Run cross-icon consistency audit.
5. Validate under 5 Material You dynamic palettes (warm red, cool blue,
   neutral gray, earth green, vibrant purple).
6. Validate under light + dark themes.
7. Confirm: each icon's identity survives system tinting in all
   palettes.
8. Output Android vector drawables with proper theme attribute tinting.
```

## 6. iOS Premium With Liquid Glass Support

```text
Premium iOS productivity app. iOS 26 Liquid Glass renders Tab Bar with
translucent material that distorts what's behind it. Our icons must work
behind glass distortion.

Premium positioning is mandatory: quiet luxury, restrained construction.

Workflow:
1. Run live research on Liquid Glass Tab Bar specs (size, tinting,
   distortion behavior).
2. Extract Brand DNA from our logo (brand/primary-symbol.svg).
3. Propose icon system rules with Liquid Glass in mind: stronger
   silhouettes, slightly bolder stroke if needed for backdrop visibility.
   Halt at the gate.
4. Generate filled + outlined variants.
5. Cross-icon consistency audit.
6. Hi-end craft pass: per-icon optical correction, anchor reduction,
   tangent G2 continuity.
7. Validate in three contexts:
   - Standard iOS Tab Bar (light + dark)
   - Liquid Glass over photo wallpaper
   - Liquid Glass over high-contrast app content
8. Output the package with iOS PDF template images and explicit Liquid
   Glass usage notes.
```

## 7. Cross-Platform Set With Single Source

```text
We ship on iOS, Android, and React Native admin tool. Need one icon set
that respects all three with a single SVG master source.

Do the following:
1. Audit existing icons across all three platforms; document
   inconsistencies.
2. Establish Brand DNA from brand/primary-symbol.svg.
3. Propose icon system rules. Halt at the gate.
4. Generate the set on a 24×24 grid SVG master.
5. Cross-icon consistency audit.
6. Output platform-specific exports:
   - iOS: PDF template images for asset catalog
   - Android: vector drawable XML with theme tint
   - React Native: SVG component with size/color props
7. Document any platform-specific deviations (size adjustments, etc.)
   in the package.
8. Validate in all three platforms' canonical UI surfaces.
```

## 8. Equity-Preserving Refresh

```text
Our app icons are 4 years old. Users recognize them. We want to refresh
construction quality (stroke weight, corner radius, optical corrections)
without changing silhouettes — existing users must still find their app.

Critical constraint: silhouettes must remain recognizable. The refresh is
evolutionary, not a reset.

Steps:
1. Audit the current set (src/assets/icons/tabs/). Document each icon's
   silhouette as the equity that must survive.
2. Extract Brand DNA from the current logo (assume logo also recently
   updated).
3. Propose new icon system rules: 1.75pt stroke (was 1.5pt), R=2 corners
   (were R=0), round terminals (were square), diagonal compensation (was
   none).
4. Halt at the mandatory user-selection gate.
5. After I confirm, generate evolutionary refresh: each icon preserves
   its outer silhouette but adopts new construction language.
6. Add a "recognizability preservation" criterion to the evaluation:
   would an existing user find this icon after the update?
7. Validate in side-by-side context: old icon + new icon at the same size,
   verify the transition feels like the same brand evolved.
8. Package with old/new comparison notes in rationale.
```

## Pattern Reference

| Prompt # | Mode | Tier | Scope |
|---|---|---|---|
| 1 | Tab Bar refresh | Standard | 5 icons, 2 platforms |
| 2 | Full set greenfield | Hi-end | 12 icons, multi-context |
| 3 | Single icon | Standard | 1 icon |
| 4 | Audit only | Standard | evaluation only |
| 5 | Material You | Hi-end | Android-first, themed |
| 6 | iOS premium | Hi-end | Liquid Glass |
| 7 | Cross-platform | Hi-end | iOS + Android + RN |
| 8 | Equity refresh | Standard | evolutionary, equity-preserving |

Pick the prompt that matches your scenario. Edit freely; the structure is more important than the specific words.
