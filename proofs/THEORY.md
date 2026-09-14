# Single-photon phase reading: exact frontiers and an experimental certificate

Date: 2026-09-14. Mathematical status: the propositions below have explicit
analytic proofs. Numerical checks are supplementary, not proofs of universal
claims. No independent external referee, formal proof assistant, interval
arithmetic, or laboratory validation is claimed. Novelty remains separate.

## 0. Scope and notation

One hidden label j is sampled uniformly and independently for each attempted
interrogation. It selects one passive optical map. The source and receiver do
not receive j. There is one traversal per decision. Reusing the same unknown
label for several probes and then decoding jointly is a different task.

All rates are per attempted interrogation:

- C: correct conclusive answer;
- E: incorrect conclusive answer;
- F=1-C-E: inconclusive.

A scored trial has value 1, -lambda, or 0 respectively. Lambda >= 0 is selected
before the test, not fitted to its outcomes. Write S_lambda=C-lambda E.

The exact photon benchmark uses one photon in the m tested paths, without an
occupied bypass rail, retained idler, vacuum/one-photon coherence, or repeated
calls. A herald outside the tested paths may define a trial but is not an
interacting computational photon. Real vacuum/multiphoton contamination is a
separate input model.

A classical probe is a nonnegative Glauber-Sudarshan mixture of coherent signal
states. The receiver is granted the mixture label, arbitrary reference states
independent of j conditional on that label, and an arbitrary final POVM. Signal
energy entering the tested section is charged. A coherent local oscillator that
never interrogates the unknown section is not charged to this signal budget.
This is not a total-energy, pump-energy, latency, or computational-complexity
comparison. The phrase 'positive-P' is avoided because the doubled-phase-space
positive-P representation is not the same classicality condition.

The receiver does not access the loss environment or an unmonitored
hypothesis-dependent side channel. Signal temporal/spectral modes are either
specified explicitly or share the same proved map bound. Probe preparation
cannot depend on the current hidden label.

## 1. Exact photon theorem for any flat orthogonal phase code

Let Z be an m by m matrix with |Z_ij|=1 and Z^dagger Z=m I. Column j supplies the
physical diagonal phase operation O_j=diag(Z_1j,...,Z_mj). Let

  eta_i in (0,1],   v_i=sqrt(eta_i),   T=diag(sqrt(eta_i)).

The loss is independent of j and precedes the unconstrained final measurement.
Known preparation phases can be absorbed into the receiver. For a normalized
probe with probabilities p_i, the surviving states are

  |phi_j> = diag(sqrt(eta_i p_i)) Z_:j.

Each hypothesis also produces the same vacuum probability 1-s, with
s=sum eta_i p_i. The first experiment has m=4 and Z=J-2I. The fixed decoder is
Z^dagger/sqrt(m), equal to J/2-I in that experiment.

### Theorem 1: complete exposed error/inconclusive boundary

For lambda >= 1/(m-1), define

  B_lambda = ((1+lambda)/m) v v^T - lambda diag(eta),
  beta_q(lambda) = largest eigenvalue of B_lambda.

Then

  sup_(all permitted probes and POVMs) (C-lambda E) = beta_q(lambda).

The bound is attained with the fixed decoder Z^dagger/sqrt(m), inconclusive
vacuum events, and input probabilities p_i=z_i^2, where z is the normalized
positive top eigenvector of B_lambda. Neither a generalized receiver nor a
successful photon filter is necessary.

#### Proof without a covariance or numerical-solver assumption

Let M_j be the photon-sector POVM effect assigned to j, so sum_j M_j <= I.
Set m_i=sum_j (M_j)_ii <= 1 and q_i=eta_i p_i. Positivity gives

  |(M_j)_ik| <= sqrt((M_j)_ii (M_j)_kk).

Since every phase-code entry has unit modulus, a second Cauchy-Schwarz
inequality over j gives

  C_ph <= (1/m) [sum_i sqrt(q_i m_i)]^2.

The average surviving density matrix is diag(q), by code orthogonality. Hence
its total conclusive probability is exactly

  C_ph+E_ph = sum_i q_i m_i.

Define x_i=sqrt(q_i m_i) and z_i=x_i/sqrt(eta_i). Then sum_i z_i^2 <= 1 and

  C_ph-lambda E_ph <= z^T B_lambda z <= beta_q(lambda).

The last inequality uses beta_q>0: the vector proportional to 1/sqrt(eta_i)
yields the positive harmonic-mean score. A conclusive guess on the common
vacuum contributes (1-(m-1)lambda)/m times its conclusive probability. This is
nonpositive in the stated lambda range, so it does not increase the bound.

