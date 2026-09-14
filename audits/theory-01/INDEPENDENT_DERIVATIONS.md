# Independent reconstruction of the theory and certificate

Audit target: `d07e4e2180992ab52ee08d0a0cad689154d2e9bd`.
This note checks the mathematical contracts in `proofs/THEORY.md`; it does not
assert novelty. The arguments below are the audit's reconstruction. Numerical
examples in `diagnostics.py` supplement these arguments and do not replace them.

## 1. Input and measurement class

There are m >= 2 uniformly likely, independently chosen labels per interrogation.
The photon is confined to the m interrogated paths. The receiver may use any
POVM after the specified channel, but not the inaccessible loss environment.
No occupied bypass rail, retained idler, extra device call, or coherence between
vacuum and one photon is added to the photon optimization.

Let Z have unit-modulus entries and Z-dagger Z = m I. Let eta_i be strictly
positive transmissions at most one. For a pure input with amplitudes a_i,
known input phases can be removed by a common diagonal receiver unitary. Write
p_i=|a_i|^2 and q_i=eta_i p_i. The accessible output for label j is

$$
\rho_j=|\phi_j\rangle\langle\phi_j|+(1-s)|\mathrm{vac}\rangle\langle\mathrm{vac}|,
\qquad (\phi_j)_i=\sqrt{q_i}Z_{ij},\quad s=\sum_i q_i.
$$

The common vacuum component is label independent. Since the states are block
diagonal, pinching a POVM in photon/vacuum number leaves all its probabilities
unchanged. Cross-number measurement terms cannot help. A mixed input can be
decomposed into pure inputs; supplying its decomposition label to the receiver
only enlarges its capabilities. A componentwise upper bound therefore covers
unlabelled mixtures and allowed classical randomization as well.

This restriction is substantive: a different quantum input architecture would
need a different theorem. The negative comparison is not an exclusion of all
quantum illumination.

## 2. Photon score: global bound and matching receiver

Let M_j be the photon-sector conclusive effects, with sum_j M_j <= I. Set
h_i=sum_j (M_j)_ii. For each positive M_j,

$$
|(M_j)_{ik}|\le\sqrt{(M_j)_{ii}(M_j)_{kk}}.
$$

Cauchy-Schwarz across the labels then gives

$$
C_{\rm ph}\le\frac1m\left(\sum_i\sqrt{q_i h_i}\right)^2,
\qquad C_{\rm ph}+E_{\rm ph}=\sum_i q_i h_i.
$$

The equality on the right follows from the row orthogonality of the square
matrix Z. It does not require a group-covariance assumption.

Put u_i=sqrt(p_i h_i), v_i=sqrt(eta_i). Then ||u|| <= 1 and

$$
C_{\rm ph}-\lambda E_{\rm ph}\le u^T B_\lambda u,
\qquad B_\lambda=\frac{1+\lambda}{m}vv^T-\lambda\,\mathrm{diag}(\eta).
$$

The largest eigenvalue beta is positive: the normalized vector proportional to
1/sqrt(eta_i) gives the strictly positive harmonic-mean score. A conclusive
vacuum decision contributes its conclusive probability times
[1-(m-1)lambda]/m. Thus, for lambda >= 1/(m-1), it is never helpful. This proves
the global score bound beta, including all POVMs and all allowed mixtures.

The off-diagonal entries of B are positive. After adding a sufficiently large
multiple of I, Perron-Frobenius gives a unique positive normalized top vector z.
Choose p_i=z_i^2 and effects given by columns Z_:j/sqrt(m), equivalently decoder
Z-dagger/sqrt(m). Each correct amplitude is sum_i sqrt(eta_i p_i)/sqrt(m), and
all surviving photons receive a label. The resulting score is beta. Thus the
same fixed decoder attains the bound after retuning the input.

### A separate dual check for the attaining input

Set a=(1+lambda)/m. The optimality equation implies

$$
a\sum_i\frac{\eta_i}{\beta+\lambda\eta_i}=1,
\qquad
p_i\propto\frac{\eta_i}{(\beta+\lambda\eta_i)^2}.
$$

For this input, the discrimination payoff operators are

$$
R_j=a|\phi_j\rangle\langle\phi_j|-\lambda\,\mathrm{diag}(q).
$$

