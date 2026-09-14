# Repair integration record

This record supplements REPORT.md. It distinguishes successful scientific checks
from a workflow publishing failure and the subsequent authorized connector write.

## Exact revisions

- Main before repair: `d07e4e2180992ab52ee08d0a0cad689154d2e9bd`.
- Preserved audit: `10410caf761ad858236d22c4a2f5d9a53bc94dff`.
- Repair work order: `969ee2b3b646fa7abfba2a9dccdddc9ec6927bdb`.
- Hash-locked source transport: `585046ab2edd8e458d8666cae3e3ec7018d39133`.
- Verified source-and-evidence commit: `09814c86d72a052a08a40663c541eecde5768528`.
- Its tree: `c9090062ce786a3a28fc685c31eaa33a940a8faa`.

## Remote checks and publication of the branch

[Integration run 34870212124](https://github.com/GoGoKo699/Loss-Aware-Optical-Reading/actions/runs/34870212124)
verified every source preimage and reconstructed hash, applied the bounded patch,
and passed all 28 unit groups, all 5,261 inherited checks and frozen comparisons,
the historical 998-check audit, and all 993 unchanged scientific audit cases
against the repaired implementation. It committed the exact 24-path change set,
including its logs and results in REMOTE_EVIDENCE.tar.xz, and checked a clean tree.

The job then failed at git push: its built-in Actions token could not update
`.github/workflows/verify.yml` without workflow-writing permission. This was not
a failed science or regression check. No token permissions were changed.

The uploaded commit object remained readable through the authorized GitHub
connector. Its complete SHA, parent, tree, exact changed-file list, job log and
REMOTE_SUMMARY.json were checked. The connector then fast-forwarded only
`repair/theory-01` to that verified commit, without force. Main was not updated
by this recovery. The one-time publishing workflow is absent in the resulting
source tree; the ordinary workflow retains read-only permissions.

REMOTE_SUMMARY.json describes the passed checks, not overall success of the
publishing job. The failed job remains visible. The final normal push, PR, and
post-merge workflows must separately pass and be recorded in the integration PR.
Do not infer their outcome merely from this file.

## Local and remote numerical records

LOCAL_SUMMARY.json records the earlier local runtime. REMOTE_SUMMARY.json and its
manifest/archive record the real GitHub runner. Both retain the same scientific
case ordering and tolerances. The number of rounding-sensitive derived-budget
name suffixes differs by environment: 74 locally and 88 on this runner. These
suffix differences are explicitly listed; no scientific check is removed.
The remote maximum independent residual is approximately `1.6126e-8`, below the
unchanged full-Hermitian diagnostic tolerance. Numerical differences between
runners are not rewritten into the original audit or frozen reference results.

Only F01-F03, their numerical contract, integration/reproduction support, and
associated documentation are included. The completed audit is carried into main
unchanged when this branch is merged. No new theorem-level novelty assessment,
optical calibration, laboratory data, license, release, or privacy change is implied.
