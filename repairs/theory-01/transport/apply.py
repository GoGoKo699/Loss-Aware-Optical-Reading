"""One-time, hash-locked source repair; only the repair branch may be published.

No network reads of code and no execution of the transported JSON. Each delta is
reconstructed from an explicitly hashed old blob plus literal UTF-8 additions.
All preimages/outputs are checked before any write. A second run refuses to apply.
"""
from __future__ import annotations
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile

REPO = 'GoGoKo699/Loss-Aware-Optical-Reading'
BRANCH = 'repair/theory-01'
ANCESTOR = '10410caf761ad858236d22c4a2f5d9a53bc94dff'
BUNDLE_SHA = 'cf82595947e7fefec9c3cb02fe5591d3f1796fde42612b5e60ccb7f2810d8a00'
BASE = 'repairs/theory-01'
TRANSPORT = BASE + '/transport'
WORKFLOW = '.github/workflows/apply-theory-repair-01.yml'
ALLOWED = {
 '.github/workflows/verify.yml', 'CLAIM_STATUS.md', 'README.md',
 'docs/NUMERICAL_CONTRACT.md', 'docs/REPRODUCE.md', 'proofs/THEORY.md',
 'provenance/changes/theory-repair-01.json', BASE+'/HIGH_PENALTY.json',
 BASE+'/LOCAL_SUMMARY.json', BASE+'/NUMERICAL_PROOF.md', BASE+'/REPORT.md',
 BASE+'/verify.py', 'requirements-test.txt', 'scripts/reproduce.py',
 'scripts/verify_import.py', 'src/photon_support.py', 'src/theory.py',
 'src/validate.py', 'tests/test_photon_support.py', 'work_orders/CURRENT.md'}
REMOTE = {BASE+'/REMOTE_SUMMARY.json', BASE+'/REMOTE_EVIDENCE.tar.xz',
          BASE+'/REMOTE_MANIFEST.json'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def safe(root, name):
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or str(p) != name:
        raise ValueError('Unsafe path: '+name)
    out = root/name
    if any(x.is_symlink() for x in (out, *out.parents)):
        raise ValueError('Symlink path: '+name)
    if root not in out.resolve().parents:
        raise ValueError('Outside root: '+name)
    return out


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, text=True).strip()


def reconstruct(root):
    manifest = json.loads((root/TRANSPORT/'MANIFEST.json').read_text())
    parts = []
    for entry in manifest['parts']:
        raw = safe(root, entry['path']).read_bytes()
        if sha(raw) != entry['sha256'] or blob(raw) != entry['git_blob']:
            raise ValueError('Transport part mismatch: '+entry['path'])
        parts.append(raw.strip())
    compressed = base64.b64decode(b''.join(parts), validate=True)
    if sha(compressed) != BUNDLE_SHA or len(compressed) != 22156:
        raise ValueError('Repair bundle hash/size mismatch')
    packet = json.loads(lzma.decompress(compressed))
    if packet['expected_branch'] != BRANCH or packet['required_ancestor'] != ANCESTOR:
        raise ValueError('Wrong packet scope')
    names = [item['path'] for item in packet['files']]
    if len(names) != len(set(names)) or set(names) != ALLOWED:
        raise ValueError('Wrong or duplicated changed-file inventory')
    outputs = {}
    for item in packet['files']:
        name = item['path']; target = safe(root, name)
        if item['old_git_blob'] is None:
            if target.exists():
                raise ValueError('New target already exists: '+name)
            old = b''
        else:
            old = target.read_bytes()
            if blob(old) != item['old_git_blob']:
                raise ValueError('Preimage changed or patch already applied: '+name)
        pieces = []
        for segment in item['segments']:
            if set(segment) == {'text'}:
                pieces.append(segment['text'].encode('utf-8'))
            elif set(segment) == {'copy_bytes'}:
                start, end = segment['copy_bytes']
                if type(start) is not int or type(end) is not int or not 0 <= start <= end <= len(old):
                    raise ValueError('Invalid copy range: '+name)
                pieces.append(old[start:end])
            else:
                raise ValueError('Unknown delta operation')
        content = b''.join(pieces)
        content.decode('utf-8')
        if sha(content) != item['new_sha256']:
            raise ValueError('Reconstructed output hash mismatch: '+name)
        outputs[name] = content
    return outputs


