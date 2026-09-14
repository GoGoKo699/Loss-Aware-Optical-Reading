# Source/version and inspection record

Reading date: 15 September 2026 (project timezone). IDs S01-S21 retain their
meanings from audit 01. S22-S25 are additional records for this follow-up only;
no older inventory or canonical source map is rewritten. Links identify primary
research texts or their official records. Original prose and complete external
articles are not redistributed in this packet.

## S18. Huang, Lami, Singh, and Wilde

*Efficiently Computable Strategies and Limits for Bosonic Channel Discrimination*,
[arXiv:2603.19911v1](https://arxiv.org/html/2603.19911v1), submitted 20 March 2026.
The [PDF](https://arxiv.org/pdf/2603.19911) was available to the web parser as a
29-page document. The actual comparison uses this arXiv version, not an assumed
identical later publisher version.

**Recovered and inspected:** main Secs. II-III, definitions (1)-(8), chain rule
(23), exponent statement (22); Appendix A divergence conventions; Appendix B
Lemma 1 / (59)-(68) and Lemma 2 / (69)-(79); Appendix F Proposition 1 / (144)-(163);
Appendix J Proposition 2 / (238)-(253). Appendices D/E/H were inspected for their
binary relative-entropy/SDP objectives, not rerun or independently proved. The
bosonic channel definitions and the numerical comparator specification in
Sec. III.2 were also read. Appendices C/G supply supporting operator/channel
notation; Appendix I is a numerical truncation example, not theorem evidence
for this project's certificate. No numerical figure was used for a claim.

**Result:** the energy-constrained BS-divergence converse has both a finite-n
form and an asymptotic exponent application. It is not a multiclass C/E/F
frontier. Its reference-assisted input class is different; the stated diagonal
optimum is a marginal, not the whole probe. Its exhibited coherent comparison
includes heterodyne readout. The rigorous truncation statement is for dephasing,
not every loss-dephasing or passive optical map.

The earlier abstract-only gap is resolved for these relevant statements. This
is a theorem-contract comparison, not a correctness audit of the external paper
or reproduction of its ancillary Python/MATLAB files. A publisher search returned
an accepted-paper record, DOI 10.1103/fypm-kjt6; direct opening failed, so no
publisher-version identity or final published content is claimed.

## S20. Zhang, Feng, Sun, and Ying

*Upper bound for the success probability of unambiguous discrimination among
quantum states*, PRA 64, 062103 (2001),
[official record](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.64.062103).
Published 8 November 2001; DOI 10.1103/PhysRevA.64.062103.

**Recovered and inspected:** the original three-page article's embedded text
from the [Yuan Feng author upload](https://www.researchgate.net/publication/243451242_Upper_bound_for_the_success_probability_of_unambiguous_discrimination_among_quantum_states).
The host identifies the upload as author content dated 18 March 2014. Original
article title, authors, DOI, page markers 062103-1 through -3, Definition 1,
Theorem 1 and its proof, sequential-measurement discussion and conclusion were
read. This is original article text, not a summary in a later citing paper.
Publisher metadata was independently checked.

The displayed Theorem 1 is unnumbered beyond its theorem label. It uses an
ordered i!=j sum, root prior weights and absolute unsquared overlaps. Its
uniform-prior specialization is exactly the zero-error endpoint in REDUCTIONS.
Theorem 1 is an upper bound; blanket attainment for arbitrary priors is not
inferred from its introductory comparison with the two-state IDP limit.

**Access limitation:** direct APS/DOI/harvest PDF retrieval and standalone
ResearchGate PDF links failed. Embedded full text was available. Consequently
the old original-text gap is resolved, but no publisher PDF download, visual
PDF check or bytewise archival comparison is claimed.

## S22. Bagan, Calsamiglia, Bergou, and Hillery

*Duality games and operational duality relations*,
[arXiv:1708.03968v1](https://arxiv.org/abs/1708.03968), submitted 13 August 2017;
PRL 120, 050402 (2018), DOI 10.1103/PhysRevLett.120.050402.
[Full PDF](https://arxiv.org/pdf/1708.03968), eight pages including supplement.

**Inspected:** main definitions (3)-(5), Lemma 1 / Eq. (9) on PDF page 3;
supplement Eqs. (18)-(41) on pages 5-7, including weighted Gram matrix (22),
coherence normalization (24), inequality (37), equality example (38)-(41),
and extension to linearly dependent ensembles. The result permits arbitrary
priors through the parent state, not only an equal-prior ensemble.

**Consequence:** exact no-failure multiclass root-overlap inequality. The useful
arbitrary-failure upper-C consequence follows by the S08 filter transformation
and the explicit reduction in this packet. This is the decisive new predecessor,
not merely a paper with similar terminology. PDF text was inspected; screenshot
attempts failed, and no figure/plot interpretation is claimed.

## S08. Bagan, Munoz-Tapia, Olivares-Renteria, and Bergou (reread)

*Optimal discrimination of quantum states with a fixed rate of inconclusive
outcomes*, [arXiv:1206.4145](https://arxiv.org/pdf/1206.4145);
PRA 86, 040303(R) (2012).

**Inspected again:** Eqs. (6)-(8), page 2, transformed POVM, normalized states and
reweighted priors; extension beyond the initial binary notation on page 3 and
concluding general-method statement. Eq. (10) supplies the binary high-bias USD
example showing why a general upper bound need not be attained. The singular
filter requires restriction to support or a limit; it is not handled by an
unjustified full inverse.

## S23. Earlier duality lineage, not the exact stronger match

Bagan, Bergou, Cottrell, and Hillery, *Relations between coherence and path
information*, [arXiv:1509.04592v2](https://arxiv.org/pdf/1509.04592), dated
10 December 2015; PRL 116, 160406 (2016).

**Inspected:** Eqs. (3)-(15): weighted l1-coherence, discrimination and the earlier
quadratic duality relation. This documents the lineage. The exact constants
used in our reduction come from S22, not from substituting into this weaker
quadratic relation. No experiment or figure was used.

## Additional scoped discovery leads

**S24. Xin Lu**, *An upper bound on the success probability of minimum-error
discrimination*, Physics Letters A 452, 128461 (2022),
[primary publisher page](https://www.sciencedirect.com/science/article/pii/S0375960122005436),
DOI 10.1016/j.physleta.2022.128461. Publisher abstract, introduction and conclusion
were accessible; the exact Eq. (17) body was not recovered. ResearchGate explicitly
reported no full text. Its l1-coherence connection is relevant, but no theorem
exclusion or exact equation identity is claimed from this access level. The S22
reduction already establishes the inherited classification without relying on
S24's unavailable equation.

**S25. Feng, Zhang, Duan, and Ying**, *Lower bound on inconclusive probability of
unambiguous discrimination*, PRA 66, 062313 (2002),
[official abstract](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.66.062313).
Publisher abstract identifies a strengthened unambiguous-discrimination bound
relative to S20. Full text was not recovered in this bounded follow-up, so this
source is a discovery/scope record only, not evidence for a finite-error formula.
No existing S20 result is claimed to be the strongest bound in the literature.

## Coverage limits

No exact optical source-class statement was found verbatim in the inspected
texts. The explicit corollary reduction is nonetheless sufficient to reject a
claim that its generic multiclass statistics inequality is newly invented.
The task does not exhaust all citations, unindexed theses or unpublished work.
Uninspected leads are not silently classified as irrelevant. The named S18/S20
questions are answered at the access levels above; those answers do not confer
worldwide priority on Claim A or publication significance on the full project.
