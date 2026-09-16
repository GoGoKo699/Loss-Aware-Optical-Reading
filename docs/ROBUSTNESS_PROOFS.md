# What survives imperfect optics, and what does not

This bounded study uses baseline `de73c9b094036b756d1ff008eaccbc52cec46207`.
Only four modes and the preselected score S=C-5E are considered. These are
analytic statements and finite-model certificates, not laboratory evidence or
claims of priority. Standard measurement optimization and calibration have
predecessors listed in [SOURCES.md](../studies/robustness-01/SOURCES.md).

## 1. The comparison is between optima on the same physical input

The input is one photon in the four tested paths. There is no occupied bypass,
idler, access to lost modes, or second call. Labels are uniform, hidden, and
fresh for each interrogation. All outcomes, including absence of a photon,
remain in the score. Source impurities and detector errors are separate from
this ideal one-photon model.

Write J(A) for the maximum score over all normalized inputs and arbitrary final
measurements on a specified device. Write F_D(A) for the maximum with a fixed
four-mode decoder D=J_4/2-I, photon counting, and arbitrary classical assignment
of each record to a label or inconclusive. Inputs may have complex amplitudes.
This strengthens the fixed-optics competitor: a failure cannot be blamed merely
on withholding available preparation phases or classical relabelling.

The receiver regret is Delta=J(A)-F_D(A), which is nonnegative. A feasible score
L_D and a proved joint upper bound U_J imply Delta <= U_J-L_D. To demonstrate
that changing the receiver really helps, one needs a feasible joint score L_J
and a fixed-optics upper bound U_D with L_J>U_D. Finding no better receiver by a
local search would establish neither statement.

## 2. Basis calibration is not a failure of the ideal theorem

Let nominal maps be A_j^0=T O_j, with T positive diagonal and O_j the ideal
one-path flips. Suppose actual maps are

```math
A_j=V T O_j W
```

with known unitaries V and W common to all labels and to the scanned family of
losses/penalties. Preparing W-dagger times the ideal input and using decoder
D V-dagger exactly reproduces every ideal distribution. Normalization and the
incident signal budget are preserved. Hence the joint and calibrated fixed
optima are unchanged. A common downstream unitary also preserves the classical
map-contrast operator.

This is a single common basis correction, not a claim that the raw, uncalibrated
D must work. If V itself changes with the scanned loss setting, using a different
D V-dagger at each point is not literally one fixed physical receiver. Record
that distinction. Label-dependent basis corrections cannot be supplied to the
reader; they are genuine changes to the discrimination problem.

## 3. A conservative certificate for arbitrary small coherent-map errors

A passive contraction A induces the accessible one-photon channel

```math
\Gamma_A(\rho)=A\rho A^\dagger
\;\oplus\;\mathrm{Tr}[(I-A^\dagger A)\rho]|\mathrm{vac}\rangle\langle\mathrm{vac}|.
```

For contractions A,B with norm distance at most epsilon and a pure input,
put u=A psi and w=B psi. The surviving-block trace norm is at most 2 epsilon,
and the difference of survival probabilities is at most 2 epsilon. Including
vacuum and dividing by two gives trace distance at most 2 epsilon. Convexity
extends this bound to mixed inputs.

An observable with score range [-5,1] changes in expectation by at most six
times trace distance. Thus every fixed strategy changes by at most 12 epsilon,
and so does the optimized joint score. If the ideal fixed and joint optima both
equal beta_0, the perturbed device satisfies

```math
0\le\Delta\le\min\{1,24\epsilon\}.
```

A sharper a posteriori statement, given a feasible fixed score L_D, is

```math
\Delta\le\min\{1,\beta_0+12\epsilon\}-L_D.
```

Use a nonnegative lower score (always abstaining is available). These bounds
hold uniformly over the stated map envelope, not merely tested directions.
They are generally loose. For example, the generic sufficient radius for an
absolute score-regret allowance 0.01 is 0.01/24; this is not a recommended chip
specification. Structured bounds can be far more informative. The radius must
cover the device on held-out trials, not only an average fitted matrix.

For a common post-device channel L, data processing instead gives J(L after A0)
<= beta_0. Consequently Delta <= beta_0-L_D. A nonunitary L can genuinely destroy
information, so this upper regret bound may include both information loss and
receiver suboptimality. Do not present it as an attained regret.

## 4. Exact robustness to symmetric dephasing

Consider the same ideal phase code and diagonal loss, followed by the common
phase-noise channel

```math
\mathcal D_v(\rho)=v\rho+(1-v)\mathrm{diag}(\rho),\qquad 0\le v\le1.
```

