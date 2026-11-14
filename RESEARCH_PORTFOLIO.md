# Research Portfolio Entry

## Project

**Does Benchmark Critique Diffuse into Evaluation Practice? A Pilot-Based Study of
EvalPlus and SWE-bench+ Adoption**

**Author:** Syed Abdul Aman (Independent Researcher)  
**Status:** Pilot-based research draft; not a completed full-scale study; not submitted.  
**Date:** 13 November 2026  
**Repository:** https://github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol

## One-paragraph summary

Benchmark critiques identify defects in widely used evaluations and release
remediations, but citation counts do not show whether citing papers change
practice. This project builds a frozen 2,666-cluster citation frame for EvalPlus
and SWE-bench+, a four-level coding rubric for documented adoption, and a
purposive 29-paper pilot. In the pilot, 27 full texts were accessible, 12 papers
were coded, 8 were eligible for the all-pair set, and 6 were eligible for the two
primary pairs. One primary-pair paper fully adopted its critique's remediation
(1/6, 16.7%; Wilson 95% CI 3.0–56.4%), while three acknowledged the finding
without adopting the artifact. The pilot shows that citation, acknowledgment,
and adoption are distinguishable; it does not estimate prevalence.

## Contribution

1. **Measurement instrument.** A four-level rubric that separates citation only,
   acknowledgment, partial adoption, and full adoption, with explicit boundary
   rules for generic contamination talk, independent remediation, derivative
   benchmarks, and main-versus-secondary use.
2. **Frozen frame.** A reproducible 2,666-cluster citation frame with strata,
   identifier coverage, anomaly counts, and SHA-256 hashes.
3. **Pilot evidence.** A 12-row coding table with short quotes and documented
   boundary decisions, plus generated tables and figures.
4. **Transparent documentation of incomplete work.** The full-scale 900-paper
   study was designed but not executed; a 335-record feasibility cohort was
   drawn, partially retrieved, and halted without coding. Both facts are
   documented rather than omitted.

## Evidence and verification

| Claim | Evidence |
|---|---|
| Frame has 2,666 title clusters | `data/citation_frame_2666.csv`; `data/frame_summary.json`; `tests/test_frame.py` |
| Pilot flow 29 → 27 → 12 → 8 → 6 | `pilot/pilot_summary.md`; `analysis/pilot_results.json`; `tests/test_pilot.py` |
| Primary full adoption 1/6 (16.7%; 3.0–56.4%) | `analysis/pilot_results.json`; `manuscript/tables/table4_pilot_scores.md` |
| All-pair full adoption 1/8 (12.5%; 2.2–47.1%) | `analysis/pilot_results.json`; `manuscript/tables/table4_pilot_scores.md` |
| Reliability is LLM–LLM only | `analysis/pilot_results.json`; `manuscript/paper.md` §12.5 |
| Frame and pilot hashes | `reproducibility/checksums.sha256`; `scripts/verify_checksums.py` |

Reproduce with:

```powershell
python -m pytest tests -q
python scripts/verify_checksums.py
```

## Methods at a glance

- **Frame:** Semantic Scholar citations to EvalPlus (arXiv:2305.01210) and
  SWE-bench+ (arXiv:2410.06992), retrieved 13 November 2026; identifier
  deduplication (2,684) then title clustering (2,666).
- **Strata:** 135 SWE-bench+ census clusters (including 23 citing both critiques)
  and 2,531 EvalPlus-only clusters.
- **Pilot:** purposive 29-paper access frame; 27 accessible; 12 coded; 8 eligible
  all-pair; 6 eligible primary-pair.
- **Instrument:** rubric v1.1, frozen on 13 November 2026 for the planned study.
- **Analysis:** counts, Wilson intervals, exact-binomial diagnostics labeled
  descriptive only.

## What is not claimed

- No population prevalence estimate.
- No causal effect of critique on adoption.
- No human inter-rater reliability.
- No full-scale results.
- No peer review, registration, or DOI.
- No generalization of the 93.1% pilot access rate.

## What would make this a full study

1. Register the protocol (OSF or equivalent) and obtain a DOI.
2. Run a 50-record access pretest on the frozen frame.
3. Draw the 900-paper stratified sample (or the documented stop-rule extension).
4. Human double-code at least 20% of eligible papers; report human κ.
5. Execute the pre-specified sensitivity analyses and design-weighted estimate.
6. Revise the manuscript from pilot-based draft to full empirical study.
7. Submit to EMSE (primary) or DMLR (alternative) after re-verifying requirements.

## Skills demonstrated

Research design under uncertainty; construct operationalization; citation-frame
construction and deduplication; rubric development and boundary adjudication;
reproducible analysis with standard-library Python; dependency-free figure
generation; research-integrity documentation; transparent reporting of incomplete
work; Git/GitHub packaging and a reproducible test suite.

## Links

- [Manuscript](manuscript/paper.md)
- [Abstract](manuscript/abstract.md)
- [Protocol](PROTOCOL.md)
- [Rubric](rubric_v1.1.md)
- [Reproducibility package](reproducibility/README.md)
- [Limitations checklist](manuscript/limitations_checklist.md)
- [Submission status](manuscript/submission/submission_checklist.md)
