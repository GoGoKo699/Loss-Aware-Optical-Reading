"""Preserve the approved philosophy and the bounded math transport correction."""
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
    _license_approval, _license_hash,
    TABLE_CLEANUP_RECORD, _table_cleanup_hash,
    verify, MATH_APPROVAL_RECORD, MATH_APPROVAL_PATHS, MATH_APPROVAL_PREIMAGES,
    MATH_APPROVAL_BASE_COMMIT, MATH_APPROVAL_BASE_TREE, LAYOUT_RECORD,
    HISTORICAL_LEDGER_SHA256, _math_approval_approvals, _math_approval_hash,
)


class MathApprovalIntegrationTests(unittest.TestCase):
    def test_exact_authorized_chain_and_current_bytes(self):
        self.assertEqual(MATH_APPROVAL_PATHS, frozenset({
            'README.md', 'CLAIM_STATUS.md', 'docs/PHILOSOPHY_DRAFT.md',
            'docs/CONTRIBUTIONS.md', 'docs/THEORY_ROUTE.md',
        }))
        ledger = json.loads((ROOT/MATH_APPROVAL_RECORD).read_text())
        self.assertEqual(ledger['base_commit'], MATH_APPROVAL_BASE_COMMIT)
        self.assertEqual(ledger['base_tree'], MATH_APPROVAL_BASE_TREE)
        self.assertEqual(ledger['previous_record'], LAYOUT_RECORD)
        self.assertEqual(ledger['previous_record_sha256'], HISTORICAL_LEDGER_SHA256[LAYOUT_RECORD])
        table_cleanup = {entry['path']: entry for entry in
                         json.loads((ROOT/TABLE_CLEANUP_RECORD).read_text())['changes']}
        license_approval = _license_approval(ROOT)
        for entry in ledger['changes']:
            self.assertEqual(entry['old_sha256'], MATH_APPROVAL_PREIMAGES[entry['path']])
            expected = _table_cleanup_hash(entry['path'], entry['new_sha256'], table_cleanup)
            expected = _license_hash(entry['path'], expected, license_approval)
            self.assertEqual(expected,
                             hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest())
        result = verify()
        self.assertEqual(set(result['authorized_math_approval_documents_verified']), MATH_APPROVAL_PATHS)
        self.assertFalse(result['mathematics_changed_by_math_approval'])
        self.assertTrue(result['historical_change_ledgers_unchanged'])

    def test_contract_scope_and_preimages_cannot_be_retargeted(self):
        fields = {
            'schema': 2, 'interpretation_only': False, 'mathematical_content_changed': True,
            'base_commit': '0'*40, 'base_tree': '0'*40,
            'previous_record': 'elsewhere.json', 'previous_record_sha256': '0'*64,
            'original_archive_sha256': '0'*64,
        }
        mutations = [lambda ledger, k=k, v=v: ledger.update({k: v})
                     for k, v in fields.items()]
        mutations += [
            lambda ledger: ledger['changes'].pop(),
            lambda ledger: ledger['changes'].append(dict(ledger['changes'][0])),
            lambda ledger: ledger.update(additions=[{'path': 'src/new.py'}]),
            lambda ledger: ledger['changes'][0].update(path='proofs/THEORY.md'),
            lambda ledger: ledger['changes'][0].update(reason='   '),
            lambda ledger: ledger['changes'][0].update(new_sha256='F'*64),
        ]
        mutations += [lambda ledger, p=p: next(e for e in ledger['changes']
                      if e['path'] == p).update(old_sha256='0'*64)
                      for p in MATH_APPROVAL_PATHS]
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                record = root/MATH_APPROVAL_RECORD
                record.parent.mkdir(parents=True)
                ledger = json.loads((ROOT/MATH_APPROVAL_RECORD).read_text())
                mutate(ledger)
                record.write_text(json.dumps(ledger))
                with self.assertRaises(ValueError):
                    _math_approval_approvals(root)

    def test_unrecorded_document_changes_are_rejected(self):
        for path in MATH_APPROVAL_PATHS:
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)/'repo'
                shutil.copytree(ROOT, root,
                                ignore=shutil.ignore_patterns('.git', 'runs', '__pycache__'))
                with (root/path).open('a') as handle:
                    handle.write('\nUnrecorded change.\n')
                with self.assertRaisesRegex(ValueError, 'Protected .* changed'):
                    verify(root)

    def test_predecessor_hash_link_cannot_be_bypassed(self):
        path = 'README.md'
        entry = {'old_sha256': MATH_APPROVAL_PREIMAGES[path], 'new_sha256': '1'*64}
        with self.assertRaisesRegex(ValueError, 'previous hash mismatch'):
            _math_approval_hash(path, '0'*64, {path: entry})
        self.assertEqual(_math_approval_hash(path, MATH_APPROVAL_PREIMAGES[path], {path: entry}), '1'*64)
        self.assertEqual(_math_approval_hash('src/theory.py', '2'*64, {path: entry}), '2'*64)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)/'repo'
            shutil.copytree(ROOT, root,
                            ignore=shutil.ignore_patterns('.git', 'runs', '__pycache__'))
            record = root/LAYOUT_RECORD
            ledger = json.loads(record.read_text())
            next(e for e in ledger['changes'] if e['path'] == path)['new_sha256'] = '0'*64
            record.write_text(json.dumps(ledger))
            with self.assertRaisesRegex(ValueError, 'previous hash mismatch'):
                verify(root)


if __name__ == '__main__':
    unittest.main()
