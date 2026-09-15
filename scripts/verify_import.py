"""Verify frozen import bytes and explicit repair/documentation hash chains.

Original archives and old ledgers are immutable. Each new document layer must
match its predecessor hash and cannot authorize numerical-source/proof changes.
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
FOLLOWUP_RECORD = 'provenance/changes/novelty-integration-02.json'
FOLLOWUP_PATHS = DOCUMENT_PATHS | DOCUMENT_ADDITIONS
HANDOVER_RECORD = 'provenance/changes/lab-handover-01.json'
HANDOVER_BASE_COMMIT = 'de73c9b094036b756d1ff008eaccbc52cec46207'
# Exact bytes read with git show at the owner's verified handover baseline.
# This allowlist is deliberately document-only. A new numerical module, proof,
# protocol, source archive, or result cannot be authorized through this layer.
HANDOVER_PREIMAGES = {
    'README.md': '5665bb7a14c0db3448600b17ab1c29f05920aae126103e13194b921890225efe',
    'CLAIM_STATUS.md': '20896a2e7a613bd997b77bde7dea25f140b1762c6eeaf84c965401048ecd7116',
    'docs/PHYSICAL_SETTING.md': 'd2fbb932a6436ce90f942b030b92f20d36f6dda63b568d7672678289890313ab',
    'docs/REPRODUCE.md': '829246ef60b6681dbfdbd5ec3cc0e2b41298b46499ec0a017579a775e1fb568f',
    'work_orders/CURRENT.md': 'fe6a277cfc4a1830385e08ddc1c1e16d4c2bf67aa0ad03d77d53a3b35684ac5e',
    'docs/ROADMAP.md': '9977d3130167188f6d6b5ebceec2415120a60481b07708b08ab54b2229120b50',
    'experiment/LAB_REVIEW.md': 'ccd011603280c3fb1bee7b9a53e1f0a14431ba52f89262719bbe2269b181750f',
}
HANDOVER_PATHS = frozenset(HANDOVER_PREIMAGES)
LAYOUT_RECORD = 'provenance/changes/layout-motivation-02.json'
LAYOUT_BASE_COMMIT = '1b0a79073050766f12317f27a0b0e9260896b90f'
LAYOUT_BASE_TREE = '0bf473a570347441887953505483b94149f7d44e'
# Pinned bytes at the merged handover. This follow-up only repairs presentation
# and gives the experiments a self-contained, conditional publication motivation.
LAYOUT_PREIMAGES = {
    'README.md': 'b7b9110f28af13e3bf1eaa030ec3a79c522000857554b3b2c89ef76f2419cf2d',
    'docs/CONTRIBUTIONS.md': 'd7f8b22cbe104c682108307598be028b7b127aaddf8b2fe9be62afe84e90a5fa',
    'docs/THEORY_ROUTE.md': '23782cf35b99a9183258c2f4f3deb44e1d720a64580d9f87171461b866434612',
    'docs/PHILOSOPHY_DRAFT.md': 'd5f4f02db38c086f54bbe49f2608f80a7bc820e5c3de7e888c2d0979da69e16c',
    'docs/ROBUSTNESS_GUIDE.md': '8bbbe30e151c99559baa14247de0d7639136a0eb56199a94911575c98abaa9a6',
    'experiment/M1.md': '27011acc7b043323792426c822848c0cb45becc54d4e76681fe95b38f470f741',
    'experiment/P1.md': '81a4b4a4515c48e446ffc3d9cb65a08cb73797e8f71ce7fd9ed2d5e37fb998b8',
    'experiment/P2.md': 'd5e70d47039930e7b7f9f39c5704a8306353b5e11112ce8b1de661ddda9d9f64',
    'experiment/SU4.md': '2357cc9550d53cd3c953da2e36ea67399840b307cb6128522cc638f796aeca2d',
    'experiment/SU8.md': '3e01a031233afd52c1cbb9bde47bde662c68787a9fb51cd29809e4b5c5ca77bf',
}
LAYOUT_PATHS = frozenset(LAYOUT_PREIMAGES)
HISTORICAL_LEDGER_SHA256 = {
    CHANGE_RECORD: 'a4b1f7eb9ec25d8ba737de30abc7ea787dd25eaeb15289207d191c2cd20c6c10',
    DOCUMENT_RECORD: '9cc64044ccfdf2bc38a3900e8141089a383bd116d7ff259c729cffe47afa2b29',
    FOLLOWUP_RECORD: 'f363b6343ce93093f6f5474ea4e1c4aca7c8d5d80a943f1aafb865346efb857d',
    HANDOVER_RECORD: '763adbbd6e003aee1a03e380fa9436c7e761e31c458e845327582e81fce984fa',
}


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


def _followup_approvals(root: Path) -> dict:
    """Accept exactly the six existing documents, never code or new paths."""
    ledger = json.loads((root/FOLLOWUP_RECORD).read_text())
    if (ledger.get('schema') != 1 or ledger.get('interpretation_only') is not True or
        ledger.get('original_archive_sha256') != ORIGINAL_ARCHIVE_SHA256 or
        ledger.get('previous_record') != DOCUMENT_RECORD or
        ledger.get('base_commit') != 'db17e1ec1868107b0fe1042d5a480769b552633e' or
        ledger.get('audit_commit') != 'ca0480eec0064dbcdf50ff3d60032022deff5d3c'):
        raise ValueError('Invalid follow-up documentation ledger contract')
    entries = ledger.get('changes', [])
    changes = {e['path']: e for e in entries}
    if (len(changes) != len(entries) or changes.keys() != FOLLOWUP_PATHS or
        ledger.get('additions')):
        raise ValueError('Follow-up ledger is not the authorized document set')
    for entry in entries:
        if not entry.get('reason'):
            raise ValueError('Follow-up documentation reason is missing')
        for key in ('old_sha256', 'new_sha256'):
            value = entry.get(key)
            if (not isinstance(value, str) or len(value) != 64 or
                any(c not in '0123456789abcdef' for c in value)):
                raise ValueError('Invalid follow-up documentation hash')
    return changes


def _followup_hash(path: str, expected: str, changes: dict) -> str:
    entry = changes.get(path)
    if entry is None:
        return expected
    if entry['old_sha256'] != expected:
        raise ValueError('Follow-up documentation previous hash mismatch: '+path)
    return entry['new_sha256']


def _handover_approvals(root: Path) -> dict:
    """Authorize exactly seven named explanations, with pinned old bytes."""
    ledger = json.loads((root/HANDOVER_RECORD).read_text())
    if (ledger.get('schema') != 1 or ledger.get('interpretation_only') is not True or
        ledger.get('original_archive_sha256') != ORIGINAL_ARCHIVE_SHA256 or
        ledger.get('previous_record') != FOLLOWUP_RECORD or
        ledger.get('previous_record_sha256') != HISTORICAL_LEDGER_SHA256[FOLLOWUP_RECORD] or
        ledger.get('base_commit') != HANDOVER_BASE_COMMIT):
        raise ValueError('Invalid handover documentation ledger contract')
    entries = ledger.get('changes', [])
    changes = {entry['path']: entry for entry in entries}
    if (len(changes) != len(entries) or changes.keys() != HANDOVER_PATHS or
        ledger.get('additions')):
        raise ValueError('Handover ledger is not the authorized document set')
    for path, entry in changes.items():
        reason = entry.get('reason')
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError('Handover documentation reason is missing: '+path)
        for key in ('old_sha256', 'new_sha256'):
            value = entry.get(key)
            if (not isinstance(value, str) or len(value) != 64 or
                any(c not in '0123456789abcdef' for c in value)):
                raise ValueError('Invalid handover documentation hash: '+path)
        if entry['old_sha256'] != HANDOVER_PREIMAGES[path]:
            raise ValueError('Handover documentation baseline hash mismatch: '+path)
    return changes


def _handover_hash(path: str, expected: str, changes: dict) -> str:
    entry = changes.get(path)
    if entry is None:
        return expected
    if entry['old_sha256'] != expected:
        raise ValueError('Handover documentation previous hash mismatch: '+path)
    return entry['new_sha256']


def _layout_approvals(root: Path) -> dict:
    """Accept the ten revised explanations, retaining every predecessor byte."""
    ledger = json.loads((root/LAYOUT_RECORD).read_text())
    if (ledger.get('schema') != 1 or ledger.get('interpretation_only') is not True or
        ledger.get('mathematical_content_changed') is not False or
        ledger.get('original_archive_sha256') != ORIGINAL_ARCHIVE_SHA256 or
        ledger.get('previous_record') != HANDOVER_RECORD or
        ledger.get('previous_record_sha256') != HISTORICAL_LEDGER_SHA256[HANDOVER_RECORD] or
        ledger.get('base_commit') != LAYOUT_BASE_COMMIT or
        ledger.get('base_tree') != LAYOUT_BASE_TREE):
        raise ValueError('Invalid layout documentation ledger contract')
    entries = ledger.get('changes', [])
    changes = {entry['path']: entry for entry in entries}
    if (len(changes) != len(entries) or changes.keys() != LAYOUT_PATHS or
        ledger.get('additions')):
        raise ValueError('Layout ledger is not the authorized document set')
    for path, entry in changes.items():
        reason = entry.get('reason')
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError('Layout documentation reason is missing: '+path)
        for key in ('old_sha256', 'new_sha256'):
            value = entry.get(key)
            if (not isinstance(value, str) or len(value) != 64 or
                any(c not in '0123456789abcdef' for c in value)):
                raise ValueError('Invalid layout documentation hash: '+path)
        if entry['old_sha256'] != LAYOUT_PREIMAGES[path]:
            raise ValueError('Layout documentation baseline hash mismatch: '+path)
    return changes


def _layout_hash(path: str, expected: str, changes: dict) -> str:
    entry = changes.get(path)
    if entry is None:
        return expected
    if entry['old_sha256'] != expected:
        raise ValueError('Layout documentation previous hash mismatch: '+path)
    return entry['new_sha256']


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
    followup = _followup_approvals(root)
    handover = _handover_approvals(root)
    layout = _layout_approvals(root)
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
            expected = _followup_hash(entry['path'], expected, followup)
            expected = _handover_hash(entry['path'], expected, handover)
            expected = _layout_hash(entry['path'], expected, layout)
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
        expected = _followup_hash(path, entry['sha256'], followup)
        expected = _handover_hash(path, expected, handover)
        expected = _layout_hash(path, expected, layout)
        if sha(_safe_path(root,path).read_bytes()) != expected:
            raise ValueError('Protected documentation changed: '+path)
    # Includes the five navigation documents outside the older import set.
    for path, entry in handover.items():
        expected = _layout_hash(path, entry['new_sha256'], layout)
        if sha(_safe_path(root, path).read_bytes()) != expected:
            raise ValueError('Protected handover document changed: '+path)
    # Includes the eight previously unfrozen teaching/experiment explanations.
    for path, entry in layout.items():
        if sha(_safe_path(root, path).read_bytes()) != entry['new_sha256']:
            raise ValueError('Protected layout document changed: '+path)
    # Check immutable predecessor bytes after their semantic checks. This keeps
    # older diagnostic failures informative while also rejecting silent rewrites
    # of historical reasons, metadata, or accepted hash-chain entries.
    for path, expected in HISTORICAL_LEDGER_SHA256.items():
        if sha((root/path).read_bytes()) != expected:
            raise ValueError('Historical change ledger changed: '+path)
    return {'status':'PASS','source_members':count,'archive_sha256':ORIGINAL_ARCHIVE_SHA256,
            'source_archive_unchanged':True,'original_import_manifest_unchanged':True,
            'scientific_content_unchanged':not changes,
            'authorized_changes_verified':sorted(changes),
            'authorized_additions_verified':sorted(additions),
            'change_record':CHANGE_RECORD,
            'document_change_record':DOCUMENT_RECORD,
            'authorized_document_changes_verified':sorted(document_changes),
            'authorized_document_additions_verified':sorted(document_additions),
            'followup_change_record':FOLLOWUP_RECORD,
            'authorized_followup_documents_verified':sorted(followup),
            'mathematics_changed_by_followup':False,
            'handover_change_record':HANDOVER_RECORD,
            'authorized_handover_documents_verified':sorted(handover),
            'mathematics_changed_by_handover':False,
            'layout_change_record':LAYOUT_RECORD,
            'authorized_layout_documents_verified':sorted(layout),
            'mathematics_changed_by_layout':False,
            'historical_change_ledgers_unchanged':True,
            'validator_change':'original I/O guard; approved numerical-method metadata update only'}


if __name__ == '__main__':
    print(json.dumps(verify(),indent=2))
