# From the two claims to the first experiment

Purpose: explain what the first measurements would establish, and what they would
not. This note supports initial technical laboratory review. It does not ask the
lab to execute the experiment or design every component before giving feedback.
The [full acquisition protocol](FIRST_EXPERIMENT.md), its P1/P2/M1 identifiers,
illustrative settings and statistical requirements are unchanged.

## Keep the apparatus simple

The intended order is

```text
source and preparation -> P0 -> hidden phase/loss section -> P1
                       -> fixed four-mode decoder -> four output detectors
```

P0 defines the incident signal-photon budget. P1 is the device output before the
selected receiver. Four paths carry one computational photon. A source herald
may define a trial upstream; no interacting auxiliary photon is needed.
Exactly one path receives a pi flip. There is no additional healthy hypothesis.
Each counted interrogation receives a fresh independent uniform hidden label.

The proposed contribution is not the interferometer alone. It is the link between
an optimized input, an attainable decision tradeoff and a bound covering all
allowed classical illumination. [Two-claim note](../docs/CONTRIBUTIONS.md).

## Which record tests which statement?

| Test | Keep fixed or vary | Record and comparison | Limit of the conclusion |
|---|---|---|---|
| M1: input-only retuning | Keep the decoder fixed; vary the input and selected error penalty at a calibrated imbalance. | Full confusion matrix and unconditional correct/wrong/inconclusive rates versus the predicted preparations. | Tests attainability and model agreement. The proof, not a finite input scan, establishes global optimality. |
| P1: positive comparison | Freeze input, score and calibration-dependent classical ceiling before held-out acquisition. | All attempted records must exceed a valid all-classical score bound with the declared confidence. | Excludes the stated classical source class under its access and calibration assumptions; not a speedup or total-energy claim. |
| P2: reverse comparison | Use a calibrated coherent illumination and a feasible fixed background displacement, without knowing the hidden label. | An observed score above the robust upper bound for every allowed tested-path single-photon probe/measurement. | Excludes only that photon architecture. Beating an uncompensated photon input is not enough. |

A uniform-loss case and an uncompensated input provide controls. The known
fixed-alphabet curve is not a new discovery. The theoretical minimum-error
coherent POVM is not automatically implemented by the proposed click detector
control. An implemented control does not define the all-classical limit.

The existing example transmissions, penalties and sample counts are planning
inputs, not requirements already validated on the lab's hardware. Independent
pilot data select viable settings; selection and scoring are then frozen before
the held-out test. No new optimization against held-out records is introduced.

## Five implementation facts needed from the lab

**Independent optical sections.** Preparation, hidden phase/loss settings and
receiver must be independently controlled. Compiling an end-to-end matrix using
the answer does not interrogate an unknown device. Send a block diagram showing
P0 and P1 and which controller sees each label.

**Input statistics at P0.** Characterize vacuum, single-photon and multiphoton
components, and justify the mean-energy and tail bounds. Do not count only
output coincidences as input trials. Source herald and pump costs are recorded
separately from the signal-photon comparison.

**A shared optical phase reference.** Calibration must compare all hidden maps
with one common reference. Dropping a different global phase from each matrix
can preserve single-photon probabilities while changing the coherent comparator.
An average fitted map is not automatically a simultaneous test-time envelope.

**All output records.** Retain all four-detector masks for every declared gate.
No clicks, multiple clicks and failed outputs remain in the trial denominator.
Own receiver and detector losses reduce measured performance; they cannot also
be charged to the ideal competing receiver after P1.

**Coherent control capability.** P2 requires actual stable background displacement
and its losses and reference power must be characterized. Without it, P2 remains
a theoretical region. P1 can still be considered, but the experimental claim must
be narrowed explicitly. Direct intensity measurements are not the same P2 test.

## Statistical and numerical conditions

Use separate calibration, pilot and test data. Fixed-sample tests require the
stated independent-trial or conditional predictable-energy assumptions; a grand
average over differently illuminated complete runs does not suffice. An energy
bound needs metering or a justified source model, not a declaration in a plan.
The code cannot verify blinding or calibration truth.

A finite-error bound must include the calibration confidence allowance and count
all trials. Selecting a score after looking at the test records or stopping at
the first apparent violation is not covered by the fixed-budget protocol.

The photon support interval encloses the optimum for specified binary64 inputs.
Its lower endpoint does not certify the performance of the rounded preparation
implemented in hardware. The classical and statistical pipeline is not wholly
interval-certified. [Numerical contract](../docs/NUMERICAL_CONTRACT.md).

## Interpreting the first outcome

Agreement with the predicted rates supports the model in the tested regime.
A statistically certified P1 violation supports an advantage over the declared
classical class. Failure to violate a sufficient bound may mean insufficient
statistics, a loose bound or unsuitable hardware; it is not a proof of no advantage.
A P2 violation needs its own implemented classical receiver and photon ceiling.
If the actual loss, phase or source model differs from the theorem's assumptions,
revise the model before making the comparison rather than moving losses between
accounting planes to improve the result.

At initial review, a block diagram, answers to the interface questions and any
existing calibration records are sufficient. This stage does not freeze a large
shot budget. Mathematical correctness, publication novelty, physical feasibility
and acquired evidence remain separate. [Lab response brief](LAB_REVIEW.md).
