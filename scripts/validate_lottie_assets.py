#!/usr/bin/env python3
"""Validate Lottie JSON and dotLottie assets for mobile icon motion."""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


SUPPORTED_SUFFIXES = {".json", ".lottie"}
DOTLOTTIE_ROOTS = {"manifest.json", "a", "i", "t", "s", "f"}
DOTLOTTIE_ID_RE = re.compile(r"^[A-Za-z0-9._ -]{1,256}$")

DEFAULT_MAX_DIMENSION_PX = 2048
DEFAULT_MAX_DURATION_MS = 1500
DEFAULT_MAX_FRAMERATE = 120

ALLOWED_LAYER_TYPES = {0, 1, 3, 4}
LAYER_TYPE_NAMES = {
    0: "precomposition",
    1: "solid",
    2: "image",
    3: "null",
    4: "shape",
    5: "text",
}


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def has_content(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return True


def json_path(parent: str, key: object) -> str:
    if isinstance(key, int):
        return f"{parent}[{key}]"
    key_text = str(key)
    if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key_text):
        return f"{parent}.{key_text}"
    return f"{parent}[{key_text!r}]"


def is_asset_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES


def discover_assets(paths: list[Path]) -> tuple[list[Path], list[tuple[str, str]]]:
    assets: list[Path] = []
    errors: list[tuple[str, str]] = []

    for path in paths:
        label = display_path(path)
        if not path.exists():
            errors.append((label, "path does not exist"))
            continue

        if path.is_file():
            assets.append(path)
            continue

        if not path.is_dir():
            errors.append((label, "path is neither a file nor a directory"))
            continue

        found = sorted(child for child in path.rglob("*") if is_asset_file(child))
        if not found:
            errors.append((label, "no .json or .lottie assets found"))
            continue
        assets.extend(found)

    unique_assets = sorted(set(assets))
    return unique_assets, errors


def read_json_file(path: Path) -> tuple[Any | None, list[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"could not read file: {exc}"]

    try:
        return json.loads(text), []
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]


def validate_lottie_json_file(
    path: Path,
    *,
    max_dimension_px: int,
    max_duration_ms: int,
    max_framerate: int,
) -> list[tuple[str, str]]:
    label = display_path(path)
    data, errors = read_json_file(path)
    if errors:
        return [(label, error) for error in errors]
    return [
        (label, error)
        for error in validate_lottie_data(
            data,
            max_dimension_px=max_dimension_px,
            max_duration_ms=max_duration_ms,
            max_framerate=max_framerate,
        )
    ]


def validate_lottie_data(
    data: Any,
    *,
    max_dimension_px: int,
    max_duration_ms: int,
    max_framerate: int,
) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["Lottie root must be a JSON object"]

    validate_version(data, errors)
    fr = validate_number_field(
        data, "fr", "$.fr", errors, required=True, minimum=0, exclusive_minimum=True
    )
    ip = validate_number_field(data, "ip", "$.ip", errors, required=True)
    op = validate_number_field(data, "op", "$.op", errors, required=True)

    validate_dimension_field(data, "w", "$.w", errors, max_dimension_px, required=True)
    validate_dimension_field(data, "h", "$.h", errors, max_dimension_px, required=True)

    if fr is not None and fr > max_framerate:
        errors.append(f"$.fr exceeds {max_framerate} fps")

    if ip is not None and op is not None:
        if op <= ip:
            errors.append("$.op must be greater than $.ip")
        elif fr is not None:
            duration_ms = ((op - ip) / fr) * 1000
            if duration_ms <= 0:
                errors.append("derived duration must be greater than 0 ms")
            if duration_ms > max_duration_ms:
                errors.append(
                    "derived duration "
                    f"{duration_ms:.0f} ms exceeds {max_duration_ms} ms"
                )

    layers = data.get("layers")
    if "layers" not in data:
        errors.append("missing required top-level field `layers`")
    elif not isinstance(layers, list):
        errors.append("$.layers must be an array")
    elif not layers:
        errors.append("$.layers must not be empty")
    else:
        validate_layers(layers, "$.layers", errors, max_dimension_px)

    validate_assets(data.get("assets"), "$.assets", errors, max_dimension_px)
    validate_font_payloads(data, errors)
    scan_for_unsupported_features(data, "$", errors)
    return errors


