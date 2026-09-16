"""Static documentation regressions, distinct from visual rendering and science."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from verify_handover import verify, verify_documents, _anchors, _tables


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

    def test_tables_reject_pipes_inside_code_and_truncated_rows(self):
        cases = [
            ('| SU4 | `O_j=I4-2|j><j|` | Port j |', 'Unescaped pipe'),
            ('| SU4 | ``A |j>`` | Port j |', 'Unescaped pipe'),
            ('| SU4 | target | output | discarded |', 'has 4 cells; expected 3'),
            ('| SU4 | target |', 'has 2 cells; expected 3'),
            ('SU4 | target | output | discarded', 'has 4 cells; expected 3'),
        ]
        for row, message in cases:
            with self.subTest(row=row):
                with self.assertRaisesRegex(ValueError, message):
                    _tables('| Route | Target | Output |\n|---|---|---|\n' + row)
        with self.assertRaisesRegex(ValueError, 'Table header'):
            _tables('| Route | Target | Output |\n|---|---|\n| SU4 | Target |')

    def test_tables_accept_escaped_pipes_and_ignore_fenced_examples(self):
        text = ('| Route | Target | Output |\n|---|:---|---:|\n'
                r'| SU4 | `O_j=I4-2\|j><j\|` | Port j |' + '\n\n'
                '```text\n| Invalid | Example |\n|---|---|\n| a | b | c |\n```\n\n'
                '```math\n|j\\rangle\n```\n\n'
                'Route | Result\n--- | ---\nSU8 | Port j\n')
        self.assertEqual(_tables(text), (2, 2))

    def test_math_fences_preserve_markdown_sensitive_expressions(self):
        # Literal fences protect escaped braces; relation macros also avoid
        # tag-like characters in a later HTML stage (the repeated screenshot).
        expressions = [
            r'C\leq\min\left\{1-E,\left[\sqrt{1-e^{-\kappa\mu}}'
            r'+\sqrt{E/(m-1)}\right]^2\right\}.',
            r'H_\Delta=\frac{1}{m(m-1)}\sum_{j\lt k}'
            r'(A_j-A_k)^\dagger(A_j-A_k).',
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root/'README.md'
            document.write_text('# Benchmark\n\n' + '\n\n'.join(
                '```math\n'+expression+'\n```' for expression in expressions))
            self.assertEqual(verify_documents(root, [document])['status'], 'PASS')

    def test_display_comparisons_avoid_html_tag_characters(self):
        for wrapper in ('```math\n{}\n```', '$$\n{}\n$$'):
            for relation in ('j<k', 'j>k', r'0<\eta_i\leq1'):
                with self.subTest(wrapper=wrapper, relation=relation), \
                        tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    document = root/'README.md'
                    document.write_text(wrapper.format(relation))
                    with self.assertRaisesRegex(ValueError, 'HTML-sensitive'):
                        verify_documents(root, [document])
            with self.subTest(wrapper=wrapper), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                document = root/'README.md'
                document.write_text(wrapper.format(r'j\lt k,\quad k\gt j,\quad 0\lt\eta_i\leq1'))
                self.assertEqual(verify_documents(root, [document])['status'], 'PASS')

    def test_math_fences_are_checked_instead_of_silently_skipped(self):
        cases = {
            '```math\n\\frac{1}{2\n```': 'Unbalanced',
            '~~~math\nx=1}\n~~~': 'Unbalanced',
            '````math\n\\operatorname{Tr}(x)\n````': 'Unsupported',
            '```math\n$$x=1$$\n```': 'Dollar delimiter',
            '```math\n\n```': 'Empty',
            '````math\nx=1\n```': 'Unclosed fenced',
        }
        for text, expected in cases.items():
            with self.subTest(text=text), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                document = root/'README.md'
                document.write_text(text)
                with self.assertRaisesRegex(ValueError, expected):
                    verify_documents(root, [document])

    def test_reported_pages_keep_math_out_of_markdown_preprocessing(self):
        pages = [
            ('docs/THEORY_ROUTE.md', 15), ('docs/CONTRIBUTIONS.md', 3),
            ('docs/ROBUSTNESS_GUIDE.md', 1), ('experiment/M1.md', 3),
            ('experiment/P1.md', 4), ('experiment/P2.md', 4),
            ('experiment/SU4.md', 6), ('experiment/SU8.md', 7),
            ('experiment/COMMISSIONING.md', 7),
            ('REPORT.md', 11), ('docs/ROBUSTNESS_REPORT.md', 3),
            ('docs/ROBUSTNESS_PROOFS.md', 16), ('docs/NUMERICAL_PROOF.md', 7),
        ]
        for name, count in pages:
            with self.subTest(document=name):
                text = (ROOT/name).read_text()
                self.assertNotIn('$$', text)
                self.assertEqual(text.count('```math\n'), count)


if __name__ == '__main__':
    unittest.main()
