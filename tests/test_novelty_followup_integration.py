"""Follow-up attribution/evidence integration, not a new scientific proof audit."""
from __future__ import annotations
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from verify_import import verify, FOLLOWUP_RECORD, FOLLOWUP_PATHS, _git_blob

INTEGRATION = ROOT/'integrations/novelty-02'
AUDIT = ROOT/'audits/novelty-02'
ARCHIVE_HASH = 'ed819f672fb24f767a8545d7fb8517d907d4795608bcb0ba1ae9909136407e34'
ORIGINAL_LEDGER_BLOBS = {
    'provenance/changes/theory-repair-01.json': '5705ac27b572aafe1429774d2d51dc3b24853d28',
    'provenance/changes/novelty-integration-01.json': '8e05fabf874f448a757822043170c94e6d435085',
}


class NoveltyFollowupIntegrationTests(unittest.TestCase):
    def copy_root(self, directory):
        dest=Path(directory)/'repo'
        shutil.copytree(ROOT,dest,ignore=shutil.ignore_patterns('.git','runs','__pycache__'))
        return dest

    def test_new_layer_and_unchanged_old_ledgers(self):
        result=verify()
        self.assertEqual(set(result['authorized_followup_documents_verified']),FOLLOWUP_PATHS)
        self.assertFalse(result['mathematics_changed_by_followup'])
        for name, expected in ORIGINAL_LEDGER_BLOBS.items():
            self.assertEqual(_git_blob((ROOT/name).read_bytes()),expected)

    def test_stale_followup_preimages_rejected(self):
        for name in ('REPORT.md','docs/CONTRIBUTIONS.md'):
            with self.subTest(name=name),tempfile.TemporaryDirectory() as d:
                root=self.copy_root(d); p=root/FOLLOWUP_RECORD
                ledger=json.loads(p.read_text())
                next(e for e in ledger['changes'] if e['path']==name)['old_sha256']='0'*64
                p.write_text(json.dumps(ledger))
                with self.assertRaisesRegex(ValueError,'Follow-up documentation previous hash'):
                    verify(root)

    def test_followup_cannot_authorize_source_or_missing_paths(self):
        for replacement in ('src/theory.py','proofs/THEORY.md','../outside.md',None):
            with self.subTest(replacement=replacement),tempfile.TemporaryDirectory() as d:
                root=self.copy_root(d); p=root/FOLLOWUP_RECORD; ledger=json.loads(p.read_text())
                if replacement is None: ledger['changes'].pop()
                else: ledger['changes'][0]['path']=replacement
                p.write_text(json.dumps(ledger))
                with self.assertRaisesRegex(ValueError,'authorized document set'):verify(root)

    def test_duplicate_and_unjustified_followup_rejected(self):
        for kind in ('duplicate','addition','reason','hash'):
            with self.subTest(kind=kind),tempfile.TemporaryDirectory() as d:
                root=self.copy_root(d); p=root/FOLLOWUP_RECORD; ledger=json.loads(p.read_text())
                if kind=='duplicate':ledger['changes'].append(dict(ledger['changes'][0]))
                elif kind=='addition':ledger['additions']=[{'path':'src/new.py'}]
                elif kind=='reason':ledger['changes'][0]['reason']=''
                else:ledger['changes'][0]['new_sha256']='not-a-hash'
                p.write_text(json.dumps(ledger))
                with self.assertRaises(ValueError):verify(root)

    def test_followup_notes_are_protected(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.copy_root(d)
            (root/'experiment/REVIEW_RATIONALE.md').write_text('Unapproved change')
            with self.assertRaisesRegex(ValueError,'Protected documentation changed'):verify(root)

    def test_committed_audit_preserved(self):
        self.assertEqual(_git_blob((AUDIT/'MANIFEST.json').read_bytes()),
                         'd889598563c30b00f9175341946864e0db1c2d27')
        for name,expected in json.loads((AUDIT/'MANIFEST.json').read_text())['files'].items():
            self.assertEqual(hashlib.sha256((AUDIT/name).read_bytes()).hexdigest(),expected)

    def supplied_members(self):
        manifest=json.loads((INTEGRATION/'SUPPLIED_MANIFEST.json').read_text())
        data=(ROOT/manifest['archive']).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(),ARCHIVE_HASH)
        self.assertEqual(manifest['archive_sha256'],ARCHIVE_HASH)
        self.assertEqual(manifest['source_zip_sha256'],
                         'e0e6558b99d15451ed02388dee3a579e03b6f37dc906d87d7cec2287fcd6f557')
        with tarfile.open(ROOT/manifest['archive']) as t:
            members=t.getmembers()
            self.assertEqual(len(members),len(set(e.name for e in members)))
            self.assertEqual({e.name for e in members},set(manifest['members']))
            result={}
            for entry in members:
                self.assertTrue(entry.isfile())
                self.assertTrue(entry.name.startswith('audits/novelty-02/'))
                self.assertNotIn('..',Path(entry.name).parts)
                b=t.extractfile(entry).read()
                self.assertEqual(hashlib.sha256(b).hexdigest(),manifest['members'][entry.name])
                result[entry.name]=b
            return result

    def test_separate_supplied_packet_preserved(self):
        members=self.supplied_members()
        original=json.loads(members['audits/novelty-02/MANIFEST.json'])
        for name,expected in original['files'].items():
            # The supplied manifest uses paths relative to its audit directory.
            key=name if name.startswith('audits/') else 'audits/novelty-02/'+name
            self.assertEqual(hashlib.sha256(members[key]).hexdigest(),expected)

    def run_diagnostic(self, script, output):
        env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
        p=subprocess.run([sys.executable,str(script),'--output',str(output)],
                         capture_output=True,text=True,timeout=45,env=env)
        self.assertEqual(p.returncode,0,p.stdout+'\n'+p.stderr)
        return json.loads((output/'RESULTS.json').read_text())

    def compare_ledger(self,fresh,old,key):
        self.assertEqual(fresh['status'],'PASS')
        self.assertEqual(fresh['groups'],old['groups'])
        self.assertEqual([(x['group'],x['name'],x['tolerance']) for x in fresh[key]],
                         [(x['group'],x['name'],x['tolerance']) for x in old[key]])
        for item in fresh[key]:
            self.assertTrue(math.isfinite(item['residual']))
            self.assertGreaterEqual(item['residual'],0)
            self.assertLessEqual(item['residual'],item['tolerance'])

    def test_committed_572_comparisons(self):
        with tarfile.open(AUDIT/'EVIDENCE.tar.xz') as t:
            old=json.loads(t.extractfile('RESULTS.json').read())
        with tempfile.TemporaryDirectory() as d:
            fresh=self.run_diagnostic(AUDIT/'comparison_checks.py',Path(d)/'new-run')
        self.assertEqual(fresh['checks'],572)
        self.compare_ledger(fresh,old,'ledger')

    def test_supplied_717_comparisons(self):
        members=self.supplied_members()
        old=json.loads(members['audits/novelty-02/results/RESULTS.json'])
        with tempfile.TemporaryDirectory() as d:
            script=Path(d)/'check_equivalences.py'
            script.write_bytes(members['audits/novelty-02/check_equivalences.py'])
            fresh=self.run_diagnostic(script,Path(d)/'new-run')
        self.assertEqual(fresh['assertions'],717)
        self.assertEqual(fresh['case_counts'],old['case_counts'])
        self.compare_ledger(fresh,old,'checks')

    def test_corrected_hierarchy_and_resource_limits(self):
        readers=['README.md','CLAIM_STATUS.md','docs/CONTRIBUTIONS.md','SOURCE_AUDIT.md',
                 'experiment/REVIEW_RATIONALE.md','docs/ROADMAP.md','work_orders/CURRENT.md']
        for name in readers:
            text=(ROOT/name).read_text()
            with self.subTest(name=name):
                self.assertIn('A',text)
                self.assertIn('B',text)
                self.assertIn('derived',text)
                self.assertNotIn('two candidate additions',text)
        source=(ROOT/'SOURCE_AUDIT.md').read_text()
        for phrase in ('S20','S22','S08','finite-n','author-uploaded','conclusive-filter'):
            self.assertIn(phrase,source)
        note=(ROOT/'docs/CONTRIBUTIONS.md').read_text()
        for phrase in ('mean incident signal budget','arbitrarily\nrare bright pulses',
                       'occupied bypass rail','retained idler','not a manuscript or a priority clearance'):
            self.assertIn(phrase,note)
        self.assertIn('not a second independently new', (ROOT/'README.md').read_text())


if __name__=='__main__':unittest.main()
