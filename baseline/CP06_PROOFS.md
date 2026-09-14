# Four-path phase-fault reading: derivations and certificates

Date: 2026-09-14. Status: analytic derivations with numerical consistency checks.
These are proposed results for the explicit model below, not a publication-level
priority claim. Standard unambiguous-discrimination and optical-reading methods
are inherited; see `SOURCE_AUDIT.md`.

## 0. Model and output contract

There are four signal paths. Exactly one path j in {0,1,2,3} undergoes a pi phase
flip, with uniform prior. Its mode operation is

\[
O_j=I-2|j\rangle\langle j|.
\]

Known, hypothesis-independent pure losses have transmissions eta_i in (0,1].
They act diagonally in the four paths, before an otherwise ideal decoder. Each
probe crosses the unknown phase section once. The losses commute with the phase
flips. Loss environments are inaccessible.

The receiver outputs one of four labels or an inconclusive symbol. Initially,
wrong conclusive answers are forbidden. Success means the unconditional mean
probability of a conclusive answer, not success conditioned on detection.

Quantum transmitter: exactly one photon in these four interrogated paths, with
no occupied bypass/reference rail or retained quantum idler. Known preparation
phases and vacuum ancillas at the receiver are permitted. Classical randomness
and knowledge of the selected preparation cannot improve the optimum derived
below. A broader quantum probe architecture is not upper-bounded here.

Classical transmitter: any nonnegative mixture of coherent states, with mean
signal photon number at most one at the input of the four interrogated paths.
An individual pulse may be brighter than one photon on average. The transmitter
may randomize intensity and allocation and retain a record of that choice. We
even grant that record to the receiver. Known coherent reference fields outside
the interrogated paths and an arbitrary quantum measurement are allowed. A
coherent reference is not charged to the sample-illumination budget. Thus this
is a bound on classical *probes*, not a restriction to classical detectors.

This counts incident signal photons, not laser-pump energy, source heralds,
calibration shots, latency, or total laboratory energy. Extra temporal signal
modes with the same four phase responses are covered by aggregating their
energies; repeated or adaptive device calls are not part of this single-use
model. Neither the preparation nor decoder controller receives j.

## 1. Exact four-mode single-photon optimum

Let J be the all-ones 4 by 4 matrix and

\[
D=J/2-I,\qquad S=J-2I=2D.
\]

D is a real unitary with D^2=I. The columns of S are the four sign patterns.
For a normalized probe with input probabilities p_i, phases can be absorbed into
known preparation/receiver phases. Write q_i=eta_i p_i. The four subnormalized
surviving states form the columns of

\[
\Phi=\operatorname{diag}(\sqrt{q_i})S.
\]

Their common vacuum probability is 1-sum_i q_i. Vacuum cannot support an
error-free conclusive outcome because it is compatible with every hypothesis.

### Fixed probe

For pure-state unambiguous discrimination, a vector of conclusive probabilities
s_j is feasible precisely when

\[
s_j\ge0,\qquad G-\operatorname{diag}(s_j)\succeq0,
\quad G=\Phi^\dagger\Phi.
\]

For nonsingular G, necessity follows by collecting the conclusive detection
amplitudes, and sufficiency follows by an isometry with a failure-state Gram
matrix G-diag(s). Singular limits follow by continuity. These are the standard
Gram-matrix conditions, not a new discrimination principle.

Here G=4D diag(q) D. Conjugating the PSD condition by D and taking diagonal
entries gives

\[
4q_i-\frac14\sum_j s_j\ge0.
\]

Therefore the uniform-prior success probability obeys

\[
Q(p)=\frac14\sum_j s_j\le4\min_i q_i.
\]

Choosing every s_j=4 min_i q_i is feasible, because the minimum eigenvalue of G
is 4 min_i q_i. Thus the fixed-probe optimum is exactly

\[
Q^*(p)=4\min_i\eta_i p_i.
\]

### Optimizing the preparation

If u=min_i eta_i p_i, normalization implies

\[
1=\sum_i p_i\ge u\sum_i\eta_i^{-1}.
\]

