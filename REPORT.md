# A first experiment for the loss–reliability boundary of single-photon reading

**Status: theory and a laboratory-review design, not experimental data.**
Scientific baseline: 2026-09-14. Reader-facing attribution updated after the
completed predecessor comparison. The first measurement campaign covers both
favorable and unfavorable regimes. The main mechanism remains a single photon, one passive mode decoder,
and final click detection. No iterative quantum optimizer is needed.

## Contribution and source status

The [two-claim note](docs/CONTRIBUTIONS.md) is the current contribution statement.
The fixed-input decoder, zero-error harmonic-mean endpoint, and uniform coherent
fixed-alphabet curve have direct predecessors. The two candidate additions are
the joint normalized-input/fixed-decoder optimum under unequal loss and the
multiclass bound over the allowed classical source class. Their mathematical
validity is supported by the theory audit; publication-level priority is not
established. [SOURCE_AUDIT.md](SOURCE_AUDIT.md) records the distinctions and
remaining coverage gaps. This update changes no equations or test settings.

## 1. Main result: retune the input, not the receiver

For an orthogonal phase code and known diagonal path losses, the entire optimal
single-photon error–inconclusive tradeoff can be attained with a fixed decoder.
Change the input amplitudes and, at the high-error end, how often an empty output
is assigned a random label. A more complicated quantum receiver cannot improve
this tradeoff within the stated single-photon architecture.

The first experiment uses four equiprobable phase operations

$$
O_j=I-2|j\rangle\langle j|,
\qquad
D=\frac12J-I.
$$

Exactly one path undergoes a pi phase flip. This is four-symbol phase reading,
not arbitrary fault diagnosis and not a five-hypothesis healthy/fault test.

Let $C,E,F$ be unconditional correct, wrong, and inconclusive probabilities.
Fix a wrong-answer penalty $\lambda$, and score each attempted interrogation
by $1,-\lambda,0$. For $\lambda\ge1/3$, define

$$
v_i=\sqrt{\eta_i},\qquad
B_\lambda=\frac{1+\lambda}{4}vv^T-\lambda\,\mathrm{diag}(\eta).
$$

The exact optimum, over every allowed input and final measurement, is

$$
\boxed{\max(C-\lambda E)=\lambda_{\max}(B_\lambda).}
$$

Prepare path probabilities $p_i=z_i^2$, where $z$ is the normalized positive
principal eigenvector, and keep the receiver at $D$. A scalar root equation
also generates the preparation, without optimizing an optical matrix. The
zero-error limit recovers inverse-transmission weighting and the harmonic mean
$4/\sum_i\eta_i^{-1}$.

At moderate imbalance $\eta=.7(1,1,1,.8)$, the zero-error preparation assigns
29.41% of the input probability to the weak path. The $\lambda=5$ preparation
assigns 27.82%. At stronger imbalance $\eta=.7(1,1,1,.2)$, that probability
changes from 62.5% at zero error to 45.71% at $\lambda=5$, and 19.38% at
$\lambda=1$. These are exact-model design choices, not fitted test data.

The proof is not a numerical search. Positivity of an arbitrary POVM bounds its
correct rate by a squared sum of amplitudes. Code orthogonality fixes the total
conclusive rate. The resulting quadratic form is bounded by its top eigenvalue,
and the fixed decoder saturates it. The same argument covers any square flat
orthogonal code, including proper eight-mode Hadamard or Fourier codes. Eight
one-path flips are not such a code.

This theorem assumes a photon in the interrogated paths, no occupied bypass or
idler, uniform prior, and hypothesis-independent diagonal loss. It does not
claim optimality for arbitrary measured chip channels. Source and hardware
imperfections enter the prediction and certificate separately.

## 2. The classical comparison is stronger than the implemented laser control

The classical class consists of nonnegative Glauber–Sudarshan mixtures of coherent
signal states. The receiver receives the preparation label, may have an optical
phase reference, and may perform any measurement. Pulse energies may be unbounded;
only the mean incident signal energy is charged. Pump energy, source heralds,
reference power, and laboratory time are different resource columns.

For uniform transmission $t$, the complete four-symbol classical finite-error
frontier is explicit in this model. Put $c=e^{-t\mu}$, with mean signal budget $\mu$.
Then

$$
P_{\mathrm{cl,ME}}=
\frac{[\sqrt{1+3c}+3\sqrt{1-c}]^2}{16}.
$$

Before the minimum-error endpoint, the exact optimum is

$$
C_{\mathrm{cl}}^*(\epsilon)=
\left[\sqrt{1-c}+\sqrt{\epsilon/3}\right]^2.
$$

It is capped at $P_{\mathrm{cl,ME}}$ when $\epsilon\ge1-P_{\mathrm{cl,ME}}$.
A matching physical POVM certificate is supplied. The upper bound includes
intensity mixtures, not only the equal coherent pulse used to attain it.