def validate_version(data: dict[str, Any], errors: list[str]) -> None:
    has_bodymovin_version = "v" in data
    has_spec_version = "ver" in data
    if not has_bodymovin_version and not has_spec_version:
        errors.append("missing version field (`v` or `ver`)")
        return

    if has_bodymovin_version:
        value = data.get("v")
        if not isinstance(value, str) or not value.strip():
            errors.append("$.v must be a non-empty string when present")

    if has_spec_version:
        value = data.get("ver")
        if isinstance(value, str):
            if not value.strip():
                errors.append("$.ver must be non-empty when present")
        elif not is_number(value):
            errors.append("$.ver must be a number or non-empty string when present")


def validate_number_field(
    obj: dict[str, Any],
    key: str,
    path: str,
    errors: list[str],
    *,
    required: bool,
    minimum: float | None = None,
    exclusive_minimum: bool = False,
) -> float | None:
    if key not in obj:
        if required:
            errors.append(f"missing required top-level field `{key}`")
        return None

    value = obj[key]
    if not is_number(value):
        errors.append(f"{path} must be a number")
        return None

    number = float(value)
    if minimum is not None:
        if exclusive_minimum and number <= minimum:
            errors.append(f"{path} must be greater than {minimum:g}")
        elif not exclusive_minimum and number < minimum:
            errors.append(f"{path} must be at least {minimum:g}")
    return number


def validate_dimension_field(
    obj: dict[str, Any],
    key: str,
    path: str,
    errors: list[str],
    max_dimension_px: int,
    *,
    required: bool,
) -> None:
    if key not in obj:
        if required:
            errors.append(f"missing required top-level field `{key}`")
        return

    value = obj[key]
    if not is_number(value):
        errors.append(f"{path} must be a number")
        return

    if value <= 0:
        errors.append(f"{path} must be greater than 0")
    if value > max_dimension_px:
        errors.append(f"{path} exceeds {max_dimension_px}px")


def validate_layers(
    layers: list[Any],
    path: str,
    errors: list[str],
    max_dimension_px: int,
) -> None:
    for index, layer in enumerate(layers):
        layer_path = json_path(path, index)
        if not isinstance(layer, dict):
            errors.append(f"{layer_path} must be an object")
            continue

        layer_type = layer.get("ty")
        if "ty" not in layer:
            errors.append(f"{layer_path}.ty is required")
        elif not isinstance(layer_type, int) or isinstance(layer_type, bool):
            errors.append(f"{layer_path}.ty must be an integer layer type")
        else:
            layer_name = LAYER_TYPE_NAMES.get(layer_type, "unknown")
            if layer_type == 2:
                errors.append(f"{layer_path} uses image layer type 2")
            elif layer_type == 5:
                errors.append(f"{layer_path} uses text layer type 5")
            elif layer_type not in ALLOWED_LAYER_TYPES:
                errors.append(f"{layer_path} uses unsupported {layer_name} layer type {layer_type}")

            if layer_type == 4:
                shapes = layer.get("shapes")
                if not isinstance(shapes, list) or not shapes:
                    errors.append(f"{layer_path}.shapes must be a non-empty array")

        if has_content(layer.get("ddd")) and layer.get("ddd") not in (0, False):
            errors.append(f"{layer_path}.ddd enables 3D rendering")

        validate_layer_timing(layer, layer_path, errors)
        for dimension_key in ("w", "h", "sw", "sh"):
            validate_dimension_field(
                layer,
                dimension_key,
                json_path(layer_path, dimension_key),
                errors,
                max_dimension_px,
                required=False,
            )