Equality is attained by inverse-transmission allocation:

\[
p_i=\frac{\eta_i^{-1}}{\sum_k\eta_k^{-1}},\qquad
H_\eta=\frac4{\sum_i\eta_i^{-1}}.
\]

Hence

\[
\boxed{Q_{\mathrm{1ph}}^*=H_\eta.}
\]

In this preparation every surviving path amplitude has magnitude sqrt(H_eta)/2.
The fixed decoder D consequently gives

\[
D\,\operatorname{diag}(\sqrt{\eta_i})O_j|a\rangle
=\sqrt{H_\eta}|j\rangle.
\]

Four threshold detectors suffice in the ideal one-photon model: a click gives
the correct label; no click is inconclusive. This is not recovery of lost
photons. The photon survives with probability H_eta.

Classical mixtures of preparations cannot improve this value because each
component, even with a receiver-visible label, is bounded by H_eta.

### Simple optical factorization

With the ordinary Hadamard matrix H_2,

\[
D=(H_2\otimes H_2)\operatorname{diag}(1,-1,-1,-1)(H_2\otimes H_2).
\]

The tensor notation labels paths and does not assert multiple physical photons.
It gives two balanced-coupler layers on either side of three phase shifts. A
four-mode universal mesh can instead compile D directly. A global phase can be
chosen to match an SU(4) convention.

## 2. Exact optimum for a fixed coherent illumination

Let n_i be the input energies, q_i=eta_i n_i the transmitted energies, and

\[
a_i=e^{-2q_i}.
\]

The four returned coherent states have Gram matrix

\[
G_{jj}=1,\quad G_{jk}=e^{-2(q_j+q_k)}\ (j\ne k),
\]

or

\[
G=\operatorname{diag}(1-a_i^2)+aa^T.
\]

Unknown optical phases are not averaged here. Relative phases in the input
amplitudes cancel from these pairwise inner products. Known bypass references
are identical under the four hypotheses and do not change G.

Define

\[
\delta=\max\{2\max_i a_i-\sum_i a_i,0\}.
\]

Then the optimal uniform-prior error-free conclusive probability is

\[
\boxed{F(q)=\frac{4-\sum_i a_i^2+\delta^2}{4}.}
\]

The following primal and dual certificates prove the formula without an SDP
solver.

### Case A: delta = 0

Use s_i=1-a_i^2. The residual Gram matrix is aa^T, which is PSD.
Since the four lengths a_i form a closed quadrilateral, choose complex numbers
z_i of modulus one such that sum_i a_i z_i=0. Then

\[
Y=zz^\dagger/4\succeq0,\qquad Y_{ii}=1/4.
\]

For any feasible s,

\[
\tfrac14\sum_i s_i\le\operatorname{Tr}(GY).
\]

The right side is (4-sum_i a_i^2)/4 and equals the primal success.

This case is physically achievable by displacing the known unflipped coherent
background. Under hypothesis j, only mode j then contains a nonzero displacement,
with energy 4q_j. A click identifies j; no click is inconclusive. The rate is
one quarter of sum_j (1-exp(-4q_j)). This use of coherent displacement is already
established receiver methodology.

### Case B: delta > 0

Let m index the largest a_i, and let T=sum_{i != m}a_i. Then delta=a_m-T.
Use failure probabilities

\[
f_m=a_mT,\qquad f_i=a_i^2+\delta a_i\ (i\ne m),\qquad s_i=1-f_i.
\]

All s_i are nonnegative and at most one. To check the residual G-diag(s), take
the Schur complement of its m,m entry a_m T. The remaining block is

\[
\delta\left[\operatorname{diag}(a_i)_{i\ne m}
-\frac{a_{\bar m}a_{\bar m}^T}{T}\right]\succeq0,
\]

by weighted Cauchy-Schwarz. Zero limits are obtained continuously.

For the dual, choose z_m=1 and z_i=-1 for the other indices. Y=zz^T/4 is PSD with
diagonal 1/4, and

\[
\operatorname{Tr}(GY)=\frac{4-\sum_i a_i^2+\delta^2}{4}
=\frac14\sum_i s_i.
\]

