# Theorem-level predecessor comparison 01

**Disposition: retain the simple optical-reading direction, but narrow the
contribution. Several formulas are exact specializations of known discrimination
results. The strongest remaining candidates are the joint input-retuning reduction
and the multiclass all-classical-source converse. This is a completed bounded
comparison, not a worldwide priority certificate.**

Baseline: `80c73751806f45411251711bcfb6bccebc887f0a`.
Branch: `audit/novelty-01`. Only `audits/novelty-01/` is changed. No canonical
proof, code, protocol, previous audit, or frozen result was modified. No merge,
new research extension, external correspondence, experiment, manuscript, license,
or public release is included.

## 1. The comparison changes the paper's center

The existing mechanism is not a new family of quantum optimizers. Single-photon
Hadamard phase reading, fixed square-root measurements, displacement receivers,
and error/inconclusive optimization all have direct predecessors. Those facts
must be the starting point of a paper, not qualifications hidden at its end.
Sources S01-S15 document the relevant primary statements.

The useful residual question is instead:

> Under a declared lossy optical map and signal budget, what part of joint
> transmitter/receiver optimization collapses to a simple design rule, and what
> performance can every classical transmitter and receiver be ruled out from
> attaining?

Two distinctions matter throughout: optimizing a measurement for a fixed set of
received states is not the same as choosing the input before a lossy unknown
operation; and optimizing a practical nulling receiver is not the same as bounding
all classical probes, all POVMs, and unbounded intensity mixtures.

The complete [claim map](CLAIM_MAP.md) classifies eighteen result/headline units.
The [reductions](REDUCTIONS.md) show the actual substitutions, not merely similar
titles or general claims about broad frameworks.

## 2. Decisive inherited results

### The uniform classical curve is not a new fixed-state formula

Herzog's 2012 Eq. (4.18) [S07] becomes the repository's four-state curve exactly
when N=4, S=exp(-t mu), and Q=F. Converting from failure probability to allowed
error produces

$$
C=(\sqrt{1-e^{-t\mu}}+\sqrt{E/3})^2
$$

on the curved branch, with the same square-root minimum-error endpoint. The
fixed-alphabet curve and measurement should be credited as a specialization.
This does not dispose of the separate claim that no *different classical input*
or intensity mixture can beat that alphabet under the stated mean budget.

### The fixed decoder and zero-error compensation have short prior reductions

For arbitrary input probabilities, the received Gram square root has constant
diagonal. Eldar and Forney's known SRM criterion [S04] identifies the fixed code
decoder. For Fourier codes, Chefles and Barnett's minimum-coefficient rule [S02]
immediately yields the zero-error endpoint; standard Gram positivity extends the
argument to the remaining flat codes. Normalizing the source gives the harmonic
mean. These are useful design explanations, not independent new principles.

### The binary spectral contrast is already an optical design object

Bouchet and colleagues [S11] optimize coherent wavefronts with
(A2-A1)-dagger(A2-A1). The repository's m=2 contrast is exactly half that operator.
The exponent and Helstrom probability agree after this factor is accounted for.
It is incorrect to introduce the binary contrast matrix or its top eigenvector
as new. For more labels the repository uses an average contrast to produce a
bound; it does not solve arbitrary multiclass input optimization by diagonalizing
that matrix.

### Loss-aware design and reliability tradeoffs are established contexts

Hashimoto and colleagues [S05] explicitly formulate joint input/measurement
optimization with an error margin. Nair and Yen [S06] optimize image-sensing probes
in loss with a larger signal-idler class. Primaatmaja and colleagues [S09] include
a loss coda and discuss how the preferred probe changes; their paper is not simply
a lossless comparison. These works do not automatically give our restricted
closed-form solution, but they rule out broad first-of-kind framing.

Melo and colleagues [S15] already scan optimal error/inconclusive tradeoffs in
path optics. Their experiment uses a laser and cameras and explicitly states its
classical-field emulation interpretation. It must not be confused with our still
unperformed, resource-matched single-photon/classical-source test.

## 3. Candidate contribution A: put the variable part in the input

The strongest compact mechanism statement is:

> For a flat orthogonal phase code and hypothesis-independent diagonal loss,
> retuning the normalized incident photon is sufficient: one fixed code decoder
> attains the globally optimized reliability tradeoff in the specified photon
> architecture.

The exact largest-eigenvalue formula is already proved and repaired in the
canonical theory. The comparison explains what is left after crediting the SRM:
a general conclusive measurement has diagonal weights w_i<=1. The photon score
is upper-bounded by a quadratic form in sqrt(p_i w_i). Normalizing those weights
into a new input p_i'=p_i w_i/sum(pw) removes the need to retain a successful
receiver filter on the positive-score branch. Common-vacuum guessing has its
separate, explicit segment.

That is a model-specific reduction, not merely a plot of a known fixed-ensemble
POVM. It also does not assert that a given input has the same optimum at every
error allowance. Input tunability and pre-device normalization are indispensable.

The cited fixed-state theorems do not state this complete contract. The bounded
search did not establish a prior theorem that subsumes it exactly. It is therefore
retained as a candidate technical contribution, not labelled unconditionally new.
Its proof is short enough to make the physical idea clearer rather than adding a
new optical component.