def validate_layer_timing(
    layer: dict[str, Any], layer_path: str, errors: list[str]
) -> None:
    ip_value = layer.get("ip")
    op_value = layer.get("op")

    if "ip" in layer and not is_number(ip_value):
        errors.append(f"{layer_path}.ip must be a number when present")
        ip_value = None
    if "op" in layer and not is_number(op_value):
        errors.append(f"{layer_path}.op must be a number when present")
        op_value = None

    if is_number(ip_value) and is_number(op_value) and op_value <= ip_value:
        errors.append(f"{layer_path}.op must be greater than {layer_path}.ip")


def validate_assets(
    assets: Any,
    path: str,
    errors: list[str],
    max_dimension_px: int,
) -> None:
    if assets is None:
        return

    if not isinstance(assets, list):
        errors.append(f"{path} must be an array when present")
        return

    for index, asset in enumerate(assets):
        asset_path = json_path(path, index)
        if not isinstance(asset, dict):
            errors.append(f"{asset_path} must be an object")
            continue

        if has_content(asset.get("p")) or has_content(asset.get("u")) or asset.get("e") == 1:
            errors.append(f"{asset_path} references image or external asset data")

        for dimension_key in ("w", "h"):
            validate_dimension_field(
                asset,
                dimension_key,
                json_path(asset_path, dimension_key),
                errors,
                max_dimension_px,
                required=False,
            )

        nested_layers = asset.get("layers")
        if nested_layers is not None:
            if isinstance(nested_layers, list) and nested_layers:
                validate_layers(nested_layers, f"{asset_path}.layers", errors, max_dimension_px)
            elif not isinstance(nested_layers, list):
                errors.append(f"{asset_path}.layers must be an array when present")


def validate_font_payloads(data: dict[str, Any], errors: list[str]) -> None:
    if has_content(data.get("fonts")):
        errors.append("$.fonts contains font metadata; convert text to vector shapes")
    if has_content(data.get("chars")):
        errors.append("$.chars contains glyph/font data; convert text to vector shapes")


def scan_for_unsupported_features(node: Any, path: str, errors: list[str]) -> None:
    if isinstance(node, dict):
        expression = node.get("x")
        if isinstance(expression, str) and expression.strip():
            errors.append(f"{json_path(path, 'x')} contains an expression")

        effects = node.get("ef")
        if has_content(effects):
            errors.append(f"{json_path(path, 'ef')} contains After Effects effects")

        for key, value in node.items():
            scan_for_unsupported_features(value, json_path(path, key), errors)
        return

    if isinstance(node, list):
        for index, item in enumerate(node):
            scan_for_unsupported_features(item, json_path(path, index), errors)


def validate_dotlottie_file(
    path: Path,
    *,
    max_dimension_px: int,
    max_duration_ms: int,
    max_framerate: int,
) -> list[tuple[str, str]]:
    label = display_path(path)
    errors: list[tuple[str, str]] = []

    if not zipfile.is_zipfile(path):
        return [(label, "not a valid ZIP archive")]

    try:
        with zipfile.ZipFile(path) as archive:
            names = [info.filename for info in archive.infolist()]
            file_names = {name for name in names if not name.endswith("/")}
            errors.extend((label, error) for error in validate_zip_paths(names))

            duplicate_names = [
                name for name, count in Counter(names).items() if count > 1
            ]
            for name in sorted(duplicate_names):
                errors.append((label, f"duplicate ZIP entry `{name}`"))

            manifest, manifest_errors = read_zip_json(archive, "manifest.json")
            if manifest_errors:
                errors.extend((label, error) for error in manifest_errors)
                return errors

            manifest_errors, animation_ids, theme_ids, state_machine_ids = (
                validate_dotlottie_manifest(manifest, file_names)
            )
            errors.extend((label, error) for error in manifest_errors)

            animation_files = sorted(
                name for name in file_names if is_immediate_json_file(name, "a")
            )
            if not animation_files:
                errors.append((label, "missing animation JSON files under `a/`"))

            for name in animation_files:
                animation_id = PurePosixPath(name).stem
                if animation_ids and animation_id not in animation_ids:
                    errors.append(
                        (label, f"`{name}` is not declared in manifest.animations")
                    )

                animation, animation_errors = read_zip_json(archive, name)
                nested_label = f"{label}!{name}"
                if animation_errors:
                    errors.extend((nested_label, error) for error in animation_errors)
                    continue
                errors.extend(
                    (nested_label, error)
                    for error in validate_lottie_data(
                        animation,
                        max_dimension_px=max_dimension_px,
                        max_duration_ms=max_duration_ms,
                        max_framerate=max_framerate,
                    )
                )

            errors.extend(validate_optional_dotlottie_json_files(archive, file_names, label, "t", theme_ids))
            errors.extend(
                validate_optional_dotlottie_json_files(
                    archive, file_names, label, "s", state_machine_ids
                )
            )
            validate_forbidden_dotlottie_asset_folders(file_names, label, errors)
    except OSError as exc:
        return [(label, f"could not read ZIP archive: {exc}")]
    except zipfile.BadZipFile as exc:
        return [(label, f"invalid ZIP archive: {exc}")]

    return errors