This high-energy case can outperform simple displacement-and-click detection.
Ignoring it would leave a loophole for bright-pulse classical transmitters.

## 3. Three equal paths and one weaker path

Now specialize to

\[
\eta=t(1,1,1,r),\quad 0<t\le1,\quad 0<r\le1.
\]

For a pure coherent pulse with incident energy N, set x=tN. The output energies
have cost sum_{good}q_i+q_bad/r=x.

### 3.1 Best displacement receiver

The concave allocation problem maximizes one quarter of
sum_i (1-exp(-4q_i)) subject to the energy cost. Its Kuhn-Tucker conditions yield
water filling. Define

\[
B_r(x)=
\begin{cases}
\frac34(1-e^{-4x/3}), & r\le e^{-4x/3},\\[2mm]
1-\frac14(3+1/r)\lambda, & r>e^{-4x/3},
\end{cases}
\]

where in the second branch

\[
\lambda=\exp\left(\frac{\ln r-4rx}{1+3r}\right).
\]

The derivative B'_r(x) equals e^{-4x/3} in the first branch and lambda in the
second. B_r is concave. In the first branch, the optimum does not illuminate the
worst path. The average criterion permits unequal per-hypothesis success.

In physical units the incident allocation is

\[
n_i=\max\{\ln(\eta_i/\Lambda)/(4\eta_i),0\},\qquad\sum_i n_i=N.
\]

For arbitrary unequal transmissions, this receiver is an achievable classical
rate only. The theorem below proves exactness for the declared one-bad-path
family at the required mean budget.

### 3.2 Pure coherent optimum at arbitrary energy

Let x_c=(3/2) ln 3 and

\[
E_3(x)=1-\frac32e^{-2x/3}+\frac32e^{-4x/3}.
\]

The exact pure-coherent optimum is

\[
F_r^*(x)=
\begin{cases}
B_r(x),& x\le x_c,\\
\max\{B_r(x),E_3(x)\},& x\ge x_c.
\end{cases}
\]

Proof: F(q) is symmetric in the q_i, so the smallest q_i can be assigned to the
worst path without increasing cost. If delta=0, the objective is the concave
nulling expression and is bounded by B_r(x).

If delta>0, the largest a_i belongs to the worst path. Write it as a_0 and the
other three amplitudes as a_1,a_2,a_3. In this sector,

\[
F=1-\frac{a_0(a_1+a_2+a_3)}2
+\frac{a_1a_2+a_1a_3+a_2a_3}{2}.
\]

Averaging two good-path energies preserves cost, decreases their amplitude sum,
and leaves delta positive. Write their amplitudes as a exp(u), a exp(-u), and
the remaining good amplitude as b. The part varying with u is
-a(a_0-b)cosh(u), maximized at u=0. Iterating gives equal good-path energies.

Write their common energy as (x-z)/3 and the bad-path energy as rz. Then

\[
a=e^{-2(x-z)/3},\qquad a_0=e^{-2rz},\qquad
F=1-\tfrac32a_0a+\tfrac32a^2.
\]

The delta-positive interval is

\[
0\le z<\frac{x-x_c}{1+3r},
\]

so it exists only for x>x_c. Its derivative is

\[
\frac{dF}{dz}=a_0a\,[\,-1+3r+2a/a_0\,].
\]

The bracket increases with z. Any stationary point is a minimum, not a maximum.
An optimum is therefore at z=0, which gives E_3(x), or at delta=0, where its value
is bounded by B_r(x). Both branches are achievable. This proves the formula.
For r=0, use the continuous limit; wasting photons in the erased path cannot
help.

### 3.3 Bright flashes do not improve the mean-one-photon benchmark

A mean budget is not a per-pulse peak constraint. To cover arbitrary classical
mixtures, it is necessary to optimize the concave envelope of F_r^*(x), not only
evaluate the pure optimum at its mean.

Let 0<m<=1 be the allowed mean effective energy. The tangent

\[
L_r(x)=B_r(m)+B'_r(m)(x-m)
\]

