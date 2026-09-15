# Laboratory handover integration record

## Scope and current verification stage

The laboratory handover is implemented on `handover/lab-01`. Both SU4 and SU8
processors are confirmed available. Supporting interfaces and calibration are
explicitly left for laboratory adaptation. No acquisition or correspondence
has occurred. Final handover-head, PR and main workflow results are reported after actual
execution; this document does not infer them from CI configuration.

Baseline main was `de73c9b094036b756d1ff008eaccbc52cec46207`, tree
`a072bbe43effca4c99ea7839c6802c530ac94099`, private. No equivalent handover
branch or open PR existed. The complete 151-file baseline was read through the
authenticated API, all blob identities checked, and the exact tree and signed
commit reconstructed as a shallow local checkout. Direct HTTPS Git transport
could not authenticate; a successful git clone is not claimed. The initial
local working directory was clean. See [START.json](START.json).

## Reader structure and delivered interfaces

- [SU4](../../experiment/SU4.md): principal four-symbol worked example.
- [SU8](../../experiment/SU8.md): four-active-mode embedding and native Walsh8.
- [Commissioning](../../experiment/COMMISSIONING.md), then [M1](../../experiment/M1.md), [P1](../../experiment/P1.md), [P2](../../experiment/P2.md).
- [Physical interfaces](../../experiment/INTERFACES.md) and [uncertainty worksheet](../../experiment/UNCERTAINTY.md).
- [Theory route](../../docs/THEORY_ROUTE.md), [reading crosswalk](../../docs/READING_CROSSWALK.md), and [robustness guide](../../docs/ROBUSTNESS_GUIDE.md).
- [Reference examples](../../examples/lab/README.md) and two safe, mode-aware reference/record scripts.

The README is approximately 1,100 words and places both chip routes in its
first screen. The 250–400-word philosophy is explicitly a draft for owner
approval. It is separate from the factual candidate-A/derived-B hierarchy.
Capmany–Pérez is the main engineering anchor at verified publisher contents/
abstract access. The accessible Barnett–Croke review was inspected for detailed
theory references. No external article or book is redistributed.

## Robustness import and ancestry

The supplied `photonic_robustness_01.zip` matches SHA-256
`ee21bb13afbd913779b5d2eae7b4f15a58d919500a7ed38b09deafb7e929c81b`.
The original ZIP, including APPLY.md, DELIVERY.json and patch, is preserved as
[SUPPLIED_ROBUSTNESS.zip](SUPPLIED_ROBUSTNESS.zip). All 15 supplied study files
are byte-preserved. The original work-order file and commit remain intact.

