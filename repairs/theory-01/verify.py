"""Repeat historical defect witnesses and the unchanged independent science cases.

Run from the repository root:
  python repairs/theory-01/verify.py --output /new/directory

The old audit is never edited. Its fixed-hash/defect assertions run on an extracted
historical source. Its scientific functions are then called on the repaired
source. New unit tests separately check fixed defects and exact enclosures.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import zipfile

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'scripts')]
from verify_import import verify


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();out=args.output.resolve()
    frozen=(ROOT/'results').resolve();runs=frozen/'runs'
    if out.exists() or out==ROOT or out==frozen or out==runs or (frozen in out.parents and runs not in out.parents):
        parser.error('Use a new directory, never frozen results or an existing run')
    integrity=verify();out.mkdir(parents=True)
    start=time.perf_counter()
    diagnostic=ROOT/'audits/theory-01/diagnostics.py'
    raw=diagnostic.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if blob!='8a089ef95ad186490546fed181a94eabd2975c34':
        raise ValueError('The archived independent audit diagnostic changed')
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='reading-historical-audit-') as temporary:
        archive=ROOT/'provenance/archives/photonic_single_photon_checkpoint_07.zip'
        with zipfile.ZipFile(archive) as z:z.extractall(temporary)
        historical=Path(temporary)/'photonic_single_photon_checkpoint_07'
        process=subprocess.run([sys.executable,str(diagnostic),'--root',str(historical),
            '--output',str(out/'historical-audit')],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (out/'historical-audit.log').write_text(process.stdout)
        process.check_returncode()
    old=json.loads((out/'historical-audit/SUMMARY.json').read_text())
    if old['checks']!=998 or old['status']!='PASS_WITH_REPRODUCED_FINDINGS':
        raise ValueError('Historical audit did not reproduce its original contract')
    spec=importlib.util.spec_from_file_location('preserved_theory_audit_01',diagnostic)
    audit=importlib.util.module_from_spec(spec);sys.modules[spec.name]=audit;spec.loader.exec_module(audit)
    ref=audit.load(ROOT/'src/theory.py','theory')
    optics=audit.load(ROOT/'src/optics.py','optics')
    analyzer=audit.load(ROOT/'src/analyze_trials.py','analyze_trials')
    for function in (audit.audit_photon,audit.audit_classical,audit.audit_maps_and_reverse,audit.audit_statistics):
        print(function.__name__,flush=True);function(ref)
    audit.audit_readout(ROOT,ref,optics,analyzer)
    checks=len(audit.LEDGER)
    if checks!=993:
        raise ValueError(f'Expected all 993 scientific checks, got {checks}')
    historical_checks=json.loads((out/'historical-audit/CHECKS.json').read_text())[:993]
    def case_identity(name):
        # These two historical test names embed a frontier budget calculated by
        # the reference code. Repair-level roundoff changes that numeric suffix,
        # not the case order, selected branch, or acceptance tolerance.
        if name.startswith(('frontier_achievability_', 'frontier_budget_')):
            return name.rsplit('_',1)[0]
        return name
    name_differences=[]
    for old_check,new_check in zip(historical_checks,audit.LEDGER):
        if case_identity(old_check['name'])!=case_identity(new_check['name']) or old_check['tolerance']!=new_check['tolerance']:
            raise ValueError('Scientific case identity or tolerance changed')
        if old_check['name']!=new_check['name']:
            name_differences.append({'historical':old_check['name'],'repaired':new_check['name']})
    # Test helper solves the ORIGINAL secular equation with 120-digit arithmetic
    # and exact binary-input conversion, independently of production endpoint signs.
    helpers=audit.load(ROOT/'tests/test_photon_support.py','repair_bound_tests')
    import mpmath as mp
    historical_details=json.loads((out/'historical-audit/DIAGNOSTICS.json').read_text())
    old_stress={r['penalty']:r['computed_score'] for r in historical_details['findings'][1]['stress_cases']}
    stress=[]
    for penalty in (1e12,1e14,1e15,1e16,1e17,1e18):
        answer=ref.photon_score([.2,.4,.8,.9],penalty)
        with mp.workdps(120):
            expected=helpers.truth([.2,.4,.8,.9],penalty)
            if not mp.mpf(answer['score_lower'])<=expected<=mp.mpf(answer['score_upper']):
                raise ValueError('Independent high-precision support escaped enclosure')
            expected_text=mp.nstr(expected,110)
        stress.append({'penalty':penalty,'historical_score':old_stress[penalty],
            'repaired_score':answer['score'],'support_lower':answer['score_lower'],
            'support_upper':answer['score_upper'],'independent_120_digit_support':expected_text,
            'nominal_error':answer['E']})
    (out/'HIGH_PENALTY.json').write_text(json.dumps(stress,indent=2)+'\n')
    now=verify()
    if now!=integrity:raise ValueError('Protected source changed during repair checks')
    with (out/'SCIENTIFIC_CHECKS.json').open('w') as f:json.dump(audit.LEDGER,f,indent=2)
    with (out/'SCIENTIFIC_DIAGNOSTICS.json').open('w') as f:json.dump(audit.TABLES,f,indent=2,default=audit.serialize)
    summary={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
        'historical_audit_checks':998,'repaired_scientific_checks':checks,
        'scientific_case_order_and_tolerances_unchanged':True,
        'derived_budget_name_differences':name_differences,
        'original_audit_git_blob':blob,'baseline_main':'d07e4e2180992ab52ee08d0a0cad689154d2e9bd',
        'audit_commit':'10410caf761ad858236d22c4a2f5d9a53bc94dff',
        'max_scientific_residual':max(x['residual'] for x in audit.LEDGER),
        'elapsed_seconds':time.perf_counter()-start,'integrity':integrity,
        'python':sys.version,'numpy':audit.np.__version__,'scipy':audit.scipy.__version__,'mpmath':audit.mp.__version__,
        'photon_support_uses_exact_rational_enclosures':True,
        'entire_pipeline_interval_certified':False,'laboratory_data':False,
        'scope':'F01-F03 bounded repair regression. Historical defect assertions apply only to historical source; new fix tests are in tests/test_photon_support.py.'}
    (out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
