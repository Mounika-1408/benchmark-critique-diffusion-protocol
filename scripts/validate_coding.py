"""Validate a pilot coding CSV without modifying it."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from pathlib import Path
import sys


COLUMNS = (
    "paper_key", "title", "venue", "year", "critique", "eligible",
    "ineligibility_reason", "score", "engagement", "independent_remediation",
    "evidence_quote", "notes",
)
CRITIQUES = {"evalplus", "swebenchplus", "gsm1k"}
BOOLEANS = {"true", "false"}
Violation = tuple[int, str, str]


def validate_coding(path: Path) -> list[Violation]:
    """Return violations as (CSV row number, column, message) tuples."""
    errors: list[Violation] = []
    seen: dict[tuple[str, str], int] = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, strict=True)
        try:
            header = next(reader, [])
            for column in COLUMNS:
                if column not in header:
                    errors.append((1, column, "missing required column"))
            for column, count in Counter(header).items():
                if count > 1:
                    errors.append((1, column, "duplicate column"))
            if errors:
                return errors

            for number, values in enumerate(reader, start=2):
                if len(values) != len(header):
                    errors.append((number, "CSV", f"expected {len(header)} fields, got {len(values)}"))
                    continue
                row = dict(zip(header, values))
                errors.extend(_validate_row(number, row))
                key = (row["paper_key"], row["critique"])
                if key in seen:
                    errors.append((number, "paper_key", f"duplicates the paper_key + critique pair on row {seen[key]}"))
                else:
                    seen[key] = number
        except csv.Error as error:
            errors.append((reader.line_num, "CSV", str(error)))
    return errors


def _validate_row(number: int, row: dict[str, str]) -> list[Violation]:
    errors: list[Violation] = []
    for column in ("paper_key", "title"):
        if not row[column].strip():
            errors.append((number, column, "must not be blank"))
    if row["year"] != "unknown" and not (row["year"].isascii() and row["year"].isdecimal()):
        errors.append((number, "year", "must be an integer or unknown"))
    if row["critique"] not in CRITIQUES:
        errors.append((number, "critique", "must be evalplus, swebenchplus or gsm1k"))

    eligible = row["eligible"]
    if eligible not in BOOLEANS:
        errors.append((number, "eligible", "must be true or false"))
    elif eligible == "true" and row["score"] not in {"0", "1", "2", "3"}:
        errors.append((number, "score", "must be 0–3 for an eligible row"))
    elif eligible == "false" and row["score"]:
        errors.append((number, "score", "must be blank for an ineligible row"))

    if row["engagement"] not in {"0", "1", "2"}:
        errors.append((number, "engagement", "must be 0–2"))
    if row["independent_remediation"] not in BOOLEANS:
        errors.append((number, "independent_remediation", "must be true or false"))
    if eligible == "true" and row["ineligibility_reason"]:
        errors.append((number, "ineligibility_reason", "must be blank for an eligible row"))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    try:
        errors = validate_coding(args.csv_path)
    except (OSError, UnicodeError) as error:
        parser.exit(2, f"{args.csv_path}: {error}\n")
    for number, column, message in errors:
        print(f"{args.csv_path}: row {number}, {column}: {message}", file=sys.stderr)
    if errors:
        return 1
    print(f"{args.csv_path}: coding schema valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
