# Feasibility and Workload

**Prepared:** 13 November 2026  
**Frame:** 2,666 title clusters (2,531 EvalPlus-only + 135 SWE-bench+ census)  
**Purpose:** Recalculate the sample-size, precision, and workload numbers from the frozen frame and state the assumptions explicitly. This file replaces earlier rough estimates.

---

## 1. What is fixed

| Quantity | Value | Source |
|---|---:|---|
| Analysis frame | 2,666 title clusters | `data/citation_frame_2666.csv` |
| SWE-bench+ stratum | 135 | Census (112 SWE-only + 23 both) |
| EvalPlus-only stratum | 2,531 | 2,666 − 135 |
| Raw citation rows | 2,708 | 2,572 EvalPlus + 136 SWE-bench+ |
| Identifier-deduplicated union | 2,684 | Before title clustering |
| Title duplicates removed | 18 rows in 14 groups | 2,684 → 2,666 |
| DOI coverage | 2,313 / 2,666 (86.8%) | CSV |
| arXiv coverage | 2,028 / 2,666 (76.1%) | CSV |
| DBLP coverage | 2,129 / 2,666 (79.9%) | CSV |
| No DOI/arXiv/DBLP | 42 / 2,666 (1.6%) | CSV |
| No publication date | 225 / 2,666 (8.4%) | CSV |
| Date after 2026-09-30 | 231 / 2,666 (8.7%) | CSV |

**Frame years:** 2022: 2; 2023: 119; 2024: 526; 2025: 838; 2026: 1,139; unknown: 42.

These are verified counts, not estimates. The year distribution shows that 42.7% of the frame is dated 2026, which is why year-based analyses are descriptive and why the frame is frozen.

---

## 2. Planning value for full adoption

The pilot produced two estimates:

| Pilot set | Full adoption | Wilson 95% CI |
|---|---:|---|
| Primary pairs only (EvalPlus + SWE-bench+) | 1/6 = 16.7% | 3.0–56.4% |
| All pairs (adds GSM1k secondary) | 1/8 = 12.5% | 2.2–47.1% |

The main study uses **p = 0.125** for precision calculations. Reasons:

1. n = 6 is too small to prefer 16.7% over 12.5%; the primary-pair interval includes both.
2. 12.5% is the more conservative value for precision: a rarer outcome needs a larger n for the same absolute half-width.
3. The all-pair estimate is not the primary estimand, but it is a reasonable planning prior and avoids anchoring on the single `whatswrong` case.

**This is a planning value, not a prediction.** The main study will estimate the parameter; it does not assume 12.5% is true.

---

## 3. Scenario table

Assumptions per row: 10 min retrieval per invited record; 20 min eligibility screen per accessible record; 30 min coding per eligible paper; 20% double-coded with 15 min reconciliation per double-coded paper; 80 h analysis, 140 h writing, 40 h admin; 15% buffer. “Adopters” is rounded from 12.5% of eligible; Wilson 95% CI is computed at the rounded counts.

| Scenario | Invited | Access | Eligibility | Accessible | Eligible | Adopters | Prevalence | Wilson 95% CI | Half-width | Total hours | h/wk (52) | h/wk (39) |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|
| Conservative, 900 | 900 | 70% | 10% | 630 | 63 | 8 | 12.7% | 6.6–23.1% | ±8.3 pp | 752.8 | 14.5 | 19.3 |
| **Base, 900** | **900** | **80%** | **18%** | **720** | **130** | **16** | **12.3%** | **7.7–19.1%** | **±5.7 pp** | **829.7** | **16.0** | **21.3** |
| Optimistic, 900 | 900 | 93.1% | 25% | 838 | 210 | 26 | 12.4% | 8.6–17.5% | ±4.5 pp | 925.6 | 17.8 | 23.7 |
| Reduced, 560 (9-month) | 560 | 80% | 18% | 448 | 81 | 10 | 12.3% | 6.8–21.3% | ±7.2 pp | 629.3 | 12.1 | 16.1 |
| Cap, conservative | 1,200 | 70% | 10% | 840 | 84 | 10 | 11.9% | 6.6–20.5% | ±7.0 pp | 904.1 | 17.4 | 23.2 |
| Cap, base | 1,200 | 80% | 18% | 960 | 173 | 22 | 12.7% | 8.5–18.5% | ±5.0 pp | 1,006.4 | 19.4 | 25.8 |

