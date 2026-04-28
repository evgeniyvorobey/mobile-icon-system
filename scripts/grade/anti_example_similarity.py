"""Anti-example similarity check.

Compares a candidate SVG to every tier-C anti-example via perceptual hash.
A near-clone (small Hamming distance) is treated as a hard failure: the
candidate has reproduced a documented failure mode (e.g. gendered profile,
12-tooth blob gear, color-only state, over-detailed glyph).

Failure-mode labels are extracted from the matching anti-example's
``<stem>.notes.md`` file (the line after the ``## Failure mode`` heading).

Optional dependency on ``imagehash`` — when missing the public functions
raise ``ReferenceUnavailable`` so callers can degrade gracefully (mirrors
``grade.reference``).

Note on rendering: this module composites the rendered RGBA over a white
background **before** hashing. The base ``grade.reference`` module hashes
``Image.fromarray(rgba).convert('RGB')`` directly, which silently drops the
alpha channel and collapses any ``stroke="currentColor"`` SVG to all-black,
making every distance 0. Compositing here keeps the hash signal real.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

from PIL import Image

from .binarize import composite_over_white
from .config import DEFAULTS
from .rasterize import RasterizeError, render_svg
from .reference import ReferenceUnavailable, is_available


SvgSource = Union[str, Path]


try:
    import imagehash  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - exercised only when dep is absent
    imagehash = None  # type: ignore[assignment]


_FAILURE_MODE_RE = re.compile(
    r"^##\s+Failure\s+mode\s*\n+\s*\*\*([^*]+?)\*\*",
    re.IGNORECASE | re.MULTILINE,
)


def _hash_svg_white_composited(svg_source: SvgSource, size: int, hash_size: int):
    """Render SVG, composite over white, then phash. Differs from
    ``grade.reference._hash_svg`` which drops alpha without compositing."""
    if imagehash is None:
        raise ReferenceUnavailable(
            "install imagehash to use anti-example similarity check"
        )
    arr = render_svg(svg_source, size)
    rgb = composite_over_white(arr)
    img = Image.fromarray(rgb).convert("RGB")
    return imagehash.phash(img, hash_size=hash_size)


def _read_failure_mode(svg_path: Path) -> str:
    """Pull the failure-mode label from the sibling ``.notes.md`` file.

    Returns the bolded text immediately after the ``## Failure mode`` heading.
    Falls back to "unspecified" when the notes file is missing or has no
    failure-mode section.
    """
    notes_path = svg_path.with_suffix(".notes.md")
    if not notes_path.exists():
        # Some anti-examples might use ``.svg.notes.md``; try that too.
        alt = Path(str(svg_path) + ".notes.md")
        if alt.exists():
            notes_path = alt
        else:
            return "unspecified"
    try:
        text = notes_path.read_text(encoding="utf-8")
    except OSError:
        return "unspecified"
    match = _FAILURE_MODE_RE.search(text)
    if not match:
        return "unspecified"
    return match.group(1).strip().rstrip(".")


def _resolve_corpus(corpus_root: Path) -> List[Path]:
    """Return sorted ``*.svg`` files under ``corpus_root`` (recursive)."""
    if not corpus_root.exists() or not corpus_root.is_dir():
        return []
    return sorted(p for p in corpus_root.rglob("*.svg") if p.is_file())


def check_anti_example_similarity(
    svg_source: SvgSource,
    *,
    corpus_root: Path,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Compare ``svg_source`` against every anti-example SVG in ``corpus_root``.

    Parameters
    ----------
    svg_source:
        File path or raw SVG string for the candidate icon.
    corpus_root:
        Directory of anti-example SVGs (typically
        ``assets/references/tier-c/`` or a user-supplied custom directory).
    config:
        Optional config dict. Reads ``config["anti_example"]`` for thresholds:
            - ``render_size`` (default 64)
            - ``hash_size`` (default 8)
            - ``hard_fail_threshold`` (default 5)
            - ``warn_threshold`` (default 12)
            - ``top_n`` (default 3)

    Returns
    -------
    dict
        ``{"passed", "matches", "verdict", "errors", "warnings", ...}``.
        ``matches`` always contains the closest ``top_n`` anti-examples
        (even when nothing trips a threshold) for diagnostic value.

    Raises
    ------
    ReferenceUnavailable
        When ``imagehash`` is not installed.
    """
    if not is_available():
        raise ReferenceUnavailable(
            "install imagehash to use anti-example similarity check"
        )

    cfg_all = config or DEFAULTS
    cfg = cfg_all.get("anti_example") or DEFAULTS["anti_example"]
    render_size = int(cfg.get("render_size", 64))
    hash_size = int(cfg.get("hash_size", 8))
    hard_threshold = int(cfg.get("hard_fail_threshold", 5))
    warn_threshold = int(cfg.get("warn_threshold", 12))
    top_n = int(cfg.get("top_n", 3))

    errors: List[str] = []
    warnings: List[str] = []

    corpus = _resolve_corpus(Path(corpus_root))
    if not corpus:
        return {
            "passed": True,
            "matches": [],
            "verdict": "ok",
            "skipped": True,
            "reason": f"no anti-example SVGs found under {corpus_root}",
            "errors": errors,
            "warnings": [
                f"anti_example: no SVGs found in {corpus_root}; check skipped"
            ],
        }

    try:
        cand_hash = _hash_svg_white_composited(svg_source, render_size, hash_size)
    except RasterizeError as exc:
        return {
            "passed": False,
            "matches": [],
            "verdict": "hard_fail",
            "errors": [f"candidate render failed: {exc}"],
            "warnings": warnings,
        }

    scored: List[Dict[str, Any]] = []
    for ref_path in corpus:
        try:
            ref_hash = _hash_svg_white_composited(ref_path, render_size, hash_size)
        except RasterizeError as exc:
            errors.append(f"render failed for {ref_path.name}: {exc}")
            continue
        distance = int(cand_hash - ref_hash)
        scored.append(
            {
                "anti_example": ref_path.name,
                "anti_example_path": str(ref_path),
                "phash_distance": distance,
                "failure_mode": _read_failure_mode(ref_path),
            }
        )

    if not scored:
        return {
            "passed": False,
            "matches": [],
            "verdict": "hard_fail",
            "errors": errors or ["no anti-example references could be hashed"],
            "warnings": warnings,
        }

    scored.sort(key=lambda m: m["phash_distance"])
    top_matches = scored[: max(top_n, 1)]
    closest = scored[0]

    if closest["phash_distance"] <= hard_threshold:
        verdict = "hard_fail"
        passed = False
    elif closest["phash_distance"] <= warn_threshold:
        verdict = "warn"
        passed = True
        warnings.append(
            f"anti_example: candidate is suspiciously close to "
            f"{closest['anti_example']} (distance {closest['phash_distance']}, "
            f"failure mode: {closest['failure_mode']})"
        )
    else:
        verdict = "ok"
        passed = True

    return {
        "passed": passed,
        "verdict": verdict,
        "matches": top_matches,
        "closest": closest,
        "n_anti_examples": len(scored),
        "hard_fail_threshold": hard_threshold,
        "warn_threshold": warn_threshold,
        "errors": errors,
        "warnings": warnings,
    }
