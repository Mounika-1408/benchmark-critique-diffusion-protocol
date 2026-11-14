#!/usr/bin/env python3
"""Generate the manuscript's tables from frozen inputs.

All tables are derived from:
* data/citation_frame_2666.csv and data/frame_summary.json
* pilot/pilot_coding_table.csv
* analysis/pilot_results.json (produced by scripts/analyze_pilot.py)

Run scripts/analyze_pilot.py first. The script is deterministic and writes both
Markdown (for the manuscript) and CSV (for audit/reuse).

Usage
-----
    python scripts/analyze_pilot.py
    python scripts/make_manuscript_tables.py
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FRAME = ROOT / "data" / "citation_frame_2666.csv"
FRAME_SUMMARY = ROOT / "data" / "frame_summary.json"
PILOT = ROOT / "pilot" / "pilot_coding_table.csv"
RESULTS = ROOT / "analysis" / "pilot_results.json"
OUT = ROOT / "manuscript" / "tables"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def pct(k: int, n: int) -> str:
    return f"{k / n * 100:.1f}%" if n else "n/a"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    frame = read_csv(FRAME)
    summary = json.loads(FRAME_SUMMARY.read_text(encoding="utf-8"))
    pilot = read_csv(PILOT)
    results = json.loads(RESULTS.read_text(encoding="utf-8"))

    strata = Counter(row["stratum"] for row in frame)
    years = Counter(row["year"] or "unknown" for row in frame)
    both = sum(1 for row in frame if row["cites"] == "evalplus+swebenchplus")

    # Table 1: benchmark pairs and remediation characteristics
    pair_rows = [
        {
            "pair": "P1",
            "critique": "EvalPlus (Liu et al., 2023)",
            "criticized": "HumanEval; MBPP",
            "recommended": "HumanEval+ / MBPP+ augmented tests as the primary evaluation",
            "artifact": "Public GitHub harness; Apache-2.0; 80× tests for HumanEval+, 35× for MBPP+, 378 MBPP+ tasks",
            "cost": "Low: drop-in test suite and harness",
            "role": "Primary",
        },
        {
            "pair": "P2",
            "critique": "SWE-bench+ (Aleithan et al., 2024)",
            "criticized": "SWE-bench; SWE-bench Lite; SWE-bench Verified",
            "recommended": "548-instance curated dataset and/or strengthened-test protocol as the primary evaluation",
            "artifact": "Public Zenodo dataset; CC BY 4.0; 548 instances",
            "cost": "High: filtered instances, harness reconciliation, agent re-runs",
            "role": "Primary",
        },
        {
            "pair": "S1",
            "critique": "GSM1k (Zhang et al., 2024)",
            "criticized": "GSM8K",
            "recommended": "GSM1k or a fully equivalent contamination-controlled replication",
            "artifact": "Public Hugging Face dataset; 1,205 rows; license field blank",
            "cost": "Medium: parallel benchmark, not a drop-in replacement",
            "role": "Secondary only; excluded from primary denominator",
        },
    ]
    write_csv(OUT / "table1_benchmark_pairs.csv", pair_rows,
              ["pair", "critique", "criticized", "recommended", "artifact", "cost", "role"])
    lines = [
        "# Table 1. Benchmark pairs and remediation characteristics\n\n",
        "| Pair | Critique | Criticized benchmark | Recommended practice | Artifact status | Cost | Role |\n",
        "|---|---|---|---|---|---|---|\n",
    ]
    for row in pair_rows:
        lines.append(
            f"| {row['pair']} | {row['critique']} | {row['criticized']} | {row['recommended']} | "
            f"{row['artifact']} | {row['cost']} | {row['role']} |\n"
        )
    lines += [
        "\nArtifact facts are verified in `verification/source_verification_log.md`. Cost is an analytic characterization, not a measured implementation time.\n",
    ]
    write_markdown(OUT / "table1_benchmark_pairs.md", "".join(lines))

    # Table 2: frame profile
    frame_rows = [
        {"quantity": "Raw EvalPlus citation rows", "count": 2572, "note": "Semantic Scholar reports 2,573; one row not returned."},
        {"quantity": "Raw SWE-bench+ citation rows", "count": 136, "note": "Semantic Scholar reports 136."},
        {"quantity": "Identifier-deduplicated union", "count": 2684, "note": "Intermediate count; not the analysis frame."},
        {"quantity": "Title-deduplicated clusters", "count": len(frame), "note": "Frozen analysis frame."},
        {"quantity": "SWE-bench+ census stratum", "count": strata.get("SWE_bench_plus_census", 0), "note": "Includes 23 clusters citing both critiques."},
        {"quantity": "EvalPlus-only sample stratum", "count": strata.get("EvalPlus_only_sample", 0), "note": "Sampled in the planned main design."},
        {"quantity": "Clusters citing both critiques", "count": both, "note": "Assigned to the SWE-bench+ census."},
    ]
    write_csv(OUT / "table2_frame_profile.csv", frame_rows, ["quantity", "count", "note"])
    lines = [
        "# Table 2. Frozen citation-frame profile\n\n",
        "| Quantity | Count | Note |\n|---|---:|---|\n",
    ]
    for row in frame_rows:
        lines.append(f"| {row['quantity']} | {row['count']:,} | {row['note']} |\n")
    lines += [
        "\nYear distribution: " + ", ".join(f"{year} = {count:,}" for year, count in sorted(years.items())) + ".\n\n",
        "2026 is incomplete and includes 231 future-dated records; 42 clusters have no publication year.\n\n",
        f"Frame SHA-256: `{summary['sha256']['citation_frame_2666_csv']}`. Source SHA-256: `{summary['sha256']['citation_frame_source']}`.\n",
    ]
    write_markdown(OUT / "table2_frame_profile.md", "".join(lines))

    # Table 3: pilot flow
    flow = results["flow"]
    flow_rows = [
        {"stage": "Purposive access frame", "n": flow["purposive_frame"], "note": "Selected for construct coverage, not randomly."},
        {"stage": "Full text accessible", "n": flow["full_text_accessible"], "note": "93.1% of the purposive frame; not generalizable."},
        {"stage": "Coded with rubric", "n": flow["coded"], "note": "Rubric v1.0; evidence quotes recorded."},
        {"stage": "Eligible, all pairs", "n": flow["eligible_all_pairs"], "note": "Includes two GSM1k secondary rows."},
        {"stage": "Eligible, primary pairs", "n": flow["eligible_primary_pairs"], "note": "EvalPlus + SWE-bench+ only."},
        {"stage": "Ineligible", "n": flow["ineligible"], "note": "Mostly no evaluation of the criticized benchmark."},
    ]
    write_csv(OUT / "table3_pilot_flow.csv", flow_rows, ["stage", "n", "note"])
    lines = ["# Table 3. Pilot flow\n\n| Stage | n | Note |\n|---|---:|---|\n"]
    for row in flow_rows:
        lines.append(f"| {row['stage']} | {row['n']} | {row['note']} |\n")
    write_markdown(OUT / "table3_pilot_flow.md", "".join(lines))

    # Table 4: score distributions
    primary = results["primary_pair"]
    all_pair = results["all_pair"]
    labels = {0: "Citation only", 1: "Acknowledged", 2: "Partial adoption", 3: "Full adoption"}
    distribution_rows = []
    for score in range(4):
        distribution_rows.append({
            "score": score,
            "label": labels[score],
            "primary_pair_n": primary["score_distribution"][str(score)],
            "primary_pair_share": f"{primary['score_share'][str(score)] * 100:.1f}%",
            "all_pairs_n": all_pair["score_distribution"][str(score)],
            "all_pairs_share": f"{all_pair['score_share'][str(score)] * 100:.1f}%",
        })
    write_csv(OUT / "table4_pilot_scores.csv", distribution_rows,
              ["score", "label", "primary_pair_n", "primary_pair_share", "all_pairs_n", "all_pairs_share"])
    lines = [
        "# Table 4. Pilot adoption-score distribution\n\n",
        "| Score | Label | Primary pair n | Primary pair share | All pairs n | All pairs share |\n",
        "|---:|---|---:|---:|---:|---:|\n",
    ]
    for row in distribution_rows:
        lines.append(
            f"| {row['score']} | {row['label']} | {row['primary_pair_n']} | {row['primary_pair_share']} | "
            f"{row['all_pairs_n']} | {row['all_pairs_share']} |\n"
        )
    lines += [
        "\nPrimary pair n = 6; all pairs n = 8. The all-pair distribution includes the two GSM1k secondary rows and is not the primary denominator.\n",
    ]
    write_markdown(OUT / "table4_pilot_scores.md", "".join(lines))

    # Table 5: pair-specific results
    critique_labels = {
        "evalplus": "EvalPlus",
        "swebenchplus": "SWE-bench+",
        "gsm1k": "GSM1k (secondary)",
    }
    pair_rows = []
    for critique in ("evalplus", "swebenchplus", "gsm1k"):
        data = results["by_critique"][critique]
        pair_rows.append({
            "critique": critique,
            "critique_label": critique_labels[critique],
            "n": data["n_eligible"],
            "full": data["full_adoption_k"],
            "full_pct": f"{data['full_adoption'] * 100:.1f}%",
            "wilson_low": f"{data['wilson_95_ci'][0] * 100:.1f}%",
            "wilson_high": f"{data['wilson_95_ci'][1] * 100:.1f}%",
            "acknowledged_or_better": data["acknowledged_or_better_k"],
            "independent_remediation": data["independent_remediation_k"],
        })
    write_csv(OUT / "table5_pair_specific.csv", pair_rows,
              ["critique", "critique_label", "n", "full", "full_pct", "wilson_low", "wilson_high", "acknowledged_or_better", "independent_remediation"])
    lines = [
        "# Table 5. Pair-specific pilot results\n\n",
        "| Critique | Eligible n | Full (3) | Full % | Wilson 95% CI | Acknowledged or better | Independent remediation |\n",
        "|---|---:|---:|---:|---|---:|---:|\n",
    ]
    for row in pair_rows:
        lines.append(
            f"| {row['critique_label']} | {row['n']} | {row['full']} | {row['full_pct']} | "
            f"{row['wilson_low']}–{row['wilson_high']} | {row['acknowledged_or_better']} | {row['independent_remediation']} |\n"
        )
    lines += [
        "\nThe EvalPlus and SWE-bench+ rows each contain three papers. The contrast is descriptive only and is not powered.\n",
    ]
    write_markdown(OUT / "table5_pair_specific.md", "".join(lines))

    # Table 6: coded cases
    case_rows = []
    for row in pilot:
        case_rows.append({
            "paper_key": row["paper_key"],
            "critique": row["critique"],
            "eligible": row["eligible"],
            "score": row["score"],
            "engagement": row["engagement"],
            "independent_remediation": row["independent_remediation"],
            "boundary_note": row["notes"],
        })
    write_csv(OUT / "table6_coded_cases.csv", case_rows,
              ["paper_key", "critique", "eligible", "score", "engagement", "independent_remediation", "boundary_note"])
    lines = [
        "# Table 6. Coded pilot cases and boundary decisions\n\n",
        "| Paper key | Critique | Eligible | Score | Engagement | Independent remediation | Boundary note |\n",
        "|---|---|---|---:|---:|---|---|\n",
    ]
    for row in case_rows:
        note = str(row["boundary_note"]).replace("|", "\\|")
        score = str(row["score"]).strip() or "—"
        eligible = "Yes" if row["eligible"] == "true" else "No"
        independent = "Yes" if row["independent_remediation"] == "true" else "No"
        critique = critique_labels.get(row["critique"], row["critique"])
        lines.append(
            f"| `{row['paper_key']}` | {critique} | {eligible} | {score} | "
            f"{row['engagement']} | {independent} | {note} |\n"
        )
    lines += [
        "\nScores are defined in `rubric_v1.1.md`. Ineligible papers receive no 0–3 score; their score field is blank in the source data and is shown here as an em dash.\n",
    ]
    write_markdown(OUT / "table6_coded_cases.md", "".join(lines))

    print(f"Wrote 6 tables to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


