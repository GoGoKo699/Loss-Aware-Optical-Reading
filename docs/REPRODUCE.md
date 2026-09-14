# Reproduction and evidence

Use Python 3.13.5. `requirements-test.txt` includes the unchanged recorded NumPy
2.3.5/SciPy 1.17.0 environment and test-only mpmath 1.3.0. The new runtime photon
support module itself uses only the standard library. No file is a complete
OS/container lock. No GPU, laboratory connection, or network access is used by
validation after installation.

```bash
python -m pip install -r requirements-test.txt
python scripts/verify_import.py
python -m unittest discover -s tests -v
python scripts/reproduce.py --output results/runs/my-first-run
python repairs/theory-01/verify.py --output results/runs/my-repair-check
```

Every output directory must be new. The reproduction wrapper uses one BLAS/OMP
thread, checks protected hashes before and after execution, and writes the full
run log, environment, source hashes, commit (when a Git checkout exists), and
frozen-reference comparison. `src/validate.py` also requires an explicit new
`--output-dir`; direct use omits the reference comparison, so prefer the wrapper.

## What is checked

All 5,261 inherited check names, their order, and tolerances still match the
original archive. Fresh residuals must be finite, nonnegative, and inside their
original tolerance. Twelve generated CSV/JSON result files are compared at the
unchanged absolute numeric tolerance 1e-8, with exact schema and nonnumeric data.
Only the two explicitly declared method-metadata fields change: the summary now
states that the photon support uses exact-rational enclosures while the other
calculations are not interval certified. No archived summary is rewritten.

The unit suite has the original 12 engineering tests and 16 repair test groups.
The latter include 135 support-enclosure cases with exact endpoint signs and a
separate 120-digit original secular equation, domain boundaries, certificate
caller tests, terminology/cap regressions, and protected-source tamper checks.
Test counts are a regression inventory, not a substitute for the enclosure proof.

The repair runner executes the unchanged 998-check audit against an extracted
historical source, including its historical defect witnesses. It then calls all
993 scientific checks from that same unchanged audit on repaired source. The
remaining five historical checks are two defect assertions and three original
source-hash checks, not scientific cases that should still pass after repairs.
The repair tests separately establish that F01-F03 are fixed. Derived frontier
budgets embedded in 74 test-name suffixes change at rounding scale; the runner
records them and checks the unchanged case order and numeric tolerances. It does
not require those numerical suffixes to be identical.

## Frozen and fresh files

`results/`, `baseline/`, the source archives, the original import manifest, and
`audits/theory-01/` are historical evidence. They remain byte-preserved. A separate
`provenance/changes/theory-repair-01.json` records old/new hashes for the four
approved canonical changes and hashes for three added numerical-support documents
or modules. The integrity checker rejects unknown changes; it never replaces the
original archive hash or refreshes its manifest to bless current bytes.

Fresh runs live under ignored `results/runs/`. The bounded repair evidence is
preserved under `repairs/theory-01/`. CI repeats the unit tests, old regression,
and historical/repaired audit cases on an actual clean Git checkout. The initial
local repair used a verified archive-based snapshot, not an authenticated clone.

## Analyzing future experimental trials

Use `src/analyze_trials.py` only with an approved preregistered plan and externally
justified simultaneous calibration and energy bounds. Every attempted trial stays
in the record. Templates remain synthetic; `--allow-synthetic` does not change
that evidential status. Use a fresh analysis filename and preserve raw records.

The reverse certificate now uses the support upper endpoint, not its nominal
score. This repair does not make every transcendental calculation or the complete
statistical pipeline interval certified. Read [the numerical contract](NUMERICAL_CONTRACT.md).
Calibration, phase-reference isolation, source tails, independent fresh labels,
and absence of optional stopping are still external assumptions, not quantities
a passing numerical test establishes.
