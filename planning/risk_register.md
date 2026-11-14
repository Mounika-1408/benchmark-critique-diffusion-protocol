# Risk Register

**Version:** 1.0  
**Prepared:** 13 November 2026  
**Owner:** Syed Abdul Aman (independent researcher)  
**Review cadence:** end of Gate 0, end of each retrieval block (weeks 11, 15, 19, 24), and at each gate G1–G6.

**Scoring:** likelihood 1–5 (1 = rare, 5 = near-certain); impact 1–5 (1 = cosmetic, 5 = study cannot produce a defensible result); score = likelihood × impact. Bands: **Low** 1–4, **Moderate** 5–9, **High** 10–15, **Critical** 16–25.

---

## 1. Summary matrix

| ID | Risk | L | I | Score | Band | Trigger | Owner |
|---|---|---:|---:|---:|---|---|---|
| R1 | Human second coder not secured, or drops out | 4 | 5 | 20 | **Critical** | No signed commitment by 2026-12-14; missed calibration session | Researcher |
| R2 | Full-text access below plan | 4 | 4 | 16 | **Critical** | 50-record pretest <70%; block access rate <70% | Researcher |
| R3 | Eligibility rate far below 18% | 3 | 4 | 12 | **High** | <10% eligible after block 1 | Researcher |
| R4 | Cap case (1,200) exceeds available hours | 3 | 4 | 12 | **High** | Projection >20 h/week or end date at risk | Researcher |
| R5 | Frame corruption or hash mismatch | 2 | 5 | 10 | **High** | SHA-256 mismatch; row count ≠ 2,666 | Researcher |
| R6 | EMSE desk rejection for scope | 3 | 3 | 9 | **Moderate** | Desk reject before review | Researcher |
| R7 | APC or fee cannot be covered | 2 | 3 | 6 | **Moderate** | Only open-access route offered; APC >$0 | Researcher |
| R8 | Copyright / text-mining restriction | 2 | 4 | 8 | **Moderate** | Publisher blocks quotation or TDM | Researcher |
| R9 | Construct validity: documented adoption ≠ execution | 4 | 4 | 16 | **Critical** | Reviewers challenge the outcome measure | Researcher |
| R10 | Reliability below threshold (κ <0.40) | 3 | 3 | 9 | **Moderate** | Calibration κ <0.40; drift at G3 | Researcher + coder |
| R11 | Sampling or weighting error | 2 | 5 | 10 | **High** | Sample strata do not match frame; weights wrong | Researcher |
| R12 | Data loss or unversioned edits | 2 | 4 | 8 | **Moderate** | Coding CSV overwritten; no backup | Researcher |
| R13 | LLM-disclosure or reproducibility failure | 2 | 3 | 6 | **Moderate** | Journal requires disclosure not yet written | Researcher |
| R14 | Scope creep beyond two pairs | 3 | 3 | 9 | **Moderate** | Requests to add benchmarks or a full census | Researcher |
| R15 | S2 frame staleness or API unavailability | 4 | 2 | 8 | **Moderate** | Frame older than retrieval date; API 429 | Researcher |
| R16 | Schedule overrun from Gate 0 slip | 3 | 3 | 9 | **Moderate** | G0 not met by 2026-12-14 | Researcher |

**Critical (16–25):** R1, R2, R9. **High (10–15):** R3, R4, R5, R11. The critical risks are external or construct-level; none is solved by working harder on the coding.

---

## 2. Risk detail

### R1 — Human second coder not secured, or drops out

**Description.** The registered protocol requires a human second coder for calibration and 20% blind double-coding. No commitment exists as of 2026-11-13. The pilot’s κ values are LLM–LLM agreement and cannot substitute.

**Likelihood 4 / Impact 5 / Score 20 — Critical.**

**Early indicators**
- No reply to the invitation by 2026-12-07.
- Commitment is verbal or conditional (“maybe in January”).
- Coder misses the calibration window (weeks 3–6).
- Coder’s availability falls below 6 h calibration + 19.5 h coding + 6 h adjudication.

**Mitigation**
- Send a written role description with exact hours and dates in week 1.
- Offer co-authorship for substantive contribution, or a fixed honorarium if funding exists.
- Identify a backup coder before G0; do not rely on one person.
- Keep calibration packets ready so a late coder can start without delaying retrieval.
- If the coder drops after calibration but before reliability, use the documented fallback (R1 trigger path) rather than inventing reliability.