Live `research/robustness-01` had not advanced from
`ddb17c5040e17cb0078121081afe15de70158fe8`. The inspected additions-only patch
was checked before application and all installed bytes compared against the
supplied packet. Its verified import commit is
`0501631adbbdab92509ccf049552d8cb108cfbb4`, tree
`8888305da239c7d5f785e8d8431cc26bf89d2cc7`, with that original work-order commit
as parent. Its actual push workflow
[34935971968](https://github.com/GoGoKo699/Loss-Aware-Optical-Reading/actions/runs/34935971968)
completed successfully. The handover preserves this ancestry when integrating.
Original “pending repository commit” prose is retained as historical delivery
status; it is not the current import status.

[ROBUSTNESS_REVIEW.md](ROBUSTNESS_REVIEW.md) gives the independent mathematical
and file review. [ROBUSTNESS_LOCAL_EXECUTION.tar.xz](ROBUSTNESS_LOCAL_EXECUTION.tar.xz)
preserves fresh checks, logs, exact witness verification and environment.
Fresh 41-scenario/381-diagnostic regeneration reproduced RESULTS.json bytes,
SHA-256 `74c0b5ca9f114be36501426f28dc012fcfdb6b872ed6bb8533d463b6cddd14db`.
Eight supplied unit groups passed. Both supplied and fresh witnesses passed
11,161 checks including 10,828 exact positive matrices; an optimizer trap
confirmed zero optimizer calls in witness verification. Existing-output refusal
was checked. These separate inventories are not combined into a proof count.

## Preservation and engineering decisions

The seven named document rewrites have a restricted
[old/new authorization ledger](../../provenance/changes/lab-handover-01.json).
Every preimage is pinned to the starting main. The verifier preserves and checks
all earlier ledgers and rejects source/proof/protocol paths in this new layer.
The prior dispatch is [preserved verbatim](PREVIOUS_CURRENT.md). No historical
audit, source archive, frozen result, canonical proof or src routine is rewritten.
The five laboratory required-response questions remain byte-identical.

No old wording test or numerical assertion was weakened. New adapters export
explicit matrices and record schemas, require new output directories, and
refuse protected evidence locations. Native eight-label records use descriptive
analysis only. The four-label embedding adapter retains full masks and a
failure-remapping ledger before invoking the existing analyzer. The historical
analyzer itself has a direct file-writing CLI without an overwrite guard; the
new laboratory route uses the guarded wrapper and does not present that CLI as
a safe output manager. Its established scientific routine is unchanged.

Independent review caught a preparation-completion mismatch between an early
new code draft and the documented matrix. The new implementation was corrected
to flip column 1 in its unitary completion. The embedding is now exactly
Uprep4 direct-sum I4, with a separate test. Earlier uncommitted synthetic files
were retained in scratch; final examples were generated in fresh directories.
This was an implementation-convention correction, not a theorem repair.

## Checks and limitations

Local environment: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, mpmath 1.3.0.
Recorded CI uses Python 3.13.5. The complete original 5,261-check reproduction
and unchanged frozen-result comparison passed. The repair runner passed the
998 historical checks and 993 repaired scientific cases with original case
order/tolerances preserved. The independent 631 predecessor translations passed.
The unit suite additionally reruns the distinct 572 and 717 follow-up packets.
Final suite, recipe-command, static-link and remote-head results are recorded
in the completion supplement after execution.

Mathematics and links receive static syntax/target checks. Actual GitHub visual
rendering has not been inspected; it is not claimed. Apparatus relationships
use physically labelled role tables rather than unverified drawings. The
complete theory and evidence remain one click away from practical pages.

Remaining laboratory inputs: port ordering, compiler conventions and controllable
sections; independent hidden phase/attenuation; wavelength/polarization;
source statistics and absolute mean/tail energy at P0; detector arrangement and
all-attempt readout; coupling and loss placement; timing, gating, fresh labels
and blinding; simultaneous calibration coverage and test-time drift; P2 coherent
displacement/reference capability. No illustrative value is a hardware
specification. Completion of this handover does not authorize data acquisition.

## Final local completion supplement

All 23 distinct commands in the nine experiment pages executed successfully;
each repeat refused to overwrite its output and preserved output hashes.
[RECIPE_COMMANDS.json](RECIPE_COMMANDS.json) records each command and result.
The nine example-README commands also executed with their exact displayed paths
and passed repeat-refusal checks in [EXAMPLE_COMMANDS.json](EXAMPLE_COMMANDS.json).
The reference developer additionally exercised all three embedded M1/P1/P2
variants; [REFERENCE_CHECKS.json](REFERENCE_CHECKS.json) pins the final scripts.

[Static checks](STATIC_CHECKS.json) and [integrity checks](INTEGRITY.json) pass.
[PRESERVATION.json](PRESERVATION.json) verifies all 143 baseline files outside
the eight authorized existing-file edits byte-for-byte. There are no deletions.
The seven document edits plus the restricted verifier are the only preexisting
files changed. All original tests and numerical tolerances remain intact.

[MAPPING_REVIEW.md](MAPPING_REVIEW.md) records independent matrix, phase,
Walsh and P2 nulling checks. Its remaining minor timestamp-schema comment was
resolved after that review: real gate timestamps are required, while a source-
herald timestamp is optional when a clock defines the trial. Separate condition/
preparation summaries were also added to avoid hiding an M1 scan in pooled rates.
The final focused suite has 14 tests; the developer snapshot hashes and execution are in the
reference-check record. Final review strengthened the new example test to require
all six committed example manifests (rather than skip absent examples); the
14-group final focused rerun passed. No scientific assertion was relaxed. The complete final unit run passed **81 tests** and is in [UNIT_TESTS.log](UNIT_TESTS.log).

Publication status remains private. No license, release, manuscript submission,
laboratory correspondence, hardware procurement or experimental acquisition
is part of this integration. Final remote verification must read the exact
PR head and the actual post-merge main workflow before completion is claimed.

[Final independent diff review](FINAL_DIFF_REVIEW.md) passed. The staged diff
also passes Git whitespace checks with `core.whitespace=cr-at-eol`, preserving
standard CSV CRLF record endings and their existing manifest hashes.
