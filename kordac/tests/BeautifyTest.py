import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.CommentPreprocessor import CommentPreprocessor
from kordac.tests.ProcessorTest import ProcessorTest

class BeautifyTest(ProcessorTest):
    '''The major concern with beautifying is that preformatted tags and
    code blocks are unchanged. The tests here cover these cases.
    '''

    def __init__(self, *args, **kwargs):
        '''Set processor name in class for file names.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'beautify'

    def test_example_inline_code(self):
        '''Tests to see that inline code formatting is unchanged.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_inline_code.md')

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_inline_code_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_example_preformatted_code(self):
        '''Tests to ensure that preformatted tag content is unchanged.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_preformatted_code.md')

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_preformatted_code_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_example_preformatted_code_with_extension(self):
        '''Tests to ensure that the fenced_code extension does not
        change output to retain compatibility.
        '''
        kordac_extension = KordacExtension([self.processor_name], {}, ['markdown.extensions.fenced_code'])
        test_string = self.read_test_file(self.processor_name, 'example_preformatted_code_with_extension.md')

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension, 'markdown.extensions.fenced_code'])
        expected_string = self.read_test_file(self.processor_name, 'example_preformatted_code_with_extension_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def text_example_mixed_code_types(self):
        '''Tests that all types of code blocks remain unchanged when
        used together.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_mixed_code_types.md')

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_mixed_code_types_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