Every off-diagonal coherence is multiplied by the same real factor v. For
independent zero-mean Gaussian path phases with identical variance sigma squared,
this model has v=exp(-sigma squared), provided the noise is independent of the
hidden label. This is an assumption on all pairwise coherences, not an arbitrary
single reported fringe visibility. A deterministic phase bias and fluctuating
phase noise are not interchangeable.

Let a_i=sqrt(eta_i). For the fixed score C-5E define

```math
B_v=\frac{3}{2} v\,aa^T-
\left(\frac{7}{2}+\frac{3}{2}v\right)\mathrm{diag}(\eta).
```

**Proposition.** The exact joint optimum is

```math
J=\max\{0,\lambda_{\max}(B_v)\}.
```

Whenever it is positive, the normalized positive top eigenvector z supplies
input probabilities p_i=z_i squared, and the same code decoder D attains it.
When the optimum is zero, always returning inconclusive attains it. Thus
Delta=0 throughout this model, including arbitrary positive unequal losses.

**Proof.** For arbitrary conclusive effects M_j, let
m_i=sum_j (M_j)_ii <=1 and q_i=eta_i p_i. The pure coherent term obeys the
baseline positivity/Cauchy-Schwarz estimate. The completely dephased term is
identical for all labels. Therefore

```math
C_{\rm ph}\le\frac{v}{4}
\left(\sum_i\sqrt{q_i m_i}\right)^2+
\frac{1-v}{4}\sum_iq_i m_i,
\qquad
C_{\rm ph}+E_{\rm ph}=\sum_iq_i m_i.
```

Set z_i=sqrt(p_i m_i); its norm is at most one. Substitution gives
S <= z-transpose B_v z <= max(0,lambda_max(B_v)). The vacuum is common to all
labels and a conclusive guess there has negative expected score, so it is
optimally inconclusive. The flat code measurement with the positive principal
eigenvector saturates both bounds, just as in the baseline argument. Input phases
may be absorbed into the receiver when deriving the bound; a real positive input
already attains it. Mixtures cannot improve a linear-score optimum. QED.

At this relatively severe error penalty, a positive score is possible exactly
when v>7/9. Indeed Cauchy-Schwarz bounds the score by
(9v/2-7/2) sum_i eta_i z_i squared, while inverse-loss weighting attains a positive
value when that coefficient is positive. This threshold is a property of the
chosen payoff, not the disappearance of every form of information in the device.

This is a direct extension of the already audited positivity proof. No independent
novelty or general noisy-optimality claim is made. Asymmetric coherence factors,
label-dependent fluctuations, arbitrary coherent biases, source contamination,
and a nonideal detector are not covered by this exact proposition.

Do not replace fluctuating maps by their mean amplitude matrix. Their output
states are averages of density matrices, not generally pure states constructed
from the averaged amplitudes. For the classical ceiling, a common subsequent
noise channel can conservatively be omitted by data processing.

## 5. A certified benchmark for diagonal phase-code errors

Small deterministic errors can leave losses diagonal while breaking code
orthogonality. More generally, suppose received photon-sector states have form

```math
\rho_j=P R_j P^\dagger,\qquad
P=\mathrm{diag}(\psi),
```

where all positive R_j have the same diagonal eta. Vacuum probability is then
label-independent for every input. For deterministic diagonal maps, R_j=g_j
g_j-dagger with g_j the vector of map diagonal entries. Symmetric dephasing is
another example of this structure.

Set W_j=(6 R_j-5 sum_k R_k)/4. On the score-positive branch the joint input and
measurement problem has the exact semidefinite formulation

```math
\max\sum_j\mathrm{Tr}(W_j X_j),
\quad X_j\succeq0,\quad
\sum_jX_j\preceq\mathrm{diag}(p),\quad
p_i\ge0,\quad\sum_ip_i=1.
```

The forward substitution is X_j=P-dagger M_j P. Conversely, choose input
sqrt(p) and divide X_j by sqrt(p) on its support to obtain a POVM; positivity
forces rows and columns with p_i=0 to vanish. Put unused support in failure.
This proves attainability in the original no-idler input class; no reference
system is being silently added. The unused vacuum can be discarded because its
best conclusive score is negative. Standard detector SDP methods predate this
study; the change of variables here states explicitly which joint model is
being optimized.

A particularly simple upper certificate is any Hermitian Y obeying

```math
Y\succeq0,\qquad Y\succeq W_j\quad\text{for all }j.
```

It implies J <= max_i Y_ii: apply the inequalities inside the trace and then
use sum p=1. The calculations store such a Y. Its five positivity conditions
are checked with exact rational LDL, not accepted merely from a solver status.
Feasible input/POVM factors separately supply lower scores. This certificate
construction is sufficient even if a numerical search terminates early.

