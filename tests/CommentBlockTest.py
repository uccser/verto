import markdown
from unittest.mock import Mock

from Kordac import Kordac
from processors.CommentBlockProcessor import CommentBlockProcessor
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

    def test_block_match_false(self):
        """
        Test no match found in string where there is no block comment.
        """
        test_string = self.read_test_file('no_block_comment')
        self.assertFalse(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('text_contains_the_word_comment')
        self.assertFalse(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_inline_comment')
        self.assertFalse(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))


    def test_block_match_true(self):
        """
        Test finds matches where block comments do exist.
        """
        test_string = self.read_test_file('contains_block_comment')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_inline_then_block_comment')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_block_then_inline_comment')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_inline_then_block_then_inline_comment')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_multiple_block_comments')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_multiple_block_comments')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

