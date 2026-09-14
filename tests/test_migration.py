"""Engineering regressions, separate from the inherited scientific checks."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from verify_import import verify
from reproduce import compare

class ImportTests(unittest.TestCase):
    def test_source_integrity(self):
        self.assertEqual(verify()['source_members'],39)

    def test_tampered_copy_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'copy'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','runs','__pycache__'))
            (root/'proofs/THEORY.md').write_text('tampered')
            with self.assertRaisesRegex(ValueError,'Protected working file changed'):
                verify(root)

    def test_missing_output_rejected(self):
        p=subprocess.run([sys.executable,str(ROOT/'src/validate.py')],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0)
        self.assertIn('--output-dir',p.stderr)

    def test_frozen_output_rejected(self):
        p=subprocess.run([sys.executable,str(ROOT/'src/validate.py'),'--output-dir',str(ROOT/'results')],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0)
        self.assertIn('archived results',p.stderr)

    def test_existing_external_output_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=subprocess.run([sys.executable,str(ROOT/'src/validate.py'),'--output-dir',d],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0)
            self.assertIn('FileExistsError',p.stderr)
            self.assertEqual(list(Path(d).iterdir()),[])

    def test_wrapper_existing_output_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=subprocess.run([sys.executable,str(ROOT/'scripts/reproduce.py'),'--output',d],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0)
            self.assertEqual(list(Path(d).iterdir()),[])

    def test_numeric_tolerance(self):
        self.assertLess(compare([1.,2.],[1.+1e-10,2.]),1e-8)
        with self.assertRaises(ValueError): compare([1.],[1.01])

    def test_schema_rejected(self):
        with self.assertRaises(ValueError): compare({'a':1},{'b':1})
        with self.assertRaises(ValueError): compare([1],[1,2])
        with self.assertRaises(ValueError): compare('PASS','FAIL')

    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError): compare(float('nan'),0.)
        with self.assertRaises(ValueError): compare(float('inf'),float('inf'))

    def test_bool_not_number(self):
        with self.assertRaises(ValueError): compare(True,1)

    def test_trial_template_has_no_data(self):
        self.assertEqual(len((ROOT/'templates/trials.csv').read_text().splitlines()),1)

    def test_synthetic_labels_retained(self):
        for p in (ROOT/'results').glob('synthetic_*.json'):
            self.assertIn('SYNTHETIC',json.loads(p.read_text())['status'])

if __name__=='__main__': unittest.main()
