"""Run validation into a new directory and compare against frozen checkpoint evidence."""
from __future__ import annotations
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import uuid
from verify_import import ROOT, verify

ATOL = 1e-8
EXPECTED = {'analyzer_accounting_check.json', 'dimension_transfer.csv',
 'high_precision_check.json', 'hypothetical_design_forecast.csv',
 'hypothetical_design_inputs.json', 'independent_dual_checks.csv',
 'phase_gauge_warning.json', 'preparation_recipes.csv', 'quantum_frontier.csv',
 'synthetic_certification_example.json', 'synthetic_reverse_example.json',
 'uniform_exact_comparison.csv', 'validation.json'}

def compare(a, b, location='root') -> float:
    if isinstance(a, bool) or isinstance(b, bool):
        if type(a) != type(b) or a != b:
            raise ValueError('Boolean mismatch: '+location)
        return 0.0
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        error = abs(a-b)
        if not math.isfinite(a) or not math.isfinite(b) or error > ATOL:
            raise ValueError(f'Numeric mismatch at {location}: {a!r} versus {b!r}')
        return error
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            raise ValueError('Key mismatch: '+location)
        return max((compare(a[k], b[k], location+'.'+k) for k in a), default=0.0)
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            raise ValueError('Length mismatch: '+location)
        return max((compare(x, y, f'{location}[{i}]') for i, (x, y) in enumerate(zip(a,b))), default=0.0)
    if a != b:
        raise ValueError(f'Value mismatch at {location}: {a!r} versus {b!r}')
    return 0.0

def load_csv(path: Path) -> list:
    def cell(x):
        try:
            return float(x)
        except ValueError:
            return x
    with path.open(newline='') as stream:
        return [[cell(x) for x in row] for row in csv.reader(stream)]

def compare_run(out: Path, reference: Path) -> dict:
    got = {p.name for p in out.iterdir() if p.suffix in ('.json','.csv')}
    if got != EXPECTED:
        raise ValueError(f'Generated-file inventory mismatch: {got ^ EXPECTED}')
    report = {}
    for name in sorted(EXPECTED-{'validation.json'}):
        left, right = reference/name, out/name
        if name.endswith('.csv'):
            error = compare(load_csv(left), load_csv(right), name)
        else:
            error = compare(json.loads(left.read_text()), json.loads(right.read_text()), name)
        report[name] = {'byte_identical': left.read_bytes() == right.read_bytes(),
                        'maximum_numeric_difference': error}
    old = json.loads((reference/'validation.json').read_text())
    new = json.loads((out/'validation.json').read_text())
    for key in ('status','checks','seed','sdp_solver_used','lab_data_used'):
        compare(old['summary'][key], new['summary'][key], 'summary.'+key)
    metadata_changes = {
        'interval_arithmetic_used': (False, True),
        'scope': (
            'Proof-backed results plus numerical diagnostics. Searches and tests are not substitutes for universal proofs.',
            'Proof-backed results plus numerical diagnostics. Photon support uses exact-rational enclosures after audit repair 01; other calculations are not interval certified. Searches and tests are not substitutes for universal proofs.')}
    for key, (historical, repaired) in metadata_changes.items():
        compare(old['summary'][key], historical, 'historical_metadata.'+key)
        compare(new['summary'][key], repaired, 'repaired_metadata.'+key)
    if new['summary']['checks'] != 5261 or len(new['checks']) != 5261:
        raise ValueError('Unexpected checkpoint check count')
    for i, (a,b) in enumerate(zip(old['checks'], new['checks'])):
        if a['name'] != b['name'] or a['tolerance'] != b['tolerance']:
            raise ValueError('Check identity/tolerance changed at '+str(i))
        if not math.isfinite(b['residual']) or not 0 <= b['residual'] <= b['tolerance']:
            raise ValueError('Residual outside declared bound: '+b['name'])
    return {'reference_comparison': 'PASS', 'absolute_numeric_tolerance': ATOL,
            'files': report, 'archived_summary': old['summary'], 'fresh_summary': new['summary'],
            'validation_policy': 'Same ordered checks and tolerances; residuals need not be byte identical.',
            'approved_metadata_changes':metadata_changes}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New results/runs/<name> directory or new external directory')
    args = parser.parse_args()
    integrity = verify()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    out = (args.output or ROOT/'results/runs'/stamp).resolve()
    frozen, runs = (ROOT/'results').resolve(), (ROOT/'results/runs').resolve()
    if out.exists() or out == frozen or out == runs or (frozen in out.parents and runs not in out.parents):
        parser.error('Output must be new and must not overwrite archived results')
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    process = subprocess.run([sys.executable, str(ROOT/'src/validate.py'), '--output-dir', str(out)],
                             cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if out.is_dir():
        (out/'run.log').write_text(process.stdout)
    print(process.stdout)
    process.check_returncode()
    comparison = compare_run(out, ROOT/'results')
    verify()
    try:
        commit = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = None
    comparison.update({'integrity': integrity, 'git_start_commit': commit,
        'utc': datetime.now(timezone.utc).isoformat(), 'output_directory': str(out),
        'source_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
                          for p in ('src/validate.py','src/theory.py','src/photon_support.py','src/optics.py','src/analyze_trials.py')},
        'purpose': 'Post-audit repair regression against preserved checkpoint-07 evidence; not a new novelty audit.',
        'lab_data_used': False})
    (out/'REPRODUCTION.json').write_text(json.dumps(comparison, indent=2)+'\n')
    print('Reproduction and protected-file verification PASS:', out)

if __name__ == '__main__':
    main()
