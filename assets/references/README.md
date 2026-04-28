# Reference corpus

This directory holds the **calibration corpus** for the `mobile-icon-system`
skill. It is read by the LLM (Claude / Codex) at two points in the workflow:

- **Phase 7 — variant generation:** the model compares each candidate icon
  against tier-A exemplars to pick stronger primitives.
- **Phase 9 — hi-end craft pass:** the model audits each shipped icon against
  every applicable tier-A reference and explains, in writing, why the icon
  meets or fails each craft trait noted in the reference's `.notes.md`.

The corpus is sized deliberately. As of v0.4 it is roughly 117 SVGs covering
44 metaphors, 9 explicit state pairs, 6 native-small (16/20pt) exemplars,
and 5 duotone exemplars — enough to anchor every tier-A craft trait the
skill names without diluting the signal.

## What's covered (v0.4)

- **44 metaphors** at tier-A — all Tab Bar destinations, all common actions,
  all status indicators, and the corpus's first text-formatting and
  security-family entries.
- **9 explicit state pairs** — outlined/filled (heart, home, star, bookmark),
  on/off (lock, eye, mic, cloud), and direction-mirror (chevron, sort,
  reply/forward, refresh-cw/ccw, download/upload).
- **6 native-small exemplars** — 5 mini at 16pt + 1 micro at 20pt — for
  calibrating fill-only construction at native deployment sizes.
- **5 duotone exemplars** — bell, heart, gear, house, camera — calibrating
  the mass-layer-plus-outline construction with `currentColor`-bound
  styling.
- **Tier-B distributed across 4 libraries** (Heroicons, Tabler, Phosphor,
  Lucide) so the LLM sees competent-but-flawed examples from a
  cross-section of the ecosystem.

## Additive custom coverage (v0.6)

The [`custom-v06/`](custom-v06/) directory adds compact original calibration
anchors for style and motion cases that are not represented by the
upstream-fetched SVG corpus. These files are **not upstream-fetched material**:
they are repo-authored MIT-licensed assets with sibling `.notes.md` files that
document structure observations, generator lessons, and provenance.

The v0.6 additive set currently covers:

- pixel-art small-size construction (`pixel-bolt-16.svg`);
- 3D/isometric planar construction (`isometric-cube-24.svg`);
- deterministic hand-drawn path jitter (`jitter-pencil-24.svg`, seed
  `v06-jitter-pencil-24-seed-137`);
- a motion/static reduced-motion fallback pair (`motion-pulse.json` and
  `motion-pulse-static.svg`).

## Tier definitions

| Tier | Meaning | What the LLM does with it |
|---|---|---|
| **A — Exemplar** | Industry-standard craft. Specific, named, auditable choices in the path data. | Compare-and-emulate. The LLM lifts construction principles, never copies pixels. |
| **B — Competent** | Reads correctly, but is missing one specific tier-A craft trait (named in the `.notes.md`). | Diagnostic — the LLM sees what "almost-but-not-quite" looks like at the path-data level. |
| **C — Anti-example** | Demonstrates a specific failure mode (over-detail, gendered figure, color-only state, blob-at-20pt). | The LLM learns to **avoid** the pattern. Read [`tier-c/README.md`](tier-c/README.md) before opening the files. |

## How to use the corpus

Each SVG ships with a sibling `<icon-name>.notes.md` that contains:

- **Path data summary** — element count, anchor count, stroke width, viewBox.
- **Why this tier** — verbatim path-data observations from the research phase.
  These are the LLM's calibration signal; they are not paraphrased and not
  shortened.
- **What a generator should learn** (tier A) / **What's missing vs tier-A**
  (tier B) / **Failure mode** + **Why the LLM must NOT replicate this** (tier C).
- **Cross-reference** — the matching section in
  [`references/icon-vocabulary.md`](../../references/icon-vocabulary.md) and the
  numbered aesthetic principles from
  [`references/aesthetic-principles.md`](../../references/aesthetic-principles.md).

The LLM is instructed to read the `.notes.md` first, then open the SVG with
that observation in mind, then compare its own draft against the SVG and the
notes simultaneously.

## How to refresh the corpus

```sh
python3 scripts/fetch_references.py            # fetch any missing files
python3 scripts/fetch_references.py --update   # force re-fetch all (refresh)
python3 scripts/fetch_references.py --dry-run  # preview without writing
python3 scripts/fetch_references.py --verify   # verify SHA256 of every file
```

