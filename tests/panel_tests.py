import unittest
import markdown

from csfg_extension import CSFGExtension
from processors.panel import *


class PanelTest(unittest.TestCase):
    # maxDiff = None

    def setUp(self):
        self.md = markdown.Markdown(extensions=[CSFGExtension()])
        self.test_file_path = 'tests/assets/panel/{}.txt'
        self.expected_file_path = 'tests/assets/panel/expected/{}.txt'

    def test_match_false(self):
        test_string = open(self.test_file_path.format('fail_string')).read()
        self.assertFalse(PanelBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        pass

    def test_match_true(self):
        test_string = open(self.test_file_path.format('basic')).read()
        self.assertTrue(PanelBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        pass

    def test_parses_no_blank_lines_single_paragraph(self):
        test_string = open(self.test_file_path.format('external_links')).read()
        converted_test_string = markdown.markdown(test_string, extensions=[CSFGExtension()]) + '\n'
        expected_file_string = open(self.expected_file_path.format('external_links_expected')).read()
        self.assertEqual(converted_test_string, expected_file_string)

    def test_parses_blank_lines_multiple_paragraphs(self):
        pass

    def test_parses_no_blank_self(self):
        pass

    def test_parses_external_link(self):
        pass

    def test_parses_glossary_link(self):
        pass

    def test_parses_video_link(self):
        pass

    def test_parses_codeblock(self):
        pass

    def test_parses_pictures(self):
        pass

    def test_parses_mathblocks(self):
        pass

    def test_parses_comments(self):
        pass

    def tearDown(self):
        self.md = None


