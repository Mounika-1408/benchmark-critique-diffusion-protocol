# Environment

## Tested environment

| Component | Version |
|---|---|
| Operating system | Windows (win32) |
| Python | 3.13.14 |
| Git | 2.53.0.windows.3 |
| GitHub CLI | 2.93.0 |
| pytest | Installed in the test environment; tests use only the standard library plus pytest |

The analysis scripts target Python 3.11+ and use only the standard library. The
pilot was executed and verified on Python 3.13.14. No network access is required
for frame verification, pilot analysis, table generation, figure generation, or
tests.

## Dependencies

### Required for the public verification path

- Python 3.11+
- pytest (tests only)

### Not required

- pandas
- NumPy
- SciPy
- statsmodels
- matplotlib
- seaborn

Figures are written as dependency-free SVG. The full study may optionally use
pandas, NumPy, SciPy, and statsmodels; those dependencies are not needed to
reproduce the pilot.

## Determinism

- The frame is frozen; no retrieval is performed by verification scripts.
- Pilot analysis reads a fixed CSV and computes deterministic counts, Wilson
  intervals, and exact-binomial probabilities.
- Tables and figures are generated from fixed CSVs.
- The analysis JSON includes a generation timestamp, so its own hash is not part
  of the frozen-input checksum list.

## Commands

```powershell
python --version
python -m pytest tests -q
python scripts/verify_checksums.py
```

If `pytest` is missing:

```powershell
python -m pip install pytest
```
