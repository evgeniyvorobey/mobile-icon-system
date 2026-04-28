#!/usr/bin/env python3
"""Render-and-grade pipeline for SVG icon sets.

Usage:
  python3 scripts/render_and_grade.py path/to/icons_dir [--config grade.toml]
                                      [--strict] [--lenient]
                                      [--report-md report.md] [--report-json report.json]
                                      [--reference-dir assets/references/tier-a]

Exit codes:
  0  every icon passes
  1  warnings only (or set-level warnings)
  2  at least one hard failure
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from grade import (  # noqa: E402
    alignment as alignment_mod,
    anti_example_similarity as anti_example_mod,
    color_only_state as color_only_state_mod,
    config as config_mod,
    pair as pair_mod,
    reference as reference_mod,
    report as report_mod,
    silhouette as silhouette_mod,
    squint as squint_mod,
    stroke as stroke_mod,
    weight as weight_mod,
)


# Default anti-example corpus location, resolved relative to repo root.
DEFAULT_ANTI_EXAMPLE_CORPUS = ROOT / "assets" / "references" / "tier-c"


def collect_svgs(target: Path) -> List[Path]:
    if target.is_file() and target.suffix.lower() == ".svg":
        return [target]
    if not target.is_dir():
        raise SystemExit(f"[FAIL] target is not an SVG file or directory: {target}")
    return sorted(p for p in target.rglob("*.svg") if p.is_file())


def _stem_root(name: str) -> Optional[str]:
    stem = Path(name).stem
    for suffix in ("_filled", "_outlined", "-filled", "-outlined"):
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return None


def _pair_partner_suffix(name: str) -> Optional[str]:
    stem = Path(name).stem
    for filled, outlined in (("_filled", "_outlined"), ("-filled", "-outlined")):
        if stem.endswith(filled):
            return outlined
        if stem.endswith(outlined):
            return filled
    return None


def grade_icon(
    path: Path,
    cfg: Dict[str, Any],
    *,
    anti_example_corpus: Optional[Path] = None,
) -> Dict[str, Any]:
    name = path.name
    checks: Dict[str, Any] = {
        "silhouette": silhouette_mod.measure_legibility(path, cfg),
        "weight": weight_mod.measure_weight(path, cfg),
        "alignment": alignment_mod.audit_alignment(path, cfg),
        "stroke": stroke_mod.measure_stroke(path, cfg),
        "squint": squint_mod.measure_squint(path, cfg),
    }
    if anti_example_corpus is not None and anti_example_corpus.is_dir():
        if anti_example_mod.is_available():
            try:
                checks["anti_example_similarity"] = (
                    anti_example_mod.check_anti_example_similarity(
                        path,
                        corpus_root=anti_example_corpus,
                        config=cfg,
                    )
                )
            except anti_example_mod.ReferenceUnavailable as exc:
                checks["anti_example_similarity"] = {
                    "passed": True,
                    "verdict": "ok",
                    "skipped": True,
                    "reason": str(exc),
                    "matches": [],
                    "errors": [],
                    "warnings": [f"anti_example_similarity: {exc}"],
                }
        else:
            checks["anti_example_similarity"] = {
                "passed": True,
                "verdict": "ok",
                "skipped": True,
                "reason": "imagehash not installed",
                "matches": [],
                "errors": [],
                "warnings": [
                    "anti_example_similarity: imagehash not installed; check skipped"
                ],
            }
    return report_mod.aggregate_icon(name, checks)


def grade_set_balance(
    paths: List[Path],
    icons: List[Dict[str, Any]],
    cfg: Dict[str, Any],
) -> Dict[str, Any]:
    ratios: List[float] = []
    labels: List[str] = []
    for path, icon in zip(paths, icons):
        wr = (icon.get("checks") or {}).get("weight", {}).get("weight_ratio")
        if wr is None:
            continue
        ratios.append(float(wr))
        labels.append(path.name)

    groups = weight_mod.stratify_pairs(labels)
    overall = weight_mod.measure_set_balance(ratios, labels, cfg)
    overall["passed"] = overall.get("passed", True)

    strata: Dict[str, Any] = {}
    for stratum in ("filled", "outlined"):
        idxs = groups.get(stratum, [])
        if len(idxs) >= 2:
            strata[stratum] = weight_mod.measure_set_balance(
                [ratios[i] for i in idxs],
                [labels[i] for i in idxs],
                cfg,
            )
    return {
        "overall": overall,
        "strata": strata,
        "passed": overall.get("passed", True)
        and all(s.get("passed", True) for s in strata.values()),
        "warnings": list(overall.get("warnings", [])),
        "errors": [],
    }


def grade_pairs(
    paths: List[Path],
    cfg: Dict[str, Any],
) -> Dict[str, Any]:
    by_root: Dict[str, Dict[str, Path]] = defaultdict(dict)
    for path in paths:
        root = _stem_root(path.name)
        if root is None:
            continue
        stem = path.stem
        if stem.endswith(("_filled", "-filled")):
            by_root[root]["filled"] = path
        elif stem.endswith(("_outlined", "-outlined")):
            by_root[root]["outlined"] = path

    results: List[Dict[str, Any]] = []
    overall_pass = True
    hard_fail_set = False
    warnings: List[str] = []
    for root, slots in sorted(by_root.items()):
        if "filled" not in slots or "outlined" not in slots:
            warnings.append(f"pair: '{root}' missing partner ({list(slots)})")
            continue
        res = pair_mod.measure_pair_distinction(slots["filled"], slots["outlined"], cfg)
        res["root"] = root
        res["filled"] = slots["filled"].name
        res["outlined"] = slots["outlined"].name
        # Color-only state distinction: hard-fail when the pair differs only
        # in color (selected/unselected indistinguishable in Forced Colors mode
        # or under deuteranopia).
        cos = color_only_state_mod.check_color_only_state(
            slots["filled"], slots["outlined"], config=cfg
        )
        res["color_only_state"] = cos
        if cos.get("hard_fail"):
            hard_fail_set = True
            overall_pass = False
            for w in cos.get("warnings", []) or []:
                warnings.append(f"{root}: {w}")
        if not res.get("passed", True):
            overall_pass = False
        results.append(res)
    return {
        "results": results,
        "passed": overall_pass,
        "hard_fail": hard_fail_set,
        "warnings": warnings,
        "errors": [],
    }


def grade_reference(
    paths: List[Path],
    reference_dir: Path,
    cfg: Dict[str, Any],
) -> Dict[str, Any]:
    if not reference_mod.is_available():
        return {
            "passed": True,
            "skipped": True,
            "reason": "imagehash not installed",
            "warnings": ["reference: imagehash not installed; skipped"],
            "errors": [],
            "results": [],
        }
    refs = sorted(reference_dir.rglob("*.svg"))
    if not refs:
        return {
            "passed": True,
            "skipped": True,
            "reason": f"no SVGs found under {reference_dir}",
            "warnings": [f"reference: no SVGs in {reference_dir}; skipped"],
            "errors": [],
            "results": [],
        }
    results: List[Dict[str, Any]] = []
    overall_pass = True
    for path in paths:
        try:
            res = reference_mod.compare_to_reference(path, refs, cfg)
        except reference_mod.ReferenceUnavailable as exc:
            return {
                "passed": True,
                "skipped": True,
                "reason": str(exc),
                "warnings": [f"reference: {exc}"],
                "errors": [],
                "results": [],
            }
        res["icon"] = path.name
        if not res.get("passed", True):
            overall_pass = False
        results.append(res)
    return {
        "results": results,
        "passed": overall_pass,
        "skipped": False,
        "warnings": [],
        "errors": [],
    }


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render and grade an SVG icon set.")
    parser.add_argument("target", type=Path, help="SVG file or directory of SVGs")
    parser.add_argument("--config", type=Path, default=None, help="TOML config override")
    parser.add_argument("--strict", action="store_true", help="Tighten thresholds")
    parser.add_argument("--lenient", action="store_true", help="Loosen thresholds")
    parser.add_argument("--report-md", type=Path, default=None)
    parser.add_argument("--report-json", type=Path, default=None)
    parser.add_argument(
        "--reference-dir",
        type=Path,
        default=None,
        help="Directory of reference SVGs (perceptual-hash comparison)",
    )
    parser.add_argument(
        "--anti-example-corpus",
        type=Path,
        default=None,
        help=(
            "Directory of tier-C anti-example SVGs. "
            "Defaults to assets/references/tier-c/ when present. "
            "Pass an explicit path to override or to add custom anti-examples. "
            "Pass 'none' to disable the check."
        ),
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    cfg = config_mod.load_config(args.config)
    cfg = config_mod.apply_strictness(cfg, strict=args.strict, lenient=args.lenient)

    svgs = collect_svgs(args.target)
    if not svgs:
        print(f"[WARN] no SVGs found under {args.target}", file=sys.stderr)
        report = {
            "icons": [],
            "set_checks": {},
            "set_warnings": ["no SVGs found"],
            "set_errors": [],
            "summary": {"n_icons": 0, "ok": 0, "warn": 1, "hard_fail": 0},
            "verdict": "warn",
        }
        report_mod.write_reports(report, args.report_md, args.report_json)
        return 1

    # Resolve the anti-example corpus path. Explicit "none" disables the
    # check; an explicit path overrides; otherwise default to the in-repo
    # tier-C corpus when present (graceful skip if the directory is missing).
    if args.anti_example_corpus is None:
        anti_corpus: Optional[Path] = (
            DEFAULT_ANTI_EXAMPLE_CORPUS
            if DEFAULT_ANTI_EXAMPLE_CORPUS.is_dir()
            else None
        )
    elif str(args.anti_example_corpus).strip().lower() == "none":
        anti_corpus = None
    else:
        anti_corpus = args.anti_example_corpus

    icons = [grade_icon(p, cfg, anti_example_corpus=anti_corpus) for p in svgs]
    set_checks: Dict[str, Any] = {
        "balance": grade_set_balance(svgs, icons, cfg),
        "pair": grade_pairs(svgs, cfg),
    }
    if args.reference_dir is not None:
        set_checks["reference"] = grade_reference(svgs, args.reference_dir, cfg)

    report = report_mod.aggregate_set(icons, set_checks)
    report_mod.write_reports(report, args.report_md, args.report_json)

    print(report_mod.render_markdown(report))

    if report["verdict"] == "hard_fail":
        return 2
    if report["verdict"] == "warn":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
