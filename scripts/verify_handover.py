"""Static handover navigation/math checks; no browser rendering or instrument I/O.

This script checks files, Markdown anchors, simple display-math syntax, and the
existence of Python scripts named in runnable shell blocks. Actual reference
execution and numerical verification remain separate recorded checks.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import shlex
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def _outside_fences(text: str) -> str:
    result = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            symbol = marker.group(1)[0]
            if fence is None:
                fence = symbol
            elif fence == symbol:
                fence = None
            result.append('')
        elif fence is None:
            result.append(line)
        else:
            result.append('')
    if fence is not None:
        raise ValueError('Unclosed fenced code block')
    return '\n'.join(result)


def _anchors(text: str) -> set[str]:
    """GitHub-style anchors for the simple headings used in the handover."""
    anchors = set()
    counts = {}
    for line in _outside_fences(text).splitlines():
        heading = re.match(r'^#{1,6}\s+(.*?)\s*#*\s*$', line)
        if not heading:
            continue
        value = re.sub(r'<[^>]*>', '', heading.group(1)).lower()
        value = re.sub(r'[^\w\-\s]', '', value, flags=re.UNICODE).replace(' ', '-')
        suffix = counts.get(value, 0)
        counts[value] = suffix+1
        anchors.add(value + (f'-{suffix}' if suffix else ''))
    # Explicit anchors are allowed in inherited targets, although the new pages
    # use ordinary headings. This does not permit HTML inside Mermaid diagrams.
    anchors.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)["\']', text))
    return anchors


def _math(text: str) -> None:
    if any('$' in line for line in text.splitlines() if re.match(r'^#{1,6}\s', line)):
        raise ValueError('Math delimiter in a heading')
    for value in ('\\operatorname', '\\[', '\\]', '\\(', '\\)'):
        if value in text:
            raise ValueError('Unsupported or raw math delimiter/macro: '+value)
    if text.count('$$') % 2:
        raise ValueError('Unpaired display-math delimiters')
    for expression in re.findall(r'\$\$(.*?)\$\$', text, flags=re.S):
        level = 0
        for match in re.finditer(r'(?<!\\)[{}]', expression):
            level += 1 if match.group() == '{' else -1
            if level < 0:
                raise ValueError('Unbalanced display-math braces')
        if level:
            raise ValueError('Unbalanced display-math braces')


def verify_documents(root: Path, documents: list[Path]) -> dict:
    root = root.resolve()
    links = 0
    script_references = 0
    for document in documents:
        document = document.resolve()
        if root not in document.parents:
            raise ValueError('Document escapes repository')
        original = document.read_text()
        text = _outside_fences(original)
        try:
            _math(text)
        except ValueError as error:
            raise ValueError(str(document.relative_to(root))+': '+str(error)) from error
        for target in re.findall(r'\]\(([^)]+)\)', text):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            path = ((document.parent/unquote(parts.path)) if parts.path else document).resolve()
            if root not in path.parents and path != root:
                raise ValueError('Local link escapes repository: '+target)
            if not path.exists():
                raise ValueError(str(document.relative_to(root))+': missing local link '+target)
            if parts.fragment and path.suffix == '.md':
                if unquote(parts.fragment) not in _anchors(path.read_text()):
                    raise ValueError(str(document.relative_to(root))+': missing local anchor '+target)
            links += 1
        for block in re.findall(r'^```(?:bash|sh|shell)\s*\n(.*?)^```\s*$',
                                original, flags=re.M | re.S):
            for line in block.replace('\\\n', ' ').splitlines():
                tokens = shlex.split(line, comments=True)
                if len(tokens) < 2 or tokens[0] not in ('python', 'python3'):
                    continue
                if tokens[1].endswith('.py'):
                    script = (root/tokens[1]).resolve()
                    if root not in script.parents or not script.is_file():
                        raise ValueError('Missing Python script in runnable block: '+tokens[1])
                    script_references += 1
    return {
        'status': 'PASS', 'documents_checked': len(documents),
        'local_links_checked': links, 'python_script_references_checked': script_references,
        'visual_rendering_checked': False, 'commands_executed_by_this_check': False,
        'scope': 'Static local navigation, simple Markdown/math syntax, and script-path checks only',
    }


def verify(root: Path = ROOT) -> dict:
    documents = {root/'README.md', root/'CLAIM_STATUS.md', root/'work_orders/CURRENT.md'}
    for name in ('docs', 'experiment'):
        documents.update((root/name).rglob('*.md'))
    return verify_documents(root, sorted(documents))


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