dominates F_r^*(x) for every x>=0.

It dominates B_r by concavity. For the extra branch, x>=x_c>1. Define
B_0(x)=(3/4)(1-exp(-4x/3)). Directly from the allocation formulas,
B_r(m)>=B_0(m) and B'_r(m)>=B'_0(m). Hence L_r(x) is no smaller than the tangent
to B_0 at m. Because B_0 is concave and x>=1>=m, that tangent is no smaller than
the tangent at 1.

At x=x_c, the latter tangent exceeds E_3(x_c)=2/3 by

\[
\frac1{12}+e^{-4/3}(x_c-7/4)>0.
\]

For example, x_c>3/2 and e^{-4/3}<1/3 already prove positivity. For all x>=x_c,

\[
E_3'(x)=a-2a^2\le1/8,
\quad a=e^{-2x/3},
\]

while the tangent has slope exp(-4/3)>1/4. It remains above E_3 forever.

For an arbitrary labelled mixture of coherent pulses, average the supporting
line. If E[x]<=m, its mean conclusive rate is at most B_r(m). A fixed water-filled
coherent pulse attains this value. Thus with m=t and mean incident energy <=1,

\[
\boxed{Q_{\mathrm{classical}}^*=B_r(t).}
\]

The proof includes unbounded rare bright pulses, arbitrary input allocations,
known optical phase references, and arbitrary receivers. It does not rely on
phase-randomizing the coherent source. It does not make an asymptotic or
multi-use capacity claim.

## 4. Exact loss-imbalance crossover

The single-photon rate in this family is

\[
Q_{\mathrm{1ph}}^*=\frac{4tr}{1+3r}.
\]

Set

\[
b(t)=\frac34(1-e^{-4t/3}),\qquad
r_*(t)=\frac{b(t)}{4t-3b(t)}.
\]

For 0<t<=1, the quantum rate exceeds the classical rate precisely when r>r_*(t).
Equality holds at r_*. For r<r_*, the classical probe has a larger no-error
conclusive rate than any single-photon probe in the specified four-path space.

Here is a proof that the crossing lies in the inactive-bad-arm branch and is
unique. At its boundary r_0=exp(-4t/3), the sign of the quantum-minus-classical
rate is the sign of

\[
g(r_0)=-4r_0\ln r_0-(1-r_0)(1+3r_0).
\]

On [1/4,1], g has a single interior maximum and no interior minimum:
g'(r)=6r-6-4ln r, and g''(r)=6-4/r changes sign once. Moreover,
g(1)=0 and g(1/4)=ln4-21/16>0. Since r_0>=exp(-4/3)>1/4, g(r_0)>=0.
The difference starts negative at r=0 and is strictly increasing in the
inactive branch, giving the stated r_* there.

For the active branch, let d=1+3r, h=4r/d, and A=lambda/h. Its derivative is

\[
\frac{d}{dr}\left[\frac{4tr}{1+3r}-B_r(t)\right]
=\frac{4t(1-A)-3A\ln r}{d^2}\ge0.
\]

To see A<=1, the active-branch condition gives lambda<=r, whereas h>=r.
Therefore no second crossing occurs. This is a model-specific reversal, not a
claim about every quantum probe architecture or every error criterion.

## 5. Allowing a small wrong-answer probability

Exact zero error is an ideal benchmark. Let C denote the unconditional average
correct-conclusive probability, E the wrong-conclusive probability, and
F=1-C-E the inconclusive probability. Suppose every path transmission is <=t.
For any classical coherent mixture with mean signal energy <=mu,

\[
\boxed{
C\le\min\left\{1-E,
\left[\sqrt{1-e^{-t\mu}}+\sqrt{E/3}\right]^2\right\}.
}
\]

This bound can be loose for unequal losses. It provides a finite-error
classical ceiling rather than assuming perfect zero-error detection.

Proof for a pure pulse: let total returned energy be Q. Its six pairwise
state overlaps obey Jensen's inequality,

\[
\sum_{j<k}|\langle\alpha_j|\alpha_k\rangle|
=\sum_{j<k}e^{-2(q_j+q_k)}\ge6e^{-Q}\ge6e^{-tN}.
\]