After addition of a large scalar multiple of I, B_lambda is an entrywise
strictly positive matrix. Its top eigenvector can therefore be chosen strictly
positive and is unique. Choose p_i=z_i^2 and the code decoder. Its decision
amplitudes have diagonal value sum_i sqrt(eta_i p_i)/sqrt(m). Thus

  C = [sum_i sqrt(eta_i p_i)]^2/m,
  E = sum_i eta_i p_i - C,
  F = 1-sum_i eta_i p_i,

and its score equals the Rayleigh quotient at z. All inequalities are saturated.
Classical randomization of probes/receivers cannot exceed a bound valid for each
component, even when its randomization label is supplied to the receiver. QED.

### Preparation recipe

The same eigenproblem is a scalar root equation:

  ((1+lambda)/m) sum_i eta_i/(beta+lambda eta_i) = 1,
  p_i proportional to eta_i/(beta+lambda eta_i)^2.

There is one positive root. This gives an implementation with a fixed decoder
and a changed input-amplitude file. It is not an adaptive parameter register.

### Theorem 2: minimum-error endpoint and the full error-budget frontier

Let l0=1/(m-1), and let C0,E0,F0 be the Theorem 1 rates at l0. Then

  P_ME = C0+F0/m
       = [1+lambda_max(v v^T-diag(eta))]/m.

For 0 <= lambda <= l0,

  beta_q(lambda)=(1+lambda)P_ME-lambda.

Proof: replacing an inconclusive event by a uniformly random label changes its
score by [1-(m-1)lambda]/m >=0. Therefore an optimum always answers. In the
photon sector a complete code measurement attains the Cauchy-Schwarz upper
bound above. The vacuum supplies correct probability (1-s)/m. Maximization over
the normalized input is exactly the displayed largest-eigenvalue problem.

For a permitted error epsilon, the complete optimal correct rate is

  C_q^*(epsilon) = inf_(lambda>=0) [beta_q(lambda)+lambda epsilon].

This support formula is attained, not only an upper bound:

1. epsilon=0: inverse-loss preparation, with
   H_eta=m/sum_i 1/eta_i, C=H_eta, E=0, F=1-H_eta.
2. 0<epsilon<E0: choose lambda>l0 whose Theorem 1 output has E=epsilon.
3. E0<=epsilon<=1-P_ME: keep the l0 probe/receiver and randomly guess on an
   appropriate fraction of vacuum events. C=C0+(epsilon-E0)/(m-1).
4. epsilon>=1-P_ME: always answer with the minimum-error strategy.

The support function is convex in lambda; where differentiable beta'_q=-E.
The positive top eigenvector is unique, so the curve is continuous. Its limit
as lambda -> infinity is the inverse-loss, zero-error preparation. Uniform
transmissions have E0=0, in which case the intermediate curved branch is absent.

The m=4 zero-error endpoint independently recovers checkpoint 06. The theorem
also covers Hadamard or Fourier codes at m=8. It does NOT say that eight
single-path phase-flip states form an orthogonal code; they do not.

## 2. A classical certificate from the actual coherent transfer maps

The next statement does not require an orthogonal code, equal losses, or exact
pi shifts. Let m>=2 uniformly likely labels select passive coherent maps A_j
from a specified input mode space to the accessible output mode space:

  |alpha> -> |A_j alpha>.

The channel may have label-dependent attenuation. Coherent signal outputs of a
passive pure-loss network are still pure coherent states after inaccessible
loss modes are discarded. Additional common quantum channels can only degrade
discrimination and do not invalidate a bound on the undamaged outputs.

Define

  H_contrast = [1/(m(m-1))] sum_(j<k) (A_j-A_k)^dagger(A_j-A_k),
  kappa = ||H_contrast||_op.

For the four one-path-pi-flip code with diagonal losses,
H_contrast=diag(eta), so kappa=max_i eta_i. More general maps can give a larger
or smaller value; kappa is not necessarily a transmission probability.

### Theorem 3: arbitrary-classical-probe finite-error bound

For every allowed classical probe mixture of mean signal energy <=mu and every
receiver,

  C <= min{1-E, [sqrt(1-exp(-kappa mu))+sqrt(E/(m-1))]^2}.

The energy distribution may have unbounded support. An external coherent phase
reference is allowed. An ancillary state common to all hypotheses after the
mixture label is given cannot invalidate the bound.

