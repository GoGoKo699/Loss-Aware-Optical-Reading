"""Reader integration, immutable science, and predecessor-translation regressions."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from verify_import import verify, DOCUMENT_RECORD

NOTES = ['README.md', 'CLAIM_STATUS.md', 'SOURCE_AUDIT.md', 'REPORT.md',
         'docs/CONTRIBUTIONS.md', 'docs/REPRODUCE.md', 'docs/ROADMAP.md',
         'experiment/LAB_REVIEW.md', 'experiment/CLAIMS_TO_TESTS.md',
         'work_orders/CURRENT.md', 'integrations/claims-01/REPORT.md']


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


class ClaimsIntegrationTests(unittest.TestCase):
    def test_document_chain_and_scope(self):
        result = verify()
        self.assertEqual(len(result['authorized_changes_verified']), 4)
        self.assertEqual(len(result['documentation_changes_verified']), 4)
        self.assertFalse(result['mathematics_changed_by_documentation'])
        self.assertEqual(len(result['documentation_additions_verified']), 2)

    def test_mathematics_and_acquisition_unchanged(self):
        expected = {
            'proofs/THEORY.md': 'daa095381a2c21f1a9a9f660fe68cd8354e56bd6',
            'src/theory.py': 'e038afe2a21c6e54e3fc6eaccfbcb07c9de3ff60',
            'src/photon_support.py': '133f2b8cb6c41edf6ec873740b58c04eb94e632b',
            'src/analyze_trials.py': '247b1fed023aed713dc677a3a47c911ed3da2186',
            'experiment/FIRST_EXPERIMENT.md': '44982c838b60ffc11379fe9052defdf8869d2037',
        }
        for name, expected_blob in expected.items():
            with self.subTest(path=name):
                self.assertEqual(git_blob((ROOT/name).read_bytes()), expected_blob)

    def test_novelty_audit_preserved(self):
        root = ROOT/'audits/novelty-01'
        data = (root/'MANIFEST.json').read_bytes()
        self.assertEqual(git_blob(data), '727238f9cfb0e364719d5e3c95343a3c1033d062')
        manifest = json.loads(data)
        for name, expected in manifest['files'].items():
            self.assertEqual(digest((root/name).read_bytes()), expected, name)

    def test_report_equations_and_lab_questions_preserved(self):
        with ZipFile(ROOT/'provenance/archives/photonic_single_photon_checkpoint_07.zip') as z:
            old = z.read('photonic_single_photon_checkpoint_07/REPORT.md').decode()
            lab = z.read('photonic_single_photon_checkpoint_07/experiment/LAB_REVIEW.md').decode()
        current = (ROOT/'REPORT.md').read_text()
        self.assertEqual(re.findall(r'\\\[(.*?)\\\]', old, re.S),
                         re.findall(r'\$\$(.*?)\$\$', current, re.S))
        no_display = re.sub(r'\$\$.*?\$\$', '', current, flags=re.S)
        self.assertEqual(re.findall(r'\\\((.*?)\\\)', old, re.S),
                         re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', no_display, re.S))
        def questions(text):
            return text.split('## Required responses\n', 1)[1].split('## What to send back\n', 1)[0]
        self.assertEqual(questions(lab), questions((ROOT/'experiment/LAB_REVIEW.md').read_text()))

    def test_reading_links_and_math_delimiters(self):
        for name in NOTES:
            text = (ROOT/name).read_text()
            with self.subTest(path=name):
                self.assertNotIn('\\operatorname', text)
                self.assertNotIn('\\[', text)
                self.assertEqual(text.count('$$') % 2, 0)
                for target in re.findall(r'\]\(([^)]+)\)', text):
                    if '://' in target or target.startswith('mailto:'):
                        continue
                    path, _, anchor = target.partition('#')
                    resolved = ((ROOT/name).parent/path).resolve() if path else ROOT/name
                    self.assertTrue(resolved.exists(), (name, target))
                    if anchor and resolved.suffix == '.md':
                        headings = re.findall(r'^#+ (.+)$', resolved.read_text(), re.M)
                        slugs = [re.sub(r'[^\w -]', '', h.lower()).replace(' ', '-') for h in headings]
                        self.assertIn(anchor, slugs, (name, target))

    def test_document_tampering_rejected(self):
        for failure in ('previous_hash', 'mathematical_path', 'duplicate', 'added_document'):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as d:
                root = Path(d)/'repo'
                shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.git', 'runs', '__pycache__'))
                path = root/DOCUMENT_RECORD
                ledger = json.loads(path.read_text())
                if failure == 'previous_hash':
                    ledger['changes'][0]['old_sha256'] = '0'*64
                elif failure == 'mathematical_path':
                    ledger['changes'][0]['path'] = 'src/theory.py'
                elif failure == 'duplicate':
                    ledger['changes'].append(ledger['changes'][0])
                else:
                    (root/'docs/CONTRIBUTIONS.md').write_text('altered')
                path.write_text(json.dumps(ledger))
                with self.assertRaises(ValueError):
                    verify(root)

    def test_candidate_and_gap_status_explicit(self):
        for name in ('README.md', 'CLAIM_STATUS.md', 'docs/CONTRIBUTIONS.md'):
            self.assertIn('candidate', (ROOT/name).read_text().lower())
        sources = (ROOT/'SOURCE_AUDIT.md').read_text()
        self.assertIn('S18', sources)
        self.assertIn('S20', sources)
        self.assertIn('not a worldwide priority certificate', sources)
        self.assertIn('not executed', (ROOT/'work_orders/CURRENT.md').read_text())

    def test_focused_predecessor_comparison(self):
        env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
        with tempfile.TemporaryDirectory() as d:
            output = Path(d)/'run'
            subprocess.run([sys.executable, str(ROOT/'audits/novelty-01/comparison_checks.py'),
                            '--source-root', str(ROOT), '--output', str(output)],
                           check=True, capture_output=True, text=True, env=env)
            actual = json.loads((output/'RESULTS.json').read_text())
        with tarfile.open(ROOT/'audits/novelty-01/EVIDENCE.tar.xz') as archive:
            expected = json.load(archive.extractfile('RESULTS.json'))
        self.assertEqual(actual['checks'], 631)
        self.assertEqual(actual['groups'], expected['groups'])
        for a, b in zip(actual['ledger'], expected['ledger']):
            self.assertEqual((a['group'], a['name'], a['tolerance']),
                             (b['group'], b['name'], b['tolerance']))
            self.assertLessEqual(a['residual'], a['tolerance'])
        for key in ('optimized_nulling_receiver', 'feasible_arbitrary_POVM'):
            self.assertAlmostEqual(actual['examples']['high_energy_scope'][key],
                                   expected['examples']['high_energy_scope'][key], places=9)
        self.assertEqual(actual['status'], 'PASS')


if __name__ == '__main__':
    unittest.main()
