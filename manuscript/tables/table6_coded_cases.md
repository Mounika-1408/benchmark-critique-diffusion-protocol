# Table 6. Coded pilot cases and boundary decisions

| Paper key | Critique | Eligible | Score | Engagement | Independent remediation | Boundary note |
|---|---|---|---:|---:|---|---|
| `whatswrong` | EvalPlus | Yes | 3 | 2 | No | Uses HumanEval+ and MBPP+ as main benchmarks, including augmented tests; reports pass rates. Full adoption. |
| `utboost` | SWE-bench+ | Yes | 1 | 2 | Yes | Discusses the critique's incorrect-patch finding but proposes its own UTBoost; no SWE-bench+ dataset/protocol adoption. |
| `schrodinger` | SWE-bench+ | Yes | 1 | 2 | Yes | Cites SWE-bench+ as an enhancement but uses its own repository transformations on SWE-bench Verified; no SWE-bench+ adoption. |
| `calibration` | EvalPlus | Yes | 1 | 1 | No | States the critique's test-gap finding but evaluates original HumanEval; no augmented tests. |
| `reagent` | SWE-bench+ | Yes | 0 | 0 | Yes | Critique appears only in the reference list; the paper's leakage analysis is independent and not presented as following SWE-bench+. |
| `correctness_internal` | EvalPlus | Yes | 0 | 0 | No | Critique appears only in the reference list; evaluates original HumanEval/MBPP without discussing the test-insufficiency finding. |
| `promptcot` | GSM1k (secondary) | Yes | 0 | 0 | No | Secondary GSM1k contrast. Generic memorization cluster; evaluates GSM8K unchanged. Pilot disagreement: order 1 vs 0; adjudicated 0 under the generic-cluster rule. |
| `understand_translate` | GSM1k (secondary) | Yes | 1 | 1 | Yes | Secondary GSM1k contrast. Generic contamination citation; runs its own KSM contamination check, not GSM1k; evaluates GSM8K/translated data unchanged. |
| `hafix` | SWE-bench+ | No | — | 0 | No | Cites Aleithan in a generic bug-fixing list; does not evaluate SWE-bench/Lite/Verified. |
| `swebenchpro` | SWE-bench+ | No | — | 0 | No | Evaluates SWE-bench Pro, a derivative, not SWE-bench/Lite/Verified. |
| `cweval` | EvalPlus | No | — | 0 | No | Evaluates its own CWEval benchmark; cites EvalPlus only as future work. |
| `demystifying` | GSM1k (secondary) | No | — | 0 | No | Cites Zhang et al. in a generic claim; does not evaluate GSM8K/GSM1k. |

Scores are defined in `rubric_v1.1.md`. Ineligible papers receive no 0–3 score; their score field is blank in the source data and is shown here as an em dash.
