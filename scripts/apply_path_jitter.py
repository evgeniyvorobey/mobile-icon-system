#!/usr/bin/env python3
"""Apply deterministic, bounded coordinate jitter to SVG path data."""
from __future__ import annotations

import argparse
import math
import random
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable, List, Optional, Sequence


_PATH_TAG_RE = re.compile(r"<path\b[^>]*>", re.IGNORECASE | re.DOTALL)
_D_ATTR_RE = re.compile(r"(\bd\s*=\s*)([\"'])(.*?)(\2)", re.IGNORECASE | re.DOTALL)
_PATH_TOKEN_RE = re.compile(
    r"[AaCcHhLlMmQqSsTtVvZz]|[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?"
)
_COMMAND_ARITY = {
    "M": 2,
    "L": 2,
    "H": 1,
    "V": 1,
    "C": 6,
    "S": 4,
    "Q": 4,
    "T": 2,
    "A": 7,
    "Z": 0,
}
_COORD_PARAM_INDEXES = {
    "M": frozenset((0, 1)),
    "L": frozenset((0, 1)),
    "H": frozenset((0,)),
    "V": frozenset((0,)),
    "C": frozenset((0, 1, 2, 3, 4, 5)),
    "S": frozenset((0, 1, 2, 3)),
    "Q": frozenset((0, 1, 2, 3)),
    "T": frozenset((0, 1)),
    # For arcs, keep radii, rotation, and flags stable; only jitter the endpoint.
    "A": frozenset((5, 6)),
    "Z": frozenset(),
}


class PathJitterError(ValueError):
    """Raised when path jitter input is invalid."""


def _is_command(token: str) -> bool:
    return len(token) == 1 and token.isalpha()


def _format_number(value: float) -> str:
    if math.isclose(value, 0.0, abs_tol=1e-12):
        value = 0.0
    text = f"{value:.6f}".rstrip("0").rstrip(".")
    return text if text else "0"


def _snap_candidates(value: float, amplitude: float, snap: float) -> List[float]:
    low = value - amplitude
    high = value + amplitude
    first = math.ceil((low - 1e-12) / snap)
    last = math.floor((high + 1e-12) / snap)
    return [index * snap for index in range(first, last + 1)]


def _jitter_number(
    value: float,
    *,
    rng: random.Random,
    amplitude: float,
    snap: Optional[float],
) -> float:
    if amplitude == 0:
        return value
    if snap is not None:
        candidates = _snap_candidates(value, amplitude, snap)
        if not candidates:
            return value
        return float(rng.choice(candidates))
    return value + rng.uniform(-amplitude, amplitude)


def jitter_path_data(
    path_data: str,
    *,
    rng: random.Random,
    amplitude: float,
    snap: Optional[float] = None,
) -> str:
    """Return path data with deterministic coordinate jitter applied.

    Numeric arc flags are preserved, and arc jitter is limited to endpoint
    coordinates. When ``amplitude`` is zero, the original path data is returned
    byte-for-byte.
    """
    if amplitude < 0:
        raise PathJitterError("amplitude must be >= 0")
    if snap is not None and snap <= 0:
        raise PathJitterError("snap increment must be > 0")
    if amplitude == 0:
        return path_data

    token_matches = list(_PATH_TOKEN_RE.finditer(path_data))
    if not token_matches:
        return path_data

    output: List[str] = []
    command: Optional[str] = None
    param_index = 0
    last_end = 0

    for match in token_matches:
        token = match.group(0)
        output.append(path_data[last_end : match.start()])
        if _is_command(token):
            upper = token.upper()
            if upper not in _COMMAND_ARITY:
                raise PathJitterError(f"unsupported SVG path command: {token}")
            command = token
            param_index = 0
            output.append(token)
            last_end = match.end()
            continue

        if command is None:
            raise PathJitterError("path data starts with a number before a command")
        upper = command.upper()
        arity = _COMMAND_ARITY[upper]
        if arity == 0:
            raise PathJitterError(f"command {command} cannot accept numeric parameters")

        value = float(token)
        if param_index in _COORD_PARAM_INDEXES[upper]:
            value = _jitter_number(value, rng=rng, amplitude=amplitude, snap=snap)
            output.append(_format_number(value))
        else:
            output.append(token)
        param_index = (param_index + 1) % arity
        last_end = match.end()

    output.append(path_data[last_end:])
    return "".join(output)


