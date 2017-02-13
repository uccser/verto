import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.CommentBlockProcessor import CommentBlockProcessor
from tests.BaseTestCase import BaseTestCase

class CommentBlockTest(BaseTestCase):
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
        self.tag_name = 'comment'
        self.ext = Mock()
        self.ext.tag_patterns = BaseTestCase.loadTagPatterns(self)

    def test_no_block_comment(self):
        test_string = self.read_test_file('no_block_comment')
        self.assertFalse(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('no_block_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_text_contains_the_word_comment(self):
        test_string = self.read_test_file('text_contains_the_word_comment')
        self.assertFalse(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('text_contains_the_word_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_inline_comment(self):
        test_string = self.read_test_file('contains_inline_comment')
        self.assertFalse(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_inline_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_block_comment(self):
        test_string = self.read_test_file('contains_block_comment')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_block_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_inline_then_block_comment(self):
        test_string = self.read_test_file('contains_inline_then_block_comment')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_inline_then_block_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_block_then_inline_comment(self):
        test_string = self.read_test_file('contains_block_then_inline_comment')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_block_then_inline_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_inline_then_block_then_inline_comment(self):
        test_string = self.read_test_file('contains_inline_then_block_then_inline_comment')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_inline_then_block_then_inline_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_block_comments(self):
        test_string = self.read_test_file('contains_multiple_block_comments')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_multiple_block_comments_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_block_comment_on_single_line(self):
        test_string = self.read_test_file('contains_block_comment_on_single_line')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_block_comment_on_single_line_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_block_comment_contains_another_block_comment(self):
        pass

    def test_comment_contains_inline_comment(self):
        pass