**Reading the table**

- The **base** row is the design target: 900 invited, 130 eligible, ±5.7 pp, 16.0 h/week over 52 weeks.
- The **conservative** row is the worst realistic case at 900 invited: 63 eligible, ±8.3 pp, 14.5 h/week. It is still reportable, but the paper must state the wider interval.
- The **optimistic** row is not a promise. A 93.1% access rate and 25% eligibility are the pilot’s best-case values, not general-frame estimates.
- The **reduced** row is the 9-month option: 560 invited, 81 eligible, ±7.2 pp, 16.1 h/week over 39 weeks.
- The **cap** rows show what happens if eligibility is low and the stop rule adds blocks to 1,200. At the base eligibility rate, the cap raises precision only modestly (±5.0 pp) while raising effort to 19.4 h/week. At the conservative rate, the cap yields 84 eligible and ±7.0 pp at 17.4 h/week.

**Important:** the “h/wk (39)” column for the 900-invited rows is not the recommended plan; it shows that compressing the 900 design into 9 months requires 21.3 h/week. The 9-month option is only feasible with the reduced 560 design.

---

## 4. Precision and power

### 4.1 H1: full adoption < 25%

One-sided exact binomial test against p0 = 0.25. At true p = 0.125, the rejection region and power are:

| Eligible n | Critical count (reject if ≤) | Actual α | Power at p = 0.125 |
|---:|---:|---:|---:|
| 63 | 9 | 0.029 | 0.742 |
| 81 | 13 | 0.037 | 0.870 |
| 120 | 21 | 0.033 | 0.958 |
| 130 | 24 | 0.049 | 0.982 |
| 173 | 33 | 0.041 | 0.995 |
| 210 | 41 | 0.037 | 0.999 |

**Interpretation:** the base design (130 eligible) has high power for H1 if the true rate is near 12.5%. The conservative design (63 eligible) has only 74% power; a non-significant result there would be uninformative, which is why the paper should lead with the prevalence estimate and CI, not the p-value.

### 4.2 H3: most eligible papers are 0/1

One-sided exact binomial test against p0 = 0.50. At true 0/1 proportions of 0.60–0.70, power at n = 130 is approximately:

| True 0/1 proportion | Power at n = 130 |
|---:|---:|
| 0.55 | 0.30 |
| 0.60 | 0.74 |
| 0.65 | 0.97 |
| 0.70 | 1.00 |

The pilot’s 0/1 proportion was 5/6 = 83.3% (primary pairs) and 7/8 = 87.5% (all pairs). If the main study is anywhere near that, H3 is well powered. If the true value is 0.55, it is underpowered; the paper must report the CI and not treat a null result as evidence that most papers adopt.

### 4.3 H2: EvalPlus vs SWE-bench+

Expected eligible counts at the base assumptions:

- EvalPlus-only: 765 × 0.80 × 0.18 ≈ **110** eligible.
- SWE-bench+ census: 135 × 0.80 × 0.18 ≈ **19** eligible.
- Total ≈ **129** (the aggregate 130 in the base row uses 900 × 0.80 × 0.18 = 129.6, rounded).

At p = 12.5%, the expected adopters are 14/110 and 2/19. Wilson 95% CIs are approximately:

| Stratum | Expected adopters / eligible | Prevalence | Wilson 95% CI | Half-width |
|---|---:|---:|---|---:|
| EvalPlus-only | 14 / 110 | 12.7% | 7.7–20.2% | ±6.3 pp |
| SWE-bench+ | 2 / 19 | 10.5% | 2.9–31.4% | ±14.2 pp |

The SWE-bench+ interval is roughly twice as wide. A Fisher exact test at these counts has low power for any plausible difference. **H2 is exploratory and the protocol says so.** The study can describe a contrast; it cannot confirm one.

### 4.4 What precision is achievable

At 130 eligible and p ≈ 12.5%, the Wilson half-width is ±5.7 pp. This distinguishes “rare” (e.g., <10%) from “common” (e.g., >20%) but not 10% from 15%. That is the right resolution for a first prevalence estimate. A census would not dramatically improve it: even 300 eligible gives ±3.8 pp, at roughly 2.3× the coding workload.

---

## 5. Chosen design

**900 invited = 135 SWE-bench+ census + 765 EvalPlus-only random sample.**