def _validate_svg(svg_text: str) -> None:
    try:
        ET.fromstring(svg_text)
    except ET.ParseError as exc:
        raise PathJitterError(f"jittered SVG is not valid XML: {exc}") from exc


def jitter_svg_paths(
    svg_text: str,
    *,
    seed: int,
    amplitude: float,
    snap: Optional[float] = None,
    validate: bool = True,
) -> str:
    """Jitter numeric coordinate data in all SVG ``<path d="...">`` attributes."""
    if amplitude < 0:
        raise PathJitterError("amplitude must be >= 0")
    if snap is not None and snap <= 0:
        raise PathJitterError("snap increment must be > 0")
    if amplitude == 0:
        return svg_text

    rng = random.Random(seed)

    def replace_tag(match: re.Match[str]) -> str:
        tag = match.group(0)

        def replace_d(attr_match: re.Match[str]) -> str:
            prefix = attr_match.group(1)
            quote = attr_match.group(2)
            path_data = attr_match.group(3)
            new_path_data = jitter_path_data(
                path_data,
                rng=rng,
                amplitude=amplitude,
                snap=snap,
            )
            return f"{prefix}{quote}{new_path_data}{quote}"

        return _D_ATTR_RE.sub(replace_d, tag, count=1)

    jittered = _PATH_TAG_RE.sub(replace_tag, svg_text)
    if validate:
        _validate_svg(jittered)
    return jittered


def apply_path_jitter_to_file(
    input_path: Path,
    *,
    seed: int,
    amplitude: float,
    output_path: Optional[Path] = None,
    in_place: bool = False,
    dry_run: bool = False,
    snap: Optional[float] = None,
) -> str:
    """Apply jitter to a file and return the would-be output text."""
    if output_path is not None and in_place:
        raise PathJitterError("use either output_path or in_place, not both")

    svg_text = input_path.read_text(encoding="utf-8")
    jittered = jitter_svg_paths(svg_text, seed=seed, amplitude=amplitude, snap=snap)

    if not dry_run:
        if in_place:
            input_path.write_text(jittered, encoding="utf-8")
        elif output_path is not None:
            output_path.write_text(jittered, encoding="utf-8")
    return jittered


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply deterministic bounded jitter to SVG path coordinates."
    )
    parser.add_argument("svg", type=Path, help="input SVG file")
    parser.add_argument("--seed", type=int, required=True, help="deterministic RNG seed")
    parser.add_argument(
        "--amplitude",
        type=float,
        required=True,
        help="maximum coordinate displacement before optional snapping",
    )
    parser.add_argument(
        "--snap",
        type=float,
        default=None,
        help="optional coordinate snap increment, e.g. 0.5",
    )
    parser.add_argument("-o", "--output", type=Path, default=None, help="output SVG path")
    parser.add_argument("--in-place", action="store_true", help="rewrite the input SVG")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the jittered SVG to stdout without writing files",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    try:
        jittered = apply_path_jitter_to_file(
            args.svg,
            seed=args.seed,
            amplitude=args.amplitude,
            output_path=args.output,
            in_place=args.in_place,
            dry_run=args.dry_run or (args.output is None and not args.in_place),
            snap=args.snap,
        )
    except PathJitterError as exc:
        parser.error(str(exc))
        return 2

    if args.dry_run or (args.output is None and not args.in_place):
        sys.stdout.write(jittered)
        if jittered and not jittered.endswith("\n"):
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
