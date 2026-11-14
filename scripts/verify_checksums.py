#!/usr/bin/env python3
"""Verify SHA-256 checksums for the frozen research inputs.

Usage:
    python scripts/verify_checksums.py
    python scripts/verify_checksums.py --write

Exit code 0 means every covered file matches. Exit code 1 means at least one
file is missing or changed.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKSUM_FILE = ROOT / "reproducibility" / "checksums.sha256"

COVERED_FILES = [
    "PROTOCOL.md",
    "rubric_v1.1.md",
    "data/citation_frame_2666.csv",
    "data/frame_summary.json",
    "data/cohort_feasibility.csv",
    "data/cohort_feasibility.manifest.json",
    "pilot/pilot_coding_table.csv",
    "pilot/pilot_summary.md",
    "pilot/rubric_v1_to_v1.1.md",
    "manuscript/abstract.md",
    "manuscript/paper.md",
    "manuscript/references.bib",
    "manuscript/tables/table1_benchmark_pairs.md",
    "manuscript/tables/table2_frame_profile.md",
    "manuscript/tables/table3_pilot_flow.md",
    "manuscript/tables/table4_pilot_scores.md",
    "manuscript/tables/table5_pair_specific.md",
    "manuscript/tables/table6_coded_cases.md",
    "manuscript/tables/table1_benchmark_pairs.csv",
    "manuscript/tables/table2_frame_profile.csv",
    "manuscript/tables/table3_pilot_flow.csv",
    "manuscript/tables/table4_pilot_scores.csv",
    "manuscript/tables/table5_pair_specific.csv",
    "manuscript/tables/table6_coded_cases.csv",
    "manuscript/figures/fig1_frame_years.csv",
    "manuscript/figures/fig2_pilot_flow.csv",
    "manuscript/figures/fig3_pilot_scores.csv",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_checksums(root: Path = ROOT) -> dict[str, str]:
    result: dict[str, str] = {}
    for relative in COVERED_FILES:
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(f"covered file missing: {relative}")
        result[relative] = sha256_file(path)
    return result


def format_checksums(checksums: dict[str, str]) -> str:
    return "".join(
        f"{digest}  {relative}\n" for relative, digest in sorted(checksums.items())
    )


def parse_checksums(text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            raise ValueError(f"malformed checksum line: {line!r}")
        digest, relative = parts
        parsed[relative.replace("\\", "/")] = digest.lower()
    return parsed


def write_checksums(root: Path = ROOT, target: Path = CHECKSUM_FILE) -> int:
    checksums = build_checksums(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(format_checksums(checksums), encoding="utf-8", newline="\n")
    print(f"Wrote {len(checksums)} checksums to {target.relative_to(root)}")
    return 0


def verify(root: Path = ROOT, target: Path = CHECKSUM_FILE) -> int:
    if not target.is_file():
        print(f"MISSING  {target.relative_to(root)}")
        return 1
    expected = parse_checksums(target.read_text(encoding="utf-8"))
    failures = 0
    for relative in sorted(set(expected) | set(COVERED_FILES)):
        path = root / relative
        if relative not in expected:
            print(f"UNLISTED  {relative}")
            failures += 1
            continue
        if relative not in COVERED_FILES:
            print(f"EXTRA     {relative}")
            failures += 1
            continue
        if not path.is_file():
            print(f"MISSING   {relative}")
            failures += 1
            continue
        actual = sha256_file(path)
        if actual == expected[relative]:
            print(f"OK        {relative}")
        else:
            print(f"FAIL      {relative}")
            print(f"          expected {expected[relative]}")
            print(f"          actual   {actual}")
            failures += 1
    print(f"\n{len(COVERED_FILES) - failures}/{len(COVERED_FILES)} files verified")
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="rewrite reproducibility/checksums.sha256 from current files",
    )
    args = parser.parse_args(argv)
    if args.write:
        return write_checksums()
    return verify()


if __name__ == "__main__":
    sys.exit(main())
