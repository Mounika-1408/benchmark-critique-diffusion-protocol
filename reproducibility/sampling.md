# Sampling

## 1. Planned full-study design (not executed)

| Stratum | Frame N | Planned sample | Design weight |
|---|---:|---:|---:|
| SWE-bench+ census (includes 23 both-critique clusters) | 135 | 135 | 1.000 |
| EvalPlus-only | 2,531 | 765 | 3.308 |
| **Total** | **2,666** | **900** | — |

The EvalPlus-only sample is allocated proportionally by publication year (2022
collapsed into 2023, minimum 10 per non-empty stratum where possible), with a
fixed seed committed at registration.

### Planning assumptions

- Full-adoption planning value: p = 0.125 (from the all-pair pilot).
- Access rate: 80%.
- Eligibility among accessible papers: 18%.
- Expected eligible papers: 900 × 0.80 × 0.18 ≈ 130.
- Expected Wilson 95% CI half-width: about 5.7 percentage points (7.7–19.1%).

These are design calculations, not observed values.

### Stop rule

Sample and code in blocks. Start with 900 invited. If fewer than 120 eligible
papers are found, add blocks of 100 EvalPlus-only records up to a hard cap of
1,200 invited. Stop when 120 eligible papers are reached. If the cap is reached
with fewer than 120 eligible, report the realized count and do not extend without
a protocol amendment.

### Status

**Not executed.** No 900-paper sample was drawn, no main coding began, and no
full-scale estimate exists.

## 2. Pilot design

The pilot is a purposive 29-paper access frame, not a probability sample. It was
selected to exercise different benchmarks and likely adoption levels:

- 29 papers in the access frame,
- 27 accessible full texts (93.1%),
- 12 coded,
- 8 eligible for the all-pair set,
- 6 eligible for the primary pairs,
- 4 ineligible.

The 93.1% access rate applies only to this purposive frame and must not be
generalized to the 2,666-paper frame.

## 3. Feasibility cohort (documented deviation)

A 335-record cohort was drawn to test retrieval beyond the pilot:

| Stratum | N | Design weight |
|---|---:|---:|
| SWE-bench+ census | 135 | 1.000 |
| EvalPlus-only | 200 | 12.655 |
| **Total** | **335** | — |

- Seed: `20261113`.
- Frame SHA-256: `6a0a374ba6120b244418e887a76a83d6bfb8a95dd61cfc822cf349ac7043d30c`.
- Manifest: `data/cohort_feasibility.manifest.json`.
- Records coded: **0**.
- Retrieval: halted before completion.

The cohort is not the registered sample and contributes no result to the
manuscript. It is retained so the deviation is auditable.

## 4. Reproduction

`scripts/sample_frame.py` implements the stratified draw. Because the planned
900-paper sample was never executed, running it now produces a new draw and must
not be described as the study's sample. The 335-record cohort can be regenerated
from the manifest and seed.
