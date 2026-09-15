# Theory from the experiment

The laboratory has both an SU(4) chip and an SU(8) chip. Start with the
[SU4 route](../experiment/SU4.md) or the [SU8 route](../experiment/SU8.md).
This page explains what their records mean. No external reading is required.
The [reading crosswalk](READING_CROSSWALK.md) offers optional engineering and
discrimination background; [the canonical proofs](../proofs/THEORY.md) retain
the complete statements and assumptions.

## 1. The question asked by one photon

There are four paths, numbered 0, 1, 2, 3 in the reference convention. One
fresh hidden label j is drawn uniformly for each attempted interrogation.
The hidden section changes the phase of path j by pi. The reader knows the
four possible operations and their probabilities, but does not know the current
label. A click at decoder output j means “the label was j.”

These are four modes occupied by **one photon in total**. They are not four
photons or four independently carried qubits. There is no fifth “no change”
hypothesis. The laboratory maps these reference indices to its physical ports
before acquisition; [interfaces](../experiment/INTERFACES.md) lists the inputs
still needed for that mapping.

Choose nonnegative probabilities p_i adding to one and prepare

```math
|\psi\rangle=\sum_{i=0}^{3}\sqrt{p_i}\,|i\rangle.
```

Relative input phases are fixed in this convention. Known preparation phases
can be compensated before freezing the receiver; the source cannot use j.
The ideal device between the signal-accounting plane P0 and the accessible
output plane P1 has

```math
O_j=I_4-2|j\rangle\langle j|,\qquad
T=\mathrm{diag}(\sqrt{\eta_0},\ldots,\sqrt{\eta_3}),
\qquad 0<\eta_i\leq1.
```

O_j is a phase operation. T describes label-independent loss and is a
contraction; programming unitary phases does not implement T. The
[commissioning recipe](../experiment/COMMISSIONING.md) checks transformations,
and the [uncertainty worksheet](../experiment/UNCERTAINTY.md) distinguishes
device loss from preparation, receiver, and detector imperfections.

## 2. What returns, including the lost photon

The unnormalized surviving vector and its probability are

```math
|\phi_j\rangle=T O_j|\psi\rangle,\qquad
s=\langle\phi_j|\phi_j\rangle=\sum_i\eta_i p_i.
```

The full state available at P1 is

```math
\rho_j=|\phi_j\rangle\langle\phi_j|
 +(1-s)|\mathrm{vac}\rangle\langle\mathrm{vac}|.
```

The vacuum term is the same for every label in this model, so it carries no
label information. It still occurs on a counted attempt. Dividing the surviving
block by s describes a detection-conditioned ensemble, and would change the
operational question if used in place of rho_j.

For a fixed input, the four states rho_j with priors 1/4 form the **received
ensemble**. A generalized measurement is described by positive effects
Pi_0 through Pi_3 and Pi_?, adding to the identity on the accessible state space.
The probability of record k under label j is the trace of Pi_k rho_j. The
question mark means that no label is reported.

Before optimizing anything, define the three unconditional rates:

```math
C=\frac{1}{4}\sum_j\mathrm{Tr}(\Pi_j\rho_j),\qquad
E=\frac{1}{4}\sum_j\sum_{k\ne j}\mathrm{Tr}(\Pi_k\rho_j),
```

```math
F=\frac{1}{4}\sum_j\mathrm{Tr}(\Pi_{?}\rho_j),\qquad C+E+F=1.
```

Here k in the error sum runs over conclusive labels. C is correct, E is wrong,
and F is inconclusive, all per attempted interrogation. Actual records also
include multiple clicks, leakage, and rejected records; the registered rule
keeps these attempts and assigns their outcome. They do not disappear from
the denominator.

A wrong-answer penalty lambda, fixed before testing, defines

```math
S_\lambda=C-\lambda E.
```

A correct answer scores 1, a wrong answer scores minus lambda, and an
inconclusive answer scores 0. A clock or source herald before exposure defines
an attempt. An output coincidence cannot define it retrospectively. The
[first-experiment protocol](../experiment/FIRST_EXPERIMENT.md) gives the fixed-N
rules, pilot/test separation, blinding, and original confidence allocation.

## 3. What the fixed decoder does

Let J_4 be the all-ones matrix and use

```math
D_4=J_4/2-I_4.
```

With equal loss eta_i=t and p_i=1/4, the returned photon reaches output j
with certainty **when it survives**. Unconditionally, the no-click-as-failure
rule gives C=t, E=0, F=1-t. At t=1 this is perfect label routing.

