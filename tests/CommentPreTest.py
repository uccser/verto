import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.CommentPreprocessor import CommentPreprocessor
from tests.BaseTestCase import BaseTestCase

class CommentPreTest(BaseTestCase):
    """
    Inline = single line comment .e.g. {comment hello you look lovely today}
    Block = multi line comment e.g.
        {comment}
        hello,
        you look lovely today.
        {comment end}
    """

    def __init__(self, *args, **kwargs):
        """Set tag name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'commentpre'
        self.ext = Mock()
        self.ext.tag_patterns = BaseTestCase.loadTagPatterns(self)

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

    def test_contains_block_comment_on_single_line(self):
        test_string = self.read_test_file('contains_block_comment_on_single_line')
        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_block_comment_on_single_line_expected')
        self.assertEqual(expected_string, converted_test_string)

    def contains_block_comment(self):
        test_string = self.read_test_file('contains_block_comment')
        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_block_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def tests_contains_inline_comment(self):
        test_string = self.read_test_file('contains_inline_comment')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_inline_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_inline_then_block_comment(self):
        test_string = self.read_test_file('contains_inline_then_block_comment')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_inline_then_block_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_block_then_inline_comment(self):
        test_string = self.read_test_file('contains_block_then_inline_comment')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_block_then_inline_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_inline_then_block_then_inline_comment(self):
        test_string = self.read_test_file('contains_inline_then_block_then_inline_comment')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_inline_then_block_then_inline_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_inline_comments(self):
        #NTS not counting number of matches?
        test_string = self.read_test_file('contains_multiple_inline_comments')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_multiple_inline_comments')
        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_multiple_inline_comments_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_inline_comment_contains_another_inline_comment(self):
        pass

    def test_inline_comment_contains_block_comment(self):
        pass
