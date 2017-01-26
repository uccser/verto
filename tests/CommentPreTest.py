import markdown
from unittest.mock import Mock

from Kordac import Kordac
from processors.CommentPreprocessor import CommentPreprocessor
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
        self.tag_name = 'comment'
        self.ext = Mock()
        self.ext.tag_patterns = BaseTestCase.loadTagPatterns(self)

    def test_inline_match_false(self):
        """
        Test no match found in string where there is no inline comment.
        """
        test_string = self.read_test_file('no_inline_comment')
        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('text_contains_the_word_comment')
        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_block_comment_on_single_line')
        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_block_comment')
        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))


    def test_inline_match_true(self):
        """
        Test finds matches where inline comments do exist.
        """
        test_string = self.read_test_file('contains_inline_comment')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_inline_then_block_comment')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_block_then_inline_comment')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_inline_then_block_then_inline_comment')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        test_string = self.read_test_file('contains_multiple_inline_comments')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))
        #NTS not counting number of matches?


    def test_unchanged(self):
        """
        Test text with no matches is unchanged.
        """
        test_string = self.read_test_file('no_inline_comment')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('no_inline_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

        test_string = self.read_test_file('text_contains_the_word_comment')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('text_contains_the_word_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

        test_string = self.read_test_file('contains_block_comment_on_single_line')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('contains_block_comment_on_single_line_expected')
        self.assertEqual(expected_string, converted_test_string)

        test_string = self.read_test_file('contains_block_comment')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('contains_block_comment_expected')
        self.assertEqual(expected_string, converted_test_string)


    def test_inline_removed(self):
        """
        Test text matching inline comment regex is removed.
        """
        test_string = self.read_test_file('contains_inline_comment')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('contains_inline_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

        test_string = self.read_test_file('contains_inline_then_block_comment')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('contains_inline_then_block_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

        test_string = self.read_test_file('contains_block_then_inline_comment')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('contains_block_then_inline_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

        test_string = self.read_test_file('contains_inline_then_block_then_inline_comment')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('contains_inline_then_block_then_inline_comment_expected')
        self.assertEqual(expected_string, converted_test_string)

        test_string = self.read_test_file('contains_multiple_inline_comments')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('contains_multiple_inline_comments_expected')
        self.assertEqual(expected_string, converted_test_string)


    """
    def test_match_false(self):
        test_string = self.read_test_file('fail_string')
        self.assertFalse(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_match_single_word_term_true(self):
        test_string = self.read_test_file('basic')
        self.assertTrue(CommentBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_parses_basic(self):
        test_string = self.read_test_file('basic')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_file_string = self.read_test_file('basic_expected')
        self.assertEqual(converted_test_string, expected_file_string)

    # NTS should preprocessor tests be separate?
    def test_preprocessor_match(self):
        test_string = self.read_test_file('singleline')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

    def test_preprocessor_parsing(self):
        test_string = self.read_test_file('singleline')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_file_string = self.read_test_file('singleline_expected')
        self.assertEqual(converted_test_string, expected_file_string)
    """
