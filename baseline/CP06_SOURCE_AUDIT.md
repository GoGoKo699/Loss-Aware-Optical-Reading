# Primary-source and novelty audit

Checked online on 2026-09-14. This is a bounded predecessor assessment, not a
priority certificate. No publication is bundled in the archive. URLs below
identify the material consulted; live websites may change.

## S1. Direct optical-reading predecessor

Saikat Guha and Jeffrey H. Shapiro, *Reading boundless error-free bits using a
single photon*, Physical Review A 87, 062306 (2013).

- https://doi.org/10.1103/PhysRevA.87.062306
- https://arxiv.org/abs/1207.6435
- https://arxiv.org/pdf/1207.6435

Inspected the primary abstract and PDF, especially the Hadamard/Green-Machine
and single-photon W-state receiver sections and the end-to-end loss discussion.
The paper already supplies the central known mechanism: distribute one photon
over paths, apply a binary phase code, and use a fixed passive interferometer
and photon counting to identify its label. Uniform-loss erasures are explicitly
discussed. It also compares coherent-state reading and stronger joint receivers.

Consequences: do not claim invention of phase-to-port reading, Hadamard decoding,
single-photon optical reading, or the mere existence of a photon-budget quantum
benefit. Uniform-loss statements in this checkpoint are specializations and
benchmarks, not standalone novelty claims. The current calculation concerns a
fixed four-label task, unequal path loss, fully optimized classical positive-P
illumination under a mean budget, and an explicit crossover.

## S2. Direct oracle-discrimination predecessor

Anthony Chefles et al., *Unambiguous discrimination among oracle operators*,
Journal of Physics A: Mathematical and Theoretical 40 (2007).

- https://arxiv.org/abs/quant-ph/0702245
- https://arxiv.org/pdf/quant-ph/0702245
- https://doi.org/10.1088/1751-8113/40/33/016

Inspected the primary abstract and PDF. It treats oracle discrimination,
including Grover-type phase oracles and multiple queries. The four-item pi-phase
oracle should not be renamed as a new algorithm. Our four-path optical circuit
is closely related to the familiar four-item exact phase-oracle readout.

Remaining comparison: determine whether any unequal-loss, source-optimized
unambiguous result already subsumes the harmonic-mean specialization. A new
name for the same oracle would not be a contribution.

## S3. Energy-constrained optical discrimination

Ignatius William Primaatmaja, Asaph Ho, and Valerio Scarani, *Optimal single-shot
discrimination of optical modes*, Physical Review A 103, 052410 (2021).

- https://arxiv.org/abs/2012.11104
- https://arxiv.org/pdf/2012.11104
- https://doi.org/10.1103/PhysRevA.103.052410

Inspected the primary abstract and PDF mathematical setup, including the
channel/source distinction, unambiguous outcomes, and energy-constrained
optimization. It establishes general LP/SDP methodology. The distinction between
phase-referenced coherent discrimination and photon-number-diagonal sources is
important; this checkpoint does not impose phase randomization on the classical
probe. Finite photon-number/energy mixtures must not be omitted from a mean-budget
comparison. Optimization by a convex program is not novel in itself.

Our calculation uses analytic Gram-matrix certificates and a global supporting
line for arbitrarily bright classical pulses. The numerical code uses SciPy
linear programming and differential evolution only; no SDP solver was run.
A full theorem-level subsumption check is still required.

## S4. Coherent displacement and click receivers

Jasminder S. Sidhu, Michael S. Bullock, Saikat Guha, and Cosmo Lupo, *Linear optics
and photodetection achieve near-optimal unambiguous coherent state discrimination*,
Quantum 7, 1025 (2023).

- https://quantum-journal.org/papers/q-2023-05-31-1025/
- https://arxiv.org/abs/2109.00008
- https://doi.org/10.22331/q-2023-05-31-1025

Inspected the primary article page and receiver description. Passive optics,
coherent displacement, vacuum auxiliary modes, and on-off detection are known
receiver ingredients. Our displacement-and-click competitor must not be treated
as a deliberately weak intensity detector. The proof actually upper-bounds
arbitrary receivers and then proves attainability for the chosen loss family.

## S5. Native mode-unitary implementation

William R. Clements et al., *An Optimal Design for Universal Multiport
Interferometers*, Optica 3, 1460-1465 (2016).

- https://arxiv.org/abs/1603.08788
- https://arxiv.org/html/1603.08788v2
- https://doi.org/10.1364/OPTICA.3.001460

Inspected the primary HTML. It provides the mode-unitary/beam-splitter mesh
primitive. The same mode matrix acts on classical fields and single-photon
amplitudes. A matched normalized intensity pattern is therefore not by itself
a quantum advantage. Our benchmark concerns unconditional optical discrimination
per incident signal-photon budget, including inconclusive trials.

It does not verify any particular lab's preparation section, source purity,
loss map, detector array, or compiler interface.

## S6. Related but not used as the main bound

Ranjith Nair, *Discriminating quantum-optical beam-splitter channels with
number-diagonal signal states: Applications to quantum reading and target
detection*, Physical Review A 84, 032312 (2011).

- https://arxiv.org/abs/1105.4063
- https://doi.org/10.1103/PhysRevA.84.032312

Primary abstract consulted. This is prior art on quantum/coherent probe
comparisons for lossy channels. It addresses binary minimum-error problems and
more general signal/idler resources. It should not be asserted to prove or to
exclude the present four-hypothesis unambiguous specialization without a full
mapping. No conclusion here is based solely on this abstract.

## Project source used for physical alignment

User File Library: `LAB_REVIEW_QUESTIONS.txt`, dated 2026-08-24. The four-mode
optical-fault branch asks about preparation of (1,1,1,1)/2, a phase change on the
fourth path, separate/cascaded preparation and receiver sections, direct receiver
MZI control, output labels, randomized held-out trials, and coherent-light versus
single-photon runs.

Those are questions in a proposal, not confirmed laboratory specifications. The
current four-hypothesis task is a proposed extension of its binary healthy/fault
example. It needs a controller capable of choosing the phase flip on any of four
paths without exposing that choice to preparation or decoding. The prior project
files and old checkpoints were not edited.

## Search boundaries and claim status

Searches covered combinations of optical reading, Hadamard phase codes,
nonuniform/unequal loss, unambiguous oracle discrimination, energy-constrained
optical discrimination, coherent-state Gram matrices, harmonic-mean compensation,
and coherent displacement receivers. Irrelevant general web pages, reviews of
unrelated sensors, and secondary topic summaries were not used as evidence of
novelty. Some publisher/HTML fetches failed; the corresponding arXiv PDF or
primary institutional/publication record was used when available.

The search found direct predecessors for the physical mechanism and mathematical
methods. It did not establish a priority claim for the exact one-bad-path
classical envelope, crossover, or finite-error bound. The current contribution
candidate is their explicit analytical combination, together with a short
realizable quantum receiver and a full mean-energy accounting.

Required before a final project freeze: compare the exact formulas, not only
keywords, with the optical-reading and unambiguous coherent-discrimination
literature. Known general results may subsume parts or all of the candidate.
