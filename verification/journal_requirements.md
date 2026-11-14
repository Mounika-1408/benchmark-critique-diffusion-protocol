# Journal Requirements and Venue Assessment

**Verified:** 13 November 2026  
**Purpose:** Record the exact, source-backed requirements for each candidate venue so that the publication plan in `PROTOCOL.md` §10 rests on verified facts rather than memory.

**Access note:** Publisher pages change and some block automated access. Each row states the access result on 2026-11-13. “HTTP 200” means the page was retrieved; it does not guarantee that every clause was parsed.

---

## 1. Primary target — Empirical Software Engineering (EMSE)

**Publisher:** Springer Nature  
**Journal home:** https://link.springer.com/journal/10664 (HTTP 200)  
**Submission guidelines:** https://link.springer.com/journal/10664/submission-guidelines (HTTP 200)  
**Aims and scope:** https://link.springer.com/journal/10664/aims-and-scope (HTTP 200)

### 1.1 Verified requirements

| Requirement | Verified detail | Source |
|---|---|---|
| Publishing model | **Hybrid** | Journal home: “Publishing model : Hybrid.” |
| Peer review | **Single-blind** | Guidelines: “This journal follows a single-blind reviewing procedure.” |
| Abstract length | **150–250 words** | Guidelines: “Please provide an abstract of 150 to 250 words.” |
| Data availability | **Mandatory data availability statement for all original research** | Guidelines: “All original research must include a data availability statement.” |
| Submission fee | **No mandatory submission fee stated**; subscription route is available. Optional Open Choice APC exists but its amount is not stated on the pages checked. | Hybrid model; guidelines list “Open Choice” under “After acceptance.” |
| Scope | “Applied software engineering research with a strong empirical component”; studies that “can be replicated or expanded upon.” | Aims and scope page. |
| Journal metrics (2025) | JIF 3.4; 5-year JIF 4.0; **median submission-to-first-decision 24 days**; 1.1M downloads (2025). | Journal home metrics block. |
| Production interval after acceptance | **Not verified.** Earlier drafts said “online 3–5 weeks”; that claim has been removed. | No source found on the pages checked. |

### 1.2 Fit assessment

**Strengths**

- The study is an empirical audit of evaluation practice in software engineering / LLM code generation, with HumanEval, MBPP, and SWE-bench as the object. That is applied SE research with a strong empirical component.
- EMSE explicitly values studies that can be replicated or expanded; the frozen frame, rubric, scripts, and coding table are designed for exactly that.
- The data-availability requirement is compatible with the planned OSF/Zenodo deposit.
- A 24-day median first decision is favorable for a 12-month project with a submission buffer.

**Risks**

- Editors or reviewers may classify a citation audit as meta-science or bibliometrics rather than empirical SE. The cover letter and introduction must lead with the SE consequence: claims about code-generation progress rest on benchmarks whose known defects are often cited but not acted on.
- EMSE reviewers may ask for a stronger SE-theory framing or a broader benchmark set. The response is to keep the two-pair design and frame it as a focused audit, not a universal diffusion study.
- The single-blind model means the author’s identity is visible; no action needed beyond normal professionalism.

**Verdict:** **Primary target.** Best scope and timeline fit; the meta-science risk is manageable with framing.

---

## 2. Strong alternative — Data-centric Machine Learning Research (DMLR)

**Publisher:** DMLR (OpenReview-hosted)  
**Home:** https://data.mlr.press/ (HTTP 200)  
**Submission guidelines:** https://data.mlr.press/submissions (HTTP 200)

### 2.1 Verified requirements

