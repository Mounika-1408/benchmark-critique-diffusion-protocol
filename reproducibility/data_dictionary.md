# Data Dictionary

## 1. `data/citation_frame_2666.csv`

One row per title-level citing work. Frozen on 13 November 2026.

| Column | Type | Description |
|---|---|---|
| `cluster_id` | string | Stable cluster identifier (`C0001`–`C2666`). |
| `stratum` | string | `SWE_bench_plus_census` (135 rows) or `EvalPlus_only_sample` (2,531 rows). |
| `title` | string | Representative title for the title cluster. |
| `year` | integer or empty | Publication year from the representative record. |
| `publicationDate` | string or empty | ISO date from Semantic Scholar, when present. |
| `venue` | string or empty | Venue name from the representative record. |
| `doi` | string or empty | Lowercased DOI, when present. |
| `arxiv` | string or empty | arXiv identifier, when present. |
| `dblp` | string or empty | DBLP key, when present. |
| `corpusId` | string or empty | Semantic Scholar CorpusId. |
| `paperId` | string | Semantic Scholar paperId for the representative record. |
| `cites` | string | Source label(s): `evalplus`, `swebenchplus`, or both joined by `+`. |
| `n_title_variants` | integer | Number of identifier-deduplicated records merged into this title cluster. |

Rows sum to 2,666. Strata sum to 2,666. The `cites` split is 2,531
EvalPlus-only, 112 SWE-bench+-only, and 23 both. The 23 both-critique clusters
are assigned to the SWE-bench+ census stratum.

## 2. `data/frame_summary.json`

Machine-readable summary of the frame build: raw row counts, identifier-deduplicated
count, title clusters, strata, year counts, identifier coverage, anomaly counts,
and SHA-256 hashes.

## 3. `pilot/pilot_coding_table.csv`

One row per coded pilot paper (12 rows).

| Column | Type | Description |
|---|---|---|
| `paper_key` | string | Short anonymized project key used in the manuscript. |
| `title` | string | Published title. |
| `venue` | string or empty | Venue as recorded during coding. |
| `year` | integer or `unknown` | Publication year as recorded. |
| `critique` | string | `evalplus`, `swebenchplus`, or `gsm1k`. |
| `eligible` | boolean | `true` or `false` after applying E1–E3. |
| `ineligibility_reason` | string or empty | `NO_EVAL` for the four ineligible rows. |
| `score` | integer 0–3 or empty | Adoption score; empty for ineligible rows. |
| `engagement` | integer 0–2 | 0 = reference only, 1 = brief mention, 2 = substantive discussion. |
| `independent_remediation` | boolean | Whether the paper remediated evaluation without adopting the critique's artifact. |
| `evidence_quote` | string | Short verbatim quote (≤60 words) or reference entry supporting the code. |
| `notes` | string | Boundary decision and coding rationale. |

The four ineligible rows have a blank `score` in the CSV. They are **not**
adoption outcomes and are excluded from every denominator.

## 4. `analysis/pilot_results.json`

Generated from the coding table by `scripts/analyze_pilot.py`.

| Field | Description |
|---|---|
| `source.pilot_coding_table_sha256` | SHA-256 of the coding table used. |
| `flow` | Purposive frame 29, accessible 27, coded 12, eligible all-pair 8, eligible primary 6, ineligible 4. |
| `primary_pair` | Distribution, full-adoption proportion, Wilson 95% CI, acknowledgment, independent remediation, engagement, exact-binomial diagnostics. |
| `all_pair` | Same quantities including the two GSM1k secondary rows. |
| `by_critique` | `evalplus`, `swebenchplus`, `gsm1k` descriptive splits. |
| `by_year` | Descriptive splits for 2025 and unknown year. |
| `reliability` | LLM–LLM agreement only; explicitly not human reliability. |
| `interpretation_rules` | Hard rules that forbid prevalence and causal claims. |

## 5. `manuscript/figures/*.csv`

Source data for the three SVG figures. `fig1_frame_years.csv` uses frame counts;
`fig2_pilot_flow.csv` and `fig3_pilot_scores.csv` use pilot results.

## 6. `manuscript/tables/*.csv`

Machine-readable versions of the six manuscript tables. The Markdown versions are
generated from the same inputs by `scripts/make_manuscript_tables.py`.

## 7. `data/cohort_feasibility.csv`

The 335-record feasibility draw (135 SWE-bench+ census + 200 EvalPlus-only, seed
`20261113`). It is a documented deviation from the 900-paper design. It was drawn
but **not coded**, and no results from it appear in the manuscript. It is included
so the deviation is auditable.