def validate_zip_paths(names: list[str]) -> list[str]:
    errors: list[str] = []
    for name in names:
        if "\\" in name:
            errors.append(f"ZIP entry `{name}` uses backslashes")
            continue

        path = PurePosixPath(name)
        if path.is_absolute():
            errors.append(f"ZIP entry `{name}` must be relative")
            continue

        parts = path.parts
        if not parts or any(part in {"", ".", ".."} for part in parts):
            errors.append(f"ZIP entry `{name}` is not a safe relative path")
            continue

        root = parts[0]
        if root not in DOTLOTTIE_ROOTS:
            errors.append(f"unexpected top-level ZIP entry `{root}`")
            continue

        if root == "manifest.json" and len(parts) != 1:
            errors.append("manifest.json must be at the ZIP root")
        if root in {"a", "t", "s", "f"} and len(parts) > 2:
            errors.append(f"ZIP entry `{name}` is nested too deeply for `{root}/`")
    return errors


def read_zip_json(
    archive: zipfile.ZipFile, name: str
) -> tuple[Any | None, list[str]]:
    try:
        with archive.open(name) as handle:
            raw = handle.read()
    except KeyError:
        return None, [f"missing required `{name}`"]
    except OSError as exc:
        return None, [f"could not read `{name}`: {exc}"]

    try:
        return json.loads(raw.decode("utf-8")), []
    except UnicodeDecodeError as exc:
        return None, [f"`{name}` is not UTF-8: {exc}"]
    except json.JSONDecodeError as exc:
        return None, [f"`{name}` invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]


def validate_dotlottie_manifest(
    manifest: Any, file_names: set[str]
) -> tuple[list[str], set[str], set[str], set[str]]:
    errors: list[str] = []
    animation_ids: set[str] = set()
    theme_ids: set[str] = set()
    state_machine_ids: set[str] = set()

    if not isinstance(manifest, dict):
        return ["manifest.json root must be a JSON object"], animation_ids, theme_ids, state_machine_ids

    version = manifest.get("version")
    if version != "2":
        errors.append("manifest.version must be `2` for dotLottie v2")

    animations = manifest.get("animations")
    if not isinstance(animations, list) or not animations:
        errors.append("manifest.animations must be a non-empty array")
    else:
        for index, animation in enumerate(animations):
            item_path = f"manifest.animations[{index}]"
            if not isinstance(animation, dict):
                errors.append(f"{item_path} must be an object")
                continue
            animation_id = validate_dotlottie_id(animation.get("id"), f"{item_path}.id", errors)
            if not animation_id:
                continue
            if animation_id in animation_ids:
                errors.append(f"duplicate animation id `{animation_id}`")
            animation_ids.add(animation_id)

            expected = f"a/{animation_id}.json"
            if expected not in file_names:
                errors.append(f"manifest animation `{animation_id}` missing `{expected}`")

    theme_ids = collect_manifest_ids(manifest, "themes", "theme", "t", file_names, errors)
    state_machine_ids = collect_manifest_ids(
        manifest, "stateMachines", "state machine", "s", file_names, errors
    )
    validate_initial_refs(manifest, animation_ids, state_machine_ids, errors)
    validate_animation_theme_refs(manifest, theme_ids, file_names, errors)

    return errors, animation_ids, theme_ids, state_machine_ids


def validate_dotlottie_id(value: Any, path: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path} must be a non-empty string")
        return None
    if not DOTLOTTIE_ID_RE.match(value):
        errors.append(
            f"{path} must contain only letters, numbers, dots, spaces, underscores, or hyphens"
        )
        return None
    return value


def collect_manifest_ids(
    manifest: dict[str, Any],
    key: str,
    label: str,
    folder: str,
    file_names: set[str],
    errors: list[str],
) -> set[str]:
    values = manifest.get(key)
    ids: set[str] = set()
    if values is None:
        return ids

    if not isinstance(values, list):
        errors.append(f"manifest.{key} must be an array when present")
        return ids

    for index, item in enumerate(values):
        item_path = f"manifest.{key}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_path} must be an object")
            continue
        item_id = validate_dotlottie_id(item.get("id"), f"{item_path}.id", errors)
        if not item_id:
            continue
        if item_id in ids:
            errors.append(f"duplicate {label} id `{item_id}`")
        ids.add(item_id)

        expected = f"{folder}/{item_id}.json"
        if expected not in file_names:
            errors.append(f"manifest {label} `{item_id}` missing `{expected}`")

    return ids


