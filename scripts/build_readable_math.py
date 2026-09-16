"""Generate current reading copies while preserving original proof/evidence bytes.

Only math transport, relative links, two obsolete report-delivery paragraphs,
and an explicit source footer change. --check never writes; --write rebuilds
the three named reading copies. Source hashes require a separate review to change.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
READERS = {
    'studies/robustness-01/REPORT.md': (
        'docs/ROBUSTNESS_REPORT.md',
        'bfce35293ec634b4ac825cce52cf500c35a5fb87a9d9964d865303dfe67030b2'),
    'studies/robustness-01/PROOFS.md': (
        'docs/ROBUSTNESS_PROOFS.md',
        '722155ce5c119a81defb63c1432013d260003e30028ef9441110baf67f1b6fed'),
    'repairs/theory-01/NUMERICAL_PROOF.md': (
        'docs/NUMERICAL_PROOF.md',
        'b20dc1174675bac9d701127930ed2c9bd1b11b53a64438e1ee5dd8951c48010e'),
}
OBSOLETE_REPORT_PARAGRAPHS = (
    '**Scientific work: completed locally. Repository publication: pending.** The\n'
    'current connection can read GitHub but exposes no write operation; direct Git\n'
    'access failed at DNS resolution. The existing target branch remains\n'
    '`research/robustness-01` at work-order commit\n'
    '`ddb17c5040e17cb0078121081afe15de70158fe8`. This packet is not a claimed remote\n'
    'commit or new CI result. It is ready as an additions-only repository patch.\n\n',
    'Only additions under `studies/robustness-01/` are proposed. The existing committed\n'
    'work order is preserved, not replaced. No main-branch edits, new GitHub commit,\n'
    'CI execution, merge, laboratory message, data acquisition, license, release or\n'
    'privacy change occurred during this continuation. The earlier work-order commit\n'
    'is not presented as containing these results.\n\n',
)


def safe_tex(tex: str) -> str:
    """Equivalent relation spelling and explicit one-token fraction arguments."""
    tex = tex.replace('<', r'\lt ').replace('>', r'\gt ')
    tex = re.sub(r'\\frac\s*([A-Za-z0-9])\s*([A-Za-z0-9])',
                 lambda m: r'\frac{' + m[1] + '}{' + m[2] + '}', tex)
    return re.sub(r'\\frac\s*([A-Za-z0-9])(?=\{)',
                  lambda m: r'\frac{' + m[1] + '}', tex)


def fence_displays(text: str) -> str:
    """Convert the source's standalone dollar displays, preserving body lines."""
    lines = text.splitlines(keepends=True)
    display = False
    output = []
    for line in lines:
        if line.strip() == '$$':
            output.append('```\n' if display else '```math\n')
            display = not display
        else:
            output.append(safe_tex(line) if display else line)
    if display:
        raise ValueError('Unpaired display delimiter')
    return ''.join(output)


def reading_copy(source: str, text: str) -> str:
    destination = READERS[source][0]
    if source == 'studies/robustness-01/REPORT.md':
        for paragraph in OBSOLETE_REPORT_PARAGRAPHS:
            if text.count(paragraph) != 1:
                raise ValueError('Original delivery paragraph changed')
            text = text.replace(paragraph, '', 1)
    text = fence_displays(text)

    def rebase(match: re.Match) -> str:
        target = match[1]
        parts = urlsplit(target)
        if parts.scheme or parts.netloc or not parts.path:
            return match[0]
        full = posixpath.normpath(posixpath.join(posixpath.dirname(source), parts.path))
        full = READERS.get(full, (full,))[0]
        relative = posixpath.relpath(full, posixpath.dirname(destination))
        return '](' + relative + ('#' + parts.fragment if parts.fragment else '') + ')'

    text = re.sub(r'\]\(([^)]+)\)', rebase, text)
    original = posixpath.relpath(source, posixpath.dirname(destination))
    footer = '\n---\n\nPreserved source: [original document](' + original + ').'
    if source == 'studies/robustness-01/REPORT.md':
        footer += (' Historical delivery-status paragraphs remain in that source;\n'
                   'see the [integration record](../integrations/lab-handover-01/REPORT.md)\n'
                   'for repository integration and verification.')
    return text.rstrip() + '\n' + footer + '\n'


def build(root: Path = ROOT, *, write: bool = False) -> dict:
    prepared = []
    for source, (destination, expected) in READERS.items():
        original = (root/source).read_bytes()
        if hashlib.sha256(original).hexdigest() != expected:
            raise ValueError('Preserved reading source changed: ' + source)
        value = reading_copy(source, original.decode('utf-8')).encode('utf-8')
        prepared.append((destination, value))
    # Validate all sources before changing any destination.
    if write:
        for destination, value in prepared:
            (root/destination).parent.mkdir(parents=True, exist_ok=True)
            (root/destination).write_bytes(value)
    else:
        for destination, value in prepared:
            if not (root/destination).exists() or (root/destination).read_bytes() != value:
                raise ValueError('Reading copy missing or stale: ' + destination)
    return {'status': 'PASS', 'mode': 'write' if write else 'check',
            'copies': {destination: hashlib.sha256(value).hexdigest()
                       for destination, value in prepared},
            'original_sources_modified': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    args = parser.parse_args()
    print(json.dumps(build(write=args.write), indent=2))
