# A single-photon phase-fault reader with an explicit loss boundary

## Result and status

A four-path single-photon receiver is compatible with the project's revised
hardware scope. The task is to identify which one of four paths has acquired a
pi phase flip. Known path losses are compensated in the input preparation, and
one fixed interferometer converts the fault label into an output port.

The basic phase-to-port mechanism is known [S1,S2]. The potentially distinctive
result is the exact nonuniform-loss comparison: the photon strategy compensates
the weakest path, whereas an optimal coherent transmitter can reduce or abandon
illumination of that path. For three equally transmitting paths and one weaker
path, the calculation gives an exact crossover, even allowing arbitrary
classical coherent-state mixtures, rare bright pulses, and arbitrary receivers.

This is a validated research candidate, not a novelty-cleared final project or
a laboratory-ready specification. Primary-source details are in
`SOURCE_AUDIT.md`; derivations are in `proofs/PROOFS.md`.

## 1. Task, score, and photon budget

One of four hypotheses j=0,1,2,3 is selected uniformly. The unknown section applies
O_j=I-2|j><j|. It is promised that exactly one flip occurred. A fifth healthy
hypothesis is not included.

The receiver can return j or say inconclusive. In the ideal benchmark, it must
never return a wrong conclusive label. The score is the average probability of a
conclusive answer per attempted interrogation. Empty and discarded events count.
The comparison does not condition on receiving a click.

The quantum probe has exactly one photon over the four interrogated paths.
The classical competitor has a mean of at most one signal photon over those
same paths. It may use arbitrary coherent-state mixtures, arbitrarily bright
rare pulses, an external phase reference, known classical source labels, and
any physically allowed quantum measurement. The competitor is not restricted
to direct detection or to phase-randomized light.

This budget counts signal photons entering the unknown section, not pump energy,
source heralds, calibration data, or total apparatus energy. There is one pass
through the unknown device. Extra quantum reference paths or idlers are outside
the stated four-mode photon optimality theorem. The quantum advantage of this
explicit four-path implementation is still compared with the larger classical
probe class described above.

## 2. The optical mechanism

Prepare amplitudes a_i in the four paths. With transmissions eta_i, choose

\[
|a_i|^2=\frac{1/\eta_i}{\sum_k1/\eta_k}.
\]

The surviving amplitudes are then balanced, independently of which path was
flipped. Apply the fixed unitary

\[
D=\frac12J-I.
\]

For each hypothesis,

\[
D\operatorname{diag}(\sqrt{\eta_i})O_j|a\rangle
=\sqrt{Q_q}|j\rangle,
\qquad Q_q=\frac4{\sum_i1/\eta_i}.
\]

A click identifies the fault; no click is inconclusive. The preparation sends
more probability into lossy paths but does not undo loss or create photons.

A Gram-matrix proof shows that Q_q is the best average no-error conclusive rate
for any input and any final measurement in the specified four-path one-photon
model. For a fixed input probability vector p, the exact rate is
4 min_i(eta_i p_i); maximizing it gives the inverse-loss allocation.

D can be factored into ordinary balanced path mixing and fixed phases, or
compiled as one 4 by 4 unitary in a programmable mesh [S5]. Its global phase can
be adjusted to meet SU(4) conventions.

## 3. Classical benchmark without an artificial weak receiver

For a coherent input carrying n_i mean photons in path i, let q_i=eta_i n_i.
The returned-state Gram matrix has off-diagonal entries exp[-2(q_j+q_k)].
Writing a_i=exp(-2q_i), its exact average no-error conclusive optimum is

\[
F(q)=\frac{4-\sum_i a_i^2+\delta^2}{4},
\qquad \delta=\max\{2\max_i a_i-\sum_i a_i,0\}.
\]

The proof includes a feasible measurement certificate and an equal-value PSD
upper-bound certificate. No numerical semidefinite solver was used.

The high-energy delta-positive term matters: simply optimizing a displacement
receiver at energy one would not exclude a transmitter that occasionally sends
a much brighter pulse. The calculation solves the pure-coherent optimization
for arbitrary pulse energy in the one-bad-path family and proves that a global
supporting line excludes improvement by arbitrary random intensity mixtures at
the required mean budget.

For eta=t(1,1,1,r), with 0<t<=1 and 0<r<=1,

\[
Q_{\rm cl}^*=B_r(t),
\]

where

\[
B_r(x)=
\begin{cases}
\tfrac34(1-e^{-4x/3}),&r\le e^{-4x/3},\\
1-\tfrac14(3+1/r)\exp[(\ln r-4rx)/(1+3r)],&r>e^{-4x/3}.
\end{cases}
\]

The attaining transmitter uses a concave energy-allocation rule. Its receiver
can displace the known unflipped background and detect the remaining signal.
Those receiver ingredients are standard [S4]. Their exact global optimality
here follows from the bounds, not from assuming all receivers take that form.

## 4. The strongest conclusion is the reversal under imbalance

The following values are hypothetical model parameters, not measurements of the
intended laboratory's chip. All rates include inconclusive trials.

| Path transmissions | Best four-path photon rate | Best classical-probe rate |
|---|---:|---:|
| (1,1,1,1) | 100.0000% | 63.2121% |
| (0.7,0.7,0.7,0.7) | 70.0000% | 50.3415% |
| (0.7,0.7,0.7,0.56) | 65.8824% | 48.5124% |
| (0.7,0.7,0.7,0.35) | 56.0000% | 45.8881% |
| (0.7,0.7,0.7,0.14) | 35.0000% | 45.5069% |

