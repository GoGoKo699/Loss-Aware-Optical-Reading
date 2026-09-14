# Equation-level reductions and remaining scope differences

This note compares the repaired baseline `80c73751806f45411251711bcfb6bccebc887f0a`
with the primary sources indexed in [SOURCES.md](SOURCES.md). It is a novelty
comparison, not an assertion that every useful special case needs to be new.
The derivations below are our translations. They do not reproduce external prose.
A numerical match supports a translation; it does not establish priority.

## R1. The fixed decoder is the established square-root measurement

Use the baseline conventions: a flat orthogonal phase matrix Z, m equally likely
labels, q_i = eta_i p_i > 0, and surviving state columns

$$
\Phi=\mathrm{diag}(\sqrt q)Z,\qquad U=Z/\sqrt m.
$$

The surviving Gram matrix and its square root are

$$
G=mU^\dagger\mathrm{diag}(q)U,
\qquad
\sqrt G=\sqrt m U^\dagger\mathrm{diag}(\sqrt q)U.
$$

Because all entries of U have modulus 1/sqrt(m), every diagonal element of
sqrt(G) is the same. The constant-diagonal square-root criterion in Eldar and
Forney [S04, Sec. 8.3] therefore applies. Common normalization by survival does
not change the receiver. Direct multiplication gives

$$
\Phi G^{-1/2}=U.
$$

The measurement vectors are the columns of U, so the optical receiver is U-dagger.
Its unconditional correct photon probability is

$$
C_{\rm ph}=\frac1m\left(\sum_i\sqrt{q_i}\right)^2.
$$

This identification covers complex Hadamard matrices without assuming that their
columns form a cyclic group orbit. It establishes a known minimum-error receiver
for a *given input*. It does not by itself establish the jointly optimized
finite-error input theorem. The common vacuum supplies a further classical
random-guess/abstain choice; it cannot encode the hidden label.

**Classification:** known measurement specialized to this code. Do not claim a
new decoder or a newly discovered square-root measurement principle.

## R2. The harmonic-mean endpoint is a short unambiguous-discrimination corollary

Chefles and Barnett [S02, Eq. (3.15)] give the minimum-coefficient rule for
linearly independent symmetric states. Fourier codes are directly in that class.
For the arbitrary flat code, the same conclusion follows from standard Gram
feasibility [S10; S13; S12 Appendix B] as follows.

If s_j are the unconditional success probabilities for error-free conclusive
outcomes, then G - diag(s_j) is positive semidefinite. An eigenvector of G
associated with its eigenvalue m min(q_i) has uniform squared entries 1/m.
Evaluating the positive residual on that vector yields

$$
\frac1m\sum_j s_j\le m\min_i q_i.
$$

Taking every s_j = m min(q_i) attains the bound. This argument does not assume
equal individual success as a restriction on the optimization.

Optimizing min(eta_i p_i) with sum(p_i)=1 is elementary: if eta_i p_i >= a for
all i, then a sum(1/eta_i) <= 1. Equality gives

$$
p_i=\frac{\eta_i^{-1}}{\sum_k\eta_k^{-1}},
\qquad C^*_{E=0}=\frac{m}{\sum_i\eta_i^{-1}}.
$$

**Classification:** direct specialization for Fourier/symmetric codes, elementary
Gram extension for other flat codes, followed by a normalization corollary.
It is a useful physical rule but should not carry the paper alone.

## R3. What is additional in input-only retuning

Error/inconclusive optimization and filter-then-minimum-error decompositions
are established [S07, S08]. Joint optimization over a probe and its measurement
under an error margin is also an established task [S05, Sec. II]; optimization
of loss-aware optical probes is not a new principle [S06]. The comparison must
therefore identify the *particular reduction*, not the general type of task.

For arbitrary conclusive photon-sector effects M_j, define

$$
w_i=\sum_j(M_j)_{ii}\le1,\qquad z_i=\sqrt{p_iw_i}.
$$

The repaired proof's positivity/Cauchy-Schwarz argument yields

$$
S_{\rm ph}\le z^TB_\lambda z,
\quad B_\lambda=\frac{1+\lambda}{m}vv^T-\lambda\mathrm{diag}(\eta),
\quad v_i=\sqrt{\eta_i}.
$$

Set a = sum(p_i w_i). If a>0, use the normalized replacement input

$$
p_i'=p_iw_i/a.
$$

The fixed code decoder on that replacement input has score

$$
S'=z^TB_\lambda z/a.
$$

When z^T B z is nonnegative, a<=1 means the replacement does at least as well
as the arbitrary measurement's upper estimate. If the upper estimate is negative,
an always-inconclusive strategy already does better. For lambda >= 1/(m-1),
conclusive guesses on the common vacuum cannot help. A positive harmonic-mean
strategy exists, so the global optimum is on the nonnegative branch.

