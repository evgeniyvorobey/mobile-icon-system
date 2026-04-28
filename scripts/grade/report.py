"""Aggregate per-icon and set-level results into Markdown + JSON reports."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


_VERDICT_ORDER = {"hard_fail": 0, "warn": 1, "ok": 2}


def _verdict_for_icon(icon: Dict[str, Any]) -> str:
    if icon.get("errors"):
        return "hard_fail"
    if icon.get("hard_fail"):
        return "hard_fail"
    if icon.get("warnings"):
        return "warn"
    return "ok"


def aggregate_icon(name: str, checks: Dict[str, Any]) -> Dict[str, Any]:
    """Roll a single icon's per-check results into one dict + verdict."""
    # Default hard-fail keys catch unambiguous failures: silhouette
    # regressions across sizes (icon literally vanishes at 16pt) and the
    # semantic-failure checks added in v0.4 (anti_example_similarity,
    # color_only_state). Alignment, single-icon weight, stroke, and squint
    # are warn-by-default because they all produced false positives on the
    # tier-A corpus during calibration:
    #   - alignment: tier-A icons (Lucide bell, Tabler settings) use
    #     mathematically-derived endpoints (12 ± √3) that read as off-grid
    #   - single-icon weight: minimal icons (check, x) sit below 0.10 floor
    #     by design
    #   - stroke: distance-transform medial-axis approximation has noise on
    #     small features
    #   - squint: hairline stroke icons tested under blur radius R/12
    #     teeter at the 0.05 signal threshold
    # See craft-rubric.md §2 caveat for the math-derivation exemption.
    # Use --strict to re-promote alignment + weight to hard_fail.
    #
    # The semantic-failure checks (anti_example_similarity, color_only_state)
    # were promoted from warn to hard_fail in v0.4 — they catch unambiguous
    # failures the LLM was producing (gendered profile silhouettes,
    # color-only state distinctions). See craft-rubric.md §10.
    hard_fail_keys = ("silhouette", "anti_example_similarity", "color_only_state")
    warn_keys = ("alignment", "weight", "stroke", "squint")
    errors: List[str] = []
    warnings: List[str] = []
    hard_fail = False

    for key, result in checks.items():
        if not isinstance(result, dict):
            continue
        for err in result.get("errors", []) or []:
            errors.append(f"{key}: {err}")
        for warn in result.get("warnings", []) or []:
            warnings.append(f"{key}: {warn}")
        # Honor explicit hard_fail flags even when ``passed`` is True
        # (semantic checks may surface a hard_fail directly).
        if result.get("hard_fail"):
            hard_fail = True
            continue
        if not result.get("passed", True):
            if key in hard_fail_keys:
                hard_fail = True
            elif key in warn_keys:
                warnings.append(f"{key}: failed soft threshold")
            else:
                warnings.append(f"{key}: failed")

    icon: Dict[str, Any] = {
        "name": name,
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
        "hard_fail": hard_fail,
    }
    icon["verdict"] = _verdict_for_icon(icon)
    return icon


def aggregate_set(
    icons: List[Dict[str, Any]],
    set_checks: Dict[str, Any],
) -> Dict[str, Any]:
    set_warnings: List[str] = []
    set_errors: List[str] = []
    hard_fail_set = False
    for key, result in set_checks.items():
        if not isinstance(result, dict):
            continue
        for warn in result.get("warnings", []) or []:
            set_warnings.append(f"{key}: {warn}")
        for err in result.get("errors", []) or []:
            set_errors.append(f"{key}: {err}")
        if not result.get("passed", True):
            # Set-level failures are warnings unless explicitly hard.
            if result.get("hard_fail"):
                hard_fail_set = True
            else:
                set_warnings.append(f"{key}: failed")
    summary = {
        "n_icons": len(icons),
        "ok": sum(1 for i in icons if i["verdict"] == "ok"),
        "warn": sum(1 for i in icons if i["verdict"] == "warn"),
        "hard_fail": sum(1 for i in icons if i["verdict"] == "hard_fail"),
    }
    overall_verdict = "ok"
    if summary["hard_fail"] > 0 or hard_fail_set:
        overall_verdict = "hard_fail"
    elif summary["warn"] > 0 or set_warnings:
        overall_verdict = "warn"
    return {
        "icons": sorted(icons, key=lambda i: (_VERDICT_ORDER[i["verdict"]], i["name"])),
        "set_checks": set_checks,
        "set_warnings": set_warnings,
        "set_errors": set_errors,
        "summary": summary,
        "verdict": overall_verdict,
    }


def render_json(report: Dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True, default=_json_default)


def _json_default(obj: Any) -> Any:
    try:
        import numpy as np  # noqa: F401  (only needed for fallback)
    except ImportError:
        raise TypeError(f"not JSON-serializable: {type(obj).__name__}")
    import numpy as np

    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"not JSON-serializable: {type(obj).__name__}")


