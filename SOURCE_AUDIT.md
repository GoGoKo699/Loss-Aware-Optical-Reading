# Source map and contribution boundaries

**The bounded predecessor comparison is complete; publication-level priority is
not cleared.** Its original report, source inventory, equation reductions, search
log, and evidence are preserved in [audit/novelty-01](audits/novelty-01/README.md).
This page integrates that record; it does not claim a new literature search.

The two candidate contributions are stated in
[docs/CONTRIBUTIONS.md](docs/CONTRIBUTIONS.md). The
[claim ledger](CLAIM_STATUS.md) separates correctness, novelty, and experiment.
Source IDs below use the audit's S01-S21 numbering. Earlier checkpoint source IDs
are historical and should not be silently reused with different meanings.

## What is already known

| Result used here | Primary predecessor and locator | Our interpretation |
|---|---|---|
| Single-photon phase-code reading and passive decoding | Guha and Shapiro, [1207.6435v3](https://arxiv.org/html/1207.6435v3), Eqs. (7)-(8), Sec. IV [S01]; Chefles et al., [quant-ph/0702245](https://arxiv.org/abs/quant-ph/0702245), Sec. V [S03] | The optical mechanism and the exceptional four-label one-flip case are inherited. |
| Fixed-input code decoder | Eldar and Forney, [quant-ph/0005132](https://arxiv.org/abs/quant-ph/0005132), Sec. 8.3 [S04] | The constant-diagonal Gram square-root criterion identifies this decoder. |
| Zero-error inverse-loss preparation | Chefles and Barnett, [quant-ph/9807023](https://arxiv.org/abs/quant-ph/9807023), Eq. (3.15) [S02], and standard Gram feasibility | The harmonic mean is a specialization plus normalization, not a new general discrimination principle. |
| Uniform coherent fixed-alphabet curve | Herzog, [1206.4412](https://arxiv.org/abs/1206.4412), Eq. (4.18) [S07] | Exactly the same curve after N=4, S=exp(-t mu), and Q=F. A separate argument is needed to optimize over transmitters. |
| Filtering and joint probe/measurement error margins | Bagan et al., [1206.4145](https://arxiv.org/abs/1206.4145), Eqs. (6)-(8) [S08]; Hashimoto et al., [0912.2610](https://arxiv.org/abs/0912.2610), Sec. II [S05] | These task types and measurement decompositions are established. |
| Loss-aware optical probe optimization | Nair and Yen, [1107.1190](https://arxiv.org/abs/1107.1190), Theorem 1 [S06]; Primaatmaja et al., [2012.11104](https://arxiv.org/abs/2012.11104), Sec. V [S09] | Loss-dependent preferred probes are known. Preserve each paper's signal/idler and phase-reference access model. |
| Binary spectral contrast | Bouchet et al., [2108.03755v2](https://arxiv.org/html/2108.03755v2), Eqs. (1)-(3) [S11] | Our binary contrast is half their discrimination operator. The multiclass average is a converse quantity, not a proved optimal input rule. |
| Coherent displacement and click detection | Sidhu et al., [2109.00008](https://arxiv.org/abs/2109.00008), Secs. 5.1-5.2, Appendix B [S12] | Known receiver ingredients. Optimizing this receiver alone does not bound every allowed measurement. |
| Experimental error/inconclusive scans | Melo et al., [2411.14537v1](https://arxiv.org/html/2411.14537v1), Secs. III-IV and footnote 4 [S15] | The cited realization uses laser/camera emulation. It is not an all-classical-source signal-photon advantage test. |

The [equation reductions](audits/novelty-01/REDUCTIONS.md) explain these statements.
In particular, R4 gives the exact Herzog substitution and R6 gives the binary
factor of two. The full [21-source inventory](audits/novelty-01/SOURCES.md)
includes overlap bounds, approximate unambiguous discrimination, and recent work.

## What remains a candidate contribution

**A: joint input-only retuning.** The model-specific argument optimizes the input
before unequal loss and an arbitrary final measurement, including erasure. A
known measurement for a fixed received ensemble does not alone establish that
joint optimum. See audit claims C04-C05 and reduction R3.

**B: the multiclass all-classical-source optical converse.** The bound covers
alternative coherent illuminations, arbitrary receivers, known mixture labels,
phase references, and unbounded pulse-energy mixtures under the mean budget.
The known uniform fixed-alphabet solution attains it there; the arbitrary-map
bound is not generally asserted to be tight. See C07-C09 and R6.

The one-bad-path zero-error optimum and crossover remain supporting candidate
results under their original restrictions, not another general framework. The
high-energy non-nulling measurement branch must be included in an all-source
proof. Standard KKT allocation, Jensen, triangle inequalities, fixed-N
concentration, and numerical enclosure methods are not separate physical
novelty claims. See C10-C16 and R5-R8.

## Coverage and unresolved items

The audit records 21 primary references and relevant full-text passage inspection
for 18; two of those recent papers received formal-scope screening only. This
integration preserves that level of evidence. It does not upgrade a scope screen
to a full theorem exclusion.

The earlier failed HTML retrievals for Herzog, Bagan, and Primaatmaja were
resolved using PDFs during the audit. The original full text of the older S20
unambiguous-discrimination bound remains unrecovered; its equation was checked
through primary source S19. Recent bosonic-channel source S18 still needs a full
theorem/appendix comparison. Equivalent multiclass bounds and wider citation
coverage also remain open. Exact tasks are recorded in
[audit SOURCES.md](audits/novelty-01/SOURCES.md) and
[SEARCH_LOG.json](audits/novelty-01/SEARCH_LOG.json).

No failure to find a result is proof that it is new. Outside specialist review,
priority evaluation, and experimentally demonstrated advantage remain separate.
The 631 translation checks establish consistency of substitutions and examples,
not absence of predecessors.

## Hardware and statistical boundaries

The project's laboratory questions are not a confirmed equipment inventory.
Universal interferometer construction is an established primitive, as described
by Clements et al., [1603.08788](https://arxiv.org/abs/1603.08788); it does not
establish the source, separated hidden-operation interface, calibration, or
receiver availability of the intended installation.

The current trial test is fixed-N with the stated independent or conditional
energy assumptions. It imports no optional-stopping guarantee from the stronger
time-uniform literature. It counts signal illumination, not pump energy, total
power, or wall-clock efficiency. [LAB_REVIEW.md](experiment/LAB_REVIEW.md) is the
technical feedback entry, not approval to run an experiment.

The original source audit remains in the unchanged checkpoint archive and Git
history. This current map supersedes its unresolved-retrieval status where the
later audit actually recovered the text; it does not rewrite the historical audit.