**Trigger and response**
- **No signed commitment by 2026-12-14:** decision remains **NEEDS EXTERNAL INPUT**; do not start main coding.
- **Dropout before calibration:** recruit replacement; delay G1; do not start retrieval.
- **Dropout after calibration, before reliability:** switch to the single-coder fallback (80 eligible, no human κ, LLM audit as diagnostic only), switch venue to DMLR/preprint, and record the deviation. This is a weaker study and must not be presented as the registered protocol.
- **Dropout after reliability coding:** retain the completed double-coded sample; do not claim more reliability than was collected.

**Owner:** Researcher. **Gate:** G0, G1, G3.

---

### R2 — Full-text access below plan

**Description.** The base case assumes 80% access. The only evidence is the purposive pilot’s 93.1%, which over-represents easily accessible papers. If access is 50%, the 900 design yields ~81 eligible (±7.2 pp); at 50% access and 10% eligibility it yields ~45 eligible (±10.0 pp).

**Likelihood 4 / Impact 4 / Score 16 — Critical.**

**Early indicators**
- 50-record pretest <70%.
- Block 1 access rate <70% after 100 records.
- Failures concentrated in a venue, year, or stratum.
- ILL queue exceeds two weeks per item.

**Mitigation**
- Run the 50-record pretest with a separate seed before the main draw (C2).
- Confirm library/ILL quota and turnaround in week 1.
- Prioritize DOI/publisher and arXiv routes; record every failure reason.
- Prepare an open-access-restriction amendment in advance; do not improvise it mid-study.
- Compare accessible vs inaccessible records on year, venue, and identifiers; report access bounds.

**Trigger and response**
- **50–70% access:** proceed with ILL plan; report stratum-specific access rates; use extreme bounds.
- **<50% access:** pause and secure institutional access, or restrict the primary frame to open-access/arXiv records as a registered amendment. Do not code from abstracts.
- **Differential access by stratum:** report both unweighted and access-adjusted estimates; do not silently treat access failure as random.

**Owner:** Researcher. **Gate:** G0 (C2), G2.

---

### R3 — Eligibility rate far below 18%

**Description.** 18% is a planning assumption, not a measured rate. At 10% eligibility and 80% access, 900 invited yields ~72 eligible (±7.7 pp); the 1,200 cap yields ~96 (±6.6 pp).

**Likelihood 3 / Impact 4 / Score 12 — High.**

**Early indicators**
- <10% eligible after block 1 (225 invited).
- Ineligibility dominated by “cites but does not use the criticized benchmark” or “not a research paper.”
- Eligibility estimate drifts downward across blocks.

**Mitigation**
- Pre-test the eligibility rule on 20 calibration papers.
- Record ineligibility reasons with counts so the flow diagram explains the shortfall.
- Use the stop rule: add 100-record blocks up to 1,200 only if the added precision is worth the workload.
- Report the realized eligible count and CI; do not extend without an amendment.

**Trigger and response**
- **<10% at block 1:** recalculate precision; decide whether the 900 design is still reportable (±7.7 pp is reportable) or whether to add blocks.
- **Cap reached with <120 eligible:** stop, report the shortfall, and do not extend. A prevalence estimate with a wide CI is still a result; an unregistered extension is not.

**Owner:** Researcher. **Gate:** G2.

---

### R4 — Cap case (1,200) exceeds available hours

**Description.** The cap case is ~1,006 h, or 19.4 h/week over 52 weeks, with retrieval peaks near 25 h/week. The base plan is 16.0 h/week with peaks of 20–21. The cap is not workload-neutral.

**Likelihood 3 / Impact 4 / Score 12 — High.**

**Early indicators**
- Weekly hours exceed 20 for two consecutive weeks.
- Add-on block started after week 27.
- Writing or analysis time being borrowed to finish retrieval.

**Mitigation**
- Protect 20–21 h/week for weeks 7–34; do not plan a uniform 16 h/week.
- Decide before week 25 whether the cap is affordable.
- If not, stop at 900 and report the realized precision.
- If the cap is triggered, extend 4–8 weeks or reduce scope; do not compress coding quality.

**Trigger and response**
- **Projection >20 h/week:** stop adding blocks; document the precision actually achieved.
- **Cap triggered with protected time unavailable:** extend the project by 4–8 weeks using the buffer, or drop to the 9-month reduced design (560/81) if the end date is fixed.

**Owner:** Researcher. **Gate:** G2, G4.

---

### R5 — Frame corruption or hash mismatch

**Description.** The analysis frame is frozen at 2,666 title clusters with SHA-256 `6a0a374b…`. A changed CSV invalidates the sampling and the registration.

