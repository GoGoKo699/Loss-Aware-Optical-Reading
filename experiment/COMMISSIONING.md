# Start with classical-light commissioning

**Question:** do our available SU(4) or SU(8) chips implement the stated input,
phase patterns, decoder, and port convention? Compatible classical illumination
lets the lab check this before single-photon acquisition. The scientific target
remains input-only retuning and unconditional single-photon reading; this setup
check is **classical-wave implementation verification**, not a quantum-advantage
experiment.

## Pick the exact target

| Route | Prepared classical amplitudes at P0 | Phase family and receiver | Ideal equal-loss output |
|---|---|---|---|
| SU4 | `A(1,1,1,1)/2` on 0–3 | `O_j=I4-2|j><j|`, `D4=J4/2-I4` | `A sqrt(t) |j>`, `j=0..3` |
| SU8 four active | `A(1,1,1,1,0,0,0,0)/2` | `O_j ⊕ I4`, `D4 ⊕ I4` | Same four labels, spare outputs ideally dark |
| SU8 native | `A(1,1,1,1,1,1,1,1)/sqrt(8)` | `O_j=diag(Z8[:,j])`, `D8=Z8†/sqrt(8)` | `A sqrt(t) |j>`, `j=0..7` |

`|A|^2` sets the incident classical amplitude normalization in the selected
mode convention. For unequal transmissions the target is `D T O_j a`, scaled
by `A`, with `T=diag(sqrt(eta))`. An attenuation block is required to realize
`T`; it cannot be supplied by a unitary compiler. The full signed matrices,
first-column preparation completion, logical ports, and consistent SU phases
are on [SU4](SU4.md) and [SU8](SU8.md), and are exported by the reference below.

Required confirmed processors: the selected SU(4) or SU(8) chip. Supporting
capabilities not yet supplied: compatible illumination, port/phase convention,
control access, transfer/intensity readout, and a phase reference if complex
transfer is to be measured. Independent preparation and hidden phase/loss roles
are additionally needed for a separated-block check. They are not prerequisites
for a known end-to-end unitary transfer check.

## Reference calculation before touching controls

From the repository root, after [environment setup](../docs/REPRODUCE.md):

```bash
python scripts/lab_reference.py --recipe commission-su4 --output results/runs/commission-su4
python scripts/lab_reference.py --recipe commission-su8-embed --output results/runs/commission-su8-embed
python scripts/lab_reference.py --recipe commission-su8-walsh --output results/runs/commission-su8-walsh
```

Choose the relevant command or run all three. Every output directory must be
new. Inspect `target_matrices.json` for input vectors, preparation matrices,
hidden operations, loss and decoder matrices, port order, and compiler phase
convention. `forecast.json` gives the corresponding transfer predictions.
`commissioning_transfer_reference.csv` lists input/output complex amplitudes
and squared magnitudes for the target transfer matrices, explicitly marked as
reference calculations. Compare actual measured columns with this file using
the same port and normalization convention.
`synthetic_trials.csv`, `synthetic_summary.json`, and `RECORD_SCHEMA.json`
demonstrate photon-style all-attempt records for teaching; they are not classical
power measurements and are not laboratory data.

The [committed example set](../examples/lab/README.md) can also be inspected
without running a command. Its 64-attempt samples remain explicitly synthetic;
the CLI defaults to 256 teaching attempts.

For example, the native-eight teaching records can be recounted with the
separate eight-label analyzer:

```bash
python scripts/lab_records.py --route su8-walsh --trials results/runs/commission-su8-walsh/synthetic_trials.csv --output results/runs/commission-su8-walsh-analysis
```

The scientific click-record example and the optical power record below serve
different purposes. Neither establishes absolute illumination by normalizing
its columns to sum to one.

## Practical setup check

1. **Identify ports.** Illuminate one logical input at a time with a known
   test amplitude. Record every accessible output, the connector mapping,
   monitoring scale and background. Confirm that rows mean output and columns
   mean input before asking the compiler for a general matrix.
