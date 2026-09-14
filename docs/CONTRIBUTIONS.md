# Two claims for loss-aware optical reading

This is a contribution note for research and initial laboratory review, not a
manuscript or a claim that publication priority is settled. The mathematical
audit supports the stated results; the predecessor comparison narrows what
could constitute a contribution. No experiment has been performed.

## The question

A reader must identify one of four promised optical phase patterns. Exactly one
path has a pi flip, with a fresh uniform hidden label for every interrogation.
The reader can return a label or an inconclusive result. Let $C$, $E$ and $F$
be the probabilities of a correct, wrong and inconclusive answer, per attempted
interrogation. Thus $C+E+F=1$. A selected penalty $\lambda$ gives the score

$$
S_\lambda=C-\lambda E.
$$

The question is not whether a four-mode interference pattern can be reproduced
with laser light. It is which input and receiver give the best decision when
illumination, loss, errors and unsuccessful trials are counted.

The single-photon mechanism and Hadamard phase reading are established
[Guha and Shapiro](https://arxiv.org/abs/1207.6435). The project keeps that simple
mechanism and studies two more specific statements.

## A. Retune the input rather than the receiver

For a flat orthogonal phase code with uniform labels and known,
hypothesis-independent diagonal transmission, the joint optimum over the
incident photon and every final measurement is attainable with the same code
decoder. Only the normalized input distribution must change; at sufficiently
large allowed error, empty outputs may also be assigned random guesses.

For the four-symbol case, let $\eta_i$ be the path transmissions and set
$v_i=\sqrt{\eta_i}$. For $\lambda\ge1/3$,

$$
B_\lambda=\frac{1+\lambda}{4}vv^T-\lambda\,\mathrm{diag}(\eta),
\qquad
\max S_\lambda=\lambda_{\max}(B_\lambda).
$$

The input probabilities are $p_i=z_i^2$, where $z$ is the normalized positive
principal eigenvector. The decoder is always $D=J/2-I$. At zero error this reduces
to $p_i\propto1/\eta_i$, which balances surviving amplitudes. Complete compensation
need not be optimal when wrong answers are allowed. Theorems 1 and 2 in the
[proof document](../proofs/THEORY.md) give the full frontier and general code.

### What is inherited, and what remains a candidate

For a fixed input, the decoder follows from the established square-root-measurement
criterion of [Eldar and Forney](https://arxiv.org/abs/quant-ph/0005132).
The harmonic-mean endpoint is a short unambiguous-discrimination and normalization
corollary. Error-margin input/measurement optimization itself is also established
[Hashimoto and colleagues](https://arxiv.org/abs/0912.2610).

The candidate contribution is the complete model-specific reduction: optimizing
the normalized input before loss removes the need to change the receiver across
the reliability frontier. A fixed received-state theorem alone does not account
for the input-dependent probability of erasure. The predecessor comparison gives
an explicit normalization argument in [R3](../audits/novelty-01/REDUCTIONS.md#r3-what-is-additional-in-input-only-retuning).
It did not locate an exact predecessor for the complete contract; that is not a
guarantee of priority.

The theorem concerns a photon in the tested paths. It does not include an occupied
bypass rail, an idler or another call to the same hidden operation. It assumes the
specified diagonal-loss model, not an arbitrary lossy mesh. Moving attenuation
between source, device and receiver can change the question being optimized.

## B. Compare against every allowed classical illumination strategy

Let $m$ uniform hidden labels select phase-referenced passive maps $A_j$ from the
charged input modes to the accessible returned modes. Define

$$
H_\Delta=\frac{1}{m(m-1)}\sum_{j<k}(A_j-A_k)^\dagger(A_j-A_k),
\qquad \kappa=\|H_\Delta\|.
$$

For mean incident signal photon number at most $\mu$, the classical bound is

$$
C\le\min\left\{1-E,
\left[\sqrt{1-e^{-\kappa\mu}}+\sqrt{\frac{E}{m-1}}\right]^2\right\}.
$$

The allowed classical source is a nonnegative mixture of coherent states in the
diagonal Glauber-Sudarshan representation. The mixture label can be given to the
receiver. Arbitrary receivers, phase references and arbitrarily rare bright
pulses are allowed. References must not supply hidden-label information, and the
loss environment is inaccessible. The map assumptions must cover the charged
modes and permitted illumination. This is a signal-energy comparison, not total
apparatus power or source cost. Theorems 3 and 4 give the bound and calibration
allowance in the [proof document](../proofs/THEORY.md).

The bound is exact for the uniform-loss four-symbol task when combined with its
attaining alphabet and measurement. It is not an exact arbitrary-map frontier,
and the top eigenvector of $H_\Delta$ is not generally proved to solve the
multiclass transmitter problem.

### What is inherited, and what remains a candidate

The uniform fixed-alphabet curve is exactly a specialization of
[Herzog, Eq. (4.18)](https://arxiv.org/abs/1206.4412). The binary contrast matrix
is inherited from [Bouchet and colleagues](https://arxiv.org/abs/2108.03755), up to
a factor of two. Overlap bounds, concavity, norm perturbation and fixed-sample
concentration are standard tools.

The candidate is the multiclass optical source-class converse: a different
transmitter or intensity mixture cannot evade the bound at the stated mean
budget. A known measurement optimum for one supplied alphabet does not establish
that claim. The exact uniform curve is therefore a credited fixed-state result
with a separate all-source optimality argument. [R4 and R6](../audits/novelty-01/REDUCTIONS.md)
show the distinction. No new priority guarantee follows from combining known tools.

## What the two claims imply for the experiment

Claim A motivates M1: vary the pre-device input with the reliability requirement
and measured loss, while keeping the receiver unchanged. This tests predicted
attainability, not global optimality against every unbuilt apparatus.

Claim B motivates P1: compare all attempted trial records with a conservative
classical ceiling based on independent calibration. Beating only the implemented
laser control is insufficient. The severe-imbalance P2 test addresses the converse
direction by comparing an implemented coherent strategy with an upper bound on
the entire declared photon class. It does not refute all quantum architectures.

The [claims-to-tests note](../experiment/CLAIMS_TO_TESTS.md) specifies the roles
of the three tests without changing the acquisition protocol. Uniform-loss and
uncompensated cases are useful controls, not independent discoveries.

## What can be stated now

The results are mathematically supported within their declared models; the code
has been audited and repaired. The two complete statements remain candidate
contributions after a bounded predecessor comparison. The original S20 full text,
S18 theorem/appendix comparison and nearby equivalent multiclass bounds remain
coverage gaps in the [source map](../SOURCE_AUDIT.md). Outside review is separate.
No observed advantage, laboratory feasibility, adaptive reading result or journal
outcome is asserted. A larger mode count or a learning label does not close any
of these gaps.
