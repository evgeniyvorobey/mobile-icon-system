#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


MIN_DURATION_MS = 50
MAX_DURATION_MS = 1500

NAMED_EASINGS = {
    "linear",
    "standard",
    "decelerate",
    "accelerate",
    "ease-in-out",
    "emphasized",
}

ALLOWED_PROPERTIES = {
    "opacity",
    "scale",
    "scaleX",
    "scaleY",
    "translateX",
    "translateY",
    "rotation",
    "strokeDashOffset",
    "pathTrimStart",
    "pathTrimEnd",
    "pathTrimOffset",
    "fillColor",
    "strokeColor",
}

REDUCED_MOTION_MODES = {
    "staticFrame",
    "dissolve",
    "highlightFade",
    "colorShift",
}

BANNED_REDUCED_MOTION_TRIGGERS = {
    "animatedblur",
    "autoadvance",
    "depth",
    "depthoffield",
    "depthsimulation",
    "multiaxis",
    "multispeed",
    "ongoingmotion",
    "parallax",
    "peripheralmotion",
    "perspective",
    "scalezoom",
    "scaling",
    "spinning",
    "vortex",
    "zaxis",
    "zooming",
}

REQUIRED_FIELDS = {
    "iconId",
    "trigger",
    "semanticPurpose",
    "timeline",
    "durationMs",
    "easing",
    "allowedProperties",
    "deliverables",
    "staticFrame",
    "reducedMotion",
    "validationEvidence",
}

CUBIC_BEZIER_RE = re.compile(
    r"^cubic-bezier\(\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,"
    r"\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*\)$"
)


