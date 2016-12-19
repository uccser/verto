import unittest
import markdown

from csfg_extension import CSFGExtension
from processors.glossary import *


class GlossaryLinkTest(unittest.TestCase):
    # maxDiff = None

    def setUp(self):
        self.md = markdown.Markdown(extensions=[CSFGExtension()])
        self.test_file_path = 'tests/assets/glossary/{}.txt'
        self.expected_file_path = 'tests/assets/glossary/expected/{}.txt'

    def test_match_false(self):
        test_string = open(self.test_file_path.format('fail_string')).read()
        self.assertFalse(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        # TODO test longer strings

    def test_match_single_word_term_true(self):
        test_string = open(self.test_file_path.format('single_word_term')).read()
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_match_multiple_word_term_true(self):
        test_string = open(self.test_file_path.format('multiple_word_term')).read()
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        # TODO test more files with multiple terms

    def test_match_inline_true(self):
        test_string = open(self.test_file_path.format('inline_leading_characters')).read()
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        test_string = open(self.test_file_path.format('inline_trailing_characters')).read()
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        test_string = open(self.test_file_path.format('inline_leading_and_trailing_characters')).read()
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_matches_more_than_one_glossary_link_true(self):
        test_string = open(self.test_file_path.format('multiple_terms')).read()
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    # should parsing tests be in their own class?
    def test_correctly_parsed_inline(self):
        test_string = open(self.test_file_path.format('inline_leading_characters')).read()
        converted_test_string = markdown.markdown(test_string, extensions=[CSFGExtension()]) + '\n'
        expected_file_string = open(self.expected_file_path.format('inline_leading_characters_expected')).read()
        self.assertEqual(converted_test_string, expected_file_string)

        test_string = open(self.test_file_path.format('inline_trailing_characters')).read()
        converted_test_string = markdown.markdown(test_string, extensions=[CSFGExtension()]) + '\n'
        expected_file_string = open(self.expected_file_path.format('inline_trailing_characters_expected')).read()
        self.assertEqual(converted_test_string, expected_file_string)

        test_string = open(self.test_file_path.format('inline_leading_and_trailing_characters')).read()
        converted_test_string = markdown.markdown(test_string, extensions=[CSFGExtension()]) + '\n'
        expected_file_string = open(self.expected_file_path.format('inline_leading_and_trailing_characters_expected')).read()
        self.assertEqual(converted_test_string, expected_file_string)

    def test_glossary_link_in_panel(self):
        pass

    def tearDown(self):
        self.md = None

