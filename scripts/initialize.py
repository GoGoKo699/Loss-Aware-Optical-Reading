"""Restore the source and reader-facing entry points; no archive-hash fallback."""
import urllib.error
import bootstrap_import as boot

# Reader-facing prose is new migration material, not protected scientific source.
# If an unreferenced prose blob has expired, these complete entry points are used.
# Source archive parts always use exact Git and SHA-256 verification and fail closed.
FALLBACK={
'66ef8c7f95e6ba361adebfc0a696b4bd5fdd0f22':'''__pycache__/
*.py[cod]
.venv/
.pytest_cache/
results/runs/
.env
.env.*
.DS_Store
''',
'429d45959b7c962cfa58a15f21ee46bccfb44ae6':'''# Loss-Aware Optical Reading

A single photon interrogates four paths. Exactly one path receives a phase flip.
A fixed interferometer reads the label. The scientific question is when loss and
required reliability make this preferable to the strongest allowed classical
illumination, and when they reverse that comparison.

**Stage:** theory, numerical validation, and a proposal for initial laboratory
review. No laboratory data, established hardware calibration, or publication-level
novelty clearance is claimed. This is a private working repository.

## Start here

| Route | Material |
|---|---|
| **LEARN** | [Scientific report](REPORT.md) and [physical setting](docs/PHYSICAL_SETTING.md) |
| **CHECK** | [Claim status](CLAIM_STATUS.md), [proofs](proofs/THEORY.md), and [source audit](SOURCE_AUDIT.md) |
| **REPRODUCE** | [Safe reproduction](docs/REPRODUCE.md) and [migration record](provenance/MIGRATION.md) |
| **LAB REVIEW** | [Short brief](experiment/LAB_REVIEW.md) and [first experiment](experiment/FIRST_EXPERIMENT.md) |
| **DEVELOP** | [Next work order](work_orders/CURRENT.md), [roadmap](docs/ROADMAP.md), and [rules](AGENTS.md) |

## Physical and evidential boundary

One photon in four paths is one four-dimensional carrier, not separately carried
qubits. The task promises exactly one flip, with a uniform hidden label and no
healthy fifth case. The photon optimum excludes occupied bypass rails, retained
idlers, and repeated interrogation of one setting. Classical probes include
coherent-state mixtures, phase references, arbitrary receivers, and rare bright
pulses under a mean incident signal-energy constraint.

The exact photon preparation/frontier assumes known diagonal loss. The calibrated
map classical certificate is a bound, not an exact optimum for every device.
See the full theorem conditions before interpreting a numerical comparison.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-recorded.txt
python scripts/verify_import.py
python -m unittest discover -s tests -v
python scripts/reproduce.py
```

Use Python 3.13.5 for the recorded environment. New runs use unique directories
under `results/runs/` and never replace the original `results/`. The wrapper
records environment, source hashes, and numeric comparisons. The inherited
5,261 checks are a regression inventory, not an independent scientific audit.

## Evidence classes

`results/quantum_frontier.csv` and related tables evaluate ideal models.
`results/validation.json` records numerical diagnostics. `hypothetical_*` files
are forecasts; `synthetic_*` files are simulated certification examples.
`templates/trials.csv` contains no acquired observations. Source/calibration
assumptions must be justified before using the trial analyzer on real data.

The original checkpoint archive and all 39 members are accounted for in the
migration manifest. Checkpoint 06 remains optional baseline evidence. Earlier
multiphoton and chirality branches are not prerequisites for this project.

The next task is an independent proof/certificate audit, followed separately by
novelty review and laboratory-interface feedback. No new scientific study was
executed as part of the migration. No license or public release has been selected.
Contact: gogoko699@gmail.com.
''',
'f6f3b21b6d38a7abff41315618c974e2bec3bd2e':'''# Workspace rules

Read README.md, CLAIM_STATUS.md, SOURCE_AUDIT.md, docs/PHYSICAL_SETTING.md, and
work_orders/CURRENT.md. Record the starting commit and working-tree status.
Use a new branch for one bounded task. Never reset another workspace or rewrite
history. Public release, licensing, and experimental acquisition require explicit
authorization.

Protect the original archive, baseline/, and frozen results/. Use the safe
reproduction wrapper. Any authorized later scientific edit needs a visible
versioned integrity-policy change; never silently refresh hashes. The original
archive identity must remain unchanged.

Keep exact bounds, attained optima, diagnostics, hypothetical forecasts, and real
data distinct. Preserve input/output planes, phase references, priors, and full
trial counting. No multiphoton computing, idlers, occupied bypass rails, quantum
memory, or repeated hidden-setting access is an implicit resource.

At completion state the actual tests, limitations, files, and commit. Do not
claim CI success from its configuration alone. Stop at the authorized boundary.
''',
'991929ee60e7ca2cb0bf770d65cdd70c7aee9bba':'''# Contributing

Use one branch for one bounded work order. Read AGENTS.md. Run integrity checks,
engineering tests, and safe reproduction. Mathematical changes need independent
arguments and targeted checks, not only legacy regressions. Do not silently repair
science during an editorial pass. Preserve previous evidence and all limitations.

New local runs belong in results/runs/. Raw laboratory acquisition and publication
need separate review. Never commit credentials or device-control secrets.
No redistribution license has been selected. Contact: gogoko699@gmail.com.
''',
'23b51ffcd0f650db31f7041a5edead33a902c425':'''# Physical setting

SU(4)/SU(8)-first, global path encoding, one computational photon at a time.
Larger existing mode processors are eligible; synchronized computational photons,
interacting auxiliaries, memory, and recirculation are not assumed.

Four equal-prior labels identify exactly one pi flip. Preparation, the unknown
operation, and the fixed decoder must be physically separable. The reader cannot
receive the label as a compiler input. A common phase reference is required for
the classical comparison; per-label global phases cannot be discarded freely.

Known hypothesis-independent diagonal loss is the ideal photon theorem's model.
General mesh/detector errors require the separate calibrated-map certificate.
Signal energy is charged immediately before the unknown section. Our downstream
loss reduces our score, not the ideal competitor's ceiling. All attempted trials
count, including no clicks and multiple clicks. Each trial receives a fresh
independent uniform hidden label. A source herald can precede interrogation;
output postselection cannot define the denominator.

No healthy fifth case, occupied bypass, retained idler, or repeated use of one
hidden setting is covered. Hypothetical values are not laboratory calibration.
The initial deliverable is theory, validation, and laboratory-review material.
The task may be direct optical reading: a reusable coherent loss gate or learning
architecture is no longer required. The quantum benefit and novelty still need
appropriate scientific justification.
''',
'2ad038519f79af7d58e9886f8c34386fe07a1a92':'''# Safe reproduction

Use Python 3.13.5 and install requirements-recorded.txt. Lower-bound dependencies
remain in requirements.txt; neither is a complete OS/container lock.

```bash
python scripts/verify_import.py
python -m unittest discover -s tests -v
python scripts/reproduce.py --output results/runs/my-first-run
```

The directory must be new. The wrapper fixes one BLAS/OMP thread, checks protected
hashes before and after execution, records the log and environment, and compares
new outputs to the frozen checkpoint. Without an output argument it chooses a
unique run directory. Direct src/validate.py now requires --output-dir; only this
I/O perimeter changed. Its mathematical body remains byte-identical.

All 5,261 ordered check names and tolerances must match. Every residual must be
finite and pass its declared bound. Twelve generated CSV/JSON files are compared
at absolute tolerance 1e-8 with identical schemas and text. Runtime, platform,
and summary residual variation remain visible in REPRODUCTION.json. A PASS is
regression reproduction, not a new proof audit or novelty clearance.

Original outputs remain in results/. New runs go under ignored results/runs/.
The complete original ZIP is in provenance/archives/; all 39 source members are
mapped in provenance/IMPORT_MANIFEST.json. The original README and SHA list are
under provenance/checkpoint07/. Their old commands are archival, not current.
The initial fresh repository run is under provenance/migration07/.

The trial analyzer does not verify whether a plan was truly preregistered or the
source calibrated. Templates are synthetic. Real use needs justified energy and
simultaneous calibration bounds, every attempted trial, and a new output file.
Never overwrite archived evidence or label a forecast as measured data.
''',
'4ab2035f6c77bce0c25ac9cfe0d4bfb86cdb40ae':'''# Roadmap

The goal is a predictive, experimentally certifiable reliability–illumination
comparison with a simple single-photon reader, not a new algorithmic name.

First independently audit the existing proofs and certificates. Next compare
candidate theorems with direct predecessors and obtain laboratory feedback on
source statistics, hidden-operation separation, common-phase calibration,
click records, and coherent displacement. Pilot calibration must precede a
frozen held-out experiment.

A second phase code may test transfer later. Arbitrary unequal-loss classical
finite-error exact optimality and adaptive total-illumination advantages remain
open tasks requiring new work. More modes do not by themselves establish scaling.
No novelty clearance, external proof review, measured advantage, experiment date,
or journal acceptance is claimed.
''',
'f434e5ba9f23868554a8709e5b6648f8a7452e4d':'''# Next task: independent proof and certificate audit

Status: READY, NOT EXECUTED by migration.

Record main's commit and working-tree status. Read AGENTS.md. Create audit/theory-01
from that baseline. If it exists, inspect and continue without restarting.

Read proofs/THEORY.md, CLAIM_STATUS.md, SOURCE_AUDIT.md, src/theory.py,
src/analyze_trials.py, and experiment/FIRST_EXPERIMENT.md. Audit the exact photon
frontier, uniform classical attainability, all-energy mixture extension,
calibrated-map certificate, reverse bound, and fixed-N statistical assumptions.
Do not weaken the competitor's access model to obtain a result.

Write only under audits/theory-01/ on the audit branch: claim-level findings,
independent derivations or counterexamples, targeted diagnostics, and limitations.
Run safe reproduction, but do not equate legacy PASS with a proof review.
Do not change canonical proofs, protocols, archives, or reference outputs. Repairs
require a separate task. No manuscript, experiment, or research extension is part
of this audit.

Commit findings and report the branch, commit, checks, and remaining gaps.
Stop. Do not merge, publish, or proceed to novelty review without authorization.
''',
'091aa5dec4237f22b29a378f0c566d92eeaf03d1':'''# Bounded work orders

CURRENT.md specifies the next task, not permission to execute the whole roadmap.
Record the baseline, permitted changes, output, and stopping condition. Read
AGENTS.md. The verified import is in provenance/MIGRATION.md. The scientific
proof audit, novelty comparison, and lab-interface review are separate tasks.
'''}

original=boot.fetch_blob

def fetch(sha):
    try:
        return original(sha)
    except urllib.error.HTTPError as error:
        if sha not in FALLBACK or error.code!=404:
            raise
        return FALLBACK[sha].encode()

if __name__=='__main__':
    boot.fetch_blob=fetch
    boot.main()
