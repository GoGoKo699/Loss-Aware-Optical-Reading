# Research roadmap

The target remains a simple, loss-aware optical reader with a defensible
reliability and signal-photon comparison. The working contribution is
[input-only optimal retuning plus an all-classical illumination bound](CONTRIBUTIONS.md),
not a new quantum-learning architecture.

## Completed foundations

The mathematical audit is complete and F01-F03 are repaired. The code distinguishes
nominal recipes from outward-safe photon-support bounds. The bounded predecessor
comparison is complete and integrated into the reading path. It identifies
inherited formulas and two candidate technical claims; it does not clear priority.
Original source, audit evidence and frozen outputs remain preserved.

## Next decisions

Close the concrete S18/S20 and nearby multiclass-bound coverage gaps using the
[current work order](../work_orders/CURRENT.md). Revise a candidate classification
only when a verified theorem, reduction or counterexample warrants it. Do not
repeat a broad literature search without addressing the named gaps.

Separately, initial laboratory feedback should establish whether the source,
independent optical sections, shared phase reference, loss model and complete
readout support the [claims-to-tests plan](../experiment/CLAIMS_TO_TESTS.md).
The lab is not being asked to execute or fully design the apparatus before review.
After that feedback, use independent pilot data to select feasible settings and
freeze the plan before held-out acquisition. No example JSON file authorizes
an experiment, and no transmission or large shot count is already confirmed.

## Later extensions, not current results

A second orthogonal phase code can test transfer of the design rule. Eight
single-path flips are not an orthogonal eight-symbol code. Exact arbitrary-loss
classical finite-error optimality and adaptive total-dose advantages need separate
proofs and scope decisions. More modes alone do not strengthen the claim.

The longer-term target is a predictive, calibrated reading capability that another
laboratory can assess under a meaningful illumination budget. Neither an observed
advantage nor external peer-review/priority clearance is established. The paper
should be drafted around a distinct supported claim, not a journal label or an
accumulation of controls.