For the fixed optics, each of four click records has five possible assignments:
one of four labels or failure. The common vacuum is always failure. A fixed
assignment has a four-by-four Hermitian score matrix Q_d; its optimum over all
complex inputs is lambda_max(Q_d). There are 5^4=625 deterministic assignments.
Randomized assignments and mixtures cannot exceed their largest optimum.
All 625 matrices are bounded by exact positivity of u I-Q_d at each reported
phase-error point. The lower score comes from an explicit normalized input.
Thus the phase-error regret intervals compare the full joint class with the
strong fixed-optics class, not just with one unoptimized preparation.

## 6. A small coherent phase error can require a different receiver

The illustrative systematic error changes the marked phase from pi to pi+delta:

```math
Z_\delta=J_4-(1+e^{i\delta})I.
```

The error is in the hidden phase operation, not a common phase that can be
cancelled before it. In the exact numerical models,
exp(i delta)=(1-q squared+2 i q)/(1+q squared), so delta=2 atan(q), with rational q.
This avoids pretending that rounded sine and cosine entries are an exact unitary.

At uniform transmission t, let x=sin(delta/2) squared. Uniform input and the
old decoder have feasible score

```math
S_D=t\left(1-\frac{9}{2}x\right).
```

At all the tabulated small phase errors, exact enumeration confirms that this
is the fixed-optics optimum up to its stated enclosure. This does not assert
that it remains optimal for every angle.

A concrete different four-mode unitary is obtained from the polar factor of
Z_delta. With P_b=J_4/4, its polar factor is

```math
U_\delta=
\frac{3-e^{i\delta}}{|3-e^{i\delta}|}P_b-
\frac{1+e^{i\delta}}{|1+e^{i\delta}|}(I-P_b).
```

Use receiver U_delta-dagger, uniform input, and discard vacuum. Its conditional
correct probability and unconditional score are

```math
p_c=\frac{[\sqrt{1+3x}+3\sqrt{1-x}]^2}{16},
\qquad S_{\rm changed}=t(6p_c-5).
```

For small delta, the old decoder loses score at order delta squared, while this
changed receiver loses only at order delta to the fourth. The formula is a
feasible receiver, not an assumption about a numerically found optimum. At the
screened uniform-loss points it nearly saturates the independent dual ceiling.
The positive lower regret intervals therefore establish genuine fixed-receiver
suboptimality. No multiple photons, nonlinear gate, or occupied auxiliary input
is needed for this example's changed receiver.

Correcting the phase bank itself can restore the intended ideal task instead.
If its systematic error cannot be corrected, the experiment should either accept
the bounded regret or state that its receiver must change; it must not continue
to assert exact ideal-code optimality on the wrong physical map.

## 7. Rotated loss is not merely a coordinate change

The additional-loss screen uses

```math
K=R\,\mathrm{diag}(1,1,1,1-d)R^\dagger,
\qquad A_j=K T O_j,
```

where R rotates paths 0 and 3 by a fixed angle 2 atan(1/10). A positive d attenuates
a superposition of paths. Unlike a common output unitary, this cannot be undone
without loss. Nonetheless it is a common downstream passive channel, so the
ideal beta_0 remains an upper bound on every input/measurement strategy. The
computed fixed-decoder score supplies a lower bound and hence a conservative
regret ceiling. This ceiling is not claimed tight and may include information
loss. At d=0.025 the extra power survival of that eigenmode is 0.950625.

## 8. What is and is not certified numerically

Exact model inputs are the recorded binary64 loss amplitudes interpreted as
rational numbers, rational unit-circle parameters, and rational dephasing
coefficients. All maps and score matrices are then complex rational. Displayed
transmissions such as 0.7 and 0.56 are rounded summaries of those models, not
claims of exact physical calibration. Perturbation bounds can separately cover
any discrepancy from a desired real-valued model or an actual calibrated device.

The LP cutting-plane method only proposes a matrix. Exact checks establish the
dual upper, feasible POVM completeness, primal score, and fixed-optics upper.
Reported rational endpoints are converted outward to binary64. The separate
verifier invokes no optimizer and reconstructs all witness inequalities.

The P1 illustration uses conventional floating-point exponentials and a
hypothetical perfect one-photon source with mean energy one and downstream
survival 0.92. It is explicitly a sensitivity screen, not a rounded-safe
statistical certificate. Source vacuum, multiphoton tails, dark clicks, drift,
phase-referenced calibration, and simultaneous confidence allowances have not
been supplied by a laboratory. No complete physical acquisition claim follows.

---

Preserved source: [original document](../studies/robustness-01/PROOFS.md).