## 4. Candidate contribution B: compare against the source class, not one laser

The calibrated-map bound uses the actual coherent map differences, an inequality
for measured correct/error/failure probabilities, and concavity in pulse energy.
It covers arbitrary nonnegative coherent mixtures, preparation labels available
to the receiver, phase references, and arbitrarily rare bright pulses under the
mean signal budget. The broad class cannot be replaced by the experimentally
implemented control when stating an advantage.

Every ingredient has precedent: Gram/fidelity arguments [S10,S14,S19], binary
contrast [S11], and basic concavity. The candidate is the particular multiclass
optical composition, its tight uniform four-symbol specialization, and its use
with declared calibration bounds. Do not advertise the triangle inequality,
Jensen's inequality, or the fixed-N Hoeffding step as separate discoveries.

The published fixed-alphabet formula in S07 answers what happens *after* a
specific alphabet is supplied. It does not itself prove that an adversary cannot
change illumination or use bright flashes. That is the nontrivial scope boundary
of the optical converse. Conversely, the general calibrated-map bound is not
claimed to be an exact optimal frontier for arbitrary maps.

The exact one-bad-path zero-error comparison in checkpoint 06 is a supporting
case. The nulling receiver's water-filling allocation is ordinary KKT calculus.
What must remain is the global POVM and mean-mixture argument, including its
high-energy branch. At one checked pulse energy the true allowed POVM attains
0.82447 while optimized nulling gives only 0.73626. Bounding only nulling would
therefore be an invalid all-classical proof. The canonical supporting-line proof
already addresses that branch; this audit makes the distinction explicit.

## 5. What the first experiment should test after this comparison

There is no reason to replace the fixed four-mode optical core or add a learning
loop. The novelty comparison changes what the data are intended to demonstrate.

Use the known uniform/alphabet and uncompensated cases as controls. The substantive
mechanism test is the *predicted pre-device input redistribution* as the loss
profile and error penalty change, while the receiver stays fixed. The positive
test must compare the unconditional measured score with the all-source bound,
not only an implemented coherent control. The reverse test remains an actual
coherent strategy above the entire restricted photon bound, not evidence against
all quantum architectures.

The existing proof and repair audits already separate nominal numerical results,
rigorous photon support endpoints, physical calibration, and experimental data.
This comparison does not change those distinctions. Single-use hidden labels,
phase references, signal-energy planes, and no-click accounting remain part of
the task. A stable-label repeated-reading experiment or a healthy fifth hypothesis
would require a different theorem.

For a future contribution note, a defensible emphasis is **input-only optimal
retuning plus an all-classical illumination certificate for a lossy phase-reading
task**. Avoid claiming a new optical reading mechanism, a new general reliability
framework, the first spectral scattering contrast, or a fully solved arbitrary
bosonic discrimination problem. The uniform curve should be stated as a credited
corollary with a separate source-optimality argument.

## 6. Coverage, execution, and limitations

The source inventory contains 21 primary references. Eighteen had relevant
full-text passages inspected (two of these recent works were used only for formal
scope screening); S18 and S21 were abstract/bibliographic scope screens, and S20
was checked via its publisher abstract and its explicit attribution/equation in
primary source S19. No source was declared fully excluded on abstract evidence.
Herzog, Bagan, and Primaatmaja full PDFs were recovered after previous HTML gaps.
Searches also included older joint-channel/input literature, binary scattering,
coherent USD, and 2025-2026 developments. The record is not an exhaustive citation
network or unpublished-work search.

The original S20 full text and the full appendix comparison for S18 remain gaps.
The general multiclass error/failure overlap bound could have additional prior
forms not caught by title searches. These limitations prevent a worldwide
priority certificate; they do not prevent the explicit inherited classifications
or the concrete reductions already established here.

Focused code checks produced 631 passing scalar comparisons across seven groups.
A second execution in a new directory reproduced RESULTS.json byte for byte.
The maximal residual was approximately 2.71e-10 against a declared 1e-9 tolerance.
These checks validate variable translations and example comparisons, not novelty,
formal proofs, or a complete rerun of the earlier scientific audit.

The code used hash-matched selected source from the supplied repair archive.
Its THEORY.md, theory.py, and photon_support.py Git blob identities were checked
against the pinned remote baseline before and after computation. Container Git
access failed at DNS resolution; no authenticated local clone or local clean Git
status is claimed. Only the new audit directory was written remotely. Branch CI
is the unchanged repository regression/repair workflow; its success does not
mean that it executed this new comparison script.

## 7. Completion decision

**Proceed with narrowed contribution statements, not another apparatus search.**
The next authorized development step can integrate the source map and revise the
reader-facing claim wording, then produce a short two-claim contribution note and
matching lab-review rationale. That integration has not been done here. The
original canonical ledger still records novelty as unestablished.

No fundamental priority guarantee, external specialist endorsement, measured
advantage, or journal outcome follows from this report. This task stops after
committing the bounded comparison and preserving its reproducible evidence.
