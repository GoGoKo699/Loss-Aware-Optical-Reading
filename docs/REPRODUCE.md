# Reproduction and evidence

Use Python 3.13.5 with `requirements-recorded.txt` for the recorded dependency
versions. `requirements.txt` retains the inherited lower bounds; neither file
is a complete OS/container lock. No GPU, laboratory connection, or network
access is used by the validation code after installation.

```bash
python scripts/verify_import.py
python -m unittest discover -s tests -v
python scripts/reproduce.py --output results/runs/my-first-run
```

The output directory must not already exist. Without `--output`, a UTC timestamp
and random suffix select a fresh directory. The wrapper sets one BLAS/OMP thread,
checks protected hashes before and after execution, captures `run.log`, and writes
`REPRODUCTION.json` with the environment, source hashes, commit, and comparison.

The historical `python src/validate.py` invocation now fails with a request for
an explicit output directory. Its only source change is an I/O guard; the body
from the seeded RNG declaration onward is byte-identical to the archived source.
A direct invocation is possible with `--output-dir` but does not perform the
reference comparison. Prefer the wrapper.

## Comparison policy

All 5,261 check names, their order, and their tolerances must match the archive.
Every new residual must be finite, nonnegative, and within its declared bound.
Twelve generated CSV/JSON files are compared field by field with absolute
numeric tolerance `1e-8`; schema and nonnumeric values must match exactly.
The comparison also records whether files are byte-identical. Environment,
runtime, and summary residual maxima are reported rather than forced to match.
This tolerance is for regression, not an experimental error bar or a proof.

A PASS means this implementation reproduced the checkpoint's checks within that
policy. It is not an independent proof review, novelty clearance, or evidence
from an experiment. The complete per-check ledger remains available in each run.

## Frozen and fresh files

`results/` contains the original checkpoint-07 records. Do not overwrite them.
Fresh runs live under ignored `results/runs/`. To preserve a reviewed new run,
copy it into a clearly named audit directory with its provenance and scope.
The initial repository run is under `provenance/migration07/`.

`provenance/archives/photonic_single_photon_checkpoint_07.zip` is the exact uploaded
archive. `provenance/IMPORT_MANIFEST.json` maps all 39 source members. The original
README and hash list are retained in `provenance/checkpoint07/`; their historical
commands and relative links are not the current entry points. The archive is
self-contained. `baseline/` holds the inherited checkpoint-06 evidence.

## Analyzing future experimental trials

Use `src/analyze_trials.py` only with a genuinely approved plan, separately
justified simultaneous calibration and energy bounds, and every attempted trial.
Templates are synthetic, not calibrated authorizations. `--allow-synthetic`
never changes that evidential status. The analyzer cannot verify the truth of
a declaration of preregistration or hardware calibration. Select a fresh output
filename and preserve raw records and plan versions independently.

No source archives, reference outputs, or experimental records should be deleted
because a newer script produces a different number. Investigate and document it.
