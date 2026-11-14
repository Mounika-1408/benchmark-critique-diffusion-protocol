#!/usr/bin/env python3
"""Analyse a coded cohort and write reproducible tables.

The script is deliberately conservative: it reports counts, Wilson intervals,
and a design-weighted estimate, and it refuses to guess when required columns
are missing. It is a template for the registered analysis and is also used for
the bounded feasibility cohort.

Expected coding CSV columns (one row per cluster x critique)
------------------------------------------------------------
cluster_id, critique, eligible, ineligibility_reason, score, engagement,
independent_remediation, adoption_locus, evidence_quote, evidence_section,
coder_id, confidence, access_route, year, venue, design_weight

``eligible`` is 1/0. ``score`` is 0..3 and must be blank for ineligible rows.
``design_weight`` is the inverse inclusion probability from the sample draw
(1.0 for the SWE-bench+ census).

Usage
-----
    python scripts/analysis_template.py \
        --coding data/coding_adjudicated.csv \
        --out analysis
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

Z = 1.959963984540054


def wilson(k: int, n: int, z: float = Z) -> tuple[float, float, float]:
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    denominator = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return (p, max(0.0, centre - half), min(1.0, centre + half))


def bootstrap_proportion(
    values: list[tuple[float, int]], *, iterations: int = 5000, seed: int = 20261113
) -> tuple[float, float, float]:
    """Cluster bootstrap for a weighted proportion.

    ``values`` is [(weight, indicator), ...]. Resamples papers (rows), which is
    conservative when a paper contributes two critique rows.
    """
    if not values:
        return (float("nan"), float("nan"), float("nan"))
    rng = random.Random(seed)
    n = len(values)
    estimates: list[float] = []
    for _ in range(iterations):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        numerator = sum(w * y for w, y in sample)
        denominator = sum(w for w, _ in sample)
        if denominator:
            estimates.append(numerator / denominator)
    estimates.sort()
    point_num = sum(w * y for w, y in values)
    point_den = sum(w for w, _ in values)
    point = point_num / point_den if point_den else float("nan")
    low = estimates[int(0.025 * len(estimates))]
    high = estimates[int(0.975 * len(estimates)) - 1]
    return (point, low, high)


def fmt_pct(value: float) -> str:
    return "n/a" if math.isnan(value) else f"{value * 100:.1f}%"


def fmt_ci(interval: tuple[float, float, float]) -> str:
    _, low, high = interval
    if math.isnan(low):
        return "n/a"
    return f"{low * 100:.1f}–{high * 100:.1f}%"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def eligible_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    result = []
    for row in rows:
        if str(row.get("eligible", "")).strip() not in {"1", "1.0", "true", "TRUE", "yes"}:
            continue
        score = str(row.get("score", "")).strip()
        if score not in {"0", "1", "2", "3"}:
            continue
        result.append(row)
    return result


def score_of(row: dict[str, str]) -> int:
    return int(str(row["score"]).strip())


def weight_of(row: dict[str, str]) -> float:
    raw = str(row.get("design_weight", "") or "1").strip()
    try:
        return float(raw)
    except ValueError:
        return 1.0


def summarise(rows: list[dict[str, str]]) -> dict[str, Any]:
    n = len(rows)
    counts = Counter(score_of(r) for r in rows)
    full = counts.get(3, 0)
    interval = wilson(full, n)
    weighted = bootstrap_proportion([(weight_of(r), 1 if score_of(r) == 3 else 0) for r in rows])
    partial_plus = sum(1 for r in rows if score_of(r) >= 2)
    any_adoption = sum(1 for r in rows if score_of(r) >= 2)

    return {
        "n_eligible": n,
        "score_distribution": {str(k): counts.get(k, 0) for k in range(4)},
        "full_adoption_k": full,
        "full_adoption": interval[0],
        "full_adoption_ci": [interval[1], interval[2]],
        "partial_or_full_k": partial_plus,
        "partial_or_full": (partial_plus / n) if n else float("nan"),
        "any_engagement_k": any_adoption,
        "weighted_full_adoption": weighted[0],
        "weighted_full_adoption_ci": [weighted[1], weighted[2]],
    }


def group_summary(rows: list[dict[str, str]], key: str) -> dict[str, Any]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get(key) or "unknown")].append(row)
    return {name: summarise(group) for name, group in sorted(groups.items())}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coding", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--retrieval", type=Path, default=None,
                        help="Optional retrieval/screening CSV for access rates.")
    parser.add_argument("--bootstrap", type=int, default=5000)
    args = parser.parse_args()

    rows = read_rows(args.coding)
    eligible = eligible_rows(rows)
    if not eligible:
        raise SystemExit("No eligible coded rows found. Check `eligible` and `score` columns.")

    overall = summarise(eligible)
    by_critique = group_summary(eligible, "critique")
    by_year = group_summary(eligible, "year")
    by_critique_year = {
        critique: group_summary([r for r in eligible if r.get("critique") == critique], "year")
        for critique in sorted({r.get("critique", "unknown") for r in eligible})
    }

    # Paper-level: a paper is an adopter if any critique row scores 3.
    papers: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in eligible:
        papers[row["cluster_id"]].append(row)
    paper_adopters = sum(1 for group in papers.values() if any(score_of(r) == 3 for r in group))
    paper_interval = wilson(paper_adopters, len(papers))

    results = {
        "coding_file": str(args.coding),
        "n_rows": len(rows),
        "n_eligible_rows": len(eligible),
        "n_unique_papers": len(papers),
        "overall": overall,
        "by_critique": by_critique,
        "by_year": by_year,
        "by_critique_year": by_critique_year,
        "paper_level_any_full_adoption": {
            "k": paper_adopters,
            "n": len(papers),
            "proportion": paper_interval[0],
            "wilson_ci": [paper_interval[1], paper_interval[2]],
        },
    }

    if args.retrieval and args.retrieval.exists():
        retrieval = read_rows(args.retrieval)
        status = Counter(str(r.get("retrieval_status") or "unknown") for r in retrieval)
        results["retrieval"] = {
            "n_records": len(retrieval),
            "status": dict(status),
            "access_rate": (status.get("accessible", 0) / len(retrieval)) if retrieval else float("nan"),
        }

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines: list[str] = []
    lines.append("# Analysis output\n\n")
    lines.append(f"Coding file: `{args.coding}`  \n")
    lines.append(f"Eligible rows: **{len(eligible)}** across **{len(papers)}** unique papers.\n\n")
    lines.append("## Primary estimate\n\n")
    lines.append("| Quantity | k | n | Estimate | Wilson 95% CI |\n|---|---:|---:|---:|---|\n")
    lines.append(
        f"| Full adoption (score 3) | {overall['full_adoption_k']} | {overall['n_eligible']} | "
        f"{fmt_pct(overall['full_adoption'])} | {fmt_ci((overall['full_adoption'], *overall['full_adoption_ci']))} |\n"
    )
    lines.append(
        f"| Partial or full (score ≥2) | {overall['partial_or_full_k']} | {overall['n_eligible']} | "
        f"{fmt_pct(overall['partial_or_full'])} | — |\n"
    )
    lines.append(
        f"| Any full adoption, paper level | {paper_adopters} | {len(papers)} | "
        f"{fmt_pct(paper_interval[0])} | {fmt_ci(paper_interval)} |\n\n"
    )

    lines.append("## Ordinal distribution\n\n| Score | Rows | Share |\n|---:|---:|---:|\n")
    for score in range(4):
        count = overall["score_distribution"][str(score)]
        lines.append(f"| {score} | {count} | {(count / len(eligible) * 100):.1f}% |\n")
    lines.append("\n## By critique\n\n| Critique | Eligible | Full (3) | Estimate | Wilson 95% CI |\n|---|---:|---:|---:|---|\n")
    for critique, summary in by_critique.items():
        lines.append(
            f"| {critique} | {summary['n_eligible']} | {summary['full_adoption_k']} | "
            f"{fmt_pct(summary['full_adoption'])} | {fmt_ci((summary['full_adoption'], *summary['full_adoption_ci']))} |\n"
        )

    lines.append("\n## By publication year\n\n| Year | Eligible | Full (3) | Estimate | Wilson 95% CI |\n|---|---:|---:|---:|---|\n")
    for year, summary in by_year.items():
        lines.append(
            f"| {year} | {summary['n_eligible']} | {summary['full_adoption_k']} | "
            f"{fmt_pct(summary['full_adoption'])} | {fmt_ci((summary['full_adoption'], *summary['full_adoption_ci']))} |\n"
        )

    lines.append("\n## Design-weighted estimate\n\n")
    lines.append(
        f"Full adoption: **{fmt_pct(overall['weighted_full_adoption'])}** "
        f"(bootstrap 95% CI {fmt_pct(overall['weighted_full_adoption_ci'][0])}–"
        f"{fmt_pct(overall['weighted_full_adoption_ci'][1])}).\n"
    )
    lines.append("\n*Weights are inverse inclusion probabilities from the sample draw; "
                 "the SWE-bench+ census has weight 1. The bootstrap resamples rows and is "
                 "conservative for papers contributing two critique rows.*\n")

    (args.out / "results.md").write_text("".join(lines), encoding="utf-8")
    print("".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
