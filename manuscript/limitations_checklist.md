# Limitations and Submission-Readiness Checklist

**Status:** pilot-based draft. This file separates limitations that are acceptable
for a pilot methods paper from limitations that block submission as a full-scale
empirical study.

## A. Limitations of the pilot evidence

| # | Limitation | Status | Where documented |
|---:|---|---|---|
| 1 | Purposive, non-probability 29-paper pilot; 12 coded; 6 primary-pair eligible | Open; by design | `pilot/pilot_summary.md`; paper §11.2, §18 |
| 2 | No human second coder; κ values are LLM–LLM only | **Blocking for a prevalence claim** | paper §12.5, §17.6, §18 |
| 3 | Exact LLM model, prompt, temperature, and raw outputs not preserved | Open; reproducibility gap | paper §12.5, §17.6 |
| 4 | Full-scale 900-paper study not executed | **Blocking for a full-scale paper** | paper §11.1, §18 |
| 5 | 335-record feasibility cohort drawn but not coded; retrieval halted | Documented deviation | paper §11.5; `reproducibility/sampling.md` |
| 6 | 93.1% access rate is purposive and not generalizable | Open | paper §11.2, §11.5; `pilot/pilot_summary.md` |
| 7 | Documented adoption is not verified execution | Construct limitation | paper §17.1 |
| 8 | No time-cohort or venue analysis; pilot is 2025-heavy | Not analyzed | paper §14.4 |
| 9 | Pair contrast has three papers per side | Not powered | paper §13.4, §14.3 |
| 10 | No page numbers for every pilot quote | Fix in full study | paper §12.4 |
| 11 | Four ineligible papers illustrate boundary rules but are not outcomes | Correctly excluded | paper §11.4 |

## B. Limitations of the frame

| # | Limitation | Status | Where documented |
|---:|---|---|---|
| 12 | Semantic Scholar snapshot; misses non-indexed venues | Open | paper §10.4 |
| 13 | 2026 incomplete; 231 future-dated records | Reported, not dropped | paper §10.3 |
| 14 | 225 records without a publication date | Reported | paper §10.3 |
| 15 | 42 records with no DOI/arXiv/DBLP | Reported | paper §10.3 |
| 16 | 14 multi-variant clusters need manual review | Open | paper §10.3, §10.4 |
| 17 | Title clustering may merge distinct works with identical titles | Sensitivity frame: 2,684 | paper §17.2 |
| 18 | No post-freeze citation refresh | By design | paper §10.4 |

## C. Claims that must not be made

- Do not call the pilot a prevalence estimate.
- Do not call the LLM–LLM κ human reliability.
- Do not call the protocol preregistered or registered.
- Do not describe the 900-paper design as executed.
- Do not generalize the 93.1% access rate.
- Do not infer causation from citation co-occurrence.
- Do not describe the manuscript as peer reviewed or accepted.
- Do not pool GSM1k into the primary denominator.
- Do not treat the zero placeholders for ineligible papers as outcomes.

## D. Submission readiness

| Requirement | Status | Action needed |
|---|---|---|
| Complete manuscript draft | **Met for pilot draft** | Revise after full study or reframe as methods/pilot paper. |
| Abstract 150–250 words | **Met** (within limit; recheck after edits) | Recheck after edits. |
| References and BibTeX | **Met for pilot** | Add any new full-study sources. |
| Figures and tables | **Met** | Regenerate after analysis changes. |
| Data availability statement | **Met** | Update repository DOI/commit at release. |
| Code availability | **Met** | Add environment lock if dependencies are introduced. |
| Human reliability | **Not met** | Recruit a human second coder; report human agreement. |
| Full-scale results | **Not met** | Execute the 900-paper design and analyses. |
| OSF registration / DOI | **Not met** | Register before main coding; obtain DOI. |
| Ethics/IRB determination | **Not documented** | Confirm local policy for public-text research. |
| LLM-use disclosure | **Met with caveat** | Full study must preserve model metadata. |
| Author affiliation and contact | **Partially met** | Confirm public contact and affiliation wording. |
| Venue requirements re-verified at submission | **Pending** | Re-check live pages; do not rely on 2026-11-13 snapshot. |
| Cover letter | **Draft only** | Complete after full study; do not send current draft. |
| Reviewer suggestions | **Not prepared** | Use expertise categories; do not fabricate names. |

## E. Honest bottom line

The repository is complete as **research infrastructure plus a pilot-based draft**.
It is not a complete full-scale empirical study. The binding constraints are the
missing human second coder and the unexecuted full-scale data collection. No amount
of rewriting can substitute for those two inputs.
