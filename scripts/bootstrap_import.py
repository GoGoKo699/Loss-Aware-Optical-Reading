"""One-time restoration of the exact uploaded checkpoint, with safe I/O migration.

Git object transport is used only by the authorized initialization job. Original
archive bytes must match their SHA-256 before any source files are installed.
"""
from __future__ import annotations
import base64
import hashlib
import io
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE_SHA='e2bd57686376549342881a5d0348b16820ebbdab094b8d72df05a6836dbad016'
PAYLOAD_SHA='011961cff37b0993077845bc69c00597c638ed49093be3892f1b18285b47fe1a'
PARTS=[
'8d2e14224b2925be844b8dd629b588f372e98b2a',
'7b4e25ab90ffa4d2067d3147012b61bf62250ee3',
'220f855a631d497cc7d747d59a7264b82755cbe7',
'179f40cc1329b193a08ed8ceeb7fb6f31edce708',
'ca1e026229e58701240af93900749dbadf6607ac',
'2552b17e155469dd46a853dc59c4253ffacffcac',
'9e76654204e6f7f3a17f954a496b56a5ae0e3851',
'bb0b0e9d7f096680cb6e07fba15aabf721163cdf',
'a7c8b686a0c7d7a7559bd7d7d063e6a42baeb7cf',
'8ba5ae47a9ea7fb7a9786f0f828329659daf9e2a',
'56024d0659811b40d9469ae12c29298ca6989999']
OLD_IO="ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results';OUT.mkdir(exist_ok=True)"
NEW_IO='''ROOT=Path(__file__).resolve().parents[1]
# Migration-only I/O guard: mathematical validation below is unchanged.
import argparse
_output_parser = argparse.ArgumentParser(description=__doc__)
_output_parser.add_argument('--output-dir', required=True,
    help='New directory outside frozen results; never overwrites an existing run.')
OUT=Path(_output_parser.parse_args().output_dir).resolve()
_frozen=(ROOT/'results').resolve()
_runs=(_frozen/'runs').resolve()
if (OUT == _frozen or OUT == _runs or
    (_frozen in OUT.parents and _runs not in OUT.parents)):
    _output_parser.error('Use a new results/runs/<name> directory, not archived results.')
OUT.mkdir(parents=True, exist_ok=False)'''

def digest(data):
    return hashlib.sha256(data).hexdigest()

def fetch_blob(sha):
    url='https://api.github.com/repos/GoGoKo699/Loss-Aware-Optical-Reading/git/blobs/'+sha
    req=urllib.request.Request(url,headers={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],
        'Accept':'application/vnd.github+json','User-Agent':'checkpoint07-verified-import'})
    with urllib.request.urlopen(req,timeout=60) as response:
        obj=json.load(response)
    data=base64.b64decode(obj['content'])
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if actual!=sha:
        raise ValueError('Git transport hash mismatch')
    return data

def restore(node):
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=node['level']) as archive:
        archive.comment=base64.b64decode(node['comment'])
        for entry in node['files']:
            name=PurePosixPath(entry['filename'])
            if name.is_absolute() or '..' in name.parts:
                raise ValueError('Unsafe archived path')
            info=zipfile.ZipInfo(str(name),tuple(entry['date_time']))
            for key in ('compress_type','create_system','create_version','extract_version',
                        'flag_bits','internal_attr','external_attr','volume'):
                setattr(info,key,entry[key])
            info.extra=base64.b64decode(entry['extra'])
            info.comment=base64.b64decode(entry['comment'])
            value=entry['data']
            if 'zip' in value:
                data=restore(value['zip'])
            elif 'text' in value:
                data=value['text'].encode()
            else:
                data=base64.b64decode(value['base64'])
            archive.writestr(info,data,compresslevel=node['level'])
    data=buffer.getvalue()
    if digest(data)!=node['sha256']:
        raise ValueError('ZIP reconstruction is not byte-identical; import stopped')
    return data

def main():
    target=ROOT/'provenance/archives/photonic_single_photon_checkpoint_07.zip'
    if target.exists():
        raise FileExistsError('Import already exists; never restart or overwrite')
    compressed=b''.join(fetch_blob(sha) for sha in PARTS)
    if digest(compressed)!=PAYLOAD_SHA:
        raise ValueError('Compressed transport SHA-256 mismatch')
    data=restore(json.loads(lzma.decompress(compressed)))
    if len(data)!=173345 or digest(data)!=ARCHIVE_SHA:
        raise ValueError('Original archive identity mismatch')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        prefix='photonic_single_photon_checkpoint_07/'
        original={name[len(prefix):]:archive.read(name) for name in archive.namelist()
                  if name.startswith(prefix) and not name.endswith('/')}
    if len(original)!=39:
        raise ValueError('Unexpected source inventory')
    for line in original['SHA256SUMS.txt'].decode().splitlines():
        expected,name=line.split(maxsplit=1)
        if digest(original[name.lstrip('*')])!=expected:
            raise ValueError('Internal source checksum mismatch: '+name)
    records=[]
    for name,content in original.items():
        rel=PurePosixPath(name)
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('Unsafe extraction path')
        dest=name; operation='byte-preserved'; installed=content
        if name in ('README.md','SHA256SUMS.txt'):
            dest='provenance/checkpoint07/'+name;operation='relocated-byte-preserved'
        elif name=='src/validate.py':
            text=content.decode()
            if text.count(OLD_IO)!=1:
                raise ValueError('Expected exact I/O perimeter not found')
            installed=text.replace(OLD_IO,NEW_IO).encode()
            operation='I/O-only guard; body after RNG unchanged'
        path=ROOT/dest
        if path.exists():
            raise FileExistsError('Refusing to overwrite '+dest)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(installed)
        records.append({'source':name,'path':dest,'operation':operation,
                        'source_sha256':digest(content),'installed_sha256':digest(installed)})
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    manifest={'archive':str(target.relative_to(ROOT)),'archive_sha256':ARCHIVE_SHA,
              'files':records,'scientific_changes':False,
              'transport':'Recursive ZIP metadata/content; original ZIP hash verified before installation.'}
    (ROOT/'provenance/IMPORT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    docs={
      '.gitignore':'66ef8c7f95e6ba361adebfc0a696b4bd5fdd0f22',
      'README.md':'429d45959b7c962cfa58a15f21ee46bccfb44ae6',
      'AGENTS.md':'f6f3b21b6d38a7abff41315618c974e2bec3bd2e',
      'CONTRIBUTING.md':'991929ee60e7ca2cb0bf770d65cdd70c7aee9bba',
      'docs/PHYSICAL_SETTING.md':'23b51ffcd0f650db31f7041a5edead33a902c425',
      'docs/REPRODUCE.md':'2ad038519f79af7d58e9886f8c34386fe07a1a92',
      'docs/ROADMAP.md':'4ab2035f6c77bce0c25ac9cfe0d4bfb86cdb40ae',
      'work_orders/CURRENT.md':'f434e5ba9f23868554a8709e5b6648f8a7452e4d',
      'work_orders/README.md':'091aa5dec4237f22b29a378f0c566d92eeaf03d1'}
    for name,sha in docs.items():
        path=ROOT/name
        if path.exists():
            raise FileExistsError('Refusing to replace existing reader-facing file: '+name)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(fetch_blob(sha))
    print('Restored exact archive, 39 source members, and reader-facing documentation.')

if __name__=='__main__':
    main()
