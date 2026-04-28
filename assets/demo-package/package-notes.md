# Package Notes - Tidepool Tasks

This package is a compact demo, not a complete client delivery. It exists to prove the repository workflow can carry a small icon system from Brand DNA through rules, vocabulary, selected masters, and review evidence.

## What Is Production-Ready

- SVG masters are valid XML and use a shared 24 by 24 grid.
- Masters are monochrome and tintable with `currentColor`.
- Naming follows the package convention.
- Navigation state distinction is shape-based.

## What Is Deliberately Omitted

- iOS PDF template image exports.
- Android vector drawable XML exports.
- Lottie or dotLottie motion deliverables.
- Full 40 to 80 icon vocabulary.

## Suggested Verification

Run the demo smoke test:

```bash
python3 scripts/smoke_test_demo_package.py
```

The test checks file presence, placeholder cleanup, XML parsing, external-reference hygiene, and contact-sheet rendering.