This explains why a receiver's possible filtering advantage can be absorbed into
the input optimization in this specific code/loss model. It is **not** an equality
of the old and new quantum channels, not reversal of attenuation, and not a free
renormalization of detected data. A physically different normalized input is
prepared *before* interrogation, without knowing the hidden label.

The remaining normalized optimization is the largest eigenvalue of B_lambda.
Its positivity makes the optimal input explicit and unique. The minimum-error
endpoint and vacuum-guessing segment complete the frontier as in the canonical
proof. None of these steps requires modifying that proof here.

A known optimal POVM for a *fixed received ensemble* does not automatically give
this result. One must account for how changing p changes both that ensemble and
the probability of erasure, and must optimize over arbitrary possible effects
rather than only the selected code measurement.

**Classification:** a potentially distinct, narrowly stated joint-design reduction
built from standard discrimination arguments. This audit did not locate an exact
statement with all these assumptions in the passages reviewed. This is not proof
that it is absent everywhere. The proof is compact; do not describe it as a new
universal optimization architecture.

## R4. The uniform fixed-alphabet curve is exactly Herzog's formula

In Herzog [S07, Sec. IV.B, Eq. (4.18)], take N=4, positive real common overlap
S=c, and identify her inconclusive probability Q with our F. Her expression on
0<=F<=c becomes

$$
C(F)=\frac14\left[
\sqrt{\frac{1+3c}{4}-F}+3\sqrt{\frac{1-c}{4}}
\right]^2.
$$

Set E=1-F-C. Algebra on this physical branch gives

$$
\sqrt C-\sqrt{E/3}=\sqrt{1-c},
\qquad
C=(\sqrt{1-c}+\sqrt{E/3})^2.
$$

For the balanced coherent alphabet in the repository, c=exp(-t mu). At F=0,

$$
C_{\rm ME}=\frac{[\sqrt{1+3c}+3\sqrt{1-c}]^2}{16}.
$$

At F=c, C=1-c and E=0. The zero-energy case is its limiting random-guess rule.
The fixed error budget stops improving C after the minimum-error endpoint.
These are the repository's formulas, not merely qualitatively similar curves.

**Classification:** direct fixed-alphabet specialization/reparameterization.
The statement that this same curve is optimal over *all allowed coherent
transmitters and their arbitrary mean-energy mixtures* still needs the separate
optical converse. Herzog's fixed-state theorem does not assert that transmitter
optimization. Counting the known curve itself and its square-root POVM as new
would be incorrect; discarding the all-source result solely because the curve
is known would also be incorrect.

## R5. Nulling the one-flip alphabet gives an established PPM receiver

For incident amplitude alpha_i and transmitted mean q_i=eta_i|alpha_i|^2, the
unflipped returned background is b_i=sqrt(eta_i) alpha_i. Hypothesis j returns
b-2b_j e_j. A displacement by -b maps it to a pulse only in mode j, with
amplitude -2b_j. The displacement depends on known background/calibration, not j.
The associated source-independent coherent-state phases cancel for this real
sign-flip family, and the Hilbert-space Gram matrix is

$$
G_{jk}=e^{-2(q_j+q_k)}\ (j\ne k),\qquad G_{jj}=1.
$$

This is the Gram matrix of unequal-energy pulse-position modulation. Equal-energy
PPM nulling/click optimality and related equivalent displaced alphabets are
established [S12, Sec. 5.1, Eqs. (48)-(52); Sec. 5.2, Eq. (53)]. This also explains
the coherent benchmark's optical simplicity. It is not a new displacement trick.

For the *nulling receiver alone*, optimizing

$$
\frac14\sum_i(1-e^{-4\eta_i n_i}),\qquad n_i\ge0,\quad\sum_i n_i=N
$$

is concave resource allocation. The KKT rule is

$$
n_i=\frac{[\log(\eta_i/\Lambda)]_+}{4\eta_i}.
$$

Abandonment of a sufficiently weak path is a standard active-set consequence of
that allocation. The KKT rule by itself does not optimize every coherent-state
POVM, much less intensity randomization.

## R6. The binary spectral contrast is already in optical discrimination

Bouchet and colleagues [S11, Eqs. (1)-(3)] define the binary discrimination
operator

$$
D_{12}=(A_2-A_1)^\dagger(A_2-A_1)
$$

and optimize coherent input wavefronts using its largest eigenvector. In the
repository at m=2,

$$
H_\Delta=D_{12}/2,
\qquad \kappa=\lambda_{\max}(D_{12})/2.
$$

