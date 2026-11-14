# Benchmark Critique Diffusion

**Does citing a benchmark critique mean adopting its remediation?**

This repository contains a pilot-based research draft, the frozen citation frame,
the coding instrument, the pilot evidence, and the reproducibility package for a
study of documented adoption of benchmark remediations in code-generation
evaluation.

> **Status: pilot-based research draft — not a completed full-scale study.**
> The pilot is purposive, the eligible samples are six and eight papers, and the
> agreement statistics are LLM–LLM rather than human inter-rater reliability. The
> project does **not** estimate population prevalence, does **not** establish
> causal diffusion, and is **not** submission-ready. See
> [`manuscript/paper.md`](manuscript/paper.md) and
> [`manuscript/limitations_checklist.md`](manuscript/limitations_checklist.md).

## The question

Benchmark critiques such as EvalPlus and SWE-bench+ identify concrete defects and
release remediations. Citation counts show attention, not practice change. This
project asks:

> Among papers that cite a benchmark critique, what proportion document using the
> critique's recommended artifact or protocol in their own primary evaluation of
> the criticized benchmark?

The coding instrument separates four levels:

| Score | Label | Meaning |
|---:|---|---|
| 0 | Citation only | Reference-list entry; no specific finding discussed; benchmark unchanged. |
| 1 | Acknowledged | Specific finding discussed; evaluation unchanged. |
| 2 | Partial adoption | Remediation used in a secondary role, not the main result. |
| 3 | Full adoption | Remediation supports a main claim/table/figure. |

## What the pilot found

- Purposive 29-paper access frame → 27 accessible (93.1%) → 12 coded → 8 eligible
  for the all-pair set → 6 eligible for the two primary pairs.
- Primary pairs (EvalPlus + SWE-bench+): **1/6 full adoption (16.7%; Wilson 95% CI
  3.0–56.4%)**, 3 acknowledged, 2 citation-only, 0 partial.
- All pairs (including two GSM1k secondary rows): **1/8 full adoption (12.5%;
  2.2–47.1%)**.
- Independent remediation: 3/6 primary-pair papers and 4/8 all-pair papers.
- None of the three SWE-bench+ cases adopted the 548-instance dataset.
- Reliability is **LLM–LLM only**: ordinal agreement 7/8, unweighted κ = 0.78,
  linear-weighted κ = 0.86. It is not human reliability.

These counts demonstrate that citation, acknowledgment, and adoption are
distinguishable. They do not estimate how common adoption is.

## Repository map

| Path | What it is |
|---|---|
| [`manuscript/paper.md`](manuscript/paper.md) | Full pilot-based manuscript draft. |
| [`manuscript/abstract.md`](manuscript/abstract.md) | 150–250 word abstract and keywords. |
| [`manuscript/references.bib`](manuscript/references.bib) | BibTeX entries for cited work. |
| [`manuscript/tables/`](manuscript/tables/) | Six generated tables (Markdown + CSV). |
| [`manuscript/figures/`](manuscript/figures/) | Three dependency-free SVG figures and source CSVs. |
| [`manuscript/submission/`](manuscript/submission/) | Venue comparison, cover-letter draft, checklist, reviewer expertise. |
| [`data/citation_frame_2666.csv`](data/citation_frame_2666.csv) | Frozen 2,666-cluster citation frame. |
| [`data/frame_summary.json`](data/frame_summary.json) | Frame counts, coverage, and SHA-256 hashes. |
| [`pilot/pilot_coding_table.csv`](pilot/pilot_coding_table.csv) | Authoritative 12-row pilot coding table. |
| [`pilot/pilot_summary.md`](pilot/pilot_summary.md) | Pilot flow, results, reliability, and caveats. |
| [`rubric_v1.1.md`](rubric_v1.1.md) | Frozen coding instrument and boundary rules. |
| [`PROTOCOL.md`](PROTOCOL.md) | Full research protocol and planned full-scale design. |
| [`reproducibility/`](reproducibility/) | Data dictionary, provenance, sampling, environment, licensing, checksums, reproduction. |
| [`scripts/`](scripts/) | Frame construction, sampling, pilot analysis, tables, figures, checksums. |
| [`tests/`](tests/) | Bounded integrity and consistency tests. |
| [`verification/`](verification/) | Source verification and journal-requirement records. |
| [`planning/`](planning/) | Feasibility, roadmap, risks, and decision record. |
| [`RESEARCH_PORTFOLIO.md`](RESEARCH_PORTFOLIO.md) | One-page portfolio summary. |

## Verify it

Requires Python 3.11+ and pytest. No network access is needed.

```powershell
python -m pytest tests -q
python scripts/verify_checksums.py
python scripts/analyze_pilot.py
```

Expected: all tests pass, every frozen input matches its checksum, and the pilot
analysis reproduces the counts and intervals reported in the manuscript. See
[`reproducibility/reproduction.md`](reproducibility/reproduction.md).

## What is not included

- Publisher PDFs and full texts: copyright and publisher terms.
- Third-party abstracts (`data/cohort_arxiv_metadata.csv`): excluded to avoid
  redistributing copyrighted text at scale.
- LLM prompts and raw model outputs: not preserved during the pilot.
- Credentials, API keys, and local temporary files.

The 335-record feasibility cohort is included because it documents a deviation
from the planned 900-paper design. It was drawn but **not coded**, and no result
from it appears in the manuscript.

## Status and next steps

| Component | Status |
|---|---|
| Citation frame | Frozen and verified. |
| Coding rubric | Frozen at v1.1. |
| Pilot data and analysis | Complete for 12 coded papers. |
| Manuscript draft | Complete as a pilot-based draft. |
| Full-scale data collection | Not executed. |
| Human reliability | Not available (no human second coder). |
| OSF registration / DOI | Not created. |
| Submission | Not ready; see [`manuscript/submission/submission_checklist.md`](manuscript/submission/submission_checklist.md). |

The next scientific step is the full study: a probability sample from the frozen
frame, a 50-record access pretest, human double-coding of at least 20% of eligible
papers, the pre-specified sensitivity analyses, and registration before main
coding. No further retrieval was performed for this repository.

## Author and citation

**Author:** Syed Abdul Aman (Independent Researcher)  
**Repository maintainer:** [P-r-e-m-i-u-m](https://github.com/P-r-e-m-i-u-m)

If you use this material, cite the repository and preserve the pilot status:

> Aman, S. A. (2026). *Does Benchmark Critique Diffuse into Evaluation Practice?
> A Pilot-Based Study of EvalPlus and SWE-bench+ Adoption* [Pilot-based research
> draft]. GitHub. https://github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol

## Licenses

- Code: [MIT](LICENSE)
- Original documentation, rubric, manuscript, and derived data: [CC BY 4.0](LICENSE-DATA)
- Citation-frame metadata is not relicensed; see
  [`reproducibility/licensing.md`](reproducibility/licensing.md).

Third-party benchmarks and papers retain their own licenses. No full texts are
redistributed.
