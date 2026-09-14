# Remote import verification

Verified on 2026-09-14. This record closes the earlier uncertainty about whether
checkpoint 07 had reached GitHub. It records repository engineering and regression
checks, not an independent mathematical audit or publication readiness.

## Repository baseline

- Repository: `GoGoKo699/Loss-Aware-Optical-Reading`, private.
- Starting `main`: `4cc807a766218e4037b8983297a69d3277ecdd51`.
- Original archive: `provenance/archives/photonic_single_photon_checkpoint_07.zip`.
- Archive SHA-256: `e2bd57686376549342881a5d0348b16820ebbdab094b8d72df05a6836dbad016`.
- Archive size: 173,345 bytes; 39 source members.
- Completion branch: `maintenance/complete-import-07`.
- Integration record: [pull request 1](https://github.com/GoGoKo699/Loss-Aware-Optical-Reading/pull/1).

Repository reads and writes used the GitHub API. Clean checkout and final working-tree
status were tested by GitHub Actions; no local authenticated clone is implied.
Local source-archive reruns used disposable extracted copies.

## The original remote import succeeded

The [import run 34856086459](https://github.com/GoGoKo699/Loss-Aware-Optical-Reading/actions/runs/34856086459)
and its job `104015895654` completed successfully. The job log was inspected, not
inferred from a configured workflow or a summary file alone. It records:

- restoration of all 39 source members and successful archive/protected-file checks;
- 12 passing engineering regression tests;
- 5,261 passing checkpoint-07 checks and a fresh frozen-reference comparison;
- 4,453 passing checkpoint-06 checks in an isolated extracted copy;
- successful commit and push of the normal repository files to `main`.

The resulting import commit is the starting baseline above. Its evidence remains
under this directory and has not been replaced by later runs.

## Normal development verification succeeded

The [development run 34858504047](https://github.com/GoGoKo699/Loss-Aware-Optical-Reading/actions/runs/34858504047)
at commit `755a655b6676b6996d2d40ce242f507b62ff9434` completed successfully on the
completion branch. It performs a fresh checkout and executes the normal read-only
verification workflow against the completed repository, rather than the bootstrap
staging tree.

The completion patch removes the obsolete bootstrap-message skip. Verification
now also requires an exact one-to-one match between archive members and manifest
entries, rejects duplicate installed paths, checks that the one-time bootstrap
workflow is absent, and checks a clean starting and finishing working tree.
Its job summary identifies the actual verified commit and original archive.

The workflow keeps the pinned environment and action revisions that passed the
import. No dependency upgrade or scientific refactor is part of this change.
Final PR-head and post-merge checks are recorded in pull request 1 and the workflow
history. A successful run applies to its stated commit, not arbitrary later edits.

## Additional supplied-archive rerun

Both supplied archives were independently rerun during completion in disposable
copies. The source ZIP was checked before and after execution and was unchanged.

| Check | Result |
|---|---|
| Checkpoint 07 | 5,261 checks, PASS |
| Same checkpoint-07 ordered check names and tolerances | PASS |
| Checkpoint 06 | 4,453 checks, PASS |
| Original source archive preserved | PASS |

Environment: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0. The local checkpoint-07
maximum algebraic residual was `1.0046144484716451e-12`; its maximum constrained-solver
gap was `4.72527572625836e-12`. Checkpoint 06's maximum algebraic residual was
`2.8816383444526843e-15`; its independent energy-search gap was
`4.12911926872539e-11`. These are floating-point consistency results, not exact
proof certificates or experimental fidelities.

## Change and evidence boundaries

The completion changes affect only the verification workflow, migration records,
and navigation to those records. Canonical proofs, physical assumptions, source
ledgers, mathematical implementations, experiment protocols, source archives,
and frozen reference outputs are unchanged from the verified import.

The original validator's output-directory guard is an existing migration change,
not a new scientific change in this completion. All later reproductions continue
to use new directories through `scripts/reproduce.py`.

No license was selected, no release or tag was created, and privacy was not
changed. There are still no acquired laboratory data, novelty clearance, or
independent proof-audit results. The next bounded scientific work order remains
[the independent proof and certificate audit](../../work_orders/CURRENT.md),
READY and not executed by migration completion.
