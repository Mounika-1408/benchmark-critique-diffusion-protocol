# Journal Comparison

**Verified:** 13 November 2026. Re-verify before submission.  
**Source of record:** `verification/journal_requirements.md`.

## Comparison matrix

| Requirement / fit | EMSE | DMLR | Scientometrics | QSS | TMLR |
|---|---|---|---|---|---|
| Publisher / system | Springer Nature | OpenReview | Springer Nature | MIT Press | OpenReview |
| Review model | Single-blind | Single-blind | Single-blind | Unknown (page blocked) | Double-blind |
| Abstract limit | 150–250 words | Not specified | 150–250 words | Unknown | Not specified |
| Data availability statement | Required for original research | Expected under open-data policy | Supported/required | Unknown | Expected |
| Mandatory fee | No mandatory submission fee stated; hybrid Open Choice optional | No fees | Hybrid subscription route | APC unresolved (third-party reports conflict) | No fee stated |
| Page limit | Journal norm | None | Journal norm | Unknown | Variable |
| Open access | Optional | Yes, no cost | Optional | Yes (APC unresolved) | Yes |
| Fit for two-pair citation audit | Strong | Strong | Moderate; requires reframing | Moderate; requires reframing | Weak |
| Verdict | **Primary** | **Alternative** | Reframe only | Defer | Not recommended |

## EMSE (primary)

**Why:** Applied software engineering with a strong empirical component; the
object is evaluation practice around HumanEval, MBPP, and SWE-bench. EMSE values
replicable or expandable studies, and the frozen frame, rubric, and scripts are
designed for replication. The verified median submission-to-first-decision is 24
days (2025 metrics).

**Risk:** Editors may classify a citation audit as meta-science or bibliometrics.
The cover letter and introduction must lead with the SE consequence: claims about
code-generation progress rest on benchmarks whose known defects are often cited
but not acted on.

## DMLR (alternative)

**Why:** Scope explicitly includes benchmarks, benchmarking tools and methods, and
empirical evaluation of data practices. No fees, no page limit, open access. The
coding instrument and frame are reusable data-centric products.

**Risk:** Reviewers may want a data-centric intervention rather than an audit. The
4–6 month turnaround is longer than EMSE's median first decision.

## Scientometrics (reframe only)

**Why:** Diffusion from citation to practice is a science-of-science question.

**Risk:** The two-pair design is narrow for a bibliometrics journal. A
Scientometrics version would need citation-network context, field normalization,
or a broader benchmark set. It is a different paper, not a drop-in fallback.

## QSS (defer)

**Why:** Natural science-of-science audience and open access.

**Risk:** The submission pages returned HTTP 403 on 2026-11-13; the APC and format
requirements are unresolved. Do not commit to QSS without checking the official
pages in a normal browser.

## TMLR (not recommended)

TMLR expects an ML contribution. A citation audit is not an ML method or benchmark
contribution in TMLR's sense. Submitting there would invite requests for work the
study does not contain.

## Decision rule

1. If the full study is completed and human reliability is reported, submit to
   EMSE first.
2. If EMSE desk-rejects for scope, submit to DMLR.
3. Reframe for Scientometrics or QSS only with additional bibliometric analysis.
4. Do not submit the current pilot draft to any venue as a full-scale study.
