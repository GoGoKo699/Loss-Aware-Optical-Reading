# Predecessor comparison: what is inherited and what remains to contribute

Target baseline: `80c73751806f45411251711bcfb6bccebc887f0a`.
Branch: `audit/novelty-01`. This is a completed bounded literature comparison,
not a new protocol, manuscript, universal priority certificate, or laboratory result.

Read [REPORT.md](REPORT.md) for the decision, [CLAIM_MAP.md](CLAIM_MAP.md) for
per-claim classifications, and [REDUCTIONS.md](REDUCTIONS.md) for explicit equation
translations. [SOURCES.md](SOURCES.md) records primary-source locators and actual
inspection scope; [SEARCH_LOG.json](SEARCH_LOG.json) records search families and
gaps without treating unsuccessful searches as evidence of novelty.

The fixed-alphabet uniform coherent curve is exactly a Herzog-2012 specialization.
The fixed code decoder is the established square-root measurement. The binary
contrast is the known coherent scattering-discrimination operator up to scale.
The two leading candidate technical claims are the *joint normalized input*
retuning reduction and the *multiclass all-classical-source* optical converse.
The report distinguishes them from their standard component arguments.

## Reproduce the focused comparisons

From the repository root at this branch:

```bash
python -m pip install -r requirements-recorded.txt
python audits/novelty-01/comparison_checks.py --source-root . --output results/runs/novelty-comparison
```

The output directory must not exist. The script accepts only source bytes with
the recorded baseline Git blob identities. It writes RESULTS.json and
ENVIRONMENT.json to a new directory and never changes protected source/results.
The local recorded run used an extracted selected-source repair package whose
three relevant files matched those remote identities, not an authenticated clone.

631 focused scalar checks passed. The results were reproduced byte for byte in a
second new directory. Check identities and tolerances are in `RESULTS.json` inside [EVIDENCE.tar.xz](EVIDENCE.tar.xz).
[SUMMARY.json](SUMMARY.json) lists the archive member hashes and the result summary.
This does not rerun all 5,261 canonical tests or establish absence of a predecessor.
The unchanged branch CI, when successful, covers the repository's existing
regression/repair suite, not this new script.

No complete third-party articles are included. Follow the primary-source links.
Only files in this audit directory are added. Main, canonical science, older
archives, audit/repair evidence, and the experiment remain unchanged.
