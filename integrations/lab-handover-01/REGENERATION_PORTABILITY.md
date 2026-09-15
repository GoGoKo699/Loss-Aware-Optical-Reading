# Regenerated witnesses and numerical backend portability

This completes the investigation recorded in [CI_DIAGNOSTICS.md](CI_DIAGNOSTICS.md).
That earlier document and its logs remain an unchanged account of the first
diagnostic stage. Its then-unidentified failure has now been reproduced with
an explicit numerical backend selection.

Both workflows on head `3e51f7da0fe1a5508814419bcd3a3d5aef936a02` failed
the fresh-byte equality assertion again:
[push 34937756547](https://github.com/GoGoKo699/Loss-Aware-Optical-Reading/actions/runs/34937756547)
and [PR 34937759633](https://github.com/GoGoKo699/Loss-Aware-Optical-Reading/actions/runs/34937759633).
The improved diagnostics established that the changed fresh witnesses passed
the unchanged exact verifier's 11,161 checks before the byte-hash assertion
failed. The [decoded PR log](REGENERATED_WITNESS_DIAGNOSIS.log) is preserved.

## Controlled reproduction

The unchanged study was run in a fresh directory with only
`OPENBLAS_CORETYPE=Haswell`, `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`
specified. The local default BLAS kernel is SkylakeX. The Haswell run reproduced
the differing CI hash exactly:

| Regeneration | RESULTS.json SHA-256 |
|---|---|
| Supplied result and local default kernel | `74c0b5ca9f114be36501426f28dc012fcfdb6b872ed6bb8533d463b6cddd14db` |
| Explicit Haswell kernel and differing CI result | `29287b9d89188fa2a4abf7fd4769a35f6e0a7b8ab17ae58a808be12db890396b` |

All 41 exact models, their order, and the complete 381-diagnostic ledger are
identical. The 2,491 differing leaves include proposed eigenvectors, measurement
factors, dual witnesses, degenerate policies, derived bounds and solver details.
The Haswell witnesses independently passed all 11,161 unchanged verifier checks,
including 10,828 exact positive-matrix checks and zero optimizer calls.

Different feasible joint receivers also have different C/E/F rates, by up to
about `9.80e-06`, while retaining compatible tightly enclosed C−5E optima.
Each witness must satisfy its own exact feasibility and payoff checks; equal
optimal score does not require identical measurement factors or outcome rates.
The separate direct optical checks and their original tolerances remain intact.

Its maximum marked-phase joint interval width is
`2.1641344161160703e-08`, retaining the reported three-significant-figure
precision `2.16e-08`. The supplied maximum
`2.16040407785556e-08` remains the precise historical result; it was not refreshed.
See [BACKEND_PORTABILITY.json](BACKEND_PORTABILITY.json) and the complete fresh
[result, environment and verification evidence](BACKEND_PORTABILITY_EVIDENCE.tar.xz).

Selecting the numerical kernel is sufficient to reproduce this difference.
The GitHub logs did not record their runtime kernel, so a particular runner CPU
is not inferred. This is computational reproducibility evidence, not an optical
robustness model, physical calibration, or a new scientific contribution.

## Correct integration contract

The supplied study and all its numerical assertions and tolerances are unchanged.
Original ZIP, patch, study-file, archive-member and frozen-result hashes remain
mandatory. Regeneration may propose a different valid witness for the same
problem; universal byte identity of an optimizer proposal was an overly strong
new integration assertion.

The corrected new integration test compares exact model and check inventories,
verifies both supplied and fresh witnesses with the unchanged rational checker,
and checks compatible certified intervals, reported precision and scientific
claim boundaries. It records fresh hashes instead of accepting a second
hardcoded hash. Invalid witnesses, changed models and incompatible bounds still
fail. The correction is confined to the new integration test; no canonical
scientific routine, original test, theorem, source class or frozen evidence is
changed. Final branch and post-merge workflows are checked separately.

[PORTABILITY_ASSERTIONS.json](PORTABILITY_ASSERTIONS.json) records the old/new
test hashes and assertion mapping. All five focused tests pass, including
changed-model, incompatible-bound, lost-claim and invalid-factor rejection.
An exactly equivalent nonzero factor-column sign change passes the unchanged
verifier. Both full backend results pass the comparison. The
[development and final test logs](PORTABILITY_TEST_LOGS.tar.xz) preserve the
initial zero-column fixture error and its corrected, successful rerun.
The full repository suite now contains 83 tests.
