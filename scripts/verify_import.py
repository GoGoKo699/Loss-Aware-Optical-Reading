"""Verify the exact source archive and protected working files; no writes or network."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify(root: Path = ROOT) -> dict:
    manifest = json.loads((root/'provenance/IMPORT_MANIFEST.json').read_text())
    archive = root/manifest['archive']
    if sha(archive.read_bytes()) != manifest['archive_sha256']:
        raise ValueError('Original checkpoint archive changed')
    count = 0
    with zipfile.ZipFile(archive) as z:
        for entry in manifest['files']:
            name = entry['source']
            old = z.read('photonic_single_photon_checkpoint_07/'+name)
            current = (root/entry['path']).read_bytes()
            if sha(old) != entry['source_sha256']:
                raise ValueError('Source manifest mismatch: '+name)
            if sha(current) != entry['installed_sha256']:
                raise ValueError('Protected working file changed: '+entry['path'])
            if name == 'src/validate.py':
                anchor = b'RNG=np.random.default_rng(2026091417)'
                if old.split(anchor, 1)[1] != current.split(anchor, 1)[1]:
                    raise ValueError('Validation mathematics changed during I/O migration')
            elif old != current:
                raise ValueError('Non-permitted migration difference: '+name)
            count += 1
    return {'status': 'PASS', 'source_members': count, 'archive_sha256': manifest['archive_sha256'],
            'scientific_content_unchanged': True, 'validator_change': 'I/O perimeter only'}

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
