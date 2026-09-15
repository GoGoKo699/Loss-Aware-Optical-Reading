# Loss-Aware Optical Reading

**Retune the incident photon for the loss and required reliability. Keep the
receiver fixed. Test the result against a credited classical-source benchmark.**

A single photon interrogates four paths. Exactly one path receives a pi phase
flip, selected uniformly and hidden from the reader. The receiver returns a
path label or an inconclusive outcome. Known unequal losses and the penalty
for wrong answers determine the optimal input amplitudes.

The phase-reading mechanism is established. **A, joint input-only retuning, is
the leading candidate theoretical contribution. B is a derived optical benchmark,
not a second independently new general discrimination theorem.** The completed
full-text follow-up supplies the specific predecessor reductions for B.

Current stage: audited and numerically repaired theory, completed bounded
predecessor comparisons, and an initial technical laboratory-review proposal.
Priority for A and publication significance remain unestablished. There are no
acquired laboratory data or confirmed device calibrations. This is a private
working repository, not a public release.

## Start here

| Route | Entry | Purpose |
|---|---|---|
| Understand | [Contribution and benchmark](docs/CONTRIBUTIONS.md), then [scientific report](REPORT.md) | Read the task, mechanism, and scope. |
| Check | [Claim status](CLAIM_STATUS.md), [source map](SOURCE_AUDIT.md), [proofs](proofs/THEORY.md) | Separate validity, attribution, and candidate novelty. |
| Laboratory review | [Why these tests](experiment/REVIEW_RATIONALE.md), then [five questions](experiment/LAB_REVIEW.md) | Assess feasibility before acquisition. |
| Reproduce or develop | [Reproduction guide](docs/REPRODUCE.md), [current task boundary](work_orders/CURRENT.md) | Work from preserved evidence, not earlier chats. |

## A. Optimal input-only retuning

For uniform labels, a square flat orthogonal phase code, and known positive
diagonal losses independent of the label, the joint optimum over the incident
photon and arbitrary final measurements is attained by retuning the input and
the no-click decision rule while keeping the code decoder fixed.

For the four-path experiment,

$$
O_j=I-2|j\rangle\langle j|,\qquad D=\frac12J-I,
$$

where J is the four-by-four all-ones matrix. At zero error the preparation
balances the surviving amplitudes. At finite error it generally changes with
the wrong-answer penalty. The fixed-input square-root measurement and
harmonic-mean endpoint are credited ingredients; the candidate result is the
complete joint optimization with erasure accounting, not a new receiver.

## B. A derived benchmark for classical illumination

The competitor may choose a different coherent input, randomize pulse energies,
keep the preparation label, use a phase reference, and perform any measurement.
Arbitrarily rare bright pulses remain allowed under the mean incident signal
budget. The general calibrated-map bound is a ceiling, not an attained optimum
for every map.

Its discrimination ingredient follows from Zhang et al.'s zero-error bound and
Bagan et al.'s duality relation with the conclusive-filter completion. Coherent
optical overlaps and concavity extend it to the classical source class. At
uniform four-path loss, a known alphabet attains the source-class frontier; its
fixed-alphabet curve is Herzog's Eq. (4.18) in different variables. See the
[full-text follow-up](audits/novelty-02/REPORT.md) and [source map](SOURCE_AUDIT.md).

This attribution correction does not weaken the comparator or alter a formula.
A valid, credited benchmark can support an experimental advance without being
a new fundamental inequality. The named S18/S20 comparisons are resolved at the
recorded access levels; this is not worldwide priority clearance for A.

## What the first experiment would establish

| Test | Meaning |
|---|---|
| M1: input retuning | Test the predicted preparations with an unchanged decoder; a finite scan alone does not prove global optimality or certify a quantum advantage. |
| P1: positive comparison | Seek unconditional performance above the all-classical-source ceiling using justified calibration and energy bounds. |
| P2: reverse comparison | Seek an implemented coherent score above the upper bound for the entire restricted four-path photon class, not merely one tested input. |

The [operational protocol](experiment/FIRST_EXPERIMENT.md) is unchanged. Count
no-click and multiple-click attempts. Each interrogation gets a fresh independent
hidden label. Preparation, unknown operation, and receiver are separate physical
roles; the answer must not enter the reader's compiler.

The platform is SU(4)/SU(8)-first with one computational photon at a time. A
source herald is not an interacting auxiliary photon. The theorem excludes an
occupied bypass rail, retained idler, repeated use of one setting, and a fifth
healthy hypothesis. See the [physical setting](docs/PHYSICAL_SETTING.md). Signal
illumination is not total apparatus energy, source cost, or wall-clock time.

## Reproduce without replacing evidence

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-test.txt
python scripts/verify_import.py
python -m unittest discover -s tests -v
python scripts/reproduce.py
python repairs/theory-01/verify.py --output results/runs/repair-01
python audits/novelty-01/comparison_checks.py --source-root . --output results/runs/novelty-01
python audits/novelty-02/comparison_checks.py --output results/runs/novelty-02
```

Every output directory must be new. The recorded numerical environment is
Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, with mpmath 1.3.0 for independent tests.
The [numerical contract](docs/NUMERICAL_CONTRACT.md) separates nominal rates from
outward-safe photon-support bounds; it does not interval-certify the whole pipeline.

The committed follow-up has 572 checks. A separate supplied 717-assertion packet
is preserved, without replacing that audit, in the
[integration record](integrations/novelty-02/REPORT.md). Their counts and results
remain distinct; neither is evidence of originality.

## Evidence and remaining work

Hypothetical forecasts, synthetic certification examples, and uncalibrated
[templates](templates/) are not laboratory data. Fresh runs go in `results/runs/`.
The [theory audit](audits/theory-01/REPORT.md), [repair](repairs/theory-01/REPORT.md),
[first comparison](audits/novelty-01/REPORT.md), and
[full-text follow-up](audits/novelty-02/REPORT.md) retain their original evidence.

Next: assess the significance and physical robustness of A, and obtain initial
laboratory feedback. The [roadmap](docs/ROADMAP.md) separates those questions from
new research requiring authorization. Exact arbitrary-loss classical finite-error
optimality, adaptive multi-query advantage, and measured advantage are not established.
More modes or a learning label do not address these gaps.

No redistribution license has been selected. Contact: gogoko699@gmail.com.