def validate_initial_refs(
    manifest: dict[str, Any],
    animation_ids: set[str],
    state_machine_ids: set[str],
    errors: list[str],
) -> None:
    initial = manifest.get("initial")
    if initial is None:
        return
    if not isinstance(initial, dict):
        errors.append("manifest.initial must be an object when present")
        return

    animation = initial.get("animation")
    if animation is not None and animation not in animation_ids:
        errors.append(f"manifest.initial.animation references unknown `{animation}`")

    state_machine = initial.get("stateMachine")
    if state_machine is not None and state_machine not in state_machine_ids:
        errors.append(f"manifest.initial.stateMachine references unknown `{state_machine}`")


def validate_animation_theme_refs(
    manifest: dict[str, Any],
    theme_ids: set[str],
    file_names: set[str],
    errors: list[str],
) -> None:
    animations = manifest.get("animations")
    if not isinstance(animations, list):
        return

    for index, animation in enumerate(animations):
        if not isinstance(animation, dict):
            continue
        item_path = f"manifest.animations[{index}]"

        initial_theme = animation.get("initialTheme")
        if initial_theme is not None:
            validate_theme_ref(initial_theme, f"{item_path}.initialTheme", theme_ids, file_names, errors)

        scoped_themes = animation.get("themes")
        if scoped_themes is None:
            continue
        if not isinstance(scoped_themes, list):
            errors.append(f"{item_path}.themes must be an array when present")
            continue
        for theme_index, theme_id in enumerate(scoped_themes):
            validate_theme_ref(
                theme_id,
                f"{item_path}.themes[{theme_index}]",
                theme_ids,
                file_names,
                errors,
            )


def validate_theme_ref(
    value: Any,
    path: str,
    theme_ids: set[str],
    file_names: set[str],
    errors: list[str],
) -> None:
    theme_id = validate_dotlottie_id(value, path, errors)
    if not theme_id:
        return
    if theme_ids and theme_id not in theme_ids:
        errors.append(f"{path} references unknown theme `{theme_id}`")
    if f"t/{theme_id}.json" not in file_names:
        errors.append(f"{path} missing `t/{theme_id}.json`")


def is_immediate_json_file(name: str, folder: str) -> bool:
    path = PurePosixPath(name)
    return len(path.parts) == 2 and path.parts[0] == folder and path.suffix == ".json"


