# Bounded robustness study of input-only retuning

Baseline main: `de73c9b094036b756d1ff008eaccbc52cec46207`.
No canonical theorem, source module, acquisition protocol, experimental setting,
old evidence or test was changed. No laboratory was contacted and no apparatus
capability is inferred from the hypothetical models.

## Decision

**The fixed-receiver idea is robust to some important noise structures, but not
to all errors called phase noise. Calibration must distinguish a random loss of
coherence from a systematic error in the encoded phase.**

The bounded analysis gives three useful outcomes: an exact fixed-receiver
optimality result for symmetric dephasing; explicit small phase-error cases
where another receiver provably does better; and conservative bounds for residual
map errors and common downstream loss. These suffice for a device-informed
pilot conversation. They do not require delaying initial laboratory review for
an arbitrary-noisy-photonics theorem.

## 1. Some errors require calibration, not a different scientific design

A known common input/output unitary change can be absorbed into preparation and
one fixed calibrated decoder. If the same change applies across the hidden labels
and the entire planned loss/penalty scan, the original optimum is unchanged.
The calculations include six such examples and check exact unitary identities.

This does not excuse choosing a new physical receiver at each data point while
calling it fixed. Label-dependent changes also cannot be corrected with the
hidden answer. The relevant questions are what can be calibrated once, what
actually varies during the scan, and what remains uncertain on test trials.

## 2. Symmetric random dephasing preserves the exact simplification

For the explicitly defined common channel

```math
\mathcal D_v(\rho)=v\rho+(1-v)\mathrm{diag}(\rho),
```

all pairwise off-diagonal coherences have the same attenuation v. Under the
original four-path orthogonal code and diagonal loss, the full input/measurement
optimum at C-5E is

```math
\max\left\{0,\lambda_{\max}\left[
\frac{3}{2}v\,aa^T-\left(\frac{7}{2}+\frac{3}{2}v\right)
\mathrm{diag}(\eta)\right]\right\},\qquad a_i=\sqrt{\eta_i}.
```

A positive optimum is attained by changing the input to the positive principal
eigenvector and retaining D=J/2-I. If the best score is zero, always returning
inconclusive is optimal. The proof bounds arbitrary POVMs, not only the selected
receiver. Thus optimized fixed-receiver regret is **exactly zero in this model**.

At the illustrative transmissions (0.7,0.7,0.7,0.56):

| Coherence factor v | Optimal C-5E score | Receiver regret |
|---|---:|---|
| 1.000 | 0.659944903 | 0 exactly in this model |
| 0.999 | 0.656971304 | 0 exactly in this model |
| 0.990 | 0.630210124 | 0 exactly in this model |
| 0.950 | 0.511299363 | 0 exactly in this model |
| 0.800 | 0.065896572 | 0 exactly in this model |
| 0.770 | 0.000000000 | 0 exactly in this model |

The source may still lose enough performance that the classical certificate
cannot be exceeded. Optimality of the photon receiver and usefulness against the
classical source class are different questions. A threshold at v=7/9 concerns
positivity of this particular penalized score, not the existence of information.

The model includes independent Gaussian phases of equal variance through
v=exp(-sigma squared), when the fluctuations are label independent. Arbitrary
phase biases, unequal coherence factors, or mean-amplitude substitution are not
covered. This is a short extension of the baseline proof, not a priority claim
for a new general noise theorem.

## 3. A systematic marked-phase error is different

Change the marked phase from pi to pi+delta, with the same bias at each possible
marked path. Losses remain diagonal. The code is then nonorthogonal.

For each finite rational model, this study optimizes over **all complex input
states and all 625 classical click-assignment policies with the fixed optics**.
The full joint input/POVM comparison has separately checked upper and lower
certificates; it is not a local circuit-search comparison.

For nominal losses (0.7,0.7,0.7,0.56), rounded summaries are:

| Marked-phase bias delta (radians) | Fixed-optics optimum, approximately | Joint optimum enclosure | Upper receiver regret |
|---:|---:|---:|---:|
| 0.000000 | 0.659944903 | [0.659944902, 0.659944904] | 0.000000001 |
| 0.019999 | 0.659647571 | [0.659944862, 0.659944878] | 0.000297307 |
| 0.049990 | 0.658087561 | [0.659943735, 0.659943751] | 0.001856190 |
| 0.099917 | 0.652529494 | [0.659926450, 0.659926465] | 0.007396971 |
| 0.199337 | 0.630504515 | [0.659656274, 0.659656294] | 0.029151779 |

For example, at delta=0.0999168 the exact saved regret bounds are approximately
[0.0073969546, 0.0073969712] score units per attempt. Both endpoints account for
input optimization and all classical decoding policies on the fixed receiver.
The lower endpoint is positive: changing the measurement genuinely helps.

At uniform loss, an explicit different four-port unitary, obtained from the
polar factor of the erroneous phase code, loses score only at order delta to
the fourth; the old decoder loses at order delta squared. This provides a
concrete receiver mechanism, not a hypothetical unconstrained black box. The
nominal four-symbol phase bank can alternatively be corrected to restore the
intended ideal code.

