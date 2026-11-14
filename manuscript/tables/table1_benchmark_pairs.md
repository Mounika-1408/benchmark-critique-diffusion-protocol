# Table 1. Benchmark pairs and remediation characteristics

| Pair | Critique | Criticized benchmark | Recommended practice | Artifact status | Cost | Role |
|---|---|---|---|---|---|---|
| P1 | EvalPlus (Liu et al., 2023) | HumanEval; MBPP | HumanEval+ / MBPP+ augmented tests as the primary evaluation | Public GitHub harness; Apache-2.0; 80x tests for HumanEval+, 35x for MBPP+, 378 MBPP+ tasks | Low: drop-in test suite and harness | Primary |
| P2 | SWE-bench+ (Aleithan et al., 2024) | SWE-bench; SWE-bench Lite; SWE-bench Verified | 548-instance curated dataset and/or strengthened-test protocol as the primary evaluation | Public Zenodo dataset; CC BY 4.0; 548 instances | High: filtered instances, harness reconciliation, agent re-runs | Primary |
| S1 | GSM1k (Zhang et al., 2024) | GSM8K | GSM1k or a fully equivalent contamination-controlled replication | Public Hugging Face dataset; 1,205 rows; license field blank | Medium: parallel benchmark, not a drop-in replacement | Secondary only; excluded from primary denominator |

Artifact facts are verified in `verification/source_verification_log.md`. Cost is an analytic characterization, not a measured implementation time.