The dual candidate Y=beta diag(p) has trace beta and is positive. Its feasibility
Y >= R_j follows from the diagonal-minus-rank-one criterion and the scalar
identity above. This independently checks measurement attainment for the chosen
input. It is not, by itself, the global input upper proof; the preceding bound
is needed for that step.

The audit's numerical dual calculation does not restrict Y to be diagonal. It
solves a full Hermitian spectral-cut relaxation, then adds an explicit identity
shift and checks every matrix constraint. The vacuum block is separated by the
justified pinching argument, not silently omitted.

## 3. Completeness of the photon frontier

Let lambda_0=1/(m-1). Below lambda_0, replacing an inconclusive event by a uniform
random answer changes the score by a nonnegative amount. An optimum may therefore
always answer. The minimum-error success probability is

$$
P_{\rm ME}=\frac{1+\lambda_{\max}(vv^T-\mathrm{diag}(\eta))}{m}.
$$

It follows that beta(lambda)=(1+lambda)P_ME-lambda on [0,lambda_0]. At lambda_0,
retain the optimal photon measurement and vary only the probability of guessing
on vacuum events. This produces the straight segment with dC/dE=1/(m-1).

For lambda>lambda_0, the simple top eigenvalue is differentiable and
beta'(lambda)=-E(lambda). Second-order eigenvalue perturbation gives

