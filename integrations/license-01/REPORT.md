# MIT license integration

[START.json](START.json) records the actual main commit, tree and initially clean
local checkout. This bounded change adds the [MIT License](../../LICENSE), with
Copyright (c) 2026 Ruge Lin, for original project material.

The current README and contribution guide link to the license and
[third-party notices](../../THIRD_PARTY_NOTICES.md). Historical records retain
their original descriptions of the repository at the time they were written.
No visibility change, release, acquisition or scientific extension is part of
this task.

## Scope and attribution

The MIT text was checked against the standard
[GitHub template](https://choosealicense.com/licenses/mit/) and
[SPDX license text](https://spdx.org/licenses/MIT.html). Its terms are unchanged;
only the copyright year and holder are populated.

A separate inventory inspected tracked files, 14 archive containers (3 ZIP and
11 tar.xz), nested archive members and transported project-repair JSON chunks.
No redistributed external article, book or separately licensed software source
was found in those project archives. Dependencies remain separately installed.

Seven saved equation SVGs contain MathJax 3.2.2 font outlines. Independent
comparison matched all 239 embedded paths (53 distinct paths) to the package's
TeX SVG font data. The notice attributes that embedded glyph data, not the
project's equations or scientific claims, to the MathJax Consortium.
The [upstream Apache 2.0 license](https://github.com/mathjax/MathJax-src/blob/3.2.2/LICENSE)
is copied verbatim to [MathJax-Apache-2.0.txt](../../licenses/MathJax-Apache-2.0.txt).
The installed package and upstream tag copies match SHA-256
`cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
No upstream NOTICE file was present in the inspected package or tag root.

## Preservation and verification

The [authorization record](../../provenance/changes/license-01.json) records the
sole protected-document edit: the README licensing notice. All seven earlier
ledgers remain unchanged and hash-pinned. Three legacy current-byte assertions
now follow this additional old/new hash link. Two focused integrity regressions
check the preimage, current bytes and refusal to widen the authorized scope.
Canonical science, experiment protocols, numerical tolerances, frozen results,
archives and the saved equation images are unchanged.

Local import integrity and the handover document validator pass. The README,
contribution guide and third-party notice also pass a separate local-link check
(38 links across those three documents). The Apache license matches the upstream
bytes. The complete diff is independently reviewed before integration.

The focused local runs passed all 37 integration tests and 13 handover-integrity
tests. The complete diff and seven predecessor ledger hashes were independently
reviewed. Whitespace checks pass.

Actual workflow results, final commit and main read-back are recorded in the
associated pull request after execution. Workflow configuration
alone is not counted as a successful check. Repository visibility is checked
separately; adding a license does not change it.
