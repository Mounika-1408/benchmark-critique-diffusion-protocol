# Coding Rubric v1.1 — Benchmark Critique Adoption

**Status:** Frozen for pre-registration, 13 November 2026  
**Supersedes:** Rubric v1.0 (pilot, 13 November 2026)  
**Applies to:** EvalPlus → HumanEval/MBPP and SWE-bench+ → SWE-bench/Lite/Verified (primary); GSM1k → GSM8K (secondary contrast only)

---

## 1. Construct

**Documented adoption** is the extent to which a citing paper's own evaluation of the criticized benchmark uses the critique's recommended artifact or protocol, as stated in the paper's text, tables, or captions.

The construct has four levels: citation only, acknowledgment, partial adoption, full adoption. It is **not** a measure of:

- citation frequency or citation context alone;
- agreement with the critique;
- general evaluation quality or reproducibility;
- independent remediation that is not the critique's recommended practice;
- verified execution of the artifact.

**Unit of analysis:** one title-level citing work × one critique. A paper that cites both critiques gets two rows. A paper that evaluates multiple criticized benchmarks gets one score per critique, based on the highest-adoption use that supports a main claim; benchmark-level details go in secondary fields.

---

## 2. Critique → benchmark → recommended practice

### 2.1 Primary pairs

| ID | Critique | Criticized benchmark | Recommended practice | What counts as the artifact/protocol |
|---|---|---|---|---|
| **P1** | EvalPlus (Liu et al., NeurIPS 2023; arXiv:2305.01210) | HumanEval; MBPP | Use **HumanEval+ / MBPP+** augmented tests as the primary code-generation evaluation | Official HumanEval+/MBPP+ test suites and harness; or the EvalPlus method applied to the criticized benchmark and used as the main evaluation |
| **P2** | SWE-bench+ (Aleithan et al., arXiv:2410.06992) | SWE-bench; SWE-bench Lite; SWE-bench Verified | Use the **SWE-bench+ 548-instance curated dataset and/or its strengthened-test protocol** as the primary SWE-bench evaluation | Official SWE-bench+ 548-instance dataset; or the paper's documented filtering + strengthened-test protocol applied to the criticized benchmark as the main evaluation |

### 2.2 Secondary contrast

| ID | Critique | Criticized benchmark | Recommended practice | Use |
|---|---|---|---|---|
| **S1** | GSM1k (Zhang et al., arXiv:2405.00332) | GSM8K | Use GSM1k or a fully equivalent contamination-controlled replication as the primary arithmetic evaluation | Secondary task-fit contrast only; **never pooled** into the primary estimate |

### 2.3 What is not a recommended practice

- A different contamination-controlled benchmark (LiveCodeBench, SWE-bench Verified, SWE-rebench, etc.) used instead of the critique's artifact.
- An independently designed stronger test suite, filtering rule, or leakage check that is not the critique's artifact/protocol.
- Merely citing the critique in related work or future work.
- Using the critique's artifact only to analyze errors after the main evaluation, unless the artifact is also used for the main evaluation.

These may be good practice, but they are **independent remediation**, not diffusion. Code them as 0 or 1 according to engagement, and set `independent_remediation=yes`.

---

## 3. Eligibility (decide before scoring)

A paper is eligible only if **all three** hold:

| ID | Condition | Failure code |
|---|---|---|
| **E1** | The paper reports empirical evaluation results on the criticized benchmark: HumanEval, MBPP, SWE-bench, SWE-bench Lite, or SWE-bench Verified. | `INELIGIBLE_NO_EVAL` |
| **E2** | The paper contains a bibliographic citation to the critique paper (reference list or official artifact citation). | `INELIGIBLE_NO_CITATION` |
| **E3** | A full text is available in English with enough methods/results detail to code. | `UNCODABLE_ACCESS` / `UNCODABLE_LANGUAGE` |

### 3.1 E1 details

