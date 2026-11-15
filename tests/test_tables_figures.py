from __future__ import annotations

import csv
import json
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_table1_pairs_are_complete(root):
    rows = read_csv(root / "manuscript" / "tables" / "table1_benchmark_pairs.csv")
    assert [row["pair"] for row in rows] == ["P1", "P2", "S1"]
    assert all(
        any(row["critique"].startswith(name) for name in ("EvalPlus", "SWE-bench+", "GSM1k"))
        for row in rows
    )


def test_table2_frame_profile_matches_summary(root):
    rows = read_csv(root / "manuscript" / "tables" / "table2_frame_profile.csv")
    values = {row["quantity"].strip(): row["count"].strip() for row in rows}
    assert values["Raw EvalPlus citation rows"] == "2572"
    assert values["Raw SWE-bench+ citation rows"] == "136"
    assert values["Identifier-deduplicated union"] == "2684"
    assert values["Title-deduplicated clusters"] == "2666"
    assert values["SWE-bench+ census stratum"] == "135"
    assert values["EvalPlus-only sample stratum"] == "2531"
    assert values["Clusters citing both critiques"] == "23"


def test_table3_flow_matches_results(root, results):
    rows = read_csv(root / "manuscript" / "tables" / "table3_pilot_flow.csv")
    by_stage = {row["stage"].strip(): int(row["n"]) for row in rows}
    assert by_stage["Purposive access frame"] == results["flow"]["purposive_frame"]
    assert by_stage["Full text accessible"] == results["flow"]["full_text_accessible"]
    assert by_stage["Coded with rubric"] == results["flow"]["coded"]
    assert by_stage["Eligible, all pairs"] == results["flow"]["eligible_all_pairs"]
    assert by_stage["Eligible, primary pairs"] == results["flow"]["eligible_primary_pairs"]
    assert by_stage["Ineligible"] == results["flow"]["ineligible"]


def test_table4_scores_match_pilot(root, results):
    rows = read_csv(root / "manuscript" / "tables" / "table4_pilot_scores.csv")
    assert len(rows) == 4
    assert sum(int(row["primary_pair_n"]) for row in rows) == 6
    assert sum(int(row["all_pairs_n"]) for row in rows) == 8
    primary = {row["score"]: int(row["primary_pair_n"]) for row in rows}
    all_pairs = {row["score"]: int(row["all_pairs_n"]) for row in rows}
    assert primary == {"0": 2, "1": 3, "2": 0, "3": 1}
    assert all_pairs == {"0": 3, "1": 4, "2": 0, "3": 1}
    assert primary == {k: v for k, v in results["primary_pair"]["score_distribution"].items()}
    assert all_pairs == {k: v for k, v in results["all_pair"]["score_distribution"].items()}


def test_table5_pair_specific_matches_results(root, results):
    rows = read_csv(root / "manuscript" / "tables" / "table5_pair_specific.csv")
    by_pair = {row["critique"]: row for row in rows}
    assert sum(int(row["n"]) for row in rows) == 8
    assert sum(int(row["full"]) for row in rows) == 1
    for critique in ("evalplus", "swebenchplus", "gsm1k"):
        assert int(by_pair[critique]["n"]) == results["by_critique"][critique]["n_eligible"]
        assert int(by_pair[critique]["full"]) == results["by_critique"][critique]["full_adoption_k"]
        assert int(by_pair[critique]["independent_remediation"]) == results["by_critique"][critique]["independent_remediation_k"]


def test_table6_coded_cases_are_complete(root):
    rows = read_csv(root / "manuscript" / "tables" / "table6_coded_cases.csv")
    assert len(rows) == 12
    assert sum(1 for row in rows if row["eligible"] == "true") == 8
    assert sum(1 for row in rows if row["eligible"] == "false") == 4
    scored = [int(row["score"]) for row in rows if row["score"] not in ("", "—")]
    assert sorted(scored) == [0, 0, 0, 1, 1, 1, 1, 3]


def test_figure1_years_match_frame(root):
    rows = read_csv(root / "manuscript" / "figures" / "fig1_frame_years.csv")
    summary = json.loads((root / "data" / "frame_summary.json").read_text(encoding="utf-8"))
    values = {row["year"]: int(row["n"]) for row in rows}
    assert values == summary["years"]
    assert sum(values.values()) == 2666


def test_figure2_flow_matches_results(root, results):
    rows = read_csv(root / "manuscript" / "figures" / "fig2_pilot_flow.csv")
    values = {row["stage"].strip(): int(row["n"]) for row in rows}
    assert values["Purposive access frame"] == results["flow"]["purposive_frame"]
    assert values["Full text accessible"] == results["flow"]["full_text_accessible"]
    assert values["Coded with rubric v1.0"] == results["flow"]["coded"]
    assert values["Eligible, all pairs"] == results["flow"]["eligible_all_pairs"]
    assert values["Eligible, primary pairs"] == results["flow"]["eligible_primary_pairs"]


def test_figure3_scores_match_results(root, results):
    rows = read_csv(root / "manuscript" / "figures" / "fig3_pilot_scores.csv")
    primary = {
        row["score"]: int(row["n"])
        for row in rows
        if row["group"].startswith("Primary")
    }
    all_pairs = {
        row["score"]: int(row["n"])
        for row in rows
        if row["group"].startswith("All")
    }
    assert primary == {k: v for k, v in results["primary_pair"]["score_distribution"].items()}
    assert all_pairs == {k: v for k, v in results["all_pair"]["score_distribution"].items()}


def test_manuscript_tables_are_embedded_and_sources_exist(root):
    paper = (root / "manuscript" / "paper.md").read_text(encoding="utf-8")
    for number in range(1, 9):
        assert f"**Table {number}." in paper
    for name in (
        "table1_benchmark_pairs.md",
        "table2_frame_profile.md",
        "table3_pilot_flow.md",
        "table4_pilot_scores.md",
        "table5_pair_specific.md",
        "table6_coded_cases.md",
    ):
        assert (root / "manuscript" / "tables" / name).is_file()
    for name in ("fig1_frame_years.svg", "fig2_pilot_flow.svg", "fig3_pilot_scores.svg"):
        assert f"figures/{name}" in paper
        assert (root / "manuscript" / "figures" / name).is_file()