class MotionSpecValidator:
    def __init__(self, spec: dict[str, Any], label: str) -> None:
        self.spec = spec
        self.label = label
        self.errors: list[str] = []

    def validate(self) -> list[str]:
        self._required_fields()
        self._basic_strings()
        self._duration()
        self._easing()
        self._allowed_properties()
        self._timeline()
        self._deliverables()
        self._static_frame()
        self._reduced_motion()
        self._validation_evidence()
        return self.errors

    def _error(self, message: str) -> None:
        self.errors.append(f"{self.label}: {message}")

    def _required_fields(self) -> None:
        missing = sorted(REQUIRED_FIELDS - self.spec.keys())
        for field in missing:
            self._error(f"missing required field `{field}`")

    def _basic_strings(self) -> None:
        for field in ("iconId", "trigger", "semanticPurpose"):
            value = self.spec.get(field)
            if not isinstance(value, str) or not value.strip():
                self._error(f"`{field}` must be a non-empty string")

        icon_id = self.spec.get("iconId")
        if isinstance(icon_id, str) and icon_id and not re.match(r"^ic_[a-z0-9_]+$", icon_id):
            self._error("`iconId` should use `ic_` + lowercase snake_case")

    def _duration(self) -> None:
        duration = self.spec.get("durationMs")
        if not isinstance(duration, int) or isinstance(duration, bool):
            self._error("`durationMs` must be an integer number of milliseconds")
            return

        if duration < MIN_DURATION_MS or duration > MAX_DURATION_MS:
            self._error(
                f"`durationMs` must be between {MIN_DURATION_MS} and "
                f"{MAX_DURATION_MS} ms"
            )

    def _easing(self) -> None:
        easing = self.spec.get("easing")
        if isinstance(easing, str):
            if easing in NAMED_EASINGS:
                return
            if self._is_valid_cubic_bezier_string(easing):
                return
            self._error(
                "`easing` must be a named easing or "
                "`cubic-bezier(x1, y1, x2, y2)`"
            )
            return

        if isinstance(easing, dict):
            if easing.get("type") == "cubic-bezier" and self._valid_bezier_values(
                easing.get("value")
            ):
                return
            self._error(
                "`easing` object must be "
                '{"type": "cubic-bezier", "value": [x1, y1, x2, y2]}'
            )
            return

        self._error("`easing` must be a string or cubic-bezier object")

    def _allowed_properties(self) -> None:
        properties = self.spec.get("allowedProperties")
        if not isinstance(properties, list) or not properties:
            self._error("`allowedProperties` must be a non-empty array")
            return

        seen: set[str] = set()
        for item in properties:
            if not isinstance(item, str) or not item:
                self._error("`allowedProperties` entries must be non-empty strings")
                continue
            if item in seen:
                self._error(f"`allowedProperties` contains duplicate `{item}`")
            seen.add(item)
            if item not in ALLOWED_PROPERTIES:
                self._error(f"`allowedProperties` contains unsupported `{item}`")

    def _timeline(self) -> None:
        timeline = self.spec.get("timeline")
        duration = self.spec.get("durationMs")
        allowed = set(self.spec.get("allowedProperties", []))

        if not isinstance(timeline, list) or not timeline:
            self._error("`timeline` must be a non-empty array")
            return

        previous_at: int | None = None
        for index, step in enumerate(timeline):
            step_label = f"`timeline[{index}]`"
            if not isinstance(step, dict):
                self._error(f"{step_label} must be an object")
                continue

            at_ms = step.get("atMs")
            if not isinstance(at_ms, int) or isinstance(at_ms, bool):
                self._error(f"{step_label}.atMs must be an integer")
            else:
                if previous_at is not None and at_ms < previous_at:
                    self._error("`timeline` must be ordered by ascending `atMs`")
                previous_at = at_ms
                if at_ms < 0:
                    self._error(f"{step_label}.atMs must be >= 0")
                if isinstance(duration, int) and not isinstance(duration, bool) and at_ms > duration:
                    self._error(f"{step_label}.atMs exceeds `durationMs`")

            state = step.get("state")
            properties = step.get("properties")
            if (not isinstance(state, str) or not state.strip()) and not isinstance(
                properties, dict
            ):
                self._error(f"{step_label} needs a non-empty `state` or `properties`")

            if isinstance(properties, dict):
                for property_name in properties:
                    if property_name not in allowed:
                        self._error(
                            f"{step_label}.properties uses `{property_name}` "
                            "outside `allowedProperties`"
                        )

        first_step = timeline[0] if isinstance(timeline[0], dict) else {}
        if first_step.get("atMs") != 0:
            self._error("`timeline` must start at `atMs: 0`")

    def _deliverables(self) -> None:
        deliverables = self.spec.get("deliverables")
        if not isinstance(deliverables, dict):
            self._error("`deliverables` must be an object")
            return

        lottie = deliverables.get("lottie")
        dot_lottie = deliverables.get("dotLottie")
        if not isinstance(lottie, str) or not lottie.endswith(".json"):
            self._error("`deliverables.lottie` must be a `.json` path")
        if not isinstance(dot_lottie, str) or not dot_lottie.endswith(".lottie"):
            self._error("`deliverables.dotLottie` must be a `.lottie` path")

    def _static_frame(self) -> None:
        static_frame = self.spec.get("staticFrame")
        duration = self.spec.get("durationMs")
        if not isinstance(static_frame, dict):
            self._error("`staticFrame` must be an object")
            return

        path = static_frame.get("path")
        if not isinstance(path, str) or not path:
            self._error("`staticFrame.path` must be a non-empty string")
        elif not path.endswith((".svg", ".pdf", ".png")):
            self._error("`staticFrame.path` must be `.svg`, `.pdf`, or `.png`")

        time_ms = static_frame.get("timeMs")
        if not isinstance(time_ms, int) or isinstance(time_ms, bool):
            self._error("`staticFrame.timeMs` must be an integer")
        else:
            if time_ms < 0:
                self._error("`staticFrame.timeMs` must be >= 0")
            if isinstance(duration, int) and not isinstance(duration, bool) and time_ms > duration:
                self._error("`staticFrame.timeMs` must be within `durationMs`")

        purpose = static_frame.get("purpose")
        if not isinstance(purpose, str) or not purpose.strip():
            self._error("`staticFrame.purpose` must describe preserved meaning")

    def _reduced_motion(self) -> None:
        reduced_motion = self.spec.get("reducedMotion")
        if not isinstance(reduced_motion, dict):
            self._error("`reducedMotion` must be an object")
            return

        mode = reduced_motion.get("mode")
        if mode not in REDUCED_MOTION_MODES:
            self._error(
                "`reducedMotion.mode` must be one of: "
                + ", ".join(sorted(REDUCED_MOTION_MODES))
            )

        fallback = reduced_motion.get("fallback")
        if not isinstance(fallback, str) or not fallback.strip():
            self._error("`reducedMotion.fallback` must be a non-empty string")

        duration = reduced_motion.get("durationMs", 0)
        if not isinstance(duration, int) or isinstance(duration, bool) or duration < 0:
            self._error("`reducedMotion.durationMs` must be a non-negative integer")
        elif duration > 250:
            self._error("`reducedMotion.durationMs` should not exceed 250 ms")

        fallback_triggers = reduced_motion.get("motionTriggers", [])
        if not isinstance(fallback_triggers, list):
            self._error("`reducedMotion.motionTriggers` must be an array when present")
            fallback_triggers = []

        for trigger in fallback_triggers:
            if not isinstance(trigger, str):
                self._error("`reducedMotion.motionTriggers` entries must be strings")
                continue
            if normalized_trigger(trigger) in BANNED_REDUCED_MOTION_TRIGGERS:
                self._error(
                    f"`reducedMotion.motionTriggers` contains banned trigger `{trigger}`"
                )

        fallback_properties = reduced_motion.get("properties", [])
        if isinstance(fallback_properties, list):
            for property_name in fallback_properties:
                if normalized_trigger(str(property_name)) in BANNED_REDUCED_MOTION_TRIGGERS:
                    self._error(
                        f"`reducedMotion.properties` contains banned trigger "
                        f"`{property_name}`"
                    )

        default_triggers = self.spec.get("motionTriggers", [])
        if isinstance(default_triggers, list) and mode not in REDUCED_MOTION_MODES:
            problematic = sorted(
                trigger
                for trigger in default_triggers
                if isinstance(trigger, str)
                and normalized_trigger(trigger) in BANNED_REDUCED_MOTION_TRIGGERS
            )
            if problematic:
                self._error(
                    "default `motionTriggers` include reduced-motion-sensitive "
                    "triggers without a valid fallback: " + ", ".join(problematic)
                )

    def _validation_evidence(self) -> None:
        evidence = self.spec.get("validationEvidence")
        if not isinstance(evidence, dict):
            self._error("`validationEvidence` must be an object")
            return

        for field in ("lottiePreview", "dotLottiePreview", "platforms"):
            if field not in evidence:
                self._error(f"`validationEvidence.{field}` is required")

        for field in ("lottiePreview", "dotLottiePreview"):
            value = evidence.get(field)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                self._error(f"`validationEvidence.{field}` must be a non-empty string")

        if evidence.get("staticFrameReviewed") is not True:
            self._error("`validationEvidence.staticFrameReviewed` must be true")
        if evidence.get("reducedMotionTested") is not True:
            self._error("`validationEvidence.reducedMotionTested` must be true")

        platforms = evidence.get("platforms")
        if not isinstance(platforms, list) or not platforms:
            self._error("`validationEvidence.platforms` must be a non-empty array")
        elif any(not isinstance(platform, str) or not platform for platform in platforms):
            self._error("`validationEvidence.platforms` entries must be strings")

    def _is_valid_cubic_bezier_string(self, value: str) -> bool:
        match = CUBIC_BEZIER_RE.match(value)
        if not match:
            return False
        return self._valid_bezier_values([float(part) for part in match.groups()])

    def _valid_bezier_values(self, value: Any) -> bool:
        if not isinstance(value, list) or len(value) != 4:
            return False
        if any(not isinstance(item, (int, float)) or isinstance(item, bool) for item in value):
            return False

        x1, y1, x2, y2 = [float(item) for item in value]
        return 0 <= x1 <= 1 and 0 <= x2 <= 1 and -2 <= y1 <= 2 and -2 <= y2 <= 2


