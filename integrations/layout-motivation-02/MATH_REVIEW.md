# Mathematical layout review

The reported displays were valid TeX before the change, but the screenshots
showed failures in the reader's GitHub display. The correction uses GitHub's
documented fenced `math` blocks, so escaped braces, underscores, comparison
signs, and matrix row separators reach the mathematics renderer literally.
All 42 displays across eight current reader pages use this convention. This
does not change the theorem, benchmark, recipes, or numerical examples.

The official reference is [GitHub: writing mathematical expressions](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions),
inspected on 2026-09-15. GitHub documents MathJax rendering and the fenced
`math` alternative. The local check used MathJax 3.2.2; GitHub's current
deployed version was not identified and is not assumed identical.

## Checks actually executed

- Compared all eight complete documents against commit
  `1b0a79073050766f12317f27a0b0e9260896b90f`. The only allowed changes were
  display wrappers and explicit braces around single-digit TeX operands.
  Each of the 42 mathematical payloads was checked separately as well.
- Parsed Markdown with markdown-it 14.1.0 in CommonMark mode. Every corrected
  display was extracted from a literal `math` fence, preserving its TeX.
- Parsed and rendered all 42 original TeX payloads and all 42 corrected
  payloads to SVG with MathJax 3.2.2. No MathJax error nodes occurred.
- Ran a controlled Markdown-before-TeX reconstruction of the four screenshot
  formulas. It reproduced the two minimum-bound delimiter errors, altered
  the theory page's norm expression, and did not reproduce the contribution
  page's matrix-definition error. This supports the escaping diagnosis but
  does not identify every step of GitHub's actual rendering pipeline.
- Ran seven documentation tests, including malformed fenced-math detection,
  literal versions of the reported formulas, preserved display counts,
  local links, and script references. The checker now inspects mathematics
  inside `math` fences; it does not silently treat it as ordinary code.
- Confirmed that rerunning the renderer on an existing output directory
  fails and leaves all 43 output files unchanged.

The machine-readable result is [MATH_RENDER.json](MATH_RENDER.json), including
per-display SVG hashes. The [verification script](verify_math_render.cjs)
records its isolated dependency installation and execution commands. It
requires a fresh output directory outside the repository. Its dependencies
are QA tools in scratch and were not added to the scientific runtime.

These automated checks are distinct from visual inspection. The JSON
explicitly records that this script did not inspect a live GitHub preview or
perform a human-style visual check. Any separate visual inspection belongs
in the enclosing integration report.
