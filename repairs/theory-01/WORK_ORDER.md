# Bounded repair of theory audit 01

Status at creation: IN PROGRESS. The user's instruction to proceed authorizes
repairing findings F01-F03, validating the repair, and merging the checked result.
This supersedes the completed audit's no-repair stop condition only for this task.

## Starting records

- Main: `d07e4e2180992ab52ee08d0a0cad689154d2e9bd`.
- Completed audit: `10410caf761ad858236d22c4a2f5d9a53bc94dff`.
- Repair branch: `repair/theory-01`, created from the audit commit so its complete
  evidence is retained unchanged. Do not write to `audit/theory-01`.
- No local authenticated checkout was available: container DNS resolution of
  github.com failed. Local execution uses a new archive-based snapshot whose
  relevant files are checked against remote Git blob identities. Do not call
  this a clean authenticated worktree. CI checks real clean GitHub checkouts.

## Required fixes

F01: replace the false chained score cap by the minimum of the two upper bounds.
F02: separate nominal returned rates from an outward-safe photon support bound;
use stable arithmetic, state the accepted numeric domain, propagate failures to
callers, and test the high-penalty counterexample independently. Do not floor an
unsafe numerical value at a feasible lower bound and call it certified.
F03: replace the ambiguous positive-P docstring with the intended nonnegative
Glauber-Sudarshan coherent-state mixture definition.

## Preservation and tests

Keep the original ZIP archives, original import manifest, all baseline/reference
results, and audit files unchanged. Record every authorized protected-source
change in a separate old/new hash ledger and teach integrity checking to enforce
that ledger without weakening the source archive checks. Keep fresh runs separate.

Rerun the inherited 5,261-check validation and all 12 engineering regressions.
Repeat the independent scientific cases without altering their original archive;
reproduce historical bug witnesses on the historical input and test that the
repaired implementation no longer has those defects. Add high-precision and
exact endpoint tests, domain rejection tests, and checks that certificate callers
use upper endpoints rather than rounded nominal scores. Run remote CI before
merge and on merged main. Record actual checks, limitations, and changed files.

## Stop

Stop after the repair and verified integration. Do not conduct a new novelty
study, extend the scientific task, execute a laboratory experiment, change
privacy, choose a license, or publish a release. Existing physical and statistical
assumptions remain in force. The original audit report remains historical evidence,
not a document to rewrite so that it appears to have found no defects.
