# Why this first experiment is worth reviewing

**Purpose: initial technical feedback, not authorization to build or collect a
large data set.** Theory and numerical checks exist; laboratory feasibility and
calibration remain unconfirmed. All example settings remain hypothetical.

The apparatus uses one computational photon at a time in four tested paths.
A source herald may be external to the computation. No interacting auxiliary
photons, quantum memory, or recirculation are requested.

## One candidate mechanism result and a credited benchmark

```text
prepare amplitudes -> P0 -> hidden phase/loss section -> P1 -> receiver -> detectors
```

P0 is the incident signal-photon accounting plane. P1 is the accessible output
of the unknown device, before our receiver. The classical comparator may use
any receiver from P1 onward. Losses in our decoder and detectors reduce our
score, not the ideal competitor's ceiling.

A, joint input-only retuning, is the leading candidate theoretical contribution.
B is a derived optical source-class benchmark, credited to earlier discrimination
results and optical overlap/concavity arguments. This changes attribution, not
what the apparatus must do or how strong the comparison is. See
[CONTRIBUTIONS.md](../docs/CONTRIBUTIONS.md) and the [source map](../SOURCE_AUDIT.md).

The question is whether pre-device retuning with a fixed decoder reaches the
predicted performance and supports a calibrated source-class separation. It is
not whether a new interference trick or generic reliability inequality has
been discovered. The known phase reader and uniform curves are controls.

## Roles of the unchanged tests

| Test | What changes | What it could establish |
|---|---|---|
| M1 | Change preparation and error penalty; keep the decoder fixed | Agreement with the predicted retuning rule. A finite scan is not proof of global optimality or a nonclassical-source certificate. |
| P1 | Use preselected photon inputs and count every attempt | A measured score above the valid all-classical ceiling excludes every permitted coherent mixture/receiver, not just the laser control. |
| P2 | Implement a coherent displacement-and-click receiver at severe imbalance | A measured score above the whole four-path photon bound excludes that restricted class, not every quantum architecture. |

No test order, penalty, confidence allocation, trial budget, or operating point
is changed here. [FIRST_EXPERIMENT.md](FIRST_EXPERIMENT.md) remains the operational
reference. Its abstract coherent minimum-error measurement is not presumed
available because the chip implements four-mode unitaries.

## What needs laboratory confirmation

**Separate roles and fresh labels.** Preparation precedes a physically hidden
operation and a label-independent receiver. Do not compile the answer into a
complete matrix. Each charged trial gets a fresh independent uniform label.
Repeated use of one stable label is another task. There are four promised pi
flips and no fifth healthy setting.

**Source and calibration.** Characterize vacuum and multiphoton components, mean
incident signal energy and tails, and all four device maps relative to a common
phase reference. The confidence region must cover test-time behavior. A fitted
matrix or calibration residual is not automatically that region. A common
post-encoding noise channel and a deterministic drift envelope are different
assumptions; neither can be silently substituted for the other.

**Complete blinded records.** A clock or source herald before exposure defines
a trial, not an output coincidence. Retain all 16 detector masks, including
no-click and multiple-click events. Reveal the hidden label only for offline
scoring. Separate pilot and test data. Do not stop at significance. The
independent-trial or conditional-energy assumptions must hold; a run-wide
average intensity alone is insufficient.

**A real reverse receiver.** P2 requires label-independent coherent background
cancellation and its measured optical/detection costs. Laser intensities through
the photon decoder do not implement it. Without this capability, M1 and P1 can
still be reviewed but the reverse region remains theoretical.

## Requested response

The [five original questions](LAB_REVIEW.md), a block diagram marking P0/P1,
relevant existing calibration records, and a feasibility assessment suffice.
Do not commit to a transmission value or 500,000 trials before a pilot supports
a conservative margin. The lab is not being asked to engineer the entire
experiment before giving feedback.

An unfavorable feasibility assessment is useful. It must not be hidden by
weakening the comparator. Conversely, failure of a sufficient certificate does
not prove that every single-photon advantage is absent.

No lab was contacted, no hardware selected, and no data acquired in this
integration. The named literature-access tasks are resolved, not the wider
priority or publication-significance question for A and the eventual experiment.
