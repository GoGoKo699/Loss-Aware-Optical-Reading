# Loss-Aware Optical Reading

A single photon interrogates four optical paths. Exactly one path receives a
phase flip. A fixed interferometer converts the returned phase pattern into a
path label. Loss and the permitted rate of wrong answers determine how the input
photon should be distributed.

This repository develops the theory, classical-probe benchmarks, and first
experimental proposal for that task. It asks **when single-photon illumination
is useful, when classical illumination is preferable, and how to certify the
comparison without discarding unsuccessful trials**.

**Current stage:** theory and numerical validation, with an initial laboratory-review
proposal. There are no acquired laboratory data. The theorem-level novelty audit
and actual hardware/calibration assessment remain open. This is a private
working research repository, not a public release.

## Start here

| Route | Read or run | Purpose |
|---|---|---|
| **LEARN** | [Scientific report](REPORT.md), then [physical setting](docs/PHYSICAL_SETTING.md) | Understand the task, fixed receiver, and proposed experiment. |
| **CHECK** | [Claim status](CLAIM_STATUS.md), [theory and proofs](proofs/THEORY.md), [source audit](SOURCE_AUDIT.md) | Separate exact model results, numerical diagnostics, assumptions, and unverified novelty. |
| **REPRODUCE** | [Reproduction guide](docs/REPRODUCE.md) and the commands below | Verify the import and regenerate the reference calculations into a new directory. |
| **LAB REVIEW** | [Short brief](experiment/LAB_REVIEW.md), then [first-experiment protocol](experiment/FIRST_EXPERIMENT.md) | Identify the source, device, receiver, and calibration questions before an experiment. |
| **DEVELOP** | [Current work order](work_orders/CURRENT.md) and [contribution rules](CONTRIBUTING.md) | Continue from a bounded task without needing earlier chats. |

## The result and its boundary

The reference code uses the four promised operations

$$
O_j=I-2|j\rangle\langle j|,\qquad j=0,1,2,3,
$$

with uniform hidden labels. The fixed receiver is

$$
D=\frac12J-I,
$$

where every entry of the four-by-four matrix $J$ is one.

Under known, hypothesis-independent diagonal loss, retuning the input amplitudes
makes this same decoder attain the ideal single-photon reliability frontier.
At zero error the preparation balances the surviving amplitudes. At finite error,
the optimal preparation depends on the penalty for a wrong answer. The proof
also specifies how no-click decisions enter the frontier.

The classical comparison optimizes the **probe class**, not merely the laser
receiver available in one lab. It includes nonnegative coherent-state mixtures,
phase references, arbitrary receivers, and rare bright pulses under a mean
incident signal-energy constraint. The uniform-loss four-symbol classical
frontier is exact. The general calibrated-map certificate is a bound and is not
claimed to be tight everywhere. See the [full statement](proofs/THEORY.md).

One photon in four paths is one four-dimensional carrier, not four separately
carried qubits. The photon theorem excludes occupied bypass rails, retained
idlers, and repeated interrogation of one hidden setting. The task has no fifth
healthy hypothesis. These restrictions belong to the problem definition.

## Reproduce without replacing the evidence

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-test.txt
python scripts/verify_import.py
python -m unittest discover -s tests -v
python scripts/reproduce.py
python repairs/theory-01/verify.py --output results/runs/repair-01
```

The recorded validation environment is Python 3.13.5, NumPy 2.3.5, and SciPy
1.17.0; test-only high-precision comparisons use mpmath 1.3.0. The new run goes under `results/runs/<unique-id>/`; its directory is never
reused. Reference results remain unchanged. Full instructions and comparison
tolerances are in [docs/REPRODUCE.md](docs/REPRODUCE.md).

The inherited validation has 5,261 ordered checks. This count is a regression
inventory, not evidence that every universal proof or novelty claim has been
independently reviewed. Runtime, platform metadata, and small constrained-solver
residuals may differ between runs. The reproduction report records those changes.

## What the first experiment would test

The protocol separates a moderate-imbalance positive comparison, a severe-imbalance
reverse comparison, and an input-retuning mechanism test. The unknown-operation
controller must remain independent of the reader. Each counted interrogation
receives a fresh hidden label. No-click and multiple-click records stay in the
trial denominator.

The physical setting is SU(4)/SU(8)-first, with one computational photon at a time.
A source herald is not an interacting auxiliary photon. Larger existing mode
processors may be considered, but multiphoton computing and quantum memory are
not implicit resources. A programmable mode matrix alone does not establish the
separate preparation, unknown-operation, receiver, and calibration interface.

## Results are not laboratory data

| Material | Meaning |
|---|---|
| `results/quantum_frontier.csv`, `results/uniform_exact_comparison.csv` | Evaluations of ideal-model expressions |
| `results/independent_dual_checks.csv`, `results/validation.json` | Numerical diagnostics and their tolerances |
| `results/hypothetical_*` | Forecasts under hypothetical source and detector inputs |
| `results/synthetic_*` | Synthetic certification examples, not observed violations |
| `templates/` | Uncalibrated examples and a header-only trial CSV |
| `results/runs/` | New local runs, ignored by Git unless deliberately archived elsewhere |

The [migration record](provenance/MIGRATION.md) identifies the exact original
archive, the import changes, and a fresh reproduction. Older checkpoint 06 is
optional evidence in [baseline/](baseline/). No earlier learning or chirality
exploration is needed to follow this project.

## Audit and numerical repair

The [independent audit](audits/theory-01/REPORT.md) supports the central results
under their stated assumptions. Its three limited findings are addressed by the
[bounded repair](repairs/theory-01/REPORT.md), with the original evidence retained.
The photon-support code now supplies an exact-rational outward enclosure and
rejects unsupported numerical inputs. See the [numeric domain and output contract](docs/NUMERICAL_CONTRACT.md)
before treating a returned value as an upper-bound certificate.

## Next scientific decisions

Compare each candidate theorem with its direct predecessors and obtain laboratory
feedback on the physical interface. The bounded mathematical audit is complete;
publication novelty and actual calibration remain separate open requirements.
Do not add an optimizer or more modes merely to enlarge the project.

The broader ambition is a predictive, calibration-aware reliability–illumination
comparison. Exact arbitrary-imbalance classical finite-error optimality, adaptive
multi-query advantage, and actual measured advantage remain outside the currently
established scope. See the [roadmap](docs/ROADMAP.md).

No redistribution license has been selected. Contact: gogoko699@gmail.com.
