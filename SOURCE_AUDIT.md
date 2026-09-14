# Primary-source and novelty audit

Date: 2026-09-14. This is a bounded source comparison, not a priority certificate.
New derivations are in proofs/THEORY.md. External mathematical or experimental
facts are attributed below. An independently rederived expression is not thereby
new. No journal submission or empirical claim is made.

## Direct predecessors and the precise boundaries

### S1. Guha and Shapiro: single-photon phase-code optical reading

Saikat Guha and Jeffrey H. Shapiro, *Capacity of optical reading, Part 1: Reading
boundless error-free bits using a single photon*, arXiv:1207.6435v3;
Physical Review A 87, 062306 (2013).

https://arxiv.org/html/1207.6435v3
https://doi.org/10.1103/PhysRevA.87.062306

Full HTML reviewed. Single-photon path superposition, Hadamard phase coding,
passive decoding, photon budgets, loss degradation, and distinctions between
single-shot discrimination and capacity are prior work. This is a direct
predecessor, not background decoration. The proposed experiment must not claim
its four-mode routing mechanism or the general possibility of quantum reading
as new. The unequal-loss joint input/measurement score frontier and calibrated
finite-record comparison require more specific novelty evaluation.

### S2. Eldar and Forney: square-root measurement

Yonina C. Eldar and G. David Forney Jr., *On Quantum Detection and the Square-Root
Measurement*, arXiv:quant-ph/0005132.

https://arxiv.org/abs/quant-ph/0005132

Primary abstract and bibliographic record reviewed. The square-root measurement
and its optimality for appropriate symmetric ensembles are established tools.
The explicit uniform-loss POVM in this package is checked independently; its
minimum-error endpoint is not being claimed as a new measurement principle.

### S3. Primaatmaja, Ho, and Scarani: optical-mode discrimination toolbox

Ignatius William Primaatmaja, Asaph Ho, and Valerio Scarani, *Optimal single-shot
discrimination of optical modes*, arXiv:2012.11104.

https://arxiv.org/abs/2012.11104

Primary abstract/bibliographic content reviewed; full HTML retrieval failed.
Do not treat this as a completed theorem-level exclusion. The work addresses
energy-constrained optical-mode discrimination using rigorous optimization and
separates phase-referenced channel discrimination from photon-number-diagonal
source discrimination. Those distinctions predate this project. Its complete
methods must be compared before a claim of new optimized probe theory is made.

### S4. Error margins and fixed inconclusive rates

Ulrike Herzog, *Optimal state discrimination with a fixed rate of inconclusive
results: Analytical solutions and relation to state discrimination with a fixed
error rate*, arXiv:1206.4412.

https://arxiv.org/abs/1206.4412

E. Bagan, R. Munoz-Tapia, G. A. Olivares-Renteria, and J. A. Bergou,
*Optimal discrimination of quantum states with a fixed rate of inconclusive
outcomes*, arXiv:1206.4145.

https://arxiv.org/abs/1206.4145

Primary abstracts and descriptions reviewed; attempted full HTML retrievals
failed. These works already connect minimum-error, error-margin, and unambiguous
strategies and solve important symmetric cases. The full uniform classical curve
is at high risk of being an immediate specialization of existing state-measurement
results. Its all-coherent-illumination mean-budget upper proof is recorded, but
that alone does not establish its novelty. The broader single-photon theorem
also optimizes the input BEFORE an unknown loss/phase operation, which should be
compared separately rather than assumed novel because its notation differs.

### S5. Experimental error/inconclusive tradeoffs in path optics

L. F. Melo, M. A. Solis-Prosser, O. Jimenez, A. Delgado, and L. Neves,
*Experimental optimal discrimination of N states of a qubit with fixed rates of
inconclusive outcomes*, arXiv:2411.14537v1.

https://arxiv.org/html/2411.14537v1

Full HTML reviewed, especially the definitions and separation-plus-minimum-error
construction. It reports path-qubit implementations for 2,3,5,7 equally likely
symmetric input states. The ability to experimentally scan a reliability
tradeoff is not new by itself. Our proposed source retuning, flat code, loss
contract, and all-classical illumination comparison are the quantities requiring
an exact difference analysis. No comparison of uninspected figures is used.

### S6. Clements and colleagues: universal passive mode meshes

William R. Clements, Peter C. Humphreys, Benjamin J. Metcalf, W. Steven Kolthammer,
and Ian A. Walmsley, *An Optimal Design for Universal Multiport Interferometers*,
arXiv:1603.08788v2; Optica 3, 1460–1465 (2016).

https://arxiv.org/html/1603.08788v2

Full HTML reviewed. Universal mode unitaries and their beam-splitter/phase-shifter
implementation justify the decoder primitive. They do not confirm the intended
lab's source, phase bank, simultaneous output readout, native MZI convention, or
ability to isolate the hidden operation from compilation.

### S7. Statistical scope

Steven R. Howard, Aaditya Ramdas, Jon McAuliffe, and Jasjeet Sekhon,
*Time-uniform Chernoff bounds via nonnegative supermartingales*, arXiv:1808.03204.

https://arxiv.org/abs/1808.03204

Referenced to distinguish fixed-budget confidence from anytime-valid testing.
The implemented test is the elementary fixed-N bounded-score Hoeffding bound,
whose moment-generating-function proof is reproduced in THEORY.md. This package
does not implement or claim an optional-stopping guarantee from this reference.

## Project hardware source

The user's 24 August 2026 LAB_REVIEW_QUESTIONS.txt asks about balanced four-path
preparation, 0/pi phase control, separate/cascaded preparation and receiver,
native MZI conventions, simultaneous outputs, coherent versus photon tests, and
calibration/drift. It is a list of questions for initial review, not a confirmed
hardware inventory. The older global-mode report explicitly distinguishes one
photon in M paths from M-basis labels interpreted as multiple qubits.

No reference paper's source/detector specification is imported as the current
lab's equipment. No larger photon architecture is assumed.

## What this stage does and does not clear

The physical mechanism and the use of reliability tradeoffs are inherited.
The explicit fixed-decoder optimal-input theorem and general map-based classical
certificate have self-contained proofs and independent diagnostics here. They
are candidate technical contributions, not cleared novelty claims.

No exact full classical finite-error optimum for arbitrary unequal losses was
established. A rigorous upper bound supports the positive experimental test, and
an achieved classical score can support the reverse test. The gap between those
bounds must remain visible.

A specialist comparison of S2–S5 and the wider optimal-probe literature is still
required before manuscript-level priority assertions. The source audit records
failed full-text retrievals rather than pretending an abstract establishes the
absence of a result. The experiment can be reviewed for feasibility without
resolving every publication question in advance; a journal-level claim cannot.
