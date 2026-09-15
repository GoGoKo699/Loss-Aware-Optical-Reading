# Explicit predecessor reductions

This note compares the statements at baseline
`db17e1ec1868107b0fe1042d5a480769b552633e` with S18, S20, S08, and the newly
identified S22. Source IDs and actual reading scope are in [SOURCES.md](SOURCES.md).
These are comparison derivations, not new protocol or priority claims.

## 1. Notation and the recovered S20 endpoint

For m normalized pure received states with uniform prior, define

$$
R=\frac{1}{m(m-1)}\sum_{i\ne j}|\langle\psi_i|\psi_j\rangle|.
$$

The sum is over ordered pairs and uses absolute overlap, not its square.
C, E, F denote unconditional correct, erroneous, and inconclusive probabilities.

S20 Theorem 1 gives, for arbitrary priors p_i,

$$
P_{\rm USD}\le 1-\frac{1}{m-1}\sum_{i\ne j}
\sqrt{p_i p_j}\,|\langle\psi_i|\psi_j\rangle|.
$$

With p_i=1/m, this is exactly C<=1-R at E=0, the repository's zero-error
statistics inequality. It is a bound, not an exact optimum for every ensemble.
For example, priors .99 and .01 and overlap .5 give the S20 ceiling .9005012563,
while the actual two-state USD optimum from S08 Eq. (10) is .7425.
S20's discussion of sequential measurements concerns the same supplied specimen;
it does not establish a fresh-copy, repeated-interrogation illumination bound.

## 2. A much closer finite-error predecessor: S22

Bagan, Calsamiglia, Bergou, and Hillery, S22 Lemma 1 / Eq. (9), prove a bound
between optimal discrimination and normalized l1 coherence. The supplement,
Eqs. (18)-(37), allows arbitrary detector-state priors p_i. Choose its parent
path state to be pure with amplitudes sqrt(p_i). Then its coherence variable is

$$
X=\frac{L}{m},\qquad
L=\sum_{i\ne j}\sqrt{p_i p_j}\,|\langle\psi_i|\psi_j\rangle|.
$$

Writing P_* for the optimal always-answer discrimination probability, their
lemma is exactly

$$
L\le h_m(P_*),\qquad
h_m(p)=(m-2)(1-p)+2\sqrt{(m-1)p(1-p)}.
$$

In particular, for uniform priors, L=(m-1)R. If F=0 and C=P_*, E=1-C,
this becomes

$$
R\le\frac{m-2}{m-1}E+2\sqrt{\frac{CE}{m-1}}.
$$

This is the repository's no-abstention multiclass core, with the same constants.
The original statement is in wave-particle duality language, which explains why
searching only optical-reading or inconclusive-discrimination titles missed it.
The 2016 predecessor S23 contains a weaker quadratic relation; the exact match
here is S22, not an attribution of the stronger formula to S23.

## 3. Inconclusive outcomes follow from the known filter transformation

S08 Eqs. (6)-(8) reduce a fixed-inconclusive problem to conditional minimum-error
discrimination, with transformed states AND transformed priors. We apply that
construction to show that the useful upper-C bound follows from S22 as well.
This is an explicit corollary calculation, not a claim that S22 printed the
following optical formula verbatim.

Let Q be the failure effect of any measurement and define

$$
K=\sqrt{I-Q},\quad u_i=K|\psi_i\rangle,\quad
q_i=\langle u_i|u_i\rangle,\quad T=1-F=\frac1m\sum_i q_i.
$$

When T>0, the conditional pure ensemble has

$$
\pi_i=\frac{q_i}{mT},\qquad |\chi_i\rangle=\frac{u_i}{\sqrt{q_i}}.
$$

Zero q_i have zero conditional weight; the corresponding terms are omitted or
handled by continuity. Singular K is inverted only on its support. The physical
measurement restricted to conclusive records is a valid conditional measurement
and has correct probability c=C/T. In general the pi_i are NOT uniform.

Set

$$
L_c=\sum_{i\ne j}\sqrt{\pi_i\pi_j}
|\langle\chi_i|\chi_j\rangle|
=\frac1{mT}\sum_{i\ne j}|\langle\psi_i|(I-Q)|\psi_j\rangle|.
$$

The decomposition I=(I-Q)+Q, triangle inequality, and positivity of Q imply

$$
R\le\frac{T L_c}{m-1}+F.
$$

For completeness, writing f_i=<psi_i|Q|psi_i>, the failure part is bounded by

$$
\frac{\sum_{i\ne j}\sqrt{f_i f_j}}{m(m-1)}
\le\frac{\sum_i f_i}{m}=F.
$$

The conclusive ensemble's optimal success P_* is at least c. The function h_m
is nonincreasing on [1/m,1]: differentiate it, or note that its maximum is at
1/m and its derivative is negative thereafter. Hence, when c>=1/m, S22 gives
L_c<=h_m(P_*)<=h_m(c). Substitution yields

$$
R\le F+\frac{T h_m(C/T)}{m-1}
=F+\frac{m-2}{m-1}E+2\sqrt{\frac{CE}{m-1}}.
$$

Using C+E+F=1 and taking the upper root gives

$$
C\le\left[\sqrt{1-R}+\sqrt{\frac{E}{m-1}}\right]^2.
$$

For c<1/m, C<E/(m-1), so this final upper-root bound is already trivial.
No monotonicity outside the justified interval is used. For T=0, C=E=0.
Thus the upper-C bound required by the optical theorem follows for EVERY
measurement, including bad decoders, all-failure, singular-filter, and
zero-conditional-prior cases. S22's supplement also handles linearly dependent
ensembles by continuity.

