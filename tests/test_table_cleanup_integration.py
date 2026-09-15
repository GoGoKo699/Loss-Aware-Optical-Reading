"""Bound the table/editorial revision without changing previous ledger bytes."""
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
    verify, TABLE_CLEANUP_RECORD, TABLE_CLEANUP_PATHS, TABLE_CLEANUP_PREIMAGES,
    TABLE_CLEANUP_BASE_COMMIT, TABLE_CLEANUP_BASE_TREE,
    _table_cleanup_approvals, _table_cleanup_hash,
)


class TableCleanupIntegrationTests(unittest.TestCase):
    def test_exact_scope_preimages_and_current_bytes(self):
        self.assertEqual(TABLE_CLEANUP_PATHS, frozenset({
            'CLAIM_STATUS.md', 'docs/PHILOSOPHY_DRAFT.md', 'docs/PHYSICAL_SETTING.md',
            'experiment/COMMISSIONING.md', 'experiment/SU4.md',
        }))
        ledger = json.loads((ROOT/TABLE_CLEANUP_RECORD).read_text())
        self.assertEqual(ledger['base_commit'], TABLE_CLEANUP_BASE_COMMIT)
        self.assertEqual(ledger['base_tree'], TABLE_CLEANUP_BASE_TREE)
        for entry in ledger['changes']:
            self.assertEqual(entry['old_sha256'], TABLE_CLEANUP_PREIMAGES[entry['path']])
            self.assertEqual(entry['new_sha256'],
                             hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest())
        result = verify()
        self.assertEqual(set(result['authorized_table_cleanup_documents_verified']), TABLE_CLEANUP_PATHS)
        self.assertFalse(result['mathematics_changed_by_table_cleanup'])
        self.assertTrue(result['historical_change_ledgers_unchanged'])

    def test_invalid_contract_scope_and_preimages_are_rejected(self):
        mutations = [
            lambda x: x.update(mathematical_content_changed=True),
            lambda x: x.update(base_commit='0'*40),
            lambda x: x.update(previous_record_sha256='0'*64),
            lambda x: x['changes'].pop(),
            lambda x: x['changes'].append(dict(x['changes'][0])),
            lambda x: x.update(additions=[{'path': 'src/new.py'}]),
            lambda x: x['changes'][0].update(path='proofs/THEORY.md'),
            lambda x: x['changes'][0].update(reason='   '),
            lambda x: x['changes'][0].update(new_sha256='F'*64),
        ]
        mutations += [lambda x, p=p: next(e for e in x['changes']
                      if e['path'] == p).update(old_sha256='0'*64)
                      for p in TABLE_CLEANUP_PATHS]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = root/TABLE_CLEANUP_RECORD
            record.parent.mkdir(parents=True)
            for index, mutate in enumerate(mutations):
                with self.subTest(mutation=index):
                    ledger = json.loads((ROOT/TABLE_CLEANUP_RECORD).read_text())
                    mutate(ledger)
                    record.write_text(json.dumps(ledger))
                    with self.assertRaises(ValueError):
                        _table_cleanup_approvals(root)

    def test_previous_hash_and_unrecorded_changes_are_rejected(self):
        path = 'docs/PHILOSOPHY_DRAFT.md'
        changes = {path: {'old_sha256': TABLE_CLEANUP_PREIMAGES[path], 'new_sha256': '1'*64}}
        with self.assertRaisesRegex(ValueError, 'previous hash mismatch'):
            _table_cleanup_hash(path, '0'*64, changes)
        self.assertEqual(_table_cleanup_hash('src/theory.py', '2'*64, changes), '2'*64)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)/'repo'
            shutil.copytree(ROOT, root,
                            ignore=shutil.ignore_patterns('.git', 'runs', '__pycache__'))
            for path in TABLE_CLEANUP_PATHS:
                with self.subTest(path=path):
                    target = root/path
                    original = target.read_bytes()
                    target.write_bytes(original+b'\nUnrecorded edit.\n')
                    with self.assertRaisesRegex(ValueError, 'Protected .* changed'):
                        verify(root)
                    target.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