Unequal loss changes the surviving path amplitudes. To remove their imbalance,
choose p_i proportional to 1/eta_i. Then every surviving amplitude has equal
magnitude again. The same decoder gives the zero-error endpoint

```math
H_\eta=\frac{4}{\sum_i1/\eta_i},\qquad
C=H_\eta,\quad E=0,\quad F=1-H_\eta.
```

More input weight goes into weak paths. This does not recover lost photons:
it changes the incident state, and its survival probability remains in the
score. If some errors are acceptable, exact balancing need not maximize the
score. That is the purpose of [M1](../experiment/M1.md).

## 4. Two different optimization questions

| Question | What may change? | What must be established? |
|---|---|---|
| Best receiver for a fixed received ensemble | Measurement only; input and device fixed | An upper bound over measurements and a measurement attaining it. |
| Best permitted photon strategy | Input and final measurement; device and resource contract fixed | An upper bound over both choices and an attaining preparation/receiver. |

The fixed-input square-root measurement is an established ingredient. The
zero-error inverse-loss endpoint is also credited prior work and a short
specialization. **A, the leading candidate contribution, concerns the complete
input-only retuning reduction for the joint problem**, under its exact
assumptions. It does not claim that state discrimination or this decoder is new.
See [contribution boundaries](CONTRIBUTIONS.md) and the
[completed predecessor reductions](../audits/novelty-02/REDUCTIONS.md).

For the four-path task, let v_i=sqrt(eta_i). For lambda at least 1/3, form

```math
B_\lambda=\frac{1+\lambda}{4}vv^T-\lambda\,\mathrm{diag}(\eta).
```

Its largest eigenvalue beta_q(lambda) is the optimum score over every permitted
input and final measurement. If z is its normalized positive top eigenvector,
prepare p_i=z_i^2. Keep D_4 fixed and call vacuum inconclusive. The achieved rates
are

```math
C=\frac{1}{4}\left(\sum_i\sqrt{\eta_i p_i}\right)^2,\qquad
E=\sum_i\eta_i p_i-C,\qquad F=1-\sum_i\eta_i p_i.
```

The proof first bounds every receiver, then shows that this preparation and
decoder attain that bound. In particular, allowing receiver filtering does not
improve the joint optimum. This is stronger than numerically finding a good
input for one chosen receiver. [Theorem 1](../proofs/THEORY.md) supplies the
bound and equality argument without assuming a numerical optimizer is correct.

For smaller penalties, a random guess on vacuum can be useful. It is correct
with probability 1/4 and wrong with probability 3/4. Theorems 1–2 retain the
same decoder, choose the appropriate input, and specify when to guess on some
or all vacuum events. This completes the error-budget frontier. The M1/P1/P2
recipes keep their own registered decision rules; this explanation does not
change them.

The reduction assumes uniform labels, a square flat orthogonal phase code,
known positive diagonal loss independent of the label, and one photon in the
tested paths. An occupied bypass, retained idler, interacting extra photon,
quantum memory, or another use of the same hidden setting changes the task.
An arbitrary noisy chip need not satisfy this exact reduction. Use the
[uncertainty worksheet](../experiment/UNCERTAINTY.md), with the applicable
model-specific evidence, before interpreting a departure from the ideal curve.

## 5. A measured score, a ceiling, and an optimum

| Statement | Meaning in this repository |
|---|---|
| Achieved score | Performance of a specified preparation and receiver. A synthetic calculation is a prediction, not a measurement. |
| Upper bound or ceiling | No allowed strategy can exceed it under the stated assumptions. Attainment may be unknown. |
| Proved optimum | A universal upper bound and an allowed strategy attaining it agree. |
| Finite-data certificate | A registered statistical comparison using justified external calibration bounds; it is not automatic proof of those inputs. |

Receiver optimality for a photon ensemble does not imply a source-class
advantage. A coherent source produces a different returned ensemble and may use
a different receiver. [P1](../experiment/P1.md) compares our unconditional score
with a ceiling covering the full declared classical source class.
[P2](../experiment/P2.md) compares an implemented coherent receiver with the
ceiling for the entire declared four-path photon class.

## 6. Why the classical comparison is broader than a laser control

The classical class contains nonnegative Glauber–Sudarshan mixtures of coherent
signal states. The receiver may know the preparation's mixture label, use a
phase reference, and perform any permitted measurement. Rare bright pulses
remain allowed under the mean signal-photon budget mu at P0.

