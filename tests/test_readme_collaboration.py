"""Limit the collaboration amendment to one notice, preserving the whole README."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from verify_import import (
    COLLABORATION_RECORD, COLLABORATION_NOTICE, COLLABORATION_README_PREIMAGE,
    COLLABORATION_PREVIOUS_BLOB, FINAL_HANDOVER_RECORD,
    _collaboration_amendment, _final_handover_approvals, _git_blob,
)


class ReadmeCollaborationTests(unittest.TestCase):
    def fixture(self, root):
        for path in ('README.md', COLLABORATION_RECORD, FINAL_HANDOVER_RECORD):
            target = root/path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT/path).read_bytes())
        record = json.loads((root/FINAL_HANDOVER_RECORD).read_text())
        return {entry['path']: entry for entry in record['changes']}

    def test_exact_insertion_and_immutable_predecessor(self):
        current = (ROOT/'README.md').read_bytes()
        notice = COLLABORATION_NOTICE.encode('utf-8')
        self.assertEqual(current.count(notice), 1)
        self.assertEqual(hashlib.sha256(current.replace(notice, b'', 1)).hexdigest(),
                         COLLABORATION_README_PREIMAGE)
        self.assertIn(b'**Experimental validation is still pending.**', notice)
        self.assertIn(b'[gogoko699@gmail.com](mailto:gogoko699@gmail.com)', notice)
        self.assertLess(current.index(notice), current.index(b'## From hardware'))
        self.assertEqual(_git_blob((ROOT/FINAL_HANDOVER_RECORD).read_bytes()),
                         COLLABORATION_PREVIOUS_BLOB)
        original = json.loads((ROOT/FINAL_HANDOVER_RECORD).read_text())
        before = {entry['path']: entry for entry in original['changes']}
        frozen = copy.deepcopy(before)
        after = _collaboration_amendment(ROOT, before)
        self.assertEqual(before, frozen)
        self.assertEqual(after.keys(), before.keys())
        for path in before:
            expected = dict(before[path])
            if path == 'README.md':
                expected['new_sha256'] = hashlib.sha256(current).hexdigest()
            self.assertEqual(after[path], expected)
        effective, additions = _final_handover_approvals(ROOT)
        self.assertEqual(effective, after)
        self.assertEqual(len(additions), 3)

    def test_bad_ledger_cannot_authorize_other_paths_or_preimages(self):
        mutations = [
            lambda x: x.update(schema=2),
            lambda x: x.update(interpretation_only=False),
            lambda x: x.update(mathematical_content_changed=True),
            lambda x: x.update(base_commit='0'*40),
            lambda x: x.update(base_tree='0'*40),
            lambda x: x.update(previous_record='elsewhere.json'),
            lambda x: x.update(previous_record_git_blob='0'*40),
            lambda x: x['changes'].clear(),
            lambda x: x['changes'].append(dict(x['changes'][0])),
            lambda x: x['changes'][0].update(path='src/theory.py'),
            lambda x: x['changes'][0].update(path='../README.md'),
            lambda x: x.update(additions=[{'path':'proofs/extra.md'}]),
            lambda x: x['changes'][0].update(old_sha256='0'*64),
            lambda x: x['changes'][0].update(new_sha256='G'*64),
            lambda x: x['changes'][0].update(reason=' '),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before = self.fixture(root)
            original = json.loads((root/COLLABORATION_RECORD).read_text())
            for i, mutate in enumerate(mutations):
                with self.subTest(mutation=i):
                    ledger = copy.deepcopy(original)
                    mutate(ledger)
                    (root/COLLABORATION_RECORD).write_text(json.dumps(ledger))
                    with self.assertRaises(ValueError):
                        _collaboration_amendment(root, before)

    def test_rehashing_cannot_hide_any_other_readme_edit(self):
        notice = COLLABORATION_NOTICE.encode('utf-8')
        mutations = [
            lambda b: b+b'\nUnrecorded edit.\n',
            lambda b: b.replace(b'No laboratory data have been acquired here.',
                                b'Experimental advantage has been observed.'),
            lambda b: b.replace(notice, b'', 1),
            lambda b: b.replace(notice, notice+notice, 1),
            lambda b: b.replace(notice, b'', 1)+notice,
            lambda b: b.replace(b'gogoko699@gmail.com', b'other@example.com'),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before = self.fixture(root)
            original = (root/'README.md').read_bytes()
            record = json.loads((root/COLLABORATION_RECORD).read_text())
            for i, mutate in enumerate(mutations):
                with self.subTest(mutation=i):
                    changed = mutate(original)
                    (root/'README.md').write_bytes(changed)
                    ledger = copy.deepcopy(record)
                    ledger['changes'][0]['new_sha256'] = hashlib.sha256(changed).hexdigest()
                    (root/COLLABORATION_RECORD).write_text(json.dumps(ledger))
                    with self.assertRaisesRegex(ValueError, 'Protected collaboration document changed'):
                        _collaboration_amendment(root, before)

    def test_changed_history_or_disconnected_chain_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before = self.fixture(root)
            before['README.md']['new_sha256'] = '0'*64
            with self.assertRaisesRegex(ValueError, 'previous hash mismatch'):
                _collaboration_amendment(root, before)
            before = self.fixture(root)
            (root/FINAL_HANDOVER_RECORD).write_bytes(
                (root/FINAL_HANDOVER_RECORD).read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError, 'ledger contract'):
                _collaboration_amendment(root, before)


if __name__ == '__main__':
    unittest.main()
