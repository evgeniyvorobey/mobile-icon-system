"""Default thresholds and config loader for the grade pipeline.

All thresholds live in `DEFAULTS`. Callers pass a config dict (typically the
return value of `load_config`) into each algorithm module.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULTS: Dict[str, Any] = {
    "silhouette": {
        "sizes": [16, 20, 24],
        "alpha_threshold": 128,
        "min_component_px": 2,
    },
    "weight": {
        "render_size": 24,
        "alpha_threshold": 128,
        "min_ratio": 0.10,
        "max_ratio": 0.55,
        "set_z_max": 2.5,
        "set_band": 0.35,
        "min_set_size_for_mad": 4,
    },
    "alignment": {
        "sizes": [16, 20, 24],
        "tolerance": 0.10,
        # Default threshold (0.50) is empirically calibrated against the tier-A
        # corpus. Tier-A icons (Lucide bell/settings, Phosphor heart) routinely
        # use mathematically-derived endpoints (e.g., 12 - √3 = 10.268 for the
        # bell's clapper at 60° subtended) that read as off-grid by the simple
        # nearest-integer test, but are correct craft per the math-derivation
        # principle. Use --strict to drop to 0.05 for catching genuinely sloppy
        # half-pixel/quarter-pixel anchors. See references/craft-rubric.md §2.
        "max_off_grid_ratio_24": 0.50,
        "default_view_box": (0.0, 0.0, 24.0, 24.0),
    },
    "stroke": {
        "render_size": 72,
        "cv_max": 0.15,
        "cv_max_strict": 0.10,
        "filled_skip_ratio": 0.40,
        "min_samples": 20,
    },
    "squint": {
        "render_size": 24,
        "blur_radius": 2.0,
        "luminance_threshold": 192,
        "min_signal_ratio": 0.05,
    },
    "pair": {
        "render_size": 24,
        "channel_diff_threshold": 16,
        "min_diff_ratio": 0.10,
        "min_relative_diff": 0.30,
        "alpha_threshold": 128,
    },
    "reference": {
        "render_size": 64,
        "hash_size": 8,
        "plagiarism_max": 5,
        "off_vocab_min": 22,
    },
}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key, value in base.items():
        if key in override and isinstance(value, dict) and isinstance(override[key], dict):
            out[key] = _deep_merge(value, override[key])
        elif key in override:
            out[key] = override[key]
        else:
            out[key] = value
    for key, value in override.items():
        if key not in base:
            out[key] = value
    return out


def _load_toml(path: Path) -> Dict[str, Any]:
    if sys.version_info >= (3, 11):
        import tomllib  # type: ignore[import-not-found]

        with path.open("rb") as fh:
            return tomllib.load(fh)
    try:
        import tomli  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover - tomli optional on 3.9/3.10
        raise RuntimeError(
            "Reading TOML config on Python <3.11 requires `tomli`. "
            "Install with: pip install tomli"
        ) from exc
    with path.open("rb") as fh:
        return tomli.load(fh)


def load_config(path: Optional[Path] = None) -> Dict[str, Any]:
    """Load a TOML config and merge it on top of DEFAULTS.

    Returns a deep-copy-style merged dict. Pass ``None`` to get the defaults.
    """
    if path is None:
        return _deep_merge(DEFAULTS, {})
    override = _load_toml(Path(path))
    return _deep_merge(DEFAULTS, override)


def apply_strictness(config: Dict[str, Any], *, strict: bool = False, lenient: bool = False) -> Dict[str, Any]:
    """Apply strict / lenient overrides on top of a loaded config."""
    cfg = _deep_merge(config, {})
    if strict:
        cfg["stroke"]["cv_max"] = cfg["stroke"]["cv_max_strict"]
        cfg["weight"]["set_z_max"] = min(cfg["weight"]["set_z_max"], 2.0)
        cfg["alignment"]["max_off_grid_ratio_24"] = min(
            cfg["alignment"]["max_off_grid_ratio_24"], 0.05
        )
    if lenient:
        cfg["stroke"]["cv_max"] = max(cfg["stroke"]["cv_max"], 0.20)
        cfg["weight"]["set_z_max"] = max(cfg["weight"]["set_z_max"], 3.0)
        cfg["alignment"]["max_off_grid_ratio_24"] = max(
            cfg["alignment"]["max_off_grid_ratio_24"], 0.20
        )
    return cfg