| Requirement | Verified detail | Source |
|---|---|---|
| Peer review | **Single-blind**; authors’ identities are not anonymized. | Home: “The DMLR employs a single-blind review system in which authors' identities are not anonymized.” |
| Fees | **No fees or payments** from authors, reviewers, action editors, or editors-in-chief; published material is open access without cost. | Submissions: “DMLR also does not require any fees or payments from authors, reviewers, action editors, or editors-in-chief.” |
| Page limit | **None.** “Submissions are not constrained by a page limit”; lengthy papers may take longer to review. | Submissions page. |
| Turnaround | Usually **4–6 months**; up to 10 months in exceptional cases. | Submissions: “The expected turnaround time for the decision is usually between 4 and 6 months.” |
| Extended work | Prior work must be from a conference or workshop (not a journal); the DMLR version needs **at least 30% additional content**. | Submissions FAQ. |
| Scope | “Benchmarks for machine learning research (collections of datasets with particular aims)”; “Benchmarking tools and methods”; “Methodology and empirical evaluation of data collection processes…”. | Submissions scope list. |
| Open access | All published material promptly accessible without associated costs. | Submissions: “Open access policy.” |
| Submission system | OpenReview. | Home and submissions pages. |

### 2.2 Fit assessment

**Strengths**

- The scope explicitly includes benchmarks, benchmarking tools and methods, and empirical evaluation of data practices. A citation audit of benchmark adoption is a data-centric contribution.
- No fees and no page limit suit a study with a large supplement (coding table, evidence quotes, sensitivity analyses).
- The 30% extension rule is irrelevant for an original paper but useful if a workshop version is produced first.
- Single-blind review is compatible with the project; no anonymization burden.

**Risks**

- DMLR reviewers may want a data-centric intervention (a new dataset, metric, or tool), not only an audit. The coding instrument and the released frame are the data-centric products; the paper should present them as reusable infrastructure.
- The 4–6 month turnaround is longer than EMSE’s median first decision, which matters for the 12-month buffer.
- DMLR’s audience may be less familiar with SE venue norms; the paper must explain why HumanEval/MBPP/SWE-bench are the right cases.

**Verdict:** **Strongest alternative.** Choose if EMSE desk-rejects for scope, or if a no-fee, longer-format venue with a data-centric audience is preferred.

---

## 3. Reframing option — Scientometrics

**Publisher:** Springer Nature  
**Journal home:** https://link.springer.com/journal/11192 (HTTP 200)  
**Submission guidelines:** https://link.springer.com/journal/11192/submission-guidelines (HTTP 200)

### 3.1 Verified requirements

| Requirement | Verified detail | Source |
|---|---|---|
| Publishing model | **Hybrid** | Journal home: “Publishing model : Hybrid.” |
| Peer review | **Single-blind** | Guidelines: “This journal follows a single-blind reviewing procedure.” |
| Abstract length | **150–250 words** | Guidelines: “Please provide an abstract of 150 to 250 words.” |
| Data availability | Data availability statement supported/required under Springer’s research data policy. | Guidelines section “Research Data Policy and Data Availability Statements.” |
| Scope | Quantitative aspects of the science of science, communication in science, and science policy. | Journal tagline and aims/scope. |

### 3.2 Fit assessment

**Strengths**

- A diffusion framing (citation → practice) is a science-of-science question. The four-level adoption scale and the citation-frame design fit a bibliometric audience.
- Single-blind review and a 150–250 word abstract are compatible with the current manuscript plan.

**Risks**

- The current two-pair design is narrow for a bibliometrics journal. Reviewers may expect citation-network context, field normalization, or a broader benchmark set.
- Turning the study into a Scientometrics paper is **a different paper**, not a drop-in fallback: it needs a stronger bibliometric contribution and probably a larger frame.
- The applied SE consequence, which is the current paper’s hook, would become secondary.

**Verdict:** **Reframing option only.** Do not submit the current design unchanged. Consider if the author wants a science-of-science audience and is willing to add citation-network analysis or broaden the benchmark set.

---

## 4. Reframing option — Quantitative Science Studies (QSS)

**Publisher:** MIT Press; open access  
**Journal site:** https://direct.mit.edu/qss  
**Submission pages attempted:** https://direct.mit.edu/qss/pages/submission-guidelines; https://direct.mit.edu/qss/pages/submissions

### 4.1 Verification status

