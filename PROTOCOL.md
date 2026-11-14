# Does Benchmark Critique Diffuse into Evaluation Practice?

## A Citation Audit of EvalPlus and SWE-bench+ Adoption

**Research protocol v1.0**  
**Frozen:** 13 November 2026  
**Author:** Syed Abdul Aman (independent researcher)  
**Status:** Execution-ready design, conditional on Gate 0 external inputs  
**Decision:** **NEEDS EXTERNAL INPUT** — see §14

---

## 0. Decision box

| Item | State |
|---|---|
| Protocol complete? | Yes: RQ, pairs, frame, sampling, rubric, analysis, reliability, ethics, feasibility, roadmap, venue plan, dependencies. |
| Citation frame built? | Yes: 2,666 title-deduplicated citing works from 2,708 raw citation rows. |
| Pilot completed? | Yes: 12 papers coded, 8 eligible across three pairs; 6 eligible in the two primary pairs. |
| Human second coder? | **No.** The pilot reliability statistics are LLM–LLM agreement, not human reliability. |
| Full-text access for the frame? | **Not confirmed.** Pilot access was 93.1% on a purposive 29-paper frame; the general-frame rate is unknown. |
| OSF registration? | **Not yet created.** Self-serve; a Gate 0 item. |
| Main coding started? | **No.** |
| Final decision | **NEEDS EXTERNAL INPUT.** The protocol is complete, but two critical inputs are missing: a human second coder and a confirmed full-text access route. |

**What this means:** the scientific design is settled. The remaining work is not more exploration; it is securing two external conditions and registering the protocol. The exact flip path is in §14.

---

## 1. Title, research question, and scope

### 1.1 Title

**Does Benchmark Critique Diffuse into Evaluation Practice? A Citation Audit of EvalPlus and SWE-bench+ Adoption**

Short title for running heads: *Benchmark Critique Diffusion*.

### 1.2 Primary research question

> Among research papers that cite a benchmark-remediation critique, what proportion document adopting the critique's recommended benchmark or protocol in their own evaluation of the criticized benchmark?

The primary outcome is **documented full adoption** (rubric score 3) among **eligible citing papers**. "Documented" means the paper's text, tables, or captions state that the recommended artifact/protocol was used. It does not mean the artifact was verified to execute correctly.

### 1.3 Secondary research questions

| ID | Question | Role |
|---|---|---|
| SQ1 | What is the distribution of engagement with the critique (citation only, acknowledged, partial adoption, full adoption)? | Descriptive, confirmatory for the typology |
| SQ2 | Does documented adoption differ between EvalPlus and SWE-bench+? | Descriptive/exploratory; the SWE-bench+ frame is small |
| SQ3 | Is adoption more common in papers published at least 12 months after the critique, in peer-reviewed venues, or in papers with author overlap? | Exploratory |
| SQ4 | How often do citing papers perform independent remediation without adopting the critique's artifact? | Descriptive |
| SQ5 | How sensitive are estimates to access failure, self-citation, benchmark version, and the treatment of partial adoption? | Robustness |

### 1.4 Hypotheses

| ID | Hypothesis | Test | Status |
|---|---|---|---|
| H1 | Full adoption is uncommon among eligible citing papers: **<25%**. | One-sided exact binomial test vs 0.25; report prevalence and Wilson 95% CI. | Confirmatory |
| H2 | Full adoption is more common for EvalPlus than for SWE-bench+. | Fisher exact test and risk difference with Newcombe CI; report pair-specific estimates. | **Exploratory** — underpowered |
| H3 | Most eligible citing papers are citation-only or acknowledged (score 0 or 1), not partial/full adopters. | One-sided exact binomial test vs 0.50 on the combined 0/1 proportion. | Confirmatory |
| H4 | Adoption is more common at least 12 months after critique release and in peer-reviewed venues. | Descriptive rates by year/venue; logistic trend if counts permit. | Exploratory |

H2 is deliberately labeled exploratory. The SWE-bench+ citation frame contains only 135 title clusters; even a census cannot support a well-powered difference test. The study can describe a contrast; it cannot confirm one.

### 1.5 Scope boundaries

**In scope:**
- Citing works that evaluate HumanEval, MBPP, SWE-bench, SWE-bench Lite, or SWE-bench Verified.
- Documented use of HumanEval+/MBPP+ or the SWE-bench+ curated dataset/protocol.
- Citation, acknowledgment, partial adoption, and full adoption as separate categories.
- Access failure and self-citation as sensitivity analyses.

**Out of scope:**
- Citation impact, h-index, or venue prestige as outcomes.
- Causal attribution: the study cannot show that the critique *caused* adoption. It measures co-occurrence of citation and documented practice.
- General evaluation quality, reproducibility, or code correctness beyond the specific adoption construct.
- GSM1k as a primary pair. It is a secondary contrast only (§3.3).
- Benchmarks outside code generation and grade-school arithmetic.
- Papers that do not evaluate the criticized benchmark, even if they cite the critique.

### 1.6 Unit of analysis

The unit is a **title-level citing work**, not a citation row, PDF, or evaluation instance. Preprints and their published versions are merged when the normalized title is identical. A paper that evaluates both HumanEval and MBPP receives one score per critique, based on the highest-adoption use that appears in its main evaluation; all benchmark-level uses are recorded in secondary fields.

---

## 2. Background and originality

### 2.1 The problem

Benchmark critiques identify a concrete failure in a widely used benchmark and release a remediation: stronger tests, filtered instances, or contamination-controlled data. The critique is scientifically useful only if subsequent evaluations change. Citation counts do not show that change. A paper can cite a critique, lament contamination, and still report the original benchmark as its main result.

The gap is empirical: there is little systematic evidence on whether benchmark critiques diffuse into **evaluation practice**, as opposed to citation practice. The closest prior work studies documentation and accessibility of non-English NLP benchmarks, not the adoption of a critique's remediation in code-generation evaluations.

### 2.2 Why these two critiques

EvalPlus and SWE-bench+ are a useful contrast because both are public, licensed, and citable, but their remediation costs differ sharply:

- **EvalPlus** adds augmented tests to HumanEval and MBPP. It is a drop-in artifact: a lab can run HumanEval+/MBPP+ with a command and report pass rates. The cost of adoption is low.
- **SWE-bench+** deposits a filtered 548-instance dataset and a strengthened-test protocol for SWE-bench. Adoption requires re-running agents on a different instance set and reconciling test harnesses. The cost is higher.

If adoption is low even for a drop-in artifact, the diffusion problem is not merely tooling cost. If adoption is high for EvalPlus but low for SWE-bench+, the contrast points to integration cost and benchmark-version inertia. This is a descriptive contrast, not a causal test.

### 2.3 Closest prior work

**Merzah (2026), "Cited but Not Used: Documented Adoption and Data Accessibility in 40 Non-English NLP Benchmarks"** (Zenodo replication materials, DOI 10.5281/zenodo.23634794, published 2026-11-01, CC BY 4.0). It studies 40 non-English NLP benchmarks, 487 citation records, a coding table, an accessibility/licensing audit, three reliability instruments, and five scripts. No Crossref DOI-registered paper or matching arXiv title was found as of 2026-11-13; treat it as unpublished replication materials, not a peer-reviewed antecedent.

This study differs in five ways:

1. **Domain:** code-generation benchmarks (HumanEval/MBPP, SWE-bench) rather than non-English NLP benchmarks.
2. **Design:** a citation-frame audit of all citing works, not a benchmark-sample audit.
3. **Outcome:** an ordinal adoption rubric (0–3) with evidence quotes and adoption locus, not only citation/accessibility indicators.
4. **Contrast:** a low-cost test-augmentation critique (EvalPlus) versus a high-cost dataset-filtering critique (SWE-bench+).
5. **Construct:** diffusion of a critique's *recommended practice* into evaluation, not data availability or licensing alone.

