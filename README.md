# Loss-Aware Optical Reading

**The laboratory has both an SU(4) chip and an SU(8) chip.**

Retune the incident photon for the loss and required reliability. Keep the
receiver fixed where the theorem applies. Measure all outcomes and compare
performance with the appropriate theoretical benchmark.

| What can we try? | Start here | First practical step |
|---|---|---|
| Our SU4 chip | [SU4: four-symbol phase reading](experiment/SU4.md) | Check preparation, four phase patterns and output routing with classical light. |
| Our SU8 chip | [SU8: two explicit routes](experiment/SU8.md) | Embed the same four-label task, or commission the native eight-mode Walsh code. |
| Choose a scientific test | [Experiment index](experiment/INDEX.md) | Separate commissioning, mechanism tests and source-class certification. |

One photon occupies a superposition of paths. Four or eight paths are not four
or eight photons, nor independently carried gate-based qubits. The four-symbol
task asks which one of four paths received a pi phase flip, in one interrogation.
The native eight-mode task uses eight different Walsh phase patterns.

**Ready now:** self-contained procedures, target matrices, synthetic records and
runnable reference calculations. **Before certified acquisition:** the laboratory
must supply its interfaces, calibration and uncertainty budget. Processor
availability is confirmed; it does not specify ports, control sections, sources,
detectors or inter-chip connections. No laboratory data have been acquired here.

## From hardware to a recorded answer

1. **Prepare.** Set a normalized path-amplitude vector before the hidden label is
   selected. Known loss and the preselected penalty for a wrong answer determine
   the target input. Preparation itself is calculated classically.
2. **Interrogate.** An independent hidden section applies its phase pattern and
   loss. P0 is the incident signal-accounting plane; P1 is the accessible output
   of that declared device. Attenuation needs a physical loss section: a unitary
   phase setting does not implement it.
3. **Decode.** Program the fixed code decoder. The reader never receives the
   hidden answer as a compiler input. One combined matrix is useful for optical
   transfer checks; it does not by itself implement an unknown-operation task.
4. **Record.** Save every attempted gate, its full detector mask, no-click,
   multiple-click, leakage and rejected records. Unseal hidden labels only after
   reader records and decisions are fixed. Score correct (C), wrong (E) and
   inconclusive (F) per attempt, with C+E+F=1.
5. **Interpret.** Compare a measured score with the bound appropriate to its
   declared optical map, source budget and uncertainty. A good routing pattern
   alone is not evidence of a source-class advantage.

The [interface guide](experiment/INTERFACES.md) maps the physical roles, including
an optional arrangement using the existing SU4 for preparation and SU8 for
reception. Its coupling and independent hidden section require confirmation.
The [commissioning procedure](experiment/COMMISSIONING.md) explains intensity
checks, phase-referenced transfer measurements and absolute power accounting.
It can be understood without reading either external anchor.

## Which result would mean what?

| Route | Change / hold fixed | Recorded result and meaning |
|---|---|---|
| Classical-light commissioning | Program known preparations and phase patterns; verify the target receiver | Port and transfer checks establish classical-wave implementation. Normalized intensities do not establish loss or a quantum advantage. |
| [M1: input retuning](experiment/M1.md) | Compare uniform, inverse-loss and finite-penalty inputs; keep the decoder fixed | Test predicted unconditional C/E/F. A scan is neither a proof of global optimality nor a source-class certificate. |
| [P1: positive comparison](experiment/P1.md) | Freeze the four-label photon preparation, receiver, calibration and plan | Seek unconditional photon performance above the derived all-classical-source ceiling. |
| [P2: reverse comparison](experiment/P2.md) | Implement a label-blind coherent displacement receiver at severe imbalance | Seek an achieved coherent score above the entire declared four-path single-photon upper bound. |
| SU8 four-active-mode route | Use ports 0–3, vacuum inputs 4–7; measure all eight outputs | Same four-label task. Extra outputs record leakage as inconclusive attempts. |
| SU8 native Walsh route | Program the eight-mode orthogonal phase code and its fixed decoder | Existing photon theorem specialization and teaching/commissioning example. No transferred four-symbol classical frontier or four-mode robustness claim. |

M1/P1/P2 retain the registered meanings, penalties, confidence allocation and
provisional trial budgets in the [first-experiment protocol](experiment/FIRST_EXPERIMENT.md).
Its native eight-mode “later” language records the earlier four-mode acquisition
scope; the new Walsh recipe is now provided separately, with descriptive records.
The native eight-mode data never enter the four-detector certification analyzer.

## What successful experiments could establish

The aim is a paper with one clear physical message: **adapt the incident photon
to the loss and required reliability, then identify when that strategy has a
measurable advantage and where its limits lie.** The existing SU4 and SU8 chips
let us test this with explicit preparations, phase patterns and receivers.

