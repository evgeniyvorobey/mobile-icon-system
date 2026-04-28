#!/usr/bin/env python3
"""Build a discovery registry for built-in and plugin style packs."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "assets" / "style-pack-registry" / "registry.json"

REGISTRY_SCHEMA_VERSION = "1.0.0"

BUILTIN_PACKS: list[dict[str, Any]] = [
    {
        "id": "duotone-chromatic",
        "name": "Chromatic Duotone",
        "path": "references/style-packs/duotone-chromatic.md",
        "status": "shipped",
        "categories": ["duotone"],
        "tags": ["two-color", "brand-tokens", "svg", "flat-fill"],
        "refuseIfFallback": "the brand has only one color in its palette",
    },
    {
        "id": "liquid-glass",
        "name": "Liquid Glass",
        "path": "references/style-packs/liquid-glass.md",
        "status": "shipped",
        "categories": ["material"],
        "tags": ["ios", "gradient", "launcher", "platform-native"],
        "refuseIfFallback": "brand is anti-gradient by declaration",
    },
    {
        "id": "claymorphism",
        "name": "Claymorphism",
        "path": "references/style-packs/claymorphism.md",
        "status": "shipped",
        "categories": ["tactile"],
        "tags": ["pastel", "rounded", "shadow", "svg-filter"],
        "refuseIfFallback": "brand demands sharp corners or stroked icons",
    },
    {
        "id": "3d-isometric",
        "name": "3D / Isometric",
        "path": "references/style-packs/3d-isometric.md",
        "status": "shipped",
        "categories": ["dimensional"],
        "tags": ["axonometric", "flat-fills", "depth", "small-size-fallback"],
        "refuseIfFallback": (
            "Brand DNA requires stroke-only icons, flat monochrome template "
            "tinting, no decorative depth, or primary 16pt output without fallback"
        ),
    },
    {
        "id": "pixel-art",
        "name": "Pixel Art",
        "path": "references/style-packs/pixel-art.md",
        "status": "shipped",
        "categories": ["bitmap"],
        "tags": ["pixel-grid", "nearest-neighbor", "binary-alpha", "small-size"],
        "refuseIfFallback": (
            "Brand DNA requires smooth curves, gradients, antialiased vector "
            "edges, or a pipeline that cannot preserve nearest-neighbor output"
        ),
    },
    {
        "id": "hand-drawn",
        "name": "Hand-Drawn",
        "path": "references/style-packs/hand-drawn.md",
        "status": "shipped",
        "categories": ["organic"],
        "tags": ["seeded-jitter", "vector", "expressive", "reproducible"],
        "refuseIfFallback": (
            "Brand DNA requires strict geometry, exact platform-symbol matching, "
            "or build steps that regenerate jitter on every export"
        ),
    },
]


class RegistryError(RuntimeError):
    """Raised when registry inputs cannot be indexed safely."""


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip(" -\n\t")


def repo_relative(path: Path) -> str:
    resolved = path.resolve()
    for root in (ROOT.resolve(), Path.cwd().resolve()):
        try:
            return resolved.relative_to(root).as_posix()
        except ValueError:
            continue
    return str(resolved)


def unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        cleaned = clean_text(value)
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)
    return result


def normalize_string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if not isinstance(value, list):
        return []
    strings: list[str] = []
    for item in value:
        if isinstance(item, str):
            strings.append(item)
    return unique_strings(strings)


def extract_markdown_title(path: Path) -> str | None:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return clean_text(line[2:])
    return None


def extract_refuse_if_summary(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")

    inline_match = re.search(
        r"\*\*Refuse if:\*\*\s*(?P<body>.*?)(?:\n\n|^##\s|\Z)",
        text,
        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    if inline_match:
        return clean_text(inline_match.group("body"))

    section_match = re.search(
        r"^## Refuse if\s*\n(?P<body>.*?)(?=^##\s|\Z)",
        text,
        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    if section_match:
        return clean_text(section_match.group("body"))

    return None


def load_validator_module() -> Any:
    scripts_dir = str(ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    try:
        import validate_style_pack  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RegistryError(
            f"could not import existing style-pack validator: {exc}"
        ) from exc
    return validate_style_pack


def discover_valid_plugin_manifests(plugin_paths: list[Path]) -> list[Path]:
    if not plugin_paths:
        return []

    validator = load_validator_module()
    manifests, discovery_errors = validator.discover_manifests(plugin_paths)
    validation_errors: list[tuple[Path, list[str]]] = [
        (path, [message]) for path, message in discovery_errors
    ]

    for manifest in manifests:
        errors = validator.validate_file(manifest)
        if errors:
            validation_errors.append((manifest, errors))

    if validation_errors:
        lines = ["style-pack plugin validation failed:"]
        for path, errors in validation_errors:
            lines.append(f"  {repo_relative(path)}:")
            for error in errors:
                lines.append(f"    - {error}")
        raise RegistryError("\n".join(lines))

    return manifests


def summarize_refuse_if(refuse_if: Any) -> tuple[str, list[str]]:
    if not isinstance(refuse_if, list):
        return "", []

    items: list[str] = []
    for item in refuse_if:
        if isinstance(item, str):
            items.append(clean_text(item))
            continue
        if isinstance(item, dict):
            for key in ("summary", "description", "reason", "if"):
                value = item.get(key)
                if isinstance(value, str) and value.strip():
                    items.append(clean_text(value))
                    break
            else:
                items.append(json.dumps(item, sort_keys=True))

    items = unique_strings(items)
    return "; ".join(items), items


def built_in_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    for spec in BUILTIN_PACKS:
        path = ROOT / spec["path"]
        if not path.exists():
            raise RegistryError(f"missing built-in style-pack reference: {spec['path']}")

        summary = extract_refuse_if_summary(path) or spec["refuseIfFallback"]
        entries.append(
            {
                "id": spec["id"],
                "name": extract_markdown_title(path) or spec["name"],
                "status": spec["status"],
                "sourceType": "builtin",
                "path": spec["path"],
                "categories": list(spec["categories"]),
                "tags": list(spec["tags"]),
                "refuseIf": {
                    "summary": summary,
                    "items": [summary],
                },
            }
        )

    return entries


def plugin_entry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}

    categories = normalize_string_list(data.get("categories"))
    category = data.get("category")
    if isinstance(category, str):
        categories = unique_strings([category, *categories])

    tags = normalize_string_list(data.get("tags"))
    tags = unique_strings([*tags, *normalize_string_list(metadata.get("tags"))])

    refuse_summary, refuse_items = summarize_refuse_if(
        data.get("brandDnaConstraints", {}).get("refuseIf")
    )

    return {
        "id": data["id"],
        "name": data["name"],
        "status": data["status"],
        "sourceType": "plugin",
        "path": repo_relative(path),
        "version": data["version"],
        "categories": categories,
        "tags": tags,
        "refuseIf": {
            "summary": refuse_summary,
            "items": refuse_items,
        },
    }


def plugin_entries(plugin_paths: list[Path]) -> list[dict[str, Any]]:
    manifests = discover_valid_plugin_manifests(plugin_paths)
    return [plugin_entry(path) for path in manifests]


def duplicate_id_map(entries: list[dict[str, Any]]) -> dict[str, list[str]]:
    by_id: dict[str, list[str]] = {}
    for entry in entries:
        by_id.setdefault(entry["id"], []).append(
            f"{entry['sourceType']}:{entry['path']}"
        )
    return {style_id: paths for style_id, paths in by_id.items() if len(paths) > 1}


def build_registry(plugin_paths: list[Path], allow_duplicates: bool) -> dict[str, Any]:
    entries = [*built_in_entries(), *plugin_entries(plugin_paths)]
    entries.sort(key=lambda entry: (entry["sourceType"], entry["id"], entry["path"]))

    duplicates = duplicate_id_map(entries)
    if duplicates and not allow_duplicates:
        lines = ["duplicate style-pack IDs found:"]
        for style_id in sorted(duplicates):
            lines.append(f"  {style_id}:")
            for source in duplicates[style_id]:
                lines.append(f"    - {source}")
        lines.append("rerun with --allow-duplicates only for inspection output")
        raise RegistryError("\n".join(lines))

    return {
        "schemaVersion": REGISTRY_SCHEMA_VERSION,
        "generatedBy": "scripts/build_style_pack_registry.py",
        "purpose": (
            "Discovery index for built-in Markdown style packs and validated "
            "plugin manifests. This is not a runtime loader."
        ),
        "phaseGate": {
            "phase": "Phase 5",
            "summary": (
                "Registry entries do not authorize automatic application. Brand DNA "
                "conflicts, accessibility implications, and user confirmation still "
                "gate every non-default style."
            ),
        },
        "entryCount": len(entries),
        "entries": entries,
        "duplicateIds": duplicates,
    }


def write_registry(registry: dict[str, Any], output: Path | None) -> None:
    text = json.dumps(registry, indent=2) + "\n"
    if output is None:
        print(text, end="")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(f"[OK] Wrote {repo_relative(output)} ({registry['entryCount']} entries)")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the mobile-icon-system style-pack discovery registry."
    )
    parser.add_argument(
        "plugin_paths",
        nargs="*",
        help="Optional .style-pack files or directories to index recursively.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Registry JSON output path. Use '-' to write to stdout.",
    )
    parser.add_argument(
        "--allow-duplicates",
        action="store_true",
        help="Allow duplicate IDs and record them in duplicateIds.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    plugin_paths = [Path(path) for path in args.plugin_paths]
    output = None if args.output == "-" else Path(args.output)

    try:
        registry = build_registry(
            plugin_paths=plugin_paths,
            allow_duplicates=args.allow_duplicates,
        )
        write_registry(registry, output)
    except RegistryError as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