The study also builds on citation-diffusion research (Small, 1978), benchmark-critique work (Benchmark Lottery; contamination and leakage studies), and reproducibility/artifact-adoption research. The contribution is not the observation that citation can be disconnected from use. It is a comparative, transparently coded design for estimating adoption across two influential code benchmarks.

### 2.4 Planned contributions

1. **Prevalence (planned full study):** a systematic estimate of documented adoption of EvalPlus and SWE-bench+ among their citing papers.
2. **Typology:** a four-level adoption scale that separates citation, acknowledgment, partial adoption, and full adoption, with a boundary rule that prevents independent remediation from being counted as diffusion.
3. **Contrast:** a descriptive comparison of a low-cost, drop-in remediation with a high-cost, dataset-level remediation, both public and licensed.
4. **Open evidence:** a frozen frame, coding rubric, sampling script, analysis code, and (where licensing permits) derived coding table.

### 2.5 What this study does not claim

- It does not claim that a citation causes adoption, or that non-citation means non-use.
- It does not claim that EvalPlus or SWE-bench+ is the best remediation.
- It does not claim that adoption rates generalize to all benchmarks, all venues, or all countries.
- It does not claim that the pilot's κ values are human reliability.
- It does not claim that a paper's reported use was executed correctly.

---

## 3. The two primary benchmark pairs and one secondary contrast

### 3.1 Pair definitions

| Pair | Critique | Criticized benchmark | Recommended practice | Artifact status | Remediation cost |
|---|---|---|---|---|---|
| **P1** | **EvalPlus** — Liu et al., "Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation," NeurIPS 2023; arXiv:2305.01210; DOI 10.52202/075280-0943 | HumanEval; MBPP | Use **HumanEval+ / MBPP+** augmented tests as the primary code-generation evaluation | GitHub `evalplus/evalplus`, Apache-2.0; first release 2023-05-03; latest v0.3.1 2024-10-20; HumanEval+ 80× tests; MBPP+ 35× tests; MBPP+ 378 tasks | Low: drop-in test suite and harness |
| **P2** | **SWE-bench+** — Aleithan et al., "SWE-Bench+: Enhanced Coding Benchmark for LLMs," arXiv:2410.06992 (v1 2024-10-09; v2 2024-10-10) | SWE-bench; SWE-bench Lite; SWE-bench Verified | Use the **SWE-bench+ 548-instance curated dataset and/or its strengthened-test protocol** as the primary SWE-bench evaluation | Zenodo record 13879453, CC BY 4.0, published 2024-10-02; `swe_bench+_data.json`, 9,543,869 bytes, 548 instances | High: filtered instance set, harness reconciliation, agent re-runs |
| **S1** | **GSM1k** — Zhang et al., "A Careful Examination of Large Language Model Performance on Grade School Arithmetic," arXiv:2405.00332 | GSM8K | Use GSM1k or a fully equivalent contamination-controlled replication as the primary arithmetic evaluation | HF `ScaleAI/gsm1k`, 1,205 rows, created 2025-03-31; license field blank; GitHub README stale | Secondary contrast only; excluded from primary denominator |

### 3.2 Why EvalPlus and SWE-bench+ are the primary pairs

- Both critiques are **publicly available and licensed**: EvalPlus Apache-2.0; SWE-bench+ CC BY 4.0. Adoption is not blocked by paywalls or missing artifacts.
- Both have **clear recommended practices** that can be observed in a paper's methods and tables.
- Both have **large enough citation frames** to study: EvalPlus 2,572 rows; SWE-bench+ 136 rows. SWE-bench+ is small but sufficient for a census and a descriptive contrast.
- Their **remediation costs differ**, which makes the comparison informative even if it is underpowered for a formal difference test.
- Both are used in **code-generation / software-engineering** research, a coherent venue and citation population.

### 3.3 Why GSM1k is secondary only

GSM1k is excluded from the primary adoption denominator for four reasons:

1. **Task fit:** GSM1k is a contamination probe built by perturbing GSM8K-style problems. It is not a drop-in replacement for GSM8K in the same way HumanEval+ is for HumanEval. Papers can legitimately use GSM8K and a separate contamination check without adopting GSM1k.
2. **Availability timing:** the full HF dataset appeared on 2025-03-31, after most of the citing papers in the frame were written. Low adoption before release would be a timing artifact, not a diffusion failure.
3. **License ambiguity:** the HF dataset card has a blank license field; the paper commits to MIT for the release, but the dataset card does not state it. This complicates a clean artifact-availability comparison.
4. **Comparability:** the primary construct is "use the critique's remediated artifact/protocol for the criticized benchmark." GSM1k's relationship to GSM8K is less substitutive than HumanEval+'s relationship to HumanEval.

GSM1k is retained as a **secondary task-fit contrast** in a separate file. It is never pooled into the primary prevalence estimate. The pilot's GSM1k cases (`understand_translate`, `promptcot`) are reported separately and are excluded from the primary-pair pilot estimate.

### 3.4 Unresolved uncertainties about the pairs

| Uncertainty | Status | Consequence | Resolution |
|---|---|---|---|
| SWE-bench+ is an arXiv preprint; no peer-reviewed record was located (the check was not exhaustive). | **Open / inherent** | Citation frame may undercount authors who treat it as a preprint. | Report publication status as “arXiv preprint; no peer-reviewed record located”; sensitivity excluding 2024–early 2025 papers. |
| SWE-bench+ Zenodo creator is "Anonymous." | **Open / inherent** | Provenance is less traceable than a named author deposit. | Record DOI and dataset hash; note in limitations. |
| SWE-bench+ releases 548 filtered instances, not the full SWE-bench test set. | **Resolved in rubric** | A paper that uses only a subset may be partial, not full. | Code 3 only if the 548-instance dataset or its protocol is the main evaluation; otherwise 2. |
| EvalPlus has multiple versions (v0.1.0–v0.3.1). | **Resolved in rubric** | Version drift could affect what "adoption" means. | Record `benchmark_version`; do not upgrade/downgrade score solely by version. |
| Some papers use HumanEval+ problems but not the augmented tests. | **Resolved in rubric** | Could inflate full adoption. | Code 3 only if the augmented tests are used for at least one main claim; otherwise 2. |
| GSM1k license is blank on HF. | **Open / secondary only** | Cannot make a clean licensing claim. | Exclude from primary; report as secondary limitation. |

---

## 4. Frame, sampling, and access

### 4.1 Frame construction

**Source:** Semantic Scholar Graph API citations to the two critique papers, retrieved 2026-11-13.

| Step | Count | Note |
|---|---:|---|
| EvalPlus citation rows fetched | 2,572 | S2 reports 2,573; one row not returned. |
| SWE-bench+ citation rows fetched | 136 | S2 reports 136. |
| Raw sum | 2,708 | 2,572 + 136. |
| Identifier-deduplicated union | 2,684 | Union-find on DOI, arXiv, DBLP, CorpusId, S2 paperId. |
| Overlap (both critiques) | 24 | 2,572 + 136 − 24 = 2,684. |
| Title-deduplicated analysis frame | **2,666** | 14 duplicate-title groups; 18 extra rows removed. |
| SWE-bench+ stratum (census) | **135** | 112 SWE-only + 23 both. |
| EvalPlus-only stratum (sample) | **2,531** | 2,666 − 135. |

**Frame hash (SHA-256):**
- Source `citation_frame.json`: `46a58fe017577d9e15c22e6bef198fdff526b511ff7897519b6a0e91542cdd72`
- Analysis CSV `citation_frame_2666.csv`: `4650ce1b67df80bdeb1691b883a36f5bda540efd1dad20da652660f216f705a0`

