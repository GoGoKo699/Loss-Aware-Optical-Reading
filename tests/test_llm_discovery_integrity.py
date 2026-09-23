"""Test the bounded navigation addition without rewriting historical approvals."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from verify_import import (
    sha, _git_blob, _llm_discovery_approval, _final_handover_approvals,
    _final_handover_hash, FINAL_HANDOVER_RECORD, FINAL_HANDOVER_PREIMAGES,
    FINAL_HANDOVER_LEDGER_SHA256, FINAL_HANDOVER_LEDGER_GIT_BLOB,
    LLM_DISCOVERY_RECORD, LLM_DISCOVERY_PREVIOUS_README,
    LLM_DISCOVERY_MAIN_README, LLM_DISCOVERY_README, LLM_DISCOVERY_GUIDE,
    LLM_DISCOVERY_AI_APPEND, LLM_DISCOVERY_OWNER_FOOTER, LLM_DISCOVERY_OLD_FOOTER,
)


class LLMDiscoveryIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        for name in ('README.md', 'llms.txt', FINAL_HANDOVER_RECORD, LLM_DISCOVERY_RECORD):
            target = self.root/name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/name, target)

    def write_ledger(self, data):
        (self.root/LLM_DISCOVERY_RECORD).write_text(json.dumps(data))

    def ledger(self):
        return json.loads((ROOT/LLM_DISCOVERY_RECORD).read_text())

    def test_exact_two_stage_readme_reconstruction(self):
        current = (self.root/'README.md').read_bytes()
        self.assertEqual(sha(current), LLM_DISCOVERY_README)
        self.assertTrue(current.endswith(LLM_DISCOVERY_AI_APPEND))
        observed = current[:-len(LLM_DISCOVERY_AI_APPEND)]
        self.assertEqual(sha(observed), LLM_DISCOVERY_MAIN_README)
        self.assertTrue(observed.endswith(LLM_DISCOVERY_OWNER_FOOTER))
        historical = observed[:-len(LLM_DISCOVERY_OWNER_FOOTER)] + LLM_DISCOVERY_OLD_FOOTER
        self.assertEqual(sha(historical), LLM_DISCOVERY_PREVIOUS_README)
        self.assertEqual(sha((self.root/'llms.txt').read_bytes()), LLM_DISCOVERY_GUIDE)
        self.assertEqual(_llm_discovery_approval(self.root), self.ledger()['changes'][0])

    def test_effective_endpoint_preserves_original_old_hashes_and_ledger(self):
        before = (self.root/FINAL_HANDOVER_RECORD).read_bytes()
        self.assertEqual(sha(before), FINAL_HANDOVER_LEDGER_SHA256)
        self.assertEqual(_git_blob(before), FINAL_HANDOVER_LEDGER_GIT_BLOB)
        historical = json.loads(before)
        changes, additions = _final_handover_approvals(self.root)
        for old in historical['changes']:
            effective = changes[old['path']]
            self.assertEqual(effective['old_sha256'], old['old_sha256'])
            self.assertEqual(effective['reason'], old['reason'])
            if old['path'] == 'README.md':
                self.assertEqual(old['new_sha256'], LLM_DISCOVERY_PREVIOUS_README)
                self.assertEqual(effective['new_sha256'], LLM_DISCOVERY_README)
            else:
                self.assertEqual(effective, old)
        self.assertEqual(additions, {e['path']: e for e in historical['additions']})
        self.assertEqual((self.root/FINAL_HANDOVER_RECORD).read_bytes(), before)
        self.assertEqual(_final_handover_hash('README.md',
                         FINAL_HANDOVER_PREIMAGES['README.md'], changes), LLM_DISCOVERY_README)
        with self.assertRaisesRegex(ValueError, 'previous hash mismatch'):
            _final_handover_hash('README.md', '0'*64, changes)

    def test_invalid_contract_or_expanded_scope_is_rejected(self):
        mutations = [
            lambda x: x.update(schema=2),
            lambda x: x.update(navigation_only=False),
            lambda x: x.update(mathematical_content_changed=True),
            lambda x: x.update(base_commit='0'*40),
            lambda x: x.update(base_tree='0'*40),
            lambda x: x.update(original_archive_sha256='0'*64),
            lambda x: x.update(previous_record='provenance/changes/license-01.json'),
            lambda x: x.update(previous_record_sha256='0'*64),
            lambda x: x.update(previous_record_git_blob='0'*40),
            lambda x: x['changes'].append(dict(x['changes'][0])),
            lambda x: x['changes'].clear(),
            lambda x: x['additions'].append(dict(x['additions'][0])),
            lambda x: x['additions'].clear(),
            lambda x: x['changes'][0].update(reason=' '),
            lambda x: x['additions'][0].update(reason=None),
        ]
        for key in ('old_sha256', 'observed_main_sha256', 'new_sha256'):
            mutations.append(lambda x, k=key: x['changes'][0].update({k: '0'*64}))
        mutations.append(lambda x: x['additions'][0].update(sha256='0'*64))
        for section in ('changes', 'additions'):
            for path in ('src/theory.py', 'proofs/THEORY.md', '../outside.md'):
                mutations.append(lambda x, s=section, p=path: x[s][0].update(path=p))
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                data = self.ledger()
                mutate(data)
                self.write_ledger(data)
                with self.assertRaises(ValueError):
                    _llm_discovery_approval(self.root)

    def test_unrelated_readme_edit_is_rejected_with_original_or_updated_hash(self):
        target = self.root/'README.md'
        target.write_bytes(target.read_bytes().replace(b'C+E+F=1', b'C+E+F=2', 1))
        with self.assertRaisesRegex(ValueError, 'Protected handover document changed'):
            _llm_discovery_approval(self.root)
        data = self.ledger()
        data['changes'][0]['new_sha256'] = sha(target.read_bytes())
        data['changes'][0]['observed_main_sha256'] = sha(
            target.read_bytes()[:-len(LLM_DISCOVERY_AI_APPEND)])
        self.write_ledger(data)
        with self.assertRaisesRegex(ValueError, 'endpoint hash mismatch'):
            _llm_discovery_approval(self.root)

    def test_owner_footer_and_ai_append_cannot_be_replaced_or_removed(self):
        target = self.root/'README.md'
        original = target.read_bytes()
        variants = [
            original[:-len(LLM_DISCOVERY_AI_APPEND)],
            original+b'\nOther unrecorded section.\n',
            original.replace(b'Experimental validation is still pending.',
                             b'Experimental validation is complete.'),
            original.replace(LLM_DISCOVERY_OWNER_FOOTER, LLM_DISCOVERY_OLD_FOOTER),
        ]
        for current in variants:
            target.write_bytes(current)
            with self.subTest(hash=sha(current)):
                with self.assertRaisesRegex(ValueError, 'Protected handover document changed'):
                    _llm_discovery_approval(self.root)

    def test_guide_edit_is_rejected_even_if_ledger_hash_is_updated(self):
        target = self.root/'llms.txt'
        target.write_bytes(target.read_bytes()+b'\nUnsupported scientific claim.\n')
        with self.assertRaisesRegex(ValueError, 'Protected LLM navigation guide changed'):
            _llm_discovery_approval(self.root)
        data = self.ledger()
        data['additions'][0]['sha256'] = sha(target.read_bytes())
        self.write_ledger(data)
        with self.assertRaisesRegex(ValueError, 'endpoint hash mismatch'):
            _llm_discovery_approval(self.root)

    def test_predecessor_ledger_cannot_be_refreshed(self):
        target = self.root/FINAL_HANDOVER_RECORD
        original = target.read_bytes()
        target.write_bytes(original+b'\n')
        data = self.ledger()
        data['previous_record_sha256'] = sha(target.read_bytes())
        data['previous_record_git_blob'] = _git_blob(target.read_bytes())
        self.write_ledger(data)
        with self.assertRaisesRegex(ValueError, 'Historical final-handover ledger changed'):
            _llm_discovery_approval(self.root)


if __name__ == '__main__':
    unittest.main()
