from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


EXPECTED_CSV_SHA256 = (
    "4650ce1b67df80bdeb1691b883a36f5bda540efd1dad20da652660f216f705a0"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_frame_row_count(frame_rows):
    assert len(frame_rows) == 2666
    assert len({row["cluster_id"] for row in frame_rows}) == 2666


def test_frame_hash_matches_summary(root, frame_rows):
    summary = json.loads((root / "data" / "frame_summary.json").read_text(encoding="utf-8"))
    assert summary["title_clusters"] == 2666
    assert summary["identifier_dedup_rows"] == 2684
    assert summary["sha256"]["citation_frame_2666_csv"] == EXPECTED_CSV_SHA256
    assert sha256(root / "data" / "citation_frame_2666.csv") == EXPECTED_CSV_SHA256


def test_frame_strata(frame_rows, root):
    summary = json.loads((root / "data" / "frame_summary.json").read_text(encoding="utf-8"))
    counts = Counter(row["stratum"] for row in frame_rows)
    assert counts["SWE_bench_plus_census"] == 135
    assert counts["EvalPlus_only_sample"] == 2531
    assert sum(counts.values()) == 2666
    assert summary["strata"]["SWE_bench_plus_census"] == 135
    assert summary["strata"]["EvalPlus_only_sample"] == 2531


def test_frame_cites_and_year_counts(frame_rows, root):
    summary = json.loads((root / "data" / "frame_summary.json").read_text(encoding="utf-8"))
    cites = Counter(row["cites"] for row in frame_rows)
    assert cites["evalplus"] == 2531
    assert cites["swebenchplus"] == 112
    assert cites["evalplus+swebenchplus"] == 23

    years = Counter((row["year"] or "unknown") for row in frame_rows)
    for year, count in summary["years"].items():
        assert years[year] == count
    assert sum(years.values()) == 2666


def test_frame_identifiers_and_anomalies(frame_rows, root):
    summary = json.loads((root / "data" / "frame_summary.json").read_text(encoding="utf-8"))
    assert sum(1 for row in frame_rows if row["doi"]) == summary["identifier_coverage"]["doi"]
    assert sum(1 for row in frame_rows if row["arxiv"]) == summary["identifier_coverage"]["arxiv"]
    assert sum(1 for row in frame_rows if row["dblp"]) == summary["identifier_coverage"]["dblp"]
    assert (
        sum(1 for row in frame_rows if not any(row[k] for k in ("doi", "arxiv", "dblp")))
        == summary["identifier_coverage"]["no_doi_arxiv_dblp"]
    )
    assert summary["multi_variant_clusters"] == 14
    assert summary["publication_date_after_2026_09_30"] == 231
    assert summary["no_publication_date"] == 225


def test_frame_has_required_columns(frame_rows):
    required = {
        "cluster_id",
        "stratum",
        "title",
        "year",
        "publicationDate",
        "venue",
        "doi",
        "arxiv",
        "dblp",
        "corpusId",
        "paperId",
        "cites",
        "n_title_variants",
    }
    assert required.issubset(frame_rows[0].keys())
