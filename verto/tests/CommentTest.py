import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.CommentPreprocessor import CommentPreprocessor
from verto.tests.ProcessorTest import ProcessorTest

class CommentTest(ProcessorTest):
    '''This test class checks to ensure that comments are removed
    without changing the formatting of the document.
    Inline = single line comment .e.g. {comment hello you look lovely today}
    '''

    def __init__(self, *args, **kwargs):
        '''Setup processor name for asset directory.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'comment'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)

    def test_no_inline_comment(self):
        '''Checks that normal text is unchanged.
        '''
        test_string = self.read_test_file(self.processor_name, 'no_inline_comment.md')

        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_inline_comment_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_text_contains_the_word_comment(self):
        '''Checks that words such as comment are not matched.
        '''
        test_string = self.read_test_file(self.processor_name, 'text_contains_the_word_comment.md')

        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'text_contains_the_word_comment_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def tests_contains_inline_comment(self):
        '''Tests that a simple inline comment is removed.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_inline_comment.md')

        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_inline_comment_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_inline_comments(self):
        '''Tests that multiple comments can be removed.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_inline_comments.md')

        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_multiple_inline_comments_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_comment_contains_comment(self):
        '''Tests that comments containing comments are not matched
        since they are illegal. (Because the first closing '}'
        would be matched and the second '}' would be left on the
        line invalidating the match).
        '''
        # We expect to match the first closing '}' to enforce simple comments
        test_string = self.read_test_file(self.processor_name, 'comment_contains_comment.md')

        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'comment_contains_comment_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_comment_within_block_container(self):
        '''Tests that comments are removed from containers.
        '''
        verto_extension = VertoExtension([self.processor_name, 'panel'], {})
        test_string = self.read_test_file(self.processor_name, 'comment_within_block_container.md')

        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'comment_within_block_container_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        '''Simple test for a common usage case.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_multiple(self):
        '''Simple test for a common usage case.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_multiple_usage.md')

        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_multiple_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