- "Reports empirical evaluation results" means a table, figure, or numeric result for the criticized benchmark. A mention in related work, a dataset description, or a future-work plan is not enough.
- A paper that evaluates a **derivative** benchmark (SWE-bench Pro, CWEval, etc.) but not SWE-bench/Lite/Verified is **ineligible**. A paper that evaluates both the original and a derivative is eligible; code the original.
- A paper that constructs a new benchmark by sampling problems from HumanEval+ or MBPP+ is eligible only if it reports evaluation results on those sampled problems (the criticized benchmark's problems). Record `derived_benchmark=yes`.
- A paper that evaluates GSM8K is not eligible for the primary pairs; it belongs to the secondary GSM1k contrast.

### 3.2 E2 details

- The citation may be to the arXiv version, the proceedings version, or the official artifact (DOI/GitHub/Zenodo). Record `citation_type=paper/artifact/both`.
- A paper that uses HumanEval+ but cites only the GitHub repository and not the paper is a boundary case. If it is in the frame via S2, it has a paper citation; if not, it is out of frame. Do not add papers to the frame manually.
- Self-citation counts as a citation; flag `author_overlap=yes`.

### 3.3 E3 details

- Use the publisher PDF, arXiv, author copy, or institutional access.
- HTML-only is acceptable if methods/results are readable; record `html_only=yes`.
- If the full text is unavailable, code `UNCODABLE_ACCESS`; do not infer eligibility or score from the abstract.
- If the paper is not in English, code `UNCODABLE_LANGUAGE`; report the count.

### 3.4 Ineligibility is not a score

Do not assign 0 to an ineligible paper. `0` means "eligible, cited, but no engagement/adoption." Ineligible papers are reported separately in the flow diagram.

---

## 4. Ordinal adoption score (eligible papers only)

### 4.1 Scale

| Score | Label | Definition | Decision test |
|---:|---|---|---|
| **0** | Citation only | The critique appears in the reference list, but the body does not discuss its specific finding or recommendation; the criticized benchmark is used unchanged. A generic mention of "contamination," "leakage," or "test quality" in a citation cluster, without the critique's specific finding, is 0. | Is there a specific sentence about what the critique found or recommended? If no → 0. |
| **1** | Acknowledged | The body mentions the critique's specific finding (test insufficiency, solution leakage, contamination) but the evaluation of the criticized benchmark is unchanged: original instances/tests, no filtering, no augmented tests, no contamination-controlled replication. | Is the finding discussed but the evaluation unchanged? → 1. |
| **2** | Partial adoption | At least one recommended practice is applied to the criticized benchmark, but not the core remediated artifact/protocol for the main results. Examples: HumanEval+ only in an appendix/robustness check while the main table uses HumanEval; SWE-bench+ filtering applied to a subset or a secondary analysis; GSM1k only as a robustness check. | Is the recommended practice present but not used for a main claim? → 2. |
| **3** | Full adoption | The core remediated artifact/protocol is used for the paper's primary evaluation of the criticized benchmark, with at least one reported result and the critique cited as the basis. | Does the recommended artifact/protocol support at least one main table/figure/claim? → 3. |

**Binary primary outcome:** full adoption = 3. Scores 0–2 are non-adoption for the primary estimate. Partial adoption is reported separately and tested as a sensitivity analysis (2+3 vs 0+1).

### 4.2 Score 0 — citation only

Use 0 when:

- The critique is only in the reference list.
- The body cites it in a generic cluster (e.g., "contamination is a concern [1,2,3]") without stating what the critique found or recommended.
- The body mentions the critique's name only as a benchmark/tool, without discussing its finding.
- The paper evaluates the criticized benchmark unchanged and does not acknowledge the critique's specific limitation.

**Evidence requirement:** quote the reference entry or the generic citation context; state that no specific in-text engagement exists.

### 4.3 Score 1 — acknowledged

Use 1 when:

- The body states the critique's specific finding (e.g., "EvalPlus shows HumanEval's tests are insufficient"; "Aleithan et al. find solution leakage in SWE-bench").
- The paper's evaluation still uses the original benchmark unchanged: original HumanEval/MBPP tests, original SWE-bench/Lite/Verified instances, no filtering, no augmented tests, no contamination-controlled replication.
- The critique is used as background, motivation, or a limitation, not as the evaluation protocol.

**Evidence requirement:** quote the sentence that states the finding and the methods sentence/table that shows the original benchmark was used.

### 4.4 Score 2 — partial adoption

Use 2 when the recommended practice is present but not core to the main results:

- HumanEval+ or MBPP+ is used only in an appendix, robustness check, or secondary table while the main results use HumanEval/MBPP.
- SWE-bench+ filtering/548-instance set is applied only to a subset, a secondary analysis, or a robustness check while the main SWE-bench results use the original benchmark.
- The paper uses the critique's protocol for one benchmark but not another, and the adopted use is not the main claim.
- The paper reports both original and augmented results but presents the augmented result only as a sanity check, not as a main claim.

**Evidence requirement:** quote the methods/table that shows the recommended practice and the main table that shows the original benchmark as primary.

### 4.5 Score 3 — full adoption

Use 3 when:

- HumanEval+ and/or MBPP+ is the main code-generation benchmark, with reported pass rates/results, and EvalPlus is cited as the basis.
- The SWE-bench+ 548-instance dataset or its documented filtering + strengthened-test protocol is the main SWE-bench evaluation, with reported results, and SWE-bench+ is cited as the basis.
- The paper uses the critique's artifact/protocol for at least one main table, figure, or claim, even if it also reports the original benchmark for comparison.
- The paper uses the protocol (not necessarily the exact released file) and documents that it follows the critique's filtering/test-strengthening method.

**Evidence requirement:** quote the main table caption or methods sentence naming the recommended artifact/protocol and the critique; quote at least one reported result.

### 4.6 What is not full adoption

- Using HumanEval+ problems but not the augmented tests, unless the augmented tests are used for at least one main claim. If only the problems are used, score 2.
- Using SWE-bench+ only to analyze errors after the main evaluation. Score 2 if the analysis is secondary; 0/1 if there is no evaluation use.
- Using a different contamination-controlled benchmark (LiveCodeBench, SWE-bench Verified, SWE-rebench) instead of the critique's artifact. Score 1 if the critique's finding is discussed; 0 if not; `independent_remediation=yes`.
- Claiming to use HumanEval+ but reporting only original HumanEval numbers. Score 1 or 2 depending on what is documented; do not infer execution.

---

## 5. Boundary rules and worked cases

### 5.1 Rule: citation is not adoption

A reference-list entry alone is 0. A paper can cite EvalPlus 20 times and still score 0 if it never engages with the test-insufficiency finding or uses the artifact.

### 5.2 Rule: generic contamination talk is not acknowledgment

If the paper says "contamination is a concern" and cites the critique in a cluster, but never states the critique's specific finding or implication for its own evaluation, score 0. This rule resolves the pilot's `promptcot` disagreement toward 0.

### 5.3 Rule: acknowledgment requires specificity

A sentence that names the critique's finding (e.g., "Liu et al. report gaps in HumanEval's test sets") and leaves the evaluation unchanged is 1. The pilot's `calibration` is the model case.

### 5.4 Rule: independent remediation is not adoption

An independently designed stronger test suite or leakage check is not adoption, even if it addresses the same problem. Score 1 if the critique's finding is discussed, 0 if not; set `independent_remediation=yes`. The pilot's `reagent` (own leakage analysis) and `utboost` (own UTBoost) are model cases.

### 5.5 Rule: partial vs full depends on the main evaluation

If the recommended artifact is only a secondary check, score 2. If it supports at least one main claim/table/figure, score 3. Do not average across benchmarks; use the highest-adoption main use.

### 5.6 Rule: both original and augmented as co-primary

Score 3 if the augmented result supports at least one main claim; otherwise 2. Record `co_primary=yes` and `benchmark_coverage=full/partial`.

### 5.7 Rule: derivative-only papers are ineligible

SWE-bench Pro, CWEval, and other derivatives do not count as evaluating SWE-bench/Lite/Verified. A paper that evaluates both the original and a derivative is eligible; code the original. The pilot's `swebenchpro` and `cweval` are ineligible for this reason.

### 5.8 Rule: benchmark version

Record `benchmark_version` (HumanEval+ v0.1/v0.2/v0.3; MBPP+; SWE-bench+ 548). Do not change the score solely because the version differs, unless the paper explicitly uses a different construct. Report version distribution.

### 5.9 Rule: code inspection

Record `artifact_check=yes/no`. Code inspection can corroborate documented use but cannot upgrade a score on its own. The construct is documented adoption. If code shows use that the paper does not document, record it in `notes` but do not change the score; run a sensitivity analysis if many such cases appear.

### 5.10 Rule: self-citation

Code normally. Set `author_overlap=yes` if any critique author is an author of the citing paper. Run a sensitivity analysis excluding these papers. Do not exclude them from the primary analysis.

### 5.11 Rule: unresolved ambiguity

Set `confidence=low` and `adjudicate=yes`. The second coder codes independently. If consensus fails, use a third coder or the conservative (lower) score; document the rationale. Do not split the difference.

### 5.12 Worked pilot cases

| Paper | Critique | Score | Why |
|---|---|---:|---|
| `whatswrong` (Dou et al., *What is Wrong with Your Code Generated by LLMs?*) | EvalPlus | **3** | Uses HumanEval+ and MBPP+ as main benchmarks, including augmented tests (164 and 399 problems), and reports pass rates. |
| `utboost` (Yu et al., *UTBoost*) | SWE-bench+ | **1** | Discusses incorrect patches and Aleithan et al., but says it cannot directly apply EvalPlus to SWE-bench and proposes its own UTBoost; no SWE-bench+ dataset/protocol adoption. `independent_remediation=yes`. |
| `schrodinger` (Chen et al., *Have LLMs Learned SWE-bench or Memorized It?*) | SWE-bench+ | **1** | Cites SWE-bench+ as an enhancement, but uses its own repository transformations on SWE-bench Verified; no SWE-bench+ dataset/protocol adoption. `independent_remediation=yes`. |
| `calibration` (Spiess et al., *Calibration and Correctness of Language Models for Code*) | EvalPlus | **1** | States that Liu et al. report gaps in HumanEval's tests, but evaluates original HumanEval; no augmented tests. |
| `reagent` (Kuang et al., *REAgent*) | SWE-bench+ | **0** | Aleithan et al. appears only in the reference list; the paper's leakage analysis is independent, not presented as following SWE-bench+. `independent_remediation=yes`. |
| `correctness_internal` (Bui et al., *Correctness Assessment of Code Generated by LLMs Using Internal Representations*) | EvalPlus | **0** | Liu et al. appears in the reference list; the paper evaluates original HumanEval/MBPP and does not discuss the test-insufficiency finding. |
| `promptcot` (Zhao et al., *PromptCoT*) | GSM1k (secondary) | **0** | Cites Zhang et al. 2024 in a generic memorization cluster; evaluates GSM8K unchanged; no specific GSM1k finding/recommendation. Pilot disagreement: second coder proposed 1; adjudicated 0 under the generic-cluster rule. |
| `understand_translate` (Ko et al., *Understand, Solve and Translate*) | GSM1k (secondary) | **1** | Cites Zhang et al. in a generic contamination sentence; runs its own contamination check on the KSM subset, not GSM1k; evaluates GSM8K/translated data unchanged. `independent_remediation=yes`. |
| `hafix` (Shi et al., *HAFix*) | SWE-bench+ | **ineligible** | Cites Aleithan et al. in a generic bug-fixing list; does not evaluate SWE-bench/Lite/Verified. |
| `swebenchpro` (Deng et al., *SWE-Bench Pro*) | SWE-bench+ | **ineligible** | Evaluates SWE-bench Pro, a derivative, not SWE-bench/Lite/Verified. |
| `cweval` (Peng et al., *CWEval*) | EvalPlus | **ineligible** | Evaluates its own CWEval benchmark; cites EvalPlus only as future work. |
| `demystifying` (Lu et al., *Demystifying Small Language Models for Edge Deployment*) | GSM1k (secondary) | **ineligible** | Cites Zhang et al. in a generic claim; does not evaluate GSM8K/GSM1k. |

---

## 6. Coding procedure

1. **Read title and abstract.** Assign a preliminary eligibility flag. Do not assign a score from the abstract.
2. **Retrieve full text.** Confirm E1–E3. If unavailable, code `UNCODABLE_ACCESS`.
3. **Search for the critique.** Author names, title, arXiv ID, artifact name, benchmark `+` variants. Record every citation locus.
4. **Read the context.** ±2 paragraphs around each citation, plus methods, main results tables, and captions.
5. **Assign the score.** Use the decision tests in §4.1. Record the highest-adoption main use.
6. **Record secondary fields.** Engagement, independent remediation, adoption locus, versions, author overlap, artifact check, confidence, access route.
7. **Record evidence.** A verbatim quote ≤60 words, with section/table. For 0, quote the reference entry or generic context.
8. **Flag ambiguity.** `adjudicate=yes`, `confidence=low`. Do not guess.
9. **Do not use metadata to infer adoption.** Citation counts, venue prestige, and author reputation are not evidence.
10. **Audit.** After calibration, re-code a 10% random sample of the first coder's work; log discrepancies.

### 6.1 Search strings

Use case-insensitive searches for:

- `EvalPlus`, `EvalPlus+`, `HumanEval+`, `HumanEvalPlus`, `MBPP+`, `MBPPPlus`
- `SWE-bench+`, `SWE-Bench+`, `SWE-bench Plus`, `SWE-bench+ 548`
- `GSM1k`, `GSM-1k`, `GSM1K`
- Author surnames: `Liu`, `Xia`, `Wang`, `Zhang` (EvalPlus); `Aleithan`, `Xue`, `Mohajer`, `Nnorom`, `Uddin`, `Wang` (SWE-bench+); `Zhang`, `Da`, `Lee` (GSM1k)
- arXiv IDs: `2305.01210`, `2410.06992`, `2405.00332`

Do not rely on a single search string; PDF extraction can break `+` and hyphens.

### 6.2 Evidence standard

- Quote must be verbatim, ≤60 words, and sufficient for an independent auditor to see why the score was assigned.
- For 3, the quote must name the recommended artifact/protocol and a main result.
- For 2, the quote must show the artifact/protocol and that it is secondary.
- For 1, the quote must show the specific finding and the unchanged evaluation.
- For 0, the quote must show the reference entry or generic context and the absence of specific engagement.
- If no quote can support the score, the score is not ready; flag for adjudication.

---

## 7. Coding form and schema

### 7.1 CSV columns

```
cluster_id,title,year,venue,doi,arxiv,critique,eligible,ineligibility_reason,score,
engagement,independent_remediation,adoption_locus,benchmark_variant,benchmark_version,
critique_version,author_overlap,artifact_check,confidence,access_route,evidence_quote,
notes,coder_id,coded_at
```

### 7.2 Field definitions

| Field | Type | Values / notes |
|---|---|---|
| `cluster_id` | string | Frame ID (`C0001`…). |
| `title` | string | Representative title. |
| `year` | integer/blank | Publication year. |
| `venue` | string | Venue or `unknown`. |
| `doi` | string/blank | DOI. |
| `arxiv` | string/blank | arXiv ID. |
| `critique` | enum | `evalplus`, `swebenchplus`, `gsm1k`. |
| `eligible` | boolean | E1–E3 all true. |
| `ineligibility_reason` | enum/blank | `NO_EVAL`, `NO_CITATION`, `ACCESS`, `LANGUAGE`, `DUPLICATE`. |
| `score` | integer/blank | 0–3 for eligible; blank otherwise. |
| `engagement` | integer | 0 = reference only; 1 = brief mention; 2 = substantive. |
| `independent_remediation` | boolean | Own mitigation, not the critique's artifact. |
| `adoption_locus` | enum | `main_results`, `secondary_results`, `appendix`, `future_work`, `related_work`, `none`. |
| `benchmark_variant` | string | `humaneval`, `mbpp`, `swebench`, `swebench_lite`, `swebench_verified`, `gsm8k`. |
| `benchmark_version` | string | e.g., `evalplus-v0.3.1`, `swebenchplus-548`. |
| `critique_version` | string | `arxiv-v1`, `arxiv-v2`, `neurips-2023`, `zenodo-13879453`, `hf-gsm1k`. |
| `author_overlap` | boolean | Any critique author is a paper author. |
| `artifact_check` | boolean | Code/repo inspected. |
| `confidence` | enum | `high`, `medium`, `low`. |
| `access_route` | enum | `publisher`, `arxiv`, `author_copy`, `repository`, `ill`, `html`. |
| `evidence_quote` | string | ≤60 words, verbatim. |
| `notes` | string | Boundary reasoning. |
| `coder_id` | string | `C1`, `C2`, etc. |
| `coded_at` | date | ISO date. |

### 7.3 JSON schema (one record)

```json
{
  "cluster_id": "C0001",
  "title": "...",
  "year": 2025,
  "venue": "...",
  "doi": "...",
  "arxiv": "...",
  "critique": "evalplus",
  "eligible": true,
  "ineligibility_reason": "",
  "score": 3,
  "engagement": 2,
  "independent_remediation": false,
  "adoption_locus": "main_results",
  "benchmark_variant": "humaneval",
  "benchmark_version": "evalplus-v0.3.1",
  "critique_version": "neurips-2023",
  "author_overlap": false,
  "artifact_check": false,
  "confidence": "high",
  "access_route": "arxiv",
  "evidence_quote": "...",
  "notes": "...",
  "coder_id": "C1",
  "coded_at": "2027-01-20"
}
```

---

## 8. Reliability

| Element | Specification |
|---|---|
| Sample | 20% of eligible papers, stratified by critique and score band (26 base / 16 reduced). No separate minimum-20 rule. |
| Blindness | Second coder receives a packet without the first coder's score; codes independently. |
| Eligibility agreement | Percent agreement + Cohen's κ. |
| Ordinal agreement | Percent agreement + unweighted κ + linear-weighted κ. |
| Low prevalence | Report PABAK if full adoption <10%; κ alone is unstable. |
| CIs | Bootstrap 95% CIs (1,000–10,000 resamples). |
| Threshold | Weighted κ ≥0.60 acceptable; 0.40–0.59 moderate with limitation; <0.40 retrain/recode. |
| Adjudication | Discussion; if unresolved, third coder or conservative lower score. |
| LLM | Pre-screening/audit only; never human reliability. Report model, prompt, temperature, agreement. |

**Pilot note:** the pilot's 0.78 unweighted / 0.86 linear-weighted κ are **LLM–LLM agreement** on 8 eligible papers, not human reliability. They are used only to debug the rubric. The primary-pair subset had no ordinal disagreements (6/6), but n=6 is too small to estimate reliability; do not report 1.00 as a reliability result.

---

## 9. Changes from v1.0 to v1.1

| # | Change | Reason | Effect on pilot |
|---:|---|---|---|
| 1 | GSM1k explicitly excluded from primary scoring; separate secondary file. | Task fit, availability timing, license ambiguity. | `promptcot` and `understand_translate` excluded from primary estimate. |
| 2 | Generic contamination/leakage mention in a citation cluster = 0, not 1. | The v1.0 "acknowledged" rule was ambiguous; caused `promptcot` disagreement. | `promptcot` adjudicated 0; rule now explicit. |
| 3 | Derivative-only papers are ineligible, not 0. | SWE-bench Pro/CWEval do not evaluate the criticized benchmark. | `swebenchpro`, `cweval` ineligible. |
| 4 | Full adoption requires the recommended artifact/protocol to support at least one main claim. | Prevents appendix/robustness use from counting as full. | `whatswrong` remains 3 (main benchmarks); no pilot change. |
| 5 | Both original and augmented as co-primary: 3 only if augmented supports a main claim; otherwise 2. | Clarifies a common design. | No pilot case; future rule. |
| 6 | Using HumanEval+ problems but not augmented tests = 2, not 3. | The artifact includes the tests, not just the problems. | No pilot change; `whatswrong` uses augmented tests. |
| 7 | Independent remediation explicitly separated; 2 only if the critique's protocol is used, not any improvement. | Keeps the construct about diffusion. | `reagent`, `utboost`, `schrodinger` remain 0/1 with flag. |
| 8 | Add `benchmark_version`, `critique_version`, `author_overlap`, `artifact_check`, `confidence`, `access_route`. | Version drift, self-citation, audit, access bias. | New fields; pilot table backfilled where possible. |
| 9 | Evidence quote and locus required for every score; no score ≥1 from abstract alone. | Auditability. | Pilot quotes recorded. |
| 10 | PABAK and prevalence-aware reliability guidance. | κ is unstable when adoption is rare. | New reliability plan. |
| 11 | Conservative lower score for unresolved adjudication; no averaging. | Prevents inflated adoption. | New rule. |
| 12 | LLM role limited to pre-screening/audit; no paywalled full texts to external APIs. | Ethics and construct validity. | Pilot LLM use documented as non-human. |

---

## 10. Freeze and amendment policy

- Rubric v1.1 is frozen at OSF registration.
- After main coding begins, changes require a dated amendment with reason and impact; affected papers are recoded if the change is material.
- Do not silently change scoring rules after seeing results.
- The pilot's v1.0 codes remain in `pilot/pilot_coding_table.csv` for audit; they are not overwritten.
