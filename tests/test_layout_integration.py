"""Keep the requested layout/motivation revision inside its document boundary.

These are integrity checks, not novelty clearance or mathematical proofs. The
previous handover ledger is immutable; current bytes follow an explicit chain.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from verify_import import (
    verify, LAYOUT_RECORD, LAYOUT_PATHS, LAYOUT_PREIMAGES, LAYOUT_BASE_COMMIT,
    LAYOUT_BASE_TREE, HANDOVER_RECORD, HISTORICAL_LEDGER_SHA256, _layout_hash,
)


class LayoutIntegrationTests(unittest.TestCase):
    def copy_root(self, directory):
        root = Path(directory)/'repo'
        shutil.copytree(ROOT, root,
                        ignore=shutil.ignore_patterns('.git', 'runs', '__pycache__'))
        return root

    def alter(self, root, change):
        path = root/LAYOUT_RECORD
        ledger = json.loads(path.read_text())
        change(ledger)
        path.write_text(json.dumps(ledger))

    def test_authorized_documents_and_immutable_history(self):
        self.assertEqual(LAYOUT_PATHS, frozenset({
            'README.md', 'docs/CONTRIBUTIONS.md', 'docs/THEORY_ROUTE.md',
            'docs/PHILOSOPHY_DRAFT.md', 'docs/ROBUSTNESS_GUIDE.md',
            'experiment/M1.md', 'experiment/P1.md', 'experiment/P2.md',
            'experiment/SU4.md', 'experiment/SU8.md',
        }))
        result = verify()
        self.assertEqual(set(result['authorized_layout_documents_verified']), LAYOUT_PATHS)
        self.assertFalse(result['mathematics_changed_by_layout'])
        self.assertTrue(result['historical_change_ledgers_unchanged'])
        self.assertTrue(result['source_archive_unchanged'])
        self.assertEqual(result['source_members'], 39)
        for path, expected in HISTORICAL_LEDGER_SHA256.items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), expected)

    def test_exact_recorded_baseline_and_old_new_bytes(self):
        ledger = json.loads((ROOT/LAYOUT_RECORD).read_text())
        self.assertEqual(ledger['base_commit'], LAYOUT_BASE_COMMIT)
        self.assertEqual(ledger['base_tree'], LAYOUT_BASE_TREE)
        self.assertEqual(ledger['previous_record'], HANDOVER_RECORD)
        self.assertEqual(ledger['previous_record_sha256'],
                         HISTORICAL_LEDGER_SHA256[HANDOVER_RECORD])
        for entry in ledger['changes']:
            self.assertEqual(entry['old_sha256'], LAYOUT_PREIMAGES[entry['path']])
            self.assertEqual(entry['new_sha256'],
                             hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest())

    def test_baseline_cannot_be_retargeted(self):
        mutations = {
            'schema': 2, 'interpretation_only': False,
            'mathematical_content_changed': True,
            'original_archive_sha256': '0'*64,
            'previous_record': 'provenance/changes/novelty-integration-02.json',
            'previous_record_sha256': '0'*64,
            'base_commit': '0'*40, 'base_tree': '0'*40,
        }
        for field, value in mutations.items():
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                self.alter(root, lambda ledger: ledger.update({field: value}))
                with self.assertRaisesRegex(ValueError, 'Invalid layout documentation ledger contract'):
                    verify(root)

    def test_stale_preimages_rejected_for_all_ten_documents(self):
        for path in LAYOUT_PATHS:
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                self.alter(root, lambda ledger: next(e for e in ledger['changes']
                    if e['path'] == path).update(old_sha256='0'*64))
                with self.assertRaisesRegex(ValueError, 'baseline hash mismatch'):
                    verify(root)

    def test_science_protocol_results_and_outside_paths_cannot_be_added(self):
        for path in ('src/theory.py', 'proofs/THEORY.md', 'experiment/FIRST_EXPERIMENT.md',
                     'results/validation.json', '../outside.md'):
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                self.alter(root, lambda ledger: ledger['changes'][0].update(path=path))
                with self.assertRaisesRegex(ValueError, 'authorized document set'):
                    verify(root)

    def test_missing_duplicate_and_new_paths_rejected(self):
        mutations = (
            lambda ledger: ledger['changes'].pop(),
            lambda ledger: ledger['changes'].append(dict(ledger['changes'][0])),
            lambda ledger: ledger.update(additions=[{'path': 'docs/UNREVIEWED.md'}]),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                self.alter(root, mutation)
                with self.assertRaisesRegex(ValueError, 'authorized document set'):
                    verify(root)

    def test_unrecorded_protected_bytes_rejected(self):
        for path in LAYOUT_PATHS:
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                with (root/path).open('a') as handle:
                    handle.write('\nAn unrecorded change.\n')
                with self.assertRaisesRegex(ValueError, 'Protected .* changed'):
                    verify(root)

    def test_reason_and_new_hash_must_be_valid(self):
        mutations = [('reason', value) for value in ('', '   ', None, ['yes'])]
        mutations += [('new_sha256', value) for value in (None, 'F'*64, 'not a hash')]
        for key, value in mutations:
            with self.subTest(key=key, value=value), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                self.alter(root, lambda ledger: ledger['changes'][0].update({key: value}))
                with self.assertRaises(ValueError):
                    verify(root)

    def test_predecessor_current_hash_must_connect_to_new_layer(self):
        path = 'README.md'
        change = {'old_sha256': LAYOUT_PREIMAGES[path], 'new_sha256': '1'*64}
        with self.assertRaisesRegex(ValueError, 'previous hash mismatch'):
            _layout_hash(path, '0'*64, {path: change})
        self.assertEqual(_layout_hash(path, LAYOUT_PREIMAGES[path], {path: change}), '1'*64)
        self.assertEqual(_layout_hash('src/theory.py', '2'*64, {path: change}), '2'*64)
        # A superficially well-formed edit of the previous accepted README hash
        # cannot be legitimized by keeping the new ledger or current file intact.
        with tempfile.TemporaryDirectory() as directory:
            root = self.copy_root(directory)
            ledger_path = root/HANDOVER_RECORD
            ledger = json.loads(ledger_path.read_text())
            next(entry for entry in ledger['changes'] if entry['path'] == path)['new_sha256'] = '0'*64
            ledger_path.write_text(json.dumps(ledger))
            with self.assertRaisesRegex(ValueError, 'previous hash mismatch'):
                verify(root)


if __name__ == '__main__':
    unittest.main()
