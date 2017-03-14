import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.CommentPreprocessor import CommentPreprocessor
from kordac.tests.ProcessorTest import ProcessorTest

class BeautifyTest(ProcessorTest):
    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'beautify'

    def test_example_inline_code(self):
        test_string = self.read_test_file(self.processor_name, 'example_inline_code.md')

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_inline_code_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_example_preformatted_code(self):
        test_string = self.read_test_file(self.processor_name, 'example_preformatted_code.md')

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_preformatted_code_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_example_preformatted_code_with_extension(self):
        kordac_extension = KordacExtension([self.processor_name], {}, ['markdown.extensions.fenced_code'])
        test_string = self.read_test_file(self.processor_name, 'example_preformatted_code_with_extension.md')

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension, 'markdown.extensions.fenced_code'])
        expected_string = self.read_test_file(self.processor_name, 'example_preformatted_code_with_extension_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def text_example_mixed_code_types(self):
        test_string = self.read_test_file(self.processor_name, 'example_mixed_code_types.md')

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_mixed_code_types_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
