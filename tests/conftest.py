from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


@pytest.fixture(scope="session")
def root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def frame_rows(root: Path) -> list[dict[str, str]]:
    with (root / "data" / "citation_frame_2666.csv").open(
        encoding="utf-8-sig", newline=""
    ) as handle:
        return list(csv.DictReader(handle))


@pytest.fixture(scope="session")
def pilot_rows(root: Path) -> list[dict[str, str]]:
    with (root / "pilot" / "pilot_coding_table.csv").open(
        encoding="utf-8-sig", newline=""
    ) as handle:
        return list(csv.DictReader(handle))


@pytest.fixture(scope="session")
def results(root: Path) -> dict:
    return json.loads((root / "analysis" / "pilot_results.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def paper(root: Path) -> str:
    return (root / "manuscript" / "paper.md").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def abstract(root: Path) -> str:
    return (root / "manuscript" / "abstract.md").read_text(encoding="utf-8")
