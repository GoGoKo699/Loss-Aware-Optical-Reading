# Claim-by-claim predecessor map

Target: repaired baseline `80c73751806f45411251711bcfb6bccebc887f0a`.
Classification is about the inspected literature, not mathematical validity.
Source IDs resolve in [SOURCES.md](SOURCES.md); equation translations are in
[REDUCTIONS.md](REDUCTIONS.md).

| ID | Baseline result or possible headline | Closest predecessor/translation | Disposition |
|---|---|---|---|
| C01 | Single photon reads a four-symbol phase code with a passive fixed receiver | S01 Eqs. 7-8; S03 one-flip oracle case | Established mechanism; not a new reading algorithm. |
| C02 | D is the minimum-error receiver for any fixed positive input distribution | S04 Sec. 8.3, constant-diagonal Gram square-root criterion; R1 | Exact specialization. Applies without requiring a cyclic group code. |
| C03 | Error-free harmonic-mean rate and inverse-loss preparation | S02 Eq. 3.15 plus Gram feasibility and source normalization; R2 | Direct/routine corollary; useful explanatory endpoint, not a lead novelty claim. |
| C04 | One fixed decoder plus retuned input attains the entire joint optimum under arbitrary positive diagonal loss | S05/S06 show general joint/loss-aware optimization is established; S07/S08 fix received states; R3 isolates the remaining normalization argument | Candidate model-specific joint-design reduction. Exact same contract not located in inspected results; priority not certified. |
| C05 | Minimum-error endpoint, partial vacuum guessing, and support-to-frontier conversion | C04, existing decision theory, and S07/S08 | Supporting consequences. Do not count every endpoint as an unrelated new theorem. |
| C06 | Uniform four-coherent-state finite-error curve and its POVM | S07 Eq. 4.18, N=4 and positive overlap; R4 | Exact fixed-alphabet reparameterization. Must be credited. |
| C07 | The same uniform curve remains optimal over arbitrary classical signal mixtures at a mean budget | C06 does not optimize the transmitter; requires the baseline optical converse; R6 | Candidate optical source-class strengthening, not a new fixed-state measurement curve. No independent novelty claim for Jensen alone. |
| C08 | Spectral map contrast and eigenmode selection | S11 Eqs. 1-3; H=D12/2 at m=2; R6 | Binary core inherited. General multiclass H is a converse quantity, not proved globally optimal receiver/source design. |
| C09 | Multiclass correct/error converse for general calibrated passive maps and unrestricted intensity mixtures | S10/S14/S19 overlap bounds, S11 binary contrast, R6 optical averaging/concavity | Candidate composite bound under a precise source/map contract. General-map tightness not established; broad priority not established. |
| C10 | Coherent background nulling and click detection | S12 Secs. 5.1-5.2; displaced one-flip code is PPM; R5 | Established receiver ingredient. |
| C11 | Weak-path abandonment and water-filling allocation within nulling | Ordinary KKT optimization of a separable concave objective; R5 | Routine allocation rule, not a standalone discovery of a classical optimum. |
| C12 | Full four-state factorized-Gram USD optimum and one-bad-path mean-budget converse | S10/S13/S12 give established feasibility and regime changes; R7 | Specialized closed form/converse remains candidate. Exact predecessor not identified in inspected passages. The high-energy non-nulling branch must be retained. |
| C13 | Specific single-photon/classical crossover | Algebra from C03 and C12; S09 Sec. V already discusses loss-dependent preferred probes | Useful consequence of optimized comparisons; do not claim the first loss-driven source reversal. |
| C14 | Calibration-radius and trace-distance perturbation bounds | Stacked operator norm triangle, bounded-payoff continuity; S14 Appendix F | Routine mathematical wrappers; necessity is not novelty. |
| C15 | Fixed-N statistical certification, energy-affine tangent, union bound | Standard concentration/concavity arguments; S21 scope distinction | Application-specific safe accounting, not a new concentration theorem or anytime-valid test. |
| C16 | Exact-rational photon support enclosure | Monotone scalar-root signs and directed conversion in repair 01 | Numerical reliability contribution; not independent physical novelty or certification of every pipeline function. |
| C17 | Experimental scan of error/inconclusive tradeoff | S15 Secs. III-IV implements the general idea using classical-wave emulation | Scanning the curve is not new. Our all-attempt, signal-budget source comparison is a different experimental claim that remains unperformed. |
| C18 | Adaptive repeated-query, total-dose, generic fault diagnosis, or universal quantum superiority | S09/S14/S17/S18 illustrate why access/metric distinctions matter | Not established by this repository; no new claim added. |

## What the record permits next

The paper can use C01-C03 and C06 as credited building blocks. C04 and C09 are
the most useful pair of candidate technical statements to emphasize. C12/C13
provide a concrete sharply solved comparison, but should remain under their
restricted one-bad-path and score assumptions. The next contribution note should
expose these reductions rather than conceal them.

A source not found in a bounded search is not a certificate of novelty. The
candidate labels mean only that the inspected statements and explicit reductions
did not subsume the complete contract. They are not predictions of peer review
or journal acceptance. No canonical claim ledger was edited in this audit.
