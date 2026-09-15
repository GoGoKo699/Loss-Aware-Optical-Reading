# Candidate contribution and derived benchmark

**Working scientific position, not a manuscript or a priority clearance.**
The independent audit and bounded repair support the mathematical statements.
The full-text follow-up changes their novelty hierarchy, not their validity.
A is the leading candidate theoretical contribution. B is a credited optical
corollary and benchmark, not a second independently new general inequality.
There are no acquired laboratory data.

The task identifies one of four equally likely optical phase patterns in one
interrogation. Exactly one tested path receives a pi phase flip. Let C, E, and F
be the correct, wrong, and inconclusive probabilities **per attempted interrogation**,
with C+E+F=1. A preselected wrong-answer penalty lambda gives C-lambda E.
The established physical mechanism is preparation, interrogation, interference,
and detection. It is not a new learning architecture.

## A. Retune the input and keep the receiver fixed

For a square flat orthogonal phase code, uniform hidden labels, and known
positive diagonal losses independent of the label, one fixed code decoder
attains the optimal single-photon reliability tradeoff when the input amplitudes
and no-click decision rule are chosen appropriately.

For the four-path code, v_i=sqrt(eta_i), with transmission probabilities eta_i.
For lambda at least 1/3, the exact optimum is

$$
\max(C-\lambda E)=\lambda_{\max}\left[
\frac{1+\lambda}{4}vv^T-\lambda\,\mathrm{diag}(\eta)
\right].
$$

Prepare p_i=z_i^2 from the normalized positive principal eigenvector and use
D=J/2-I. No click is inconclusive on this branch. The minimum-error endpoint and
partial guessing on vacuum complete the frontier. The preparation is computed
classically; there is no coherent parameter register.

**Inherited ingredients.** The decoder for a fixed input is a known square-root
measurement. The zero-error harmonic mean follows from established unambiguous
state discrimination and normalization. Joint input/measurement optimization
and error-margin tasks also predate this project.

**Candidate distinction.** The complete lossy joint optimization compares with
arbitrary final measurements, not only the selected decoder. A possible receiver
filter can be absorbed into a different normalized input before interrogation.
This neither reverses loss nor conditions the score on detection. The
[original reductions R1-R3](../audits/novelty-01/REDUCTIONS.md) identify the exact
remaining step after crediting the predecessors.

The theorem excludes an occupied bypass rail, retained idler, repeated calls to
one setting, and a fifth healthy hypothesis. It is not an optimum for every
noisy chip. The named follow-up sources did not state this complete contract;
that is not proof of worldwide priority. See
[Theorems 1-2](../proofs/THEORY.md) and the [claim ledger](../CLAIM_STATUS.md).

## B. A derived benchmark over the classical source class

For uniform hidden labels selecting passive coherent maps A_j, a mean incident signal budget
mu, and inaccessible loss modes, every permitted nonnegative Glauber-Sudarshan
coherent-state mixture satisfies

$$
C\le\min\left\{1-E,
\left[\sqrt{1-e^{-\kappa\mu}}+\sqrt{E/(m-1)}\right]^2\right\}.
$$

Here m is the number of labels and kappa is the operator norm of

$$
H_\Delta=\frac{1}{m(m-1)}\sum_{j<k}
(A_j-A_k)^\dagger(A_j-A_k).
$$

The receiver may know the illumination's mixture label, use a phase reference,
and perform any measurement. The illumination may contain arbitrarily
rare bright pulses. Count signal photons entering the tested section, not total
apparatus energy. The physical maps share a phase reference; independent
label-dependent global phases cannot be discarded.

**Attribution.** S20, Zhang et al. (2001), supplies the zero-error overlap bound.
S22, Bagan et al. (2018), gives the exact no-failure multiclass relation. The
established conclusive-filter transformation S08, with reweighted conditional
priors, gives the useful arbitrary-failure upper-C consequence. A separate
failure-row argument in the supplied follow-up reaches the same interpretation.
Coherent-state overlaps, the map norm, and concavity produce the mean-energy
optical corollary. See [the explicit follow-up reductions](../audits/novelty-02/REDUCTIONS.md).

The uniform four-symbol fixed-alphabet curve is Herzog's Eq. (4.18). The optical
source-class converse rules out alternative transmitters and intensity mixtures,
so it remains necessary, but the short reduction does not support claiming a
new generic discrimination theorem. The general-map ceiling is not asserted to
be attained everywhere. Binary spectral contrast, nulling receivers, calibration
norm bounds, and fixed-N statistics are also credited supporting methods.

**Experimental role.** B is a strong comparison for P1, not merely a model of
one laboratory laser receiver. A useful new implementation or calibrated source
comparison need not invent its benchmark. No exact experimental advantage or
publication significance follows merely from writing down this corollary.

See [Theorems 3-5 and score witnesses](../proofs/THEORY.md) and the
[numerical contract](NUMERICAL_CONTRACT.md). Only the photon-support enclosure
and its specified perturbation addition use outward-safe arithmetic; this is
not an interval certificate for the full experimental pipeline.

## What the paper and experiment must establish

M1 tests predicted input retuning while the decoder stays fixed. A scan is not
a proof of global optimality. P1 seeks unconditional performance above B using
independently justified calibration and energy bounds. P2 requires a measured
coherent score above the entire declared four-path photon ceiling, not one poor
photon preparation and not every possible quantum architecture.

The one-bad-path zero-error crossover remains a supporting solved case under
its original restrictions. Known uniform curves are controls. No more modes or
new algorithmic name is required by this attribution update.

The named S18/S20 comparisons are resolved at the recorded access levels. S20
was read in embedded author-uploaded original text, not a downloaded publisher
PDF. S18 includes finite-n results but uses a different binary/reference-assisted
contract. Partial additional leads and wider priority remain open; they do not
undo the explicit S22 reduction. See the [source map](../SOURCE_AUDIT.md) and
[lab-review rationale](../experiment/REVIEW_RATIONALE.md).
