# Actual CI diagnosis and preserved results

The first handover head `ab49872fa5ef8eed95bb6f1ec907b5ca750213aa`
passed 80 of 81 unit tests on both its push and PR runs. Fresh robustness
RESULTS.json had hash
`29287b9d89188fa2a4abf7fd4769a35f6e0a7b8ab17ae58a808be12db890396b`,
which failed the new test's required original hash
`74c0b5ca9f114be36501426f28dc012fcfdb6b872ed6bb8533d463b6cddd14db`.
That assertion preceded certificate verification, so those first CI runs did
not establish whether the differing result had valid witnesses.

- [Initial push failure: 34936982892](https://github.com/GoGoKo699/Loss-Aware-Optical-Reading/actions/runs/34936982892).
- [Initial PR failure: 34937012992](https://github.com/GoGoKo699/Loss-Aware-Optical-Reading/actions/runs/34937012992), with decoded [job log preserved](INITIAL_PR_FAILURE.log).

Diagnostic commit `1ae37afd5b3cac74fc6056f5dcce26f16da9a4a9` moves the
unchanged exact verifier ahead of the unchanged hash assertion and reports JSON
field differences if they recur. It does not change the study, its optimizer,
its rational arithmetic, its supplied tests, or any assertion or tolerance.

Both subsequent workflows passed all 81 tests, the 5,261-check reproduction,
998 historical and 993 repaired cases, and the clean-tree gates:

- [Diagnostic push success: 34937266828](https://github.com/GoGoKo699/Loss-Aware-Optical-Reading/actions/runs/34937266828).
- [Diagnostic PR success: 34937269388](https://github.com/GoGoKo699/Loss-Aware-Optical-Reading/actions/runs/34937269388).
- Both complete decoded logs are preserved in [CI_DIAGNOSTIC_SUCCESSES.tar.xz](CI_DIAGNOSTIC_SUCCESSES.tar.xz).

Their fresh results matched the required original hash exactly and passed
11,161 optimizer-free verification checks. No JSON differences were emitted.
A separate local Python 3.13.5 environment with the recorded dependencies also
passed all three integration tests, including the same fresh-result hash and
exact verifier; see [PYTHON313_ROBUSTNESS.log](PYTHON313_ROBUSTNESS.log).

The source of the intermittent first-run byte mismatch remains unidentified.
Python version alone is not an explanation: the supplied Python 3.13.5 run,
local Python 3.12.14 and 3.13.5 runs, and subsequent GitHub Python 3.13.5 runs
all matched. These observations do not establish universal cross-environment
byte determinism. The failed runs remain part of the record, and a future hash
mismatch still fails rather than being ignored or accepted under a second hash.

The final handover head and post-merge main workflows must also be inspected.
These diagnostic successes do not substitute for those final checks.
