# chat

**Tier:** A
**Source:** Lucide outline (`message-circle.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/message-circle.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>`)
- Total anchor points: ~6 path-command anchors
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
(1) Single path implementing a circular bubble + tail in one continuous stroke. The tail is geometrically continuous with the bubble — same path, same fill rule. (2) Tail "drop" lands at `(2, 22)` corner, pointing diagonally down-left — natural reading position for a left-anchored speech metaphor. (3) No `…` ellipsis inside (cliché-free).

## What a generator should learn
A speech bubble is one continuous path. The tail flows OUT of the bubble's edge as part of the same `<path>` element, never as a separate triangle.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Messages / Chat
- Aesthetic principles applied: 1 (restraint — single path), 5 (one-ornament rule — the tail is the signature deviation), 9 (metaphor before ornament — no ellipsis)
