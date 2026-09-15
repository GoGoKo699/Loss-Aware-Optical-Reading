# Choose an experiment

**The laboratory has both an SU(4) chip and an SU(8) chip.** Start with a
classical-light setup check on either. The scientific target is one photon in
a superposition of paths: retune its incident amplitudes for known loss and the
required reliability, keep the code decoder fixed where the theorem applies,
and count every attempted interrogation.

| Start here | Chip and labels | What is established or tested | Status |
|---|---|---|---|
| [SU4 worked example](SU4.md) | SU(4), four labels | Exact four-symbol matrices and output decisions | Existing photon theorem; ready for reference calculations |
| [SU8 route A](SU8.md#route-a-four-active-modes) | SU(8), four labels, four spare inputs in vacuum | Same task embedded in ports 0–3 | Existing four-mode result with explicit leakage accounting |
| [SU8 route B](SU8.md#route-b-native-eight-mode-walsh-code) | SU(8), eight labels | Native flat orthogonal Walsh phase code | Verified specialization of the photon theorem; separate eight-mode records |
| [Classical-light commissioning](COMMISSIONING.md) | Either chip; all three routes above | Preparation, transfer, phase-pattern routing, port identification | Classical-wave implementation verification |
| [M1: input-only retuning](M1.md) | SU4 or four active SU8 modes | Change the input while retaining the decoder | Single-photon mechanism test; no standalone source-class certificate |
| [P1: positive comparison](P1.md) | SU4 or four active SU8 modes | Photon score above the derived all-classical-source ceiling | Requires calibrated bounds and a fixed-N held-out acquisition |
| [P2: reverse comparison](P2.md) | Either chip in the four-label task | Implemented coherent receiver above the whole declared photon bound | Requires coherent displacement and its own held-out acquisition |

Eight single-path flips, an eight-label classical optimum copied from the
four-label formula, and extension of the four-mode robustness certificates to
eight modes are **not established**. Extra occupied rails, retained idlers,
interacting photons, memory, or repeated calls to one hidden setting are outside
the main task. A distinct routed output for each ideal codeword demonstrates a
mechanism; it does not by itself demonstrate a source-class advantage.

## The first useful action

From the repository root, run one of the commissioning reference calculations
below with a new output directory. The generated settings, predictions, and
synthetic records can be inspected before adapting a hardware interface.

```bash
python scripts/lab_reference.py --recipe commission-su4 --output results/runs/first-su4
python scripts/lab_reference.py --recipe commission-su8-embed --output results/runs/first-su8-four
python scripts/lab_reference.py --recipe commission-su8-walsh --output results/runs/first-su8-eight
```

See [the environment and reproduction instructions](../docs/REPRODUCE.md).
These commands do not connect to instruments and refuse an existing output
directory. The small synthetic trial samples are teaching records, not
experimental data or a replacement for the registered trial budgets.
The [committed examples](../examples/lab/README.md) provide inspectable matrices,
forecasts and 64-attempt synthetic records without requiring a run.

**Can begin commissioning** means the lab can identify ports, compile the stated
unitaries using its own documented conventions, and measure optical transfer
with available compatible illumination/readout. **Ready for certified acquisition**
additionally requires the independent hidden section, source and map confidence
bounds, complete attempt records, blinding, and the frozen statistical plan in
[FIRST_EXPERIMENT.md](FIRST_EXPERIMENT.md). Both chips are available; those
supporting interfaces and calibration values have not been supplied.

## Where the next questions go

| Question | Local route |
|---|---|
| Which block performs preparation, loss, phase encoding, or decoding? | [Interfaces and proposed arrangements](INTERFACES.md) |
| Which lab-specific values must be supplied? | [Uncertainty and readiness worksheet](UNCERTAINTY.md) |
| Why do these input settings work? | [Theory route](../docs/THEORY_ROUTE.md), then [canonical proofs](../proofs/THEORY.md) |
| What happens when the ideal assumptions are imperfect? | [Robustness guide](../docs/ROBUSTNESS_GUIDE.md) and the [study worksheet](../studies/robustness-01/CALIBRATION_WORKSHEET.md) |
| Which acquisition and statistics rules control M1/P1/P2? | [Preserved first-experiment protocol](FIRST_EXPERIMENT.md) |
| What is candidate novelty, and what is credited prior work? | [Contributions](../docs/CONTRIBUTIONS.md), [claim ledger](../CLAIM_STATUS.md), [source map](../SOURCE_AUDIT.md) |

The new pages make the existing protocol easier to use. They do not change its
M1/P1/P2 meanings, penalty, confidence allocation, provisional caps, or
acquisition rules. A hypothetical number is a worked input, never an apparatus
specification.
