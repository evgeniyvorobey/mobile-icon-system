#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_motion_spec.py"


VALID_SPEC = {
    "iconId": "ic_action_refresh",
    "trigger": "pullToRefreshReleased",
    "semanticPurpose": "Confirms that refresh has started and the list is updating.",
    "durationMs": 420,
    "easing": "standard",
    "allowedProperties": ["rotation", "opacity"],
    "timeline": [
        {
            "atMs": 0,
            "state": "idle",
            "properties": {"rotation": 0, "opacity": 1},
        },
        {
            "atMs": 220,
            "state": "active",
            "properties": {"rotation": 180, "opacity": 1},
        },
        {
            "atMs": 420,
            "state": "settled",
            "properties": {"rotation": 360, "opacity": 1},
        },
    ],
    "motionTriggers": [],
    "deliverables": {
        "lottie": "exports/lottie/ic_action_refresh.json",
        "dotLottie": "exports/dotlottie/ic_action_refresh.lottie",
    },
    "staticFrame": {
        "path": "exports/static/ic_action_refresh_static.svg",
        "timeMs": 420,
        "purpose": "Final settled refresh glyph used when motion is disabled.",
    },
    "reducedMotion": {
        "mode": "staticFrame",
        "fallback": "Use the static frame and update surrounding status text.",
        "motionTriggers": [],
        "durationMs": 0,
    },
    "validationEvidence": {
        "lottiePreview": "exports/reviews/ic_action_refresh_lottie_preview.png",
        "dotLottiePreview": "exports/reviews/ic_action_refresh_dotlottie_preview.png",
        "staticFrameReviewed": True,
        "reducedMotionTested": True,
        "platforms": ["ios", "android"],
    },
}

INVALID_SPEC = {
    "iconId": "refresh",
    "trigger": "onLoad",
    "semanticPurpose": "Decorative spin.",
    "durationMs": 3000,
    "easing": "springy",
    "allowedProperties": ["rotation", "blur"],
    "timeline": [
        {"atMs": 10, "state": "idle", "properties": {"blur": 6}},
        {"atMs": 3001, "state": "active", "properties": {"rotation": 360}},
    ],
    "deliverables": {
        "lottie": "exports/lottie/refresh.lottie",
        "dotLottie": "exports/dotlottie/refresh.json",
    },
    "staticFrame": {
        "path": "exports/static/refresh.txt",
        "timeMs": 4000,
        "purpose": "",
    },
    "reducedMotion": {
        "mode": "staticFrame",
        "fallback": "Keep spinning, slower.",
        "motionTriggers": ["spinning"],
        "durationMs": 500,
    },
    "validationEvidence": {
        "lottiePreview": "exports/reviews/refresh.png",
        "dotLottiePreview": "",
        "staticFrameReviewed": False,
        "reducedMotionTested": False,
        "platforms": [],
    },
}


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mobile-icon-motion-spec-") as temp:
        temp_root = Path(temp)
        valid_path = temp_root / "valid-motion-spec.json"
        invalid_path = temp_root / "invalid-motion-spec.json"
        batch_path = temp_root / "batch-motion-spec.json"

        write_json(valid_path, VALID_SPEC)
        write_json(invalid_path, INVALID_SPEC)
        write_json(batch_path, {"motionSpecs": [VALID_SPEC]})

        valid_result = run_validator(valid_path)
        if valid_result.returncode != 0:
            raise SystemExit(
                "[FAIL] valid motion spec failed validation\n"
                f"stdout:\n{valid_result.stdout}\n"
                f"stderr:\n{valid_result.stderr}"
            )

        invalid_result = run_validator(invalid_path)
        if invalid_result.returncode == 0:
            raise SystemExit(
                "[FAIL] invalid motion spec unexpectedly passed\n"
                f"stdout:\n{invalid_result.stdout}\n"
                f"stderr:\n{invalid_result.stderr}"
            )
        if "spinning" not in invalid_result.stderr:
            raise SystemExit(
                "[FAIL] invalid motion spec did not report banned reduced-motion trigger\n"
                f"stdout:\n{invalid_result.stdout}\n"
                f"stderr:\n{invalid_result.stderr}"
            )

        batch_result = run_validator(batch_path)
        if batch_result.returncode != 0:
            raise SystemExit(
                "[FAIL] batch motion spec failed validation\n"
                f"stdout:\n{batch_result.stdout}\n"
                f"stderr:\n{batch_result.stderr}"
            )

    print("[OK] Motion spec smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
