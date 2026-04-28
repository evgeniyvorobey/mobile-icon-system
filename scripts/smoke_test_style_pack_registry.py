#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_style_pack_registry.py"
VALID_FIXTURE = ROOT / "assets" / "style-pack-fixtures" / "valid" / "soft-plastic.style-pack"

EXPECTED_BUILTIN_IDS = {
    "duotone-chromatic",
    "liquid-glass",
    "claymorphism",
    "3d-isometric",
    "pixel-art",
    "hand-drawn",
}
EXPECTED_PLUGIN_ID = "fixture.soft-plastic"


def run_builder(*args: str, expect_success: bool) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(BUILDER), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if expect_success and result.returncode != 0:
        raise SystemExit(
            f"[FAIL] registry build failed: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    if not expect_success and result.returncode == 0:
        raise SystemExit(
            f"[FAIL] registry build unexpectedly succeeded: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def load_json(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[FAIL] registry output is invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("[FAIL] registry output root is not an object")
    return data


def assert_ids(registry: dict[str, object]) -> None:
    entries = registry.get("entries")
    if not isinstance(entries, list):
        raise SystemExit("[FAIL] registry entries is not a list")

    ids = {entry.get("id") for entry in entries if isinstance(entry, dict)}
    missing = (EXPECTED_BUILTIN_IDS | {EXPECTED_PLUGIN_ID}) - ids
    if missing:
        raise SystemExit(f"[FAIL] registry missing expected IDs: {sorted(missing)}")

    if registry.get("entryCount") != len(entries):
        raise SystemExit("[FAIL] entryCount does not match entries length")

    if registry.get("duplicateIds") != {}:
        raise SystemExit("[FAIL] clean registry unexpectedly recorded duplicates")

    for entry in entries:
        if not isinstance(entry, dict):
            raise SystemExit("[FAIL] registry entry is not an object")
        for key in ("id", "name", "status", "sourceType", "path", "categories", "tags", "refuseIf"):
            if key not in entry:
                raise SystemExit(f"[FAIL] registry entry missing {key}: {entry}")
        refuse_if = entry.get("refuseIf")
        if not isinstance(refuse_if, dict) or not refuse_if.get("summary"):
            raise SystemExit(f"[FAIL] registry entry missing refuseIf summary: {entry}")


def write_manifest(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    if not VALID_FIXTURE.exists():
        raise SystemExit(f"[FAIL] Missing valid fixture: {VALID_FIXTURE}")

    fixture_data = json.loads(VALID_FIXTURE.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory(prefix="mobile-icon-style-registry-") as temp:
        temp_root = Path(temp)
        registry_path = temp_root / "registry.json"

        run_builder(str(VALID_FIXTURE.parent), "--output", str(registry_path), expect_success=True)
        registry = load_json(registry_path)
        assert_ids(registry)

        duplicate_dir = temp_root / "duplicates"
        duplicate_dir.mkdir()
        duplicate_data = copy.deepcopy(fixture_data)
        duplicate_data["id"] = "pixel-art"
        duplicate_path = duplicate_dir / "pixel-art-duplicate.style-pack"
        write_manifest(duplicate_path, duplicate_data)

        duplicate_result = run_builder(
            str(duplicate_dir),
            "--output",
            str(temp_root / "should-not-exist.json"),
            expect_success=False,
        )
        duplicate_output = duplicate_result.stdout + duplicate_result.stderr
        if "duplicate style-pack IDs" not in duplicate_output or "pixel-art" not in duplicate_output:
            raise SystemExit(
                "[FAIL] duplicate detection output did not identify pixel-art\n"
                f"stdout:\n{duplicate_result.stdout}\n"
                f"stderr:\n{duplicate_result.stderr}"
            )

        allowed_path = temp_root / "allowed-duplicates.json"
        run_builder(
            str(duplicate_dir),
            "--allow-duplicates",
            "--output",
            str(allowed_path),
            expect_success=True,
        )
        allowed_registry = load_json(allowed_path)
        duplicates = allowed_registry.get("duplicateIds")
        if not isinstance(duplicates, dict) or "pixel-art" not in duplicates:
            raise SystemExit("[FAIL] --allow-duplicates did not record pixel-art")

    print("[OK] Style-pack registry smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
