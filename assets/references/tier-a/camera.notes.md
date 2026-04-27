# camera

**Tier:** A
**Source:** Phosphor regular (`camera.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/phosphor-icons/core/main/raw/regular/camera.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 3 (1 `<rect>` transparent canvas + 1 `<path>` body+hood + 1 `<circle>` lens)
- Total anchor points: ~22 path-command anchors in the body path; circle lens contributes 4 implicit anchors
- Stroke width: filled style (Phosphor regular weight; ~16-unit stroke at 256-canvas)
- Coordinate system: viewBox 0 0 256 256

## Why this tier
(1) Body + a single `<circle cx="128" cy="132" r="36"/>`. Two elements. (2) Hood uses pure straight lines — no fake bevel detail. The hood is offset from the body by a single connector segment. (3) Lens is below geometric vertical center: `cy=132` not `cy=128`. This is a 4pt downward optical shift compensating for the hood's visual mass at the top.

## What a generator should learn
Camera = body rectangle + hood polyline + lens circle. Lens is shifted down from geometric center to compensate for hood weight.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Camera / Capture
- Aesthetic principles applied: 1 (restraint — three primitives only), 4 (weight perception — lens shifted down 4pt), 9 (metaphor before ornament — no fake bevel)
