# Pilot Summary — Benchmark Critique Adoption

**Pilot date:** 13 November 2026  
**Frame:** 29 purposively selected citing papers  
**Coded:** 12 papers  
**Purpose:** test whether the construct, rubric, and coding workflow can distinguish citation, acknowledgment, partial adoption, and full adoption; estimate access and coding effort; debug boundary rules.  
**Not a prevalence study.** The frame was purposive, not random, and the sample is tiny.

---

## 1. What was done

1. Assembled a 29-paper access frame from papers citing EvalPlus, SWE-bench+, or GSM1k, selected to cover different benchmarks and likely adoption levels.
2. Attempted full-text retrieval for all 29.
3. Coded 12 papers with rubric v1.0; the remaining 17 were used for access testing only or were not needed after category saturation.
4. Ran a second, independent LLM pass on the 12 coded papers with a fresh context to test rubric reproducibility.
5. Adjudicated the one ordinal disagreement and documented boundary cases.

---

## 2. Access

| Quantity | Count |
|---|---:|
| Purposive frame | 29 |
| Full text accessible | 27 |
| Access rate | **93.1%** |
| Coded | 12 |
| Eligible (all three pairs) | 8 |
| Eligible (two primary pairs only) | 6 |
| Ineligible | 4 |

**Do not generalize 93.1%.** The frame was chosen because the papers were likely to be accessible and relevant. The general 2,666-paper frame may have a lower rate, especially for paywalled venue papers and recent 2026 records.

---

## 3. Primary-pair results (EvalPlus + SWE-bench+)

| Paper | Critique | Score | Label |
|---|---|---:|---|
| `whatswrong` | EvalPlus | **3** | Full adoption |
| `utboost` | SWE-bench+ | **1** | Acknowledged |
| `schrodinger` | SWE-bench+ | **1** | Acknowledged |
| `calibration` | EvalPlus | **1** | Acknowledged |
| `reagent` | SWE-bench+ | **0** | Citation only |
| `correctness_internal` | EvalPlus | **0** | Citation only |

**Score distribution:** 1 full, 3 acknowledged, 2 citation-only, 0 partial.

**Full adoption:** 1/6 = **16.7%**; Wilson 95% CI **3.0–56.4%**. The interval is enormous because n=6. This is a prior for planning, not an estimate.

**Acknowledgment or stronger:** 4/6 = 66.7%. **Citation-only:** 2/6 = 33.3%.

---

## 4. All-pair results (including GSM1k secondary contrast)

| Paper | Critique | Score | Label |
|---|---|---:|---|
| `whatswrong` | EvalPlus | **3** | Full adoption |
| `utboost` | SWE-bench+ | **1** | Acknowledged |
| `schrodinger` | SWE-bench+ | **1** | Acknowledged |
| `calibration` | EvalPlus | **1** | Acknowledged |
| `understand_translate` | GSM1k | **1** | Acknowledged |
| `reagent` | SWE-bench+ | **0** | Citation only |
| `correctness_internal` | EvalPlus | **0** | Citation only |
| `promptcot` | GSM1k | **0** | Citation only |

**Score distribution:** 1 full, 4 acknowledged, 3 citation-only, 0 partial.

**Full adoption:** 1/8 = **12.5%**; Wilson 95% CI **2.2–47.1%**.

The all-pair estimate is the origin of the 12.5% planning value. The protocol excludes GSM1k from the primary denominator; the primary-pair estimate is 1/6 = 16.7%. Because n=6 is too small to prefer 16.7%, the main study uses 12.5% as a conservative planning value for precision calculations.

---

## 5. Reliability (machine–machine, not human)

| Check | Result |
|---|---|
| Eligibility agreement | 12/12 = 100% |
| Eligibility κ | 1.00 by convention (no variance) |
| Ordinal agreement | 7/8 = 87.5% |
| Ordinal unweighted κ | 0.78 |
| Ordinal linear-weighted κ | 0.86 |
| Disagreement | `promptcot`: second pass proposed 1; first coder 0; adjudicated **0** |

**Critical caveat:** both passes were LLM annotations with fresh context. This is **not** human inter-rater reliability. The κ values are useful for debugging the rubric, not for the manuscript's reliability claim. No human second coder has coded the pilot.

