# Why this first experiment is worth reviewing

**Purpose: initial technical feedback, not authorization to build or collect a
large data set.** The theory and numerical checks exist. The source, optical
interface, calibration accuracy, and obtainable margins have not been confirmed
by the laboratory. All example settings in the protocol remain hypothetical.

The proposed apparatus has one computational photon at a time and four tested
paths. A source herald may sit outside the computation. There is no request for
interacting auxiliary photons, quantum memory, or recirculation.

## One mechanism, two questions

The optical sequence is

```text
prepare amplitudes -> P0 -> hidden phase/loss section -> P1 -> receiver -> detectors
```

P0 is where incident signal photons are charged. P1 is the output of the declared
unknown device, before the chosen receiver. The ideal classical comparison is
allowed any receiver from P1 onward. Losses in our decoder and detectors reduce
our measured score; they cannot also be used to lower the competitor's ceiling.

The first question is whether changing only the preparation reaches the predicted
loss/reliability tradeoff with one fixed photon decoder. The second is whether
the unconditional performance can exceed the entire declared classical source
class at the same incident signal budget. These are the two
[candidate contribution statements](../docs/CONTRIBUTIONS.md).

The basic phase-code reader and several of its measurement formulas are known.
The experiment is not proposed as a new interference trick. Its value would be a
predictive test of input-only retuning and a calibrated source-class comparison.
The predecessor distinctions are recorded in the [source map](../SOURCE_AUDIT.md).

## How the existing tests support those questions

| Existing test | What changes and what stays fixed | What the result would establish |
|---|---|---|
| M1: preparation test | Change the pre-device amplitudes and wrong-answer penalty; keep the photon decoder fixed. | Agreement with the predicted retuning rule in the calibrated model. This alone is not a nonclassical-source certificate. |
| P1: positive test | Use a preselected photon preparation and record every attempt. | A score above a valid classical ceiling excludes every allowed coherent-state mixture and receiver under the stated assumptions. Beating only the implemented laser control is insufficient. |
| P2: reverse test | Implement a coherent displacement-and-click receiver at a severe-imbalance setting. | A measured score above the restricted photon ceiling excludes that entire four-path one-photon class, not every possible quantum architecture. |

These are explanations of the existing tests, not changes to their order,
endpoints, penalties, confidence allocation, or trial budgets. The
[first-experiment protocol](FIRST_EXPERIMENT.md) remains the operational reference.
The known uniform-loss curve and uncompensated preparations serve as controls.
Its abstract coherent minimum-error measurement is not presumed available merely
because the chip can perform four-mode unitaries.

## What must be established before collecting held-out trials

**Independent optical roles.** Preparation must precede a physically hidden
operation, followed by a label-independent receiver. An answer-dependent compiled
matrix is not a substitute. Each charged trial receives a fresh independent
uniform hidden label; repeated interrogation of a stable label is a different
task. Four one-path pi flips are promised, with no fifth healthy setting.

**A defensible source and calibration model.** The laboratory should describe
vacuum and multiphoton components, the mean signal-energy bound and its tail
assumptions, and the four device maps relative to one common optical phase
reference. The maps' confidence region must cover test-time behavior. A fitted
mean matrix or a residual from calibration is not automatically such a bound.
Label-independent post-encoding noise and a deterministic drift envelope are
different assumptions and should not be conflated.

**Complete, blinded records.** A trial begins at a pre-exposure clock or source
herald, not an output coincidence. Retain all 16 detector masks, including no
click and multiple clicks. Keep the label away from preparation and decoding,
then reveal it for offline scoring. Pilot and test data remain separate; do not
stop when significance first appears. The independent-trial or explicit
conditional-energy contract must hold, not only a run-averaged intensity claim.

**An actual reverse receiver.** P2 needs label-independent background
cancellation with a coherent reference and its measured losses. Ordinary laser
intensities through the photon decoder do not implement that receiver. Without
this capability, P1 and M1 may still be reviewed, but P2 stays theoretical.

## The requested laboratory response

Use the five questions in [LAB_REVIEW.md](LAB_REVIEW.md). A block diagram showing
P0/P1, available preparation and detection controls, relevant existing
calibration records, and a feasibility assessment are sufficient for this stage.
Do not commit to a particular transmission or a 500,000-trial test before pilot
characterization supports a conservative positive margin.

A useful review may find that the source presence, losses, phase stability, or
recording interface cannot support the intended comparison. That is actionable
feedback, not a reason to silently change the benchmark. A failed certification
test also does not prove that all single-photon advantages are absent.

This integration adds no laboratory data and selects no hardware. The remaining
priority checks and outside proof review are separate from technical feasibility.