$$
\beta''(\lambda)=2\sum_{k\ne 0}
\frac{|\langle u_k|B'|z\rangle|^2}{\beta-\beta_k}\ge0.
$$

For unequal positive transmissions the inequality is strict. If it vanished,
z would be a common eigenvector of B and B'. Hence it would be an eigenvector
of vv^T with a nonzero eigenvalue, so z is proportional to v. Requiring B'v to
be proportional to v forces every eta_i to be equal. Thus unequal-loss E(lambda)
is continuous and strictly decreasing, rather than merely nonincreasing.

Finally,

$$
z^T B'z=\frac{(v^Tz)^2}{m}-\sum_i\eta_i z_i^2\le0,
$$

with equality only when sqrt(eta_i)z_i is constant. As lambda increases, the
maximizer approaches this null direction, giving p_i proportional to 1/eta_i,
E=0 and C=m/(sum_i 1/eta_i). This supplies the zero-error limit. Together these
arguments fill the intermediate range and justify the complete support formula

$$
C_q^*(\epsilon)=\inf_{\lambda\ge0}[\beta(\lambda)+\lambda\epsilon].
$$

Uniform transmission is the degenerate case: the curved segment is absent.
No generalization to nonorthogonal codes, unequal priors, zero transmissions,
or multiple interrogations is used.

## 4. Coherent-state benchmark without an energy cutoff

Let the actual accessible coherent outputs be |A_j alpha>. For one pulse with
N=||alpha||^2,

$$
|\langle A_j\alpha|A_k\alpha\rangle|
=\exp[-\|(A_j-A_k)\alpha\|^2/2].
$$

Define H as in the canonical theorem and kappa=||H||. A useful independent
identity is

$$
H=\frac1{m-1}\sum_j(A_j-\overline A)^\dagger(A_j-\overline A),
\qquad\overline A=\frac1m\sum_j A_j.
$$

Convexity of the exponential gives the normalized mean pair-overlap lower bound
exp(-alpha-dagger H alpha) >= exp(-kappa N).

For any POVM {M_y}, completeness and Cauchy-Schwarz imply

$$
|\langle\psi_j|\psi_k\rangle|
\le\sum_y\sqrt{p(y|j)p(y|k)}.
$$

This is proved directly here; no assumed optical receiver restriction enters.
At a conclusive outcome assigned to j, let d=p(y|j) and let w be the sum of the
other m-1 conditional probabilities. The sum of pairwise square roots at that
outcome is at most sqrt((m-1)dw)+(m-2)w/2. For all inconclusive records together,
the corresponding upper contribution is m(m-1)F/2. After summing conclusive
records and applying Cauchy-Schwarz again,

$$
e^{-\kappa N}\le F+2\sqrt{CE/(m-1)}+\frac{m-2}{m-1}E.
$$

Since F=1-C-E, this is equivalent to

$$
\left(\sqrt C-\sqrt{E/(m-1)}\right)^2\le1-e^{-\kappa N}.
$$

Taking the upper branch and using C+E<=1 proves the bound for one coherent pulse.

### Mixtures and references

The upper function A+E/(m-1)+2 sqrt(AE/(m-1)) is jointly concave and increasing in
A; A(N)=1-exp(-kappa N) is concave. Jensen proves the same bound after averaging
any labelled intensity and amplitude mixture at its mean energy. Equivalently,
one can carry the preparation label into the full classical outcome record
and apply the preceding pairwise-statistics argument after averaging overlaps.
Both routes retain arbitrarily rare bright pulses. No maximum pulse energy or
photon-number cutoff has been introduced.

A reference state independent of the hidden label conditional on the preparation
label factors from the pure coherent signal. Granting it to the receiver does
not change these pair overlaps. A common downstream quantum channel can only
make discrimination harder. Access to a label-dependent side channel or the
lost-light environment would change the contract.

The passive response bound must apply to every permitted signal mode and pulse
energy. A finite-energy calibration does not alone prove a device remains linear
at arbitrarily high illumination; this is an explicit model assumption, not a
consequence of the intensity-mixture theorem.

## 5. Exact uniform-loss attainment

For m=4 and a balanced coherent pulse with effective energy x=t mu, let
c=exp(-x). Its state Gram matrix is G=(1-c)I+cJ. For any proposed C,E, take the
conclusive amplitude matrix B with diagonal sqrt(C) and off-diagonal sqrt(E/3).
The conclusive map T=B G^(-1/2) is a valid contraction precisely when

$$
(\sqrt C+\sqrt{3E})^2\le1+3c,
\qquad
(\sqrt C-\sqrt{E/3})^2\le1-c.
$$

The second inequality is saturated by the claimed curve. The first becomes tight
at the minimum-error point, whose probability is

$$
P_{\rm ME}=\frac{[\sqrt{1+3c}+3\sqrt{1-c}]^2}{16}.
$$

Together with the all-probe upper bound, this establishes global classical
optimality at uniform loss, not just optimality for a prescribed balanced probe.
For x=0, all outputs are identical: guessing on a chosen fraction gives
C=min(epsilon/3,1/4). This resolves the singular inverse in the limit.

An abstract POVM exists along the whole frontier. Only specific endpoints or
separately constructed receivers may be assigned a simple optical realization.
The proof does not equate an arbitrary coherent-state POVM with the fixed
four-port photon decoder.

## 6. Calibration and the reverse benchmark

Stack the pair differences (A_j-A_k)/sqrt(m(m-1)) into L. Then kappa=||L||^2.
For simultaneous operator-norm errors epsilon_j, the stacked difference obeys

$$
\|L-\widehat L\|\le\delta,
\qquad
\delta^2=\frac{\sum_{j<k}(\epsilon_j+\epsilon_k)^2}{m(m-1)}.
$$

Hence kappa <= (sqrt(kappa_hat)+delta)^2. A fitted central transfer matrix or an
average of fluctuating matrices does not supply these simultaneous bounds.
Hypothesis-specific overall optical phases must remain in A_j. The gauge-change
example kappa=1 to 4/3 was independently reproduced.

For photon states with surviving vectors u and v and respective vacuum weights,
||u-v||<=epsilon implies

$$
\tfrac12\|\rho_u-\rho_v\|_1\le2\epsilon.
$$

A score in [-lambda,1] changes by at most 2(1+lambda)epsilon. This proves the
reverse ceiling after adding the nominal photon bound. Coordinatewise upper
transmission bounds are safe because the receiver can append additional loss
to emulate any smaller diagonal transmission vector.

The reverse conclusion is about the specified one-photon class. It is not a
claim that classical states dominate all quantum states. This distinction must
remain even if a measured coherent control beats the bound.

For the illustrative Gaussian phase noise, the small deterministic map radius
cannot literally cover unbounded Gaussian draws. The safe interpretation is the
one already allowed by the theory: independent, label-independent phase noise
is a common post-encoding channel, while the operator radius bounds the coherent
map calibration. An experiment must justify that common-channel assumption or
supply another valid uncertainty model.

## 7. Score bound and fixed-budget statistics

Let q=m-1 and lambda>1/q. Optimizing the correct-rate upper bound minus lambda E
without the normalization constraint yields

$$
S_\lambda\le K_\lambda[1-e^{-\kappa\mu}],
\qquad K_\lambda=\frac{q\lambda}{q\lambda-1}.
$$

Separately S_lambda<=1. The correct combined statement is

$$
S_\lambda\le\min\{1,K_\lambda[1-e^{-\kappa\mu}]\}.
$$

The canonical text's additional inequality K_lambda[1-exp(-kappa mu)]<=1 is false
in general. Finding F01 records an explicit example. The canonical implementation
already uses the correct minimum, so this transcription error does not undermine
its primary test.

Concavity supplies a tangent b+nu mu at any reference budget. For a conditional
null with predictable mean energies m_i and sum_i m_i<=N mu_U along every allowed
history, use the tangent at mu_U. This bounds the cumulative conditional score by
N K_lambda[1-exp(-kappa mu_U)], also capped by N. For scores X_i in [-lambda,1],
conditional Hoeffding's lemma gives

$$
\mathbb E[e^{t(X_i-\mathbb E[X_i|\mathcal F_{i-1}])}|\mathcal F_{i-1}]
\le e^{t^2(1+\lambda)^2/8}.
$$

Multiplication and exponential Markov inequality yield the stated fixed-N
radius (1+lambda)sqrt(log(1/alpha)/(2N)). The iid null is the special case with
a constant conditional law. Independent hidden labels and absence of a source
or controller leak are essential. The receiver's per-use output contract also
excludes a hidden collective multi-query experiment.

A single random choice of brightness shared by a whole run is not iid. At a
run-averaged mean of one photon, choose vacuum runs with probability .9 and
10-photon-mean coherent runs with probability .1. A bound misapplied as iid can
reject with probability at least .09556 at nominal alpha=.01 in the explicit
1000-trial negative control. This does not refute the theorem: it demonstrates
why its predictable-budget/iid conditions cannot be weakened to a grand mean.

Calibration is charged with a union bound, not validated by a JSON approval flag.
The two primary tests require their shared simultaneous calibration allocation
plus both statistical allocations. Optional stopping or outcome-selected
calibration/test partitions would require a different analysis.

## 8. Detectors, source tails and software interpretation

For photons occupying a single spatial superposition, conditional on a phase
vector, the occupation distribution is multinomial, including the loss mode.
This yields the no-click generating function in the reference code. An independent
calculation enumerating every occupation and dark-click mask and integrating over
Gaussian phases agrees with it. The phase is shared by all photons of a pulse;
it is not redrawn independently per photon.

The trial analyzer retains zero-click and multiple-click attempts. The independent
64-record accounting test, containing each of 16 masks for each hidden label,
returns C_count=4, E_count=12 and F_count=48. Its synthetic and external-calibration
warnings are retained. The two published synthetic margins reproduce by direct
count arithmetic; they are not observations.

Subtracting an upper bound q_tail on the multiphoton probability from a score
removes at least every possible positive contribution from those events, since
a trial score is at most one. It is optional conservative attribution, not output
postselection. Tail energy must still enter the illumination budget. A probability
bound or g2 measurement alone cannot cap arbitrarily large photon-number tails.

The floating-point photon support routine is not valid over its entire accepted
finite-penalty input domain: at very large lambda it subtracts two numbers to
obtain E and then amplifies that cancellation by lambda. F02 gives a reproducible
case below the score of an explicitly feasible zero-error strategy. It is a
numerical implementation defect, not a counterexample to the analytic theorem.
A domain guard or a stable higher-precision/outward-bounded implementation is
needed before unrestricted use as a certificate. The audited lambda=5 protocol
points are not affected by that example.

## Conclusion of the reconstruction

The photon frontier, uniform classical optimum, all-energy classical extension,
map-calibration bound, reverse bound, and fixed-N assumptions support the intended
primary comparisons in their declared models. The false chained cap, numerical
large-penalty behavior, and terminology discrepancy require separate correction.
No conclusion of experimental feasibility, external peer review, formal proof
verification, or publication-level novelty follows from this audit.