### 4.2 Deduplication rules

1. **Identifier union-find:** two records are the same work if they share any of DOI (lowercased), arXiv ID, DBLP key, CorpusId, or S2 paperId. Transitive closure is applied.
2. **Title clustering:** after identifier dedupe, normalize titles by lowercasing, replacing non-alphanumerics with spaces, and collapsing whitespace. Identical normalized titles are one cluster.
3. **Representative record:** prefer a record with a DOI; then arXiv; then earliest year; then paperId. All source labels (`evalplus`, `swebenchplus`) are unioned into the cluster.
4. **Manual review:** the 14 multi-variant clusters are reviewed before sampling. If two different works share a title, split them and document the split. If a preprint and a published version share a title, keep them merged and use the published version as representative.
5. **No mid-study refresh:** the frame is frozen at 2026-11-13. New citations after that date are out of scope. A post-hoc citation refresh may be reported as a sensitivity analysis but cannot change the sampling frame.

### 4.3 Frame profile

| Year | Title clusters |
|---|---:|
| 2022 | 2 |
| 2023 | 119 |
| 2024 | 526 |
| 2025 | 838 |
| 2026 | 1,139 |
| Unknown | 42 |
| **Total** | **2,666** |

| Identifier coverage | Count |
|---|---:|
| DOI | 2,313 |
| arXiv | 2,028 |
| DBLP | 2,129 |
| None of DOI/arXiv/DBLP | 42 |

**Data-quality flags:** 225 clusters have no publication date; 231 have a publication date after 2026-09-30 (likely forthcoming issue dates); 14 clusters have multiple title variants. These are reported, not silently dropped.

**Top venues (title clusters):** arXiv.org 974; unknown 331; ACL 110; EMNLP 82; TOSEM 71; NeurIPS 70; ICLR 69; ASE 39; ICML 33; ICSE 21. The frame is code-generation/ML/SE-heavy, which matches the critiques.

### 4.4 Sampling design

**Design:** stratified random sampling with a census of the small SWE-bench+ stratum.

| Stratum | Frame N | Sample | Weight |
|---|---:|---:|---:|
| SWE-bench+ census (includes 23 both-critique clusters) | 135 | **135** (census) | 1.000 |
| EvalPlus-only | 2,531 | **765** (random) | 3.308 |
| **Total invited** | **2,666** | **900** | — |

The EvalPlus-only sample is drawn with **proportional allocation by year** (2022 collapsed into 2023; minimum 10 per stratum where possible), then simple random sampling within stratum. A fixed seed is committed at OSF registration. The sampling script is `scripts/sample_frame.py`.

**Why 900?** At the planning value p=0.125, 80% access, and 18% eligibility, 900 invited yields about 130 eligible papers and a Wilson 95% CI of 7.7–19.1% (half-width 5.7 percentage points). That is precise enough to distinguish "rare" from "common" and to compare with the pilot. A census of 2,666 would cost roughly three times as much for a modest precision gain.

**Stop rule:** sample in blocks. The initial 900 is the target. If, after 900 invited, fewer than 120 eligible papers are found, add blocks of 100 EvalPlus-only records up to a hard cap of **1,200 invited**. Stop as soon as 120 eligible papers are reached. If the cap is reached with fewer than 120 eligible, report the realized eligible count and do not extend further without a protocol amendment.

**Why not census?** A full census would require retrieving and screening 2,666 full texts. At 10 min retrieval + 20 min screening per accessible paper, that is roughly 1,300–1,700 hours before coding, writing, and reliability work. It is not feasible for a solo researcher in 9–12 months. The sample is the defensible compromise.

### 4.5 Inclusion and exclusion

**Include a citing work if:**
- It is in the frozen frame (cites EvalPlus or SWE-bench+ at identifier/title level).
- A full text is retrievable in English (publisher PDF, arXiv, author copy, or institutional access).
- It reports empirical evaluation results on the criticized benchmark (HumanEval, MBPP, SWE-bench, SWE-bench Lite, or SWE-bench Verified).
- It contains a bibliographic citation to the critique.

**Exclude (record reason):**
- **No evaluation of the criticized benchmark:** surveys, position papers, editorials, errata, benchmark-construction papers that only introduce a derivative and never evaluate the original.
- **Derivative-only evaluation:** SWE-bench Pro, CWEval, or another derivative is evaluated, but not SWE-bench/Lite/Verified. This is not evidence about the criticized benchmark.
- **No critique citation:** if a frame record somehow lacks the citation (metadata error), exclude and log.
- **Full text unavailable:** code as `UNCODABLE_ACCESS`; do not infer eligibility or score.
- **Not in English:** code as `UNCODABLE_LANGUAGE`; report.
- **Duplicate:** merged at title clustering.

**Eligibility is decided before adoption scoring.** A paper that is ineligible receives no 0–3 score. This prevents "citation only" from becoming a dumping ground for papers that never evaluated the benchmark.

### 4.6 Access and retrieval

1. Try the DOI landing page, publisher PDF, arXiv, and author preprint in that order.
2. Use institutional subscriptions and interlibrary loan where available.
3. Record the access route (`publisher`, `arxiv`, `author_copy`, `repository`, `ill`) and the date.
4. If only HTML is available, use the publisher HTML or arXiv HTML; record `html_only=yes`.
5. Do not use pirated copies. Do not scrape paywalled PDFs in violation of terms of service.
6. Store PDFs in a private local folder. Do not commit PDFs to the public workspace or OSF.

**Access pretest (Gate 0):** draw 50 random frame records, attempt retrieval, and compute the access rate. If ≥70%, proceed. If 50–70%, add ILL and document the shortfall. If <50%, restrict the primary frame to open-access records and report the restriction as a limitation, or pause.

### 4.7 Frame-freeze policy

The frame is frozen before main coding. Any post-freeze citation refresh is reported separately and cannot alter the sampling frame. This prevents denominator drift and selective inclusion.

---

## 5. Measurement: rubric v1.1

The full rubric is in `rubric_v1.1.md`. This section states the measurement contract.

### 5.1 Construct

**Documented adoption** = the extent to which a citing paper's own evaluation of the criticized benchmark uses the critique's recommended artifact or protocol, as stated in the paper.

It is **not**:
- citation count or citation context alone;
- agreement with the critique;
- general evaluation quality;
- independent remediation that is not the critique's recommended practice;
- verified execution of the artifact.

### 5.2 Eligibility (E1–E3)

A paper is eligible only if:

- **E1:** it reports empirical evaluation results on the criticized benchmark (HumanEval, MBPP, SWE-bench, SWE-bench Lite, or SWE-bench Verified).
- **E2:** it contains a bibliographic citation to the critique.
- **E3:** a full text is available in English and contains enough methods/results detail to code.

If E1 fails → `INELIGIBLE_NO_EVAL`.  
If E2 fails → `INELIGIBLE_NO_CITATION`.  
If E3 fails → `UNCODABLE_ACCESS` or `UNCODABLE_LANGUAGE`.

### 5.3 Ordinal scale

| Score | Label | Definition | Typical evidence |
|---:|---|---|---|
| **0** | Citation only | The critique appears in the reference list, but the body does not discuss its specific finding or recommendation; the criticized benchmark is used unchanged. A generic mention of "contamination" or "leakage" in a citation cluster, without discussing the critique's finding, is 0. | Reference entry; generic related-work sentence with no specific claim. |
| **1** | Acknowledged | The body mentions the critique's specific finding (test insufficiency, solution leakage, contamination) but the evaluation is unchanged: original instances/tests, no filtering, no augmented tests, no contamination-controlled replication. | "Liu et al. report gaps in HumanEval's tests; we use the original HumanEval." |
| **2** | Partial adoption | At least one recommended practice is applied to the criticized benchmark, but not the core remediated artifact/protocol for the main results. Examples: HumanEval+ only in an appendix or robustness check while the main table uses HumanEval; SWE-bench+ filtering applied to a subset or a secondary analysis; GSM1k only as a robustness check. | Main table uses HumanEval; appendix reports HumanEval+. |
| **3** | Full adoption | The core remediated artifact/protocol is used for the paper's primary evaluation of the criticized benchmark, with at least one reported result and the critique cited as the basis. | Main table uses HumanEval+/MBPP+; main SWE-bench table uses the 548-instance SWE-bench+ set or its protocol. |

