# Source follow-up 02

Read [REPORT.md](REPORT.md) for the disposition and [REDUCTIONS.md](REDUCTIONS.md)
for the exact dependency chain. [SOURCES.md](SOURCES.md) distinguishes recovered
full texts from partial discovery leads. The work is confined to this audit;
canonical claims and the experimental protocol are not updated here.

The named S18 and S20 comparisons are resolved. The key additional result is a
predecessor reduction: Bagan et al.'s 2017/2018 duality lemma plus the established
conclusive-filter transformation gives the generic upper-C inequality used by
Claim B. Standard optical overlap and concavity arguments then give the source-
class certificate. It remains useful, but should be presented as an optical
corollary rather than an independently new general discrimination theorem.

Claim A, the joint input-only retuning reduction under the declared model, remains
the leading candidate technical contribution. This is not priority clearance.

## Focused reproduction

```bash
python audits/novelty-02/comparison_checks.py --output results/runs/novelty-02
```

NumPy is the only nonstandard dependency; the recorded run used version 2.3.5.
Use a new output directory. The script imports neither canonical code nor any
article's implementation, writes no source files and does not require a network.
It checks explicit finite matrices and normalization identities, not absence of
prior art or correctness of all external papers.

572 checks passed in six groups. A second new-directory run reproduced RESULTS.json
byte for byte. The full result ledger, environment and second-run hash comparison
are in EVIDENCE.tar.xz; SUMMARY.json and MANIFEST.json identify the evidence.
The normal repository CI remains unchanged and does not invoke this new script.

Original third-party PDFs and article text are not redistributed. The source
inventory provides primary access links and exact locators. No experiment,
calibration, manuscript, release, license or merge is included.