For any measurement, Cauchy-Schwarz bounds each state overlap by the classical
fidelity of its outcome distributions. Aggregate arbitrary decision records
into four conclusive labels and an inconclusive symbol. At a conclusive output,
write its correct contribution as d and the sum of its three wrong contributions
as w. The pair-fidelity contribution is at most sqrt(3dw)+w. Summing conclusive
outputs yields at most 4sqrt(3CE)+4E. The inconclusive contribution is at most
6F. Therefore

\[
6e^{-tN}\le6F+4\sqrt{3CE}+4E.
\]

Substituting F=1-C-E gives

\[
(\sqrt C-\sqrt{E/3})^2\le1-e^{-tN},
\]

and hence the claimed pure-pulse upper bound. The function
A+E/3+2sqrt(AE/3) is concave and increasing in A, while A=1-exp(-tN) is concave in
N. Jensen's inequality proves the same bound for arbitrary labelled mixtures
at the mean budget. Independently, C<=1-E.

Known common post-channel noise cannot improve the classical score, so the
ceiling remains valid when the ideal coherent outputs undergo a common noisy
channel. A noise label depending on the hidden hypothesis would instead change
the access model.


### Check of the low-error boundary in the uniform case

For uniform transmission t and equal coherent input energies, put c=exp(-t).
The Gram matrix has eigenvalues 1+3c and 1-c. Let the desired conclusive detection
amplitude matrix have diagonal sqrt(C) and off-diagonal sqrt(E/3). Its squared
eigenvalues are (sqrt(C)+sqrt(3E))^2 and (sqrt(C)-sqrt(E/3))^2. It is feasible
when these are no larger than the corresponding Gram eigenvalues.

Choosing

\[
C=[\sqrt{1-c}+\sqrt{E/3}]^2
\]

saturates the latter condition. The former remains satisfied for

\[
0\le E\le\frac3{16}[\sqrt{1+3c}-\sqrt{1-c}]^2.
\]

Thus the bound is not merely vacuous near zero error: it is attainable in this
symmetric interval. The code constructs the POVM by multiplying the conclusive
amplitude matrix by G^{-1/2} and verifies positivity of the failure effect.
This is a certificate for the formula, not a claim that error-margin symmetric
state discrimination is a new topic.

### An illustrative phase-error screen

For the loss-compensated single-photon probe, suppose each of the four paths
has an independent Gaussian phase error of variance sigma^2, distributed
independently of the hidden fault. Then

\[
C_q=H_\eta(1/4+3e^{-\sigma^2}/4),\quad
E_q=3H_\eta(1-e^{-\sigma^2})/4,\quad
F_q=1-H_\eta.
\]

The common random phase channel only degrades the outputs. For
eta=(0.7,0.7,0.7,0.56) and sigma=0.05 radians:

- correct conclusive: 0.6575897781;
- wrong conclusive: 0.0012337513;
- inconclusive: 0.3411764706;
- classical upper bound at that error and mu=1: 0.5326029868.

These are model calculations, not measured hardware performance. Detector
false clicks, source impurity, calibration uncertainty, and hypothesis-dependent
loss require explicit treatment. Empirical use of the ceiling requires
confidence bounds on C, E, the illumination budget, and transmissions.

## 6. Scope and evidence status

The identities above are analytic arguments. `src/validate.py` supplies separate
matrix, full-loss-space, coherent photon-sector, primal-dual, optimization,
mixture-LP, and phase-quadrature checks. The finite tests are not the proof of
universal claims. No SDP solver, interval arithmetic, hardware experiment, or
full literature-priority certification was performed.

Known ingredients include Hadamard optical reading, phase-oracle discrimination,
Gram-matrix unambiguous discrimination, coherent displacement receivers, and
concave energy allocation. The potentially distinctive contribution is the
exact nonuniform-loss comparison (including the bright-flash envelope) and its
explicit operational boundary. That contribution remains subject to a deeper
predecessor comparison before any novelty claim or lab-ready project freeze.