def _format_pct(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"{float(value) * 100:.1f}%"


def _format_float(value: Any, ndigits: int = 3) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{ndigits}f}"


def _icon_row(icon: Dict[str, Any]) -> str:
    checks = icon.get("checks", {})
    sil = checks.get("silhouette", {})
    w = checks.get("weight", {})
    align = checks.get("alignment", {})
    sk = checks.get("stroke", {})
    sq = checks.get("squint", {})
    align24 = (align.get("off_grid_by_size") or {}).get(24, {})
    align_ratio = align24.get("ratio") if isinstance(align24, dict) else None
    return (
        f"| {icon['name']} | {icon['verdict']} | "
        f"{'pass' if sil.get('passed') else 'fail'} ({sil.get('expected', 'n/a')}) | "
        f"{_format_float(w.get('weight_ratio'))} | "
        f"{_format_pct(align_ratio)} | "
        f"{_format_float(sk.get('cv'))} | "
        f"{_format_float(sq.get('signal_ratio'))} |"
    )


def render_markdown(report: Dict[str, Any]) -> str:
    summary = report["summary"]
    out: List[str] = []
    out.append("# Icon grading report")
    out.append("")
    out.append(f"Overall verdict: **{report['verdict']}**")
    out.append(
        f"- Icons: {summary['n_icons']} (ok={summary['ok']}, "
        f"warn={summary['warn']}, hard_fail={summary['hard_fail']})"
    )
    out.append("")

    if report.get("set_warnings"):
        out.append("## Set-level warnings")
        for w in report["set_warnings"]:
            out.append(f"- {w}")
        out.append("")
    if report.get("set_errors"):
        out.append("## Set-level errors")
        for e in report["set_errors"]:
            out.append(f"- {e}")
        out.append("")

    out.append("## Per-icon results")
    out.append(
        "| Icon | Verdict | Silhouette (count) | Weight ratio | Off-grid@24 | Stroke CV | Squint signal |"
    )
    out.append(
        "| --- | --- | --- | --- | --- | --- | --- |"
    )
    for icon in report["icons"]:
        out.append(_icon_row(icon))
    out.append("")

    # Anti-example similarity table: surface which anti-example the icon
    # most resembled, the failure mode it represents, and the pHash distance.
    anti_rows: List[str] = []
    for icon in report["icons"]:
        ae = (icon.get("checks") or {}).get("anti_example_similarity") or {}
        if not isinstance(ae, dict) or ae.get("skipped"):
            continue
        closest = ae.get("closest")
        if not closest:
            continue
        anti_rows.append(
            f"| {icon['name']} | {ae.get('verdict', 'n/a')} | "
            f"{closest.get('anti_example', 'n/a')} | "
            f"{closest.get('failure_mode', 'unspecified')} | "
            f"{closest.get('phash_distance', 'n/a')} |"
        )
    if anti_rows:
        out.append("## Anti-example similarity")
        out.append(
            "| Icon | Verdict | Closest anti-example | Failure mode | pHash distance |"
        )
        out.append("| --- | --- | --- | --- | --- |")
        out.extend(anti_rows)
        out.append("")

    # Color-only state diagnostics: surface every state pair's color vs
    # shape diff so reviewers can sanity-check borderline calls.
    pair_block = report.get("set_checks", {}).get("pair") or {}
    pair_results = pair_block.get("results") or []
    cos_rows: List[str] = []
    for pr in pair_results:
        cos = pr.get("color_only_state") or {}
        if not isinstance(cos, dict):
            continue
        cos_rows.append(
            f"| {pr.get('root', 'n/a')} | {cos.get('verdict', 'n/a')} | "
            f"{_format_float(cos.get('color_diff_ratio'))} | "
            f"{_format_float(cos.get('shape_diff_ratio'))} | "
            f"{cos.get('reason', '')} |"
        )
    if cos_rows:
        out.append("## Color-only state distinction")
        out.append(
            "| Pair | Verdict | Color diff | Shape diff | Notes |"
        )
        out.append("| --- | --- | --- | --- | --- |")
        out.extend(cos_rows)
        out.append("")

    failures = [i for i in report["icons"] if i["verdict"] != "ok"]
    if failures:
        out.append("## Failures and warnings")
        for icon in failures:
            out.append(f"### {icon['name']} ({icon['verdict']})")
            for err in icon.get("errors", []):
                out.append(f"- error: {err}")
            for warn in icon.get("warnings", []):
                out.append(f"- warn: {warn}")
            out.append("")
    return "\n".join(out)


def write_reports(
    report: Dict[str, Any],
    md_path: Path | None,
    json_path: Path | None,
) -> Tuple[Path | None, Path | None]:
    md_out = json_out = None
    if md_path is not None:
        md_path = Path(md_path)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_markdown(report), encoding="utf-8")
        md_out = md_path
    if json_path is not None:
        json_path = Path(json_path)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(render_json(report), encoding="utf-8")
        json_out = json_path
    return md_out, json_out
