# Pilot analysis output

Generated from `pilot/pilot_coding_table.csv` (SHA-256 `5bf96b3e0567dbe6…`).

**Status:** purposive pilot, not a prevalence study. No human second coder.

## Flow

| Stage | n |
|---|---:|
| purposive frame | 29 |
| full text accessible | 27 |
| coded | 12 |
| eligible all pairs | 8 |
| eligible primary pairs | 6 |
| ineligible | 4 |

## Primary-pair estimate (EvalPlus + SWE-bench+)

| Quantity | k | n | Estimate | Wilson 95% CI |
|---|---:|---:|---:|---|
| Full adoption (score 3) | 1 | 6 | 16.7% | 3.0–56.4% |
| Acknowledged or better (1–3) | 4 | 6 | 66.7% | — |
| Citation only (0) | 2 | 6 | 33.3% | — |
| Independent remediation | 3 | 6 | 50.0% | — |

## All-pair distribution (includes GSM1k secondary contrast)

| Score | Primary pair | All pairs |
|---:|---:|---:|
| 0 | 2 | 3 |
| 1 | 3 | 4 |
| 2 | 0 | 0 |
| 3 | 1 | 1 |

## By critique

| Critique | Eligible | Full (3) | Estimate | Wilson 95% CI |
|---|---:|---:|---:|---|
| evalplus | 3 | 1 | 33.3% | 6.1–79.2% |
| gsm1k | 2 | 0 | 0.0% | 0.0–65.8% |
| swebenchplus | 3 | 0 | 0.0% | 0.0–56.1% |

## Reliability (LLM–LLM only, not human)

| Check | Result |
|---|---|
| Eligibility agreement | 12/12 (100%) |
| Ordinal agreement | 7/8 (87.5%) |
| Unweighted κ | 0.78 |
| Linear-weighted κ | 0.86 |
| Disagreement | promptcot: first pass 0, second pass proposed 1, adjudicated 0. |

## Exact-binomial diagnostics

These p-values are shown only to document the pre-specified thresholds. They are not evidence about the population.

- H1 (full adoption <25%): p = 0.534
- H3 (score 0/1 >50%): p = 0.109
