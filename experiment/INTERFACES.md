# Physical arrangements and hardware adapter boundaries

**The SU(4) and SU(8) processors are both available.** Their names specify
mode-space targets; they do not confirm connector order, three independent
programmable sections, compatible sources/detectors, independently controlled
loss, or how the chips can be interconnected. The following arrangements can
be reviewed and their reference calculations run without inventing those details.

## Keep four roles separate

| Role or plane | Meaning | Who may know the current hidden label? |
|---|---|---|
| Preparation | Set the photon amplitudes or declared coherent illumination using pretest information | No current label |
| **P0: incident signal-accounting plane** | Immediately before the declared hidden device; charge every signal pulse crossing it | No answer-dependent selection of illumination |
| Hidden section | Apply the actual label-selected phase operation and declared device loss | An isolated controller knows the label |
| **P1: accessible device-output plane** | End of the declared hidden device, before the reader's receiver | The reader receives only the permitted optical output |
| Receiver | Apply `D4`, `D4 ⊕ I4`, `D8`, or the separately declared P2 displacement | No current label |
| Readout | Record every attempted gate, then apply the frozen decision rule | Labels unsealed only after records are sealed |

`P1` here denotes a physical plane; [P1.md](P1.md) denotes the positive test.
Device maps run from P0 to P1. Preparation losses determine the actual signal
arriving at P0. Our receiver, detector and coupling losses after P1 lower our
achieved score; they do not automatically lower an unrestricted competitor's
ceiling. Hidden-path attenuation is a contraction implemented by loss to
inaccessible modes, not by programming a unitary phase matrix.

## A possible use of both existing chips

The following is a **proposed physical arrangement** for the four-label task.
It uses confirmed processors with supporting connections still to be established.

| Order along the light path | Block | Status and exact role |
|---|---|---|
| 1 | Compatible source entering logical SU4 port 0 | Source statistics, wavelength/polarization and coupling not supplied |
| 2 | **Available SU(4) chip** | Program a preparation unitary whose first column is `(sqrt(p_0),...,sqrt(p_3))` |
| 3 | **P0** | Meter/bound signal energy here after preparation and its coupling losses |
| 4 | Independent four-path hidden phase/loss section | Proposed; implements `T O_j`, common phase convention, fresh isolated label controller |
| 5 | **P1** | Define the accessible output and the start of the unrestricted receiver comparison |
| 6 | **Available SU(8) chip** | Couple the four signal outputs into logical ports 0–3, vacuum at 4–7; program `D4 ⊕ I4` |
| 7 | Output detection | Record all eight outputs or establish a complete bounded leakage treatment; arrangement not supplied |

The inter-chip connections, mode match, loss placement, independent hidden
section and timing require confirmation. This table does not assert that the
two chips have already been coupled or that the hidden block is built into
either chip. For [P2](P2.md), replace the fixed-decoder receiver role with the
label-independent coherent displacement-and-click receiver; `D4` is not its
nulling operation.

## Alternatives to review

| Arrangement | What the available chip performs | Supporting capability to identify |
|---|---|---|
| SU4 receiver | `D4` after a four-path hidden section | Independent preparation network and hidden phase/loss section |
| SU8 receiver, route A | `D4 ⊕ I4` on four active modes | Independent four-path preparation/hidden section and monitoring of spare outputs |
| SU8 receiver, route B | `D8` for eight Walsh labels | Independent eight-mode preparation and hidden phase/loss section |
| An available chip prepares | `Uprep` from one populated input | An independent hidden section and an appropriate separate receiver |
| Separately accessible sections within a chip | Preparation or receiver blocks in separately controlled portions | Actual topology and control access demonstrating those sections; a universal overall compiler alone is insufficient |
| One compiled matrix for commissioning | Known-label optical transfer check | Compatible test light and transfer measurement only; no reading claim |

