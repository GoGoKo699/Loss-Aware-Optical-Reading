# SU4: four-symbol phase reading

**Your SU(4) chip is available.** The principal example reads which one of four
paths received a pi phase flip. A single photon occupies a superposition of
the four paths; this is not four photons or four independently carried qubits.
Begin with [classical-light commissioning](COMMISSIONING.md), then use the same
mode convention for [M1](M1.md), [P1](P1.md), or [P2](P2.md).

## What to program and measure

Logical ports are ordered **0, 1, 2, 3**. Vectors are columns; a matrix has
output ports in its rows and input ports in its columns. The laboratory must
record the mapping from these indices to actual chip connectors and detector
channels; the mathematical convention does not claim their physical order.

| Role | Exact target | Physical implementation to identify |
|---|---|---|
| Preparation | A photon with amplitudes `a_i = sqrt(p_i)`, `sum(p_i) = 1` | A programmable preparation section, the other chip, or a separate preparation network |
| Hidden operation | `O_j = I4 - 2 |j><j|`, uniformly selected `j = 0,1,2,3` | An independently controlled phase section, hidden from the reader |
| Device loss | `T = diag(sqrt(eta_0),...,sqrt(eta_3))`, `0 < eta_i <= 1` | Characterized physical attenuation between P0 and P1; independent of the label in the ideal model |
| Photon receiver | `D4 = J4/2 - I4` | A four-mode programmed interferometer after P1 |
| Decision | A single click in output `k` reports `k` | A recorded, fixed-window detector arrangement; no or multiple clicks are inconclusive |

The exact matrices are

$$
O_0=\mathrm{diag}(-1,1,1,1),\quad O_1=\mathrm{diag}(1,-1,1,1),
$$

$$
O_2=\mathrm{diag}(1,1,-1,1),\quad O_3=\mathrm{diag}(1,1,1,-1),
$$

$$
D_4=\frac12
\begin{pmatrix}
-1&1&1&1\\
1&-1&1&1\\
1&1&-1&1\\
1&1&1&-1
\end{pmatrix}.
$$

Here `J4` is the all-ones matrix. In the ideal device the returned amplitude
vector is `T O_j a`, and the detector amplitude vector is `D4 T O_j a`.
The unitary phase operation and attenuation commute in this diagonal model;
distributed loss inside an imperfect mesh needs an actual calibrated map.
**T is a contraction, not an SU(4) unitary.** Four programmed phases do not
implement its attenuation.

For the equal-input, lossless check, `a = (1,1,1,1)/2` and
`D4 O_j a = |j>`. With uniform transmission `t`, the surviving amplitude is
`sqrt(t)|j>`, so the ideal one-photon rates are `C=t, E=0, F=1-t`.
Loss remains an inconclusive attempt even when every surviving photon is routed
correctly.

## Preparation and compiler conventions

The reference files supply an explicit unitary whose first column is `a`.
For a real normalized target `a != |0>`, one convenient completion is

$$
w=\frac{|0\rangle-a}{\|\,|0\rangle-a\,\|},\qquad
U_{\rm prep}=(I-2ww^\dagger)(I-2|1\rangle\langle1|).
$$

This has determinant one and maps input port 0 to `a`; use the identity for
`a = |0>`. The other columns are a programming convention, not extra occupied
inputs. A classical commissioning input of complex amplitude `A` at port 0
instead produces `A a`.

`O_j` and `D4` have determinant minus one. If the compiler accepts only SU(4)
matrices, the targets `exp(i*pi/4) O_j` and `exp(i*pi/4) D4` have determinant
one. **Use the same multiplier for every hidden label.** Record whether and
how this physical common phase is realized. An independent label-dependent
global phase can change the coherent-state comparison even though single-photon
intensities look identical. The raw `O_j` matrices are the canonical physical
task; calibration must establish a shared optical phase convention or retain
the actual phase-referenced maps in the benchmark. See [interfaces](INTERFACES.md).

## From the transfer check to reading

For commissioning, the lab may compile a known end-to-end matrix
`D4 O_j Uprep` to check optical transfer, or verify its blocks separately.
Attenuation must be physically present if `T` is included. This uses a known
test pattern and is classical-wave verification.

A genuine reading experiment needs a preparation fixed without knowing the
current `j`, an independent hidden phase/loss section, and a receiver fixed
without access to `j`. An answer-dependent end-to-end compiled matrix cannot
establish that task. The [arrangements page](INTERFACES.md) shows use of either
existing chip as one role and a proposed use of both chips together.

## Choose the input for the scientific question

For positive diagonal loss and penalty `lambda >= 1/3`, take the positive
normalized top eigenvector `z` of

$$
B_\lambda=\frac{1+\lambda}{4}vv^T-\lambda\,\mathrm{diag}(\eta),
\qquad v_i=\sqrt{\eta_i},\qquad p_i=z_i^2.
$$

Keep `D4` fixed and make no click inconclusive. At the zero-error endpoint,
`p_i = (1/eta_i)/sum_k(1/eta_k)`. The known square-root receiver and this endpoint
are credited ingredients; the leading candidate contribution is the complete
joint input-only retuning reduction under its exact assumptions.

| Recipe | Changes | Fixed during each held-out condition |
|---|---|---|
| [M1](M1.md) | Compare uniform, inverse-loss, and penalty-selected inputs | Decoder, task, port decisions; each calibration/configuration is identified |
| [P1](P1.md) | Select input from pretest calibration | Decoder, penalty, trial budget, source/energy contract, decision rule |
| [P2](P2.md) | Use a declared coherent preparation and background displacement | Hidden task, energy budget and displacement independent of the current label; P2 has its own receiver |

## Run and inspect a reference example

```bash
python scripts/lab_reference.py --recipe commission-su4 --output results/runs/su4-commission
python scripts/lab_reference.py --recipe m1 --chip su4 --output results/runs/su4-m1
python scripts/lab_records.py --route su4 --trials results/runs/su4-m1/synthetic_trials.csv --output results/runs/su4-m1-analysis
```

Run from the repository root after [environment setup](../docs/REPRODUCE.md).
Every output directory must be new. `target_matrices.json` contains the exact
target conventions and numerical matrices; `forecast.json` contains the model
predictions; `synthetic_trials.csv` and `synthetic_summary.json` demonstrate
record accounting. `RECORD_SCHEMA.json` defines the columns. The samples are
explicitly synthetic and descriptive, not acquired evidence.

Record all 16 four-bit click masks, the attempted-trial ID, sealed label,
condition/preparation/receiver/calibration IDs, timing, energy-bound ID, and
integrity flags. Rejected records remain in the denominator. An upstream clock
or pre-exposure source herald may define the attempt; an output coincidence
cannot. Keep pilot and held-out records separate.

A clean routing pattern establishes optical implementation. Agreement with M1
supports the retuning mechanism. A P1/P2 conclusion requires the appropriate
bound and complete acquisition contract; normalized intensity alone provides
neither an illumination budget nor a source-class certificate. Review the
[uncertainty worksheet](UNCERTAINTY.md), [theory route](../docs/THEORY_ROUTE.md),
[Theorems 1–2](../proofs/THEORY.md), and [robustness guide](../docs/ROBUSTNESS_GUIDE.md).