#### Proof: physical overlap bound

For one pulse, N=||alpha||^2 and

  |<A_j alpha|A_k alpha>| = exp[-|| (A_j-A_k) alpha ||^2/2].

Convexity of exp(-x), followed by the operator bound, gives

  sum_(j<k) |<A_j alpha|A_k alpha>|
    >= [m(m-1)/2] exp[-alpha^dagger H_contrast alpha]
    >= [m(m-1)/2] exp[-kappa N].

#### Proof: output statistics bound

Let p(y|j) denote any measured record, already assigned to a conclusive label
or to failure. Quantum overlap is no larger than the classical fidelity of the
record distributions. At a conclusive output, let d be its correct conditional
probability contribution and w the sum of its m-1 incorrect contributions.
The sum over hypothesis pairs is at most

  sqrt((m-1)dw) + (m-2)w/2.

The corresponding failure contribution is at most m(m-1)F/2. Summing all outputs
and using Cauchy-Schwarz once more yields

  exp(-kappa N)
    <= F + 2sqrt(CE/(m-1)) + (m-2)E/(m-1).

Since F=1-C-E,

  [sqrt(C)-sqrt(E/(m-1))]^2 <= 1-exp(-kappa N).

Taking its upper branch proves the correct-rate inequality for a pure pulse.
The function f(A,E)=A+E/(m-1)+2sqrt(AE/(m-1)) is jointly concave and monotone in A,
and A(N)=1-exp(-kappa N) is concave. Jensen therefore gives the same bound for
arbitrary labelled mixtures at their mean energy. No peak-pulse bound, photon
number truncation, or finite energy scan is used in this proof. QED.

This is a sufficient benchmark for arbitrary maps, not an exact arbitrary-map
classical frontier.

### Theorem 4: a robust matrix-calibration version

Suppose simultaneous, phase-referenced calibration gives

  ||A_j-Ahat_j||_op <= epsilon_j.

Let khat be calculated from the Ahat_j. Then

  kappa <= [sqrt(khat)+delta]^2,
  delta^2 = sum_(j<k)(epsilon_j+epsilon_k)^2/[m(m-1)].

Proof: stack all pair differences divided by sqrt(m(m-1)) into one rectangular
matrix L. Then kappa=||L||_op^2. The perturbation has operator norm at most its
blockwise norm bound delta. Apply the triangle inequality.

For m=4 and equal radii epsilon, kappa_U=(sqrt(khat)+sqrt(2)epsilon)^2.
This addresses coherent map uncertainty without multiplying its error by an
unbounded pulse energy outside the exponential.

A fitted average transfer matrix is not enough to certify this interval for a
fluctuating channel. The interval must cover the stated operation on test
trials, or a common post-encoding noise model must separately justify the bound.
Uncovered bad-channel probability or extra modes need explicit treatment.

### Critical optical-phase warning

A_j and exp(i phi_j)A_j describe the same single-photon output density operator
but need not describe the same coherent-state output relative to a reference.
Independent per-label global phases cannot be removed during this calibration.

For the ideal four one-flip code, kappa=1. Multiplying only A_0 by -1 leaves every
single-photon density operator unchanged but gives kappa=4/3. The classical
probe can exploit that additional phase information. An SU(4) compiler is safe
only when the physical phase convention is shared/known, not independently
chosen modulo a different global phase for each hidden label.

## 3. An exact classical frontier at uniform loss

For m=4 one-flip reading and uniform transmission t, let x=t mu and c=exp(-x).
Define

  P_cl,ME(x) = [sqrt(1+3c)+3sqrt(1-c)]^2/16,
  E_ME(x)=1-P_cl,ME(x).

### Theorem 5

The optimal correct rate over all classical probe mixtures and receivers,
subject to E<=epsilon and mean signal energy <=mu, is

  C_cl^*(epsilon,x) =
    [sqrt(1-c)+sqrt(epsilon/3)]^2,  if 0<=epsilon<=E_ME(x),
    P_cl,ME(x),                    if epsilon>=E_ME(x).

Proof of upper bound: Theorem 3 with kappa=t gives the first branch. Combining
it with C+E<=1 maximizes C at the branch intersection, which is P_cl,ME. The
first branch is increasing, so an error budget cannot exceed its value there.