Pure stdlib, no third-party dependencies, Python 3.8+. The script writes
[`manifest.json`](manifest.json) with one entry per fetched file:

```json
{
  "url": "...",
  "license": "ISC | MIT | Apache-2.0",
  "source": "Lucide | Phosphor | Tabler Icons | Heroicons | Material Symbols",
  "sha256": "...",
  "bytes": 1234,
  "fetched_at": "2026-04-27T..."
}
```

Custom files (the three hand-crafted tier-C anti-examples) are listed under
`custom_files` in the same manifest and are not fetched — they live in this
repo only.

## License

- All upstream SVGs are MIT, ISC, or Apache-2.0 — see
  [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md) for per-source attribution and links to
  the upstream LICENSE files.
- The six hand-crafted tier-C SVGs (`home-overdetailed.svg`,
  `user-gendered.svg`, `notification-color-state.svg`,
  `fingerprint-9loops.svg`, `credit-card-branded.svg`,
  `duotone-color-only.svg`) are MIT-licensed under this repo's
  [`LICENSE`](../../LICENSE).
- The v0.6 `custom-v06/` SVG and JSON anchors are original repo-authored
  calibration assets, MIT-licensed under this repo's [`LICENSE`](../../LICENSE),
  and are not fetched from upstream icon libraries.
- Notes files (`*.notes.md`), `manifest.json`, `README.md`, `ATTRIBUTIONS.md`,
  and `tier-c/README.md` are MIT-licensed under this repo.

## Honest limitations

The v0.4 corpus closed many gaps that v0.3 carried, and v0.6 adds a small
custom set for style/motion calibration, but the corpus is still deliberately
scoped. Future expansion should still address:

1. **Pause / Stop / Skip media controls** — only `play.svg` is calibrated
   today; the rest of the transport family is missing.
2. **Volume + Mute state pair** — neither is in the corpus.
3. **Cast / AirPlay / Picture-in-Picture** — no exemplars.
4. **Map / Compass / Navigation arrow** (turn-by-turn) — only `map-pin.svg`
   covers location, and even that is the static pin, not the live arrow.
5. **Accessibility / Help / Info / Theme** — these are essential utility
   metaphors with no calibration anchor yet.
6. **Trending / Live / Record** — content-state indicators not represented.
7. **Group / Community / Follow / Block** — the single-person `user.svg`
   does not generalize, and LLMs default to gendered clusters when asked
   for multi-person silhouettes (see `tier-c/user-gendered.svg`). Needs
   distinct anchors.
8. **Cart-vs-Bag-vs-Wallet trio** finished — tag/discount, receipt, and gift
   would complete the commerce family.
9. **Archive / File-type variants** (PDF, IMG) — `file.svg` and `folder.svg`
   are present but the variants are not.
10. **Tier-C coverage gaps** — the v0.4 corpus added brand-coupled and
    color-only-duotone failure modes; trend-of-the-week styling, color
    compensating for weak silhouette, drift between corner radii, and
    family-level inconsistency are still under-anchored.
11. **Multi-library tier-A picks for the same metaphor** — second tier-A
    from a different library for Home, Search, Settings, Heart, Bell, and
    Calendar would let the LLM see "two correct ways to do this."
12. **Material Symbols Outlined and Carbon at tier-A** — both libraries
    appear only at tier-C in v0.4.
13. **Platform-native references** — still excluded by license. SF Symbols
    cannot be redistributed; the skill refers the user to
    `references/platform-icon-specs.md` for native deployment.
14. **Native large-size exemplars** — 32pt or 40pt canvas references are
    absent (mini-16, micro-20, and standard-24 are the three sizes covered).
15. **Broader animated state transitions** — v0.6 adds one motion/static
    fallback anchor, but a fuller `tier-d-motion/` corpus for multiple
    interaction patterns is still not created.

The corpus reaches the **size-of-corpus diminishing-returns boundary at
~80 SVGs** (we sit at ~117 entries today, with most over the threshold being
state-pair siblings and tier-B examples for craft contrast). Future expansion
should be additive in *kind* (filling named gaps), not in *count*.

To extend the corpus, fork, add the SVG + `.notes.md`, re-run
`fetch_references.py --update`, and submit a PR including the calibration
observation in the same path-data style as the existing notes.