- The SWE-bench+ stratum is small enough to census; this avoids sampling error in the descriptive contrast and guarantees coverage of the 23 both-critique papers.
- The EvalPlus-only sample is 765 / 2,531 = 30.2% of that stratum, drawn with proportional allocation by year (2022 collapsed into 2023; minimum 10 per stratum where possible) and a fixed seed.
- Target: 120 eligible. Base expectation: 130. Hard cap: 1,200 invited.
- Stop rule: after 900 invited, if fewer than 120 eligible, add blocks of 100 EvalPlus-only records up to 1,200. Stop as soon as 120 is reached. If 1,200 is reached with fewer than 120, report the realized count and do not extend without a protocol amendment.

**Why 120?** At p = 12.5%, 120 eligible gives ±5.9 pp; 130 gives ±5.7 pp. The difference is trivial. The target is a round operational threshold, not a power calculation. The stop rule prevents endless extension.

**Why not a census?** 2,666 full texts at 10 min retrieval + 20 min screening per accessible paper is roughly 1,100–1,300 hours before coding and writing. That is 21–25 h/week for a year, with no reliability or analysis time. The sample is the defensible compromise.

---

## 6. Workload

### 6.1 Base case (900 invited, 720 accessible, 130 eligible)

| Task | Assumption | Hours |
|---|---|---:|
| Full-text acquisition | 900 × 10 min | 150.0 |
| Eligibility screening | 720 × 20 min | 240.0 |
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

### 6.2 Reduced 9-month case (560 invited, 448 accessible, 81 eligible)

| Task | Assumption | Hours |
|---|---|---:|
| Full-text acquisition | 560 × 10 min | 93.3 |
| Eligibility screening | 448 × 20 min | 149.3 |
| Ordinal coding + evidence | 81 × 30 min | 40.5 |
| Reconciliation | 16 double-coded × 15 min | 4.0 |
| Analysis + robustness | fixed | 80.0 |
| Writing/editing | fixed | 140.0 |
| Admin, OSF, ethics, data | fixed | 40.0 |
| **Subtotal** | | **547.2** |
| 15% buffer | | **82.1** |
| **Total** | | **629.3** |
| 9 months (39 weeks) | | **16.1 h/week** |

### 6.3 Cap case (1,200 invited, 960 accessible, 173 eligible)

| Task | Assumption | Hours |
|---|---|---:|
| Full-text acquisition | 1,200 × 10 min | 200.0 |
| Eligibility screening | 960 × 20 min | 320.0 |
| Ordinal coding + evidence | 173 × 30 min | 86.5 |
| Reconciliation | 35 double-coded × 15 min | 8.7 |
| Analysis + robustness | fixed | 80.0 |
| Writing/editing | fixed | 140.0 |
| Admin, OSF, ethics, data | fixed | 40.0 |
| **Subtotal** | | **875.1** |
| 15% buffer | | **131.3** |
| **Total** | | **1,006.4** |
| 12 months (52 weeks) | | **19.4 h/week** |

**The cap case is the real workload risk.** If eligibility is low and the stop rule runs to 1,200, the project needs ~19.4 h/week, not 16.0. The researcher should decide in advance whether that is protected time or whether to stop at 900 and report the realized precision. The protocol permits stopping at 900 with fewer than 120 eligible, provided the shortfall is reported and the analysis is honest about the wider CI.

### 6.4 Second coder

| Case | Double-coded | Coding (45 min each) | Calibration | Adjudication | Total |
|---|---:|---:|---:|---:|---:|
| Base (130 eligible) | 26 | 19.5 h | 6 h | 6 h | **31.5 h** |
| Reduced (81 eligible) | 16 | 12.0 h | 6 h | 4 h | **22.0 h** |
| Cap (173 eligible) | 35 | 26.3 h | 6 h | 6 h | **38.3 h** |

The second coder’s work is concentrated in calibration (month 1) and the reliability window (months 5–6), not spread evenly. The commitment must be scheduled, not assumed.

**Reliability sample note:** the base design double-codes 26 papers (20% of 130). The reduced design double-codes 16 (20% of 81). The rubric’s earlier “minimum 20” wording conflicted with the 16-paper reduced option; the operative rule is 20% of eligible papers, with 16 as the floor for the reduced design and 26 preferred for the base design.

---

## 7. 12-month vs 9-month

