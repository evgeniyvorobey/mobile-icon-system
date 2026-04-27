# user

**Tier:** A
**Source:** Lucide outline (`user.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/user.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` shoulders + `<circle>` head)
- Total anchor points: ~10 (~6 on the shoulder path, 4 implicit on the head circle)
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
(1) Two primitives: head `<circle cx="12" cy="7" r="4"/>` + shoulders `<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>`. (2) Head radius 4 + shoulder height 6 (from y=15 to y=21) gives a 4:6 head-to-torso visual ratio — childlike-not-realistic, which is the safe abstraction for cross-cultural avatars (no perceived gender). (3) Shoulder corners use `a4 4` arcs — exactly matching the head radius, a Brand DNA move that makes the figure feel made of one geometric alphabet.

## What a generator should learn
Person = circle (head) + arched rectangle (shoulders). Shoulder corner radius = head radius. No torso, no neck, no face features.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Profile / Account / Me
- Aesthetic principles applied: 1 (restraint), 8 (family resemblance — shoulder arc radius = head radius), 9 (metaphor before ornament — no facial features)
