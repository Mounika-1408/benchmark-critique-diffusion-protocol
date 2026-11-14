# Rubric v1.0 → v1.1: Change Log and Rationale

**Frozen:** 13 November 2026  
**Basis:** Pilot coding of 12 papers, one ordinal disagreement (`promptcot`), and a review of boundary cases.

---

## 1. Why a revision was needed

Rubric v1.0 was usable but left four decisions under-specified:

1. **Generic citation clusters.** A paper that cites a critique in a list of contamination references could be scored 0 (citation only) or 1 (acknowledged). The pilot's `promptcot` case split exactly this way.
2. **Derivative benchmarks.** It was unclear whether a paper evaluating SWE-bench Pro or CWEval was eligible for the SWE-bench+ or EvalPlus pair.
3. **Partial vs full.** It was unclear whether using HumanEval+ only in an appendix, or using HumanEval+ problems without the augmented tests, counted as full adoption.
4. **Independent remediation.** The v1.0 boundary rule said independent remediation is not adoption, but did not define when it could be scored 2 versus 1 versus 0.

The revision resolves these before main coding. It does not change the construct.

---

## 2. Changes

| # | v1.0 | v1.1 | Rationale | Pilot impact |
|---:|---|---|---|---|
| 1 | Three pairs, all eligible for the primary estimate. | GSM1k → GSM8K is a **secondary contrast only**; excluded from the primary denominator. | Task fit, release timing (HF full dataset 2025-03-31), license ambiguity, and non-substitutive relationship to GSM8K. | `promptcot`, `understand_translate` move to secondary; primary-pair eligible n becomes 6, not 8. |
| 2 | 0 = citation only; 1 = acknowledged, including a generic finding mention. | A **generic contamination/leakage mention in a citation cluster is 0**, not 1. Acknowledgment requires the critique's specific finding. | Prevents citation padding from counting as engagement; resolves the `promptcot` disagreement. | `promptcot` adjudicated 0. |
| 3 | Eligibility required evaluating the criticized benchmark, but derivative cases were not explicit. | **Derivative-only papers are ineligible** (SWE-bench Pro, CWEval, etc.). A paper evaluating both original and derivative is eligible; code the original. | A derivative is a different benchmark; it cannot show adoption on the criticized benchmark. | `swebenchpro`, `cweval` ineligible. |
| 4 | 3 = core remediated artifact/protocol used for primary evaluation. | 3 requires the artifact/protocol to support **at least one main table, figure, or claim**; appendix/robustness-only is 2. | Makes "main results" operational and auditable. | No pilot change; `whatswrong` remains 3. |
| 5 | Both original and augmented as co-primary was not specified. | If both are co-primary, 3 only if the augmented result supports a main claim; otherwise 2. Record `co_primary=yes`. | Common design in benchmark papers; prevents automatic 3. | New rule; no pilot case. |
| 6 | "Use HumanEval+/MBPP+" was not distinguished from using only the problems. | Using HumanEval+ problems **without the augmented tests** is 2, not 3, unless the augmented tests support a main claim. | The artifact's value is the tests, not just the problem set. | No pilot change; `whatswrong` uses augmented tests. |
| 7 | Independent remediation: "not adoption; code 0 or 1 according to engagement." | 2 only if the critique's **released artifact or documented protocol** is used; an independently designed mitigation is 1 (if the finding is discussed) or 0, with `independent_remediation=yes`. | Keeps the measure about diffusion, not general good practice. | `reagent` 0, `utboost` 1, `schrodinger` 1, all flagged. |
| 8 | Secondary fields: engagement, independent remediation, evidence quote. | Added `benchmark_version`, `critique_version`, `author_overlap`, `artifact_check`, `confidence`, `access_route`, `adoption_locus`. | Version drift, self-citation, auditability, access bias, adjudication triage. | Pilot table backfilled where possible. |
| 9 | Evidence quote required, but abstract-only scoring was not prohibited. | No score ≥1 from abstract alone; every score needs a quote and locus. | Construct validity and audit. | Pilot quotes recorded. |
| 10 | Cohen's κ only. | Added PABAK for low prevalence and bootstrap CIs. | κ is unstable when full adoption is rare (expected ~12.5%). | New reliability plan. |
| 11 | Disagreements resolved by discussion. | If unresolved, third coder or **conservative lower score**; no averaging. | Prevents inflated adoption under ambiguity. | New rule. |
| 12 | LLM role unspecified. | LLM only for pre-screening/audit; never human reliability; no paywalled full texts to external APIs. | Ethics and construct validity. | Pilot LLM use documented as non-human. |
| 13 | Unit of analysis: paper. | Title-level cluster × critique; both-critique papers get two rows; one score per critique based on highest-adoption main use. | Avoids double-counting versions and handles both-critique papers. | No pilot change; clarifies future coding. |
| 14 | No freeze/amendment policy. | Rubric frozen at OSF; post-freeze changes require dated amendment and recoding. | Pre-registration integrity. | New policy. |

---

## 3. What did not change

- The construct: documented adoption, not citation, agreement, or general quality.
- The 0–3 ordinal scale and the binary full-adoption outcome (score 3).
- The eligibility principle: evaluate the criticized benchmark and cite the critique.
- The requirement for a verbatim evidence quote.
- The rule that independent remediation is not adoption.
- The rule that citation alone is 0.

---

## 4. Coding implications

1. **Search the full text, not just the abstract.** Generic clusters are common; the score depends on whether the critique's specific finding is discussed.
2. **Read the main table captions.** Full vs partial often turns on whether the augmented/filtered benchmark appears in the main results.
3. **Record the locus.** `main_results`, `secondary_results`, `appendix`, `future_work`, `related_work`.
4. **Do not upgrade for code.** Code inspection is corroboration, not the construct.
5. **Flag self-citation.** Do not exclude it from the primary analysis; run a sensitivity analysis.
6. **Use the conservative rule.** If two coders cannot agree after discussion, take the lower score and document why.

---

## 5. Unchanged pilot codes

The pilot's v1.0 codes are preserved in `pilot/pilot_coding_table.csv`. The v1.1 rules are applied to the main study; the pilot is not recoded retroactively except for the documented `promptcot` adjudication. This preserves an audit trail of rubric evolution.

---

## 6. Residual ambiguity

The following remain judgment calls and should be flagged `confidence=low`:

- A paper that uses HumanEval+ as the main benchmark but reports only a subset of problems.
- A paper that uses the SWE-bench+ filtering criteria but not the exact 548-instance file.
- A paper that reports the augmented benchmark in a footnote rather than a table.
- A paper that cites the critique only in a limitations paragraph but changes nothing.
- A paper with author overlap that evaluates its own artifact.

These are not reasons to delay the study; they are reasons to double-code and adjudicate.
