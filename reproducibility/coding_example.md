
# Worked Coding Example: Calibration and Correctness of Language Models for Code

This example demonstrates how to apply the eligibility criteria and ordinal
adoption scale in `rubric_v1.1.md`.

The example uses the existing `calibration` row from
`pilot/pilot_coding_table.csv`. It does not add a paper to the study frame or
introduce evidence from material outside the public repository.

## 1. Paper selected

| Field | Recorded value |
|---|---|
| Paper key | `calibration` |
| Title | Calibration and Correctness of Language Models for Code |
| Year | 2025 |
| Critique | EvalPlus |
| Criticized benchmark | HumanEval |
| Pilot eligibility | `true` |
| Pilot score | `1` |
| Engagement | `1` |
| Independent remediation | `false` |

The pilot row records the following evidence quote:

> e.g., Liu et al. [13] report gaps in the test sets of HumanEval.

The pilot notes:

> States the critique's test-gap finding but evaluates original HumanEval; no augmented tests.

## 2. Eligibility decision (E1–E3)

Eligibility must be decided before assigning an adoption score.

| Criterion | Decision recorded or supported by the pilot | Explanation |
|---|---|---|
| E1: Empirical evaluation | Supported by the pilot notes | The row states that the paper evaluates original HumanEval. |
| E2: Critique citation | Recorded as eligible in the pilot | The row identifies EvalPlus and contains an in-text statement about the HumanEval test-gap finding. The exact citation type is not preserved in this row. |
| E3: English full text with sufficient methods/results detail | Recorded as eligible in the pilot, but supporting access details are not preserved | The row does not document whether the full text was obtained from a publisher PDF, arXiv, author copy, institutional access, or readable HTML. |

**Eligibility outcome:** `eligible = true` in the existing pilot table.

**Audit-trail limitation:** The public pilot row does not retain separate evidence for every E1–E3 decision. In particular, it does not independently demonstrate how E3 was verified. This example preserves the recorded pilot decision; it does not claim to have independently re-established full-text access.

If full text cannot be accessed during a new coding exercise, the coder must use `UNCODABLE_ACCESS` rather than infer eligibility or a score from the abstract.

### Citation metadata

The pilot row does not preserve the following additional fields:

- `citation_type`: not documented in the pilot row. The full reference must be checked to distinguish `paper`, `artifact`, or `both`.
- `author_overlap`: not documented in the pilot row. Check author overlap before coding `yes` or `no`.

A self-citation still satisfies the citation criterion; if author overlap is confirmed, record `author_overlap=yes`.

## 3. Ordinal adoption score

**Assigned pilot score: 1 — Acknowledged**

The evidence quote identifies a specific EvalPlus finding: gaps in HumanEval's test sets.

However, the pilot notes state that the paper evaluates original HumanEval and does not use augmented tests.

This matches the score-1 definition:

- The critique's specific finding is acknowledged.
- The criticized benchmark is still evaluated without the recommended augmented tests.
- No partial or full adoption of the recommended EvalPlus practice is recorded.

**Decision:** Score `1`, not `0`, because the evidence goes beyond a reference-list citation or generic mention. It identifies the specific test-gap finding.

**Decision:** Score `1`, not `2` or `3`, because the pilot records no use of HumanEval+ augmented tests.

## 4. Counterfactual boundary cases

The following are hypothetical variants of the same coding situation. They are not claims about what the selected paper actually did.

### Counterfactual A — Score decreases from 1 to 0

Suppose the paper only includes EvalPlus in its reference list and does not discuss the specific HumanEval test-gap finding in the body.

The paper evaluates original HumanEval unchanged.

**Score: 0 — Citation only**

Reason: A reference-list citation alone does not establish acknowledgment. There is no specific discussion of the critique's finding or recommendation.

### Counterfactual B — Score increases from 1 to 2

Suppose the paper uses HumanEval+ augmented tests only in an appendix or robustness check, while its main results continue to use original HumanEval.

**Score: 2 — Partial adoption**

Reason: A recommended practice is applied to the criticized benchmark, but it does not support the main evaluation results.

### Counterfactual C — Score increases from 1 to 3

Suppose the paper uses HumanEval+ augmented tests in its primary evaluation, reports results from those tests in a main table or figure, and cites EvalPlus as the basis for this practice.

**Score: 3 — Full adoption**

Reason: The recommended artifact supports at least one main claim, table, or figure, and the critique is cited as the basis.

## 5. Common misreads

| Potential misread | Correct coding interpretation |
|---|---|
| A paper cites EvalPlus, so it adopted EvalPlus. | Citation alone is not adoption. Check whether the finding is discussed and whether the recommended practice is used. |
| A paper mentions contamination or test quality, so it acknowledged EvalPlus. | Generic contamination or test-quality discussion is not acknowledgment. The specific critique finding must be discussed. |
| A paper discusses the HumanEval test gap, so it partially adopted the recommendation. | Discussion without applying the recommended practice is score 1, not score 2. |
| A paper creates its own stronger tests, so it adopted EvalPlus. | Independent remediation is not adoption of the critique's recommended artifact or protocol. |
| HumanEval+ appears in an appendix, so adoption is full. | Appendix-only use is score 2 when the main results still use original HumanEval. |
| A paper cites only the official GitHub artifact, not the paper. | Check whether the paper is in the predefined frame via S2. Do not add it manually. Record the citation type accurately. |
| The citing paper shares an author with the critique. | Self-citation counts. Record `author_overlap=yes` and flag it for sensitivity analysis. |

## 6. Final coding record

The following reproduces the relevant pilot coding decision without adding unsupported metadata.

| Field | Value |
|---|---|
| `paper_key` | `calibration` |
| `eligible` | `true` |
| `score` | `1` |
| `engagement` | `1` |
| `independent_remediation` | `false` |
| `evidence_quote` | `e.g., Liu et al. [13] report gaps in the test sets of HumanEval.` |
| `citation_type` | Not documented in pilot row |
| `author_overlap` | Not documented in pilot row |

The recorded score is **1 — Acknowledged**. The paper-specific evidence and limitations above should be retained when interpreting this pilot decision.

## 7. Coding principle demonstrated

The example illustrates the central distinction in the protocol:

**Discussing a critique is not the same as adopting its recommended evaluation practice.**

- Score 0: citation without specific engagement.
- Score 1: specific finding acknowledged, evaluation unchanged.
- Score 2: recommended practice applied in a secondary role.
- Score 3: recommended practice supports a main evaluation result.

Eligibility is assessed separately and must never be replaced by an adoption score.
