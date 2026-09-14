# Theory audit 01: bounded repair

**F01-F03 are corrected. The planned lambda=5 experiment and the analytic physical
model are unchanged. The photon-support implementation now separates a nominal
recipe from an outward-safe upper bound and rejects unsupported numerical inputs.**

Main input: `d07e4e2180992ab52ee08d0a0cad689154d2e9bd`.
Audit input: `10410caf761ad858236d22c4a2f5d9a53bc94dff`.
Repair branch: `repair/theory-01`. The branch includes the original audit without
editing it. Integration and final CI commit identities are recorded in the repair
pull request, rather than self-referencing a commit that contains this report.

## Fixes

| Finding | Correction | Effect on the existing experimental predictions |
|---|---|---|
| F01 | The score is bounded by the minimum of 1 and the uncapped expression, not a false chained inequality. | The classical code already had the cap; no change to P1. |
| F02 | Exact-rational secular signs enclose the optimum; stable 90-digit nominal rates avoid survival-minus-correct subtraction; reverse certification uses the upper endpoint. | Planned results agree with frozen outputs within the unchanged 1e-8 regression tolerance. |
| F03 | The code specifies nonnegative Glauber-Sudarshan coherent-state mixtures, not the doubled positive-P representation. | Terminology only; no weaker classical comparator. |

## The reported high-penalty failure is removed

For eta=(0.2,0.4,0.8,0.9) and lambda=1e15:

| Quantity | Value |
|---|---:|
| Reproduced historical score | 0.35012265158564393 |
| Repaired nominal support | 0.40563380281690165 |
| Lower binary64 support endpoint | 0.4056338028169016 |
| Upper binary64 support endpoint | 0.40563380281690165 |

The independently computed support for the exact binary64 inputs begins
`0.4056338028169015920211113999996831587144403210798074052444`.
The decimal display of an endpoint is not an exact decimal input: endpoints
represent binary64 numbers. Exact rational sign checks establish enclosure.

This is not a floor at a feasible harmonic-mean score. A monotone secular equation
brackets the true finite-penalty optimum, and all endpoint signs are evaluated with
integer rational arithmetic. The nominal recipe and the upper bound are distinct
outputs. The reverse-certificate caller uses the latter and outward-rounds the
existing perturbation allowance.

The accepted implementation domain is 2..64 modes, transmissions in [1e-12,1],
and penalties in [0,1e18]. Invalid inputs raise an explicit exception; frontier
points requiring a larger finite penalty are rejected. The zero-error endpoint
remains available. These are implementation boundaries, not new restrictions on
the mathematical theorem or experimental specifications.

See [NUMERICAL_PROOF.md](NUMERICAL_PROOF.md) for the enclosure argument and
[the output contract](../../docs/NUMERICAL_CONTRACT.md) for the remaining numerical
qualifications. In particular, nominal rates and physical calibration are not
interval-certified by this repair. Neither are all classical/statistical routines.

## Executed local checks

The local environment is Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, mpmath 1.3.0.
Local evidence is preserved in the downloadable repair packet. `LOCAL_SUMMARY.json`
and `HIGH_PENALTY.json` expose the local results. The branch-restricted integration
job additionally records a fresh remote run in `REMOTE_EVIDENCE.tar.xz`, with member
hashes and a separate `REMOTE_SUMMARY.json`. Local and remote runs are not conflated.

| Check | Result |
|---|---|
| Original engineering suite | 12/12 passed, byte-identical test file |
| New repair unit groups | 16/16 passed, including 135 enclosure instances, independent 120-digit roots, domain/caller/tamper tests |
| Inherited validator on repaired source | 5,261 checks passed with the same ordered names and tolerances |
| Fresh tables versus frozen outputs | Passed; largest numeric difference 6.823e-12, below unchanged 1e-8 tolerance |
| Historical audit on historical source | 998 checks passed with its original reproduced-findings status |
| Original independent scientific cases on repaired source | All 993 passed; same case order and tolerances |
| Original ZIP, import manifest, baseline evidence, and audit bytes | Unchanged |

The largest independent scientific residual is 1.1606256511420554e-8, its original
full-Hermitian numerical-dual gap, below the unchanged 3e-6 diagnostic tolerance.
The inherited repaired run's largest algebraic residual is about 1.005e-12 and
its maximum constrained-solver gap about 7.260e-12. These numerical diagnostics
do not replace the exact enclosure argument or the analytic quantum/optical proofs.

A second repaired-audit run reproduced SCIENTIFIC_CHECKS.json,
SCIENTIFIC_DIAGNOSTICS.json, and HIGH_PENALTY.json byte for byte.

A preliminary repaired-audit wrapper stopped because 74 historical check names
embed a derived frontier budget that changed at rounding scale. No scientific
residual failed. The wrapper now compares the unchanged case identity/order and
tolerance, records both versions of the derived numeric suffix, and retains all
993 scientific checks. The unchanged historical audit's five other checks are
two assertions that the historical defects exist and three original source hashes;
those still run on the original source, not on the repaired code. The preliminary
log is preserved. No original audit test or tolerance was changed.

## Source and regression preservation

The original `provenance/IMPORT_MANIFEST.json` and checkpoint ZIP are unchanged.
A separate [old/new hash ledger](../../provenance/changes/theory-repair-01.json)
records four approved canonical changes and protects three added numerical files.
The verifier checks the original manifest's Git blob identity, every original
source member, the complete one-to-one inventory, each approved previous hash,
and each current hash. It rejects unlisted changes and path traversal.

The inherited validator's mathematical checks are unchanged. Only two method
metadata fields now disclose the new exact-rational photon-support enclosures.
The reproduction wrapper checks those two explicit old/new values and preserves
all original check names, tolerances, output inventories, and comparison limits.
Frozen outputs and the historical audit remain available to reproduce the defects.

The repaired runtime needs no new third-party arithmetic package. mpmath is an
independent test dependency in `requirements-test.txt`, not a production dependency.
CI is configured to repeat the full regression, historical audit, and repaired
scientific cases on a clean actual checkout. CI success is attached to its exact
commit and must be inspected before merge and again on main.

## Access and integration method

Container DNS could not resolve github.com; no local authenticated Git clone is
claimed. The local snapshot was reconstructed from the uploaded source ZIP and
audit ZIP. Canonical source, validator guard, original import manifest, original
reproduction scripts, and original engineering tests were matched to remote Git
blob identities. Repository state and branch ancestry were read through the
GitHub connector.

The proposed patch is transported as a hash-checked source bundle. A temporary,
branch-restricted Actions job checks every old Git blob before applying it, runs
the complete checks, commits only the declared changed paths, and pushes only to
the repair branch without force. It removes its one-time workflow in that commit.
The normal read-only workflow then verifies the final PR and merged main. This
avoids claiming that an uploaded bundle alone is an integrated code change.

## Remaining boundaries and next work

No new scientific task, source class, prior, photon budget, phase-reference
assumption, trial protocol, or hardware capability is introduced. No laboratory
data, measured advantage, outside peer review, novelty clearance, license, release,
or privacy change is part of this work.

The next scientific task is a bounded theorem-level prior-art comparison. Source
and channel calibration plus laboratory-interface review remain separate. The
repair does not justify calling the entire software stack formally or interval
verified, and it does not remove statistical or physical assumptions.
