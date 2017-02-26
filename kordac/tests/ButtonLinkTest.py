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
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name), 'relative-file-link': ProcessorTest.loadJinjaTemplate(self, 'relative-file-link')}

    def test_no_button(self):
        test_string = self.read_test_file(self.processor_name, 'no_button.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False] * 7, [ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))
        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_button_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_button(self):
        test_string = self.read_test_file(self.processor_name, 'contains_button.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_button_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_missing_button(self):
        test_string = self.read_test_file(self.processor_name, 'missing_end_brace.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False], [ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'missing_end_brace_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_buttons(self):
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_buttons.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, False, True, False, False, True, False, False , True], [ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])

        expected_string = self.read_test_file(self.processor_name, 'contains_multiple_buttons_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_file_link_button(self):
        test_string = self.read_test_file(self.processor_name, 'contains_file_link_button.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True], [ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])

        expected_string = self.read_test_file(self.processor_name, 'contains_file_link_button_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_file(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_file_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_file_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_file(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_file_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_file_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        kordac_extension = KordacExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
