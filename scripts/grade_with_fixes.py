#!/usr/bin/env python3
"""Grade an icon set and emit a per-icon regeneration brief.

This is the "self-correcting" wrapper around ``render_and_grade.py``: it runs
the same grader, then for every icon with verdict ``warn`` or ``hard_fail``
generates a Markdown fix prompt the LLM can read and act on. The brief is
written to ``--brief-out`` (default ``regeneration_brief.md`` in the cwd).

Usage:
  python3 scripts/grade_with_fixes.py path/to/icons_dir
                                       [--config grade.toml]
                                       [--strict]
                                       [--brief-out regeneration_brief.md]
                                       [--max-iterations 2]
                                       [--reference-corpus assets/references/tier-a/]

Exit codes:
  0  every icon passes
  1  warnings only
  2  at least one hard failure
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from grade import config as config_mod  # noqa: E402
from grade import fix_brief as fix_brief_mod  # noqa: E402
from grade import report as report_mod  # noqa: E402
from render_and_grade import (  # noqa: E402
    collect_svgs,
    grade_icon,
    grade_pairs,
    grade_set_balance,
)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Grade an SVG icon set and emit a per-icon regeneration brief."
    )
    parser.add_argument("target", type=Path, help="SVG file or directory of SVGs")
    parser.add_argument("--config", type=Path, default=None, help="TOML config override")
    parser.add_argument("--strict", action="store_true", help="Tighten thresholds")
    parser.add_argument(
        "--brief-out",
        type=Path,
        default=Path("regeneration_brief.md"),
        help="Where to write the per-icon regeneration brief (default: ./regeneration_brief.md)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=2,
        help="Cap recommended to the LLM on regeneration loops per icon (default: 2)",
    )
    parser.add_argument(
        "--reference-corpus",
        type=Path,
        default=ROOT / "assets" / "references" / "tier-a",
        help="Directory of tier-A reference SVGs + .notes.md files",
    )
    parser.add_argument(
        "--report-md",
        type=Path,
        default=None,
        help="Optional grading report (Markdown) — same as render_and_grade.py",
    )
    parser.add_argument(
        "--report-json",
        type=Path,
        default=None,
        help="Optional grading report (JSON) — same as render_and_grade.py",
    )
    return parser.parse_args(argv)


def _build_brief(
    report: Dict[str, Any],
    *,
    target_dir: Path,
    corpus_root: Optional[Path],
    max_iterations: int,
) -> str:
    """Render the aggregate regeneration brief Markdown."""
    needs_fix = [
        icon for icon in report["icons"] if icon.get("verdict") in ("hard_fail", "warn")
    ]
    out: List[str] = []
    out.append("# Regeneration brief")
    out.append("")
    summary = report.get("summary", {})
    out.append(
        f"Overall verdict: **{report.get('verdict', 'unknown')}** "
        f"(ok={summary.get('ok', 0)}, warn={summary.get('warn', 0)}, "
        f"hard_fail={summary.get('hard_fail', 0)})."
    )
    out.append("")
    if not needs_fix:
        out.append(
            "No icons need regeneration — every icon graded `ok`. "
            "Treat this brief as empty."
        )
        out.append("")
        return "\n".join(out)

    out.append(
        f"{len(needs_fix)} icon(s) need regeneration. For each one below: "
        "address every numbered fix, preserve the metaphor, and re-output the "
        "SVG. After regenerating, re-run the grader (instructions at the end "
        "of this brief)."
    )
    out.append("")
    out.append("## Icons needing regeneration")
    out.append("")
    for icon in needs_fix:
        warns = ", ".join(sorted({w.split(":", 1)[0] for w in icon.get("warnings", [])}))
        errs = ", ".join(sorted({e.split(":", 1)[0] for e in icon.get("errors", [])}))
        bits = []
        if errs:
            bits.append(f"errors in: {errs}")
        if warns:
            bits.append(f"warns in: {warns}")
        detail = "; ".join(bits) if bits else "(see below)"
        out.append(f"- `{icon['name']}` — verdict `{icon['verdict']}` ({detail})")
    out.append("")

    out.append("## Per-icon fix prompts")
    out.append("")
    for icon in needs_fix:
        out.append(
            fix_brief_mod.render_fix_brief(
                icon,
                corpus_root=corpus_root,
                source_dir=target_dir,
            )
        )

    out.append("## How to verify the fix")
    out.append("")
    out.append(
        f"After regenerating the icon(s) above, re-run "
        f"`python3 scripts/grade_with_fixes.py {target_dir}` and confirm:"
    )
    out.append("")
    out.append(
        "1. Every previously-failing icon's verdict has improved "
        "(`hard_fail` → `warn`/`ok`, or `warn` → `ok`)."
    )
    out.append("2. No previously-passing icon has regressed.")
    out.append("3. Set-level checks (balance, pair distinction) still pass.")
    out.append("")
    out.append(
        f"Cap regeneration at **{max_iterations}** iterations per icon. If an "
        "icon still fails after this many passes, surface it as an unresolved "
        "item in workflow phase 12 (Improve or question) rather than looping "
        "indefinitely."
    )
    out.append("")
    return "\n".join(out)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    cfg = config_mod.load_config(args.config)
    cfg = config_mod.apply_strictness(cfg, strict=args.strict, lenient=False)

    svgs = collect_svgs(args.target)
    target_dir = args.target if args.target.is_dir() else args.target.parent

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
        brief_text = _build_brief(
            report,
            target_dir=target_dir,
            corpus_root=args.reference_corpus,
            max_iterations=args.max_iterations,
        )
        args.brief_out.parent.mkdir(parents=True, exist_ok=True)
        args.brief_out.write_text(brief_text, encoding="utf-8")
        return 1

    icons = [grade_icon(p, cfg) for p in svgs]
    set_checks: Dict[str, Any] = {
        "balance": grade_set_balance(svgs, icons, cfg),
        "pair": grade_pairs(svgs, cfg),
    }
    report = report_mod.aggregate_set(icons, set_checks)
    report_mod.write_reports(report, args.report_md, args.report_json)

    brief_text = _build_brief(
        report,
        target_dir=target_dir,
        corpus_root=args.reference_corpus,
        max_iterations=args.max_iterations,
    )
    args.brief_out.parent.mkdir(parents=True, exist_ok=True)
    args.brief_out.write_text(brief_text, encoding="utf-8")

    print(report_mod.render_markdown(report))
    print()
    print(f"[brief] wrote {args.brief_out}")

    if report["verdict"] == "hard_fail":
        return 2
    if report["verdict"] == "warn":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
