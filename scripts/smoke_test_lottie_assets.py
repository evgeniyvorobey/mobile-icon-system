#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_lottie_assets.py"


VALID_LOTTIE = {
    "v": "5.12.2",
    "fr": 60,
    "ip": 0,
    "op": 36,
    "w": 512,
    "h": 512,
    "layers": [
        {
            "ddd": 0,
            "ind": 1,
            "ty": 4,
            "nm": "Check",
            "ip": 0,
            "op": 36,
            "ks": {
                "o": {"a": 0, "k": 100},
                "r": {"a": 0, "k": 0},
                "p": {"a": 0, "k": [256, 256, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 0, "k": [100, 100, 100]},
            },
            "shapes": [
                {
                    "ty": "gr",
                    "it": [
                        {"ty": "el", "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [128, 128]}},
                        {"ty": "st", "c": {"a": 0, "k": [0, 0, 0, 1]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 12}},
                        {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}},
                    ],
                }
            ],
        }
    ],
}


INVALID_LOTTIE = {
    "v": "5.12.2",
    "fr": 60,
    "ip": 0,
    "op": 240,
    "w": 5000,
    "h": 512,
    "fonts": {"list": [{"fName": "BrandSans"}]},
    "assets": [
        {
            "id": "image_0",
            "w": 128,
            "h": 128,
            "u": "images/",
            "p": "image_0.png",
            "e": 0,
        }
    ],
    "layers": [
        {
            "ddd": 1,
            "ind": 1,
            "ty": 5,
            "nm": "Counter",
            "ip": 0,
            "op": 240,
            "ef": [{"nm": "Glow"}],
            "ks": {
                "r": {
                    "a": 0,
                    "k": 0,
                    "x": "var $bm_rt = time * 60;",
                }
            },
            "t": {"d": {"k": [{"s": {"t": "1", "f": "BrandSans"}}]}},
        }
    ],
}


def run_validator(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_lottie_archive(path: Path, manifest: object, animations: dict[str, object]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("manifest.json", json.dumps(manifest, indent=2))
        for animation_id, animation in animations.items():
            archive.writestr(f"a/{animation_id}.json", json.dumps(animation, indent=2))


def assert_success(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode != 0:
        raise SystemExit(
            f"[FAIL] {label} failed validation\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def assert_failure(
    result: subprocess.CompletedProcess[str], label: str, expected_fragments: list[str]
) -> None:
    if result.returncode == 0:
        raise SystemExit(
            f"[FAIL] {label} unexpectedly passed\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    output = result.stdout + result.stderr
    for fragment in expected_fragments:
        if fragment not in output:
            raise SystemExit(
                f"[FAIL] {label} did not report {fragment!r}\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mobile-icon-lottie-assets-") as temp:
        temp_root = Path(temp)
        valid_dir = temp_root / "valid"
        invalid_dir = temp_root / "invalid"
        nested_dir = valid_dir / "nested"
        valid_dir.mkdir()
        invalid_dir.mkdir()
        nested_dir.mkdir()

        valid_json = valid_dir / "valid-icon.json"
        nested_json = nested_dir / "nested-icon.json"
        invalid_json = invalid_dir / "invalid-icon.json"
        valid_archive = valid_dir / "valid-icon.lottie"
        invalid_archive = invalid_dir / "invalid-icon.lottie"

        write_json(valid_json, VALID_LOTTIE)
        write_json(nested_json, VALID_LOTTIE)
        write_json(invalid_json, INVALID_LOTTIE)

        write_lottie_archive(
            valid_archive,
            {"version": "2", "animations": [{"id": "valid-icon"}]},
            {"valid-icon": VALID_LOTTIE},
        )

        invalid_archive_lottie = copy.deepcopy(INVALID_LOTTIE)
        invalid_archive_lottie["layers"] = []
        write_lottie_archive(
            invalid_archive,
            {
                "version": "2",
                "animations": [
                    {"id": "missing-icon", "initialTheme": "missing-theme"}
                ],
                "themes": [{"id": "theme-light"}],
                "initial": {"animation": "missing-icon"},
            },
            {"bad-icon": invalid_archive_lottie},
        )

        assert_success(run_validator(str(valid_json)), "valid Lottie JSON")
        assert_success(run_validator(str(valid_archive)), "valid dotLottie archive")
        assert_success(run_validator(str(valid_dir)), "recursive valid directory")

        assert_failure(
            run_validator(str(invalid_json)),
            "invalid Lottie JSON",
            [
                "derived duration",
                "uses text layer type 5",
                "contains an expression",
                "references image or external asset data",
            ],
        )
        assert_failure(
            run_validator(str(invalid_archive)),
            "invalid dotLottie archive",
            [
                "manifest animation `missing-icon` missing",
                "`a/bad-icon.json` is not declared",
                "$.layers must not be empty",
                "missing `t/missing-theme.json`",
            ],
        )

    print("[OK] Lottie asset smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