**Binary primary outcome:** full adoption = score 3. Scores 0–2 are non-adoption for the primary estimate. Partial adoption is reported separately and tested as a sensitivity analysis (2+3 vs 0+1).

### 5.4 Boundary rules (the ones that decide cases)

1. **Citation is not adoption.** A reference-list entry alone is 0.
2. **Generic contamination talk is not acknowledgment.** If the paper says "contamination is a concern" and cites the critique in a cluster, but never states the critique's specific finding or implication for its own evaluation, score 0.
3. **Acknowledgment requires specificity.** A sentence that names the critique's finding (e.g., "EvalPlus shows HumanEval's tests are insufficient") and leaves the evaluation unchanged is 1.
4. **Partial requires a recommended practice, not any improvement.** An independently designed stronger test suite is not adoption; score 1 (if the critique's finding is discussed) and set `independent_remediation=yes`.
5. **Full requires the main evaluation.** If the augmented/filtered benchmark is only a secondary check, score 2. If it is used for at least one main claim/table/figure, score 3.
6. **Both original and augmented as co-primary:** score 3 if the augmented result supports at least one main claim; otherwise 2.
7. **Derivative-only papers are ineligible.** SWE-bench Pro, CWEval, and other derivatives do not count as evaluating SWE-bench/Lite/Verified. A paper that evaluates both the original and a derivative is eligible; code the original.
8. **Benchmark version:** record `benchmark_version` (HumanEval+ v0.1/v0.2/v0.3; MBPP+; SWE-bench+ 548). Do not change the score solely because the version differs, unless the paper explicitly uses a different construct.
9. **Code inspection:** record `artifact_check=yes/no`. Code inspection can corroborate documented use but cannot upgrade a score on its own. The construct is documented adoption.
10. **Self-citation:** code normally, set `author_overlap=yes` if any critique author is a paper author, and run a sensitivity analysis excluding these papers.
11. **Unresolved ambiguity:** assign `confidence=low`, send to adjudication. If still unresolved, use the conservative (lower) score and document why.

### 5.5 Secondary fields

| Field | Values | Purpose |
|---|---|---|
| `engagement` | 0 = reference only; 1 = brief mention; 2 = substantive discussion | Separates citation from engagement. |
| `independent_remediation` | yes/no | Captures good practice that is not diffusion. |
| `adoption_locus` | main_results / secondary_results / appendix / future_work / related_work | Distinguishes full from partial. |
| `benchmark_version` | free text | Version drift. |
| `critique_version` | arXiv v1/v2/v3, proceedings, dataset DOI | Which artifact was cited. |
| `author_overlap` | yes/no | Self-citation sensitivity. |
| `artifact_check` | yes/no | Whether code/repo was inspected. |
| `confidence` | high/medium/low | Adjudication triage. |
| `access_route` | publisher/arxiv/author_copy/repository/ill | Access-bias analysis. |
| `evidence_quote` | ≤60 words, verbatim | Audit trail. |
| `notes` | free text | Boundary cases. |

### 5.6 Coding procedure

1. Read title and abstract; assign a preliminary eligibility flag.
2. Retrieve full text; confirm E1–E3.
3. Search the full text for the critique's author names, title, arXiv ID, and artifact name. Also search for benchmark names and `+` variants.
4. Read the citation context ±2 paragraphs; read the methods, main results tables, and captions.
5. Assign the ordinal score and all secondary fields.
6. Record a verbatim evidence quote (≤60 words) and its section/table.
7. If ambiguous, set `adjudicate=yes`; do not guess.
8. Do not code from abstract alone for scores ≥1.
9. Do not use citation counts, venue prestige, or author reputation to infer adoption.
10. Re-code a 10% random audit of the first coder's work after calibration; log discrepancies.

### 5.7 Blinding

- The second coder receives a blinded packet: title, abstract, methods/results excerpt, and reference list, with the first coder's score removed. If full blinding is impossible because the paper names the critique, that is inherent; the second coder still codes independently before seeing the first score.
- The first coder does not see the second coder's scores until both are submitted.
- Adjudication is a discussion, not an average. If consensus fails, a third coder or the conservative rule applies.

### 5.8 Reliability

- **Sample:** 20% of eligible papers, stratified by critique and score band. At the base-case 130 eligible that is 26 papers; at the reduced 81 eligible it is 16 papers (the floor for the reduced design). There is no separate “minimum 20” rule; the operative rule is 20% of eligible papers.
- **Metrics:** percent agreement and Cohen's κ for eligibility; unweighted and linear-weighted κ for the ordinal score; PABAK when prevalence is <10% because κ is unstable; 95% bootstrap CIs.
- **Threshold:** weighted κ ≥0.60 is acceptable for the main analysis; 0.40–0.59 is moderate and requires a limitation paragraph; <0.40 triggers retraining and recoding.
- **LLM annotator:** may be used for pre-screening, flagging, or a second-pass audit, but **never** reported as human reliability. If used, report model/version, prompt, temperature, date, and agreement with the human coder. Do not send paywalled full texts to external APIs; use abstracts/metadata or a local model.
- **No human reliability claim without a human coder.** The pilot's 0.78/0.86 are LLM–LLM agreement, not human κ.

### 5.9 Coding form

The coding table has one row per `cluster_id` × `critique` (a paper citing both critiques gets two rows). Columns:

`cluster_id, title, year, venue, doi, arxiv, critique, eligible, ineligibility_reason, score, engagement, independent_remediation, adoption_locus, benchmark_version, critique_version, author_overlap, artifact_check, confidence, access_route, evidence_quote, notes, coder_id, coded_at`

A JSON schema is in `rubric_v1.1.md` §7.

---

## 6. Analysis plan

### 6.1 Descriptive analysis

- Frame profile: counts by critique, year, venue, identifier coverage, access route.
- Sample realized: invited, accessible, eligible, coded, by stratum and year.
- Score distribution: 0/1/2/3 counts and proportions, overall and by critique.
- Engagement and independent remediation rates.
- Evidence-locus distribution.

### 6.2 Primary estimate

**Estimand:** proportion of eligible citing papers with score 3, in the frame represented by the sample.

- Report **pair-specific** proportions with Wilson 95% CIs.
- Report a **pooled weighted** proportion using stratum weights (SWE-bench+ weight 1; EvalPlus-only weight 2,531/765 = 3.308), with a stratified bootstrap 95% CI (10,000 resamples).
- Report the unweighted sample proportion as a descriptive check; the weighted estimate is primary for the frame.
- Do **not** report a single pooled number without the pair-specific numbers.

### 6.3 Hypothesis tests

| Hypothesis | Test | Reporting |
|---|---|---|
| H1: full adoption <25% | One-sided exact binomial test vs 0.25 | p-value, prevalence, Wilson CI; reject if upper CI <25% or p<0.05 with prespecified direction. |
| H3: most papers are 0/1 | One-sided exact binomial test vs 0.50 on (0+1)/eligible | p-value, proportion, Wilson CI. |
| H2: EvalPlus > SWE-bench+ | Fisher exact test; risk difference with Newcombe CI | Label exploratory; report pair-specific n and CI; do not claim confirmation. |
| H4: time/venue gradient | Descriptive rates; logistic regression only if ≥10 events per predictor | Label exploratory; no multivariable model with sparse data. |

### 6.4 Sensitivity analyses (pre-specified)

1. **Partial-as-adoption:** score 2+3 vs 0+1.
2. **Exclude self-citations:** `author_overlap=yes`.
3. **Exclude 2026 records** and records with publication date after 2026-09-30.
4. **Exclude records with no DOI/arXiv** (42 clusters).
5. **Peer-reviewed only:** exclude arXiv-only/unknown venue.
6. **≥12 months after critique release:** EvalPlus before/after 2024-05; SWE-bench+ before/after 2025-10.
7. **Access extreme bounds:** lower bound = adopters / (eligible + all uncodable assumed non-adopters); upper bound = (adopters + all uncodable) / (eligible + all uncodable). Report both.
8. **Main-results-only vs any-use:** if a paper uses the artifact only in an appendix, does the estimate change?
9. **Title-cluster vs identifier-deduped frame:** repeat the primary estimate on the 2,684-row frame as a check.
10. **Manual-review clusters:** drop the 14 multi-variant clusters and repeat.

### 6.5 Access-bias analysis

Compare accessible vs inaccessible records on year, venue, DOI/arXiv presence, and stratum. If differences are material, report the extreme bounds and a propensity-weighted estimate (if the model is stable). Do not silently treat access failure as random.

### 6.6 Missing data

- `UNCODABLE_ACCESS` and `UNCODABLE_LANGUAGE` are not eligible; they are reported in the flow diagram and bounds.
- Missing metadata (year, venue, DOI) is reported, not imputed for the primary analysis.
- If a paper's score is missing because of ambiguity, it goes to adjudication; if still unresolved, use the conservative score and flag.

### 6.7 Multiplicity and interpretation

- H1 and H3 are confirmatory; H2 and H4 are exploratory. No alpha adjustment across confirmatory tests because there are only two, but report both and interpret conservatively.
- Do not describe a non-significant H2 as evidence of no difference. Report the CI and the small SWE-bench+ n.
- Do not infer causality from cross-sectional associations.
- Pre-specify the primary estimate; do not switch outcomes after seeing results.

### 6.8 Software and reproducibility

- Python 3.11+, pandas, statsmodels, scipy, matplotlib.
- `scripts/analysis_template.py` computes Wilson intervals and the weighted estimate; the final analysis script is versioned with the manuscript.
- A reproducibility check recomputes every number in the abstract and main tables from the coding CSV.
- The coding CSV, scripts, and a data dictionary are deposited on OSF/Zenodo at publication, except paywalled text.

---

## 7. Ethics, licensing, and data availability

### 7.1 Human subjects

No human subjects are involved. The study analyzes published papers and metadata. Institutional IRB review is not required for publicly available text, but the researcher will confirm local policy and state the determination in the manuscript.

### 7.2 Copyright and text use

- Full texts are stored privately and are not redistributed.
- Evidence quotes are ≤60 words per paper, used for research criticism and verification; they are not a substitute for the original.
- The public coding table contains metadata, codes, and short quotes only; no PDFs.
- Do not send paywalled full texts to external LLM APIs. If LLM assistance is used, restrict it to abstracts/metadata or a local model, and disclose.

### 7.3 Artifact licenses

| Artifact | License | Implication |
|---|---|---|
| EvalPlus code/data | Apache-2.0 | Reuse with attribution; patent grant. |
| SWE-bench+ dataset | CC BY 4.0 | Reuse with attribution. |
| SWE-bench code/data | MIT | Reuse with attribution. |
| GSM1k | HF card blank; paper says MIT for release | Do not rely on a license claim; secondary only. |

### 7.4 Data availability statement (draft)

> The frozen citation frame, sampling script, coding rubric, coding table, and analysis scripts are available at [OSF DOI] and [Zenodo DOI]. Full texts are not redistributed. The frame was retrieved from the Semantic Scholar Graph API on 13 November 2026 and is provided as derived metadata under the API's terms.

### 7.5 LLM use disclosure (draft)

> A large language model was used for [pre-screening/flagging/formatting] on [dates] with [model/version]. It did not serve as the human second coder, and its agreement is not reported as inter-rater reliability. All final codes were assigned by the human coder. Prompts and settings are in the supplement.

### 7.6 Pre-registration

Register on OSF Registries before main coding:
- protocol v1.0;
- rubric v1.1;
- sampling script and seed;
- analysis plan;
- frame hash.

Deviations are logged with date, reason, and impact. The registration is updated, not silently overwritten.

### 7.7 Authorship and CRediT

- **Lead researcher:** conceptualization, methodology, data curation, formal analysis, investigation, writing – original draft.
- **Second coder:** validation, reliability analysis, writing – review & editing, if the contribution meets authorship criteria; otherwise acknowledged.
- **Advisors/collaborators:** only if they contribute substantially; no honorary authorship.

---

## 8. Feasibility and workload

### 8.1 Verified frame facts

- 2,666 title clusters; 135 SWE-bench+ census; 2,531 EvalPlus-only.
- 2,313 DOI; 2,028 arXiv; 2,129 DBLP; 42 with none.
- 225 no publication date; 231 date after 2026-09-30.
- Top venues: arXiv.org 974; ACL 110; EMNLP 82; TOSEM 71; NeurIPS 70; ICLR 69.

### 8.2 Planning scenarios

Planning value p=0.125 for full adoption, informed by the all-pair pilot (1/8). The primary-pair pilot was 1/6 = 16.7%, but n=6 is too small to prefer; using 12.5% is conservative for precision calculations.

| Scenario | Invited | Access | Eligible rate | Accessible | Eligible | Adopters at 12.5% | Wilson 95% CI | Half-width |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| Conservative | 900 | 70% | 10% | 630 | 63 | 8 | 6.6–23.1% | ±8.3 pp |
| **Base** | **900** | **80%** | **18%** | **720** | **130** | **16** | **7.7–19.1%** | **±5.7 pp** |
| Optimistic | 900 | 93.1% | 25% | 838 | 210 | 26 | 8.6–17.5% | ±4.5 pp |
| 9-month reduced | 560 | 80% | 18% | 448 | 81 | 10 | 6.8–21.3% | ±7.2 pp |
| Cap, conservative | 1,200 | 70% | 10% | 840 | 84 | 10 | 6.6–20.5% | ±7.0 pp |
| Cap, base | 1,200 | 80% | 18% | 960 | 173 | 22 | 8.5–18.5% | ±5.0 pp |

These are planning scenarios, not predictions. The base case is the design target; the conservative and cap rows define the worst-case workload.

### 8.3 Chosen design

**900 invited = 135 SWE-bench+ census + 765 EvalPlus-only random sample.** Target 120 eligible; hard cap 1,200 invited if eligibility is low. The base case expects 130 eligible and ±5.7 pp precision. The conservative case expects 63 eligible and ±8.3 pp; that is still reportable as a prevalence estimate, but the study should say so.

### 8.4 Workload (base case, 130 eligible)

| Task | Assumption | Hours |
|---|---|---:|
| Full-text acquisition | 900 × 10 min | 150.0 |
| Eligibility screening | 720 accessible × 20 min | 240.0 |
| Ordinal coding + evidence | 130 × 30 min | 65.0 |
| Reconciliation | 26 double-coded × 15 min | 6.5 |
| Analysis + robustness | fixed | 80.0 |
| Writing/editing | fixed | 140.0 |
| Admin, OSF, ethics, data | fixed | 40.0 |
| **Subtotal** | | **721.5** |
| 15% buffer | | **108.2** |
| **Total** | | **829.7** |
| 12 months (52 weeks) | | **16.0 h/week** |
| 9 months (39 weeks) | | **21.3 h/week** |

**Second coder (external):** 26 × 45 min = 19.5 h + 6 h calibration + 6 h adjudication = **31.5 h** across 12 months.

### 8.5 9-month reduced option

560 invited, 448 accessible, 81 eligible, 16 double-coded:
- acquisition 93.3 h; screening 149.3 h; coding 40.5 h; reconciliation 4.0 h; analysis 80 h; writing 140 h; admin 40 h; subtotal 547.2 h; buffer 82.1 h; **total 629.3 h = 16.1 h/week over 39 weeks**.
- Second coder: 16 × 45 min = 12 h + 6 h calibration + 4 h adjudication = **22 h**.
- Precision: ±7.2 pp at p=0.125.

**Recommendation:** choose the 12-month design. It delivers better precision (130 vs 81 eligible) at essentially the same weekly effort (16.0 vs 16.1 h/week), and it leaves a real buffer for access delays and review. The 9-month option is feasible only if the start date cannot move and the researcher can protect 16 h/week without interruption.

### 8.6 Budget

| Item | Cost | Note |
|---|---:|---|
| Mandatory cash | $0 | Assuming institutional access and no APC. |
| OSF | $0 | Free registries. |
| Software | $0 | Python/open source. |
| Second coder | $0–honorarium | Unpaid collaborator preferred; if paid, 31.5 h × rate. |
| ILL/document delivery | institutional | Check library quota. |
| EMSE Open Choice APC | optional | Amount at submission; not required for subscription route. |
| DMLR | $0 | No fees. |
| QSS APC | unresolved | Third-party reports conflict ($800 vs $1,200); not primary. |

### 8.7 What would make the study infeasible

- Access <50% with no institutional/ILL route and no defensible open-access restriction.
- Fewer than 5% of accessible papers eligible after screening, with no supplement.
- No human second coder **and** a journal that requires reliability evidence, with no acceptable fallback.
- Legal restriction on text analysis or short quotation.

None of these is currently established. The pilot suggests the coding task is tractable; the frame is built; the main uncertainty is external input, not scientific viability.

---

## 9. Execution roadmap

**Assumed start:** 1 December 2026 (after Gate 0). **End:** 30 November 2027. Dates shift if Gate 0 slips; the week structure does not.

| Phase | Weeks | Dates | Work | Gate/output |
|---|---:|---|---|---|
| **0. Gate 0** | 1–2 | 2026-12-01 to 12-14 | Secure second coder; access pretest on 50 records; create OSF registration; freeze frame; confirm library route. | **G0:** C1–C3 met; else decision remains NEEDS EXTERNAL INPUT. |
| **1. Calibration** | 3–6 | 12-15 to 2027-01-11 | Code 20 fresh papers (not the pilot 12); calibrate rubric v1.1; second coder training; measure agreement; lock rubric. | **G1:** weighted κ ≥0.60 or consensus; rubric locked; OSF updated. |
| **2. Retrieval/screening/coding** | 7–30 | 01-12 to 06-28 | Four blocks of 225 invited (900 total); retrieve, screen, code eligible; weekly access log. Add 100-record blocks if <120 eligible. This is a **24-week** phase, not 16 weeks. | **G2:** ≥120 eligible or 1,200 invited; flow diagram complete. |
| **3. Reliability/adjudication** | 27–30 | 06-01 to 06-28 | Overlaps the last retrieval block: 20% blind double-code (26 base, 16 reduced); adjudicate; compute κ; lock coding table. | **G3:** 100% coded; reliability report; adjudication log. |
| **4. Analysis** | 31–34 | 06-29 to 07-26 | Primary estimate; pair-specific; sensitivity; access bounds; figures/tables; reproducibility check. | **G4:** analysis memo; every number recomputes. |
| **5. Writing** | 35–42 | 07-27 to 09-19 | Draft; co-author/second-coder review; polish; data availability statement; LLM disclosure. | **G5:** manuscript ready; sign-off. |
| **6. Submission** | 43–46 | 09-20 to 10-17 | Submit to EMSE; post arXiv preprint; update OSF; prepare response file. | **G6:** submitted; preprint live. |
| **Buffer** | 47–52 | 10-18 to 11-29 | Review response; contingency; venue fallback if desk-rejected; project close. | Final deposit; decision log closed. |

**Why retrieval is 24 weeks:** the base workload is 455 h of retrieval, screening, and coding. Compressing it into 16 weeks implies ~28 h/week, which is not compatible with a part-time project. Spread over 24 weeks it averages 19.0 h/week; overlap with reliability in weeks 27–30 peaks at ~21 h/week. See `planning/execution_roadmap.md` §3 for the load profile.

### 9.1 Gates in detail

- **G0 (critical):** C1 second coder signed; C2 access pretest ≥70% (or ILL plan); C3 OSF DOI. Without G0, do not start main coding.
- **G1:** calibration on 20 fresh papers; weighted κ ≥0.60 or documented consensus; rubric version locked. If κ <0.40, revise rubric and repeat calibration (adds 2–3 weeks).
- **G2:** target 120 eligible. If 900 invited yields <120, add 100-record blocks to 1,200. Do not exceed 1,200 without amendment.
- **G3:** 20% double-coded (26 at base 130, 16 at reduced 81); adjudication complete; κ reported with CI; coding table frozen.
- **G4:** analysis script reproduces abstract/main-table numbers; sensitivity table complete; access bounds reported.
- **G5:** manuscript complete; second coder/co-author sign-off; data availability and LLM disclosure checked.
- **G6:** submission confirmation; preprint DOI; OSF update.

### 9.2 Deliverables

1. Frozen frame + hash.
2. OSF registration + DOI.
3. Calibration report.
4. Coding table + evidence quotes.
5. Reliability report.
6. Analysis scripts + reproducibility log.
7. Manuscript.
8. arXiv preprint.
9. Public data/code deposit (OSF/Zenodo).
10. Decision/deviation log.

### 9.3 9-month compressed option

If the start must be 2026-12-01 and the end must be 2027-08-31:
- Target 560 invited / 81 eligible (not 900/130).
- Calibration: weeks 3–5 (compressed).
- Retrieval/screening/coding: four blocks of 140 over **weeks 6–21 (16 weeks)**.
- Reliability: weeks 19–21, overlapping retrieval.
- Analysis: weeks 22–25.
- Writing: weeks 26–32 (7 weeks, ~20 h/week).
- Submission: weeks 33–35.
- Buffer: weeks 36–39.
- Precision ±7.2 pp; second coder 22 h.
- Retrieval averages 17.7 h/week over 16 weeks, with peaks near 22 h/week. This option is feasible only with protected time and a cooperative second coder; it leaves little room for access delays or a desk rejection. It is the fallback, not the recommendation.

---

## 10. Publication strategy

### 10.1 Primary target: Empirical Software Engineering (EMSE)

**Why:** EMSE publishes empirical software-engineering research with a strong empirical component, including replications and AI applications to SE. The study is an empirical audit of evaluation practice in SE/LLM code generation, not a bibliometric exercise. EMSE's single-blind review, data-availability requirement, and relatively fast first decision fit the project.

**Verified requirements:** single-blind; no mandatory submission fee on the subscription route; optional Open Choice APC (amount not stated on the pages checked); abstract 150–250 words; data-availability statement required for original research; median submission-to-first-decision 24 days (2025 metrics); LLM use must be documented. The production interval after acceptance is **not verified**; do not claim “online 3–5 weeks.”

**Risk:** editors/reviewers may see meta-science as out of scope. Mitigation: frame the paper as an empirical study of SE evaluation practice; lead with the SE benchmarks (HumanEval, MBPP, SWE-bench) and the practical consequence for SE claims; cite SE venue norms (ICSE, ASE, TOSEM) and the reproduction/artifact-evaluation literature.

**Submission package:** manuscript; supplementary coding table; analysis scripts; OSF/Zenodo DOI; data-availability statement; LLM disclosure; cover letter explaining fit and contribution.

### 10.2 Strong alternative: Data-centric Machine Learning Research (DMLR)

**Why:** DMLR's scope explicitly includes benchmarks, benchmarking methods, methodology and empirical evaluation, and audits of existing datasets/use. The study is a benchmark audit with a data-centric outcome. DMLR is single-blind via OpenReview, has no fees and no page limit, and reports 4–6 months turnaround. The 30% extension rule allows a conference paper to be extended.

**Risk:** DMLR reviewers may want broader benchmark coverage or a stronger data-centric intervention. Mitigation: emphasize the audit of benchmark use, the released coding instrument, and the contrast between test-level and dataset-level remediation.

**When to choose:** if EMSE desk-rejects or if the author wants a no-fee, longer-format venue with a data-centric audience.

### 10.3 Reframing alternatives: Scientometrics or Quantitative Science Studies (QSS)

**Scientometrics:** scope covers quantitative aspects of the production, communication, and use of scientific information; single-blind; hybrid; abstract 150–250; data-availability statement; optional Open Choice APC. A diffusion framing (citation → practice) fits, but the paper would need a stronger bibliometric contribution: citation-network context, field normalization, and perhaps a broader benchmark set. The current two-pair design may be too narrow for a bibliometrics audience.

**QSS:** official ISSI journal, MIT Press, open access; scope includes science of science, scholarly communication, indicators, and policy. The submission page is Cloudflare-blocked; search snippets say no submission fee and an APC for accepted papers, but the amount is unresolved ($800 vs $1,200 in third-party reports). Do not commit to QSS until the APC and scope are confirmed.

**When to choose:** if the author wants a science-of-science audience and is willing to broaden the frame or add citation-network analysis. This is a different paper, not a drop-in fallback.

### 10.4 Not recommended: TMLR

TMLR is double-blind, any length, CC BY 4.0, and uses OpenReview; acceptance is based on evidence and interest. It is a strong ML venue, but the fit for a meta-science/citation audit is weak. Reviewers may ask for an ML contribution that the study does not have. Use only if the paper is reframed around benchmark methodology and accepted by the ML community.

### 10.5 Preprint and dissemination

- Post on arXiv (cs.SE, cross-list cs.CL/cs.LG) after EMSE submission, subject to the journal's preprint policy; confirm at submission.
- Deposit data/code on OSF/Zenodo with a DOI.
- Present at a workshop on evaluation/reproducibility if a suitable venue appears; not required.
- Do not post the accepted version before the publisher's embargo; check the policy.

### 10.6 Authorship and credit

Lead researcher: conceptualization, methodology, data curation, formal analysis, investigation, writing – original draft. Second coder: validation, reliability, writing – review & editing if authorship criteria are met; otherwise acknowledgment. No honorary authorship.

### 10.7 What would change the venue choice

- EMSE desk-reject for scope → DMLR.
- Reviewers demand a broader bibliometric frame → Scientometrics/QSS, with a new frame and analysis (12+ months).
- Reviewers demand a causal design → not feasible with this frame; revise claims, not design.
- APC becomes mandatory and unfunded → choose EMSE subscription route or DMLR.

---

## 11. External dependencies

| Dependency | Critical? | Needed by | Current status | Mitigation / fallback |
|---|---|---|---|---|
| **Human second coder** | **Critical** | G0, 2026-12-14 | **Not secured.** | Recruit from SE/ML lab; 31.5 h over 12 months; fallback single-coder audit (§14.3). |
| **Institutional full-text access / ILL** | **Critical** | G0, 2026-12-14 | **Not confirmed.** | 50-record pretest; library/ILL; open-access restriction if <50%. |
| OSF registration | Important | G0, 2026-12-14 | Not created. | Self-serve; 1 day; DOI. |
| S2 API key | Optional | G1, 2027-01-11 | Not secured. | Backoff; request key; citation fetch is already done. |
| OpenAlex API key | Optional | Not needed | Daily budget exhausted. | Not required for primary; skip. |
| Statistician review | Optional | G4, 2027-06-28 | Not secured. | Internal review; pre-specified methods; ask a colleague. |
| APC funding | Optional | Submission | Unknown. | EMSE subscription route or DMLR (no fees). |
| Legal/licensing review | Optional | G5, 2027-08-23 | Not needed if quotes ≤60 words and no PDFs shared. | Institutional counsel if quotes exceed fair use. |
| Conference/workshop venue | Optional | Post-submission | Not selected. | arXiv + journal is sufficient. |

### 11.1 Dependency risks

- **Second coder dropout:** recruit a backup; document training; keep the blinded packet ready. If the coder drops after calibration, the fallback is a single-coder study with an LLM audit, not a claim of human reliability.
- **Access denial:** prioritize open-access and arXiv versions; use ILL; if a publisher blocks text mining, exclude and report. Do not circumvent paywalls.
- **API limits:** the frame is already fetched; no new API dependency for the primary analysis. A refresh is optional and can be skipped.

---

## 12. Threats to validity

### 12.1 Construct validity

**Threat:** documented adoption ≠ actual use. A paper may claim HumanEval+ but run HumanEval; a paper may use HumanEval+ silently.
**Mitigation:** evidence quotes, adoption locus, artifact-check subsample, sensitivity analysis; explicitly label the construct "documented adoption." Do not claim execution fidelity.

**Threat:** the rubric may conflate "use of a benchmark" with "adoption of a critique."
**Mitigation:** the boundary rule requires the critique's recommended artifact/protocol, not any improvement; independent remediation is coded separately.

### 12.2 Internal validity

**Threat:** coder bias and rubric drift.
**Mitigation:** pre-registration, blinded second coding, calibration, adjudication log, 10% audit, conservative rule for unresolved cases.

**Threat:** selection bias from access failure.
**Mitigation:** access pretest, metadata comparison, extreme bounds, report flow diagram.

**Threat:** sampling bias from title clustering or S2 coverage.
**Mitigation:** identifier + title dedupe, manual review of 14 multi-variant clusters, sensitivity on the 2,684-row frame.

### 12.3 External validity

**Threat:** findings may not generalize beyond code-generation benchmarks, English full texts, or the S2-indexed literature.
**Mitigation:** state the scope; do not claim universal benchmark-critique diffusion; invite replication on other pairs.

**Threat:** 2026 is incomplete; the frame overrepresents arXiv and ML/SE venues.
**Mitigation:** report year/venue distribution; sensitivity excluding 2026 and future-dated records.

### 12.4 Statistical conclusion validity

**Threat:** small eligible n, wide CIs, low power for H2.
**Mitigation:** pre-specify H1/H3 as confirmatory; label H2/H4 exploratory; report CIs, not just p-values; do not overinterpret null results.

**Threat:** multiple sensitivity analyses could be cherry-picked.
**Mitigation:** pre-specify the sensitivity list; report all; no post-hoc selection of the "best" result.

### 12.5 Benchmark-version validity

**Threat:** EvalPlus and SWE-bench+ changed over time; "adoption" may refer to different versions.
**Mitigation:** record `benchmark_version` and `critique_version`; report version distribution; do not score version differences as adoption differences.

---

## 13. Consolidated unresolved uncertainties

**Open (must be resolved or accepted as a limitation):**

1. **Human second coder** — not secured. Blocks the planned reliability claim. Resolution: C1 or fallback.
2. **General-frame full-text access** — unknown; pilot 93.1% is purposive. Blocks precision/access-bias certainty. Resolution: C2.
3. **Construct validity (documented vs actual use)** — inherent; cannot be fully resolved without executing every artifact. Accepted limitation; mitigate with evidence quotes and artifact-check subsample.
4. **S2 frame coverage** — misses non-indexed venues; 2026 incomplete; 42 no ID; 225 no date; 231 future-dated. Inherent; report and sensitivity.
5. **Self-citation/author overlap** — not yet measured. Add flag; sensitivity.
6. **SWE-bench+ preprint status / anonymous Zenodo creator** — inherent; report.
7. **QSS APC and submission terms** — unresolved; not blocking EMSE/DMLR.
8. **EMSE scope fit** — publication risk; mitigate framing; DMLR fallback.
9. **Access bias** — unknown direction; extreme bounds.
10. **Pilot estimate instability** — 1/6 primary-pair, 1/8 all-pair; planning value 12.5%; main study designed to narrow.

**Resolved in protocol v1.0 / rubric v1.1:**

11. **Unit of analysis** — title-level cluster; 14 multi-variant groups manually reviewed.
12. **Derivative-only papers** — ineligible.
13. **Partial vs full** — full only if the remediated artifact/protocol supports at least one main claim; otherwise partial.
14. **Generic citation cluster** — score 0; resolves the `promptcot` pilot disagreement toward 0.
15. **GSM1k** — excluded from primary; secondary contrast only.
16. **LLM role** — pre-screening/audit only; not human reliability; no paywalled full texts to external APIs.
17. **Frame refresh** — frozen; no mid-study refresh.
18. **Multiple comparisons** — H1/H3 confirmatory; H2/H4 exploratory.

---

## 14. Final decision

### 14.1 Decision

**NEEDS EXTERNAL INPUT.**

The protocol is complete and internally consistent. The frame is built, the rubric is specified, the pilot shows the coding task is tractable, and the analysis plan is prepared for registration. The study is therefore neither **READY TO EXECUTE** nor **NOT FEASIBLE**; it **NEEDS EXTERNAL INPUT**.

Two critical external inputs are missing:

1. **A human second coder** for the 20% blind reliability sample. Without this, the planned inter-rater reliability analysis cannot be executed. The pilot's κ values are LLM–LLM agreement and cannot substitute.
2. **A confirmed full-text access route** for the general frame. The pilot's 93.1% is from a purposive 29-paper frame; the 2,666-paper frame may have a lower rate, and access bias is a threat to the prevalence estimate.

A third Gate 0 item, OSF registration, is self-serve but must be completed before coding.

### 14.2 Flip conditions to READY TO EXECUTE

| ID | Condition | Deadline | Evidence |
|---|---|---|---|
| **C1** | One human second coder commits to 6 h calibration, blind coding of 20% of eligible papers (≥26 base / ≥16 reduced), and 6 h adjudication. | 2026-12-14 | Signed email/letter; calendar block; training plan. |
| **C2** | Access pretest on 50 random frame records achieves ≥70% full-text retrieval. | 2026-12-14 | Pretest log with route and failure reasons. |
| **C3** | OSF registration created with protocol v1.0, rubric v1.1, sampling script/seed, analysis plan, and frame hash. | 2026-12-14 | OSF DOI. |
| **C4** | Optional: S2 API key for any refresh; not blocking. | 2027-01-11 | Key confirmed. |

If C1–C3 are met: **READY TO EXECUTE** on 2026-12-15. If C2 is 50–70%, proceed with ILL and a documented access limitation. If C2 is <50%, restrict to open-access records and report the restriction, or pause.

### 14.3 Fallback if C1 fails

A single-coder study would **not** satisfy the planned protocol. If C1 fails:

- Target 80 eligible papers (560 invited at 80% access/18% eligibility).
- No human κ; run a 10% LLM-assisted audit and report agreement as a diagnostic, not reliability.
- Add a limitation paragraph: "No human second coder was available; reliability is not established."
- Submit to DMLR or post a preprint; do not claim EMSE-level reliability evidence.
- Record the deviation in the decision log and update OSF.

This fallback is feasible but weaker. It is not the recommended path.

### 14.4 What would make the study NOT FEASIBLE

- No second coder **and** access <50% **and** no institutional/ILL route.
- Fewer than 5% of accessible papers eligible after screening, with no supplement.
- Legal prohibition on text analysis or short quotation.
- Frame corruption or loss of the frozen citation data without a reproducible rebuild.

None of these is currently established.

### 14.5 What would change the decision to READY TO EXECUTE

Only the Gate 0 evidence above. More literature search, another pilot, or another feasibility report would not change the scientific design; it would delay execution. The next action is operational: recruit the coder, run the access pretest, register the protocol.

---

## 15. References

1. Liu, J., Xia, C. S., Wang, Y., & Zhang, L. (2023). *Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation.* NeurIPS 2023. arXiv:2305.01210. DOI: 10.52202/075280-0943. https://arxiv.org/abs/2305.01210
2. Aleithan, R., Xue, H., Mohajer, M. M., Nnorom, E., Uddin, G., & Wang, S. (2024). *SWE-Bench+: Enhanced Coding Benchmark for LLMs.* arXiv:2410.06992. https://arxiv.org/abs/2410.06992
3. SWE-bench+ dataset. Zenodo record 13879453. DOI: 10.5281/zenodo.13879453. https://zenodo.org/records/13879453
4. EvalPlus artifact. GitHub `evalplus/evalplus`. Apache-2.0. https://github.com/evalplus/evalplus
5. Chen, M., Tworek, J., Jun, H., et al. (2021). *Evaluating Large Language Models Trained on Code.* arXiv:2107.03374. https://arxiv.org/abs/2107.03374
6. Austin, J., Odena, A., Nye, M., et al. (2021). *Program Synthesis with Large Language Models.* arXiv:2108.07732. https://arxiv.org/abs/2108.07732
7. Jimenez, C. E., Yang, J., Wettig, A., et al. (2023). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv:2310.06770; ICLR 2024. https://arxiv.org/abs/2310.06770
8. Zhang, H., Da, J., Lee, D., et al. (2024). *A Careful Examination of Large Language Model Performance on Grade School Arithmetic.* arXiv:2405.00332. https://arxiv.org/abs/2405.00332
9. GSM1k dataset. Hugging Face `ScaleAI/gsm1k`. https://huggingface.co/datasets/ScaleAI/gsm1k
10. Merzah, B. M. (2026). *Replication materials for "Cited but Not Used: Documented Adoption and Data Accessibility in 40 Non-English NLP Benchmarks."* Zenodo. DOI: 10.5281/zenodo.23634794. https://doi.org/10.5281/zenodo.23634794
11. Small, H. (1978). Cited documents as concept symbols. *Social Studies of Science*, 8(3), 327–340. DOI: 10.1177/030631277800800305. https://doi.org/10.1177/030631277800800305
12. Kapoor, S., & Narayanan, A. (2023). Leakage and the reproducibility crisis in machine-learning-based science. *Patterns*, 4(9), 100804. DOI: 10.1016/j.patter.2023.100804. https://doi.org/10.1016/j.patter.2023.100804
13. Dehghani, M., Tay, Y., Bahri, D., & Metzler, D. (2021). *The Benchmark Lottery.* arXiv:2107.07002. https://arxiv.org/abs/2107.07002
14. Empirical Software Engineering (EMSE), Springer. Journal home and submission guidelines. https://link.springer.com/journal/10664
15. Data-centric Machine Learning Research (DMLR). Scope, submissions, acceptance criteria. https://data.mlr.press/
16. Scientometrics, Springer. Journal home and submission guidelines. https://link.springer.com/journal/11192
17. Quantitative Science Studies (QSS), MIT Press. https://direct.mit.edu/qss
18. Transactions on Machine Learning Research (TMLR). https://jmlr.org/tmlr/

*All URLs verified 2026-11-13. Some publisher pages block automated access; see `verification/journal_requirements.md` for the access route and exact verified claims.*
