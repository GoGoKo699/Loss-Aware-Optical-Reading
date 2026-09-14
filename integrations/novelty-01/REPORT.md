# Reader-facing predecessor integration

This task integrates the completed predecessor comparison into the working
repository. It adds no new scientific result and changes no mathematical
implementation, canonical proof, operational experiment, or physical assumption.

Starting main: `80c73751806f45411251711bcfb6bccebc887f0a`.
Preserved audit: `eaa452615096cca9a498c10c5d492a2a74966123`.
Working branch: `integration/novelty-01`. The branch starts from the audit so its
original commits and complete evidence accompany the integration. The work order
is [WORK_ORDER.md](WORK_ORDER.md). Final commit and CI outcomes are recorded in
the integration pull request; this report does not self-claim future checks.

## Reader-facing changes

The README leads with two candidate contributions and makes the established
mechanism explicit. [CONTRIBUTIONS.md](../../docs/CONTRIBUTIONS.md) states each
claim, its assumptions, inherited ingredients, and the remaining possible
technical distinction. [REVIEW_RATIONALE.md](../../experiment/REVIEW_RATIONALE.md)
connects these claims to the existing M1/P1/P2 tests without changing the tests.

The root claim ledger now separates mathematical validity, novelty classification,
and experimental evidence. The source map integrates the actual recovered-text
status and the S01-S21 attribution system. It retains the S18/S20 gaps and does
not call the uniform fixed-alphabet curve or binary contrast newly invented.
The roadmap and current task boundary no longer list the completed audit as
unexecuted. They do not authorize a new research task.

The scientific report retains its equations and operating numbers. Its attribution
and historical verification wording are updated, and display delimiters are
made suitable for GitHub. The short lab brief links the rationale but preserves
all five original technical questions. This is still initial review, not a
request that the lab execute or fully engineer the project before responding.

## Preservation and verification design

No files under `src/`, `proofs/`, `baseline/`, `results/`, `templates/`, the two
old audit directories, or the prior repair packet are changed by this task.
`experiment/FIRST_EXPERIMENT.md`, `docs/PHYSICAL_SETTING.md`, the numerical
contract, original ZIP, original import manifest, and previous repair ledger
are also unchanged. The predecessor audit's original files are included intact.

Four protected document edits are recorded in a separate
[old/new hash ledger](../../provenance/changes/novelty-integration-01.json), applied
after the previous repair ledger. The verifier restricts this new ledger to the
four named documents and two new notes. It cannot be used to authorize a
numerical-source or proof edit, and it rejects stale predecessor hashes.
The original archive hash is not refreshed.

Nine new unit-test groups check the document chain, negative/tamper cases,
all preserved predecessor-manifest members, exact preservation of the report's
11 display equations and five lab questions, local reader-facing link targets,
math delimiters, and explicit contribution limits. Existing unit tests and
scientific tolerances are not modified. The normal CI already discovers these
new tests and still runs the inherited and repaired science suites read-only.

## Local execution evidence

The nine new test groups passed in a fresh selected-source snapshot. The
preserved comparison script also passed all 631 checks; its RESULTS.json was
byte-identical to the previous audit's recorded result, with SHA-256
`aaf6d71e854a421db0eb63ae579118139ac243c07f5be65bd113ccabc2e5c22f`.
The maximum residual was `2.70924301656178e-10` against the existing `1e-9`
tolerance. This checks unchanged equation translations, not priority.

[LOCAL_CHECKS.json](LOCAL_CHECKS.json) records environment and scope.
[LOCAL_TESTS.log](LOCAL_TESTS.log) contains the new document test output. Container
Git access failed at DNS resolution. This is not a claim of an authenticated
local clone or a full local repository regression; the full checks and clean
tree are inspected through GitHub CI at their exact commits.

The first local link test found four references to an existing repair report
that was absent from the selected local snapshot. Copying the existing report
from the supplied repair archive fixed that snapshot issue; no assertion or
tolerance was weakened. The full-checkout CI is the integration check.

## Remaining boundary

The task integrates prior evidence; it does not extend the literature search or
close the remaining source gaps. No laboratory was contacted, no calibration
was acquired, no experiment was executed, and no manuscript was drafted.
Publication-level priority, outside peer review, and measured advantage remain
open. Privacy, license selection, and release state are unchanged.

Stop after reviewed integration and verified main CI. The next scientific step
requires its own bounded authorization; the laboratory feedback path remains
separate from the source-comparison path.
