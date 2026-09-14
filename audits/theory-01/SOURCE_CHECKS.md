# Bounded primary-source checks

This is source checking for the mathematical/operational audit, not the next
novelty audit. Checked 2026-09-14. No source is credited with validating the
repository's new theorem merely because its abstract uses related terminology.
The canonical SOURCE_AUDIT.md remains unchanged.

## Optical access model

I. W. Primaatmaja, A. Ho and V. Scarani, *Optimal single-shot discrimination of
optical modes*, arXiv:2012.11104v1, PRA 103, 052410 (2021).

https://arxiv.org/html/2012.11104v1
https://doi.org/10.1103/PhysRevA.103.052410

Full HTML text was accessible in this audit. Section I explicitly distinguishes
a phase-referenced channel scenario from a photon-number-diagonal source
scenario. Sections II and III formulate energy-constrained discrimination and
separate direct measurement optimization from photon-number allocation. This
supports the need to keep optical phases, access to references and source energy
in the task definition. We do not infer that its optimization directly proves
or excludes the current arbitrary-loss photon theorem. No figure interpretation
is used in this check.

This updates a retrieval limitation, not the novelty status: the canonical source
ledger said that an earlier full-text retrieval failed. The later successful read
is recorded here without rewriting that historical record.

## State-measurement mathematics

Y. C. Eldar and G. D. Forney Jr., *On Quantum Detection and the Square-Root
Measurement*, arXiv:quant-ph/0005132.

https://arxiv.org/abs/quant-ph/0005132

The primary bibliographic record and abstract explicitly state minimum-error
optimality for geometrically uniform pure-state ensembles. The audit checks
attainment through an explicit Gram-matrix contraction and matching upper bound;
it does not use a novelty assertion about the square-root measurement.

U. Herzog, *Optimal state discrimination with a fixed rate of inconclusive
results: Analytical solutions and relation to state discrimination with a fixed
error rate*, arXiv:1206.4412.

https://arxiv.org/abs/1206.4412

Primary abstract/bibliographic content checked. Full HTML attempts for v1 and v2
failed in this turn. The record states that fixed-inconclusive and fixed-error
solutions can be transformed into one another and that symmetric ensembles are
studied. This confirms the standard setting, not absence of our specialization
from the full paper. Theorem-level priority checking remains outside this audit.

C. A. Fuchs and C. M. Caves, *Mathematical Techniques for Quantum Communication
Theory*, arXiv:quant-ph/9604001.

https://arxiv.org/abs/quant-ph/9604001

Primary record checked for fidelity and measurement-distinguishability context.
The overlap-to-outcome inequality used here is proved directly by POVM
completeness and Cauchy-Schwarz; no uninspected theorem is essential to the audit.

## Statistical contract

S. R. Howard, A. Ramdas, J. McAuliffe and J. Sekhon, *Time-uniform Chernoff bounds
via nonnegative supermartingales*, arXiv:1808.03204.

https://arxiv.org/abs/1808.03204

Primary record/abstract checked; attempted HTML retrieval failed. The paper
addresses time-uniform martingale bounds. The repository implements a fixed-N
bounded-score test, independently derived in the audit note. No optional-stopping
permission is imported from this citation.

## Optical mechanism and terminology

S. Guha and J. H. Shapiro, *Capacity of optical reading, Part 1: Reading boundless
error-free bits using a single photon*, arXiv:1207.6435v3.

https://arxiv.org/html/1207.6435v3

Full HTML text accessible. Single-photon phase coding, passive decoding and loss
sensitivity are inherited optical-reading mechanisms. The audit does not promote
them to novel contributions or convert a single-use test into a capacity result.

P. Deuar and P. D. Drummond, *First-principles quantum dynamics in interacting
Bose gases I: The positive P representation*, arXiv:cond-mat/0412174.

https://arxiv.org/abs/cond-mat/0412174

Primary record confirms positive-P as a representation used for full quantum
dynamics, not as the source-class condition of this optical-reading comparison.
The audit also located authors' and published material explicitly distinguishing
the doubled phase space from the diagonal Glauber-Sudarshan representation.
The canonical mathematical definition is correct; the isolated code docstring
'positive-P mixtures' should be replaced by its explicit intended source class.

## What was not done

No new exhaustive literature search, priority clearance, hardware availability
survey, legal/licensing review, paper drafting or source-purity calibration was
performed. The inaccessible full texts above cannot support a negative novelty
claim. All independent conclusions are tied to the equations and resource
contracts in INDEPENDENT_DERIVATIONS.md.
