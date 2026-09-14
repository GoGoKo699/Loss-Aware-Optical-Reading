# Loss-Aware Optical Reading

**Choose the input for the loss and the required reliability. Keep the photon
receiver fixed. Compare the result with a bound on the classical source class.**

A single photon interrogates four paths. Exactly one path receives a pi phase
flip, selected uniformly and hidden from the reader. A fixed interferometer
returns a path label or an inconclusive outcome. Known unequal losses and the
penalty for wrong answers determine how the input photon should be distributed.

The physical reading mechanism is established. The project develops two precise
candidate contributions: a joint input/measurement optimum reached by input-only
retuning, and an optical performance ceiling covering every allowed classical
coherent-state mixture under a mean signal-photon budget.

**Current stage:** audited and numerically repaired theory, a completed bounded
predecessor comparison, and a proposal for initial technical laboratory review.
Publication-level priority remains unestablished. There are no acquired laboratory
data or confirmed device calibrations. This is a private working repository,
not a public release.

## Start here

| Route | Entry | Purpose |
|---|---|---|
| **Understand** | [Two-claim contribution note](docs/CONTRIBUTIONS.md), then [scientific report](REPORT.md) | See the simple mechanism, exact scope, and proposed result. |
| **Check** | [Claim status](CLAIM_STATUS.md), [source map](SOURCE_AUDIT.md), [proofs](proofs/THEORY.md) | Separate mathematical validity from prior work and candidate novelty. |
| **Laboratory review** | [Why these tests](experiment/REVIEW_RATIONALE.md), then [five review questions](experiment/LAB_REVIEW.md) | Assess the physical interface before designing or running the experiment. |
| **Reproduce or develop** | [Reproduction guide](docs/REPRODUCE.md), [current task boundary](work_orders/CURRENT.md) | Run checks without changing archived evidence and continue from the repository. |

## Two results, with different roles

**A. Optimal input-only retuning.** Under uniform labels, an orthogonal flat phase
code, and known positive diagonal losses independent of the label, retuning the
incident photon and its no-click decision rule reaches the full reliability
tradeoff with a fixed decoder. The optimization covers arbitrary final
measurements within the stated photon architecture, not just this decoder.

For the four-path experiment,

$$
O_j=I-2|j\rangle\langle j|,\qquad D=\frac12J-I,
$$

where J is the four-by-four all-ones matrix. At zero error, balance the surviving
amplitudes. With a finite wrong-answer penalty, the optimal preparation generally
changes. The fixed-input square-root measurement and harmonic-mean endpoint are
credited building blocks, not separate novelty claims.

**B. A bound on all allowed classical illumination.** The competitor may change
its coherent input, randomize intensities, keep the mixture label, use a phase
reference, and perform an arbitrary measurement. Rare bright pulses are permitted
under the mean incident signal-energy constraint. The general calibrated-map
bound is a ceiling, not an attained optimum for every map.

At uniform four-path loss, a known coherent alphabet attains the source-class
bound. Its fixed-alphabet curve is a direct Herzog-2012 specialization; the
additional comparison is against alternative transmitters and intensity mixtures.
See the [source map and explicit reductions](SOURCE_AUDIT.md).

Neither a successful literature search nor numerical agreement proves priority.
The remaining S18/S20 coverage gaps and possible equivalent multiclass bounds
remain visible in the source map. The two statements remain **candidate technical
contributions**, not cleared publication claims.

## What the first experiment would establish

| Test | Meaning |
|---|---|
| M1: preparation retuning | Test the predicted change in input amplitudes while the photon decoder remains fixed. This alone does not certify a quantum source advantage. |
| P1: positive comparison | Seek an unconditional measured photon score above a valid classical-source ceiling using independently justified calibration and energy bounds. |
| P2: reverse comparison | Seek a measured coherent-receiver score above the entire restricted four-path photon bound, not merely above one tested photon preparation. |

The [operational protocol](experiment/FIRST_EXPERIMENT.md) is unchanged. All
no-click and multiple-click records remain attempts. Each interrogation receives
a fresh independent hidden label. Preparation, the unknown operation, and the
receiver must be physically separate roles; the hidden answer cannot be a
compiler input.

The platform is SU(4)/SU(8)-first with one computational photon at a time. A source
herald is not an interacting auxiliary photon. The photon theorem excludes an
occupied bypass rail, retained idler, and repeated interrogation of one setting.
There is no fifth healthy hypothesis. See the [physical setting](docs/PHYSICAL_SETTING.md).
The signal-photon comparison is not a total-energy or wall-clock comparison.

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

Each named output directory must be new. The recorded environment is Python
3.13.5, NumPy 2.3.5, SciPy 1.17.0, with mpmath 1.3.0 for independent tests.
The full guide explains tolerances and the distinction between original source,
repaired source, and frozen evidence. Numerical checks are not new universal
proofs or evidence of novelty.

The [numerical contract](docs/NUMERICAL_CONTRACT.md) separates nominal rates from
outward-safe photon-support bounds. It is not an interval guarantee for all
classical, statistical, calibration, or experimental calculations.

## Evidence and remaining work

`results/hypothetical_*` are forecasts; `results/synthetic_*` are simulated
certification examples; `templates/` are uncalibrated plans and a header-only
trial CSV. None is laboratory data. Fresh runs go under `results/runs/`.

The [theory audit](audits/theory-01/REPORT.md), [repair](repairs/theory-01/REPORT.md),
and [predecessor comparison](audits/novelty-01/REPORT.md) remain intact. Original
archives, import hashes, and reference outputs are preserved. The
[integration record](integrations/novelty-01/REPORT.md) explains the current
wording changes and their checks.

The next decisions are the remaining focused source comparison and initial
laboratory feedback, as set out in the [roadmap](docs/ROADMAP.md). Adaptive
multi-query advantage, exact arbitrary-loss classical finite-error optimality,
and measured advantage are not established. No more elaborate optimizer or
larger chip is required merely to continue this work.

No redistribution license has been selected. Contact: gogoko699@gmail.com.