The strongest planned result would combine three pieces of evidence. M1 would
show the predicted preparation changes working with one fixed decoder. P1 would
establish a certified single-photon advantage over the entire declared classical
source class at the same mean incident signal budget. P2 would show the opposite
ordering in a separate severe-imbalance regime: an implemented coherent receiver
outperforming the entire declared four-path single-photon class.

Together, these results could support a theory-and-experiment paper explaining
**when single photons help, when coherent illumination wins, and why loss changes
the best choice.** The complete input-only retuning reduction (contribution A)
would remain the leading candidate contribution; the derived optical benchmark
(B) would supply the credited comparison.
Calibrated robustness measurements could show how closely the laboratory follows
the ideal model and which imperfections matter.

There are useful smaller outcomes too. Commissioning establishes optical
implementation; M1 alone supports a mechanism result. A source-class advantage
claim needs P1's full certificate. P2 makes the boundary scientifically useful
even where the photon strategy loses. Native Walsh8 remains a separate
implementation example until its own source-class comparison is established.

This is an experimental and publication objective, not a report of measured
results. The eventual venue and significance should be judged from the data,
calibration, complete comparisons and a current novelty assessment.

## Run the reference calculations

From the repository root, install the recorded dependencies and use a new output
directory for each command. [Reproduction instructions](docs/REPRODUCE.md) also
cover the full historical and repaired checks.

```bash
python -m pip install -r requirements-test.txt
python scripts/verify_import.py
python scripts/lab_reference.py --help
python -m unittest discover -s tests -v
```

The chip and test pages give exact generation/analysis commands and explain their
synthetic outputs. No script is a vendor driver or a working instrument adapter.
Generated examples are calculations, not calibrated device specifications.

## Why this small experiment?

The [inspiration and working philosophy](docs/PHILOSOPHY_DRAFT.md) explains
the preference for a small task with a clear mechanism,
a simple receiver and an operational resource comparison. Negative regions,
including regimes where a classical strategy wins, are part of the account.

The factual contribution hierarchy is separate: **A, complete joint input-only
retuning, remains the leading candidate contribution. B is a derived optical
benchmark, not a second independently new general discrimination theorem.**
The fixed-input square-root measurement and zero-error endpoint are credited
ingredients. Named predecessor comparisons are resolved at their documented
access levels; worldwide priority and publication significance remain open.
See [contributions](docs/CONTRIBUTIONS.md), [claim status](CLAIM_STATUS.md) and
[source attribution](SOURCE_AUDIT.md).

## Understand or inspect the support

| Need | Route |
|---|---|
| Learn the experiment's theory | [Self-contained theory route](docs/THEORY_ROUTE.md): states, measurements, C/E/F, then optimization and benchmarks |
| Connect to familiar material | [Optional reading crosswalk](docs/READING_CROSSWALK.md): Capmany–Pérez engineering chapters and Barnett–Croke discrimination review |
| Decide how an error changes interpretation | [Robustness guide](docs/ROBUSTNESS_GUIDE.md) and [practical uncertainty worksheet](experiment/UNCERTAINTY.md) |
| Inspect complete arguments | [Canonical proofs](proofs/THEORY.md), [numerical contract](docs/NUMERICAL_CONTRACT.md), [robustness proofs](docs/ROBUSTNESS_PROOFS.md) |
| Reproduce or trace evidence | [Reproduction](docs/REPRODUCE.md), [handover integration](integrations/lab-handover-01/REPORT.md), [current scope](work_orders/CURRENT.md) |

The classical comparator includes arbitrary permitted receivers, coherent
mixtures with receiver-known preparation labels, phase references and rare bright
pulses under a mean signal budget at P0. Our receiver and detector losses reduce
our achieved performance; they do not automatically lower that ceiling at P1.
Signal photons are counted separately from pump, herald and reference energy,
total apparatus energy and wall-clock cost.

Fresh independent hidden labels, reader blinding, separate pilot/test records
and fixed-N acquisition remain required. There is no optional-stopping claim,
occupied bypass, retained idler, interacting ancillary photon, memory or repeated
interrogation of one setting in the main class. Further extensions are listed
in the [roadmap](docs/ROADMAP.md), with their present limits.

Original project material is available under the [MIT License](LICENSE).
Third-party material retains its own terms; see [third-party notices](THIRD_PARTY_NOTICES.md).

## Experimental status and collaboration

**Experimental validation is still pending.** The theoretical analysis,
reference code, and experimental procedures are available in this repository;
laboratory results have not yet been collected.

Experimental and theoretical collaborators are welcome. To discuss implementing
the protocols, device characterization, or further analysis, please contact
[gogoko699@gmail.com](mailto:gogoko699@gmail.com).
