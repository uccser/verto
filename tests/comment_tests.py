import unittest
import markdown

from csfg_extension import CSFGExtension
from processors.comment import *


class CommentTest(unittest.TestCase):

    def setUp(self):
        self.md = markdown.Markdown(extensions=[CSFGExtension()])
        self.test_file_path = 'tests/assets/comment/{}.txt'
        self.expected_file_path = 'tests/assets/comment/expected/{}.txt'

    def test_match_false(self):
        test_string = open(self.test_file_path.format('fail_string')).read()
        self.assertFalse(CommentBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_match_single_word_term_true(self):
        test_string = open(self.test_file_path.format('basic')).read()
        self.assertTrue(CommentBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_parses_basic(self):
        test_string = open(self.test_file_path.format('basic')).read()
        converted_test_string = markdown.markdown(test_string, extensions=[CSFGExtension()])
        expected_file_string = open(self.expected_file_path.format('basic_expected')).read()
        self.assertEqual(converted_test_string, expected_file_string)

    # NTS should preprocessor tests be separate?
    def test_preprocessor_match(self):
        test_string = open(self.test_file_path.format('singleline')).read()
        self.assertTrue(CommentPreprocessor(self.md.parser).test(test_string), msg='"{}"'.format(test_string))

    def test_preprocessor_parsing(self):
        test_string = open(self.test_file_path.format('singleline')).read()
        converted_test_string = markdown.markdown(test_string, extensions=[CSFGExtension()])
        expected_file_string = open(self.expected_file_path.format('singleline_expected')).read()
        self.assertEqual(converted_test_string, expected_file_string)

    def tearDown(self):
        self.md = None