| Item | Status | Evidence |
|---|---|---|
| Site reachable | **No** | HTTP 403 (Cloudflare “Just a moment…” challenge) on 2026-11-13 for both submission URLs and the MIT Press redirect. |
| Open access | **Partially verified** | Prior retrieval indicated MIT Press open access; not re-verified in this pass because of the 403. |
| APC / submission fee | **UNRESOLVED** | Third-party reports conflict (roughly $800 vs $1,200). No official page could be read. |
| Abstract/format requirements | **UNRESOLVED** | Not readable in this pass. |
| Scope fit | Plausible for science-of-science, but not verified against the current aims page. | Prior retrieval; not re-verified. |

### 4.2 Fit assessment

**Strengths (conditional)**

- QSS is a natural venue for a science-of-science study of evaluation practice.
- Open access would maximize reach.

**Risks**

- The APC is unresolved and could be a hard blocker for an unfunded independent researcher.
- The current design may be too narrow for QSS without a broader bibliometric frame.
- A 403-blocked submission page is not a basis for a venue commitment.

**Verdict:** **Do not commit.** Re-check the official submission page from a normal browser, confirm the APC and scope, and treat QSS as a post-EMSE/DMLR option only.

---

## 5. Not recommended — Transactions on Machine Learning Research (TMLR)

**Publisher:** JMLR  
**Home:** https://jmlr.org/tmlr/ (HTTP 200)

### 5.1 Verified facts

| Item | Verified detail | Source |
|---|---|---|
| Review model | **Double-blind** | Home: “providing fast turnarounds and double blind reviewing.” |
| Submission system | OpenReview. | Home: “We use the reviewing and publication systems on OpenReview.” |
| Format | Variable manuscript length; shorter-format manuscripts typical of conferences. | Home. |
| Fit | Weak for a citation audit; TMLR expects an ML contribution. | Judgment based on scope and audience. |

### 5.2 Assessment

TMLR is a strong ML venue, but a meta-science/citation audit is not an ML contribution in TMLR’s sense. Submitting there would invite requests for an ML method or a benchmark contribution the study does not have. **Do not use TMLR as a fallback** unless the paper is fundamentally reframed around benchmark methodology and an ML audience accepts the reframing.

---

## 6. Requirements matrix for the current manuscript

| Manuscript element | EMSE | DMLR | Scientometrics | QSS |
|---|---|---|---|---|
| Single-blind compatible | Yes | Yes | Yes | Unknown |
| Double-blind required | No | No | No | Unknown |
| Abstract 150–250 | **Yes** | Not specified | **Yes** | Unknown |
| Data availability statement | **Required** | Expected (open data policy) | Supported/required | Unknown |
| No mandatory fee | Subscription route | **Yes** | Hybrid subscription route | **Unresolved** |
| Page limit | Journal norm | **None** | Journal norm | Unknown |
| Open access | Optional | **Yes, no cost** | Optional | **Yes (APC unresolved)** |
| Fit for two-pair audit | **Strong** | **Strong** | Moderate (reframe) | Moderate (reframe) |
| Recommended role | **Primary** | **Alternative** | Reframe | Defer |

---

## 7. Submission-time checklist (all venues)

Before submitting, re-verify on the live site and record the date:

- [ ] Current peer-review model and anonymity requirements.
- [ ] Abstract word limit and structure.
- [ ] Data availability statement wording and repository requirements.
- [ ] LLM-use disclosure policy (EMSE/Springer and DMLR/OpenReview policies may differ).
- [ ] APC or Open Choice amount, and whether the subscription route is available.
- [ ] Preprint policy (arXiv timing, embargo, accepted-version rules).
- [ ] Supplementary-material format and size limits.
- [ ] Whether the journal requires a cover letter and suggested reviewers.
- [ ] Whether the journal accepts a registered report or preregistration; if yes, consider it.

**Record the exact requirement and URL in this file when checked.** Do not rely on this snapshot after 2026-11-13 without re-checking.

---

## 8. Decision

**Primary:** EMSE. **Alternative:** DMLR. **Reframe only:** Scientometrics, QSS. **Not recommended:** TMLR.

The venue decision does **not** block Gate 0. The protocol can be registered and the access pretest run before choosing between EMSE and DMLR. The choice can be made at submission, after the results are known and the framing is settled.
