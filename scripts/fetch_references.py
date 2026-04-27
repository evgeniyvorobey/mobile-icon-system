#!/usr/bin/env python3
"""
fetch_references.py — populate the icon calibration corpus.

Downloads the upstream SVG references used by the mobile-icon-system skill's
phase-7 (variant generation) and phase-9 (hi-end craft pass) calibration loop.

Pure stdlib. No third-party dependencies. Works on Python 3.8+.

Usage:
    python3 scripts/fetch_references.py            # fetch any missing files
    python3 scripts/fetch_references.py --update   # force re-fetch all
    python3 scripts/fetch_references.py --dry-run  # show what would be fetched
    python3 scripts/fetch_references.py --verify   # verify existing SHA256s

The script writes a manifest at assets/references/manifest.json so subsequent
runs can verify integrity without re-fetching.

License posture:
  All upstream URLs in CORPUS were verified to be ISC, MIT, or Apache-2.0 at
  the time the corpus was assembled. Per-source attributions live in
  assets/references/ATTRIBUTIONS.md. Custom files (the three tier-C
  hand-crafted anti-examples) are MIT-licensed under this repo's LICENSE.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# Repo paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
REFERENCES_DIR = REPO_ROOT / "assets" / "references"
MANIFEST_PATH = REFERENCES_DIR / "manifest.json"

# ---------------------------------------------------------------------------
# Corpus definition (verified live 2026-04-27)
# ---------------------------------------------------------------------------
# Each entry: (relative dest path, upstream URL, license short id, source label)
# License ids: "ISC" (Lucide), "MIT" (Phosphor, Tabler, Heroicons),
# "Apache-2.0" (Material Symbols).

CORPUS: list[tuple[str, str, str, str]] = [
    # Tier A — exemplar craft references
    ("tier-a/home-outlined.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/house.svg",
     "ISC", "Lucide"),
    ("tier-a/home-filled.svg",
     "https://raw.githubusercontent.com/phosphor-icons/core/main/raw/fill/house-fill.svg",
     "MIT", "Phosphor"),
    ("tier-a/search.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/search.svg",
     "ISC", "Lucide"),
    ("tier-a/user.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/user.svg",
     "ISC", "Lucide"),
    ("tier-a/settings.svg",
     "https://raw.githubusercontent.com/tabler/tabler-icons/main/icons/outline/settings.svg",
     "MIT", "Tabler Icons"),
    ("tier-a/bell.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/bell.svg",
     "ISC", "Lucide"),
    ("tier-a/plus.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/plus.svg",
     "ISC", "Lucide"),
    ("tier-a/heart-outlined.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/heart.svg",
     "ISC", "Lucide"),
    ("tier-a/heart-filled.svg",
     "https://raw.githubusercontent.com/phosphor-icons/core/main/raw/fill/heart-fill.svg",
     "MIT", "Phosphor"),
    ("tier-a/camera.svg",
     "https://raw.githubusercontent.com/phosphor-icons/core/main/raw/regular/camera.svg",
     "MIT", "Phosphor"),
    ("tier-a/calendar.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/calendar.svg",
     "ISC", "Lucide"),
    ("tier-a/chat.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/message-circle.svg",
     "ISC", "Lucide"),
    ("tier-a/share.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/share.svg",
     "ISC", "Lucide"),
    ("tier-a/trash.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/trash-2.svg",
     "ISC", "Lucide"),
    ("tier-a/check.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/check.svg",
     "ISC", "Lucide"),
    ("tier-a/x.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/x.svg",
     "ISC", "Lucide"),

    # Tier B — competent but missing a tier-A craft trait
    ("tier-b/home-outlined.svg",
     "https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/home.svg",
     "MIT", "Heroicons"),
    ("tier-b/search.svg",
     "https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/magnifying-glass.svg",
     "MIT", "Heroicons"),
    ("tier-b/settings-bezier.svg",
     "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/settings.svg",
     "ISC", "Lucide"),
    ("tier-b/heart-symmetric.svg",
     "https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/heart.svg",
     "MIT", "Heroicons"),
    ("tier-b/share-graph.svg",
     "https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/share.svg",
     "MIT", "Heroicons"),
    ("tier-b/camera-decorative.svg",
     "https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/camera.svg",
     "MIT", "Heroicons"),

    # Tier C — anti-examples (upstream sources)
    ("tier-c/calendar-overdetailed.svg",
     "https://raw.githubusercontent.com/phosphor-icons/core/main/raw/regular/calendar.svg",
     "MIT", "Phosphor"),
    ("tier-c/settings-12tooth.svg",
     "https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/settings/materialsymbolsoutlined/settings_24px.svg",
     "Apache-2.0", "Material Symbols"),
]

# Sentinel for "this file is hand-authored in this repo, do not fetch."
CUSTOM_FILES: list[str] = [
    "tier-c/home-overdetailed.svg",
    "tier-c/user-gendered.svg",
    "tier-c/notification-color-state.svg",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

USER_AGENT = "mobile-icon-system fetch_references/1.0 (+https://github.com/)"


def fetch(url: str, timeout: float = 30.0) -> bytes:
    """Fetch URL and return raw bytes; raise on non-200 or any URL error."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} for {url}")
        return resp.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_svg_payload(data: bytes) -> bool:
    """Loose check that the payload is SVG/XML.

    Some upstream sources (e.g. Tabler) prefix their SVGs with an HTML comment
    block of metadata (`<!-- tags: ... -->`) before the `<svg>` element.
    Accept any payload that starts with `<svg`, `<?xml`, or `<!--` AND
    contains a `<svg` element somewhere in its first 4 KB.
    """
    head = data.lstrip()[:6].lower()
    if head.startswith(b"<svg") or head.startswith(b"<?xml"):
        return True
    if head.startswith(b"<!--") and b"<svg" in data[:4096].lower():
        return True
    return False


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        try:
            return json.loads(MANIFEST_PATH.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_manifest(manifest: dict) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def iter_corpus() -> Iterable[tuple[str, str, str, str]]:
    yield from CORPUS


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_fetch(force: bool, dry_run: bool) -> int:
    manifest = load_manifest()
    manifest.setdefault("generated", None)
    manifest.setdefault("entries", {})
    manifest.setdefault("custom_files", CUSTOM_FILES)

    failures: list[tuple[str, str]] = []
    fetched = 0
    skipped = 0

    for rel_path, url, license_id, source in iter_corpus():
        dest = REFERENCES_DIR / rel_path
        existing = manifest["entries"].get(rel_path)

        if dest.exists() and existing and not force:
            print(f"  skip   {rel_path}  (already present, sha256 known)")
            skipped += 1
            continue

        if dry_run:
            print(f"  WOULD  {rel_path}  <-  {url}")
            continue

        print(f"  fetch  {rel_path}  <-  {url}")
        try:
            data = fetch(url)
        except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as exc:
            print(f"    FAILED: {exc}")
            failures.append((rel_path, str(exc)))
            continue

        if not data:
            failures.append((rel_path, "empty payload"))
            continue
        if not is_svg_payload(data):
            failures.append((rel_path, f"not an SVG (head={data[:32]!r})"))
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        manifest["entries"][rel_path] = {
            "url": url,
            "license": license_id,
            "source": source,
            "sha256": sha256_bytes(data),
            "bytes": len(data),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }
        fetched += 1

    if not dry_run:
        manifest["generated"] = datetime.now(timezone.utc).isoformat()
        save_manifest(manifest)

    print()
    print(f"Done. fetched={fetched} skipped={skipped} failed={len(failures)}")
    if failures:
        print()
        print("Failures:")
        for rel, msg in failures:
            print(f"  {rel}: {msg}")
        return 1
    return 0


def cmd_verify() -> int:
    manifest = load_manifest()
    if not manifest.get("entries"):
        print("No manifest found; run --update first.")
        return 1

    bad: list[str] = []
    missing: list[str] = []
    for rel_path, meta in manifest["entries"].items():
        dest = REFERENCES_DIR / rel_path
        if not dest.exists():
            missing.append(rel_path)
            continue
        actual = sha256_bytes(dest.read_bytes())
        if actual != meta.get("sha256"):
            bad.append(f"{rel_path} (manifest={meta.get('sha256')[:12]}… actual={actual[:12]}…)")

    print(f"verified {len(manifest['entries']) - len(bad) - len(missing)} ok, "
          f"{len(bad)} mismatched, {len(missing)} missing")
    for rel in missing:
        print(f"  MISSING  {rel}")
    for line in bad:
        print(f"  BAD      {line}")
    return 0 if not (bad or missing) else 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch the mobile-icon-system reference corpus."
    )
    parser.add_argument(
        "--update", action="store_true",
        help="Force re-fetch every entry, even if it already exists locally."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be fetched but make no changes."
    )
    parser.add_argument(
        "--verify", action="store_true",
        help="Verify SHA256 of every file in the manifest; do not fetch."
    )
    args = parser.parse_args(argv)

    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)

    if args.verify:
        return cmd_verify()
    return cmd_fetch(force=args.update, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
