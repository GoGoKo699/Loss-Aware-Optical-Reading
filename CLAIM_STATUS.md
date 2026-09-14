# Claim-status ledger

This ledger separates mathematical correctness in a model, numerical validation,
implementation assumptions, and novelty. None can stand in for another.

| Claim | Evidence in this package | Domain or missing step |
|---|---|---|
| Fixed decoder reaches the entire ideal photon reliability frontier | Explicit upper bound and attaining preparation; independent eigenproblem/dual/POVM checks | Uniform flat orthogonal code, arbitrary positive diagonal loss, one photon in tested paths, no occupied reference/idler |
| Zero-error harmonic-mean rule | Recovered as a limit and independently rerun baseline proof | Error-free answers, not arbitrary finite-error preparation |
| Complete classical finite-error frontier at uniform four-one-flip loss | General coherent-mixture upper bound plus matching Gram/POVM construction | Arbitrary receiver exists mathematically; not all points implemented by the proposed click receiver |
| General calibrated-map classical correct/error certificate | Coherent-overlap and measurement-fidelity proof; concavity handles all intensity mixtures | Passive coherent maps, uniform labels, signal mean budget, phase-referenced map envelope; generally not tight |
| Robust contrast from operator-norm intervals | Triangle/operator norm inequality | Calibration must actually supply simultaneous valid radii, not fit residuals |
| Linear fixed-score test and fixed-N confidence | Analytic supporting witness and bounded-mgf proof | Preregistration; iid or explicit conditional predictable-budget assumptions; energy tails externally bounded |
| Robust reverse comparison against all four-path photons | Exact score bound plus trace-distance perturbation bound | A measured coherent receiver is still needed; excludes only the declared one-photon architecture |
| Moderate-imbalance positive margin | Finite-source/detector model and synthetic count example | Hypothetical parameters only; source presence and map calibration not measured |
| Severe-imbalance reverse margin | Explicit coherent nulling model and synthetic count example | Coherent displacement, phase stability, energy upper bound, and real readout to be confirmed |
| 5,261 new consistency checks | Reproducible scripts and per-check ledger | Floating-point checks; not external validation or an exact interval certificate |
| Checkpoint-06 results retained | Original archive hash; independent extracted rerun with 4,453 checks | Its claims stay under its original scope, not generalized silently |
| The optical mechanism or general error-margin method is new | NOT CLAIMED | Direct predecessors are listed in SOURCE_AUDIT.md |
| The new theorem package clears publication novelty | NOT ESTABLISHED | Further theorem-by-theorem comparison and specialist review required |
| Exact arbitrary-loss classical finite-error boundary | NOT ESTABLISHED | Current arbitrary-map upper bound suffices for positive certification; do not plot it as an attained frontier |
| Adaptive multi-query or total-dose advantage | NOT ESTABLISHED | Different access model; iid repeated single-use gates do not prove it |
| Actual laboratory implementation fits the proposed margins | NOT ESTABLISHED | Initial technical review, then pilot calibration, then preregistered held-out test |

## Changes to the interpretation of earlier checkpoints

The main new result is finite-error input retuning with a fixed ideal decoder.
The inverse-loss preparation is optimal only at the zero-error endpoint, not
throughout the decision tradeoff.

The classical comparison must retain the optical phase of every hidden physical
setting. Independently choosing global phases for four SU(4) matrices changes the
coherent comparator even when it leaves one-photon probabilities unchanged.

A predicted crossing is not an observed reverse advantage. The negative primary
test now requires an actually implemented coherent control above an upper bound
for the entire stated photon class.

The first experiment remains single use per independently hidden label. No result
for adaptive reuse of the same label is inferred.