**Likelihood 2 / Impact 5 / Score 10 — High.**

**Early indicators**
- Row count ≠ 2,666.
- SHA-256 ≠ `6a0a374ba6120b244418e887a76a83d6bfb8a95dd61cfc822cf349ac7043d30c`.
- Duplicate `cluster_id` values.
- Strata counts ≠ 2,531 / 135.

**Mitigation**
- Verify the hash before every sample draw and at G0.
- Keep the frozen CSV read-only; never edit it in place.
- Rebuild only from the frozen source and compare counts; never “fix” a row by hand.
- Back up the frame and summary to a second location.

**Trigger and response**
- **Hash mismatch:** stop. Rebuild from the frozen source and verify. Do not sample from a changed frame.
- **Source cannot be rebuilt:** the study cannot proceed as registered; document and pause.

**Owner:** Researcher. **Gate:** G0, G2.

---

### R6 — EMSE desk rejection for scope

**Description.** EMSE is the primary target, but editors may classify a citation audit as meta-science or bibliometrics rather than empirical SE.

**Likelihood 3 / Impact 3 / Score 9 — Moderate.**

**Early indicators**
- Desk-reject decision within days of submission.
- Editor comment on “out of scope” or “better suited to Scientometrics.”

**Mitigation**
- Lead the cover letter and introduction with the SE consequence: claims about code-generation progress rest on benchmarks whose known defects are cited but not acted on.
- Cite SE venue norms and artifact-evaluation literature.
- Keep the two-pair design; do not expand to appease a scope objection.
- Prepare the DMLR reformat in advance (same manuscript, different cover letter).

**Trigger and response**
- **Desk reject:** reformat for DMLR within 4 weeks; keep the preprint live; record the decision.
- **Reject after review:** use the reviews to strengthen the paper; DMLR or a reframed Scientometrics submission only if the contribution genuinely changes.

**Owner:** Researcher. **Gate:** G6.

---

### R7 — APC or fee cannot be covered

**Description.** EMSE’s subscription route has no mandatory fee; the optional Open Choice APC amount is not stated on the pages checked. DMLR has no fees. QSS APC is unresolved.

**Likelihood 2 / Impact 3 / Score 6 — Moderate.**

**Early indicators**
- Acceptance conditional on an APC the researcher cannot pay.
- Journal moves to fully open access.

**Mitigation**
- Prefer the subscription route at EMSE; confirm at submission.
- Keep DMLR as the no-fee alternative.
- Do not commit to QSS until the APC is confirmed from the official page.
- If an APC is required, ask about waivers before accepting.

**Trigger and response**
- **APC required and unaffordable:** decline the open-access option if the subscription route is available; otherwise switch to DMLR.
- **No fee-free route:** treat the venue as unavailable and record why.

**Owner:** Researcher. **Gate:** G6.

---

### R8 — Copyright / text-mining restriction

**Description.** The study quotes short passages as evidence. Some publishers restrict TDM or quotation; sending paywalled full texts to external APIs may violate terms.

**Likelihood 2 / Impact 4 / Score 8 — Moderate.**

**Early indicators**
- Publisher terms prohibit TDM or storage.
- A request to remove evidence quotes.
- An LLM API’s terms conflict with paywalled text.

**Mitigation**
- Quote only the minimum needed; store evidence in a non-public working file.
- Do not send paywalled full texts to external APIs; use abstracts/metadata or a local model.
- Public deposit contains the coding table and derived evidence fields, not PDFs.
- Check the target journal’s copyright policy before submission.

**Trigger and response**
- **Restriction discovered:** remove the affected quotes from the public deposit; keep the coding decision and a paraphrased rationale.
- **Blanket TDM prohibition:** exclude that publisher’s records from the evidence-quote field; code from what is permitted and record the limitation.

**Owner:** Researcher. **Gate:** G3, G6.

---

### R9 — Construct validity: documented adoption ≠ execution

**Description.** The outcome is *documented protocol adoption*: the paper says it used the remediated benchmark/protocol. It does not verify that the harness ran correctly. Reviewers may argue the study measures rhetoric, not practice.

**Likelihood 4 / Impact 4 / Score 16 — Critical.**

**Early indicators**
- Reviewers ask for execution checks.
- Evidence quotes show “we use HumanEval+” but the results table is ambiguous.
- Artifact-check subsample reveals misreporting.