This argument establishes a direct dependency on known results for the relevant
finite-F consequence. It does not assert that the complete two-sided intermediate
inequality for a below-chance decoder is a literal instance of S22's optimal-P
statement. The repository's direct positivity proof supplies that stronger
intermediate formulation independently.

## 4. The optical source-class statement is a short additional corollary

For a pure coherent input alpha, energy N=||alpha||^2, and returned states
|A_j alpha>, the standard coherent overlap is

$$
|\langle A_i\alpha|A_j\alpha\rangle|
=\exp\left[-\frac12\|(A_i-A_j)\alpha\|^2\right].
$$

Define the repository contrast

$$
H_\Delta=\frac1{m(m-1)}\sum_{i<j}(A_i-A_j)^\dagger(A_i-A_j),
\qquad \kappa=\|H_\Delta\|.
$$

Jensen over the unordered pairs, with the 1/2 in the overlap exponent, gives

$$
R\ge e^{-\alpha^\dagger H_\Delta\alpha}\ge e^{-\kappa N}.
$$

Together with Section 3 this proves the pure-pulse correct-rate bound. Let
A(N)=1-exp(-kappa N) and

$$
g(A,E)=A+\frac{E}{m-1}+2\sqrt{\frac{AE}{m-1}}.
$$

g is jointly concave and increasing in A, and A(N) is concave. For any
receiver-labelled classical illumination mixture with finite mean energy <=mu,

$$
\bar C\le\mathbb E[g(A(N),E)]
\le g(\mathbb E[A(N)],\bar E)
\le g(A(\mu),\bar E).
$$

Combining with normalization gives exactly the canonical classical ceiling.
No pulse-energy cutoff is used. This remains true when an independent reference
state is supplied conditional on the illumination label: it cannot add information
about the hidden device label. Granting the illumination label strengthens, rather
than weakens, the competitor.

The complete source-class optical statement has not been located verbatim in
S22/S08. Nevertheless its generic measurement ingredient is inherited and its
additional overlap/energy steps are short standard arguments. The defensible
framing is an application-specific optical corollary and certification tool,
not a newly invented general multiclass error/inconclusive inequality. Its
uniform fixed-alphabet attainment was already credited to Herzog in audit 01.
Calibration wrappers and energy-tail accounting remain operationally important;
the reduction does not remove their assumptions or make a numerical test a
physical calibration.

## 5. What S18 does and does not imply

S18 main Eqs. (1)-(8), Appendix B Lemmas 1-2, and Appendix F Proposition 1 concern
binary asymmetric discrimination of channels, with reference systems and possibly
adaptive repeated use. Their finite-n inequality, Eq. (144), is

$$
\frac{-\ln\beta_n^*(E,\varepsilon)}n
\le\frac{\widehat D_{H,E}(\mathcal N\|\mathcal M)+h_2(\varepsilon)/n}
{1-\varepsilon}.
$$

It is not only an asymptotic statement: it holds at finite n as well. Its
objective is a type-II error bound given a type-I constraint, not a uniform
m-class unconditional C/E/F score. Their Eq. (60) is an energy-constrained Choi
operator optimization; it is not the photon Rayleigh quotient in Claim A.
Their phase-covariance reduction concerns a diagonal SIGNAL MARGINAL of a
purified input-reference state, not an incoherent whole probe. Section III.2
states this explicitly. The displayed coherent comparison is coherent input
plus heterodyne detection, not the whole classical class of Claim B.

A concrete non-subsumption check is available. Two distinct pure coherent returns
have nonparallel one-dimensional supports. Represent them as

$$
|a\rangle=(1,0)^T,\qquad |b\rangle=(c,\sqrt{1-c^2})^T,
\qquad 0<c<1.
$$

Then

$$
\mathrm{Tr}[(I-|b\rangle\langle b|)|a\rangle\langle a|]=1-c^2>0.
$$

Thus their relative entropy, and hence their Belavkin-Staszewski divergence,
is infinite. In the ideal coherent-return subcase this already makes the
corresponding energy-constrained divergence supremum infinite. Directly using
S18's divergence ceiling is then vacuous, while our finite-error/abstention
bound remains finite. This is not a criticism of S18 or a claim about every
possible use of its framework. It shows why Eq. (144) alone does not recover
our operational certificate.

Appendix J Proposition 2, Eq. (238), gives a truncation allowance
2E D(p||q)/(N+1) for BOSONIC DEPHASING channels. It is not an unqualified guarantee
for arbitrary loss-dephasing maps, multimode phase reading, or unrestricted
classical pulse mixtures. The paper explicitly identifies missing general
loss-dephasing truncation control. We do not import its finite Fock cutoff into
our all-intensity converse.

## 6. Status of the comparison

S18's named relevant theorem/appendix gap and S20's original-text gap are resolved
at the versions and access levels recorded. This is not an independent correctness
audit of all S18 statements or source code. Claim A is not subsumed by these
sources under the complete repository contract. Its priority is still not proved.
Claim B's generic statistics core is more directly inherited than audit 01
established, and its full optical bound should be presented as a corollary with
explicit attribution. No canonical files have been changed in this stage.

The independent script checks 572 normalization, filter, attainment, mixture,
and scope examples. Universal reductions above, not those examples, support
the classifications. No laboratory data or external proof endorsement is used.
