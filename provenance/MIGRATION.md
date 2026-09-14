# Verified checkpoint-07 import

Status: PASS. This is an import/reproduction record, not a new scientific audit.

The exact uploaded archive is retained in `archives/photonic_single_photon_checkpoint_07.zip`.
Its SHA-256 is `e2bd57686376549342881a5d0348b16820ebbdab094b8d72df05a6836dbad016`. All 39 source members are accounted for
in [IMPORT_MANIFEST.json](IMPORT_MANIFEST.json).

## Changes

Proofs, claim/source ledgers, experimental protocols, mathematical implementation,
reference results, and checkpoint-06 archive remain byte-preserved. The original
README and hash list were relocated to `checkpoint07/` without changing their bytes.
The validator received only an explicit-new-output-directory guard. Everything
from its seeded RNG declaration onward is unchanged. A reader-facing README,
safe reproduction wrapper, integrity checker, engineering tests, documentation,
and work-order rules were added. No substantive scientific claims were changed.

The original ZIP was transported as compressed recursive ZIP metadata/content.
Reconstruction was accepted only after the complete original ZIP hash matched.
Temporary transport parts are not part of the final working tree. The restoration
program remains for provenance and refuses to overwrite an existing import.

## Fresh execution

- Checkpoint 07: 5261 checks, status PASS.
- Maximum algebraic residual: 1.951927459453545e-12.
- Maximum constrained-solver gap: 7.5032757784754267e-12.
- Checkpoint 06: 4453 checks, status PASS, in an isolated temporary copy.
- Engineering regression suite: 12 tests, with log retained in `migration07/unit-tests.log`.

The full fresh checkpoint-07 outputs are under [migration07/run/](migration07/run/).
[REPRODUCTION.json](migration07/run/REPRODUCTION.json) records the environment,
source hashes, per-file comparisons, and both archived and fresh summaries.
Fresh residuals and runtime need not be byte-identical to the archive. Twelve
result tables/JSON files match within the declared absolute tolerance of 1e-8;
all 5,261 check identities/tolerances are unchanged and all fresh residuals pass.
The reference `results/` directory was not regenerated or overwritten.

## Remaining boundaries

No acquired laboratory data, physical calibration, outside peer review, formal
proof verification, or novelty clearance is implied. The next work order is an
independent proof/certificate audit. No license, tag, or public release was selected.
The original relative links inside archived checkpoint documents retain their
historical context; use the current README for navigation.
