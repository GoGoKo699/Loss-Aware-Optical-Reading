# Table layout and reader-text cleanup

This follow-up starts at main `55a90a3162326e924b460977d4c19714f39ae606`.
[START.json](START.json) records the actual tree, initial clean local checkout,
dedicated branch and authority. The work corrects presentation and keeps the
experimental reader route independent of editorial discussions.

## Reader changes

The commissioning page now has a short table of routes, prepared paths, labels
and expected bright outputs. Exact preparations, phase operations and decoders
are displayed directly beneath it. A matching defect in the SU4 hidden-operation
row is corrected the same way. The original three rows contained unescaped
vertical bars inside code spans; GFM treated these as cell separators and
discarded or misplaced parts of the mathematical text.

The philosophy opens directly with its substantive text. Its body is unchanged;
the approval preamble is removed. Related approval commentary and owner
attribution are removed from the claim ledger and physical-setting introduction.
Both SU4 and SU8 availability remain unequivocal. Editorial authorization stays
in preserved provenance, without a new marker in the reader-facing explanation.

## Preservation and validation

The [authorization ledger](../../provenance/changes/table-cleanup-04.json)
records exactly five old/new document pairs. All six previous ledgers are
unchanged and hash-pinned. Three legacy current-byte checks now follow the new
explicit hash link, with their reasons recorded. Scientific routines, canonical
proofs, numerical tolerances, acquisition protocols and previous evidence are
unchanged.

The documentation checker now checks table widths before GFM can silently fill
or truncate cells. It also catches unescaped table pipes inside code spans.
Two targeted regressions cover the reported defect, missing/excess cells,
escaped pipes and fenced examples. The display-count assertion now includes
seven commissioning displays and the SU4 formula moved out of its table.
These are existing target equations presented in a different place.

## Executed checks and visual review

- `python3 scripts/verify_import.py`: PASS; all 39 original archive members and
  the successive authorization layers verify.
- `python3 -m unittest discover -s tests`: PASS; 105 tests in 103.472 seconds.
- `python3 scripts/verify_handover.py`: PASS; reader links, math delimiters,
  references and table structure verify.
- [GFM_TABLES.json](GFM_TABLES.json): PASS; 24 reader documents, 28 tables,
  169 body rows, three reproduced defective rows and 13 rendered math displays.
  The [reproduction helper](verify_gfm_tables.cjs) uses Markdown-it 14.1.0 and
  MathJax 3.2.2 in a separate scratch runtime. It rejects an existing output
  directory and any output directory inside the repository.
- Full tracked diff and new validation files independently reviewed; exact
  old/new document hashes and all previous ledger hashes verified.
- `git diff --check`: PASS.

The commissioning and SU4 target sections were visually inspected as PNGs
rendered from offline PDFs. WeasyPrint 70.0 typeset the helper's self-contained
GFM/MathJax HTML with all external resource requests disabled; PyMuPDF rasterized
those PDFs. The table headings and cells remain aligned and complete, and all
13 equations are readable without overlap or clipping. The review used a
1100-pixel page width and the helper's simplified GitHub-like stylesheet.

Live GitHub visual rendering was **not** checked. Browser policy blocked local
file navigation, so the review used an offline document renderer, without
browser navigation. This checks the generated content and document layout;
it does not establish pixel-for-pixel equivalence to GitHub's current CSS.

The associated pull request records the actual branch and post-merge workflow
results and final commit read-back. Those are recorded only after execution;
a configured workflow is not counted as a successful run.
