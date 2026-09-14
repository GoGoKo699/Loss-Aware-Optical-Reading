# Physical setting and scope

The baseline is a programmable SU(4)/SU(8) mode interferometer using global path
encoding and one computational photon at a time. Existing larger photonic
platforms may be proposed when they simplify the experiment. Synchronized
multiphoton computation, interacting ancillary photons, quantum memory, and
recirculation are not assumed.

## Four-symbol task

Exactly one of four tested paths receives a pi flip, with a uniform hidden label.
This is reading a promised phase code, not fault diagnosis with an extra healthy
case. The source prepares a path superposition, the unknown section applies its
physical phase-and-loss map, and a fixed receiver is followed by four detectors.

Known, hypothesis-independent diagonal transmission is the ideal photon model.
Distributed chip loss or unequal downstream detectors cannot silently be folded
into those four transmissions. The general-map classical bound and its
calibration intervals have their own assumptions in `proofs/THEORY.md`.

The input optimality excludes an occupied bypass rail, a retained idler, and
multiple interrogations of the same setting. The classical comparison allows
coherent-state mixtures, rare bright pulses, phase references, and arbitrary
receivers. It is not restricted to matching the implemented laser control.

## Physical interfaces to confirm with the laboratory

Preparation, the hidden operation, and the receiver must be separable. The
reader cannot receive the hidden answer as a compiler input. Physical maps must
share a calibrated phase reference: independently discarding each map's global
phase changes the coherent-light comparison.

Signal illumination is charged at the plane just before the unknown operation.
The competitor may use any receiver after the declared device-output plane.
Our decoder and detector losses reduce our score, not the competitor's ceiling.
The score is not a total pump-energy, source-cost, or wall-clock comparison.

A source herald may define a trial before interrogation. No-click, multiple-click,
and rejected output records remain trials. Each interrogation receives a fresh
independent uniform hidden label. Fixed-label repeated estimation is another task.

## Stage and evidence

The first deliverable is self-contained theory, validation, and an initial
technical laboratory-review proposal. The example transmissions, noise values,
source probabilities, and sample counts are hypothetical. No laboratory has
been declared calibrated in this repository. Complete the questions in
`experiment/LAB_REVIEW.md` before treating those values as feasible.

A simple established optical mechanism is acceptable only if the substantive
result is new. The central performance benefit must be quantum under matched
input access and resource accounting; a favorable normalized intensity pattern
alone is insufficient. A reusable coherent loss gate or learning algorithm is
not required by the current project scope.