For actual passive coherent maps A_j from P0 to P1, define

```math
H_\Delta=\frac{1}{m(m-1)}\sum_{j<k}
(A_j-A_k)^\dagger(A_j-A_k),\qquad
\kappa=\|H_\Delta\|_{\mathrm{op}}.
```

The derived source-class benchmark B is

```math
C\leq\min\left\{1-E,
\left[\sqrt{1-e^{-\kappa\mu}}+\sqrt{E/(m-1)}\right]^2\right\}.
```

For the ideal four-label model, m=4 and kappa=max_i eta_i. A general-map
ceiling is not an exact frontier. The exact uniform-loss four-symbol frontier
has a separate attainment argument in [Theorem 5](../proofs/THEORY.md); not every
point is implemented by the proposed click receiver.

B is a **derived optical benchmark**, not an independently new general
discrimination theorem. Its source reductions credit Zhang et al. for the
zero-error overlap relation, Bagan et al. for the no-failure relation and the
conclusive-filter construction, and Herzog for the uniform fixed-alphabet
curve. [The source map](../SOURCE_AUDIT.md) preserves those reductions and the
resolved access qualifications. Numerical agreement does not establish priority.

Calibrate A_j in one shared optical phase convention across labels. Removing a
different global phase from each map can change coherent-state discrimination
relative to a reference. Our receiver/detector losses lower our achieved score;
they do not automatically lower an unrestricted competitor's P1 ceiling.
The symbol P1 here denotes the accessible plane when used in a block diagram
and the positive-comparison test when used as a recipe name.

Signal photons are distinct from herald photons, pump energy, reference power,
total apparatus energy, and wall-clock cost. The source energy/tail bound and
calibration coverage must be supplied independently. There is no
optional-stopping claim.

The preferred source can change with the decision requirement. At uniform
t=0.7 and incident budget mu=1, the exact ideal zero-error correct rates are
0.7 for a photon and approximately 0.5034146962 for classical illumination.
At the always-answer endpoint the exact ideal correct rates are 0.775 and
approximately 0.8586096698, respectively. These canonical examples are task
optima, not acquired data or a claim that the laboratory implements the
minimum-error coherent receiver.

## 7. What carries to the existing SU8 chip

**Route A uses the same four labels.** Occupy reference modes 0–3, leave inputs
4–7 in vacuum, and use D_4 direct-sum I_4 as the receiver. Output leakage into
modes 4–7 remains a recorded failure. Extra empty modes do not turn the task
into an eight-label result; see [SU8 route A](../experiment/SU8.md).

**Route B uses an actual eight-label flat phase code.** With i,j ordered as the
three-bit representations of 0 through 7, take

```math
Z_8[i,j]=(-1)^{i\cdot j},\qquad
O_j=\mathrm{diag}(Z_8[:,j]),\qquad
D_8=Z_8^\dagger/\sqrt{8}.
```

The binary dot product is evaluated modulo two. Columns have squared norm 8.
Two distinct columns have zero inner product: their product is a nonconstant
binary character, with four plus and four minus entries. Thus
Z_8^dagger Z_8=8 I_8. Uniform input amplitudes 1/sqrt(8), with unit transmission,
give D_8 O_j psi=e_j under exactly this port order. These are not eight
single-path flips.

The existing photon theorem therefore applies with m=8: replace 4 by 8 in the
matrix/rate formulas and use the vacuum-as-inconclusive branch for lambda at
least 1/7. In particular,

```math
B_\lambda^{(8)}=\frac{1+\lambda}{8}vv^T-\lambda\,\mathrm{diag}(\eta),
\qquad p_i=z_i^2,
```

and the zero-error correct rate is 8 divided by the sum of inverse
transmissions. This is a specialization of the existing proof, with a separate
[eight-mode recipe and data format](../experiment/SU8.md). Eight-port records
must not be passed to the four-detector analyzer.

Ideal eight-label routing and the photon optimum establish neither an
eight-mode source-class advantage nor an exact eight-mode classical frontier.
The general-map benchmark retains its own assumptions and requires the actual
eight-label maps and comparison contract. The exact four-symbol classical
frontier and four-mode robustness results are not eight-mode results.

Return to the [experiment index](../experiment/INDEX.md) to choose a procedure.
The chip/interface and uncertainty pages distinguish what can begin
commissioning from what is ready for statistically certified acquisition.
