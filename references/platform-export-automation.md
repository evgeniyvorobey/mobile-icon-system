# Platform Export Automation

This reference covers the stdlib-only exporter in `scripts/export_platform_assets.py`. It turns path-based SVG masters, plus a narrow set of simple primitives, into Android VectorDrawable XML and scaffolds iOS PDF-backed image sets.

## Source-Backed Constraints

- Android's `VectorDrawable` is an XML vector graphic defined with a `<vector>` element. The official Android API reference defines `android:width` and `android:height` as intrinsic dimensions, normally specified in `dp`, and `android:viewportWidth` / `android:viewportHeight` as the virtual canvas where paths are drawn. It also defines `android:pathData` as the same format as the SVG `d` path data, plus path attributes such as `fillColor`, `strokeColor`, and `strokeWidth`. Source: [Android Developers, VectorDrawable](https://developer.android.com/reference/android/graphics/drawable/VectorDrawable).
- Apple's asset catalog Image Set format supports `.pdf` files and the `properties.preserves-vector-representation` Boolean. Apple's reference states that setting it to `true` preserves vector information for a PDF file. Source: [Apple Asset Catalog Format Reference, Image Set Type](https://developer.apple.com/library/archive/documentation/Xcode/Reference/xcode_ref-Asset_Catalog_Format/ImageSetType.html).

## CLI

```bash
python3 scripts/export_platform_assets.py exports/svg-masters --platform both
```

Defaults:

- Android XML: `exports/android/res/drawable/*.xml`
- iOS catalog: `exports/ios/Assets.xcassets/*.imageset`
- Existing iOS PDFs: `exports/ios/pdf/<same-stem>.pdf`

Useful options:

```bash
python3 scripts/export_platform_assets.py exports/svg-masters \
  --platform android \
  --android-out app/src/main/res/drawable \
  --android-tint "?attr/colorControlNormal"

python3 scripts/export_platform_assets.py exports/svg-masters \
  --platform ios \
  --ios-pdf-dir exports/ios/pdf \
  --ios-xcassets App/Assets.xcassets
```

Use `--platform android`, `--platform ios`, or `--platform both`.

## Android Export

The exporter reads each `.svg` in the master directory and writes one `res/drawable/<resource>.xml` VectorDrawable.

Supported SVG subset:

- Root `<svg>` with numeric `viewBox`.
- One or more `<path>` elements.
- Simple `rect`, `circle`, and `line` primitives, converted to path data when they use unitless coordinates and no transforms.
- `d` copied to `android:pathData`.
- `fill`, `stroke`, `stroke-width`, `stroke-linecap`, `stroke-linejoin`, `stroke-miterlimit`, and `fill-rule` mapped to their Android path equivalents when present.
- `currentColor` converted to `#000000` with a warning; pair with `--android-tint` to preserve template-color behavior.
- Root `width` and `height` converted to `dp`; when omitted, viewBox width and height are used.
- Optional `--android-tint` copied to `android:tint` on the `<vector>`.

Unsupported features fail by default:

- Filters, masks, clip paths, gradients, patterns, text, images, symbols, `use`, and foreign objects.
- Complex non-path primitives such as `ellipse`, `polyline`, and `polygon`.
- SVG transforms on paths or groups.
- Paint servers such as `fill="url(#gradient)"`.
- Rendering-affecting attributes the exporter does not map, including opacity, stroke dashes, display/visibility, and vector effects.

`--ignore-non-path` skips unsupported non-path primitives with a warning, but it does not enable filters, masks, gradients, images, text, or transforms. Flatten complex primitives and effects before production export.

## iOS Export

The exporter scaffolds `.imageset` folders for Xcode asset catalogs. It does not convert SVG to PDF.

For each SVG master, iOS export requires a vector PDF with the same source stem:

```text
exports/svg-masters/home.svg
exports/ios/pdf/home.pdf
```

The output image set copies the PDF and writes:

```json
{
  "images": [
    {
      "idiom": "universal",
      "filename": "home.pdf"
    }
  ],
  "properties": {
    "preserves-vector-representation": true
  },
  "info": {
    "author": "xcode",
    "version": 1
  }
}
```

If the PDF is not ready, pass `--ios-placeholder-manifest` to create `Contents.json` and a `TODO.md` note. This is a scaffold only; the asset is not production-ready until a real vector PDF is added and referenced.

## Verification

Run the smoke test:

```bash
python3 scripts/smoke_test_platform_exports.py
```

It verifies:

- A simple SVG path exports to Android VectorDrawable XML with viewport, dimensions, path data, fill, stroke, stroke width, and tint.
- A matching dummy PDF scaffolds an iOS `.imageset` with `preserves-vector-representation: true`.
- An unsupported SVG feature fails instead of being silently dropped.

## Limitations

- Stdlib-only Python cannot reliably convert SVG to vector PDF. Use a design tool, Xcode workflow, or dedicated vector conversion tool to produce the iOS PDF, then run this exporter to package it.
- The Android converter is intentionally conservative. It does not evaluate CSS, apply transforms, resolve symbols, preserve opacity, or rasterize unsupported effects. Only simple `rect`, `circle`, and `line` primitives are expanded to path data.
- Resource names are sanitized to lowercase Android-safe names. If two masters sanitize to the same name, export fails to avoid overwriting assets.
