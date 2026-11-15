# Zenodo deposit — operator checklist

**Status:** published 15 November 2026.
**DOI:** [10.5281/zenodo.24245000](https://doi.org/10.5281/zenodo.24245000)
**Record:** <https://zenodo.org/records/24245000>
**Deposit type:** Publication → Preprint. **Version:** 1.0.

The steps below record how the record was created. Open
<https://zenodo.org/uploads/new> in the browser where you are already
signed in as `P-r-e-m-i-u-m` to create a new version.

Do not sign up through GitHub on that page. On 15 November, the GitHub identity
used in the automation browser was not linked to `P-r-e-m-i-u-m`; Zenodo offered
to create a second account (`aman`). Creating it would have attached the DOI to
the wrong profile.

---

## 1. Files

The record contains six files. Their local copies were verified against these
SHA-256 values before upload:

| File | Bytes | SHA-256 |
|---|---:|---|
| `paper.pdf` | 229,726 | `76923A889BFAB711837B8E3C40ABCDDB8F5EFB5CEDEF7919D45367D045F2C6B6` |
| `paper-source.zip` | 126,890 | `7E1771C36026E871782428233E15A80F00B6985945C5472C25E550508BCF164A` |
| `reproducibility-package.zip` | 164,059 | `719E1D469869D243583FFC4315095B7EAC57ACE21B15B715A507AD96DC89288C` |
| `README.md` | 3,114 | `4F1B48B0775A2C06855F30EE1CC34A58BE50DA42C7A91867F076D96C2AE60551` |
| `LICENSE` | 1,088 | `16F41230C1CBE5E4860E30E103B3DC031421DB14076FC55CF16CD2AB5BC188B3` |
| `LICENSE-DATA` | 2,361 | `F1390988FD7E678FBBE6E52EEF75A40D39073E2F43EFFBD9F2C2586C2AFB899B` |

---

## 2. Basic fields

| Field | Value |
|---|---|
| Resource type | Publication → **Preprint** |
| Title | Does Benchmark Critique Diffuse into Evaluation Practice? A Pilot-Based Study of EvalPlus and SWE-bench+ Adoption |
| Creator | **Syed Abdul Aman** — Independent Researcher |
| Publication date | 2026-11-15 |
| Version | 1.0 |
| Language | English |
| License | **CC BY 4.0** |

Creator notes:

- The account name may auto-fill as `🄂ʏᴇᴅ 🄰ʙᴅᴜʟ 🄰ᴍᴀ🄝 ✧`. Replace it with
  **Syed Abdul Aman** so the record matches the paper and the PDF metadata.
- Do not add a second creator. Do not add an ORCID unless you have a real one.

---

## 3. Description (HTML)

Paste this into the Description field. Zenodo renders the HTML.

```html
<p>This record is a pilot-study preprint together with its LaTeX source and reproducibility materials. It reports a small, purposive study of whether research papers that cite a benchmark critique go on to use the remediation that critique released.</p>

<p>Two remediations are examined. EvalPlus augments HumanEval and MBPP with additional tests; SWE-bench+ releases a filtered 548-instance dataset for SWE-bench. A frozen citation frame of 2,666 title clusters was built from Semantic Scholar records retrieved on 13 November 2026. From that frame, 29 papers were drawn by purposive sampling: 27 full texts were accessible, 12 papers were coded, 8 were eligible for the all-pair set, and 6 for the two primary pairs. Rubric v1.1 distinguishes citation only (0), acknowledgment (1), partial adoption (2), and full adoption (3).</p>

<p>One of the six primary-pair papers fully adopted the remediation (16.7%; Wilson 95% CI 3.0–56.4); the all-pair figure is 1 of 8 (12.5%; 2.2–47.1). Three of six primary-pair papers, and four of eight all-pair papers, remediated independently instead of adopting the critique's artifact. The agreement statistics reported in the paper are LLM–LLM (κ = 0.78 unweighted, 0.86 linear weighted) and are not human inter-rater reliability.</p>

<p><strong>Status.</strong> The paper is a pilot study and a preprint. It has not been peer reviewed and has not been accepted for publication. It does not estimate prevalence in the 2,666-cluster frame, and it does not establish causal diffusion from critique to practice. The full-scale study described in the protocol — a stratified sample of 900 invited papers, human double-coding, and pre-specified sensitivity analyses — was designed but not executed.</p>

<p><strong>Contents.</strong> <em>paper.pdf</em> (20 pages, A4); <em>paper-source.zip</em> (XeLaTeX source, vector figures and figure data, abstract, reference metadata); <em>reproducibility-package.zip</em> (coding rubric, pilot coding table, analysis scripts and tests, generated tables, protocol, provenance and licensing notes, aggregate frame summary); <em>README.md</em>; <em>LICENSE</em>; <em>LICENSE-DATA</em>.</p>

<p><strong>Licensing.</strong> The paper, documentation, rubric, and derived data are released under CC BY 4.0. Original code is released under the MIT license. The frozen citation frame and the arXiv metadata export are not redistributed here because they derive from Semantic Scholar records; aggregate counts and SHA-256 hashes are included, and the frame itself is available in the repository under Semantic Scholar's terms.</p>

<p><strong>Links.</strong> Repository: <a href="https://github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol">github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol</a>. Research website: <a href="https://p-r-e-m-i-u-m.github.io/benchmark-critique-diffusion-protocol/">p-r-e-m-i-u-m.github.io/benchmark-critique-diffusion-protocol</a>.</p>
```

---

## 4. Keywords

```
benchmark evaluation; benchmark critique; EvalPlus; SWE-bench+; citation diffusion; meta-research; reproducibility; code generation
```

---

## 5. Notes

```
Preprint. Not peer reviewed. No journal has accepted this manuscript.

The registration-status section of the paper was drafted before this deposit and refers to a planned OSF registration. No OSF registration was created. The DOI assigned to this record is a Zenodo DOI, not an OSF DOI.

The deposited PDF is the version described in the paper. Its SHA-256 is 76923A889BFAB711837B8E3C40ABCDDB8F5EFB5CEDEF7919D45367D045F2C6B6.
```

This note exists because §10.6 of the paper still mentions OSF. It prevents a
reader from mistaking the Zenodo DOI for an OSF registration DOI.

---

## 6. Related identifiers

Add both under **Related works**:

| Relation | Identifier | Scheme |
|---|---|---|
| is supplemented by | `https://github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol` | URL |
| is documented by | `https://p-r-e-m-i-u-m.github.io/benchmark-critique-diffusion-protocol/` | URL |

---

## 7. Publish

1. Check the preview: 20 pages, title and author correct, six files listed.
2. Click **Publish**.
3. Copy the **DOI** and the record URL.

---

## 8. After publishing

The DOI and record URL are recorded at the top of this file. The deposit was
verified after publication: the six files match the local SHA-256 values in §1,
and the re-downloaded `paper.pdf` hashes to
`76923A889BFAB711837B8E3C40ABCDDB8F5EFB5CEDEF7919D45367D045F2C6B6`
(229,726 bytes, 20 A4 pages).

Repository updates completed:

1. `README.md` — DOI in the header and citation block.
2. `docs/cite.bib` — `doi`, `publisher`, and `version` fields.
3. `docs/index.html` — DOI link, structured metadata, and citation.
4. `manuscript/submission/submission_checklist.md` — DOI recorded as obtained.
5. Test suite and checksum verifier re-run; DOI resolver and Zenodo API record
   confirmed.
