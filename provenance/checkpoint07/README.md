# Loss-aware single-photon phase reading

This package supplies an analytic design rule, independent numerical checks, and
a first-experiment proposal for a single photon in four programmable optical
paths. Its main result is that one fixed phase-code decoder reaches the entire
optimal ideal photon reliability tradeoff by retuning the input amplitudes.

The proposed experiment tests both a regime with a certifiable advantage over
all allowed classical probes and a regime where an implemented coherent receiver
can beat the specified single-photon architecture. It is not a demonstration of
a quantum optimizer and contains no laboratory data.

## Start here

| Purpose | File |
|---|---|
| Scientific result and experimental plan in context | [REPORT.md](REPORT.md) |
| Full definitions, proofs, and restrictions | [proofs/THEORY.md](proofs/THEORY.md) |
| First experiment for initial technical lab review | [experiment/FIRST_EXPERIMENT.md](experiment/FIRST_EXPERIMENT.md) |
| Short list of hardware/calibration questions | [experiment/LAB_REVIEW.md](experiment/LAB_REVIEW.md) |
| Exact theorem versus bound versus unperformed experiment | [CLAIM_STATUS.md](CLAIM_STATUS.md) |
| Primary references and uncompleted novelty comparisons | [SOURCE_AUDIT.md](SOURCE_AUDIT.md) |

## Reproduce

Python 3.10 or later is expected; the archived run used Python 3.13.5. The only
third-party requirements are NumPy and SciPy. The code makes no network requests.

```bash
python -m pip install -r requirements.txt
python src/validate.py
```

This regenerates the numerical tables, the validation ledger, both explicitly
synthetic certification examples, and the trial-analyzer accounting checks.
It overwrites generated files under `results/`, not proofs or protocols. The
recorded environment is in `requirements-recorded.txt` and `results/validation.json`.

The expected run has 5,261 checks. Algebraic checks, a high-precision independent
reduction, explicit primal/dual comparisons, random feasible POVMs, detector
probability enumeration, and independent Gaussian integration serve different
purposes. Their count is not a substitute for the analytic proofs. No SDP solver,
interval-arithmetic certificate, or formal proof assistant is used.

The independent constrained solver uses SLSQP with explicit eigenvalue
positivity conditions. It is labelled as a numerical diagnostic, not as a
rigorous semidefinite-program certificate. The uniform classical POVM and the
photon upper/attainment arguments are explicit analytic constructions.

## Analyze a future fixed-budget run

The templates are examples, not calibrated plans. They are marked synthetic and
have no associated experimental trial data. The CSV file contains only a header.
A real plan needs externally justified simultaneous calibration bounds, source
energy/tail conditions, blinding, fixed N, and prior approval.

```bash
python src/analyze_trials.py \
  --plan path/to/approved_primary_plan.json \
  --trials path/to/all_attempted_trials.csv \
  --output path/to/conditional_result.json
```

The same command supports the reverse comparison with an approved plan based on
`templates/reverse_plan.example.json`. The output file's parent must exist.

For synthetic demonstrations only, the command permits `--allow-synthetic`.
This flag never makes the records experimental. The main validation includes a
64-record all-mask accounting test and rejects invalid inputs. It also generates
rounded expected-count examples directly; those are not an acquired data set.

The analyzer rejects missing trials, duplicate IDs, and undeclared configuration
changes. It cannot infer the physical validity of a calibration or prevent a
human from falsely declaring preregistration. Read the assumptions in the output.

## Important distinctions

One photon in four paths is one four-dimensional carrier, not multiple physical
qubits. A source herald can define the input trial; it is not an interacting
computational photon. Every photon interrogates the unknown section only once.

The ideal single-photon benchmark excludes occupied bypass rails and retained
idlers. The classical-probe class includes nonnegative Glauber–Sudarshan mixtures,
receiver-visible preparation labels, arbitrary measurements, phase references,
and rare bright pulses under the signal mean-energy bound.

Output no-click and multiple-click records remain in the trial denominator.
Source-herald normalization, output postselection, and incident photon accounting
must not be conflated. The test is neither device independent nor a wall-clock,
pump-energy, or computation-time comparison.

## Results and provenance

`results/hypothetical_design_forecast.csv` contains model predictions, not measured
hardware values. `results/synthetic_*` contains synthetic acceptance calculations,
not statistical evidence from an experiment. `results/quantum_frontier.csv` and
`results/uniform_exact_comparison.csv` evaluate proved ideal-model expressions.

`baseline/` preserves the original checkpoint-06 archive and its proofs unchanged.
It is optional provenance, not required to understand the current main result.
The archival reports may contain their original relative links; open the included
archive for the complete old package. No earlier optical/chirality branch is
required by this proposal.

All new mathematical claims have declared domains. Exact arbitrary-imbalance
classical finite-error optimality, adaptive repeated-use advantages, actual lab
calibrations, and publication-level novelty are not claimed. This is a working
research checkpoint, not a licensed public release; no redistribution license
has been selected here.