A bias around 0.05 radians costs about 0.00186 score units in the moderate-loss
example; around 0.10 it costs about 0.00740; around 0.20 it costs about 0.02915.
These are sensitivity examples, not universal phase specifications. A one-label
bias has different effects, and is separately checked. Calibration must identify
the actual pattern, not only one RMS number.

## 4. Generic error and distributed loss have different kinds of bounds

The baseline trace-distance argument gives, for an arbitrary coherent-map
operator-norm radius epsilon around the ideal family,

```math
0\le\Delta\le\min\{1,24\epsilon\}.
```

It is uniform but often very conservative. If a feasible actual fixed score is
available, use the joint perturbation ceiling minus that score instead. The
worksheet distinguishes certification failure due to a loose bound from actual
failure of the optical mechanism.

The common downstream rotated-loss screen is more informative. One attenuated
superposition has extra amplitude factor 1-d, at a fixed mixing angle about
0.1993 radians. At d=0.025, the extra power survival of that eigenmode is 0.950625.
The same-device joint optimum cannot exceed the ideal pre-channel optimum by
data processing. For moderate imbalance the fixed strategy achieves 0.650658032,
while the ideal ceiling is 0.659944903. Its receiver regret is therefore at most
0.009286871. The corresponding stronger-imbalance bound is 0.008916384.

These last two bounds are not asserted tight: some of the score difference can
be genuine loss of accessible information rather than receiver suboptimality.
Only the phase-error cases have tightly enclosed joint-versus-fixed regret in
this study. No general exact solution for distributed noisy meshes is claimed.

## 5. Consequence for the first experiment

Keep M1, P1 and P2 unchanged. M1 concerns the preparation rule; P1 compares
unconditional measured performance with the credited all-classical ceiling; P2
compares an achieved coherent receiver with the declared entire photon class.

Before freezing the main acquisition, ask the laboratory to identify whether its
dominant residual is a common basis offset, symmetric dephasing, systematic
encoding error, or more general mixing/loss. Then use the appropriate exact or
bounded comparison and add actual source/readout/calibration uncertainty.

For scale only, an extra ideal-source screen retains a positive modeled P1 margin
at v=0.99 even with downstream survival 0.92 and the parent's illustrative
500,000-trial statistical allowance. At v=0.95 that screen fails although the
fixed photon receiver is still exactly optimal in its model. Conversely a
systematic phase error can produce receiver regret without removing every
possible photon advantage. These fields are ordinary floating forecasts with
mean signal budget **one**, no dark counts, and no source impurity; they are
not the parent's source model, calibration, power guarantee, or acquisition plan.

The [calibration worksheet](../studies/robustness-01/CALIBRATION_WORKSHEET.md) supplies separate
near-optimality and source-advantage conditions, while leaving every laboratory
input unfilled. Initial review and calibration pilots should proceed before
selecting final hardware tolerances. No extra optical component is mandated by
this study.

## 6. Verification and exactness

The final run contains **41 scenarios**: 17 deterministic phase-code cases,
12 symmetric-dephasing cases, six common-unitary calibrations and six rotated-loss
cases. It also performs 381 higher-level optical/algebraic diagnostics. These
counts have separate meanings; they are not combined into a proof count.

The phase cases use an exact joint diagonal-channel SDP formulation, but no SDP
solver is required by the code. SciPy linear programs with spectral cuts propose
a dual matrix; exact rational LDL verifies its positivity and all state-payoff
inequalities. Exact positive factors and a completeness check supply a feasible
POVM and lower score. Each fixed-optics upper checks all 625 policies.

The widest saved joint interval for a phase case is 2.16e-08. A separate
optimizer-free verifier passed **11,161 checks**, including
**10,828 exact positive-matrix tests**, and independent
direct optical and uniform-case formula checks. Its narrow rational guarantees
are not extrapolated to calibration or the ordinary floating-point P1 screens.

A second final run in a fresh directory reproduced RESULTS.json byte for byte.
Its SHA-256 is `74c0b5ca9f114be36501426f28dc012fcfdb6b872ed6bb8533d463b6cddd14db`.
The evidence archive contains the complete results, exact witnesses, solver
retry records, environments, logs and verification ledger. No original project
module or external article code is imported. See [PROOFS.md](ROBUSTNESS_PROOFS.md) and
[DEVELOPMENT_NOTES.md](../studies/robustness-01/DEVELOPMENT_NOTES.md) for assumptions and failures.

## 7. Delivery boundary

This completes the bounded scientific study locally. What remains before a
main experiment is a laboratory-specific model and uncertainty budget, not a
requirement to solve arbitrary noisy optical discrimination. Wider publication
significance and priority for A remain distinct from these tolerance results.

---

Preserved source: [original document](../studies/robustness-01/REPORT.md). Historical delivery-status paragraphs remain in that source;
see the [integration record](../integrations/lab-handover-01/REPORT.md)
for repository integration and verification.