**Mitigation**
- Name the construct precisely in the title, abstract, and methods: “documented adoption,” not “adoption” simpliciter.
- Require an evidence quote for every score ≥2.
- Include an artifact-check subsample (e.g., 10–20 papers with public code) and report the concordance rate; label it a validation subsample, not a full audit.
- Pre-specify that execution fidelity is out of scope and explain why (cost, incomplete artifacts).
- Use the “citation only” (0) vs “acknowledged” (1) distinction to separate awareness from action.

**Trigger and response**
- **Reviewer rejects the construct:** add the artifact-check results and a limitations paragraph; do not claim execution.
- **Artifact check shows low concordance:** report it prominently; the paper’s contribution becomes “documented adoption overstates practice,” which is still a finding.

**Owner:** Researcher. **Gate:** G4, G5.

---

### R10 — Reliability below threshold

**Description.** Weighted κ may fall below 0.40 because the ordinal rubric is judgment-heavy, or because adoption is rare and κ is unstable.

**Likelihood 3 / Impact 3 / Score 9 — Moderate.**

**Early indicators**
- Calibration κ <0.40.
- Disagreements cluster on the 1 vs 2 boundary.
- Prevalence of score 3 <10%, making κ unstable.

**Mitigation**
- Calibrate on 20 fresh papers before retrieval.
- Use rubric v1.1’s generic-citation-cluster rule and evidence-quote requirement.
- Report PABAK alongside κ when prevalence is <10%.
- If κ <0.40, revise the rubric and repeat calibration with 10 new papers (adds 2–3 weeks).

**Trigger and response**
- **κ 0.40–0.59:** proceed with a limitation paragraph and sensitivity analysis using the second coder’s scores.
- **κ <0.40 after one revision:** consider collapsing 1 and 2 into a single “acknowledged/partial” category for the reliability analysis; report the collapse as a deviation.
- **Still <0.40:** the ordinal scale is not reliable enough for the primary analysis; report the binary adoption estimate and treat the ordinal typology as descriptive only.

**Owner:** Researcher + second coder. **Gate:** G1, G3.

---

### R11 — Sampling or weighting error

**Description.** The design is 135 SWE-bench+ census + 765 EvalPlus-only sample, with proportional allocation by year. A wrong denominator, wrong stratum label, or unweighted pooled estimate would bias the prevalence.

**Likelihood 2 / Impact 5 / Score 10 — High.**

**Early indicators**
- Sample strata counts ≠ 135 / 765.
- Duplicate clusters in the sample.
- Pooled estimate equals a simple average of stratum rates rather than a weighted estimate.
- Year distribution of the sample differs materially from the frame.

**Mitigation**
- Draw with a committed seed and script; record the seed and hash in OSF.
- Verify unique `cluster_id`, stratum counts, and year distribution after the draw.
- Pre-specify the weighting: SWE-bench+ census weight 1; EvalPlus-only sampled with known inclusion probability; pooled estimate weighted by frame stratum size.
- Recompute the estimate from the coding CSV, not from a hand table.

**Trigger and response**
- **Sample mismatch:** redraw from the frozen frame with the same seed and a corrected script; record the change.
- **Weighting error discovered after coding:** recompute; do not change the coding to fit the estimate.

**Owner:** Researcher. **Gate:** G0, G4.

---

### R12 — Data loss or unversioned edits

**Description.** The coding table is the study’s primary data. A overwritten CSV or an unlogged edit destroys reproducibility.

**Likelihood 2 / Impact 4 / Score 8 — Moderate.**

**Early indicators**
- More than one “final” coding file.
- No dated backup.
- Edits made without an adjudication note.

**Mitigation**
- One canonical coding CSV; dated backups after each block.
- Never edit the frozen frame; never edit the coding CSV by hand after G3.
- Log every post-G3 change as an amendment with a reason.
- Keep the analysis script and coding CSV together in the deposit.

**Trigger and response**
- **Corruption:** restore the last dated backup; reconcile against the adjudication log; document the recovery.
- **Silent edit:** treat the affected codes as unreliability; re-code or flag.

**Owner:** Researcher. **Gate:** G3, G6.

---

### R13 — LLM-disclosure or reproducibility failure

**Description.** Journals increasingly require disclosure of LLM assistance. The study uses LLMs for pilot coding and possibly pre-screening; the manuscript must describe this accurately without presenting LLM output as human reliability.

**Likelihood 2 / Impact 3 / Score 6 — Moderate.**

**Early indicators**
- Journal submission form asks for an LLM-use statement.
- Reviewers ask how the pilot codes were produced.

