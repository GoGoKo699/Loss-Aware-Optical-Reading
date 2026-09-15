# Follow-up mathematical display review

The owner supplied a new screenshot after the previous correction: the
minimum-bound display rendered, but the definition of H_Delta still reported
a missing brace. The source was valid TeX inside a literal math fence. The
remaining vulnerable token was the raw less-than sign in the pair-sum subscript.

## Diagnosis and exact correction

[MathJax's HTML guidance](https://docs.mathjax.org/en/latest/input/tex/html.html)
explains that a browser can interpret a less-than sign followed by a letter as
the beginning of an HTML tag before TeX processing. It recommends the relation
macro `\lt`. The [KaTeX supported-functions table](https://katex.org/docs/supported.html)
also lists that macro. Both primary sources were inspected on 2026-09-15.

The only mathematical source edits are:

| Current reader page | Before | After |
| --- | --- | --- |
| `docs/CONTRIBUTIONS.md` | `j<k` in one sum | `j\lt k` |
| `docs/THEORY_ROUTE.md` | `j<k` in one sum | `j\lt k` |
| `docs/THEORY_ROUTE.md` | `0<\eta_i\leq1` | `0\lt\eta_i\leq1` |

All other bytes of these two documents match baseline
`01d715a80dbe48c3c20f43337fb524753e3cdb54`. The fences, assumptions,
normalization, benchmark, and numerical meanings are unchanged. The loss
condition is normalized defensively; it did not fail in the controlled parser.

## Checks actually executed

The [reproducible checker](verify_math_transport.cjs) uses isolated versions
of markdown-it 14.1.0, MathJax 3.2.2, KaTeX 0.16.22, and parse5 7.2.1. The
[machine-readable result](MATH_TRANSPORT.json) records the actual versions,
all 18 displays, the three changed payloads, and hashes of generated SVGs.

- Compared both complete documents against the baseline with only the three
  exact substitutions allowed. Parsed all 18 math fences as literal payloads.
- Rendered all 18 old and all 18 corrected expressions in both mathematics
  engines. Old and new MathJax SVGs are byte-identical; old and new KaTeX HTML
  outputs are byte-identical. No direct TeX parser errors occurred.
- Passed each changed payload through a controlled HTML5 parsing step before
  TeX. For both old pair sums, parse5 discarded the suffix beginning at the
  less-than sign, leaving the unfinished subscript `\sum_{j`. Both mathematics
  engines then rejected the result. Every corrected payload survived the HTML
  step byte-for-byte and parsed successfully in both engines.
- The coordinating reviewer independently reproduced the same two old
  truncations and corrected preservation using Python's `HTMLParser`.
- Ran `python3 -m unittest discover -s tests -p test_handover_documents.py`:
  all eight tests passed. The static checker now rejects raw less-than and
  greater-than characters inside display mathematics and accepts their TeX
  relation macros. Its new regression covers both math fences and dollar
  displays. The existing reported-formula fixture now uses the corrected
  macro; its literal-payload and escaped-brace checks remain in place.
- Ran `python3 scripts/verify_handover.py`: 24 documents, 276 local links,
  and 33 Python script references passed.
- A repeated renderer invocation using the existing output directory was
  refused, leaving all 19 generated files unchanged. No previous integration
  report, renderer, source archive, certificate, or frozen result was edited.

The three changed displays are preserved as SVGs for inspection:
[contribution matrix](docs-CONTRIBUTIONS-3.svg),
[theory matrix and norm](docs-THEORY_ROUTE-12.svg), and
[phase operation and loss condition](docs-THEORY_ROUTE-2.svg).

## Scope and limits

This is a controlled reproduction of an HTML-before-TeX failure mechanism,
supported by the screenshot and documented parser behavior. It does not
identify the owner's exact renderer or verify an authenticated live GitHub
page. The earlier direct-TeX checks passed because that step received intact
TeX. This follow-up adds the missing HTML-transport check and preserves the
earlier evidence unchanged. Automated SVG generation is distinct from visual
inspection; any separate visual review is recorded in the integration report.
