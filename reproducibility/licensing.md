# Licensing and Redistribution

## Project licenses

| Material | License | File |
|---|---|---|
| Original code in `scripts/` and `tests/` | MIT | `LICENSE` |
| Original documentation, rubric, protocol, manuscript, derived tables and figures, pilot coding table | CC BY 4.0, to the extent the author can license it | `LICENSE-DATA` |
| Citation-frame metadata | Not relicensed; provided for research use subject to Semantic Scholar's terms | This file |

## What is included

- The frozen 2,666-cluster citation frame derived from Semantic Scholar metadata.
- The 12-row pilot coding table with short evidence quotes.
- Analysis scripts, tests, tables, figures, and the manuscript draft.
- The 335-record feasibility cohort and manifest (drawn, not coded).

## What is excluded

| Material | Reason |
|---|---|
| Publisher PDFs and full-text copies | Copyright and publisher terms; not redistributable. |
| `data/cohort_arxiv_metadata.csv` | Third-party abstracts; excluded to avoid redistributing copyrighted text at scale. |
| Long quotations | The coding table uses short quotes only (target ≤60 words per paper) for research criticism and verification. |
| LLM prompts and raw outputs | Not preserved; cannot be reconstructed honestly. |
| Credentials and API keys | Security. |
| Local absolute paths and temporary files | Privacy and portability. |

## Third-party artifacts

| Artifact | License | Note |
|---|---|---|
| EvalPlus code/data | Apache-2.0 | Reuse with attribution; patent grant. |
| SWE-bench+ dataset | CC BY 4.0 | Reuse with attribution. |
| SWE-bench code/data | MIT | Reuse with attribution. |
| GSM1k | Hugging Face card blank; paper states MIT for release | Do not rely on a license claim; secondary only. |

No third-party artifact is redistributed in this repository. The frame contains
metadata and titles, not benchmark data or model outputs.

## Semantic Scholar metadata

The citation frame is derived from the Semantic Scholar Graph API. It is provided
for research and verification. Downstream users are responsible for complying with
Semantic Scholar's API terms and any applicable database rights. The project does
not relicense the metadata.

## Quotes

Evidence quotes are short, attributed, and used for criticism, verification, and
research commentary. They are not a substitute for the original papers. Anyone
reusing the coding table should verify quotes against the published sources and
respect the original licenses.

## What this means for reuse

You may reuse the original code under MIT and the original documentation and
derived data under CC BY 4.0 with attribution to:

> Syed Abdul Aman (P-r-e-m-i-u-m), *Does Benchmark Critique Diffuse into Evaluation
> Practice?*, 2026, https://github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol

Do not represent the pilot as a full-scale prevalence study. Do not remove the
status warnings or the LLM–LLM reliability caveat.
