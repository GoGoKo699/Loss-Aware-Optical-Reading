"""Static documentation regressions, distinct from visual rendering and science."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from verify_handover import verify, verify_documents, _anchors


class HandoverDocumentTests(unittest.TestCase):
    def test_final_local_documentation(self):
        result = verify()
        self.assertEqual(result['status'], 'PASS')
        self.assertFalse(result['visual_rendering_checked'])
        self.assertFalse(result['commands_executed_by_this_check'])

    def test_valid_links_math_and_script_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'target.md').write_text('# Phase (and loss)\n\n## Outcome\n')
            (root/'runner.py').write_text('print("REFERENCE ONLY")\n')
            document = root/'README.md'
            document.write_text('# Input\n\n[Target](target.md#phase-and-loss)\n\n'
                '$$\na_i=\\sqrt{p_i}.\n$$\n\n```bash\npython runner.py --output fresh\n```\n')
            result = verify_documents(root, [document])
            self.assertEqual(result['local_links_checked'], 1)
            self.assertEqual(result['python_script_references_checked'], 1)

    def test_rejects_broken_navigation_and_math(self):
        cases = {
            '[Missing](absent.md)': 'missing local link',
            '[Missing](target.md#absent)': 'missing local anchor',
            '[Outside](../outside.md)': 'escapes repository',
            '# $x$': 'heading',
            '$$\nx=1\n': 'Unpaired',
            '$$\n\\frac{1}{2\n$$': 'Unbalanced',
            '$$\nx=1}\n$$': 'Unbalanced',
            '$$\n\\operatorname{Tr}(x)\n$$': 'Unsupported',
            '\\[x=1\\]': 'raw math',
            '```bash\npython absent.py\n```': 'Missing Python script',
            '```bash\npython existing.py': 'Unclosed fenced',
        }
        for text, expected in cases.items():
            with self.subTest(text=text), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root/'target.md').write_text('# Actual\n')
                document = root/'README.md'
                document.write_text(text)
                with self.assertRaisesRegex(ValueError, expected):
                    verify_documents(root, [document])

    def test_duplicate_headings_and_fences(self):
        text = '# Port 0\n\n## Port 0\n\n```python\n# Not a heading\n```\n'
        self.assertEqual(_anchors(text), {'port-0', 'port-0-1'})


if __name__ == '__main__':
    unittest.main()
