# Final release and laboratory-handover sanity check

**Decision: ready for a reference release and initial experimental-laboratory
review after the bounded presentation repairs. Certified acquisition still
requires the laboratory inputs below.** No scientific, recipe or accounting
defect blocking that handover was found. This is a scoped technical review,
not independent peer review or a novelty clearance.

The live baseline was `ba00d9ce64333ad08ef3b61108aa6df959cc5fc7`, tree
`605719db8b64ec45d75454dbe4338d56140d8593`. [START.json](START.json) records
the real local checkout, initial clean status, dedicated audit branch and
history-preserving reconciliation of the newer photonic-computing relevance
section. The repository was already public and MIT licensed; no release or
tag existed. This task did not change visibility, create a release/tag, contact
the laboratory or acquire data.

## Findings fixed

Live GitHub displayed three equation errors in the main report. Related
Markdown transport problems affected linked historical proofs. The current
report now uses literal math fences, and three deterministic reading copies
make the supplied proofs readable without modifying their original bytes.
Navigation points to those copies. The report also now correctly states that
both SU4 and SU8 chips are available, while interfaces and calibration remain
unsupplied.

All 37 reformatted display equations produce byte-identical direct MathJax
output before and after the change. Independent scientific review found no
change to hypotheses, constants, bounds or acquisition requirements. The
[change record](../../provenance/changes/final-handover-01.json) gives the
four exact protected-document edits and three source-pinned additions. All
eight earlier change ledgers and the supplied study/repair evidence remain
unchanged. Six markup/hash-chain test adaptations are explicitly recorded;
no scientific tolerance was relaxed.

The implementation is commit `f8a7b72fe9d0e4dcc7447e60569bf762d5c6208f`,
tree `874a9b8a8ba8f7c0ff3ef352d6f5769087fc6608`. This audit-evidence follow-up
adds results only. Actual final-head and post-merge workflow results are linked
in [PR 12](https://github.com/GoGoKo699/Loss-Aware-Optical-Reading/pull/12);
the report itself does not pre-claim their success or a merge.

## Verification executed

| Check | Observed result |
|---|---|
| Final full unit suite | 116 tests pass |
| Inherited reproduction | 5,261 checks and reference comparison pass, tolerance unchanged at 1e-8 |
| Independent historical and repaired audit | 998 historical checks and 993 repaired scientific checks pass |
| Supplied robustness local suite and regeneration | 8 tests; 41 cases and 381 diagnostics pass; regenerated results byte-identical to supplied results |
| Optimizer-free certificate verification | 11,161 checks and 10,828 exact positive-matrix checks pass; separate optimizer trap records zero calls |
| Laboratory references and record adapters | 48 successful CLI calls, seven expected refusals, 193 independent checks pass |
| Six compact teaching examples | Reproduced; only Python-version metadata differs from the older example environment |
| Integrity and navigation | Protected bytes/chain pass; 28 current pages, 307 local links, 33 script references and 31 tables pass |
| Presentation | Local parser/transport checks pass on current routes; targeted live GitHub screenshots confirm repaired report and proof equations |

The recorded scientific environment was Python 3.13.5, NumPy 2.3.5, SciPy
1.17.0 and mpmath 1.3.0. Every numerical output directory was fresh. The
[core manifest](CORE_CHECKS.json) inventories the commands, environment and
SHA-256 hashes of all 40 raw output/log files in
[CORE_EXECUTION.tar.xz](CORE_EXECUTION.tar.xz). The archive retains the initial
115-test run with its one obsolete-markup assertion failure as well as the
successful 116-test retry. The corrected test still compares all 11 original
report formulas and detects coefficient, sign and relation changes.

Separate records provide the [science review](SCIENCE_REVIEW.md),
[recipe review](RECIPE_REVIEW.md), [document review](DOCUMENT_REVIEW.md), and
[live rendering observations](LIVE_RENDERING.json). The bounded sensitive-data
scan found no credential patterns in current tracked files or readable archive
members; it is not a scan of all Git history or a guarantee of absence.

The exact certificates concern specified finite models, not physical calibration.
The entire classical/statistical pipeline is not interval certified. Synthetic
records remain labelled and do not become experimental evidence. Native Walsh8
has no transferred four-mode classical frontier or robustness/advantage claim.

## What the laboratory can use

Start with [SU4](../../experiment/SU4.md) or [SU8](../../experiment/SU8.md),
then [classical-light commissioning](../../experiment/COMMISSIONING.md).
The [experiment index](../../experiment/INDEX.md) separates commissioning,
[M1](../../experiment/M1.md), [P1](../../experiment/P1.md),
[P2](../../experiment/P2.md) and native Walsh8. The
[theory route](../../docs/THEORY_ROUTE.md) and
[robustness guide](../../docs/ROBUSTNESS_GUIDE.md) supply local explanations.
The original robustness delivery is integrated and preserved; its fresh
regeneration and independent witness verification passed this review.

Use the [interface guide](../../experiment/INTERFACES.md) and
[uncertainty worksheet](../../experiment/UNCERTAINTY.md) to supply:

- Physical port order, compiler phase convention, accessible controls and
  independent preparation/hidden-phase-and-loss/receiver roles; inter-chip
  connections if that arrangement is chosen.
- Wavelength/polarization, source statistics and independently justified mean
  signal/tail bounds at P0, compatible readout and all detector-mask records.
- Trial clock or pre-exposure herald, gate timing, dark/multiple-click/leakage
  handling and source/receiver/detector loss accounting at the declared planes.
- Common-phase map calibration, simultaneous uncertainty and drift bounds;
  independent pilot data and a frozen fixed-N, blinded hidden-label plan.
- For P2, an implemented stable displacement receiver and its calibration.

Physical commissioning needs compatible illumination/readout and control
interfaces. The reference software already runs. The descriptive record adapter
checks that timestamps are present, but actual timestamp validity belongs to the
laboratory adapter; it must not be mistaken for a timing-certification service.
