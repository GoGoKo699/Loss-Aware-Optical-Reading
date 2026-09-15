# Small runnable laboratory examples

All files here are **synthetic teaching references, not laboratory data or
calibration**. Start with the [SU4 route](../../experiment/SU4.md) or
[SU8 route](../../experiment/SU8.md). Both chips are available; this code supplies
target matrices and an explicit record interface, with no instrument drivers.

Run from the repository root in the environment in
[REPRODUCE.md](../../docs/REPRODUCE.md). Every destination must be new:

```bash
python scripts/lab_reference.py --recipe commission-su4 --output results/runs/lab-commission-su4
python scripts/lab_reference.py --recipe commission-su8-embed --output results/runs/lab-commission-su8-embed
python scripts/lab_reference.py --recipe commission-su8-walsh --output results/runs/lab-commission-su8-walsh
python scripts/lab_reference.py --recipe m1 --output results/runs/lab-m1
python scripts/lab_reference.py --recipe p1 --output results/runs/lab-p1
python scripts/lab_reference.py --recipe p2 --output results/runs/lab-p2
```

Use `--chip su8-embed` for M1/P1/P2 on the four active modes of SU8. These retain
four hidden labels. The P2 receiver is direct-path coherent displacement plus
click detection. It does not use the D4 decoder. Native Walsh8 is its own route.

| Output | Contents and meaning |
|---|---|
| `target_matrices.json` | Logical ports, input amplitudes, a preparation matrix, physical phases, loss contraction, decoder, common SU phase choice, transfer targets. Complex matrices have separate `real` and `imag` arrays. |
| `forecast.json` | Explicit model assumptions, nominal rates, established benchmark values, and full conditional mask law. M1 includes all four preparations. |
| `commissioning_transfer_reference.csv` | Commissioning recipes only: complex transfer and intensity targets for every input/output port and known phase setting. These are calculated targets, not measurements. |
| `synthetic_trials.csv` | 256 attempts by default, with independently generated labels and every sampled outcome retained. These are descriptive draws, not a registered acquisition. |
| `synthetic_summary.json` | Unconditional C/E/F, separate condition/preparation summaries, confusion matrix, full-width mask histogram, and failure diagnostics. |
| `RECORD_SCHEMA.json` | Raw fields, bit/port convention, trial definition, and allowed flags. |
| `MANIFEST.json` | Hashes of this particular generated teaching output. |

Commissioning uses classical-wave transfer measurements. Its synthetic click
CSV is a separate **ideal one-photon categorical illustration**, not a model
for arbitrary laser pulse brightness. Normalized intensities do not establish
P0 energy, detector efficiency, vacuum probability, or a source-class advantage.
Intensity-only checks do not determine the relative complex phases needed for
general transfer calibration; use phase-referenced measurements for those.

Analyze the example without a statistical claim:

```bash
python scripts/lab_records.py --route su4 --trials examples/lab/p1/synthetic_trials.csv --output results/runs/lab-descriptive-p1
python scripts/lab_records.py --route su8-embed --trials examples/lab/commission-su8-embed/synthetic_trials.csv --output results/runs/lab-descriptive-embed
python scripts/lab_records.py --route su8-walsh --trials examples/lab/commission-su8-walsh/synthetic_trials.csv --output results/runs/lab-descriptive-walsh
```

Port 0 is the least significant mask bit. Four detector channels have 16 masks;
eight have 256. On the embedded route every click in logical ports 4–7 is an
inconclusive attempt, including simultaneous active/spare clicks. No-click,
multiple-click, and predeclared integrity-rejected attempts remain in N. The
adapter writes its fail-only mapping separately and preserves original mask
histograms and per-row changes. It never discards the input CSV.

For four-label certification, `lab_records.py` accepts `--plan` and delegates
to the established analyzer. The plan must match the complete fixed-N input,
calibration IDs, receiver, code, and registered test. The examples here are too
short for the unchanged provisional P1/P2 budgets of 500,000/50,000 attempts;
using their plans with these short records correctly fails. The small sample
size is a teaching choice, not a revision of those budgets or confidence
allocations. Native-eight records explicitly refuse four-label plans.

The committed compact examples contain 64 attempts each; the CLI default is
256. The generator uses seed 20260915. `--sample-attempts` and `--seed` change
only synthetic teaching draws. A hardware adapter must obtain the actual port
map, compiler convention, phase/loss interfaces, timestamps, energy accounting,
and calibration from the laboratory. Sealed detector records must be joined
to separately held hidden labels only for offline scoring. Passing software
checks cannot establish these physical conditions.

The [canonical protocol](../../experiment/FIRST_EXPERIMENT.md),
[theory](../../proofs/THEORY.md), and
[numerical contract](../../docs/NUMERICAL_CONTRACT.md) control scientific meaning.
The photon support upper endpoint is outward-safe for its numerical inputs;
nominal matrices, classical exponentials, and the full planning calculation are
not a single interval-certified pipeline.