For $t=.7,\mu=1$, the photon wins at zero error: .7 versus .5034146962.
When an answer is mandatory, it loses: .775 versus .8586096698. The receiver
attaining the coherent minimum-error number is an abstract quantum measurement;
the report does not assume that our four-click classical control implements it.
The fixed-alphabet curve is exactly Herzog's Eq. (4.18) after the substitution
recorded in [reduction R4](audits/novelty-01/REDUCTIONS.md). The separate
source-class claim rules out alternative coherent transmitters and intensity
mixtures. The curve and its square-root measurement are not claimed as new.

## 3. A certificate from actual phase-referenced device maps

For calibrated passive maps $A_j$, let

$$
H_\Delta=\frac1{m(m-1)}\sum_{j<k}(A_j-A_k)^\dagger(A_j-A_k),
\qquad \kappa=\|H_\Delta\|.
$$

For any allowed classical source and receiver,

$$
\boxed{C\le\min\left\{1-E,
[\sqrt{1-e^{-\kappa\mu}}+\sqrt{E/(m-1)}]^2\right\}.}
$$

This is generally an upper bound, not an exact arbitrary-device optimum. It
allows unequal and even hypothesis-dependent attenuation, subject to the
specified passive coherent-map model and inaccessible loss environment. For
the ideal four-one-flip code, $\kappa=\max_i\eta_i$.

The proof combines coherent-state overlaps, measurement fidelity, and concavity.
It therefore covers rare bright pulses analytically. A bounded numerical scan
would not do so. The binary contrast is an established scattering-discrimination
operator up to normalization; the multiclass average is used here as a converse
quantity, not a proved globally optimal source-selection rule. See
[reduction R6](audits/novelty-01/REDUCTIONS.md).

If simultaneous calibration gives $\|A_j-\widehat A_j\|\le\epsilon_j$, a
rigorous bound is

$$
\kappa_U=\left[\sqrt{\widehat\kappa}+
\sqrt{\frac{\sum_{j<k}(\epsilon_j+\epsilon_k)^2}{m(m-1)}}\right]^2.
$$

At $m=4,\lambda=5$, the simpler registered score bound is

$$
C-5E\le \frac{15}{14}(1-e^{-\kappa_U\mu_U}),
$$

capped at one. This bound is deliberately conservative. A violation establishes
an advantage even when the exact unequal-loss classical frontier is unknown.

### A phase convention is part of the comparator

Replacing just $A_0$ by $-A_0$ leaves every single-photon output density
matrix unchanged, but changes the ideal contrast from 1 to 4/3. A coherent probe
with a phase reference can observe that difference. Independently normalizing
each hidden setting into SU(4) can therefore change the classical task without
changing the single-photon pattern.

All hidden settings must be calibrated against one common optical phase
reference. Averaging fluctuating amplitude matrices is not automatically a
valid noise model either. A proved common post-encoding noise channel is allowed;
label-dependent drift and side channels need their own simultaneous bounds.

## 4. The first experiment has two primary tests and one mechanism test

| Test | Purpose | Required optical operation |
|---|---|---|
| P1: moderate imbalance | Certify a measured photon score above every allowed classical-probe strategy | One-photon preparation, hidden section, fixed D, four click detectors |
| P2: severe imbalance | Show an actually implemented coherent receiver above the entire specified photon-class ceiling | Known coherent preparation, hidden section, fixed background displacement, click detection |
| M1: input-only retuning | Test the predicted change of best preparation as the error penalty changes | The same photon receiver, several preregistered input vectors |

A suitable initial grid is $\eta=t(1,1,1,r)$, with $r\in\{1,.8,.5,.2,.05\}$
and an experimentally attainable $t$. These are provisional design points,
not hardware specifications. The actual values and run sizes must be frozen
using independent pilot calibration before held-out acquisition.

P2 compares an achieved coherent score against a proved single-photon upper
bound, not merely against the tested photon circuit. In the severe nominal
case $t=.7,r=.05,\lambda=5$, that ideal photon ceiling is .1860224979. A
simultaneous map-radius allowance .003 raises the conservative ceiling to
.2220224979. This excludes only the declared one-photon architecture, not every
possible quantum probe.

Displacement requires a phase reference and couplers. It is an additional
classical receiver capability to confirm with the lab, not an assumed current
inventory item. If unavailable, the reverse comparison remains theoretical;
a laser run through D cannot be substituted and called equivalent.

The physical layout must have separate source/preparation, unknown-operation,
and receiver roles. A source herald can define a trial before exposure. A
successful output click cannot define one retrospectively. The existing project
review already asks about separate/cascaded sections; a generic matrix compiler
does not by itself supply this interface.

## 5. Preregistration and finite data are part of the design

For a preselected penalty and fixed N, let $\widehat S$ be the mean trial score.
A conservative lower confidence bound is

$$
\widehat S-(1+\lambda)
\sqrt{\frac{\log(1/\alpha_{\mathrm{stat}})}{2N}}.
$$

This follows from the bounded-score Hoeffding argument given in the proofs. It
is not a normal approximation to the detected-event ratio. It requires the
stated independent-trial model or a separately validated conditional predictable
energy contract. An unconditional mean for a random run-wide bright regime is
not enough for an iid or martingale conclusion.