def normalized_trigger(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def load_specs(path: Path) -> list[tuple[str, dict[str, Any]]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[FAIL] Invalid JSON: {path}: {exc}") from exc
    except OSError as exc:
        raise SystemExit(f"[FAIL] Cannot read {path}: {exc}") from exc

    if isinstance(data, dict) and "motionSpecs" in data and not isinstance(
        data["motionSpecs"], list
    ):
        raise SystemExit(f"[FAIL] {path}: `motionSpecs` must be an array")

    if isinstance(data, dict) and isinstance(data.get("motionSpecs"), list):
        if not data["motionSpecs"]:
            raise SystemExit(f"[FAIL] {path}: `motionSpecs` must not be empty")
        specs: list[tuple[str, dict[str, Any]]] = []
        for index, item in enumerate(data["motionSpecs"]):
            if isinstance(item, dict):
                specs.append((f"{path}:motionSpecs[{index}]", item))
            else:
                raise SystemExit(
                    f"[FAIL] {path}:motionSpecs[{index}] must be an object"
                )
        return specs

    if isinstance(data, dict):
        return [(str(path), data)]

    raise SystemExit("[FAIL] Motion spec must be an object or contain `motionSpecs`")


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    for label, spec in load_specs(path):
        errors.extend(MotionSpecValidator(spec, label).validate())
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate mobile icon motion specs.")
    parser.add_argument("spec", type=Path, help="Path to a motion spec JSON file.")
    args = parser.parse_args(argv)

    errors = validate_file(args.spec)
    if errors:
        for error in errors:
            print(f"[FAIL] {error}", file=sys.stderr)
        return 1

    print(f"[OK] Motion spec passed: {args.spec}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
