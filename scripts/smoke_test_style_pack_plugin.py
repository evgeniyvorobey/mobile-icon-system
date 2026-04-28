#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_style_pack.py"
VALID_FIXTURE = ROOT / "assets" / "style-pack-fixtures" / "valid" / "soft-plastic.style-pack"


def run_validator(*args: str, expect_success: bool) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if expect_success and result.returncode != 0:
        raise SystemExit(
            f"[FAIL] validator command failed: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    if not expect_success and result.returncode == 0:
        raise SystemExit(
            f"[FAIL] validator command unexpectedly succeeded: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def write_manifest(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def expect_error_contains(path: Path, expected: str) -> None:
    result = run_validator(str(path), expect_success=False)
    output = result.stdout + result.stderr
    if expected not in output:
        raise SystemExit(
            f"[FAIL] expected validator output to contain {expected!r}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def main() -> int:
    if not VALID_FIXTURE.exists():
        raise SystemExit(f"[FAIL] Missing valid fixture: {VALID_FIXTURE}")

    valid_result = run_validator(str(VALID_FIXTURE), expect_success=True)
    if "[OK]" not in valid_result.stdout:
        raise SystemExit("[FAIL] Valid fixture did not produce an OK summary")

    with tempfile.TemporaryDirectory(prefix="mobile-icon-style-pack-") as temp:
        temp_root = Path(temp)
        nested_dir = temp_root / "nested"
        nested_dir.mkdir()
        shutil.copyfile(VALID_FIXTURE, nested_dir / "nested-soft-plastic.style-pack")
        run_validator(str(temp_root), expect_success=True)

        fixture_data = json.loads(VALID_FIXTURE.read_text(encoding="utf-8"))

        invalid_id = copy.deepcopy(fixture_data)
        invalid_id["id"] = "Bad Id"
        invalid_id_path = temp_root / "invalid-id.style-pack"
        write_manifest(invalid_id_path, invalid_id)
        expect_error_contains(invalid_id_path, "id must match")

        invalid_version = copy.deepcopy(fixture_data)
        invalid_version["version"] = "v1"
        invalid_version_path = temp_root / "invalid-version.style-pack"
        write_manifest(invalid_version_path, invalid_version)
        expect_error_contains(invalid_version_path, "version must be semver-ish")

        invalid_status = copy.deepcopy(fixture_data)
        invalid_status["status"] = "beta"
        invalid_status_path = temp_root / "invalid-status.style-pack"
        write_manifest(invalid_status_path, invalid_status)
        expect_error_contains(invalid_status_path, "status must be one of")

        missing_refuse_if = copy.deepcopy(fixture_data)
        missing_refuse_if["brandDnaConstraints"]["refuseIf"] = []
        missing_refuse_if_path = temp_root / "missing-refuse-if.style-pack"
        write_manifest(missing_refuse_if_path, missing_refuse_if)
        expect_error_contains(
            missing_refuse_if_path,
            "brandDnaConstraints.refuseIf must be a nonempty list",
        )

        missing_checks = copy.deepcopy(fixture_data)
        missing_checks["validation"]["checks"] = []
        missing_checks_path = temp_root / "missing-checks.style-pack"
        write_manifest(missing_checks_path, missing_checks)
        expect_error_contains(
            missing_checks_path,
            "validation.checks must be a nonempty list",
        )

        malformed_path = temp_root / "malformed.style-pack"
        malformed_path.write_text("{", encoding="utf-8")
        expect_error_contains(malformed_path, "invalid JSON")

    print("[OK] Style-pack plugin smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
