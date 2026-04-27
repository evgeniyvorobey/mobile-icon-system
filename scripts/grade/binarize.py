"""Binarization helpers: alpha mask, luminance, white-composited grayscale."""
from __future__ import annotations

import numpy as np


def alpha_mask(rgba: np.ndarray, threshold: int = 128) -> np.ndarray:
    """Return a (H, W) bool mask where alpha >= threshold."""
    if rgba.ndim != 3 or rgba.shape[-1] != 4:
        raise ValueError(f"Expected RGBA array, got shape {rgba.shape}")
    return rgba[..., 3] >= threshold


def composite_over_white(rgba: np.ndarray) -> np.ndarray:
    """Composite an RGBA image over a white background; returns RGB uint8 (H, W, 3)."""
    if rgba.ndim != 3 or rgba.shape[-1] != 4:
        raise ValueError(f"Expected RGBA array, got shape {rgba.shape}")
    rgb = rgba[..., :3].astype(np.float32)
    a = rgba[..., 3:4].astype(np.float32) / 255.0
    out = rgb * a + 255.0 * (1.0 - a)
    return np.clip(out, 0.0, 255.0).astype(np.uint8)


def luminance(rgb_or_rgba: np.ndarray) -> np.ndarray:
    """Compute Rec. 601 luminance; returns float32 (H, W) in [0, 255]."""
    if rgb_or_rgba.ndim != 3 or rgb_or_rgba.shape[-1] not in (3, 4):
        raise ValueError(f"Expected RGB or RGBA array, got shape {rgb_or_rgba.shape}")
    if rgb_or_rgba.shape[-1] == 4:
        rgb = composite_over_white(rgb_or_rgba)
    else:
        rgb = rgb_or_rgba
    rgb_f = rgb.astype(np.float32)
    return 0.299 * rgb_f[..., 0] + 0.587 * rgb_f[..., 1] + 0.114 * rgb_f[..., 2]
