# Reader layout and motivation correction

The owner reported broken mathematical displays and a philosophy paragraph
that depended on an unseen private chat. This bounded follow-up repairs the
current reader route and explains what successful experiments could support.
The actual starting state and authorization are in [START.json](START.json).
Work began from main `1b0a79073050766f12317f27a0b0e9260896b90f` on
`handover/layout-motivation-02`, preserving the prior handover and its evidence.

## Reader changes

The [README](../../README.md#what-successful-experiments-could-establish) now
connects the planned measurements to a possible theory-and-experiment paper:
M1 tests preparation retuning with a fixed decoder; P1 certifies the declared
single-photon source-class advantage; P2 establishes the reverse ordering in
its separate four-path regime. Smaller outcomes, native Walsh8 limitations,
and the conditional nature of the publication objective are explicit.
The [philosophy draft](../../docs/PHILOSOPHY_DRAFT.md) gives this motivation
directly, retains owner-approval status, and needs no private-chat history.
An independent claim review checked the new prose against the existing
contribution and experiment boundaries. README is 1,374 words; the complete
philosophy document is 399 words.

All 42 mathematical displays in eight current reader pages now use GitHub's
documented literal `math` fences. Explicit braces around short TeX operands
improve readability of the source. Whole-document and per-equation comparisons
verified that the eight pages contain only these formatting changes. The
[math review](MATH_REVIEW.md), [machine-readable results](MATH_RENDER.json), and
[reproducible checker](verify_math_render.cjs) record the exact scope.

## Verification actually performed

- Python 3.12.14: `python3 -m unittest discover -s tests` passed all 95 tests
  in 103.178 seconds. This includes the existing scientific regression tests,
  seven documentation tests, and nine new bounded integration tests.
- `python3 scripts/verify_import.py` passed, including original archive and
  current protected-document checks.
- `python3 scripts/verify_handover.py` passed: 24 documents, 276 local links,
  and 33 Python script references.
- Local MathJax 3.2.2 parsed and rendered 42 old and 42 corrected expressions;
  all 42 corrected CommonMark fence payloads preserved their TeX. A second
  invocation targeting the existing render directory was refused without
  changing its outputs. See the math review for the precise reproduction
  of the escaping symptoms and its limits.
- The four reported expressions were rasterized from the generated SVGs using
  CairoSVG 2.8.2 and visually inspected: braces, summation limits, square roots,
  adjoints and norm bars were legible, with no error box or cropped symbol.
  Preserved SVGs: [theory matrix](docs-THEORY_ROUTE-12.svg),
  [theory ceiling](docs-THEORY_ROUTE-13.svg),
  [contribution ceiling](docs-CONTRIBUTIONS-2.svg), and
  [contribution matrix](docs-CONTRIBUTIONS-3.svg).
- The complete diff was reviewed; `git diff --check` passed. The 14 modified
  existing files are the ten authorized reader documents and four bounded
  validator/test files. All other existing files remain byte-for-byte intact.

The browser was not signed in to this private repository and returned a GitHub
404. Therefore this records local mathematical visual verification, not an
authenticated live GitHub page-render check. Remote branch/PR and post-merge
workflow results are recorded in the associated pull request after they occur;
workflow configuration alone is not counted as a successful run.

## Preservation

The [new authorization ledger](../../provenance/changes/layout-motivation-02.json)
records all ten old/new document hashes and pins the previous ledger unchanged.
The single existing integrity-test assertion now follows the explicit later
old-to-new link before checking current bytes. Its original scientific meaning
and all numerical tolerances are preserved. No theorem, registered protocol,
source archive, supplied robustness file, study code, frozen output or historical
ledger changed. No laboratory values, measured results, novelty clearance or
journal outcome are asserted by this correction.
