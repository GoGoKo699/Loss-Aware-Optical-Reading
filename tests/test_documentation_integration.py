"""Document integration checks, separate from mathematical validation.

These tests protect the interpretation-only hash chain, attribution/limitations,
existing equations and lab questions, and the preserved predecessor audit.
They do not prove scientific novelty or validate laboratory calibration.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from verify_import import verify, DOCUMENT_RECORD, DOCUMENT_PATHS

READERS = ('README.md', 'CLAIM_STATUS.md', 'SOURCE_AUDIT.md', 'REPORT.md',
           'docs/CONTRIBUTIONS.md', 'docs/ROADMAP.md', 'experiment/LAB_REVIEW.md',
           'experiment/REVIEW_RATIONALE.md', 'work_orders/CURRENT.md')


class DocumentationIntegrationTests(unittest.TestCase):
    def copy_root(self, directory):
        target = Path(directory)/'repo'
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('.git', 'runs', '__pycache__'))
        return target

    def test_document_chain_passes(self):
        result = verify()
        self.assertEqual(set(result['authorized_document_changes_verified']), DOCUMENT_PATHS)
        self.assertTrue(result['source_archive_unchanged'])
        self.assertTrue(result['original_import_manifest_unchanged'])

    def test_stale_document_preimage_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.copy_root(d)
            p = root/DOCUMENT_RECORD
            ledger = json.loads(p.read_text())
            ledger['changes'][0]['old_sha256'] = '0'*64
            p.write_text(json.dumps(ledger))
            with self.assertRaisesRegex(ValueError, 'Documentation ledger previous hash'):
                verify(root)

    def test_document_ledger_cannot_authorize_source_or_missing_document(self):
        for replacement in ('src/theory.py', '../outside.md', None):
            with self.subTest(replacement=replacement), tempfile.TemporaryDirectory() as d:
                root = self.copy_root(d)
                p = root/DOCUMENT_RECORD
                ledger = json.loads(p.read_text())
                if replacement is None:
                    ledger['changes'].pop()
                else:
                    ledger['changes'][0]['path'] = replacement
                p.write_text(json.dumps(ledger))
                with self.assertRaisesRegex(ValueError, 'authorized document set'):
                    verify(root)

    def test_changed_note_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.copy_root(d)
            (root/'docs/CONTRIBUTIONS.md').write_text('Unsupported novelty claim')
            with self.assertRaisesRegex(ValueError, 'Protected documentation changed'):
                verify(root)

    def test_predecessor_audit_preserved(self):
        audit = ROOT/'audits/novelty-01'
        manifest = json.loads((audit/'MANIFEST.json').read_text())
        for name, expected in manifest['files'].items():
            with self.subTest(name=name):
                self.assertEqual(hashlib.sha256((audit/name).read_bytes()).hexdigest(), expected)

    def test_report_equations_and_lab_questions_preserved(self):
        manifest = json.loads((ROOT/'provenance/IMPORT_MANIFEST.json').read_text())
        with ZipFile(ROOT/manifest['archive']) as archive:
            prefix = 'photonic_single_photon_checkpoint_07/'
            before = archive.read(prefix+'REPORT.md').decode()
            old_questions = archive.read(prefix+'experiment/LAB_REVIEW.md').decode()
        old_math = re.findall(r'\\\[(.*?)\\\]', before, flags=re.S)
        new_math = re.findall(r'\$\$(.*?)\$\$', (ROOT/'REPORT.md').read_text(), flags=re.S)
        self.assertEqual(len(old_math), 11)
        self.assertEqual(old_math, new_math)
        section = lambda s: s.split('## Required responses')[1].split('## What to send back')[0]
        self.assertEqual(section(old_questions), section((ROOT/'experiment/LAB_REVIEW.md').read_text()))

    def test_reader_links_resolve(self):
        for name in READERS:
            text = (ROOT/name).read_text()
            for target in re.findall(r'\]\(([^)]+)\)', text):
                parts = urlsplit(target)
                if parts.scheme or parts.netloc or not parts.path:
                    continue
                path = ((ROOT/name).parent/unquote(parts.path)).resolve()
                with self.subTest(document=name, target=target):
                    self.assertTrue(path.exists())
                    self.assertIn(ROOT.resolve(), path.parents)

    def test_reader_math_delimiters_and_headings(self):
        for name in READERS:
            text = (ROOT/name).read_text()
            with self.subTest(name=name):
                self.assertEqual(text.count('$$') % 2, 0)
                self.assertNotIn('\\operatorname', text)
                self.assertNotIn('\\[', text)
                self.assertFalse(any('$' in line for line in text.splitlines() if line.startswith('#')))

    def test_claim_boundaries_are_visible(self):
        note = (ROOT/'docs/CONTRIBUTIONS.md').read_text()
        source = (ROOT/'SOURCE_AUDIT.md').read_text()
        rationale = (ROOT/'experiment/REVIEW_RATIONALE.md').read_text()
        for phrase in ('per attempted interrogation', 'mean incident signal budget',
                       'arbitrarily\nrare bright pulses', 'occupied bypass rail',
                       'retained idler', 'not a manuscript or a priority clearance'):
            self.assertIn(phrase, note)
        for phrase in ('S18', 'S20', "Eq. (4.18)", 'not a proved optimal input rule'):
            self.assertIn(phrase, source)
        for phrase in ('M1', 'P1', 'P2', 'All example settings', 'all 16 detector masks'):
            self.assertIn(phrase, rationale)
        self.assertIn('does not claim a new literature search', source.replace('\n', ' '))


if __name__ == '__main__':
    unittest.main()