A provisional familywise allocation is .0005 for simultaneous calibration
failures and .00025 for each of the two primary statistical tests. The combined
false-certification probability is then at most .001 under those assumptions.
These probabilities must be supplied by a valid calibration procedure; the
simulation does not create them.

The acquisition protocol requires fresh independent uniform hidden labels for
each interrogation, a label-blind preparation and decoder, fixed input windows,
all no-click and multiple-click records, and no stopping when significance first
appears. An unbounded classical energy mixture is included theoretically, but
finite click samples alone cannot certify the absence of an unbounded source
tail. Independent energy metering or a justified stable-source/tail model is
necessary.

The raw CSV and two plan templates are provided. The analyzer checks accounting,
IDs, fixed N, and approved settings, then calculates the conditional certificate.
It does not verify source tails, phase calibration, or blinding by reading a JSON
field. Example plans are explicitly synthetic and cannot be analyzed as real
experiments without changing the approval declaration.

## 6. Hypothetical feasibility calculation

The positive example uses source probabilities (.029,.97,.001) for 0,1,2 photons
in one prepared spatial mode, mean .972, budget upper .98, post-device survival
and detection .92, dark probability 1e-6 per detector gate, and independent path
phase noise .035 radians shared within a pulse. The static map-radius allowance
is .003. Common phase noise and static map uncertainty are distinct assumptions.

At the moderate-imbalance point the exact finite-support model predicts

$$
C=.59005719,\quad E=.000707285,\quad F=.40923552.
$$

The predicted score is .58652077 versus a classical upper bound .53562201.
The non-primary coherent controls at the other grid points use the same nominal
mean .972 and upper budget .98; P2 deliberately uses a different one-photon-budget
comparison. The energy columns must not be silently interchanged.
At 500,000 trials the registered statistical allowance is .01727964. Even after
an extra .002 subtraction removing every possible positive contribution from
the declared multiphoton tail, rounded expected counts leave a margin .03162.
This is a synthetic calculation, not an observed violation or a claim that the
lab will meet those source and calibration values.

For the negative example, a coherent control is intentionally operated at
nominal mean .99 so calibration can upper-bound it by one. With the same phase
noise and readout factor, plus Poisson leakage intensity 1e-4 per output, its
predicted score is .42648719. The robust photon ceiling is .22202250. At 50,000
trials, rounded expected counts still exceed that ceiling after the statistical
allowance by .14983. Optical displacement fidelity remains a lab question.

Vacuum dilution is a real feasibility restriction. It reduces the useful
single-photon rate while also reducing the fair classical energy budget. Keeping
only output coincidences would conceal rather than repair this issue.

## 7. Verification and completion status

The original checkpoint-07 record reports an unchanged checkpoint-06 rerun
with 4,453 passing checks and a 5,261-check validation of that package. Its maximum algebraic residual is
about 1.01e-12; the largest independent constrained-dual solver gap is 3.51e-12.
The independent solver is SciPy SLSQP with explicit positivity constraints, not
a semidefinite-program solver. A 75-digit Decimal calculation checks a separate
rational two-by-two reduction. Full photon-number/detector laws and Gaussian
coherent-control integration are checked with independent implementations.

The main claims have analytic proofs. Random tests and parameter searches are
supporting diagnostics, not universal certificates. The later
[independent audit](audits/theory-01/REPORT.md) and
[bounded repair](repairs/theory-01/REPORT.md) now provide exact-rational outward
photon-support enclosures within the documented domain. This does not interval-
certify every classical or statistical routine. No outside referee, formal proof
assistant, experimental run, or device-availability confirmation is claimed.
The original numerical record above remains historical evidence, not a fresh
execution claimed by this wording update.

The first two experimental comparisons no longer depend on an unproved exact
finite-error classical solution for arbitrary unequal loss. That broader
frontier remains open in this package; adaptive repeated reading and arbitrary
noisy bosonic-channel optimization remain separate extensions. Priority and
publication novelty are not settled by numerical reproducibility. Optical
reading, error-margin optimization, and symmetric-state receivers have direct
predecessors identified in the [current source map](SOURCE_AUDIT.md).

The next external step is an initial laboratory review of the preparation–hidden
section–receiver separation, common-phase calibration, source energy/tail
characterization, gated trial rate, and displacement control. A specialist
independent reading of the main proofs should precede a manuscript novelty claim.
The experimental mechanism need not become more complicated while those checks
are completed.

## Reading routes

- Candidate contributions: [docs/CONTRIBUTIONS.md](docs/CONTRIBUTIONS.md)
- Laboratory rationale: [experiment/REVIEW_RATIONALE.md](experiment/REVIEW_RATIONALE.md)

- Full protocol: [experiment/FIRST_EXPERIMENT.md](experiment/FIRST_EXPERIMENT.md)
- Mathematical proofs: [proofs/THEORY.md](proofs/THEORY.md)
- Claim status: [CLAIM_STATUS.md](CLAIM_STATUS.md)
- Primary sources and novelty limits: [SOURCE_AUDIT.md](SOURCE_AUDIT.md)
- Reproduction and analysis commands: [README.md](README.md)
