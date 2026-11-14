# Checksums and Integrity

## Purpose

The frame, rubric, and pilot table are frozen inputs. Their SHA-256 hashes make
silent edits detectable and let a reader confirm that the manuscript's counts came
from the committed files.

## Covered files

`reproducibility/checksums.sha256` covers:

- `data/citation_frame_2666.csv`
- `data/frame_summary.json`
- `data/cohort_feasibility.csv`
- `data/cohort_feasibility.manifest.json`
- `pilot/pilot_coding_table.csv`
- `pilot/pilot_summary.md`
- `rubric_v1.1.md`
- `PROTOCOL.md`
- `manuscript/abstract.md`
- `manuscript/paper.md`
- `manuscript/references.bib`
- the six Markdown tables in `manuscript/tables/`
- the three figure CSV files in `manuscript/figures/`

The generated `analysis/pilot_results.json` is excluded because it contains a
generation timestamp. The analysis's source hash is recorded inside the JSON and
checked by the tests.

## Verify

```powershell
python scripts/verify_checksums.py
```

Expected output: one `OK` line per covered file and a final count, exit code 0.
Any mismatch prints `FAIL` and exits 1.

## Regenerate

Only regenerate after an intentional, documented change to a frozen input:

```powershell
python scripts/verify_checksums.py --write
```

Regenerating checksums does not make an edit correct. Record the reason in the
commit message and, for a frame change, in `reproducibility/provenance.md`.

## Known hashes

| File | SHA-256 |
|---|---|
| `data/citation_frame_2666.csv` | `6a0a374ba6120b244418e887a76a83d6bfb8a95dd61cfc822cf349ac7043d30c` |
| `data/frame_summary.json` (source frame hash field) | `46a58fe017577d9e15c22e6bef198fdff526b511ff7897519b6a0e91542cdd72` |
| `pilot/pilot_coding_table.csv` | Recorded in `analysis/pilot_results.json` and verified by tests. |