For the moderate-imbalance case (0.7,0.7,0.7,0.56), the photon input probabilities
are (4,4,4,5)/17. In contrast, the best coherent input assigns approximately
0.25873 photons to each good path and 0.22380 to the worse path.

For severe imbalance the coherent optimum stops illuminating the weakest path.
It is permitted to have lower or zero success on one label because the declared
score is an average over a uniform prior. Both competitors have the same score
and output contract; equal success for every label was not imposed on either.

The exact crossover is

\[
r_*(t)=\frac{b(t)}{4t-3b(t)},\qquad
b(t)=\tfrac34(1-e^{-4t/3}).
\]

For t=0.7, r_*=0.3171676307. The four-path photon strategy wins above that ratio,
and the classical strategy wins below it. This is a limit of the specified
architecture and score, not an impossibility theorem for quantum sensing.

## 5. A finite-error comparison survives a small phase error

The ideal no-error benchmark is not sufficient for an experiment. Let C, E,
and F be correct, wrong, and inconclusive probabilities, each per attempted
interrogation. For any classical probe mixture with mean incident energy mu
and with every path transmission at most t,

\[
C\le\min\{1-E,[\sqrt{1-e^{-t\mu}}+\sqrt{E/3}]^2\}.
\]

This bound is not generally tight for unequal losses. It nevertheless gives a
receiver-independent finite-error ceiling. The proof covers intensity mixtures
and coherent references, rather than assuming that every optical pulse is
randomly vacuum or nonvacuum.

For an illustrative independent Gaussian phase error of standard deviation
0.05 radians in each path, with eta=(0.7,0.7,0.7,0.56), the photon design gives:

| Outcome | Unconditional probability |
|---|---:|
| Correct conclusive | 65.75898% |
| Wrong conclusive | 0.12338% |
| Inconclusive | 34.11765% |

At that same wrong-answer budget and mean signal energy, every classical probe
in the defined class has correct-conclusive probability at most 53.26030%.
This is a theoretical noise screen, not predicted lab performance. Larger phase
errors eventually remove this sufficient certification. Full detector/source
noise and statistical uncertainty remain to be assessed.

## 6. Hardware alignment and what is not assumed

The useful path is

single-photon preparation -> separately controlled unknown phase section ->
fixed four-mode receiver -> four output click detectors.

No multiple simultaneous probe photons, auxiliary interacting photons, PNR
readout, in-flight feedforward, quantum memory, or recirculation is required.
An ordinary external source-herald event may be used to timestamp a trial; the
herald photon is not a computational ancilla. Source impurity and trigger losses
still require accounting before a physical claim.

The project already has a four-mode optical-fault proposal with questions about
balanced preparation, a 0/pi phase switch, separate/cascaded preparation and
receiver sections, MZI control, and held-out randomized trials. This candidate
extends its binary healthy-versus-fixed-fault setup to one-of-four fault labels.
The ability to choose each of four phase locations remains to be confirmed.

The phase index must not be supplied to the preparation or decoder software.
Compiling a different end-to-end matrix using the known fault index would not
test the proposed input-access advantage. The unknown section needs a genuine
independent physical/control interface.

The exact eta model is a diagonal loss channel before an ideal reader. Arbitrary
distributed internal mesh loss, output-dependent detector loss, dark clicks,
multiphoton contamination, and hypothesis-dependent attenuation are not already
covered by those four numbers. Uniform downstream loss can be charged as an
additional erasure, but more general noise needs a fresh model.

Coherent-light transfer measurements remain useful for calibration. Their
normalized intensities reproduce single-photon mode probabilities [S5]. The
quantum claim instead concerns the full conclusive/error/inconclusive record
under a finite incident-energy budget and a rigorously optimized classical
probe comparator. It does not claim that this small unitary is hard to simulate.

## 7. Independent validation

The archive contains analytic proofs and separately implemented checks:

- decoder identities, Gram bounds, and complete eight-mode single-photon loss
  dilations for 120 random transmission vectors;
- primal and dual PSD certificates for 224 coherent illuminations, including
  singular and bright-pulse examples;
- coherent Gram matrices reconstructed independently from photon-number series;
- 25 independent continuous source-allocation searches at different energies;
- 24 finite-grid linear programs over random pulse intensities, plus supporting
  line tests extending to high energy;
- random POVM tests and 108 explicitly constructed small-error POVMs for the
  error ceiling, crossover tests, and independent Gaussian quadrature of the
  phase-error formulas.

The archived run passes 4,453 assertions. The largest algebraic consistency
residual is 2.89e-15. The largest discrepancy between an independent numerical
source-allocation search and the proved optimum is 4.13e-11. Repeated grid-point
assertions are not independent experiments. No hardware data, SDP solver, or
interval-arithmetic certificate is claimed.

The exact all-energy and all-mixture statements come from the proofs, not from
a finite scan. In particular, a scan stopping at energy 100 would not alone
exclude rarer, brighter probes; the global supporting-line argument does.

## 8. Scientific interpretation and next boundary

The simple operational idea is to balance the *surviving* amplitudes, rather
than the input amplitudes, and read a phase fault through a fixed interference
pattern. Its cost is an exact harmonic-mean survival probability.

The optical-reading mechanism itself is old [S1,S2]. Energy-constrained optical
discrimination and coherent displacement receivers are also established [S3,S4].
A contribution would have to be the exact unequal-loss comparison, its
mean-budget guarantee and reversal, or a substantive extension of that result.
The bounded literature review has not certified those statements as new.

The next useful work is an independent theorem-level predecessor comparison and
a mapping of the ideal loss/noise contract to a realistic four-mode experimental
layout. Adding an optimizer, many more paths, or a learning label would not
resolve either issue. The existing project proposal has not been replaced or
modified by this checkpoint.
