import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.CommentPreprocessor import CommentPreprocessor
from verto.tests.ProcessorTest import ProcessorTest

class CommentTest(ProcessorTest):
    """
    Inline = single line comment .e.g. {comment hello you look lovely today}
    """

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'comment'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)

    def test_no_inline_comment(self):
        test_string = self.read_test_file(self.processor_name, 'no_inline_comment.md')

        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_inline_comment_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_text_contains_the_word_comment(self):
        test_string = self.read_test_file(self.processor_name, 'text_contains_the_word_comment.md')

        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'text_contains_the_word_comment_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def tests_contains_inline_comment(self):
        test_string = self.read_test_file(self.processor_name, 'contains_inline_comment.md')

        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_inline_comment_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_inline_comments(self):
        #NTS not counting number of matches?
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_inline_comments.md')

        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_multiple_inline_comments_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_comment_contains_comment(self):
        # We expect to match the first closing '}' to enforce simple comments
        test_string = self.read_test_file(self.processor_name, 'comment_contains_comment.md')

        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'comment_contains_comment_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_multiple(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_multiple_usage.md')

        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_multiple_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
