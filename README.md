# Loss-Aware Optical Reading

**Change the incident photon, keep the receiver fixed, and test when classical
illumination cannot match the result.**

One photon enters four optical paths. Exactly one path receives a phase flip.
A fixed interferometer turns the returned pattern into a path label. A missing
or rejected output remains an inconclusive trial. The task is to choose the
input distribution for the measured losses and the required reliability.

## The two results to assess

**A. Input-only optimal retuning.** For a flat orthogonal phase code, uniform
labels and known diagonal loss, changing the input amplitudes is sufficient to
attain the joint input-and-measurement optimum. The code decoder stays fixed.
At larger error allowances, the decision rule may also guess on empty outputs.
This is a result within a specified single-photon architecture, not arbitrary
optical sensing.

**B. An all-classical illumination bound.** A bound on correct and wrong answers
covers nonnegative coherent-state mixtures, arbitrary receivers, phase references
and rare bright pulses under a mean incident signal-energy budget. It is exact
for the uniform-loss four-symbol task; the general-map bound need not be tight.

These statements have analytic proofs and a completed bounded mathematical
audit. They are **candidate contributions**, not cleared priority claims.
The [two-claim note](docs/CONTRIBUTIONS.md) separates each statement from its
predecessors. The [current source map](SOURCE_AUDIT.md) records exact reductions
and the remaining coverage gaps. The optical reading mechanism, fixed-alphabet
uniform curve and square-root measurement are inherited results.

**Stage:** theory, numerical validation and an initial technical laboratory-review
proposal. There are no acquired laboratory data. The repository is private;
publication novelty and actual hardware/calibration remain unverified.

## Start here

| Purpose | Entry point |
|---|---|
| Understand the contribution | [Two-claim note](docs/CONTRIBUTIONS.md), then [scientific report](REPORT.md) |
| Check the reasoning and scope | [Claim ledger](CLAIM_STATUS.md), [proofs](proofs/THEORY.md), [source map](SOURCE_AUDIT.md) |
| Review the experiment | [Lab brief](experiment/LAB_REVIEW.md), [claims to tests](experiment/CLAIMS_TO_TESTS.md), [full protocol](experiment/FIRST_EXPERIMENT.md) |
| Reproduce or continue | [Reproduction guide](docs/REPRODUCE.md), [current work order](work_orders/CURRENT.md) |

## The physical task

The four equally likely operations and the fixed decoder are

$$
O_j=I-2|j\rangle\langle j|,\qquad D=\frac12J-I,
$$

where every entry of the four-by-four matrix $J$ is one. There is no fifth
healthy hypothesis. One photon across four paths is one four-dimensional carrier,
not four separately carried qubits.

The platform is SU(4)/SU(8)-first, with one computational photon at a time.
The photon theorem excludes an occupied bypass rail, retained idler and repeated
interrogation of one hidden setting. Existing larger mode processors are eligible
when useful, but multiphoton computing, memory and recirculation are not assumed.
The [physical setting](docs/PHYSICAL_SETTING.md) gives the complete boundary.

The classical comparator is not restricted to the laser receiver implemented in
the lab. Signal energy is charged immediately before the unknown section, and
our downstream receiver losses cannot be used to weaken its allowed performance.
Preparation, the hidden operation and the receiver must be independently controlled.
Each counted interrogation receives a fresh hidden label. All attempted trials,
including no-click and multiple-click records, remain in the denominator.

## What the first experiment would test

The mechanism test changes the input while leaving the decoder fixed. A positive
test compares unconditional measured performance with the all-classical bound.
A separate severe-imbalance test uses an implemented coherent receiver to challenge
the entire declared photon class. These are M1, P1 and P2 respectively in the
[unchanged acquisition protocol](experiment/FIRST_EXPERIMENT.md).

Known uniform-loss curves are controls, not the principal novelty claim. Numerical
agreement with a predicted optimum is not a new proof of global optimality.
A missing coherent-displacement capability limits P2; it does not authorize an
unmatched substitute. Lab feedback precedes pilot calibration and held-out data.

## Reproduce without replacing the evidence

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-test.txt
python scripts/verify_import.py
python -m unittest discover -s tests -v
python scripts/reproduce.py
python repairs/theory-01/verify.py --output results/runs/repair-01
python audits/novelty-01/comparison_checks.py --source-root . --output results/runs/novelty-01
```

Named output directories must be new. The recorded environment is Python 3.13.5,
NumPy 2.3.5 and SciPy 1.17.0, with test-only mpmath 1.3.0. The inherited 5,261
checks, preserved historical audit and repaired scientific cases have separate
roles. The 631 predecessor-translation checks validate algebraic translations,
not originality. [Reproduction details](docs/REPRODUCE.md) state the tolerances.

The photon-support routine returns nominal recipes separately from outward-safe
support bounds. Only the specified calculation has exact-rational enclosures;
the complete statistical or experimental pipeline is not machine-certified.
Read the [numerical contract](docs/NUMERICAL_CONTRACT.md) before using an upper bound.

## Evidence and next work

`results/hypothetical_*` are forecasts; `results/synthetic_*` are synthetic
examples, not observations. New outputs go under ignored `results/runs/`.
The original archives, frozen tables, mathematical audit, repair and predecessor
comparison are preserved. [Integration record](integrations/claims-01/REPORT.md).

The next bounded task is to close the outstanding predecessor checks, not to add
an optimizer or more modes. Exact arbitrary-loss classical finite-error optimality,
adaptive total-dose advantage and actual measured advantage remain unestablished.
[Roadmap](docs/ROADMAP.md). No redistribution license has been selected.
Contact: gogoko699@gmail.com.