The chips do not have to be cascaded. The project does not assume that either
contains three independent full processors. A test that compiles a different
end-to-end matrix using the hidden answer can check a programmed transfer
matrix; it cannot demonstrate an unknown-operation interrogation. The source
and receiver must remain blind to each fresh label in a genuine experiment.

## What to supply before adapting the reference matrices

| Interface input | Required record | Why the SU label does not settle it |
|---|---|---|
| Port ordering | Logical-to-connector and connector-to-detector maps; input/output direction | Mathematical row/column indices need not match connector labels |
| Compiler convention | Matrix direction, transpose/conjugation convention, phase gauge, determinant handling and quantization | A vendor may accept a different convention or choose a global phase |
| Control access | Which elements/sections can be changed independently and which are shared | Overall universality does not imply separable preparation/oracle/receiver roles |
| Operating light | Wavelength, bandwidth, polarization and permitted modes | Calibration only applies to its specified optical mode |
| Hidden section | Phase/loss locations, independent actuation, phase references and isolation | `O_j` is unitary while `T` requires actual attenuation |
| Chip connection | Coupling map, path stability, crosstalk, additional modes, loss and accessible output definition | Two available chips do not imply a characterized interconnection |
| Source | Pre-exposure herald/clock, vacuum/one-/multi-photon statistics, mean and tail-energy bounds | A photon presence probability does not establish its tail-energy budget |
| Readout | Detector channel map, simultaneous monitoring, gate width, dark counts, efficiencies, dead time and leakage handling | Eight ports do not imply eight simultaneous calibrated detectors |
| Timing | Phase settling, gated single exposure, label draw and isolation timing | A fast chip update is not itself a valid single-use trial rate |
| Calibration | Common-phase complex maps, uncertainty coverage and held-out drift model | Intensity fits and nominal specifications are not simultaneous confidence bounds |

Do not wait for all these values to run [commissioning references](COMMISSIONING.md).
Mark unsupplied fields as unsupplied. Actual compatible light/readout and the
lab's own control access are needed for physical commissioning; the full
[uncertainty worksheet](UNCERTAINTY.md) and fixed-N plan are additionally needed
before a certified acquisition.

## A hardware adapter is an explicit laboratory interface

The repository exports target matrices and record schemas; it does **not**
contain vendor drivers or working voltage control. A lab adapter should accept
a logical matrix plus its port/phase convention, compile it using documented
device calibration, and preserve the resulting settings with their calibration
and configuration identifiers. Voltage settings must come from the lab.

For interrogation, use separate preparation/receiver configuration and hidden
controller interfaces. The hidden controller writes a sealed label ledger;
it must not send the answer, a label-dependent setting filename, timing marker,
or accessible optical side channel to the reader. Trial records refer to a
phase-code family, not a reader-visible current answer. Join the labels only
after optical records are sealed for offline scoring.

An adapter also records pre-exposure aborts separately and confirms that they
send no uncounted signal across P0. A clock or source herald before exposure may
define a trial. A successful output coincidence cannot define it retrospectively.
Any rejected exposed record remains an attempt. Configuration changes belong
to separate identified pilot/test conditions; do not recalibrate on held-out
outcomes and then call the resulting receiver fixed.

## Optical phase and resource accounting

Use a common optical phase reference for the maps of all hidden labels. The
SU representatives on [SU4](SU4.md) and [SU8](SU8.md) specify one consistent
overall phase, not permission to erase different label phases. A label-dependent
global optical phase can be visible to the coherent comparator even when a
single-photon density operator is unchanged. Preserve it in the physical map.

Signal photons crossing P0, source herald photons, pump energy, local-oscillator
or reference power, total apparatus energy and wall-clock cost are distinct
reporting columns. P1 allows arbitrary permitted classical receivers, mixtures
whose preparation labels the receiver knows, phase references, and rare bright
pulses at the declared mean signal budget. It is not a comparison with one weak
laser control. The excluded photon architecture still has one photon in the
tested paths, no occupied bypass, retained idler, interacting ancillary photon,
memory, or repeated call to the same hidden setting.
