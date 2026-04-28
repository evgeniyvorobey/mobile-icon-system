#!/usr/bin/env python3
"""Compare rendered PNG review snapshots for visual regressions."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from PIL import Image


def collect_pngs(root: Path) -> dict[str, Path]:
    return {
        str(path.relative_to(root)): path
        for path in sorted(root.rglob("*.png"))
        if path.is_file()
    }


def load_rgba(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        return np.asarray(image.convert("RGBA"), dtype=np.int16)


def compare_pair(
    baseline: Path,
    current: Path,
    *,
    max_channel_delta: int,
) -> dict[str, Any]:
    base = load_rgba(baseline)
    cur = load_rgba(current)
    if base.shape != cur.shape:
        return {
            "passed": False,
            "reason": "dimension-mismatch",
            "baseline_shape": list(base.shape),
            "current_shape": list(cur.shape),
            "diff_ratio": 1.0,
            "max_delta": None,
        }

    delta = np.abs(base - cur)
    per_pixel = delta.max(axis=2)
    changed = per_pixel > int(max_channel_delta)
    changed_px = int(changed.sum())
    total_px = int(changed.size)
    max_delta = int(delta.max()) if delta.size else 0
    return {
        "passed": True,
        "reason": "compared",
        "baseline_shape": list(base.shape),
        "current_shape": list(cur.shape),
        "changed_px": changed_px,
        "total_px": total_px,
        "diff_ratio": float(changed_px) / float(max(total_px, 1)),
        "max_delta": max_delta,
    }


def compare_dirs(
    baseline_dir: Path,
    current_dir: Path,
    *,
    max_diff_ratio: float,
    max_channel_delta: int,
) -> dict[str, Any]:
    baseline_pngs = collect_pngs(baseline_dir)
    current_pngs = collect_pngs(current_dir)
    results: list[dict[str, Any]] = []
    passed = True

    for rel, baseline_path in baseline_pngs.items():
        current_path = current_pngs.get(rel)
        if current_path is None:
            results.append(
                {
                    "file": rel,
                    "passed": False,
                    "reason": "missing-current",
                    "diff_ratio": 1.0,
                }
            )
            passed = False
            continue
        result = compare_pair(
            baseline_path,
            current_path,
            max_channel_delta=max_channel_delta,
        )
        result["file"] = rel
        if result["diff_ratio"] > max_diff_ratio or result["reason"] != "compared":
            result["passed"] = False
            passed = False
        results.append(result)

    extra_current = sorted(set(current_pngs) - set(baseline_pngs))
    for rel in extra_current:
        results.append(
            {
                "file": rel,
                "passed": False,
                "reason": "extra-current",
                "diff_ratio": 1.0,
            }
        )
        passed = False

    return {
        "passed": passed,
        "baseline_dir": str(baseline_dir),
        "current_dir": str(current_dir),
        "max_diff_ratio": max_diff_ratio,
        "max_channel_delta": max_channel_delta,
        "results": sorted(results, key=lambda item: item["file"]),
    }


def update_baseline(baseline_dir: Path, current_dir: Path) -> None:
    if baseline_dir.exists():
        shutil.rmtree(baseline_dir)
    shutil.copytree(current_dir, baseline_dir)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare PNG contact-sheet snapshots against a baseline."
    )
    parser.add_argument("baseline_dir", type=Path)
    parser.add_argument("current_dir", type=Path)
    parser.add_argument("--max-diff-ratio", type=float, default=0.003)
    parser.add_argument("--max-channel-delta", type=int, default=24)
    parser.add_argument("--report-json", type=Path, default=None)
    parser.add_argument(
        "--update-baseline",
        action="store_true",
        help="Replace baseline_dir with current_dir after comparison.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    if not args.baseline_dir.is_dir():
        print(f"[FAIL] baseline directory not found: {args.baseline_dir}", file=sys.stderr)
        return 1
    if not args.current_dir.is_dir():
        print(f"[FAIL] current directory not found: {args.current_dir}", file=sys.stderr)
        return 1

    report = compare_dirs(
        args.baseline_dir,
        args.current_dir,
        max_diff_ratio=args.max_diff_ratio,
        max_channel_delta=args.max_channel_delta,
    )
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.report_json:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(text + "\n", encoding="utf-8")
    print(text)

    if report["passed"] and args.update_baseline:
        update_baseline(args.baseline_dir, args.current_dir)

    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
