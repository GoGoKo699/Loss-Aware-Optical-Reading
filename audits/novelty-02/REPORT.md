# Focused source follow-up: S18, S20, and the multiclass bound

**The two named full-text gaps are resolved for this comparison. A newly located
2017/2018 predecessor substantially narrows Claim B's novelty: its generic
multiclass statistics bound follows from known duality and conclusive-filter
results. The optical certificate remains useful, but should be framed as an
application-specific corollary rather than an independent general discrimination
theorem. Claim A remains the leading candidate for a distinct theoretical result.**

Baseline: `db17e1ec1868107b0fe1042d5a480769b552633e`.
Branch: `audit/novelty-02`. Only this audit directory is added. Main, the canonical
proofs/code/claim ledger, experiment, prior audits, and frozen evidence are unchanged.
No merge, laboratory contact, experiment, manuscript, or release is part of this task.

## 1. What has actually been resolved

| Question | Result | Evidence |
|---|---|---|
| S18 full theorem and appendix comparison | Relevant full text inspected, not merely the abstract | arXiv:2603.19911v1, main definitions and Eqs. (22)-(23), Appendix B Lemmas 1-2, Appendix F Proposition 1, Appendix J Proposition 2; numerical SDPs screened by objective |
| S20 original theorem and conventions | Original article text recovered from an author upload | PRA 64, 062103, Theorem 1 and its proof; publisher metadata cross-checked |
| Close-equivalent finite-error multiclass bound | An exact no-failure predecessor and a short arbitrary-failure reduction found | Bagan et al., arXiv:1708.03968, PRL 120, 050402 (2018), Lemma 1; Bagan et al. 2012 conclusive-filter transformation |

S20 was read as the author's full embedded article text. The publisher PDF and
standalone ResearchGate PDF download were not recovered. This is a resolved
original-TEXT comparison, not a claim that a publisher PDF was downloaded.
S18 was read in arXiv HTML with the full PDF text also available. No external
numerical code or experimental figures were used as evidence for our results.

The [source inventory](SOURCES.md) records exact versions, locators, access
limitations and the smaller set of additional leads. These are bounded research
conclusions, not a worldwide priority certificate.

## 2. S18 addresses a different decision contract

Huang, Lami, Singh, and Wilde study energy-constrained binary asymmetric channel
discrimination. Their chain rule supports an adaptive error-exponent converse
and a finite-n version in Appendix F. Reference systems and repeated channel
uses are allowed. Their SDP objectives are channel divergences, not the uniform
multiclass correct/error/inconclusive score of this project.

Three distinctions prevent an incorrect reduction:

- Their Fock-diagonal optimum is a signal marginal of a purified probe. Dropping
  the reference is not an innocuous reinterpretation of that theorem.
- The coherent comparison described in Section III.2 is coherent input with
  heterodyne readout. It is not an upper bound on all classical receivers.
- The proved Appendix J truncation allowance concerns bosonic dephasing. It
  cannot certify every loss-dephasing or multimode reading problem by changing
  notation.

The audit includes a more concrete check than task labels. For distinct pure
coherent returns, the relevant relative entropies are infinite because the
one-dimensional supports differ. S18's principal divergence ceiling is then
vacuous when applied directly to that subcase, while the repository's finite
C/E/F bound is nontrivial. This does not invalidate S18 or exclude every future
connection to its methods. It shows why its displayed converse is not our result.

**Disposition:** S18 supplies important surrounding theory but does not directly
subsume either complete current claim. The previous abstract-only gap is closed
for the relevant statements. No external-paper correctness audit is claimed.

## 3. S20 is exactly the zero-error statistics endpoint

S20 bounds unambiguous discrimination of pure states with arbitrary priors by
one minus an ordered sum of weighted absolute overlaps. For equal priors it is
exactly

$$
C\le1-R,\qquad
R=\frac{1}{m(m-1)}\sum_{i\ne j}|\langle\psi_i|\psi_j\rangle|,
\qquad E=0.
$$

Both the ordered-pair normalization and the use of absolute, unsquared overlap
matter. This is the zero-error statistics step in our classical bound; it must
be credited. It is an upper bound, not an attained formula for all priors and
ensembles. Its discussion of sequential measurements is about the same specimen,
not repeated fresh illumination of an unknown optical device.

**Disposition:** inherited endpoint confirmed from original article text. S20
alone neither gives our finite-error optical theorem nor proves its novelty.

## 4. The decisive new predecessor is S22

Bagan, Calsamiglia, Bergou, and Hillery's *Duality games and operational duality
relations* contains the close equivalent that the earlier search missed. The
paper appeared as arXiv:1708.03968 in 2017 and PRL 120, 050402 in 2018.

Their Lemma 1 relates discrimination success to normalized l1 coherence. For
uniform priors its variables convert exactly into our no-inconclusive bound:

$$
R\le\frac{m-2}{m-1}E+2\sqrt{\frac{CE}{m-1}},\qquad F=0.
$$

