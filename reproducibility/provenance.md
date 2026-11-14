# Provenance

## Citation frame

- **Source:** Semantic Scholar Graph API citations endpoint.
- **Critique records:** EvalPlus arXiv:2305.01210; SWE-bench+ arXiv:2410.06992.
- **Retrieval date:** 13 November 2026.
- **Raw rows:** 2,572 EvalPlus citation rows and 136 SWE-bench+ citation rows
  (2,708 total). Semantic Scholar reported 2,573 EvalPlus citations; one row was
  not returned by the API. The shortfall is recorded rather than repaired.
- **Identifier deduplication:** DOI, arXiv ID, DBLP key, CorpusId, and
  Semantic Scholar paperId, with transitive closure. Result: 2,684 records.
- **Title clustering:** normalized-title identity, representative chosen by DOI,
  then arXiv, then earliest year, then paperId. Result: 2,666 clusters.
- **Freeze:** the frame was not refreshed after 13 November 2026. The source JSON
  and analysis CSV hashes are recorded in `data/frame_summary.json`.

### Known frame limitations

- Semantic Scholar coverage is incomplete; non-indexed venues and very recent work
  are missing.
- The 2026 portion is incomplete. Two hundred thirty-one records have publication
  dates after 30 September 2026, consistent with forthcoming issue metadata.
- Two hundred twenty-five records have no publication date.
- Forty-two records have no DOI, arXiv ID, or DBLP key.
- Fourteen multi-variant clusters merge 18 extra identifier-level records. These
  require manual review before the full study.
- Title clustering can merge distinct works that share an identical normalized
  title. The 2,684-record identifier-deduplicated set is the sensitivity frame.

## Pilot

- **Design:** purposive 29-paper access frame assembled from papers citing EvalPlus,
  SWE-bench+, or GSM1k, selected for construct coverage rather than representativeness.
- **Retrieval:** full texts were obtained from public sources during the pilot on
  13 November 2026. They are stored outside the public repository.
- **Coding:** 12 papers were coded with rubric v1.0; rubric v1.1 was frozen after
  boundary cases were resolved and before the results were interpreted.
- **Second pass:** a fresh-context LLM pass re-coded the 12 papers. This is
  LLM–LLM agreement, not human reliability.
- **Raw model metadata:** the exact model identifier, prompt, temperature, and
  output logs were not preserved. This is a documented reproducibility gap.

### Why only 12 of 27 accessible papers were coded

The pilot was an instrument-feasibility study, not a prevalence study. Coding
continued until the four score categories and the main boundary cases were
exercised. Fifteen accessible papers were not coded after category saturation.
The two inaccessible papers were not coded.

## Feasibility cohort (deviation)

- **Design:** 135 SWE-bench+ census records + 200 EvalPlus-only records.
- **Seed:** `20261113`.
- **Frame hash:** `6a0a374ba6120b244418e887a76a83d6bfb8a95dd61cfc822cf349ac7043d30c`.
- **Manifest:** `data/cohort_feasibility.manifest.json`.
- **Status:** drawn and partially retrieved, then halted. **No records were coded.**
  No cohort result appears in the manuscript. It is documented because it is a
  deviation from the planned 900-paper design.

## Excluded from publication

| Material | Reason |
|---|---|
| Publisher PDFs and full texts | Copyright and publisher terms; not redistributable. |
| `data/cohort_arxiv_metadata.csv` | Contains third-party abstracts; excluded to avoid redistributing copyrighted text at scale. |
| LLM prompts and raw model outputs | Not preserved; no reliable reconstruction is possible. |
| Credentials, API keys, local absolute paths | Security and privacy. |
| Temporary retrieval directories | Not part of the research record. |