2. **Check preparation.** Illuminate input port 0 and program the exported
   `Uprep`. Compare output power fractions with `p_i`; use phase-referenced
   measurements to verify the relative phases needed by the code. Other
   populated test inputs are useful transfer probes, not computational ancillas.
3. **Check receiver transfer.** Program the fixed decoder and measure its
   column responses. The ideal `D4` has squared entry magnitude `1/4`; `D8`
   has `1/8`; the embedded decoder is block diagonal. Verify spare-port isolation
   for the embedding. Intensity columns alone do not verify the signs.
4. **Check phase-pattern routing.** With equal prepared amplitudes, apply each
   known phase code and inspect all outputs. The bright output should follow
   the logical label table. Repeat with an explicitly chosen unequal-loss
   example and compare the unnormalized transfer with `D T O_j a`.
5. **Choose what was actually verified.** If the lab compiled one known
   end-to-end matrix `D O_j Uprep`, label the result as that transfer check.
   If separately controlled blocks implemented preparation, hidden operation
   and receiver, record each block's settings and its physical location. The
   former does not demonstrate the latter's independent interrogation interface.
6. **Retain calibration records.** Keep raw powers, references, backgrounds,
   complex-map data where taken, uncertainties, settings, timestamps and failed
   measurements. Identify repeated power scans as commissioning; they are not
   independent single-use scientific trials at one hidden setting.

In these checks the decoder's mathematical target stays fixed across phase
patterns. The known code label changes for routing measurements; preparation
changes only for a declared input check. Calibration may adjust actuator settings
to realize the same target, with the calibration ID and measured residuals
recorded. A calibration change is not a theorem about optimality, and it does
not authorize tuning a receiver using future held-out scientific outcomes.

## What to record

For each optical measurement retain a unique measurement ID, route, logical and
physical input/output ports, programmed target and settings IDs, phase pattern,
preparation/receiver/calibration IDs, wavelength and polarization, timestamp,
integration time, incident/reference reading, all raw output readings,
background reading, units, saturation/failure flags and uncertainty method.
Failed or rejected measurements remain in the commissioning ledger with their
reason. Phase-referenced scans also retain reference phase and its shared
convention across hidden settings.

Later single-photon records use a clock or a pre-exposure herald to define every
attempt and keep no-click, multiple-click, leakage and rejected attempts.
SU4 requires all 16 masks; either SU8 route retains all 256. Native8 has eight
labels; the embedded task still has four. [SU8](SU8.md) explains the distinct
scoring and prevents an eight-detector file from being silently treated as
four-detector data.

## Interpretation and next step

Intensity measurements can identify port routing, relative transmitted power,
gross crosstalk, dark offsets and loss variation. For a basis-input transfer
scan they estimate squared matrix-entry magnitudes. They do not identify the
complex signs/phases, a shared phase between different hidden operations, or a
simultaneous operator-norm uncertainty bound. A phase reference and an explicit
calibration analysis are needed for those claims.

At uniform transmission `t`, all ideal output power for codeword `j` goes to
port `j`, with total output-to-input power ratio `t` before receiver/readout
losses. If output powers are normalized to their own sum, the same picture
appears at very different absolute losses. Thus a normalized bright-port
pattern neither establishes the P0 signal budget nor accounts for no-click
events. A photon experiment with ideal uniform loss would instead report
`C=t, E=0, F=1-t` per attempt.

Wrong port permutations, a transposed compiler convention, missing relative
phase signs, label-dependent global phases, unmonitored leakage, and attenuation
silently attributed to the wrong physical plane are common interpretation
failures. Resolve them in [interfaces](INTERFACES.md) and the
[uncertainty worksheet](UNCERTAINTY.md). Then choose [M1](M1.md) to test the
single-photon mechanism. [P1](P1.md) and [P2](P2.md) additionally require the
unchanged [certified-acquisition protocol](FIRST_EXPERIMENT.md).

The [theory route](../docs/THEORY_ROUTE.md) explains the local code construction;
[Theorems 1–2](../proofs/THEORY.md) justify the photon preparation and rates.
The [robustness guide](../docs/ROBUSTNESS_GUIDE.md) explains why a calibration
error, lost information, and a suboptimal fixed receiver are distinct effects.
