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


def _fenced_blocks(text: str) -> list[tuple[int, int, str, str]]:
    """Return line spans, language, and literal contents of fenced blocks."""
    blocks = []
    opening = None
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if opening is None:
            marker = re.match(r'^\s*(`{3,}|~{3,})([^`\n]*)$', line)
            if marker:
                opening = (index, marker.group(1), marker.group(2).strip())
        else:
            start, fence, language = opening
            marker = re.match(r'^\s*(' + re.escape(fence[0]) + r'{'
                              + str(len(fence)) + r',})\s*$', line)
            if marker:
                blocks.append((start, index, language, '\n'.join(lines[start+1:index])))
                opening = None
    if opening is not None:
        raise ValueError('Unclosed fenced code block')
    return blocks


def _outside_fences(text: str) -> str:
    lines = text.splitlines()
    for start, end, _, _ in _fenced_blocks(text):
        lines[start:end+1] = [''] * (end-start+1)
    return '\n'.join(lines)


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
    outside = _outside_fences(text)
    if any('$' in line for line in outside.splitlines() if re.match(r'^#{1,6}\s', line)):
        raise ValueError('Math delimiter in a heading')
    expressions = re.findall(r'\$\$(.*?)\$\$', outside, flags=re.S)
    for _, _, language, expression in _fenced_blocks(text):
        if language == 'math':
            if '$' in expression:
                raise ValueError('Dollar delimiter inside a fenced math block')
            if not expression.strip():
                raise ValueError('Empty fenced math block')
            expressions.append(expression)
    math_text = outside + '\n' + '\n'.join(expressions)
    for value in ('\\operatorname', '\\[', '\\]', '\\(', '\\)'):
        if value in math_text:
            raise ValueError('Unsupported or raw math delimiter/macro: '+value)
    if outside.count('$$') % 2:
        raise ValueError('Unpaired display-math delimiters')
    for expression in expressions:
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
            _math(original)
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