For equal priors and an incident pulse energy N, the achievable binary Helstrom
success becomes

$$
P_{\rm ME}=\frac12\left[1+\sqrt{1-e^{-2\kappa N}}\right].
$$

Thus the spectral contrast is not new in the binary case. Pairwise overlap/fidelity
bounds are themselves standard [S10, S14, S19], and the unambiguous multi-state
pairwise-overlap bound is attributed to S20 in S19's Sec. II. S20's complete text
was not recovered in this audit; that attribution is explicitly second-hand
through another primary research paper, not a claimed direct reading.

For m>2, the repository replaces the binary operator by an average of pair
contrasts. Its top eigenvector is **not** proved generally to optimize the actual
multiclass decision; the operator is used in a converse. Positivity of measurement
probabilities gives, for average root overlap R,

$$
R\le F+2\sqrt{CE/(m-1)}+\frac{m-2}{m-1}E.
$$

Coherent overlaps and Jensen give R>=exp(-kappa N). A second concavity step
extends the resulting upper bound to arbitrary labelled classical mixtures at
mean mu. Reference states common across hypotheses after the mixture label is
given do not increase distinguishability.

**Classification:** potentially distinct multiclass optical composition and
calibration-oriented certificate, not a new fidelity inequality, binary
wavefront-selection principle, or general exact multiclass optimum. The m=4
uniform alphabet saturates the bound, which adds an optical source-class converse
to R4. The general-map bound is not asserted to be attainable.

## R7. Why the checkpoint-06 global comparison is more than water filling

The structured four-state Gram matrix has the form

$$
G=\mathrm{diag}(1-a_i^2)+aa^T,\qquad a_i=e^{-2q_i}.
$$

The repository's fixed-pulse optimum is

$$
P_{\rm USD}^*(q)=\frac{4-\sum_i a_i^2+\delta^2}{4},
\qquad \delta=\max(0,2\max_i a_i-\sum_i a_i).
$$

The underlying feasibility optimization G-diag(success)>=0 is established
[S10, S13, S12 Appendix B]. S13 solves nontrivial asymmetric three-state regimes;
this audit did not identify its formula as a direct statement of the above
four-state factorized case. Treat this as a specialized closed form on an old
optimization problem, not a new theory of unambiguous discrimination.

There is an operational distinction that a comparison cannot omit. At effective
energy x=3 with one weak-to-good transmission ratio r=.01, the optimized
background-nulling strategy gives approximately .736263. The delta>0 POVM gives
.824471, and explicit Gram residual positivity verifies its feasibility. Therefore
optimality of the simple nulling receiver at every pulse energy is false.

The checkpoint-06 all-source mean-budget theorem must bound this second branch
as well. Its separate supporting-line argument at mean effective energy <=1
does so analytically for the stated one-bad-path family; a finite scan cannot
replace that argument. The exact crossover with the harmonic-mean photon rate
then follows algebraically from two optimized scores.

**Classification:** the complete fixed-pulse/mean-budget converse and resulting
specific boundary remain candidate technical contributions in the bounded source
comparison. The receiver design, KKT allocation, and the general existence of
loss-dependent reversals are not independently new. In particular [S09, Sec. V]
already discusses how loss changes preferred photon-number probes.

## R8. Calibration and statistical wrappers

Stacking all map differences and applying the triangle inequality yields the
reported operator-radius allowance. The score's trace-distance perturbation bound
is an application of the range of a bounded payoff [compare S14, Appendix F].
The fixed-N radius is the ordinary bounded-variable exponential-moment argument;
calibration failure probabilities combine by a union bound. Its exact-rational
scalar-root enclosure is a conventional certified numerical implementation.

These are necessary safeguards and useful reproducibility work, not separate
new physical theorems. No anytime-valid conclusion follows from the fixed-N test;
[S21] addresses a different, stronger statistical setting. Likewise the quantum
Hoeffding exponents in [S17] are not the scalar Hoeffding concentration radius
used on our trial log.

## Executed checks and their limits

`comparison_checks.py` verifies R1-R7 identities on pinned source inputs. It
checks complex Fourier and nontrivial complex Hadamard cases, the Herzog change
of variables, the binary factor of two, normalized input/filter scores, PPM
Gram equivalence, and an explicit high-energy non-nulling example.

631 scalar consistency checks passed at the declared 1e-9 tolerances. The maximum
residual was about 2.71e-10 at a near-zero-error Herzog endpoint where binary64
subtraction precedes a square root. A second fresh-directory execution reproduced
the entire results file byte for byte. This is not an interval or formal proof,
not a global energy scan, and not evidence that no predecessor exists.