def validate_optional_dotlottie_json_files(
    archive: zipfile.ZipFile,
    file_names: set[str],
    archive_label: str,
    folder: str,
    declared_ids: set[str],
) -> list[tuple[str, str]]:
    errors: list[tuple[str, str]] = []
    files = sorted(name for name in file_names if is_immediate_json_file(name, folder))

    for name in files:
        file_id = PurePosixPath(name).stem
        if declared_ids and file_id not in declared_ids:
            manifest_key = "themes" if folder == "t" else "stateMachines"
            errors.append(
                (archive_label, f"`{name}` is not declared in manifest.{manifest_key}")
            )

        data, read_errors = read_zip_json(archive, name)
        nested_label = f"{archive_label}!{name}"
        if read_errors:
            errors.extend((nested_label, error) for error in read_errors)
        elif not isinstance(data, dict):
            errors.append((nested_label, "must be a JSON object"))

    return errors


def validate_forbidden_dotlottie_asset_folders(
    file_names: set[str],
    archive_label: str,
    errors: list[tuple[str, str]],
) -> None:
    image_assets = sorted(name for name in file_names if name.startswith("i/"))
    font_assets = sorted(name for name in file_names if name.startswith("f/"))

    for name in image_assets:
        errors.append((archive_label, f"`{name}` is an image asset; use vector shapes"))
    for name in font_assets:
        errors.append((archive_label, f"`{name}` is a font asset; convert text to shapes"))


def validate_file(
    path: Path,
    *,
    max_dimension_px: int,
    max_duration_ms: int,
    max_framerate: int,
) -> list[tuple[str, str]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return validate_lottie_json_file(
            path,
            max_dimension_px=max_dimension_px,
            max_duration_ms=max_duration_ms,
            max_framerate=max_framerate,
        )
    if suffix == ".lottie":
        return validate_dotlottie_file(
            path,
            max_dimension_px=max_dimension_px,
            max_duration_ms=max_duration_ms,
            max_framerate=max_framerate,
        )
    return [(display_path(path), "unsupported file type; expected .json or .lottie")]


def group_errors(errors: list[tuple[str, str]]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for label, message in errors:
        grouped.setdefault(label, []).append(message)
    return grouped


def print_errors(errors: list[tuple[str, str]]) -> None:
    print("[FAIL] Lottie asset validation failed.", file=sys.stderr)
    for label, messages in group_errors(errors).items():
        print(f"{label}:", file=sys.stderr)
        for message in messages:
            print(f"  - {message}", file=sys.stderr)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate Lottie JSON and dotLottie assets for mobile icon motion."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Lottie .json, dotLottie .lottie, or directories to scan recursively.",
    )
    parser.add_argument(
        "--max-dimension-px",
        type=int,
        default=DEFAULT_MAX_DIMENSION_PX,
        help=f"Maximum allowed width/height in pixels. Default: {DEFAULT_MAX_DIMENSION_PX}.",
    )
    parser.add_argument(
        "--max-duration-ms",
        type=int,
        default=DEFAULT_MAX_DURATION_MS,
        help=f"Maximum derived animation duration. Default: {DEFAULT_MAX_DURATION_MS}.",
    )
    parser.add_argument(
        "--max-framerate",
        type=int,
        default=DEFAULT_MAX_FRAMERATE,
        help=f"Maximum allowed framerate. Default: {DEFAULT_MAX_FRAMERATE}.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    assets, discovery_errors = discover_assets(args.paths)
    errors = list(discovery_errors)

    for asset in assets:
        errors.extend(
            validate_file(
                asset,
                max_dimension_px=args.max_dimension_px,
                max_duration_ms=args.max_duration_ms,
                max_framerate=args.max_framerate,
            )
        )

    if errors:
        print_errors(errors)
        return 1

    print(f"[OK] {len(assets)} Lottie asset(s) valid.")
    for asset in assets:
        print(f"  - {display_path(asset)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
