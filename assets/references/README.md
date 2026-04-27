# Reference corpus

This directory holds the **calibration corpus** for the `mobile-icon-system`
skill. It is read by the LLM (Claude / Codex) at two points in the workflow:

- **Phase 7 — variant generation:** the model compares each candidate icon
  against tier-A exemplars to pick stronger primitives.
- **Phase 9 — hi-end craft pass:** the model audits each shipped icon against
  every applicable tier-A reference and explains, in writing, why the icon
  meets or fails each craft trait noted in the reference's `.notes.md`.

The corpus is small on purpose. Twenty-six SVGs are enough to anchor every
tier-A craft trait the skill names; more would dilute the signal.

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
- The three hand-crafted tier-C SVGs (`home-overdetailed.svg`,
  `user-gendered.svg`, `notification-color-state.svg`) are MIT-licensed under
  this repo's [`LICENSE`](../../LICENSE).
- Notes files (`*.notes.md`), `manifest.json`, `README.md`, `ATTRIBUTIONS.md`,
  and `tier-c/README.md` are MIT-licensed under this repo.

## Honest limitations

The corpus is deliberately scoped — it does not yet cover every gap:

- **Coverage is partial.** 16 tier-A icons cannot represent the full ~50–80
  icon set a typical app needs. The corpus prioritizes the most common
  metaphors (tab bar + actions + a few status); rare metaphors (cast,
  picture-in-picture, equalizer, etc.) have no calibration reference yet.
- **One library per metaphor for tier B.** Heroicons supplies most tier-B
  references; Material Symbols and Carbon are not yet represented at tier B.
- **Tier C is not exhaustive.** Five anti-examples cover four named failure
  modes (over-detail, gendered, color-only state, blob-at-20pt). There are
  more (e.g., trend-of-the-week styling, color compensating for weak
  silhouette, drift between corner radii across a set) that the LLM is told
  about in `aesthetic-principles.md` but cannot calibrate against here.
- **Filled / duotone variants are sparse.** Two filled exemplars (heart, home)
  and zero duotone references. Sets shipping in those styles will rely on the
  outline references plus the rules in `references/`.
- **No platform-native references.** SF Symbols and Material Symbols Outlined
  ship with the OS rather than as standalone open files; SF Symbols
  specifically cannot be redistributed under our license. The skill calibrates
  craft from the open-license sources above and refers the user to platform
  references via `references/platform-icon-specs.md` for native deployment.

These gaps are tracked. To extend the corpus, fork, add the SVG + `.notes.md`,
re-run `fetch_references.py --update`, and submit a PR including the
calibration observation in the same path-data style as the existing notes.
