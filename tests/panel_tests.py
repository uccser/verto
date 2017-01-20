import unittest
import markdown

from csfg_extension import CSFGExtension
from processors.panel import *
from tests.start_tests import BaseTestCase

class PanelTest(BaseTestCase):
    
    def __init__(self, *args, **kwargs):
        """Set tag name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'panel'
    
    def test_match_false(self):
        test_string = self.read_test_file('fail_string')
        self.assertFalse(PanelBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_match_true(self):
        test_string = self.read_test_file('basic')
        self.assertTrue(PanelBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_parses_no_blank_lines_single_paragraph(self):
        test_string = self.read_test_file('external_links')
        converted_test_string = markdown.markdown(test_string, extensions=[CSFGExtension()]) + '\n'
        expected_file_string = self.read_test_file('external_links_expected')
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