The primary-pair subset had no ordinal disagreements (6/6), but n=6 is too small to estimate reliability. Do not report 1.00 as a reliability result.

---

## 6. Boundary cases and what they taught

| Case | Issue | Resolution in v1.1 |
|---|---|---|
| `whatswrong` | Uses HumanEval+/MBPP+ as main benchmarks; samples 164/399 problems and reports pass rates. | Score 3. Full adoption can include a derived benchmark built from the remediated artifact if the augmented tests support the main evaluation. |
| `utboost` | Cites both EvalPlus and SWE-bench+; discusses incorrect patches; says it cannot directly apply EvalPlus; proposes UTBoost. | Score 1, `independent_remediation=yes`. Discussing a critique and building your own mitigation is not adoption. |
| `schrodinger` | Cites SWE-bench+ as an enhancement; uses its own repository transformations on SWE-bench Verified. | Score 1, `independent_remediation=yes`. A different remediation is not the critique's artifact. |
| `calibration` | States that Liu et al. report gaps in HumanEval's tests; evaluates original HumanEval. | Score 1. Specific acknowledgment without adoption. |
| `reagent` | Cites Aleithan only in the reference list; runs its own leakage analysis. | Score 0, `independent_remediation=yes`. Independent remediation without engagement is citation-only. |
| `correctness_internal` | Cites Liu et al. only in the reference list; evaluates original HumanEval/MBPP. | Score 0. No specific engagement. |
| `promptcot` | Cites GSM1k in a generic memorization cluster; evaluates GSM8K unchanged. | Score 0 under the generic-cluster rule; secondary only. The v1.0 second pass proposed 1; adjudicated 0. |
| `understand_translate` | Cites Zhang et al. in a generic contamination sentence; runs its own KSM check; evaluates GSM8K/translated data. | Score 1, `independent_remediation=yes`; secondary only. |
| `swebenchpro` | Evaluates SWE-bench Pro, a derivative. | Ineligible: derivative-only. |
| `cweval` | Evaluates CWEval; cites EvalPlus only as future work. | Ineligible: no evaluation of HumanEval/MBPP. |
| `hafix` | Cites Aleithan in a generic bug-fixing list; no SWE-bench evaluation. | Ineligible: no evaluation. |
| `demystifying` | Cites Zhang et al. in a generic claim; no GSM8K evaluation. | Ineligible: no evaluation. |

---

## 7. What the pilot supports

- The coding task is tractable: 12 papers were coded with evidence quotes in a single session.
- The rubric can distinguish full adoption, acknowledgment, and citation-only; the categories are not collapsing.
- Full adoption exists but is rare in the pilot: one clear case (`whatswrong`).
- Access to a purposive frame is high (93.1%), so the main study is not obviously blocked by paywalls.
- The main boundary problems are identifiable and can be resolved in rubric v1.1: generic clusters, independent remediation, derivative benchmarks, and partial vs full.

## 8. What the pilot does not establish

- It does not estimate prevalence in the 2,666-paper frame. The frame is purposive and n=8 eligible.
- It does not establish human reliability. The κ values are LLM–LLM.
- It does not show that the 93.1% access rate generalizes.
- It does not show that adoption is caused by the critique; it only shows that some citing papers document use.
- It does not validate the full-adoption rate for SWE-bench+; the pilot has only three SWE-bench+ papers, and none adopted the 548-instance dataset.

## 9. Implications for the main study

1. Use **p=0.125** as the planning value; target **120 eligible** papers, not 8.
2. Double-code **20%** of eligible papers with a **human** second coder; do not reuse the pilot κ.
3. Apply the **generic-cluster rule** (score 0) to avoid inflating acknowledgment.
4. Keep **GSM1k** out of the primary denominator.
5. Add **derivative-only** and **partial-vs-full** rules to the coding form.
6. Treat SWE-bench+ as a **census/descriptive contrast**, not a powered comparison.
7. Budget **20 minutes** per eligibility screen and **30 minutes** per eligible paper; the pilot did not time precisely, so these are estimates to validate in calibration.
8. Run the **50-record access pretest** before committing to the 900-paper sample.
