# Two candidate contributions

**Working scientific position, not a manuscript or a priority clearance.**
The mathematical statements are supported by the repository's independent audit
and bounded numerical repair. The completed predecessor comparison narrows what
may be distinct. There are no acquired laboratory data.

The task is to identify one of four equally likely optical phase patterns with
one interrogation. Exactly one tested path receives a pi phase flip. The reader
returns a path label or an inconclusive result. Let C, E, and F be the correct,
wrong, and inconclusive probabilities **per attempted interrogation**, so
C+E+F=1. A chosen penalty lambda gives the score C-lambda E.

The simple mechanism is established: prepare path amplitudes, apply the unknown
optical operation, interfere the returned light, and read the outputs. The two
candidate contributions concern the optimal preparation and the comparison with
classical illumination, not a new reading circuit or learning architecture.

## A. Retune the input and keep the receiver fixed

**Statement.** For a square flat orthogonal phase code, uniform hidden labels,
and known positive diagonal losses independent of the label, a fixed code
decoder attains the optimal single-photon reliability tradeoff when the incident
amplitudes and the no-click decision rule may be chosen appropriately.

For the four-path code, put v_i=sqrt(eta_i), where eta_i is the transmission
probability of path i. For lambda at least 1/3, the optimum is

$$
\max(C-\lambda E)=\lambda_{\max}\left[
\frac{1+\lambda}{4}vv^T-\lambda\,\mathrm{diag}(\eta)
\right].
$$

Prepare p_i=z_i^2 from its normalized positive principal eigenvector and use
D=J/2-I, where J is the four-by-four all-ones matrix. No click is inconclusive
on this branch. The minimum-error endpoint and partial guessing on vacuum
outcomes complete the frontier. This is classical calculation of a preparation,
not a coherent parameter register.

**What is inherited.** The fixed-input decoder is a known square-root
measurement. The zero-error harmonic-mean rule follows from established
unambiguous-discrimination arguments and normalization. Joint probe/measurement
optimization and error-margin tasks also predate this work.

**What remains a candidate contribution.** The particular joint optimization
collapses to input-only retuning despite unequal losses and erasure. The proof
compares with arbitrary final measurements, not only the chosen decoder.
Normalizing a putative receiver filter into a different pre-device input explains
why that filter need not remain in the receiver. It does not reverse loss or
condition the reported statistics on detection.

The theorem excludes an occupied bypass rail, retained idler, repeated calls to
one hidden setting, and an additional healthy hypothesis. It is not an optimum
for an arbitrary noisy chip. See [Theorems 1-2](../proofs/THEORY.md) and
[reductions R1-R3](../audits/novelty-01/REDUCTIONS.md), including the Eldar-Forney,
Chefles-Barnett, Hashimoto, and Bagan predecessors.

## B. Bound the classical source class, not one implemented laser receiver

**Statement.** For uniform hidden labels selecting declared passive coherent
maps A_j, a mean incident signal budget mu, and inaccessible loss modes, every
allowed nonnegative Glauber-Sudarshan coherent-state mixture satisfies

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
and perform an arbitrary measurement. The illumination may contain arbitrarily
rare bright pulses. The energy budget counts signal photons entering the tested
section, not total apparatus energy. The maps must share a physical phase
reference; independent label-dependent global phases cannot be discarded.

**What is inherited.** Overlap bounds, the binary scattering contrast, concavity,
and error/inconclusive measurements are established. At uniform four-path loss,
the attained fixed-alphabet curve is exactly Herzog's Eq. (4.18) after a change
of variables. Calibration norm bounds and the fixed-N statistical wrappers are
supporting tools, not separate novelty claims.

**What remains a candidate contribution.** The multiclass optical converse
covers alternative transmitters and their entire intensity mixtures, not just
measurements of one given alphabet. It supplies an all-source upper bound to
which an unconditional experimental score can be compared. Combining it with
the known uniform alphabet gives an exact source-class frontier there; the
general-map ceiling is not claimed to be attainable everywhere.

See [Theorems 3-5 and the score witnesses](../proofs/THEORY.md),
[reductions R4-R8](../audits/novelty-01/REDUCTIONS.md), and the
[numerical contract](NUMERICAL_CONTRACT.md). Only the photon-support enclosure
and its specified perturbation addition have outward-safe arithmetic; this is
not an interval certificate for the entire experimental pipeline.

## What would substantiate the paper

The mechanism test M1 measures predicted input redistribution with the same
receiver. The positive test P1 seeks an unconditional score above the classical
ceiling using independently justified calibration and energy bounds. The reverse
test P2 seeks an actually measured coherent score above the entire stated
four-path photon bound. Neither a theoretical forecast nor a favorable normalized
intensity pattern is an observed advantage.

The narrow one-bad-path zero-error crossover remains a supporting solved case,
not a third general framework. The uniform curve is a credited control. More
modes are unnecessary for these first tests.

The bounded search did not subsume A or the complete B contract in the inspected
passages. That is not proof of priority. In particular, the original S20 text,
a full S18 theorem/appendix comparison, and potentially equivalent multiclass
bounds remain coverage gaps. See the [source map](../SOURCE_AUDIT.md) and
[lab-review rationale](../experiment/REVIEW_RATIONALE.md). No experimental date,
external endorsement, or journal outcome is implied.
