"""Preserve the supplied study and rerun its independent finite-model checks."""
from pathlib import Path
import hashlib
import json
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

    def test_regeneration_and_optimizer_free_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'fresh';verified=Path(tmp)/'verified'
            self.run_script('study.py','--output',out)
            b=(out/'RESULTS.json').read_bytes()
            self.assertEqual(hashlib.sha256(b).hexdigest(),
                '74c0b5ca9f114be36501426f28dc012fcfdb6b872ed6bb8533d463b6cddd14db')
            self.run_script('verify_certificates.py','--results',out/'RESULTS.json','--output',verified)
            result=json.loads((verified/'VERIFICATION.json').read_text())
            self.assertEqual(result['status'],'PASS')
            self.assertEqual(result['checks'],11161)
            # A second invocation must refuse to replace the fresh evidence.
            p=subprocess.run([sys.executable,str(STUDY/'study.py'),'--output',str(out)],capture_output=True,text=True,timeout=20)
            self.assertNotEqual(p.returncode,0)
            self.assertEqual((out/'RESULTS.json').read_bytes(),b)

if __name__=='__main__':unittest.main()
