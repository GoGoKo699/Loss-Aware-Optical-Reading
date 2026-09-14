# Reproduction and evidence

Use Python 3.13.5. `requirements-test.txt` includes the recorded NumPy 2.3.5,
SciPy 1.17.0 and test-only mpmath 1.3.0. No dependency version is changed by the
claims integration. No GPU or laboratory connection is required. This is not a
complete OS/container lock.

```bash
python -m pip install -r requirements-test.txt
python scripts/verify_import.py
python -m unittest discover -s tests -v
python scripts/reproduce.py --output results/runs/my-first-run
python repairs/theory-01/verify.py --output results/runs/my-repair-check
python audits/novelty-01/comparison_checks.py --source-root . --output results/runs/my-source-comparison
```

Every output directory must be new. The reproduction wrapper checks protected
hashes before and after execution and records logs, source hashes, environment,
commit when available, and the frozen-reference comparison. Direct use of
`src/validate.py` requires `--output-dir` and omits that comparison.

## Different checks answer different questions

The 5,261 inherited checks keep their names, order and tolerances. Twelve generated
CSV/JSON files are compared at the unchanged absolute tolerance 1e-8, with exact
schema and nonnumeric data. The repair's two declared method-metadata changes
remain explicit; archived summaries are not rewritten.

The original 12 engineering tests and 16 repair groups remain unchanged. The
repair groups include exact support endpoints, an independent 120-digit equation,
135 enclosure cases, accepted-domain tests and caller/tamper regressions.
The repair runner executes the historical 998-check audit on historical source,
then its 993 scientific cases on repaired source. Its five defect/hash assertions
belong to historical source, not the repaired implementation. Derived floating
budget suffixes can change at rounding scale; case order and tolerances remain.

The added claims-integration tests check the documentation hash chain, unchanged
canonical mathematics and acquisition protocol, preserved novelty audit, report
math expressions, lab questions and local reading links. They also execute the
631 predecessor-translation checks in a new temporary directory and compare case
identities, tolerances and example values with the archived comparison. Original
scientific tests are not replaced. This means normal CI now executes the focused
comparison, rather than only checking that its script exists.

Passing translations is not evidence of originality. Passing mathematics is not
laboratory calibration. Only the photon-support bounds and documented perturbation
addition have exact-rational/outward guarantees; nominal rates and the complete
classical/statistical pipeline are not interval certified.
[Numerical contract](NUMERICAL_CONTRACT.md).

## Frozen and fresh content

The original checkpoint ZIP, `provenance/IMPORT_MANIFEST.json`, `baseline/`,
frozen `results/`, earlier audits and repair evidence remain byte-preserved.
The existing `theory-repair-01.json` ledger is also unchanged. A separate
[documentation ledger](../provenance/changes/claims-integration-01.json) records
post-repair old/new hashes for four documents and hashes for two added notes.
The verifier checks each transition without resetting an old hash. That ledger
cannot authorize changes to numerical modules or acquisition settings.

Fresh outputs belong under ignored `results/runs/`. Preserve reviewed runs with
their scope and provenance, not by overwriting reference files. The
[integration record](../integrations/claims-01/REPORT.md) distinguishes local
archive-based checks from full remote-checkout CI. The novelty audit's historical
execution record is not rewritten to claim later remote runs.

## Future experimental records

Use `src/analyze_trials.py` only with a genuinely preregistered plan and externally
justified calibration, illumination and source-tail bounds. All attempted trials
stay in the record. Templates remain synthetic, including with `--allow-synthetic`.
A plan field cannot establish that calibration, blinding or source assumptions
are true. Do not stop a fixed-budget test at the first apparent violation.

Use fresh analysis filenames and preserve raw records independently. Hypothetical
forecasts, rounded synthetic counts and acquired data must remain separate.