**Mitigation**
- Write the disclosure early: which model, which task, which prompts, what was human-checked.
- State that pilot κ is LLM–LLM agreement, not human reliability.
- Keep prompts and outputs for the audit; do not send paywalled text to external APIs.
- Deposit the analysis script so every number recomputes.

**Trigger and response**
- **Disclosure requirement exceeded by the study’s records:** reconstruct from logs; if impossible, report the gap.
- **Reviewer challenges LLM use:** provide the audit trail; do not overclaim human validation.

**Owner:** Researcher. **Gate:** G5, G6.

---

### R14 — Scope creep beyond two pairs

**Description.** Reviewers or collaborators may ask for GSM1k in the primary denominator, more benchmarks, a full census, or a citation-network analysis. Each expansion raises workload and weakens the focused design.

**Likelihood 3 / Impact 3 / Score 9 — Moderate.**

**Early indicators**
- A request to “just add” another benchmark.
- Pressure to make the study a general diffusion study.
- Sample size creeping beyond 1,200 without an amendment.

**Mitigation**
- Keep GSM1k as a secondary task-fit contrast, explicitly excluded from the primary denominator.
- State the two-pair scope in the title and abstract.
- Treat expansions as new studies or registered amendments with a workload estimate.
- Use the “focused audit, not universal diffusion study” framing.

**Trigger and response**
- **Reviewer requests expansion:** add as a limitation/future work; only expand if the added analysis is cheap and pre-specified.
- **Collaborator requests a census:** show the workload table; decline or renegotiate the timeline.

**Owner:** Researcher. **Gate:** G5.

---

### R15 — S2 frame staleness or API unavailability

**Description.** The frame is a Semantic Scholar snapshot retrieved 2026-11-13. S2 updates continuously; a re-fetch would change counts. The live API returned 429 on re-check.

**Likelihood 4 / Impact 2 / Score 8 — Moderate.**

**Early indicators**
- A re-fetch returns materially different counts.
- API requires a key or paid tier.
- Missing 2026 records become apparent.

**Mitigation**
- Freeze the frame and state the retrieval date in every methods section.
- Do not refresh mid-study; if a refresh is unavoidable, treat it as an amendment and re-register.
- Report the S2 coverage limitation (non-indexed venues, books, theses).
- Keep the raw retrieval files and hashes.

**Trigger and response**
- **Frame found incomplete:** report as a limitation; do not silently add records.
- **Refresh required by reviewers:** run a sensitivity analysis on the refreshed frame; keep the frozen frame as primary.

**Owner:** Researcher. **Gate:** G0, G5.

---

### R16 — Schedule overrun from Gate 0 slip

**Description.** Every week of Gate 0 delay shifts the 52-week plan. If G0 slips past 2026-12-14, the end date moves and the buffer shrinks.

**Likelihood 3 / Impact 3 / Score 9 — Moderate.**

**Early indicators**
- C1/C2/C3 not met by 2026-12-07.
- OSF registration blocked by a technical issue.
- Access pretest incomplete.

**Mitigation**
- Start C1 and C2 in week 1, not week 2.
- Prepare the OSF materials before creating the registration.
- Treat the 2026-12-14 date as a hard review, not a soft target.
- If G0 slips, shift the calendar but keep the phase structure; do not compress retrieval.

**Trigger and response**
- **G0 slips 1–2 weeks:** shift all dates; keep 24-week retrieval.
- **G0 slips >4 weeks:** reassess the 12-month design; consider the 9-month reduced option only if the end date is fixed and the reduced sample is acceptable.

**Owner:** Researcher. **Gate:** G0.

---

## 3. Top five risks and the one-line response

| Rank | Risk | Response |
|---:|---|---|
| 1 | R1 second coder | Signed commitment by 2026-12-14 or the study stays **NEEDS EXTERNAL INPUT**. |
| 2 | R2 access | 50-record pretest; <50% triggers an open-access amendment or a pause. |
| 3 | R9 construct validity | Name the outcome “documented adoption”; add an artifact-check subsample; never claim execution. |
| 4 | R3 low eligibility | Stop rule and honest CI; do not extend past 1,200 without an amendment. |
| 5 | R4 cap-case workload | Decide before week 25; protect 25 h/week or stop at 900. |

---

## 4. Risk review log

| Date | Event | Changes | Next review |
|---|---|---|---|
| 2026-11-13 | Register created | Initial 16 risks scored | 2026-12-14 (G0) |
|  |  |  |  |

**Standing rule:** a risk that materializes is recorded in `planning/decision_record.md` with the date, the trigger, the response, and the effect on the protocol. A risk that is closed is marked closed with evidence, not deleted.
