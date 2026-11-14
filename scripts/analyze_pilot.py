#!/usr/bin/env python3
"""Analyse the frozen 12-paper pilot and write a machine-readable audit trail.

The pilot is purposive and tiny. This script therefore reports counts, score
distributions, and Wilson intervals. It also computes exact-binomial
diagnostics for the protocol's H1/H3 thresholds, but labels them as
descriptive only. They are not confirmatory tests and must not be reported as
population evidence.

Inputs
------
pilot/pilot_coding_table.csv   frozen pilot coding table (12 rows)
pilot/pilot_summary.md         source for the 29 -> 27 access flow and the
                               LLM-LLM agreement figures

Outputs
-------
analysis/pilot_results.json
analysis/pilot_results.md
analysis/pilot_rows_normalized.csv

Usage
-----
    python scripts/analyze_pilot.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
PILOT_CSV = ROOT / "pilot" / "pilot_coding_table.csv"
OUT_DIR = ROOT / "analysis"
Z = 1.959963984540054
PRIMARY_CRITIQUES = {"evalplus", "swebenchplus"}

# Access flow is recorded in pilot/pilot_summary.md, not in the coding table.
PILOT_FLOW = {
    "purposive_frame": 29,
    "full_text_accessible": 27,
    "coded": 12,
    "eligible_all_pairs": 8,
    "eligible_primary_pairs": 6,
    "ineligible": 4,
}

# Reliability is LLM-LLM agreement. It is NOT human inter-rater reliability.
PILOT_RELIABILITY = {
    "type": "LLM-LLM agreement; not human inter-rater reliability",
    "eligibility_agreement": "12/12 (100%)",
    "eligibility_kappa": 1.00,
    "eligibility_kappa_note": "1.00 by convention because there is no variance.",
    "ordinal_agreement": "7/8 (87.5%)",
    "ordinal_unweighted_kappa": 0.78,
    "ordinal_linear_weighted_kappa": 0.86,
    "disagreement": "promptcot: first pass 0, second pass proposed 1, adjudicated 0.",
    "human_second_coder": False,
    "model_version_logged": False,
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wilson(k: int, n: int, z: float = Z) -> tuple[float, float, float]:
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    denominator = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return (p, max(0.0, centre - half), min(1.0, centre + half))


def binom_cdf(k: int, n: int, p: float) -> float:
    """P(X <= k) for X ~ Binomial(n, p)."""
    if n < 0 or k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return sum(math.comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k + 1))


def is_true(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "1.0", "true", "yes"}


def score_of(row: dict[str, str]) -> int:
    return int(str(row["score"]).strip())


def read_pilot(path: Path = PILOT_CSV) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def eligible_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if is_true(row.get("eligible")) and str(row.get("score", "")).strip() in {"0", "1", "2", "3"}
    ]


def summarise(rows: list[dict[str, str]]) -> dict[str, Any]:
    n = len(rows)
    counts = Counter(score_of(row) for row in rows)
    full = counts.get(3, 0)
    proportion, low, high = wilson(full, n)
    citation_only = counts.get(0, 0)
    acknowledged = counts.get(1, 0)
    partial = counts.get(2, 0)
    independent = sum(1 for row in rows if is_true(row.get("independent_remediation")))
    engagement = Counter(int(str(row.get("engagement") or 0)) for row in rows)

    return {
        "n_eligible": n,
        "score_distribution": {str(score): counts.get(score, 0) for score in range(4)},
        "score_share": {
            str(score): (counts.get(score, 0) / n if n else float("nan"))
            for score in range(4)
        },
        "full_adoption_k": full,
        "full_adoption": proportion,
        "wilson_95_ci": [low, high],
        "acknowledged_or_better_k": sum(1 for row in rows if score_of(row) >= 1),
        "acknowledged_or_better": (sum(1 for row in rows if score_of(row) >= 1) / n if n else float("nan")),
        "partial_or_full_k": sum(1 for row in rows if score_of(row) >= 2),
        "partial_or_full": (sum(1 for row in rows if score_of(row) >= 2) / n if n else float("nan")),
        "citation_only_k": citation_only,
        "acknowledged_k": acknowledged,
        "partial_k": partial,
        "independent_remediation_k": independent,
        "independent_remediation_share": (independent / n if n else float("nan")),
        "engagement_distribution": {str(key): engagement.get(key, 0) for key in range(3)},
        "exact_binomial_diagnostic": {
            "h1_p_value_full_adoption_below_0_25": binom_cdf(full, n, 0.25) if n else float("nan"),
            "h3_p_value_zero_or_one_above_0_50": (
                1 - binom_cdf(citation_only + acknowledged - 1, n, 0.50) if n else float("nan")
            ),
            "status": "descriptive only; the pilot is too small for confirmatory inference",
        },
    }


def main() -> int:
    rows = read_pilot()
    eligible = eligible_rows(rows)
    primary = [row for row in eligible if str(row.get("critique", "")).strip() in PRIMARY_CRITIQUES]
    all_pair = eligible

    if len(rows) != 12 or len(eligible) != 8 or len(primary) != 6:
        raise SystemExit(
            f"Pilot integrity failure: rows={len(rows)}, eligible={len(eligible)}, primary={len(primary)}"
        )

    by_critique: dict[str, Any] = {}
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in eligible:
        groups[str(row.get("critique") or "unknown")].append(row)
    for critique, group in sorted(groups.items()):
        by_critique[critique] = summarise(group)

    by_year: dict[str, Any] = {}
    year_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in eligible:
        year_groups[str(row.get("year") or "unknown")].append(row)
    for year, group in sorted(year_groups.items()):
        by_year[year] = summarise(group)

    results = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "pilot_coding_table": str(PILOT_CSV.relative_to(ROOT)),
            "pilot_coding_table_sha256": sha256_file(PILOT_CSV),
            "pilot_summary": "pilot/pilot_summary.md",
            "note": "Purposive pilot, not a probability sample; no population prevalence is estimated.",
        },
        "flow": PILOT_FLOW,
        "coded_rows": len(rows),
        "eligible_rows": len(eligible),
        "primary_pair_rows": len(primary),
        "ineligible_rows": len(rows) - len(eligible),
        "ineligibility_reasons": dict(
            Counter(str(row.get("ineligibility_reason") or "unspecified") for row in rows if not is_true(row.get("eligible")))
        ),
        "primary_pair": summarise(primary),
        "all_pair": summarise(all_pair),
        "by_critique": by_critique,
        "by_year": by_year,
        "reliability": PILOT_RELIABILITY,
        "interpretation_rules": [
            "Do not report these counts as population prevalence.",
            "Do not describe the LLM-LLM kappa values as human reliability.",
            "Do not pool the GSM1k rows into the primary-pair estimate.",
            "Do not infer causation from citation co-occurrence.",
        ],
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "pilot_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    normalized_fields = [
        "paper_key",
        "critique",
        "eligible",
        "ineligibility_reason",
        "score",
        "engagement",
        "independent_remediation",
        "evidence_quote",
        "notes",
    ]
    with (OUT_DIR / "pilot_rows_normalized.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=normalized_fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in normalized_fields})

    def fmt_pct(value: float) -> str:
        return "n/a" if math.isnan(value) else f"{value * 100:.1f}%"

    def fmt_ci(values: list[float]) -> str:
        if any(math.isnan(value) for value in values):
            return "n/a"
        return f"{values[0] * 100:.1f}–{values[1] * 100:.1f}%"

    lines = [
        "# Pilot analysis output\n\n",
        f"Generated from `pilot/pilot_coding_table.csv` (SHA-256 `{results['source']['pilot_coding_table_sha256'][:16]}…`).\n\n",
        "**Status:** purposive pilot, not a prevalence study. No human second coder.\n\n",
        "## Flow\n\n| Stage | n |\n|---|---:|\n",
    ]
    for key, value in PILOT_FLOW.items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |\n")
    lines += [
        "\n## Primary-pair estimate (EvalPlus + SWE-bench+)\n\n",
        "| Quantity | k | n | Estimate | Wilson 95% CI |\n|---|---:|---:|---:|---|\n",
        f"| Full adoption (score 3) | {results['primary_pair']['full_adoption_k']} | {results['primary_pair']['n_eligible']} | "
        f"{fmt_pct(results['primary_pair']['full_adoption'])} | {fmt_ci(results['primary_pair']['wilson_95_ci'])} |\n",
        f"| Acknowledged or better (1–3) | {results['primary_pair']['acknowledged_or_better_k']} | {results['primary_pair']['n_eligible']} | "
        f"{fmt_pct(results['primary_pair']['acknowledged_or_better'])} | — |\n",
        f"| Citation only (0) | {results['primary_pair']['citation_only_k']} | {results['primary_pair']['n_eligible']} | "
        f"{fmt_pct(results['primary_pair']['score_share']['0'])} | — |\n",
        f"| Independent remediation | {results['primary_pair']['independent_remediation_k']} | {results['primary_pair']['n_eligible']} | "
        f"{fmt_pct(results['primary_pair']['independent_remediation_share'])} | — |\n",
        "\n## All-pair distribution (includes GSM1k secondary contrast)\n\n",
        "| Score | Primary pair | All pairs |\n|---:|---:|---:|\n",
    ]
    for score in range(4):
        lines.append(
            f"| {score} | {results['primary_pair']['score_distribution'][str(score)]} | "
            f"{results['all_pair']['score_distribution'][str(score)]} |\n"
        )
    lines += [
        "\n## By critique\n\n| Critique | Eligible | Full (3) | Estimate | Wilson 95% CI |\n|---|---:|---:|---:|---|\n",
    ]
    for critique, summary in by_critique.items():
        lines.append(
            f"| {critique} | {summary['n_eligible']} | {summary['full_adoption_k']} | "
            f"{fmt_pct(summary['full_adoption'])} | {fmt_ci(summary['wilson_95_ci'])} |\n"
        )
    lines += [
        "\n## Reliability (LLM–LLM only, not human)\n\n",
        "| Check | Result |\n|---|---|\n",
        f"| Eligibility agreement | {PILOT_RELIABILITY['eligibility_agreement']} |\n",
        f"| Ordinal agreement | {PILOT_RELIABILITY['ordinal_agreement']} |\n",
        f"| Unweighted κ | {PILOT_RELIABILITY['ordinal_unweighted_kappa']:.2f} |\n",
        f"| Linear-weighted κ | {PILOT_RELIABILITY['ordinal_linear_weighted_kappa']:.2f} |\n",
        f"| Disagreement | {PILOT_RELIABILITY['disagreement']} |\n",
        "\n## Exact-binomial diagnostics\n\n",
        "These p-values are shown only to document the pre-specified thresholds. They are not evidence about the population.\n\n",
        f"- H1 (full adoption <25%): p = {results['primary_pair']['exact_binomial_diagnostic']['h1_p_value_full_adoption_below_0_25']:.3f}\n",
        f"- H3 (score 0/1 >50%): p = {results['primary_pair']['exact_binomial_diagnostic']['h3_p_value_zero_or_one_above_0_50']:.3f}\n",
    ]
    (OUT_DIR / "pilot_results.md").write_text("".join(lines), encoding="utf-8")

    print(json.dumps({
        "primary_pair": results["primary_pair"],
        "all_pair": results["all_pair"],
        "output": str(OUT_DIR / "pilot_results.json"),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
