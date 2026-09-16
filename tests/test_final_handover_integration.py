"""Bound final reader repairs while preserving every scientific source and ledger."""
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
    verify, FINAL_HANDOVER_RECORD, FINAL_HANDOVER_PATHS, FINAL_HANDOVER_PREIMAGES,
    FINAL_HANDOVER_ADDITIONS, FINAL_HANDOVER_READER_SOURCES,
    FINAL_HANDOVER_BASE_COMMIT, FINAL_HANDOVER_BASE_TREE, LICENSE_RECORD,
    HISTORICAL_LEDGER_SHA256, _final_handover_approvals, _final_handover_hash,
)


class FinalHandoverIntegrationTests(unittest.TestCase):
    def test_exact_scope_preimages_sources_and_current_bytes(self):
        self.assertEqual(FINAL_HANDOVER_PATHS, frozenset({
            'README.md', 'REPORT.md', 'docs/ROBUSTNESS_GUIDE.md', 'docs/NUMERICAL_CONTRACT.md',
        }))
        self.assertEqual(FINAL_HANDOVER_ADDITIONS, frozenset({
            'docs/ROBUSTNESS_REPORT.md', 'docs/ROBUSTNESS_PROOFS.md', 'docs/NUMERICAL_PROOF.md',
        }))
        ledger = json.loads((ROOT/FINAL_HANDOVER_RECORD).read_text())
        self.assertEqual(ledger['base_commit'], FINAL_HANDOVER_BASE_COMMIT)
        self.assertEqual(ledger['base_tree'], FINAL_HANDOVER_BASE_TREE)
        self.assertEqual(ledger['previous_record'], LICENSE_RECORD)
        self.assertEqual(ledger['previous_record_sha256'], HISTORICAL_LEDGER_SHA256[LICENSE_RECORD])
        changes, additions = _final_handover_approvals(ROOT)
        for path, entry in changes.items():
            self.assertEqual(entry['old_sha256'], FINAL_HANDOVER_PREIMAGES[path])
            self.assertEqual(entry['new_sha256'], hashlib.sha256((ROOT/path).read_bytes()).hexdigest())
        for path, entry in additions.items():
            self.assertEqual((entry['source_path'], entry['source_sha256']),
                             FINAL_HANDOVER_READER_SOURCES[path])
            self.assertEqual(entry['source_sha256'],
                             hashlib.sha256((ROOT/entry['source_path']).read_bytes()).hexdigest())
            self.assertEqual(entry['sha256'], hashlib.sha256((ROOT/path).read_bytes()).hexdigest())
        self.assertEqual(len(HISTORICAL_LEDGER_SHA256), 8)
        for path, expected in HISTORICAL_LEDGER_SHA256.items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), expected)
        result = verify()
        self.assertEqual(set(result['authorized_final_handover_documents_verified']), FINAL_HANDOVER_PATHS)
        self.assertEqual(set(result['authorized_reader_copies_verified']), FINAL_HANDOVER_ADDITIONS)
        self.assertFalse(result['mathematics_changed_by_final_handover'])
        self.assertTrue(result['reader_source_documents_unchanged'])
        self.assertTrue(result['historical_change_ledgers_unchanged'])

    def test_invalid_contract_scope_preimages_and_sources_are_rejected(self):
        mutations = [
            lambda x: x.update(schema=2),
            lambda x: x.update(interpretation_only=False),
            lambda x: x.update(mathematical_content_changed=True),
            lambda x: x.update(base_commit='0'*40),
            lambda x: x.update(base_tree='0'*40),
            lambda x: x.update(original_archive_sha256='0'*64),
            lambda x: x.update(previous_record='provenance/changes/table-cleanup-04.json'),
            lambda x: x.update(previous_record_sha256='0'*64),
            lambda x: x['changes'].pop(),
            lambda x: x['changes'].append(dict(x['changes'][0])),
            lambda x: x['additions'].pop(),
            lambda x: x['additions'].append(dict(x['additions'][0])),
            lambda x: x['changes'][0].update(reason='   '),
            lambda x: x['changes'][0].update(new_sha256='F'*64),
            lambda x: x['additions'][0].update(reason=None),
            lambda x: x['additions'][0].update(sha256='not-a-hash'),
            lambda x: x['additions'][0].update(source_sha256='0'*64),
            lambda x: x['additions'][0].update(source_path='studies/robustness-01/study.py'),
        ]
        mutations += [lambda x, p=p: next(e for e in x['changes']
                      if e['path'] == p).update(old_sha256='0'*64)
                      for p in FINAL_HANDOVER_PATHS]
        for field in ('changes', 'additions'):
            for path in ('src/theory.py', 'proofs/THEORY.md', 'results/validation.json',
                         'studies/robustness-01/PROOFS.md', 'repairs/theory-01/NUMERICAL_PROOF.md',
                         'experiment/FIRST_EXPERIMENT.md', '../outside.md'):
                mutations.append(lambda x, f=field, p=path: x[f][0].update(path=p))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = root/FINAL_HANDOVER_RECORD
            record.parent.mkdir(parents=True)
            for index, mutate in enumerate(mutations):
                with self.subTest(mutation=index):
                    ledger = json.loads((ROOT/FINAL_HANDOVER_RECORD).read_text())
                    mutate(ledger)
                    record.write_text(json.dumps(ledger))
                    with self.assertRaises(ValueError):
                        _final_handover_approvals(root)

    def test_final_layer_requires_exact_previous_hash(self):
        path = 'README.md'
        changes = {path: {'old_sha256': FINAL_HANDOVER_PREIMAGES[path], 'new_sha256': '1'*64}}
        with self.assertRaisesRegex(ValueError, 'previous hash mismatch'):
            _final_handover_hash(path, '0'*64, changes)
        self.assertEqual(_final_handover_hash(path, FINAL_HANDOVER_PREIMAGES[path], changes), '1'*64)
        self.assertEqual(_final_handover_hash('src/theory.py', '2'*64, changes), '2'*64)

    def test_unrecorded_current_documents_and_frozen_sources_are_rejected(self):
        paths = FINAL_HANDOVER_PATHS | FINAL_HANDOVER_ADDITIONS | {
            source for source, _ in FINAL_HANDOVER_READER_SOURCES.values()}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)/'repo'
            shutil.copytree(ROOT, root,
                            ignore=shutil.ignore_patterns('.git', 'runs', '__pycache__'))
            for path in paths:
                with self.subTest(path=path):
                    target = root/path
                    original = target.read_bytes()
                    target.write_bytes(original+b'\nUnrecorded edit.\n')
                    with self.assertRaisesRegex(ValueError, '(Protected .*|Frozen reader source) changed'):
                        verify(root)
                    target.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