Proof of attainment: send a coherent pulse with mu/4 incident photons per path.
Its four returned states have Gram matrix G=(1-c)I+cJ. They can be represented by
the columns of sqrt(G). For proposed rates C,E, take a conclusive amplitude
matrix B with diagonal sqrt(C) and off-diagonal sqrt(E/3). The measurement
operator T=B G^(-1/2) gives those conclusive amplitudes. Its failure effect is
I-T^dagger T. Positivity reduces to

  (sqrt(C)+sqrt(3E))^2 <= 1+3c,
  (sqrt(C)-sqrt(E/3))^2 <= 1-c.

The first-branch formula saturates the second inequality and satisfies the
first exactly until E_ME. At the endpoint the measurement is the square-root
measurement. Singular x=0 is the continuous limit, equivalent to guessing on a
chosen fraction of trials.

This supplies a physically allowed abstract POVM. It does not assert that the
whole frontier can be implemented with the same four passive ports and four
click detectors used by the photon experiment. A displaced-and-click receiver
attains the zero-error endpoint. Minimum-error coherent-state receivers require
a separate implementation argument.

The square-root measurement and error-margin discrimination methods are
established prior art. This corollary is a checked specialization with an
all-classical-probe mean-budget upper bound, not a novelty assertion.

### Example that must remain visible in the paper

At t=.7, mu=1, the exact one-photon zero-error correct rate is .7, versus
1-exp(-.7)=.5034146962 for classical probes. At the always-answer endpoint the
one-photon rate is .775, versus .8586096698 for classical probes. The preferred
source depends on the decision requirement. These are ideal task optima, not
claims that our passive classical control implements the latter optimum.

## 4. Experiment-ready linear score witnesses

For lambda>1/(m-1), let

  K_lambda=(m-1)lambda/((m-1)lambda-1).

Maximizing the Theorem 3 upper bound minus lambda E over E>=0 gives

  C-lambda E <= min{1, K_lambda[1-exp(-kappa mu)]}.

This upper bound is not always tight. At a fixed reference budget mu0, concavity
further gives the energy-affine witness

  C-lambda E <= b+nu mu,
  b=K_lambda[1-(1+kappa mu0)exp(-kappa mu0)],
  nu=K_lambda kappa exp(-kappa mu0).

The same supporting line applies at every pulse energy. This is the reason it
covers bright flashes and, with the conditional assumptions below, predictable
intensity changes. It does not assume that an individual pulse has <=1 photon.

### Finite-N test, not optional stopping

Choose lambda, N, the maps/uncertainty envelope, decoder, and primary test before
acquisition. Let X_i in {-lambda,0,1} be each score. Under an iid classical null
with mean energy <=mu_U and contrast <=kappa_U,

  Pr[ mean(X) > U_cl + (1+lambda)sqrt(log(1/alpha_stat)/(2N)) ] <= alpha_stat,

where U_cl=K_lambda[1-exp(-kappa_U mu_U)] or its cap at one. This is the bounded
Hoeffding inequality applied to the score, not a normal approximation to a ratio
of conclusive counts. A direct proof follows by bounding the centered mgf by
exp(theta^2(1+lambda)^2/8), multiplying over N trials, and minimizing Markov's
inequality over theta>0.

The same argument works for a conditional null if j_i remains independent and
uniform given the past, the conditional expected score is bounded by
b+nu m_i, and the cumulative *predictable conditional* energy satisfies
sum_i m_i <= N mu_U along every allowed history (or with the separately charged
calibration failure probability). The affine witness then bounds the cumulative
conditional score, and the conditional mgf proof gives the same radius.

A bound on E[sum m_i] alone is not a pathwise bound. In particular, selecting one
bright operating regime randomly for an entire run can violate a naive iid
interpretation of an average-energy calibration. Use the actual validated null
contract rather than silently applying the martingale version.

If calibration envelopes jointly fail with probability <=alpha_cal, a union
bound gives total false-certification probability <=alpha_stat+alpha_cal. Two
primary tests require splitting the statistical allocation; exploratory plots
do not acquire separate uncorrected significance claims.

An iid fixed source with an unbounded intensity mixture is allowed. However,
finite click data alone cannot upper-bound the mean of an arbitrary unbounded
source distribution: a sufficiently rare, sufficiently bright tail is a
counterexample. The experiment needs an independently justified energy upper
bound (metering or a validated stable source/tail model). A measured g^(2)(0)
value or a multiphoton *probability* bound alone does not bound tail energy.

Calibration bounds are inputs to the analysis software, not quantities that
its 'PASS' result can validate. Stopping after the first apparent violation is
not permitted by this fixed-N test. A separately derived test supermartingale or
alpha-spending procedure would be required for that policy.

