import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.ButtonLinkBlockProcessor import ButtonLinkBlockProcessor
from kordac.tests.ProcessorTest import ProcessorTest


class ButtonLinkTest(ProcessorTest):
    """
    """

    def __init__(self, *args, **kwargs):
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'button-link'
        self.ext = Mock()
        self.ext.processor_patterns = ProcessorTest.loadProcessorPatterns(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}

    def test_no_button(self):
        test_string = self.read_test_file(self.processor_name, 'no_button.md')
        self.assertFalse(ButtonPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_button_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_button(self):
        test_string = self.read_test_file(self.processor_name, 'contains_button.md')
        self.assertTrue(ButtonPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_button_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_button(self):
        test_string = self.read_test_file(self.processor_name, 'missing_end_brace.md')
        self.assertTrue(ButtonPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'missing_end_brace_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_buttons_expected(self):
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_buttons.md')
        self.assertTrue(ButtonPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_multiple_buttons_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
