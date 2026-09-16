"""Keep the new licensing authorization confined to the existing README notice."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from verify_import import (
    _final_handover_approvals, _final_handover_hash,
    verify, LICENSE_RECORD, LICENSE_README_PREIMAGE,
    _license_approval, _license_hash,
)


class LicenseIntegrationTests(unittest.TestCase):
    def test_exact_preimage_current_bytes_and_predecessor(self):
        entry = _license_approval(ROOT)
        self.assertEqual(entry['path'], 'README.md')
        self.assertEqual(entry['old_sha256'], LICENSE_README_PREIMAGE)
        final_handover, _ = _final_handover_approvals(ROOT)
        expected = _final_handover_hash('README.md', entry['new_sha256'], final_handover)
        self.assertEqual(expected, hashlib.sha256((ROOT/'README.md').read_bytes()).hexdigest())
        with self.assertRaisesRegex(ValueError, 'previous hash mismatch'):
            _license_hash('README.md', '0'*64, entry)
        self.assertEqual(_license_hash('src/theory.py', '1'*64, entry), '1'*64)
        result = verify()
        self.assertEqual(result['authorized_licensing_documents_verified'], ['README.md'])
        self.assertTrue(result['historical_change_ledgers_unchanged'])

    def test_scope_and_preimage_cannot_authorize_other_changes(self):
        mutations = [
            lambda x: x.update(license_only=False),
            lambda x: x.update(mathematical_content_changed=True),
            lambda x: x.update(base_commit='0'*40),
            lambda x: x.update(previous_record_sha256='0'*64),
            lambda x: x['changes'].clear(),
            lambda x: x['changes'].append(dict(x['changes'][0])),
            lambda x: x['changes'][0].update(path='proofs/THEORY.md'),
            lambda x: x.update(additions=[{'path': 'src/new.py'}]),
            lambda x: x['changes'][0].update(old_sha256='0'*64),
            lambda x: x['changes'][0].update(new_sha256='F'*64),
            lambda x: x['changes'][0].update(reason='   '),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = root/LICENSE_RECORD
            record.parent.mkdir(parents=True)
            for index, mutate in enumerate(mutations):
                with self.subTest(mutation=index):
                    ledger = json.loads((ROOT/LICENSE_RECORD).read_text())
                    mutate(ledger)
                    record.write_text(json.dumps(ledger))
                    with self.assertRaises(ValueError):
                        _license_approval(root)


if __name__ == '__main__':
    unittest.main()