def run_logged(root, args, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
               PYTHONDONTWRITEBYTECODE='1')
    with path.open('w') as log:
        p = subprocess.run(args, cwd=root, env=env, text=True,
                           stdout=log, stderr=subprocess.STDOUT)
    print(path.read_text(), flush=True)
    p.check_returncode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-root', type=Path)
    args = parser.parse_args()
    root = (args.check_root or Path.cwd()).resolve()
    outputs = reconstruct(root)
    if args.check_root:
        print(f'All {len(outputs)} preimages and reconstructed outputs verified; no writes.')
        return
    if os.environ.get('GITHUB_REPOSITORY') != REPO or os.environ.get('GITHUB_REF') != 'refs/heads/'+BRANCH:
        raise ValueError('Publishing is restricted to the authorized GitHub branch')
    if git(root, 'branch', '--show-current') != BRANCH or git(root, 'status', '--porcelain', '--untracked-files=all'):
        raise ValueError('Expected a clean checkout of the repair branch')
    subprocess.run(['git','merge-base','--is-ancestor',ANCESTOR,'HEAD'],cwd=root,check=True)
    start = git(root, 'rev-parse', 'HEAD')
    start_tree = git(root, 'rev-parse', 'HEAD^{tree}')
    for name in REMOTE:
        if safe(root, name).exists():
            raise ValueError('Remote evidence already exists')
    for name, raw in outputs.items():
        path = safe(root, name); path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
    logdir = root/'results/runs/repair-integration-logs'
    if logdir.exists():
        raise ValueError('Log directory already exists')
    logdir.mkdir(parents=True)
    run_logged(root, [sys.executable,'-m','pip','install','-r','requirements-test.txt'], logdir/'install.log')
    run_logged(root, [sys.executable,'scripts/verify_import.py'], logdir/'integrity.log')
    run_logged(root, [sys.executable,'-m','unittest','discover','-s','tests','-v'], logdir/'unit-tests.log')
    run_logged(root, [sys.executable,'scripts/reproduce.py','--output','results/runs/repair-integration'], logdir/'regression.log')
    run_logged(root, [sys.executable,BASE+'/verify.py','--output','results/runs/repair-integration-audit'], logdir/'audit.log')
    run_logged(root, [sys.executable,'scripts/verify_import.py'], logdir/'integrity-after.log')
    r = json.loads((root/'results/runs/repair-integration/REPRODUCTION.json').read_text())
    a = json.loads((root/'results/runs/repair-integration-audit/SUMMARY.json').read_text())
    if r['reference_comparison'] != 'PASS' or r['fresh_summary']['checks'] != 5261 or a['status'] != 'PASS' or a['repaired_scientific_checks'] != 993:
        raise ValueError('Wrong remote validation result')
    for name, raw in outputs.items():
        if safe(root, name).read_bytes() != raw:
            raise ValueError('Tests changed a patched file: '+name)
    summary = {'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
        'repository':REPO,'branch':BRANCH,'source_commit':start,'source_tree':start_tree,
        'audit_ancestor':ANCESTOR,'workflow_run':os.environ['GITHUB_RUN_ID'],
        'bundle_sha256':BUNDLE_SHA,'unit_test_groups':28,'original_engineering_groups':12,
        'new_repair_groups':16,'support_enclosure_instances':135,
        'inherited_checks':r['fresh_summary']['checks'],
        'historical_audit_checks':a['historical_audit_checks'],
        'repaired_scientific_checks':a['repaired_scientific_checks'],
        'derived_budget_name_differences':len(a['derived_budget_name_differences']),
        'max_independent_residual':a['max_scientific_residual'],
        'reference_comparison':r['reference_comparison'],
        'integrity':r['integrity'],'python':a['python'],'numpy':a['numpy'],
        'scipy':a['scipy'],'mpmath':a['mpmath'],
        'photon_support_exact_rational_enclosure':True,
        'entire_pipeline_interval_certified':False,'laboratory_data':False,
        'note':'Fresh GitHub Actions execution; final committed head is recorded by git/PR after creation.'}
    (root/BASE/'REMOTE_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    evidence = root/BASE/'REMOTE_EVIDENCE.tar.xz'
    evidence_files = {}
    with tarfile.open(evidence,'w:xz') as archive:
        for sub in ('repair-integration-logs','repair-integration','repair-integration-audit'):
            for path in sorted((root/'results/runs'/sub).rglob('*')):
                if path.is_file():
                    name = path.relative_to(root/'results/runs').as_posix()
                    archive.add(path,arcname=name,recursive=False)
                    evidence_files[name] = sha(path.read_bytes())
    manifest = {'archive':evidence.name,'sha256':sha(evidence.read_bytes()),
                'members':evidence_files,'source_bundle':BUNDLE_SHA,
                'scope':'Remote F01-F03 repair checks, not experimental evidence.'}
    (root/BASE/'REMOTE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (root/WORKFLOW).unlink()
    changed = set(git(root,'diff','--name-only').splitlines())
    untracked = set(git(root,'ls-files','--others','--exclude-standard').splitlines())
    allowed = ALLOWED | REMOTE | {WORKFLOW}
    if not (changed | untracked) <= allowed:
        raise ValueError('Unexpected changes before commit: '+str((changed|untracked)-allowed))
    subprocess.run(['git','add','--',*sorted(allowed)],cwd=root,check=True)
    if set(git(root,'diff','--cached','--name-only').splitlines()) != allowed:
        raise ValueError('Staged inventory is not the exact authorized output')
    git(root,'config','user.name','github-actions[bot]')
    git(root,'config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    subprocess.run(['git','commit','-m','Repair audit findings F01-F03 with exact photon bounds and preserved regression evidence'],cwd=root,check=True)
    if git(root,'status','--porcelain','--untracked-files=all'):
        raise ValueError('Working tree not clean after repair commit')
    subprocess.run(['git','push','origin','HEAD:refs/heads/'+BRANCH],cwd=root,check=True)
    print('Verified repair published only to '+BRANCH+' at '+git(root,'rev-parse','HEAD'))

if __name__ == '__main__':
    main()
