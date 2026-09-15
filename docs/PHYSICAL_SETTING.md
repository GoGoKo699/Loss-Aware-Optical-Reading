# Physical setting and scope

**Both an SU(4) chip and an SU(8) chip are available in the laboratory.**
Use [SU4](../experiment/SU4.md) or
[SU8](../experiment/SU8.md) to choose an experiment. This confirmation concerns
the processors; their complete experimental interfaces and calibration have not
been supplied.

## One photon in global paths

One computational photon occupies a superposition of four or eight optical
paths. Path count is not photon count or a set of independently carried qubits.
No synchronized multiphoton computation, interacting ancillary photons, retained
idler, occupied bypass rail, quantum memory or recirculation is included.
A source herald before exposure can define an attempt and remains outside the
computational signal. Each counted attempt uses one newly sampled independent
hidden label and at most one interrogation of that setting.

The principal task has four equally likely labels: exactly one tested path
receives a pi flip. There is no fifth healthy hypothesis. SU8 can implement this
same task in ports 0–3 with its remaining inputs in vacuum. Native eight-mode
reading uses the explicit Walsh phase code, not eight single-path flips.

## Separate physical roles and accounting planes

The [apparatus guide](../experiment/INTERFACES.md) shows preparation, P0, the
hidden phase/loss section, P1, the fixed receiver and readout. P0 is immediately
before the declared unknown device and charges incident signal photons per
attempt. P1 is the accessible device output, before the chosen receiver.
The competing source class may use any receiver after P1.

Known positive, label-independent diagonal transmission is the ideal photon
model. Its matrix T is a contraction, not an SU unitary. Phase-only programming
does not implement attenuation. Distributed loss, extra chip/decoder loss and
unequal detector efficiencies cannot silently be reassigned to T. Our receiver
loss lowers achieved performance; it does not automatically lower an unrestricted
competitor's ceiling. A general-map or noise model needs its declared assumptions
and simultaneous uncertainty envelope.

The hidden answer must not reach the preparation or receiver compiler. Compiling
one answer-dependent end-to-end matrix verifies optical transfer, not an unknown
operation. Both chips may be used together, but coupling and the independent
hidden section are proposed connections, not confirmed assemblies. Neither chip
is assumed to contain three separately controlled full processors.

## Interfaces still to supply

| Laboratory input | Why it matters |
|---|---|
| Physical port ordering and measured logical-port map | Repository indices are 0-based conventions, not inferred vendor labels. |
| Compiler row/column, phase, sign and determinant conventions | Complex transfer amplitudes and common optical phase must match the target. |
| Accessible control sections and independent phase/loss operations | Establish preparation/hidden-operation/receiver separation; identify actual attenuation. |
| Wavelength, polarization, bandwidth and stability | Determine the optical mode to which the model and calibration apply. |
| Source statistics and P0 mean/tail bounds | Establish the charged incident resource, including vacuum and high-number tails. |
| Detector arrangement and complete readout | Count no-click, multiple-click and leakage on every fixed gate. |
| Inter-chip coupling and losses | Determine whether the proposed cascade is feasible and where its losses belong. |
| Timing, settling, gates, independent label control and blinding | Establish the single-use iid-label contract and attainable attempt rate. |
| Simultaneous calibration uncertainty and test-time drift | Turn fitted maps into justified bounds rather than illustrative parameters. |
| Coherent displacement and phase-reference arrangement for P2 | Implement the particular classical receiver without label knowledge. |

A common optical phase convention must hold across all hidden settings. An SU
compiler cannot introduce or discard different label-dependent global phases:
those change coherent-state discrimination with a phase reference. One common
phase across the whole family can be tracked consistently.

## Data and claim boundaries

Count correct, wrong and inconclusive outcomes per attempted interrogation.
No-click, multiple-click, leakage and rejected records remain attempts. A clock
or source herald before exposure defines a trial; an output coincidence cannot
define it retrospectively. Keep pilot/calibration/test records distinct and N
fixed before held-out data. No optional-stopping claim is made.

The classical comparator includes coherent mixtures, receiver-known preparation
labels, phase references, rare bright pulses and arbitrary receivers. Signal
illumination is distinct from pump energy, herald photons, reference power,
source cost, total apparatus energy and wall-clock time.

The [uncertainty worksheet](../experiment/UNCERTAINTY.md) can be completed later.
Its absence does not prevent classical-light commissioning or reference-level
handover. No illustrative transmission, source purity, noise range or sample
count is a measured hardware specification. M1/P1/P2 retain the
[original acquisition protocol](../experiment/FIRST_EXPERIMENT.md).
