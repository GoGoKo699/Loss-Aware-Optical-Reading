"""Restrict the handover hash layer to its owner-authorized explanations.

These checks validate preservation and bookkeeping. They do not establish the
scientific validity of prose or turn a document hash into a laboratory result.
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
    TABLE_CLEANUP_RECORD, _table_cleanup_hash,
    verify, HANDOVER_RECORD, HANDOVER_PATHS, HANDOVER_PREIMAGES,
    HANDOVER_BASE_COMMIT, HISTORICAL_LEDGER_SHA256, FOLLOWUP_RECORD,
    CHANGE_RECORD, DOCUMENT_RECORD, ORIGINAL_ARCHIVE_SHA256, _handover_hash,
    LAYOUT_RECORD, _layout_hash, MATH_APPROVAL_RECORD, _math_approval_hash,
)


class HandoverIntegrityTests(unittest.TestCase):
    def copy_root(self, directory):
        root = Path(directory)/'repo'
        shutil.copytree(ROOT, root,
                        ignore=shutil.ignore_patterns('.git', 'runs', '__pycache__'))
        return root

    def alter(self, root, change):
        path = root/HANDOVER_RECORD
        ledger = json.loads(path.read_text())
        change(ledger)
        path.write_text(json.dumps(ledger))

    def test_layer_is_exactly_the_authorized_seven_documents(self):
        self.assertEqual(HANDOVER_PATHS, frozenset({
            'README.md', 'CLAIM_STATUS.md', 'docs/PHYSICAL_SETTING.md',
            'docs/REPRODUCE.md', 'work_orders/CURRENT.md', 'docs/ROADMAP.md',
            'experiment/LAB_REVIEW.md',
        }))
        result = verify()
        self.assertEqual(set(result['authorized_handover_documents_verified']), HANDOVER_PATHS)
        self.assertFalse(result['mathematics_changed_by_handover'])
        self.assertTrue(result['source_archive_unchanged'])
        self.assertTrue(result['original_import_manifest_unchanged'])
        self.assertTrue(result['historical_change_ledgers_unchanged'])
        self.assertEqual(result['source_members'], 39)

    def test_visible_preimages_and_predecessor_chain(self):
        ledger = json.loads((ROOT/HANDOVER_RECORD).read_text())
        self.assertEqual(ledger['base_commit'], HANDOVER_BASE_COMMIT)
        self.assertEqual(ledger['previous_record'], FOLLOWUP_RECORD)
        self.assertEqual(ledger['previous_record_sha256'], HISTORICAL_LEDGER_SHA256[FOLLOWUP_RECORD])
        self.assertEqual(ledger['original_archive_sha256'], ORIGINAL_ARCHIVE_SHA256)
        layout = {entry['path']: entry for entry in
                  json.loads((ROOT/LAYOUT_RECORD).read_text())['changes']}
        math_approval = {entry['path']: entry for entry in
                         json.loads((ROOT/MATH_APPROVAL_RECORD).read_text())['changes']}
        table_cleanup = {entry['path']: entry for entry in
                         json.loads((ROOT/TABLE_CLEANUP_RECORD).read_text())['changes']}
        for entry in ledger['changes']:
            self.assertEqual(entry['old_sha256'], HANDOVER_PREIMAGES[entry['path']])
            # Old ledgers remain immutable. Every later authorized edit must
            # begin at its exact previous hash before reaching the current bytes.
            expected = _layout_hash(entry['path'], entry['new_sha256'], layout)
            expected = _math_approval_hash(entry['path'], expected, math_approval)
            expected = _table_cleanup_hash(entry['path'], expected, table_cleanup)
            self.assertEqual(expected, hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest())
        for path, expected in HISTORICAL_LEDGER_SHA256.items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), expected)

    def test_stale_baseline_hash_rejected_for_every_document(self):
        for path in HANDOVER_PATHS:
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                self.alter(root, lambda ledger: next(e for e in ledger['changes']
                    if e['path'] == path).update(old_sha256='0'*64))
                with self.assertRaisesRegex(ValueError, 'baseline hash mismatch'):
                    verify(root)

    def test_cannot_authorize_science_protocol_evidence_or_outside_paths(self):
        for path in ('src/theory.py', 'src/photon_support.py', 'proofs/THEORY.md',
                     'experiment/FIRST_EXPERIMENT.md', 'results/validation.json',
                     'provenance/IMPORT_MANIFEST.json', '../outside.md'):
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                self.alter(root, lambda ledger: ledger['changes'][0].update(path=path))
                with self.assertRaisesRegex(ValueError, 'authorized document set'):
                    verify(root)

    def test_missing_duplicate_and_added_paths_rejected(self):
        changes = (
            lambda ledger: ledger['changes'].pop(),
            lambda ledger: ledger['changes'].append(dict(ledger['changes'][0])),
            lambda ledger: ledger.update(additions=[{'path': 'src/new.py'}]),
        )
        for change in changes:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                self.alter(root, change)
                with self.assertRaisesRegex(ValueError, 'authorized document set'):
                    verify(root)

    def test_reason_must_be_nonempty_explanatory_text(self):
        for reason in ('', '   \n', None, False, ['authorized']):
            with self.subTest(reason=reason), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                self.alter(root, lambda ledger: ledger['changes'][0].update(reason=reason))
                with self.assertRaisesRegex(ValueError, 'reason is missing'):
                    verify(root)

    def test_invalid_hashes_rejected(self):
        for value in ('not-a-hash', 'F'*64, None, 123):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                self.alter(root, lambda ledger: ledger['changes'][0].update(new_sha256=value))
                with self.assertRaisesRegex(ValueError, 'Invalid handover documentation hash'):
                    verify(root)

    def test_contract_and_predecessor_cannot_be_retargeted(self):
        fields = {
            'schema': 2, 'interpretation_only': False,
            'original_archive_sha256': '0'*64, 'previous_record': DOCUMENT_RECORD,
            'previous_record_sha256': '0'*64, 'base_commit': '0'*40,
        }
        for field, value in fields.items():
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                self.alter(root, lambda ledger: ledger.update({field: value}))
                with self.assertRaisesRegex(ValueError, 'Invalid handover documentation ledger contract'):
                    verify(root)

    def test_unrecorded_new_document_bytes_rejected(self):
        for path in HANDOVER_PATHS:
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                with (root/path).open('a') as handle:
                    handle.write('\nUnrecorded alteration.\n')
                with self.assertRaisesRegex(ValueError, 'Protected .* changed'):
                    verify(root)

    def test_previous_hash_is_checked_at_each_existing_layer(self):
        path = 'CLAIM_STATUS.md'
        entry = {'old_sha256': HANDOVER_PREIMAGES[path], 'new_sha256': '1'*64}
        with self.assertRaisesRegex(ValueError, 'previous hash mismatch'):
            _handover_hash(path, '0'*64, {path: entry})
        self.assertEqual(_handover_hash(path, HANDOVER_PREIMAGES[path], {path: entry}), '1'*64)
        self.assertEqual(_handover_hash('src/theory.py', '2'*64, {path: entry}), '2'*64)

    def test_historical_reasons_cannot_be_rewritten(self):
        for path in HISTORICAL_LEDGER_SHA256:
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                ledger = json.loads((root/path).read_text())
                ledger['changes'][0]['reason'] = 'A different nonempty historical justification'
                (root/path).write_text(json.dumps(ledger))
                with self.assertRaisesRegex(ValueError, 'Historical change ledger changed'):
                    verify(root)

    def test_old_ledger_cannot_bless_new_numerical_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.copy_root(directory)
            path = root/'src/theory.py'
            path.write_text(path.read_text()+'\n# Unauthorized numerical-source alteration\n')
            ledger_path = root/CHANGE_RECORD
            ledger = json.loads(ledger_path.read_text())
            entry = next(e for e in ledger['changes'] if e['path'] == 'src/theory.py')
            entry['new_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
            ledger_path.write_text(json.dumps(ledger))
            with self.assertRaisesRegex(ValueError, 'Historical change ledger changed'):
                verify(root)

    def test_canonical_protocol_source_and_frozen_evidence_still_protected(self):
        for path in ('experiment/FIRST_EXPERIMENT.md', 'src/optics.py',
                     'proofs/THEORY.md', 'results/validation.json'):
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                root = self.copy_root(directory)
                (root/path).write_text('Unapproved replacement')
                with self.assertRaisesRegex(ValueError, 'Protected working file changed'):
                    verify(root)


if __name__ == '__main__':
    unittest.main()
