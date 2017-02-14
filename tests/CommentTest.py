import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.CommentPreprocessor import CommentPreprocessor
from tests.BaseTestCase import BaseTestCase

class CommentTest(BaseTestCase):
    """
    Inline = single line comment .e.g. {comment hello you look lovely today}
    """

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.processor_name = 'comment'
        self.ext = Mock()
        self.ext.processor_patterns = BaseTestCase.loadProcessorPatterns(self)

    def test_no_inline_comment(self):
        test_string = self.read_test_file('no_inline_comment')
        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('no_inline_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_text_contains_the_word_comment(self):
        test_string = self.read_test_file('text_contains_the_word_comment')
        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('text_contains_the_word_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def tests_contains_inline_comment(self):
        test_string = self.read_test_file('contains_inline_comment')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_inline_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_inline_comments(self):
        #NTS not counting number of matches?
        test_string = self.read_test_file('contains_multiple_inline_comments')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_multiple_inline_comments_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_comment_contains_comment(self):
        # We expect to match the first closing '}' to enforce simple comments
        test_string = self.read_test_file('comment_contains_comment')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('comment_contains_comment_expected')
        self.assertEqual(expected_string, converted_test_string)
