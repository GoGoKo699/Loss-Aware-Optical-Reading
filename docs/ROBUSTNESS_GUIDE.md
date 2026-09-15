# How errors affect the experiment

The supplied four-mode robustness study has been imported unchanged and its
results independently regenerated. Start with the table below and the
[uncertainty worksheet](../experiment/UNCERTAINTY.md). Full proofs and exact
certificates are available when needed; they are not prerequisites for
commissioning. The [integration record](../integrations/lab-handover-01/REPORT.md)
records import and verification. Pending-commit language inside the original
study describes its delivery date and is preserved as evidence.

## Classify the physical error before choosing a conclusion

| Measured or hypothesized structure | Result under its precise assumptions | What the lab must establish |
|---|---|---|
| Common calibratable basis change | If every map is V T O_j W, known common unitary V and W are absorbed into preparation and one decoder. The ideal optimum is unchanged. | The same V/W must apply across all hidden labels and every point claimed to share a fixed physical receiver. Label-dependent correction is forbidden. |
| Specified symmetric dephasing | The channel sends rho to v rho + (1−v) diag(rho), with the same real v on every off-diagonal pair. At four-mode score C−5E the jointly optimal input still uses the fixed D4. | One measured visibility or one RMS phase value does not establish this channel. It must be label independent; unequal coherence factors and deterministic bias are different models. |
| Systematic marked-phase bias | Replacing the marked pi by pi+delta breaks orthogonality. Exact finite examples prove positive regret for the old optics even after optimizing its input and all 625 click-assignment policies. | Identify the actual phase-error pattern. These examples use exact rational unit-circle parameters, not a universal tolerance on any reported phase error. |
| General coherent-map deviation | A simultaneous operator-norm radius epsilon gives conservative score/regret envelopes including the vacuum. They are often loose. | Bound the full maps and test-time drift, not just a fit residual or mean amplitude matrix. |
| Common downstream rotated loss | Data processing supplies a joint ceiling, and a feasible fixed score supplies a conservative gap bound. | Establish the actual placement/map. This gap can contain information loss and is not an attained receiver regret. |

All rows concern the stated **four-mode, one-photon, uniform-label, one-use model**.
The quantitative study uses C−5E. Its results do not become native Walsh eight-mode
claims because an SU8 processor is available. The embedded four-label route can
use a four-mode result only when its effective active-mode model satisfies the
assumptions and leakage/readout uncertainty is separately covered.

## Three different losses of performance

**Information loss** changes what any permitted receiver can learn from P1.
**Fixed-receiver regret** is the gap between the optimized fixed receiver class
and the joint input/arbitrary-measurement optimum for the same device.
**Implementation error** is the difference between a specified feasible strategy
and what our source, receiver and readout achieve. These quantities answer
different questions. Keeping the optimal decoder does not guarantee enough
score to beat the classical source class.

For the symmetric dephasing model, let a_i=sqrt(eta_i). The exact joint optimum
at the registered penalty is

```math
J=\max\{0,\lambda_{\max}(B_v)\},\qquad
B_v=\frac{3}{2} v aa^T-\left(\frac{7}{2}+\frac{3}{2}v\right)\mathrm{diag}(\eta).
```

When positive, its positive top eigenvector gives the retuned input and D4
attains it. Otherwise always inconclusive attains zero. Positive score requires
v>7/9; that is a threshold for this payoff, not for all information. At the
illustrative eta=(.7,.7,.7,.56), v=.99 gives approximately .630210124, whereas
v=.95 gives .511299363. Both have zero optimized receiver regret in that model.
These are calculations, not hardware measurements or acceptable-noise limits.

By contrast, the finite systematic-bias example near delta=.0999168 radians
has strictly positive regret enclosed approximately by
[.0073969546, .0073969712] per attempt. This compares the optimized fixed optics
with the full declared joint class. It is more than a comparison against one
poor input. See the exact model and certificates before using extra digits.

## What was verified

The original archive hash matches the owner's supplied SHA-256. Eight supplied
unit tests pass. A fresh regeneration yields 41 scenarios and 381 diagnostics,
with RESULTS.json byte-identical to the supplied result. The optimizer-free
checker passes 11,161 checks, including 10,828 exact positive-matrix checks,
on both supplied and regenerated evidence. A separate run forbids optimizer
calls and confirms zero calls. These are separate inventories, not one proof count.

GitHub regeneration also exposed numerical-backend dependence of proposed
witness bytes. Selecting the Haswell BLAS kernel reproduced that differing
hash exactly, with the same models and all exact certificate checks passing.
Fresh witnesses are checked for validity, compatible bounds and reported
precision; all supplied evidence hashes remain fixed. See the
[preserved portability investigation](../integrations/lab-handover-01/REGENERATION_PORTABILITY.md).

The optimizer proposes witnesses; exact rational inequalities verify the finite
model bounds. The verifier shares model and arithmetic helpers with the study,
so this is not formal verification of all software. The continuous analytic
statements have proofs. Ordinary floating forecasts, rounding of displayed
examples and physical calibration have separate status.

In particular the study's ideal-source P1 screens use mean signal budget one,
no source impurity and no dark counts. They do not replace the original
imperfect-source forecast, registered statistics or acquisition plan.

## Follow the evidence only as far as needed

- [Practical worksheet](../experiment/UNCERTAINTY.md): laboratory values left to supply.
- [Original calibration worksheet](../studies/robustness-01/CALIBRATION_WORKSHEET.md): near-optimality and source-class advantage conditions.
- [Full study report](../studies/robustness-01/REPORT.md): model-specific results and boundaries.
- [Proofs](../studies/robustness-01/PROOFS.md): common bases, dephasing, phase errors and map bounds.
- [Study commands and manifest](../studies/robustness-01/README.md): reproducible code and exact witnesses.
- [Independent import review](../integrations/lab-handover-01/ROBUSTNESS_REVIEW.md): precise checks and environment.
