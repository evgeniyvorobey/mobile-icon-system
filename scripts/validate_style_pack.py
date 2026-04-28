#!/usr/bin/env python3
"""Validate mobile-icon-system .style-pack manifests."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z][0-9A-Za-z.-]*)?$")
STATUS_VALUES = {"shipped", "deferred", "experimental"}
MANIFEST_SUFFIXES = (".style-pack", ".style-pack.json")

REQUIRED_TOP_LEVEL = [
    "id",
    "name",
    "version",
    "status",
    "category",
    "compatibility",
    "brandDnaConstraints",
    "constructionRules",
    "accessibility",
    "validation",
    "prompts",
    "artifactExpectations",
]

REQUIRED_OBJECT_SECTIONS = [
    "compatibility",
    "brandDnaConstraints",
    "constructionRules",
    "accessibility",
    "validation",
    "prompts",
    "artifactExpectations",
]


def usage() -> str:
    return (
        "Usage: python3 scripts/validate_style_pack.py "
        "<manifest.style-pack|directory> [...]"
    )


def is_manifest_file(path: Path) -> bool:
    return path.is_file() and any(path.name.endswith(suffix) for suffix in MANIFEST_SUFFIXES)


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def discover_manifests(paths: list[Path]) -> tuple[list[Path], list[tuple[Path, str]]]:
    manifests: list[Path] = []
    discovery_errors: list[tuple[Path, str]] = []

    for path in paths:
        if not path.exists():
            discovery_errors.append((path, "path does not exist"))
            continue

        if path.is_file():
            manifests.append(path)
            continue

        if not path.is_dir():
            discovery_errors.append((path, "path is neither a file nor a directory"))
            continue

        found = sorted(child for child in path.rglob("*") if is_manifest_file(child))
        if not found:
            discovery_errors.append((path, "no .style-pack manifests found"))
            continue
        manifests.extend(found)

    unique_manifests = sorted(set(manifests))
    return unique_manifests, discovery_errors


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def non_empty_object(value: Any) -> bool:
    return isinstance(value, dict) and len(value) > 0


def list_entries_are_present(value: Any) -> bool:
    if not non_empty_list(value):
        return False
    for item in value:
        if isinstance(item, str) and item.strip():
            continue
        if isinstance(item, dict) and item:
            continue
        return False
    return True


def validate_manifest_data(data: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["manifest root must be a JSON object"]

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"missing required top-level key: {key}")

    for key in REQUIRED_OBJECT_SECTIONS:
        if key in data and not non_empty_object(data[key]):
            errors.append(f"{key} must be a nonempty object")

    style_id = data.get("id")
    if "id" in data:
        if not non_empty_string(style_id):
            errors.append("id must be a nonempty string")
        elif not ID_RE.match(style_id):
            errors.append(
                "id must match ^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$"
            )

    name = data.get("name")
    if "name" in data and not non_empty_string(name):
        errors.append("name must be a nonempty string")

    version = data.get("version")
    if "version" in data:
        if not non_empty_string(version):
            errors.append("version must be a nonempty string")
        elif not VERSION_RE.match(version):
            errors.append("version must be semver-ish, for example 1.0.0")

    status = data.get("status")
    if "status" in data:
        if not non_empty_string(status):
            errors.append("status must be a nonempty string")
        elif status not in STATUS_VALUES:
            allowed = ", ".join(sorted(STATUS_VALUES))
            errors.append(f"status must be one of: {allowed}")

    category = data.get("category")
    if "category" in data and not non_empty_string(category):
        errors.append("category must be a nonempty string")

    brand_dna = data.get("brandDnaConstraints")
    if isinstance(brand_dna, dict):
        refuse_if = brand_dna.get("refuseIf")
        if not list_entries_are_present(refuse_if):
            errors.append("brandDnaConstraints.refuseIf must be a nonempty list")

    validation = data.get("validation")
    if isinstance(validation, dict):
        checks = validation.get("checks")
        if not list_entries_are_present(checks):
            errors.append("validation.checks must be a nonempty list")

    prompts = data.get("prompts")
    if isinstance(prompts, dict):
        examples = prompts.get("examples")
        if not list_entries_are_present(examples):
            errors.append("prompts.examples must be a nonempty list")

    return errors


def validate_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"could not read file: {exc}"]

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]

    return validate_manifest_data(data)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv

    if not args:
        print(usage(), file=sys.stderr)
        return 1

    if args == ["-h"] or args == ["--help"]:
        print(usage())
        return 0

    manifests, discovery_errors = discover_manifests([Path(arg) for arg in args])
    all_errors: list[tuple[Path, list[str]]] = [
        (path, [message]) for path, message in discovery_errors
    ]

    for manifest in manifests:
        errors = validate_file(manifest)
        if errors:
            all_errors.append((manifest, errors))

    if all_errors:
        print("[FAIL] Style-pack validation failed.", file=sys.stderr)
        for path, errors in all_errors:
            print(f"{display_path(path)}:", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"[OK] {len(manifests)} style-pack manifest(s) valid.")
    for manifest in manifests:
        print(f"  - {display_path(manifest)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
