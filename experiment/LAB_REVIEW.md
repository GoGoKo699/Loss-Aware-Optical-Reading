# Initial technical laboratory review

Purpose: decide whether the proposed experiment has a defensible physical input,
unknown-operation, receiver, and calibration interface. The lab is not being asked
to execute or fully engineer the experiment before giving feedback.

## The requested experiment

A single photon in four paths interrogates one hidden, independently chosen pi
phase flip. Known intentional loss imbalance is varied. A fixed four-mode decoder
returns a path label or an inconclusive outcome. The preparation changes with the
selected wrong-answer penalty; the receiver does not.

The primary positive claim compares measured unconditional performance with an
upper bound on every classical coherent-state mixture at the calibrated incident
signal mean budget. A separate severe-imbalance test uses a coherent displacement
receiver to challenge the entire ideal four-path single-photon class.

No computational multiphoton source, quantum memory, recirculation, or invented
component is requested. A herald outside the computation is permitted. Detector
and source capabilities below are questions, not confirmed inventory.

## Why these measurements matter

The optical phase-reading mechanism and uniform fixed-alphabet curve are known.
The proposed technical contribution is twofold: input-only retuning attains the
joint optimum in the stated photon model; a separate bound covers all allowed
classical illumination, not just the control receiver available in the lab.
These remain candidate contributions after a bounded predecessor comparison.

M1 tests the predicted input redistribution with the receiver fixed. P1 tests
whether unconditional data exclude the classical source class under calibrated
assumptions. P2 requires an implemented coherent strategy above the bound for
the whole declared photon class. The test identifiers, settings and acquisition
requirements are unchanged. See [claims to tests](CLAIMS_TO_TESTS.md) and the
[two-claim note](../docs/CONTRIBUTIONS.md).

## Required responses

1. **Physical separation.** Can preparation, the hidden phase/loss bank, and the
   fixed receiver be independently controlled in that order? Please mark incident
   photon accounting plane P0 and device-output plane P1. Compiling a whole matrix
   using the hidden answer is not an acceptable substitute.
2. **One-use gating.** Can a fresh hidden label be sampled, settled, and exposed
   to exactly one charged trial before another fresh draw? What label-independent
   gate and attainable trial rate are realistic? The label may repeat by chance.
3. **Source and energy.** What vacuum/single-photon/multiphoton characterization,
   incident mean-energy bound, tail model, and stability guarantee can be supplied
   at P0? Pump and source-herald costs should be reported separately.
4. **Phase-referenced calibration.** Can all four complex device maps be compared
   with the same optical phase reference, including a simultaneous test-time drift
   bound? Independently discarded global phases change the classical benchmark.
5. **Readout and coherent control.** Can all four outputs be recorded in every
   fixed gate, including no-click and multiple-click masks? Is a stable
   displacement-and-click coherent receiver feasible with existing components,
   and what additional attenuation, reference power, and false-click rates result?

The positive test can remain useful without the coherent displacement branch, but
then the negative region is theoretical, not experimentally demonstrated. State
that limitation rather than substitute an unmatched laser receiver.

## What to send back

A block diagram, the answers above, relevant existing calibration files, and the
lab's assessment of whether independent pilot data can support the declared score
margins. No precise test transmission or 500,000-shot commitment is frozen until
that review. Full protocol: [FIRST_EXPERIMENT.md](FIRST_EXPERIMENT.md).
Theory: [proofs](../proofs/THEORY.md).
