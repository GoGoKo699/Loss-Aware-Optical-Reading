"""Preserve the supplied study and rerun its independent finite-model checks."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
import math
import os
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT/'studies/robustness-01'
ARCHIVE = ROOT/'integrations/lab-handover-01/SUPPLIED_ROBUSTNESS.zip'
ARCHIVE_HASH = 'ee21bb13afbd913779b5d2eae7b4f15a58d919500a7ed38b09deafb7e929c81b'
RESULTS_HASH = '74c0b5ca9f114be36501426f28dc012fcfdb6b872ed6bb8533d463b6cddd14db'


def supplied_results():
    with tarfile.open(STUDY/'EVIDENCE.tar.xz', 'r:xz') as archive:
        return archive.extractfile('RESULTS.json').read()


def certified_interval(record):
    """Read rational endpoints, using outward floats only if no exact field exists."""
    return (Fraction(record.get('lower_exact', record['lower'])),
            Fraction(record.get('upper_exact', record.get('u', record['upper']))))


def assert_portable_results(reference, fresh):
    """Compare scientific content; acceptance ALSO requires the unchanged verifier.

    BLAS kernels may propose different feasible POVMs or choose different tied
    policies. Their byte encodings and C/E/F need not agree. The finite models,
    named checks, exact optimum enclosures and scientific claims must agree.
    No tolerance in the supplied study or verifier is changed here.
    """
    def require(condition, name):
        if not condition:
            raise AssertionError(name)

    def same_keys(a, b, name):
        require(isinstance(b, dict) and a.keys() == b.keys(), name+' schema')

    def overlap(a, b, name):
        lo, hi = certified_interval(a)
        flo, fhi = certified_interval(b)
        require(lo <= hi and flo <= fhi, name+' endpoint order')
        require(max(lo, flo) <= min(hi, fhi), name+' nonoverlap')

    def nominal(a, b, name):
        # The supplied direct optical crosscheck already uses 1e-12.
        require(math.isfinite(b) and abs(a-b) < 1e-12, name+' nominal crosscheck')

    def rates(record, name):
        values = [record[k] for k in ('C', 'E', 'F')]
        require(all(math.isfinite(x) and x >= -1e-13 for x in values), name+' probabilities')
        require(abs(sum(values)-1) < 1e-12, name+' outcome accounting')
        require(abs(record['C']-5*record['E']-float(Fraction(record['lower_exact']))) < 1e-12,
                name+' payoff accounting')

    same_keys(reference, fresh, 'results')
    for key in reference.keys()-{'cases'}:
        require(reference[key] == fresh[key], 'results/'+key)
    require(len(fresh['cases']) == 41, 'case inventory')
    require(Counter(c['model']['kind'] for c in fresh['cases']) ==
            {'marked_phase':17, 'dephase':12, 'unitary':6, 'distributed_loss':6}, 'model inventory')

    # The report gives 2.16e-08 to three significant figures for phase precision.
    # The longer SUMMARY number is an observation of the preserved run, not a
    # portable acceptance tolerance. Fresh enclosures must retain those digits.
    phase_precision = float(format(json.loads((STUDY/'SUMMARY.json').read_text())
                                   ['maximum_phase_joint_interval_width'], '.3g'))
    fixed_precision = max(float(format(float(certified_interval(c['fixed'])[1]-
                                            certified_interval(c['fixed'])[0]), '.3g'))
                          for c in reference['cases'])
    ideal_precision = max(float(format(float(certified_interval(c['ideal'])[1]-
                                            certified_interval(c['ideal'])[0]), '.3g'))
                          for c in reference['cases'])

    for old, new in zip(reference['cases'], fresh['cases']):
        name = old['id']
        same_keys(old, new, name)
        require(old['id'] == new['id'] and old['model'] == new['model'], name+' model')
        for key in ('fixed', 'ideal', 'joint', 'regret', 'P1_illustrative'):
            same_keys(old[key], new[key], name+'/'+key)
        for key in ('fixed', 'ideal', 'joint'):
            overlap(old[key], new[key], name+'/'+key)
        for key, ceiling in (('fixed', fixed_precision), ('ideal', ideal_precision)):
            lo, hi = certified_interval(new[key])
            require(float(format(float(hi-lo), '.3g')) <= ceiling, name+'/'+key+' precision')
        require(old['fixed']['scope'] == new['fixed']['scope'] and
                old['fixed']['policies_checked'] == new['fixed']['policies_checked'], name+' fixed class')
        policy = new['fixed']['policy']
        require(len(policy) == 5 and policy[-1] == 4 and
                all(type(x) is int and 0 <= x <= 4 for x in policy), name+' policy')
        rates(new['fixed'], name+'/fixed')
        require(old['regret']['scope'] == new['regret']['scope'], name+' regret interpretation')
        overlap(old['regret'], new['regret'], name+'/regret')
        if old['regret']['lower'] > 0:
            require(new['regret']['lower'] > 0, name+' positive-regret claim lost')
        kind = new['model']['kind']
        if kind == 'marked_phase':
            joint = new['joint']
            require(joint['exact_dual_checked'] is True and joint['exact_measurement_checked'] is True,
                    name+' exact certificate flags')
            lo, hi = certified_interval(joint)
            require(float(format(float(hi-lo), '.3g')) <= phase_precision, name+' joint precision')
            # Proposal diagnostics may differ. They never replace exact checks.
            require(type(joint['iterations']) is int and 1 <= joint['iterations'] <= 300,
                    name+' iteration inventory')
            require(math.isfinite(joint['LP_residual']) and 0 <= joint['LP_residual'] < 2e-8,
                    name+' unchanged proposal target')
            require(all(set(event) == {'iteration', 'method', 'message'} for event in joint['solver_events']),
                    name+' solver-event schema')
            rates(joint, name+'/joint')
            if old['regret']['lower'] > 0:
                require(lo > certified_interval(new['fixed'])[1], name+' exact positive regret lost')
        else:
            require(old['joint']['proof'] == new['joint']['proof'], name+' proof interpretation')
            if kind == 'dephase':
                require(old['regret'] == new['regret'], name+' exact zero-regret claim')
                same_keys(old['joint']['support'], new['joint']['support'], name+'/support')
                overlap(old['joint']['support'], new['joint']['support'], name+'/support')
                lo, hi = certified_interval(new['joint']['support'])
                require(float(format(float(hi-lo), '.3g')) <= ideal_precision, name+' dephasing precision')
            if kind == 'unitary':
                nominal(new['ideal']['lower'], new['calibrated_score'], name+' calibration invariance')
        for key in ('generic_map_radius', 'generic_regret_upper'):
            if old[key] is None:
                require(new[key] is None, name+'/'+key)
            else:
                nominal(old[key], new[key], name+'/'+key)
        for key, value in old['P1_illustrative'].items():
            if key in ('status', 'mean_budget', 'uniform_downstream_survival'):
                require(value == new['P1_illustrative'][key], name+'/P1/'+key)
            else:
                nominal(value, new['P1_illustrative'][key], name+'/P1/'+key)


class RobustnessImportTests(unittest.TestCase):
    def test_delivery_bytes_and_work_order_preserved(self):
        self.assertEqual(hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(), ARCHIVE_HASH)
        with zipfile.ZipFile(ARCHIVE) as z:
            for name in z.namelist():
                if name.startswith('studies/') and not name.endswith('/'):
                    self.assertEqual((ROOT/name).read_bytes(), z.read(name), name)
            delivery = json.loads(z.read('DELIVERY.json'))
            self.assertEqual(hashlib.sha256(z.read('robustness-01.patch')).hexdigest(), delivery['patch_sha256'])
        b=(STUDY/'WORK_ORDER.md').read_bytes()
        self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),
                         '9b59ff9a5260587f30021ed33a8477a0a9f8a88c')
        for name, expected in json.loads((STUDY/'MANIFEST.json').read_text())['files'].items():
            self.assertEqual(hashlib.sha256((STUDY/name).read_bytes()).hexdigest(),expected,name)

    def run_script(self,script,*args):
        env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
        p=subprocess.run([sys.executable,str(STUDY/script),*map(str,args)],capture_output=True,text=True,env=env,timeout=180)
        self.assertEqual(p.returncode,0,p.stdout+'\n'+p.stderr)
        return p

    def test_supplied_units(self):
        self.run_script('test_local.py')

    def verify_file(self, path, output):
        self.run_script('verify_certificates.py', '--results', path, '--output', output)
        result = json.loads((output/'VERIFICATION.json').read_text())
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['verified_cases'], 41)
        self.assertEqual(result['checks'], 11161)
        self.assertEqual(result['exact_positive_matrices'], 10828)
        self.assertIs(result['solver_called'], False)
        self.assertEqual(result['results_sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
        with tarfile.open(STUDY/'EVIDENCE.tar.xz', 'r:xz') as archive:
            original_checks = json.loads(archive.extractfile('VERIFICATION.json').read())['checks_passed']
        self.assertEqual(result['checks_passed'], original_checks)
        return result

    def test_regeneration_and_optimizer_free_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'fresh'
            reference_bytes = supplied_results()
            self.assertEqual(hashlib.sha256(reference_bytes).hexdigest(), RESULTS_HASH)
            reference_path = Path(tmp)/'supplied.json'
            reference_path.write_bytes(reference_bytes)
            self.verify_file(reference_path, Path(tmp)/'supplied-verified')
            self.run_script('study.py','--output',out)
            b=(out/'RESULTS.json').read_bytes()
            result=self.verify_file(out/'RESULTS.json', Path(tmp)/'fresh-verified')
            reference = json.loads(reference_bytes)
            fresh = json.loads(b)
            differences = []
            def compare(a, c, path=''):
                if isinstance(a, dict) and isinstance(c, dict) and a.keys() == c.keys():
                    for key in a:
                        compare(a[key], c[key], path+'/'+key)
                elif isinstance(a, list) and isinstance(c, list) and len(a) == len(c):
                    for index, (aa, cc) in enumerate(zip(a, c)):
                        compare(aa, cc, path+'/'+str(index))
                elif a != c:
                    differences.append({'path':path, 'reference':str(a)[:160], 'fresh':str(c)[:160]})
            compare(reference, fresh)
            print(json.dumps({'supplied_results_sha256':RESULTS_HASH,
                'fresh_results_sha256':hashlib.sha256(b).hexdigest(),
                'byte_identical':b == reference_bytes,
                'fresh_witness_verification':result['status'],
                'checks':result['checks'], 'exact_positive_matrices':result['exact_positive_matrices'],
                'difference_count':len(differences), 'differences':differences[:40]}, indent=2), flush=True)
            assert_portable_results(reference, fresh)
            # A second invocation must refuse to replace the fresh evidence.
            p=subprocess.run([sys.executable,str(STUDY/'study.py'),'--output',str(out)],capture_output=True,text=True,timeout=20)
            self.assertNotEqual(p.returncode,0)
            self.assertEqual((out/'RESULTS.json').read_bytes(),b)

    def test_portability_rejects_scientific_tampering(self):
        reference = json.loads(supplied_results())
        assert_portable_results(reference, reference)
        changed = deepcopy(reference)
        changed['cases'][0]['model']['amplitudes_hex'][0] = float(.5).hex()
        with self.assertRaisesRegex(AssertionError, 'model'):
            assert_portable_results(reference, changed)
        changed = deepcopy(reference)
        changed['cases'][0]['joint'].update(lower_exact='1', upper_exact='2', lower=1., upper=2.)
        with self.assertRaisesRegex(AssertionError, 'nonoverlap'):
            assert_portable_results(reference, changed)
        changed = deepcopy(reference)
        next(c for c in changed['cases'] if c['regret']['lower'] > 0)['regret']['lower'] = 0.
        with self.assertRaisesRegex(AssertionError, 'positive-regret claim lost'):
            assert_portable_results(reference, changed)
        changed = deepcopy(reference)
        changed['ledger'][0]['pass'] = False
        with self.assertRaisesRegex(AssertionError, 'ledger'):
            assert_portable_results(reference, changed)
        changed = deepcopy(reference)
        c = next(c for c in changed['cases'] if c['model']['kind'] == 'dephase')
        c['regret']['upper'] = 1e-6
        with self.assertRaisesRegex(AssertionError, 'zero-regret'):
            assert_portable_results(reference, changed)

    def test_different_factor_encoding_requires_exact_verification(self):
        reference = json.loads(supplied_results())
        changed = deepcopy(reference)
        # Negating one whole factor column leaves its positive effect FF* exact.
        factor = changed['cases'][0]['joint']['effect_factors'][0]
        column = max(range(4), key=lambda k: sum(Fraction(part)**2 for row in factor for part in row[k]))
        for row in factor:
            row[column] = [str(-Fraction(part)) for part in row[column]]
        self.assertNotEqual(changed, reference)
        assert_portable_results(reference, changed)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'equivalent.json'
            path.write_text(json.dumps(changed)+'\n')
            self.verify_file(path, Path(tmp)/'equivalent-verified')
            # The semantic comparison alone is insufficient: an invalid effect
            # still looks like a different encoding, but exact completeness fails.
            invalid = deepcopy(reference)
            for row in invalid['cases'][0]['joint']['effect_factors'][0]:
                row[column] = [str(2*Fraction(part)) for part in row[column]]
            assert_portable_results(reference, invalid)
            invalid_path = Path(tmp)/'invalid.json'
            invalid_path.write_text(json.dumps(invalid)+'\n')
            result = subprocess.run([sys.executable, str(STUDY/'verify_certificates.py'),
                '--results', str(invalid_path), '--output', str(Path(tmp)/'invalid-verified')],
                capture_output=True, text=True, timeout=180)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('measurement_complete', result.stderr)
            self.assertFalse((Path(tmp)/'invalid-verified').exists())

if __name__=='__main__':unittest.main()
