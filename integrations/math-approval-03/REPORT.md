# Remaining equation layout and philosophy approval

The owner reported that the pair-sum matrix definition still failed after the
previous layout correction, and explicitly approved the philosophy text.
The actual starting commit, tree and clean local state are in [START.json](START.json).
This branch starts at main `01d715a80dbe48c3c20f43337fb524753e3cdb54`.

## What changed

The pair-sum subscript in [contributions](../../docs/CONTRIBUTIONS.md) and the
[theory route](../../docs/THEORY_ROUTE.md) now spells the less-than relation as
the TeX command `\lt`. The theory route's positive-transmission condition uses
the same spelling. These are the only three changes in those two documents.
The existing math fences and all mathematical content are unchanged.

The earlier local checks validated the TeX itself and Markdown fence extraction.
They did not cover a subsequent raw HTML interpretation. The new controlled
HTML5 test reproduces the reported symptom: the old `j<k` becomes an unfinished
tag, leaving the sum's subscript without its closing brace and dropping the
rest of the equation. The replacement survives that step without losing text.
This explains a concrete failure mechanism; it does not claim inspection of
the user's exact renderer implementation or an authenticated GitHub preview.

[PHILOSOPHY_DRAFT.md](../../docs/PHILOSOPHY_DRAFT.md) now records owner approval
on 2026-09-15. Its body is byte-for-byte unchanged after the opening status
paragraph. README and the claim ledger no longer request that approval.
The existing filename remains to preserve links. Approval of this text does
not change the scientific claim ledger or authorize experimental acquisition.

## Verification

The [math review](MATH_REVIEW.md), [transport results](MATH_TRANSPORT.json) and
[reproducible checker](verify_math_transport.cjs) record these completed checks:

- All 18 displays in the two changed math documents have identical old/new
  MathJax SVG and KaTeX HTML output. Whole-document comparison permits only
  the three exact relation substitutions.
- Both old pair-sum expressions fail after controlled HTML5 parsing; both
  corrected expressions preserve every character and parse in both renderers.
  An independent Python HTMLParser check reproduced the same two failures and
  successful corrections. The transmission condition is normalized defensively;
  its old version did not fail these HTML tests.
- The three affected displays were rasterized with CairoSVG 2.8.2 and visually
  inspected: complete, legible equations, with no missing braces or cropped
  terms. Their SVGs are preserved alongside this report.
- The renderer refuses an existing output directory and preserves its files.
- The document checker now rejects raw HTML-sensitive comparison characters
  in display math. A regression covers both math fences and dollar delimiters.
- The navigation check passed for 24 reader documents, 276 local links and
  33 Python script references. Import and protected-hash verification passed.

The new [old/new record](../../provenance/changes/math-approval-03.json) permits
exactly five reader-document edits. All five previous ledgers are preserved and
hash-pinned. Two existing integrity assertions follow the explicit additional
old-to-new link; their reasons are recorded. The earlier layout fixture now
uses the safe relation spelling, while the new regression rejects the original
failing spelling. No numerical tolerance or scientific assertion is weakened.

The full local suite passed: `python3 -m unittest discover -s tests` ran
100 tests successfully on Python 3.12.14. Remote workflow results are recorded
in the associated pull request after execution. No prior archive, proof, protocol, source routine,
study result or integration record was rewritten. The repository stays private.
