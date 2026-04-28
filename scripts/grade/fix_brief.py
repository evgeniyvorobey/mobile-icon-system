"""Per-icon regeneration brief generator.

Given an icon's grade result (the dict returned by ``report.aggregate_icon``),
build a Markdown fix brief the LLM can read and act on. The brief explains:

* which checks failed and by how much,
* which `craft-rubric.md` section to consult,
* whether a tier-A reference for the same metaphor exists in the corpus and
  what its `.notes.md` says to do,
* the original SVG markup so the LLM has full context to regenerate from.

Public API: :func:`render_fix_brief`. Helper :func:`infer_metaphor` exposed
for the orchestrator's reference-corpus matching.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Maps each measurable check to its craft-rubric.md citation. These citations
# are the anchors that survive even if numeric thresholds are later relaxed.
RUBRIC_CITATIONS: Dict[str, str] = {
    "silhouette": "craft-rubric.md §8.2 (silhouette connected-component count)",
    "weight": "craft-rubric.md §7.1 (visual weight variance) + §6.2 (counter-form area)",
    "alignment": "craft-rubric.md §2 (pixel grid alignment, with the math-derivation caveat)",
    "stroke": "craft-rubric.md §4.1 (within-icon stroke variation)",
    "squint": "craft-rubric.md §8.1 (identifiability under blur)",
    "balance": "craft-rubric.md §7.1 (visual weight variance across set)",
    "pair": "craft-rubric.md §7.3 (selected vs unselected state contrast)",
    "reference": "craft-rubric.md §3 (anchor economy) + corpus comparison",
}


# Section heading inside a tier-A `.notes.md` file we want to surface verbatim.
LEARN_SECTION = "## What a generator should learn"


# Suffixes we strip when inferring metaphor from a filename.
_SUFFIX_PATTERNS = (
    "_filled", "_outlined", "-filled", "-outlined",
    "_fill", "_outline", "-fill", "-outline",
)
# Common iOS/Android icon prefixes (e.g., ``ic_tab_home_filled.svg``).
_PREFIX_PATTERNS = (
    "ic_tab_", "ic_action_", "ic_status_", "ic_nav_", "ic_system_",
    "ic_", "icon_", "tab_", "nav_",
)


def infer_metaphor(filename: str) -> str:
    """Strip common platform prefixes/suffixes to recover the metaphor token.

    >>> infer_metaphor("ic_tab_home_filled.svg")
    'home'
    >>> infer_metaphor("bell.svg")
    'bell'
    >>> infer_metaphor("heart-outlined.svg")
    'heart'
    """
    stem = Path(filename).stem.lower()
    for prefix in _PREFIX_PATTERNS:
        if stem.startswith(prefix):
            stem = stem[len(prefix):]
            break
    for suffix in _SUFFIX_PATTERNS:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    return stem


def _read_svg(name: str, source_dir: Optional[Path]) -> str:
    if source_dir is None:
        return "(SVG path not provided to fix-brief renderer)"
    candidate = source_dir / name
    if not candidate.exists():
        return f"(SVG file not found at {candidate})"
    try:
        return candidate.read_text(encoding="utf-8")
    except OSError as exc:
        return f"(could not read SVG: {exc})"


def _find_corpus_match(metaphor: str, corpus_root: Optional[Path]) -> Optional[Path]:
    """Return the .svg file in `corpus_root` whose stem matches the metaphor."""
    if corpus_root is None or not corpus_root.exists():
        return None
    candidates = sorted(corpus_root.rglob("*.svg"))
    # Exact stem match (e.g., 'bell.svg', 'heart-filled.svg' -> match by metaphor).
    for path in candidates:
        if path.stem.lower() == metaphor:
            return path
    # Loosened: stem starts with metaphor (e.g., 'heart' matches 'heart-filled').
    for path in candidates:
        if path.stem.lower().startswith(f"{metaphor}-") or path.stem.lower().startswith(f"{metaphor}_"):
            return path
    return None


def _extract_learn_section(notes_path: Path) -> Optional[str]:
    """Pull the verbatim 'What a generator should learn' block from a .notes.md."""
    if not notes_path.exists():
        return None
    try:
        text = notes_path.read_text(encoding="utf-8")
    except OSError:
        return None
    lines = text.splitlines()
    block: List[str] = []
    in_block = False
    for line in lines:
        if line.strip().startswith(LEARN_SECTION):
            in_block = True
            continue
        if in_block:
            stripped = line.strip()
            # Stop at the next H2/H1 header.
            if stripped.startswith("## ") or stripped.startswith("# "):
                break
            block.append(line)
    body = "\n".join(block).strip()
    return body or None


def _format_pct(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"{float(value) * 100:.1f}%"


def _format_float(value: Any, ndigits: int = 3) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{ndigits}f}"


def _silhouette_lines(check: Dict[str, Any]) -> List[str]:
    expected = check.get("expected", "n/a")
    sizes = check.get("sizes") or {}
    out: List[str] = [
        f"- Measured: connected-component count expected {expected}, "
        f"observed at sizes {dict(sorted(sizes.items()))}.",
    ]
    for reg in check.get("regressions") or []:
        size = reg.get("size")
        count = reg.get("count")
        out.append(
            f"- At {size}pt the icon collapsed to {count} components "
            f"(should stay {reg.get('expected')})."
        )
    out.append(
        "- Fix: redraw so each visually-distinct region remains separated by "
        "≥2pt at the failing render size; consider adding a 1-2pt gap between "
        "touching strokes, or simplifying detail that disappears under "
        "rasterization."
    )
    return out


def _weight_lines(check: Dict[str, Any]) -> List[str]:
    ratio = check.get("weight_ratio")
    lo = check.get("min_ratio", 0.10)
    hi = check.get("max_ratio", 0.55)
    direction = (
        "below" if ratio is not None and ratio < float(lo)
        else "above" if ratio is not None and ratio > float(hi)
        else "outside"
    )
    return [
        f"- Measured: filled-pixel ratio at 24pt = {_format_float(ratio)} "
        f"(allowed band {_format_float(lo)}–{_format_float(hi)}).",
        f"- Verdict: ratio is {direction} the allowed band.",
        "- Fix: if too light (e.g., a 2-anchor tick), thicken the dominant "
        "stroke or convert to a filled silhouette; if too heavy, hollow out "
        "interior negative space (counter-form ≥35% of bounding box, "
        "see craft-rubric.md §6.2).",
    ]


def _alignment_lines(check: Dict[str, Any]) -> List[str]:
    by_size = check.get("off_grid_by_size") or {}
    out: List[str] = []
    for size in sorted(by_size.keys(), key=lambda x: int(x)):
        info = by_size[size]
        if not isinstance(info, dict):
            continue
        total = info.get("total")
        off = info.get("off_grid")
        ratio = info.get("ratio")
        out.append(
            f"- At {size}pt: {off}/{total} anchors off the integer grid "
            f"({_format_pct(ratio)})."
        )
        examples = info.get("examples") or []
        if examples:
            sample = ", ".join(f"({x}, {y})" for x, y in examples[:5])
            out.append(f"  Example off-grid coordinates: {sample}.")
    out.append(
        "- Fix: each off-grid coordinate must be either (a) a curve handle, "
        "(b) explicitly math-derived (e.g., from √3 / golden ratio / equal "
        "angular spacing — document the derivation in a comment), or "
        "(c) snapped to the nearest integer. The check tolerates math-derived "
        "anchors but cannot infer intent — document or snap."
    )
    return out


def _stroke_lines(check: Dict[str, Any]) -> List[str]:
    cv = check.get("cv")
    cv_max = check.get("cv_max", 0.15)
    return [
        f"- Measured: stroke-width coefficient of variation = {_format_float(cv)} "
        f"(threshold {_format_float(cv_max)}).",
        "- Fix: walk every stroked path and verify every segment uses the same "
        "`stroke-width`. Watch for: an interior detail with a thinner stroke, "
        "a hairline accent in the hood / clapper / roof region, or a path that "
        "carries a default 1px stroke from missing markup.",
    ]


def _squint_lines(check: Dict[str, Any]) -> List[str]:
    sig = check.get("signal_ratio")
    floor = check.get("min_signal_ratio", 0.05)
    return [
        f"- Measured: post-blur signal ratio = {_format_float(sig)} "
        f"(threshold {_format_float(floor)}).",
        "- Fix: the icon nearly vanishes at sigma=2px blur. Either thicken the "
        "stroke (1pt → 1.5pt or 2pt — see craft-rubric.md §2.4 for clean "
        "alignment values), or recruit more ink mass into the silhouette "
        "(e.g., add a filled element or close a hairline outline).",
    ]


def _generic_check_lines(name: str, check: Dict[str, Any]) -> List[str]:
    """Fallback summary used when a check has a non-standard shape."""
    out: List[str] = []
    if check.get("errors"):
        for err in check["errors"]:
            out.append(f"- error: {err}")
    if check.get("warnings"):
        for warn in check["warnings"]:
            out.append(f"- warn: {warn}")
    if not out:
        out.append("- (no detail extracted from this check)")
    return out


_CHECK_RENDERERS = {
    "silhouette": _silhouette_lines,
    "weight": _weight_lines,
    "alignment": _alignment_lines,
    "stroke": _stroke_lines,
    "squint": _squint_lines,
}


def _failed_checks(checks: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
    """Return (name, dict) pairs for every check that failed or warned."""
    failed: List[Tuple[str, Dict[str, Any]]] = []
    for name, check in checks.items():
        if not isinstance(check, dict):
            continue
        passed = bool(check.get("passed", True))
        has_errors = bool(check.get("errors"))
        has_warns = bool(check.get("warnings"))
        if not passed or has_errors or has_warns:
            failed.append((name, check))
    return failed


def render_fix_brief(
    icon_result: Dict[str, Any],
    *,
    corpus_root: Optional[Path] = None,
    source_dir: Optional[Path] = None,
) -> str:
    """Render a Markdown fix brief for an icon that failed or warned in grading.

    Parameters
    ----------
    icon_result:
        The per-icon dict from ``report.aggregate_icon`` — must contain
        ``name``, ``verdict``, ``checks``.
    corpus_root:
        Optional directory containing tier-A reference SVGs and their
        ``.notes.md`` files. When provided and a same-metaphor reference
        exists, the brief quotes that reference's "What a generator should
        learn" block verbatim.
    source_dir:
        Directory the icon was loaded from; used to read the original SVG
        markup so the LLM has the path data.
    """
    name = icon_result.get("name", "<unknown>")
    verdict = icon_result.get("verdict", "warn")
    checks = icon_result.get("checks") or {}

    out: List[str] = []
    out.append(f"### {name} — verdict: `{verdict}`")
    out.append("")

    failed = _failed_checks(checks)
    if not failed:
        out.append("- (no failing checks; this icon should not be in the brief)")
        out.append("")
        return "\n".join(out)

    out.append("**Why this icon needs regeneration**")
    out.append("")
    for check_name, check in failed:
        citation = RUBRIC_CITATIONS.get(check_name, "see craft-rubric.md")
        out.append(f"#### {check_name} (cite: {citation})")
        renderer = _CHECK_RENDERERS.get(check_name, lambda c: _generic_check_lines(check_name, c))
        for line in renderer(check):
            out.append(line)
        out.append("")

    metaphor = infer_metaphor(name)
    ref_svg = _find_corpus_match(metaphor, corpus_root)
    out.append("**Tier-A reference for this metaphor**")
    out.append("")
    if ref_svg is None:
        out.append(
            f"- No tier-A reference for metaphor `{metaphor}` in the corpus. "
            "Apply craft-rubric thresholds directly."
        )
    else:
        rel_ref = ref_svg
        out.append(f"- Reference SVG: `{rel_ref}`")
        notes_path = ref_svg.with_suffix(".notes.md")
        learn = _extract_learn_section(notes_path)
        if learn:
            out.append("- Key principles (from the reference's notes, verbatim):")
            out.append("")
            for line in learn.splitlines():
                out.append(f"  > {line}" if line.strip() else "  >")
            out.append("")
        else:
            out.append(
                f"- No `.notes.md` found at `{notes_path}` — read the SVG "
                "directly for path-data construction patterns."
            )
    out.append("")

    out.append("**Original SVG (regenerate from this baseline)**")
    out.append("")
    out.append("```xml")
    out.append(_read_svg(name, source_dir))
    out.append("```")
    out.append("")

    out.append("**Regeneration instructions**")
    out.append("")
    out.append(
        "1. Address every numbered fix above. Do not introduce new failures "
        "on other axes."
    )
    out.append(
        "2. Preserve the icon's metaphor and visual identity — this is a "
        "craft refinement, not a redesign."
    )
    if ref_svg is not None:
        out.append(
            "3. Compare the regenerated path data against the tier-A "
            "reference's construction — the reference is the calibration target, "
            "not a copy source."
        )
    out.append(
        f"{'4' if ref_svg is not None else '3'}. Output the new SVG only "
        "(no commentary inside the SVG; commentary outside is welcome)."
    )
    out.append("")
    return "\n".join(out)
