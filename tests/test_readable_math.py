"""Reader generation must preserve original evidence and reject silent drift."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from build_readable_math import READERS, build, fence_displays
from verify_handover import _fenced_blocks


class ReadableMathTests(unittest.TestCase):
    def copied_tree(self, directory):
        root = Path(directory)
        for source, (destination, _) in READERS.items():
            for name in (source, destination):
                (root/name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT/name, root/name)
        return root

    def test_current_copies_match_preserved_sources(self):
        self.assertEqual(build()['status'], 'PASS')
        for source, (destination, _) in READERS.items():
            original = (ROOT/source).read_text()
            generated = (ROOT/destination).read_text()
            self.assertNotIn('$$', generated)
            expressions = [block for block in _fenced_blocks(generated) if block[2] == 'math']
            self.assertEqual(len(expressions), original.count('\n$$\n')//2)

    def test_stale_copy_check_fails_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.copied_tree(directory)
            target = root/'docs/ROBUSTNESS_REPORT.md'
            target.write_text(target.read_text().replace('0.659944903', '0.1', 1))
            snapshot = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*.md')}
            with self.assertRaisesRegex(ValueError, 'missing or stale'):
                build(root)
            self.assertEqual(snapshot, {str(p.relative_to(root)): p.read_bytes()
                                        for p in root.rglob('*.md')})

    def test_source_change_prevents_partial_rebuild(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.copied_tree(directory)
            source = root/'repairs/theory-01/NUMERICAL_PROOF.md'
            source.write_text(source.read_text()+'\nUnreviewed change.\n')
            before = {d: (root/d).read_bytes() for d, _ in READERS.values()}
            with self.assertRaisesRegex(ValueError, 'Preserved reading source changed'):
                build(root, write=True)
            self.assertEqual(before, {d: (root/d).read_bytes() for d, _ in READERS.values()})

    def test_display_transport_preserves_escaped_delimiters(self):
        source = '$$\n' + r'\min\{1,\frac32\epsilon\},\quad\sum_{j<k}a_j.' + '\n$$\n'
        expected = '```math\n' + r'\min\{1,\frac{3}{2}\epsilon\},\quad\sum_{j\lt k}a_j.' + '\n```\n'
        self.assertEqual(fence_displays(source), expected)
        with self.assertRaisesRegex(ValueError, 'Unpaired'):
            fence_displays('$$\nx=1\n')


if __name__ == '__main__':
    unittest.main()