The supplement's weighted-prior statement is important. A conclusive filter
changes the priors even when the original labels were uniform. Combining that
statement with the known Bagan-2012 filter transformation recovers the useful
upper-C inequality with arbitrary failure. [REDUCTIONS.md](REDUCTIONS.md) supplies
the complete argument, including singular filters, zero conditional weights,
the all-failure case and below-chance decoders.

This is stronger than saying the formulas look alike. The coefficients match,
and the needed finite-failure consequence follows through an explicit short
reduction. It is not a claim that the 2018 paper printed our full optical theorem
or experimental resource contract verbatim.

## 5. Consequence for the two contribution statements

| Component | Classification after this task |
|---|---|
| A: joint input-only retuning with diagonal loss, arbitrary final measurement and erasure accounting | Remains a candidate model-specific optimization reduction. These sources do not state that complete contract. Priority is not established. |
| B's zero-error overlap ingredient | Direct S20 specialization. |
| B's generic no-failure multiclass ingredient | Exact S22 normalization. |
| B's useful arbitrary-failure upper bound | Corollary of S22 plus the established S08 conclusive-filter transformation and elementary failure-overlap control. |
| B's coherent-map, spectral-norm and mean-energy-mixture extension | Short optical corollary using standard coherent overlaps and concavity; not an independently new general discrimination inequality. |
| General calibrated-map certificate as an operational tool | Retain with full assumptions. Its practical application may contribute, but this comparison does not establish a new generic theorem. |

The optical step is still necessary: for each coherent pulse, average overlap
is bounded below by exp(-kappa N), then concavity extends the correct-rate bound
to arbitrary intensity mixtures with mean <=mu. The proof therefore continues
to cover rare bright pulses; no numerical energy cutoff replaces it. But the
appearance of that physical source class does not justify calling its known
statistics ingredient newly discovered.

**Recommendation:** lead the theoretical narrative with Claim A and use Claim B
as the credited optical converse supporting a rigorous experiment. Do not present
them as two equally independent new mathematical principles without a further
substantive result or outside evaluation. The title or importance of a journal
cannot compensate for an inherited theorem.

The complete optical statement has not been located verbatim in the inspected
sources. This audit distinguishes that fact from a mathematical judgment: its
reduction to those sources is short enough that an independent claim of a new
general multiclass bound is not defensible. Whether the specialized application
and experiment provide sufficient publication significance remains a separate
scientific decision.

## 6. Effect on the first experiment

There is no new counterexample to the canonical mathematical bounds here, and
no reason from this comparison to replace the optical core. The meanings of the
existing tests remain:

M1 tests predicted input-only retuning with the fixed decoder. A scan is not a
proof of global optimality. P1 seeks an unconditional score above the correctly
credited all-classical ceiling. P2 requires a measured coherent strategy above
the entire declared four-path photon bound, not above one poorly chosen input.

The experiment could validate a useful implementation and source-class separation
even when its benchmark is a corollary. It must not be advertised as the first
observation of a newly invented general error/inconclusive tradeoff. The task
still has four promised phase patterns, one use per fresh hidden label, externally
justified illumination/calibration bounds, and no output postselection.

No laboratory assumptions have been filled in by this audit. No actual lab
feedback, calibration, data acquisition, or resource advantage is recorded.

## 7. Executed evidence

The independent script imports no canonical module or article code. It uses
explicit finite-dimensional state and measurement constructions to verify the
predecessor translations and boundary cases.

| Check family | Scalar checks |
|---|---:|
| S20 root-overlap normalization and zero-error examples | 64 |
| S22 exact no-failure relation and physical-branch monotonicity | 52 |
| Conditional-filter lift, including changed priors and edge cases | 248 |
| Nonzero-failure equality and feasible measurements | 144 |
| Coherent-map and finite pulse-mixture composition | 54 |
| S18 support and reference-system distinctions | 10 |
| Total | 572 |

All passed at the declared tolerance 2e-10. The largest residual was
1.2168044349891716e-13. A second new-directory execution reproduced RESULTS.json
byte for byte. The environment and full ledger are in EVIDENCE.tar.xz; SUMMARY.json
records their hashes. No finite sample proves the all-intensity or universal
predecessor implication; those rely on the written reductions.

The old 5,261-check and audit/repair suites were not rerun locally for this task.
Any branch CI success refers to the existing repository workflow, not the new
572-check script unless separately recorded. Remote content, parent and branch
checks identify the final committed result. Local work is an independent-script
workspace, not an authenticated repository checkout.

## 8. Completion boundary

This stage closes the named text-access comparisons and identifies a concrete
finite-error predecessor. It does not close every possible citation-network or
unpublished-priority question. A narrow set of additional retrieved abstracts and
metadata is recorded as scope screening only, not theorem exclusion.

The next authorized integration can update Claim B's attribution, its dependency
chain, and the contribution note using this packet. That edit is not performed
here. The useful next scientific judgment is the significance and robustness of
Claim A plus a credible experimental certificate, not another unbounded search
for an unrelated apparatus. Stop after preserving and verifying this audit.