## 5. Robust negative comparison against the photon architecture

Theorem 1 also gives a finite-error upper score for every four-path photon
strategy. For independently calibrated diagonal-loss upper bounds eta_U, use
beta_q(lambda;eta_U). Coordinatewise monotonicity follows by appending extra
loss to simulate any smaller transmission vector; the receiver is unrestricted.

If actual one-photon maps differ by operator norm <=epsilon from the nominal
maps, accessible output states (surviving block plus vacuum) differ in trace
distance by at most 2epsilon. To see this, for surviving vectors u,v of norms
<=1, ||uu^dagger-vv^dagger||_1 <=2||u-v|| and
| ||u||^2-||v||^2 | <=2||u-v||. Include the vacuum block and divide by two.

Any score in [-lambda,1] therefore changes by at most
2(1+lambda)epsilon. This supplies the conservative exclusion ceiling

  S_lambda,photon <= beta_q(lambda;eta_U)+2(1+lambda)epsilon.

An actually implemented coherent receiver exceeding this ceiling shows that
this classical strategy beats the entire specified ideal one-photon class in
that regime. It does not show that it beats every quantum probe, quantum idler,
occupied reference rail, or multi-query protocol.

This comparison concerns a strict ideal one-photon benchmark. Nonclassical
multiphoton contamination must not be credited as single-photon optimality.

## 6. Source and detector model used only for planning

The numerical forecast assumes a phase-insensitive source distribution P_n with
all n photons occupying the same prepared superposition. Independent Gaussian
path phases are drawn once for a pulse and shared by its photons. It does NOT
replace the source by n distinguishable independently phase-noised photons.

For a given phase vector and label, let w_l be the probability that one photon
is detected at output l, including its efficiency. For a subset B of detectors,

  Pr(no clicks in B) = product_(l in B)(1-d_l) * sum_n P_n(1-sum_(l in B)w_l)^n.

Inclusion-exclusion produces all 16 click masks. Only masks with exactly one
click are assigned a port label. Zero and multiple clicks remain inconclusive.

The code evaluates the Gaussian phase average through exact finite Fourier
moments for the declared finite source support, then cross-checks against direct
multinomial enumeration in the zero-phase-noise case. This is not source
characterization, detector tomography, or a claim about the actual lab.

For an unknown tail with probability at most q_tail, a score forecast can charge
its worst possible contribution in [-lambda,1]. For a positive experimental
certificate one may additionally subtract q_tail from the observed score,
conservatively removing every possible positive tail contribution. No events
are removed from the trial count. Tail energy must still be included in mu_U.

Vacuum dilution affects both the useful photon probability and the classical
budget. P_0 and P_1 must not be renormalized after heralding/output detection.
For a vacuum-plus-one-photon source with weight s, phase-insensitive statistics
are equivalent to transmissions s*eta in the photon model, but the fair
classical mean budget is mu=s, not mu=1.

## 7. What is proved, and what remains outside these theorems

Proved for the stated contracts: arbitrary-loss flat-code photon frontier;
exact uniform four-one-flip classical frontier; general passive-code classical
finite-error bound; operator-interval robustness; fixed-N certification under
explicit statistical/energy assumptions; photon-class negative comparison.

Retained from checkpoint 06: the exact zero-error classical envelope for
eta=t(1,1,1,r) at mean effective energy <=1, including its high-energy-pulse
supporting-line argument and crossover. The original proof is copied unchanged
in baseline/CP06_PROOFS.md, with a separate audit record.

Not established: the exact classical finite-error frontier for arbitrary unequal
losses; an optimal repeated/adaptive reading protocol; arbitrary noisy bosonic
channels; arbitrary code/prior optimality; a device-independent test; a full
photon-energy calibration procedure for this laboratory; experimental source
parameters; global literature priority; or a journal-level novelty conclusion.
An upper/lower comparison is labelled as such rather than promoted to an exact
frontier. None of these outstanding items is assumed by the two primary tests.

## Numerical implementation after theory audit 01

The analytic theorems above retain their original domain. The floating-point
implementation has an explicit accepted domain and distinguishes nominal recipes
from outward-safe photon support bounds. See [the numerical contract](../docs/NUMERICAL_CONTRACT.md)
and [repair proof](../repairs/theory-01/NUMERICAL_PROOF.md). The original audit
report and source archive are preserved; F01 is the score-cap correction in
section 4, F02 is the numerical repair, and F03 is a code terminology correction.
These changes do not establish novelty or measured advantage.
