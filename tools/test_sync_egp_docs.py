"""Regression checks for rendered Markdown heading hierarchy."""

import unittest

from sync_egp_docs import consecutive_headings


class HeadingTests(unittest.TestCase):
    def test_skipped_levels_keep_sibling_and_child_hierarchy(self):
        source = "# Guide\n### First\n#### Child\n### Second\n## Existing\n"
        expected = "# Guide\n## First\n### Child\n## Second\n## Existing\n"
        self.assertEqual(consecutive_headings(source), expected)

    def test_fenced_code_is_opaque(self):
        source = "# Guide\n```cpp\n### unchanged code\n#include <memory>\n```\n~~~text\n### unchanged text\n~~~\n### Section\n"
        self.assertEqual(consecutive_headings(source), source.replace("### Section", "## Section"))


if __name__ == "__main__":
    unittest.main()