| Dimension | 12-month base | 9-month reduced |
|---|---|---|
| Invited | 900 | 560 |
| Eligible (expected) | 130 | 81 |
| Precision at 12.5% | ±5.7 pp | ±7.2 pp |
| Total hours | 829.7 | 629.3 |
| Weekly hours | 16.0 | 16.1 |
| Second coder | 31.5 h | 22.0 h |
| Buffer | 10 weeks after submission | 5 weeks after submission |
| Risk | Access delays, slow review | Less room for access delays or desk rejection |

**Recommendation: 12 months.** The weekly effort is essentially identical (16.0 vs 16.1 h/week), but the 12-month design has more eligible papers, better precision, a larger reliability sample, and a real buffer. The 9-month option is a fallback for a hard external deadline, not the preferred plan.

**Caveat:** 16 h/week for 52 weeks is a sustained commitment. If the researcher cannot protect it, the honest options are (a) the 9-month reduced design at the same weekly effort, or (b) extend the 12-month design to 15–18 months at a lower weekly rate. Do not plan 16 h/week and then discover in month 4 that only 8 h/week are available.

---

## 8. Budget

| Item | Cost | Note |
|---|---:|---|
| Submission fees | $0 | EMSE subscription route; DMLR no fees. |
| OSF | $0 | Free registries. |
| Software | $0 | Python, pandas, statsmodels, scipy, matplotlib. |
| Second coder | $0–1,575 | Unpaid collaborator preferred; if paid at $30–50/h × 31.5 h. |
| ILL/document delivery | Institutional | Check quota; may be free or per-item. |
| Open Choice APC (EMSE) | Optional | Amount quoted at acceptance; not required for subscription route. |
| QSS APC | Unresolved | Do not budget until confirmed; not a primary venue. |
| Travel/conference | Optional | Not required for publication. |

**Cash requirement: $0** if the second coder is an unpaid collaborator and institutional access/ILL is available. That is the base assumption. If either fails, the budget changes; see `planning/risk_register.md`.

---

## 9. Assumptions that could be wrong

| Assumption | Value used | Evidence | If wrong |
|---|---:|---|---|
| Access rate | 80% | Pilot 93.1% (purposive); general frame unknown | 70% at 18% eligibility → 113 eligible, ±6.1 pp; 50% at 18% → 81 eligible, ±7.2 pp; at 50% access and 10% eligibility → 45 eligible, ±10.0 pp. Consider open-access restriction. |
| Eligibility rate among accessible | 18% | **Planning assumption, not measured** | 10% at 80% access → 72 eligible, ±7.7 pp; 25% at 80% access → 180 eligible, ±4.8 pp. The first block gives an early observed rate; the stop rule handles the low end. |
| Retrieval time | 10 min/record | Pilot did not time precisely | 15 min → +75 h at 900; 20 min → +150 h. |
| Screening time | 20 min/record | Pilot estimate | 30 min → +120 h at 720. |
| Coding time | 30 min/eligible | Pilot estimate | 45 min → +32.5 h at 130. |
| Double-coding rate | 20% | Protocol | 25% → +6.5 h reconciliation and +6.5 h coder time at 130. |
| Buffer | 15% | Judgment | 25% → +72 h; weekly hours rise to 17.3. |
| No-shows / withdrawals | 0% | Not yet known | Even 10% attrition raises invited needed by ~11%; the cap absorbs some of this. |

**The two assumptions that matter most are access and eligibility.** Both are measured in the first 4–6 weeks of retrieval. The protocol should not pretend they are known now.

---

## 10. Feasibility verdict

**Feasible at 16 h/week for 12 months under the base assumptions, conditional on Gate 0.** The frame is built, the rubric is specified, the pilot shows the coding task is tractable, and the workload is comparable to a part-time research project. The main risks are external (second coder, access) and empirical (eligibility rate), not scientific.

**Not feasible as a solo census.** A full 2,666-paper retrieval and screen would require roughly 1,100–1,300 hours before coding, which is not compatible with a 12-month part-time project. The sample is necessary, not a shortcut.

**Not recommended at 9 months with 900 invited.** That combination requires 21.3 h/week. The 9-month option is only coherent with the reduced 560 design.

**Decision dependency:** if C1–C3 are not met by 2026-12-14, the project remains **NEEDS EXTERNAL INPUT**; the workload analysis does not change that. See `planning/decision_record.md`.
