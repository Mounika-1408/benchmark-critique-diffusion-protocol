from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import analyze_pilot


PRIMARY = {"evalplus", "swebenchplus"}


def test_pilot_row_and_eligibility_counts(pilot_rows):
    assert len(pilot_rows) == 12
    eligible = [row for row in pilot_rows if row["eligible"].lower() == "true"]
    ineligible = [row for row in pilot_rows if row["eligible"].lower() == "false"]
    assert len(eligible) == 8
    assert len(ineligible) == 4
    assert len([row for row in eligible if row["critique"] in PRIMARY]) == 6
    assert all(row["ineligibility_reason"] == "NO_EVAL" for row in ineligible)
    assert all(row["score"] == "" for row in ineligible)


def test_pilot_primary_distribution(pilot_rows, results):
    primary = [
        row
        for row in pilot_rows
        if row["eligible"].lower() == "true" and row["critique"] in PRIMARY
    ]
    scores = Counter(int(row["score"]) for row in primary)
    assert scores[0] == 2 and scores[1] == 3 and scores[2] == 0 and scores[3] == 1
    assert results["primary_pair"]["n_eligible"] == 6
    assert results["primary_pair"]["score_distribution"] == {
        "0": 2,
        "1": 3,
        "2": 0,
        "3": 1,
    }
    assert results["primary_pair"]["full_adoption_k"] == 1
    assert results["primary_pair"]["independent_remediation_k"] == 3


def test_pilot_all_pair_distribution(pilot_rows, results):
    eligible = [row for row in pilot_rows if row["eligible"].lower() == "true"]
    scores = Counter(int(row["score"]) for row in eligible)
    assert scores[0] == 3 and scores[1] == 4 and scores[2] == 0 and scores[3] == 1
    assert results["all_pair"]["n_eligible"] == 8
    assert results["all_pair"]["score_distribution"] == {
        "0": 3,
        "1": 4,
        "2": 0,
        "3": 1,
    }
    assert results["all_pair"]["full_adoption_k"] == 1
    assert results["all_pair"]["acknowledged_k"] == 4
    assert results["all_pair"]["independent_remediation_k"] == 4


def test_pilot_flow_is_consistent(results):
    flow = results["flow"]
    assert flow["purposive_frame"] == 29
    assert flow["full_text_accessible"] == 27
    assert flow["coded"] == 12
    assert flow["eligible_all_pairs"] == 8
    assert flow["eligible_primary_pairs"] == 6
    assert flow["ineligible"] == 4
    assert flow["eligible_all_pairs"] + flow["ineligible"] == flow["coded"]


def test_pilot_keys_are_unique_and_expected(pilot_rows):
    keys = [row["paper_key"] for row in pilot_rows]
    assert len(keys) == len(set(keys))
    assert set(keys) == {
        "whatswrong",
        "utboost",
        "schrodinger",
        "calibration",
        "reagent",
        "correctness_internal",
        "promptcot",
        "understand_translate",
        "hafix",
        "swebenchpro",
        "cweval",
        "demystifying",
    }


def test_pilot_analysis_matches_summarise(pilot_rows, results):
    eligible = analyze_pilot.eligible_rows(pilot_rows)
    primary = [row for row in eligible if row["critique"] in PRIMARY]
    recomputed_primary = analyze_pilot.summarise(primary)
    recomputed_all = analyze_pilot.summarise(eligible)

    assert recomputed_primary["score_distribution"] == results["primary_pair"]["score_distribution"]
    assert recomputed_all["score_distribution"] == results["all_pair"]["score_distribution"]
    assert recomputed_primary["full_adoption_k"] == results["primary_pair"]["full_adoption_k"]
    assert recomputed_all["full_adoption_k"] == results["all_pair"]["full_adoption_k"]


def test_wilson_intervals_are_not_overstated(results):
    low, high = results["primary_pair"]["wilson_95_ci"]
    assert 0.0 <= low < 0.167 < high <= 1.0
    assert round(low * 100, 1) == 3.0
    assert round(high * 100, 1) == 56.4

    low8, high8 = results["all_pair"]["wilson_95_ci"]
    assert round(low8 * 100, 1) == 2.2
    assert round(high8 * 100, 1) == 47.1


def test_exact_binomial_diagnostics(results):
    primary = results["primary_pair"]["exact_binomial_diagnostic"]
    assert round(primary["h1_p_value_full_adoption_below_0_25"], 3) == 0.534
    assert round(primary["h3_p_value_zero_or_one_above_0_50"], 3) == 0.109
    assert "descriptive only" in primary["status"]


def test_reliability_is_llm_only(results):
    reliability = results["reliability"]
    assert reliability["human_second_coder"] is False
    assert "not human" in reliability["type"]
    assert reliability["ordinal_agreement"] == "7/8 (87.5%)"
    assert reliability["ordinal_unweighted_kappa"] == 0.78
    assert reliability["ordinal_linear_weighted_kappa"] == 0.86


def test_source_hash_is_current(root, results):
    import hashlib

    digest = hashlib.sha256(
        (root / "pilot" / "pilot_coding_table.csv").read_bytes()
    ).hexdigest()
    assert results["source"]["pilot_coding_table_sha256"] == digest
