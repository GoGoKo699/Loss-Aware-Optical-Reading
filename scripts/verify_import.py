"""Verify frozen import bytes and explicit repair/documentation hash chains.

The original import manifest and ZIP remain immutable. Documentation integration
cannot authorize a numerical-source or proof change. Unknown edits are rejected.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_ARCHIVE_SHA256 = 'e2bd57686376549342881a5d0348b16820ebbdab094b8d72df05a6836dbad016'
ORIGINAL_MANIFEST_GIT_BLOB = '5756ee7d295229db370f0da98af19fc890e178ef'
CHANGE_RECORD = 'provenance/changes/theory-repair-01.json'
DOCUMENT_RECORD = 'provenance/changes/novelty-integration-01.json'
DOCUMENT_PATHS = frozenset({'CLAIM_STATUS.md', 'SOURCE_AUDIT.md', 'REPORT.md',
                            'experiment/LAB_REVIEW.md'})
DOCUMENT_ADDITIONS = frozenset({'docs/CONTRIBUTIONS.md', 'experiment/REVIEW_RATIONALE.md'})


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def _safe_path(root: Path, relative: str) -> Path:
    path = (root/relative).resolve()
    if root.resolve() not in path.parents:
        raise ValueError('Change ledger path escapes repository: '+relative)
    return path


def _document_approvals(root: Path) -> tuple[dict, dict]:
    ledger = json.loads((root/DOCUMENT_RECORD).read_text())
    if (ledger.get('schema') != 1 or ledger.get('interpretation_only') is not True or
        ledger.get('original_archive_sha256') != ORIGINAL_ARCHIVE_SHA256 or
        ledger.get('previous_record') != CHANGE_RECORD or
        ledger.get('base_commit') != '80c73751806f45411251711bcfb6bccebc887f0a' or
        ledger.get('audit_commit') != 'eaa452615096cca9a498c10c5d492a2a74966123'):
        raise ValueError('Invalid documentation ledger contract')
    changes = {e['path']: e for e in ledger['changes']}
    additions = {e['path']: e for e in ledger['additions']}
    if (len(changes) != len(ledger['changes']) or len(additions) != len(ledger['additions']) or
        changes.keys() != DOCUMENT_PATHS or additions.keys() != DOCUMENT_ADDITIONS):
        raise ValueError('Documentation ledger path set is not the authorized document set')
    for entry in list(changes.values()) + list(additions.values()):
        if not entry.get('reason'):
            raise ValueError('Documentation ledger reason is missing')
    return changes, additions


def verify(root: Path = ROOT) -> dict:
    manifest_bytes = (root/'provenance/IMPORT_MANIFEST.json').read_bytes()
    if _git_blob(manifest_bytes) != ORIGINAL_MANIFEST_GIT_BLOB:
        raise ValueError('Original import manifest changed')
    manifest = json.loads(manifest_bytes)
    archive = root/manifest['archive']
    if manifest['archive_sha256'] != ORIGINAL_ARCHIVE_SHA256 or sha(archive.read_bytes()) != ORIGINAL_ARCHIVE_SHA256:
        raise ValueError('Original checkpoint archive changed')
    ledger = json.loads((root/CHANGE_RECORD).read_text())
    if ledger['original_archive_sha256'] != ORIGINAL_ARCHIVE_SHA256:
        raise ValueError('Repair ledger does not refer to the original archive')
    changes = {e['path']:e for e in ledger['changes']}
    additions = {e['path']:e for e in ledger['additions']}
    if len(changes) != len(ledger['changes']) or len(additions) != len(ledger['additions']):
        raise ValueError('Duplicate repair ledger path')
    installed = {e['path']:e for e in manifest['files']}
    if len(installed) != len(manifest['files']) or not changes.keys() <= installed.keys():
        raise ValueError('Repair ledger changes an unknown imported path')
    if additions.keys() & installed.keys() or additions.keys() & changes.keys():
        raise ValueError('Added source path collides with the import')
    document_changes, document_additions = _document_approvals(root)
    if document_additions.keys() & (installed.keys() | additions.keys()):
        raise ValueError('Documentation addition collides with protected source')
    sources = [e['source'] for e in manifest['files']]
    if len(sources) != len(set(sources)):
        raise ValueError('Duplicate source member')
    count = 0
    with zipfile.ZipFile(archive) as z:
        members = [n for n in z.namelist() if not n.endswith('/')]
        if sorted(members) != sorted('photonic_single_photon_checkpoint_07/'+n for n in sources):
            raise ValueError('Import manifest does not cover the complete archive')
        for entry in manifest['files']:
            name = entry['source']
            old = z.read('photonic_single_photon_checkpoint_07/'+name)
            current = _safe_path(root,entry['path']).read_bytes()
            if sha(old) != entry['source_sha256']:
                raise ValueError('Source manifest mismatch: '+name)
            approved = changes.get(entry['path'])
            expected = entry['installed_sha256']
            if approved is not None:
                if approved['old_sha256'] != expected or not approved['reason']:
                    raise ValueError('Repair ledger previous hash/reason mismatch: '+name)
                expected = approved['new_sha256']
            document = document_changes.get(entry['path'])
            if document is not None:
                if document['old_sha256'] != expected:
                    raise ValueError('Documentation ledger previous hash mismatch: '+name)
                expected = document['new_sha256']
            if sha(current) != expected:
                raise ValueError('Protected working file changed: '+entry['path'])
            if approved is None and document is None:
                if name == 'src/validate.py':
                    anchor = b'RNG=np.random.default_rng(2026091417)'
                    if old.split(anchor,1)[1] != current.split(anchor,1)[1]:
                        raise ValueError('Unapproved validation mathematics change')
                elif old != current:
                    raise ValueError('Non-permitted migration difference: '+name)
            count += 1
    for path, entry in additions.items():
        if sha(_safe_path(root,path).read_bytes()) != entry['sha256']:
            raise ValueError('Protected added file changed: '+path)
    for path, entry in document_additions.items():
        if sha(_safe_path(root,path).read_bytes()) != entry['sha256']:
            raise ValueError('Protected documentation changed: '+path)
    return {'status':'PASS','source_members':count,'archive_sha256':ORIGINAL_ARCHIVE_SHA256,
            'source_archive_unchanged':True,'original_import_manifest_unchanged':True,
            'scientific_content_unchanged':not changes,
            'authorized_changes_verified':sorted(changes),
            'authorized_additions_verified':sorted(additions),
            'change_record':CHANGE_RECORD,
            'document_change_record':DOCUMENT_RECORD,
            'authorized_document_changes_verified':sorted(document_changes),
            'authorized_document_additions_verified':sorted(document_additions),
            'validator_change':'original I/O guard; approved numerical-method metadata update only'}


if __name__ == '__main__':
    print(json.dumps(verify(),indent=2))
