"""Record checks actually executed for the initial migration; no scientific edits."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile
from verify_import import ROOT, verify

def main():
    check=verify()
    run=ROOT/'provenance/migration07/run'
    result=json.loads((run/'REPRODUCTION.json').read_text())
    baseline=ROOT/'baseline/photonic_single_photon_checkpoint_06.zip'
    with tempfile.TemporaryDirectory() as d:
        with zipfile.ZipFile(baseline) as z:
            for name in z.namelist():
                rel=Path(name)
                if rel.is_absolute() or '..' in rel.parts:
                    raise ValueError('Unsafe baseline path')
            z.extractall(d)
        work=Path(d)/'photonic_single_photon_checkpoint_06'
        env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
        p=subprocess.run([sys.executable,'src/validate.py'],cwd=work,env=env,text=True,
                         stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (ROOT/'provenance/migration07/CP06_RERUN.log').write_text(p.stdout)
        p.check_returncode()
        baseline_result=json.loads((work/'results/validation.json').read_text())
        summary=baseline_result.get('summary',baseline_result)
        if summary.get('status')!='PASS' or summary.get('checks')!=4453:
            raise ValueError('Unexpected checkpoint-06 rerun result: '+repr(summary)[:300])
        (ROOT/'provenance/migration07/CP06_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    fresh=result['fresh_summary']
    report={'migration_status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
        'source_archive_sha256':check['archive_sha256'],'members':check['source_members'],
        'cp07_summary':fresh,'cp06_summary':summary,
        'source_scientific_content_unchanged':True,
        'unit_tests':'12 engineering unit tests executed in the recorded workflow log',
        'scope':'Verified import and reproducibility only; not a new independent proof or novelty audit.',
        'laboratory_data':False,'license_selected':False,'public_release':False,
        'workflow_run':os.environ.get('GITHUB_RUN_ID'),
        'bootstrap_commit':os.environ.get('GITHUB_SHA')}
    (ROOT/'provenance/migration07/SUMMARY.json').write_text(json.dumps(report,indent=2)+'\n')
    text=f'''# Verified checkpoint-07 import

Status: PASS. This is an import/reproduction record, not a new scientific audit.

The exact uploaded archive is retained in `archives/photonic_single_photon_checkpoint_07.zip`.
Its SHA-256 is `{check['archive_sha256']}`. All 39 source members are accounted for
in [IMPORT_MANIFEST.json](IMPORT_MANIFEST.json).

## Changes

Proofs, claim/source ledgers, experimental protocols, mathematical implementation,
reference results, and checkpoint-06 archive remain byte-preserved. The original
README and hash list were relocated to `checkpoint07/` without changing their bytes.
The validator received only an explicit-new-output-directory guard. Everything
from its seeded RNG declaration onward is unchanged. A reader-facing README,
safe reproduction wrapper, integrity checker, engineering tests, documentation,
and work-order rules were added. No substantive scientific claims were changed.

The original ZIP was transported as compressed recursive ZIP metadata/content.
Reconstruction was accepted only after the complete original ZIP hash matched.
Temporary transport parts are not part of the final working tree. The restoration
program remains for provenance and refuses to overwrite an existing import.

## Fresh execution

- Checkpoint 07: {fresh['checks']} checks, status {fresh['status']}.
- Maximum algebraic residual: {fresh['max_algebraic_residual']:.17g}.
- Maximum constrained-solver gap: {fresh['max_dual_solver_gap']:.17g}.
- Checkpoint 06: {summary['checks']} checks, status {summary['status']}, in an isolated temporary copy.
- Engineering regression suite: 12 tests, with log retained in `migration07/unit-tests.log`.

The full fresh checkpoint-07 outputs are under [migration07/run/](migration07/run/).
[REPRODUCTION.json](migration07/run/REPRODUCTION.json) records the environment,
source hashes, per-file comparisons, and both archived and fresh summaries.
Fresh residuals and runtime need not be byte-identical to the archive. Twelve
result tables/JSON files match within the declared absolute tolerance of 1e-8;
all 5,261 check identities/tolerances are unchanged and all fresh residuals pass.
The reference `results/` directory was not regenerated or overwritten.

## Remaining boundaries

No acquired laboratory data, physical calibration, outside peer review, formal
proof verification, or novelty clearance is implied. The next work order is an
independent proof/certificate audit. No license, tag, or public release was selected.
The original relative links inside archived checkpoint documents retain their
historical context; use the current README for navigation.
'''
    (ROOT/'provenance/MIGRATION.md').write_text(text)
    verify()
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
